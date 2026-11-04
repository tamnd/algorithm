# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tango-tree/. The authors are listed in prov/MK70WC.jsonl.

import math
import random

import pytest

from tango_tree import TangoTree


def interleave_bound(n, seq):
    """Wilber's interleave bound on the reference tree with root (1 + n) // 2."""
    total = 0
    stack = [(1, n)]
    while stack:
        a, b = stack.pop()
        if a > b:
            continue
        y = (a + b) // 2
        labels = ["L" if x <= y else "R" for x in seq if a <= x <= b]
        total += sum(1 for s, t in zip(labels, labels[1:]) if s != t)
        stack.append((a, y - 1))
        stack.append((y + 1, b))
    return total


def test_small_example() -> None:
    t = TangoTree(7)
    assert t.root == 4
    t.check_invariant()
    assert t.access(1) == (3, 0)
    assert sorted(t.paths()) == [[1, 2, 4], [3], [5], [6], [7]]
    assert t.access(3) == (2, 1)
    assert sorted(t.paths()) == [[1], [2, 3, 4], [5], [6], [7]]
    assert t.access(6) == (2, 1)
    assert sorted(t.paths()) == [[1], [2, 3], [4, 5, 6], [7]]
    t.check_invariant()
    with pytest.raises(KeyError):
        t.access(8)


def test_switches_equal_interleave_bound() -> None:
    rng = random.Random(20251104)
    for case in range(600):
        n = rng.randrange(1, 70)
        t = TangoTree(n)
        seq = []
        visited_total = 0
        for _ in range(rng.randrange(1, 60)):
            if seq and rng.random() < 0.3:
                x = min(n, max(1, seq[-1] + rng.choice([-1, 1])))
            else:
                x = rng.randrange(1, n + 1)
            seq.append(x)
            visited, k = t.access(x)
            assert 0 <= k <= visited
            visited_total += visited
        t.check_invariant()
        # each path change below the top is an L-R switch or a first choice, which happens once per node
        assert visited_total <= t.lr_switches + len(seq) + n
        assert t.lr_switches == interleave_bound(n, seq)


def test_comparisons_are_log_log_per_path() -> None:
    rng = random.Random(5)
    n = 2 ** 12 - 1
    t = TangoTree(n)
    visited_total = 0
    for _ in range(3000):
        before = t.comparisons
        v, _ = t.access(rng.randrange(1, n + 1))
        visited_total += v
        # each path has at most lg(n + 1) = 12 nodes, so a binary search makes at most 4 comparisons
        assert t.comparisons - before <= v * (math.ceil(math.log2(13)))
    t.check_invariant()
    assert visited_total <= t.lr_switches + 3000 + n


def test_bit_reversal() -> None:
    k = 8
    n = 2 ** k - 1
    seq = [int(format(i, "0%db" % k)[::-1], 2) for i in range(1, 2 ** k)]
    seq = [x for x in seq if x != 0] * 3
    t = TangoTree(n)
    for x in seq:
        t.access(x)
    assert t.lr_switches == interleave_bound(n, seq)
