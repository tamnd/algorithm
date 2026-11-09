# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beyer-hedetniemi/. The authors are listed in prov/VB34EV.jsonl.

import itertools
import random

import pytest

from beyer_hedetniemi import rooted_trees

# OEIS A000081, a_0 .. a_14.
A000081 = [0, 1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842, 4766, 12486, 32973]


def otter(m: int) -> list[int]:
    a = [0, 1]
    for n in range(1, m):
        s = 0
        for k in range(1, n + 1):
            s += sum(d * a[d] for d in range(1, k + 1) if k % d == 0) * a[n - k + 1]
        a.append(s // n)
    return a


def level_sequences(n: int) -> list[tuple[int, ...]]:
    """All ordered rooted trees with n nodes, as level sequences."""
    if n == 0:
        return []
    out = []
    for tail in itertools.product(range(1, n), repeat=n - 1):
        seq = (0,) + tail
        if all(seq[i + 1] <= seq[i] + 1 for i in range(n - 1)):
            out.append(seq)
    return out


def canonical(seq: tuple[int, ...]) -> tuple[int, ...]:
    """Sort the child subtrees of every node in decreasing order."""

    def build(i: int) -> tuple[tuple[int, ...], int]:
        d = seq[i]
        j = i + 1
        kids = []
        while j < len(seq) and seq[j] > d:
            block, j = build(j)
            kids.append(block)
        kids.sort(reverse=True)
        return (d,) + tuple(x for b in kids for x in b), j

    return build(0)[0]


def parents_of(levels: tuple[int, ...]) -> tuple[int, ...]:
    out = []
    for i, x in enumerate(levels):
        j = i - 1
        while j >= 0 and levels[j] != x - 1:
            j -= 1
        out.append(j + 1)
    return tuple(out)


def test_small() -> None:
    assert list(rooted_trees(0)) == []
    assert list(rooted_trees(1)) == [(0,)]
    assert list(rooted_trees(2)) == [(0, 1)]
    assert list(rooted_trees(3)) == [(0, 1, 2), (0, 1, 1)]
    assert list(rooted_trees(4)) == [(0, 1, 2, 3), (0, 1, 2, 2), (0, 1, 2, 1), (0, 1, 1, 1)]
    with pytest.raises(ValueError):
        list(rooted_trees(-1))


def test_example_n5() -> None:
    got = ["".join(map(str, t)) for t in rooted_trees(5)]
    assert got == ["01234", "01233", "01232", "01231", "01222", "01221", "01212", "01211", "01111"]


def test_brute_force() -> None:
    for n in range(0, 9):
        expected = sorted({canonical(s) for s in level_sequences(n)}, reverse=True)
        assert list(rooted_trees(n)) == expected


def test_counts() -> None:
    a = otter(14)
    assert a == A000081
    for n in range(0, 15):
        assert sum(1 for _ in rooted_trees(n)) == a[n]


def test_parent_array() -> None:
    for n in range(1, 12):
        for levels, par in rooted_trees(n, parents=True):
            assert par == parents_of(levels)


def test_suffix_identity() -> None:
    # Sum over all trees of n - p + 1, with p the last entry > 1 (p = 1 for the star),
    # equals a_1 + ... + a_n; this is the work of the successor without the shortcut.
    a = A000081
    for n in range(1, 14):
        total = 0
        for t in rooted_trees(n):
            p = max((i + 1 for i in range(n) if t[i] > 1), default=1)
            total += n - p + 1
        assert total == sum(a[1 : n + 1])


def test_random_trees_are_listed() -> None:
    rng = random.Random(7)
    n = 11
    listed = set(rooted_trees(n))
    assert len(listed) == A000081[n]
    for _ in range(300):
        seq = [0]
        for _ in range(n - 1):
            seq.append(rng.randint(1, seq[-1] + 1))
        assert canonical(tuple(seq)) in listed
