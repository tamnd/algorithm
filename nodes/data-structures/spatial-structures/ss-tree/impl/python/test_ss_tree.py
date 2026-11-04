# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ss-tree/. The authors are listed in prov/G93DHE.jsonl.
import math
import random

import pytest

from ss_tree import SSTree, dist, split_entries

P = {"a": (1, 1), "b": (2, 3), "c": (3, 1), "d": (8, 8), "e": (9, 6), "f": (7, 7),
     "g": (2, 8), "h": (4, 4)}


def leaves(t):
    nodes = [t.root] if t.root.leaf else t.root.entries
    return sorted("".join(sorted(k for _, k in u.entries)) for u in nodes)


def test_page_example():
    t = SSTree(4, 2)
    for k in "abcde":
        t.insert(P[k], k)
    assert leaves(t) == ["abc", "de"]
    assert t.root.center == pytest.approx((4.6, 3.8))
    for k in "fgh":
        t.insert(P[k], k)
    assert leaves(t) == ["abch", "defg"]
    t.check_invariant()
    near = t.knn((5, 5), 3)
    assert [k for _, k in near] == ["h", "f", "b"]
    assert near[0][0] == pytest.approx(math.sqrt(2))
    assert sorted(t.ball((3, 3), 2)) == ["b", "c", "h"]
    for k in "def":
        assert t.delete(P[k], k)
        t.check_invariant()
    assert leaves(t) == ["ac", "bgh"]
    assert not t.delete((0, 0), "zz")


def test_small_and_errors():
    t = SSTree(3, 1)
    assert t.knn((0, 0), 2) == [] and t.ball((0, 0), 5) == []
    t.insert((1, 2), "x")
    assert t.knn((0, 0), 5) == [(math.sqrt(5), "x")]
    assert t.delete((1, 2), "x") and t.root is None and t.height() == -1
    with pytest.raises(ValueError):
        SSTree(1)
    with pytest.raises(ValueError):
        SSTree(4, 3)


def test_split_uses_highest_variance_axis():
    pts = [(0, 0), (0.1, 5), (0.2, 10), (0.3, 15), (0.4, 20)]
    a, b = split_entries(list(range(5)), pts, 2)
    assert (a, b) == ([0, 1], [2, 3, 4])  # split on y, not on x


def test_random_against_brute_force():
    rng = random.Random(9)
    for trial in range(500):
        d = rng.choice([1, 2, 3, 5])
        M = rng.randint(2, 7)
        t = SSTree(M, rng.randint(1, M // 2))
        pts = {}
        for k in range(rng.randint(0, 50)):
            p = tuple(float(rng.randint(0, 20)) for _ in range(d))
            pts[k] = p
            t.insert(p, k)
        for k in rng.sample(sorted(pts), len(pts) // 3):
            assert t.delete(pts.pop(k), k)
        t.check_invariant()
        assert t.n == len(pts)
        for _ in range(3):
            q = tuple(rng.uniform(-2, 22) for _ in range(d))
            r = rng.uniform(0, 8)
            assert sorted(t.ball(q, r)) == sorted(k for k, p in pts.items() if dist(q, p) <= r)
            kk = rng.randint(1, 6)
            got = [x for x, _ in t.knn(q, kk)]
            want = sorted(dist(q, p) for p in pts.values())[:kk]
            assert got == pytest.approx(want)
