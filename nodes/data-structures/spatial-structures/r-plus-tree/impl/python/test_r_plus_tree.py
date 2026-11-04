# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-plus-tree/. The authors are listed in prov/SFMMBA.jsonl.
import random

import pytest

from r_plus_tree import RPlusTree, choose_cut, intersects

E = {"a": (0, 0, 2, 2), "b": (1, 5, 3, 7), "c": (6, 0, 8, 1), "d": (7, 6, 9, 9),
     "e": (2, 1, 3, 3), "f": (6, 7, 7, 8), "g": (1, 3, 2, 4), "h": (3, 6, 4, 8),
     "i": (2, 2, 7, 4)}


def leaves(t):
    return sorted((u.region, "".join(sorted(x for x, _ in u.items))) for u in t.leaves())


def test_page_example():
    inf = float("inf")
    t = RPlusTree(4)
    for k in "abcde":
        t.insert(k, E[k])
    assert leaves(t) == [((-inf, -inf, 6, inf), "abe"), ((6, -inf, inf, inf), "cd")]
    for k in "fgh":
        t.insert(k, E[k])
    assert leaves(t) == [((-inf, -inf, 6, 5), "aeg"), ((-inf, 5, 6, inf), "bh"),
                         ((6, -inf, inf, inf), "cdf")]
    t.insert("i", E["i"])
    assert leaves(t) == [((-inf, -inf, 6, 5), "aegi"), ((-inf, 5, 6, inf), "bh"),
                         ((6, -inf, inf, inf), "cdfi")]
    assert t.copies() == 10 and t.n == 9
    t.check_invariant(E)
    assert sorted(t.search((2.5, 2.5, 7, 7))) == list("bdefhi")
    assert t.search((4.5, 4.5, 5.5, 5.5)) == []
    assert sorted(t.search((6.5, 2.5, 6.6, 2.6))) == ["i"]
    assert t.delete("i", E["i"])
    assert t.copies() == 8
    assert not t.delete("i", E["i"])


def test_empty_and_errors():
    t = RPlusTree(2)
    assert t.search((0, 0, 1, 1)) == []
    with pytest.raises(ValueError):
        RPlusTree(1)
    with pytest.raises(ValueError):
        t.insert("x", (1, 0, 0, 1))


def test_same_point_overflows():
    t = RPlusTree(2)
    objs = {k: (1, 1, 1, 1) for k in range(5)}
    for k, r in objs.items():
        t.insert(k, r)
    assert len(t.leaves()) == 1 and t.copies() == 5  # no cut can help
    assert sorted(t.search((0, 0, 2, 2))) == list(range(5))
    t.check_invariant(objs)


def brute(objs, q):
    return sorted(k for k, r in objs.items() if intersects(q, r))


def rand_rect(rng, size):
    x, y = rng.randint(0, 30), rng.randint(0, 30)
    return (x, y, x + rng.randint(0, size), y + rng.randint(0, size))


def test_random_against_brute_force():
    rng = random.Random(7)
    for trial in range(600):
        M = rng.randint(2, 6)
        t = RPlusTree(M)
        objs = {}
        for k in range(rng.randint(0, 40)):
            r = rand_rect(rng, rng.choice([0, 3, 8]))
            t.insert(k, r)
            objs[k] = r
        for k in rng.sample(sorted(objs), len(objs) // 3):
            assert t.delete(k, objs.pop(k))
        t.check_invariant(objs)
        assert t.n == len(objs)
        stack = [t.root]
        while stack:  # a node stays over full only if no cut helps
            u = stack.pop()
            if u.size() > M:
                assert u.leaf and choose_cut(u) is None
            if not u.leaf:
                stack.extend(u.children)
        for _ in range(5):
            q = rand_rect(rng, 12)
            res = t.search(q)
            assert len(res) == len(set(res))
            assert sorted(res) == brute(objs, q)
