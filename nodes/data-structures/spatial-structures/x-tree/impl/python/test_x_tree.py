# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/x-tree/. The authors are listed in prov/19MBBA.jsonl.
import random

import pytest

from x_tree import XTree, intersects, mindist, overlap_ratio


def test_empty_and_errors():
    t = XTree(4)
    assert t.search(((0, 0), (1, 1))) == []
    assert t.knn((0, 0), 3) == []
    assert not t.delete(1, ((0, 0), (0, 0)))
    t.check_invariant()
    with pytest.raises(ValueError):
        XTree(1)
    with pytest.raises(ValueError):
        XTree(4, 3)
    with pytest.raises(ValueError):
        t.insert(1, ((1, 1), (0, 0)))


def test_overlap_ratio():
    a = ((0, 0), (2, 2))
    b = ((1, 1), (3, 3))
    assert overlap_ratio(a, b) == pytest.approx(1 / 7)
    assert overlap_ratio(a, ((5, 5), (6, 6))) == 0.0
    assert overlap_ratio(a, a) == 1.0


def test_same_point_many_times():
    t = XTree(3)
    for i in range(40):
        t.insert(i, ((1, 1), (1, 1)))
        t.check_invariant()
    assert sorted(t.search(((0, 0), (2, 2)))) == list(range(40))
    for i in range(40):
        assert t.delete(i, ((1, 1), (1, 1)))
        t.check_invariant()
    assert t.n == 0


def _brute_knn(live, q, k):
    return sorted(round(mindist(q, r), 9) for r in live.values())[:k]


def test_random_against_brute_force():
    with_super = 0
    for trial in range(600):
        rnd = random.Random(trial)
        d = rnd.choice([1, 2, 3, 4])
        M = rnd.choice([2, 3, 4, 5, 8])
        t = XTree(M)
        live = {}
        nxt = 0
        for _ in range(rnd.randint(0, 70)):
            if live and rnd.random() < 0.25:
                j = rnd.choice(list(live))
                assert t.delete(j, live.pop(j))
            else:
                lo = tuple(float(rnd.randint(0, 20)) for _ in range(d))
                w = rnd.choice([0, 1, 4, 12])
                hi = tuple(x + rnd.randint(0, w) for x in lo)
                t.insert(nxt, (lo, hi))
                live[nxt] = (lo, hi)
                nxt += 1
        t.check_invariant()
        with_super += bool(t.supernodes())
        assert t.n == len(live)
        for _ in range(3):
            lo = tuple(float(rnd.randint(-2, 20)) for _ in range(d))
            hi = tuple(x + rnd.randint(0, 10) for x in lo)
            q = (lo, hi)
            assert sorted(t.search(q)) == sorted(j for j, r in live.items() if intersects(r, q))
            p = tuple(rnd.uniform(-5, 25) for _ in range(d))
            k = rnd.randint(1, 6)
            got = t.knn(p, k)
            assert [round(x, 9) for x, _ in got] == _brute_knn(live, p, k)
            assert all(round(mindist(p, live[j]), 9) == round(x, 9) for x, j in got)
        assert not t.delete(-1, ((0.0,) * d, (0.0,) * d))
    assert with_super > 0


EXAMPLE = [((3, 0), (8, 3)), ((8, 3), (13, 3)), ((2, 3), (7, 7)), ((9, 5), (9, 7)),
           ((9, 6), (12, 7)), ((9, 3), (13, 5)), ((7, 1), (10, 6))]


def _leaves(t):
    return [sorted("abcdefg"[o] for _, o in leaf.entries) for leaf in t.root.entries]


def test_page_example():
    t = XTree(3)
    for i, r in enumerate(EXAMPLE[:4]):
        t.insert(i, r)
    assert _leaves(t) == [["a", "b"], ["c", "d"]]
    assert [sorted(u.hist) for u in t.root.entries] == [[1], [1]]
    t.insert(4, EXAMPLE[4])
    t.insert(5, EXAMPLE[5])
    assert _leaves(t) == [["a", "b"], ["c"], ["d", "e", "f"]]
    assert t.supernodes() == []
    c = t.root.entries[1]
    assert c.rect == ((2.0, 3.0), (7.0, 7.0))
    rest = ((3.0, 0.0), (13.0, 7.0))
    assert overlap_ratio(c.rect, rest) == pytest.approx(16 / 74)
    t.insert(6, EXAMPLE[6])
    t.check_invariant()
    assert t.root.blocks == 2 and t.supernodes() == [t.root]
    assert t.height() == 1
    assert _leaves(t) == [["a", "b"], ["c"], ["g"], ["d", "e", "f"]]
    assert overlap_ratio(((3, 0), (13, 6)), ((2, 3), (13, 7))) == pytest.approx(30 / 74)
    assert [(round(x, 9), o) for x, o in t.knn((10, 4), 3)] == [(0.0, 6), (0.0, 5), (1.0, 1)]
    assert sorted(t.search(((8, 4), (9, 6)))) == [3, 4, 5, 6]
