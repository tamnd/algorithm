# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-bin-first-search/. The authors are listed in prov/THZZ2G.jsonl.

import math
import random

from best_bin_first_search import bbf_search, brute_force, build, sqdist


def cloud(rng, n, d):
    return [tuple(rng.random() for _ in range(d)) for _ in range(n)]


def leaves(node):
    if node.dim < 0:
        return [node]
    return leaves(node.left) + leaves(node.right)


def test_tree_holds_every_point_once_and_respects_splits():
    rng = random.Random(1)
    for leaf_size in (1, 3):
        pts = cloud(rng, 150, 4)
        root = build(pts, leaf_size)
        ids = sorted(i for leaf in leaves(root) for i in leaf.ids)
        assert ids == list(range(len(pts)))

        def check(node, lo, hi):
            if node.dim < 0:
                assert len(node.ids) <= leaf_size
                for i in node.ids:
                    for t in range(4):
                        assert lo[t] <= pts[i][t] <= hi[t]
                return
            hl = list(hi)
            hl[node.dim] = node.split
            check(node.left, lo, hl)
            ll = list(lo)
            ll[node.dim] = node.split
            check(node.right, ll, hi)

        check(root, [-math.inf] * 4, [math.inf] * 4)


def test_unlimited_search_equals_brute_force():
    rng = random.Random(2)
    for d in (1, 2, 3, 5, 8):
        pts = cloud(rng, 120, d)
        root = build(pts, rng.choice((1, 2, 4)))
        for _ in range(25):
            q = tuple(rng.uniform(-0.2, 1.2) for _ in range(d))
            for k in (1, 2, 5):
                got, exact = bbf_search(root, pts, q, k)
                want = brute_force(pts, q, k)
                assert exact
                assert [g[0] for g in got] == [w[0] for w in want]


def test_many_small_inputs_with_ties_against_brute_force():
    rng = random.Random(9)
    for _ in range(600):
        d = rng.randint(1, 3)
        pts = [tuple(rng.randint(0, 4) for _ in range(d)) for _ in range(rng.randint(1, 12))]
        root = build(pts, rng.choice((1, 2, 3)))
        q = tuple(rng.randint(-1, 5) + rng.choice((0.0, 0.5)) for _ in range(d))
        k = rng.randint(1, 3)
        got, exact = bbf_search(root, pts, q, k)
        assert exact
        assert [g[0] for g in got] == [w[0] for w in brute_force(pts, q, k)]
        got1, _ = bbf_search(root, pts, q, k, max_leaves=1)
        assert all(sqdist(pts[i], q) == g for g, i in got1)


def test_exact_flag_is_never_wrong():
    rng = random.Random(3)
    pts = cloud(rng, 300, 6)
    root = build(pts)
    for _ in range(60):
        q = tuple(rng.random() for _ in range(6))
        for e in (1, 3, 10, 40):
            got, exact = bbf_search(root, pts, q, 2, max_leaves=e)
            if exact:
                assert [g[0] for g in got] == [w[0] for w in brute_force(pts, q, 2)]


def test_bin_distances_are_lower_bounds_and_do_not_decrease():
    rng = random.Random(4)
    pts = cloud(rng, 200, 5)
    root = build(pts, 2)
    for _ in range(30):
        q = tuple(rng.uniform(-0.5, 1.5) for _ in range(5))
        log = []
        bbf_search(root, pts, q, 1, log=log)
        prev = -1.0
        for b, ids in log:
            assert b >= prev - 1e-12
            prev = b
            for i in ids:
                assert sqdist(pts[i], q) >= b - 1e-12


def test_more_leaves_never_give_a_worse_answer():
    rng = random.Random(5)
    pts = cloud(rng, 400, 10)
    root = build(pts)
    for _ in range(20):
        q = tuple(rng.random() for _ in range(10))
        last = math.inf
        for e in range(1, 60, 3):
            got, _ = bbf_search(root, pts, q, 1, max_leaves=e)
            assert got[0][0] <= last
            last = got[0][0]


def test_one_leaf_is_the_plain_descent():
    rng = random.Random(6)
    pts = cloud(rng, 64, 3)
    root = build(pts)
    for _ in range(20):
        q = tuple(rng.random() for _ in range(3))
        node = root
        while node.dim >= 0:
            node = node.left if q[node.dim] < node.split else node.right
        got, _ = bbf_search(root, pts, q, 1, max_leaves=1)
        assert got == [(sqdist(pts[node.ids[0]], q), node.ids[0])]


def test_duplicates_and_empty_input():
    pts = [(0.5, 0.5)] * 5 + [(0.0, 1.0)]
    root = build(pts)
    got, exact = bbf_search(root, pts, (0.5, 0.4), 3)
    assert exact and [g[0] for g in got] == [w[0] for w in brute_force(pts, (0.5, 0.4), 3)]
    assert bbf_search(None, [], (0.0,), 1) == ([], True)
