# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/li-chao-tree/. The authors are listed in prov/E3PVVE.jsonl.

import random

import pytest

from li_chao_tree import LiChaoTree


def test_example() -> None:
    t = LiChaoTree(0, 8)
    for a, b in [(0, 5), (1, 0), (-1, 7), (-2, 12)]:
        t.insert(a, b)
    assert t.line[0] == (-1, 7)
    assert t.line[t.left[0]] == (1, 0)
    assert t.line[t.right[0]] == (-2, 12)
    assert len(t.line) == 3
    assert t.query(2) == 2 and t.query(5) == 2 and t.query(7) == -2
    lines = [(0, 5), (1, 0), (-1, 7), (-2, 12)]
    for x in range(8):
        assert t.query(x) == min(a * x + b for a, b in lines)
    t.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        LiChaoTree(3, 3)
    t = LiChaoTree(-5, -4)
    assert t.query(-5) is None
    t.insert(2, 1)
    t.insert(3, 0)
    assert t.query(-5) == -15
    with pytest.raises(IndexError):
        t.query(-4)
    big = LiChaoTree(-(10**9), 10**9)
    big.insert(10**9, 10**18)
    big.insert(-(10**9), 10**18)
    assert big.query(0) == 10**18
    assert big.query(-(10**9)) == 0


def test_random_against_brute_force() -> None:
    rng = random.Random(2013)
    for _ in range(500):
        lo = rng.randint(-30, 30)
        hi = lo + rng.randint(1, 40)
        t = LiChaoTree(lo, hi)
        lines: list[tuple[int, int]] = []
        for _ in range(rng.randint(0, 25)):
            if rng.random() < 0.5:
                a, b = rng.randint(-6, 6), rng.randint(-50, 50)
                t.insert(a, b)
                lines.append((a, b))
            else:
                x = rng.randrange(lo, hi)
                want = min((a * x + b for a, b in lines), default=None)
                assert t.query(x) == want
        assert len(t.line) <= max(1, len(lines))
        t.check_invariant()
