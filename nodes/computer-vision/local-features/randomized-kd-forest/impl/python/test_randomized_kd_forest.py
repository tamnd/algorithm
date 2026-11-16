# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-kd-forest/. The authors are listed in prov/GS7MJP.jsonl.

import math
import random

import pytest

from randomized_kd_forest import RandomizedKDForest, brute_force


def cloud(rng, n, d):
    return [tuple(rng.random() for _ in range(d)) for _ in range(n)]


def test_build_holds_every_point_in_every_tree():
    rng = random.Random(1)
    for trees, leaf in ((1, 1), (4, 1), (3, 4)):
        f = RandomizedKDForest(cloud(rng, 200, 7), trees=trees, leaf_size=leaf, seed=trees)
        f.check_invariant()


def test_trees_differ_with_random_split_dimensions():
    rng = random.Random(2)
    f = RandomizedKDForest(cloud(rng, 300, 10), trees=4, seed=3)
    assert len({r.dim for r in f.roots}) > 1


def test_split_dimension_is_among_the_top_variances():
    rng = random.Random(3)
    pts = [tuple(rng.random() * (j + 1) for j in range(10)) for _ in range(400)]
    f = RandomizedKDForest(pts, trees=20, top_dims=3, seed=4)
    for r in f.roots:
        assert r.dim in (7, 8, 9)


def test_random_inserts_and_queries_against_brute_force():
    rng = random.Random(4)
    for d in (2, 5, 9):
        f = RandomizedKDForest(cloud(rng, 40, d), trees=3, leaf_size=2, seed=d)
        for step in range(150):
            if rng.random() < 0.6:
                f.insert(tuple(rng.random() for _ in range(d)))
            else:
                q = tuple(rng.uniform(-0.2, 1.2) for _ in range(d))
                k = rng.choice((1, 2, 3))
                got, exact, evals = f.search(q, k)
                assert exact and evals <= len(f.points)
                assert [g[0] for g in got] == [w[0] for w in brute_force(f.points, q, k)]
        f.check_invariant()


def test_many_small_forests_with_ties_against_brute_force():
    rng = random.Random(12)
    for trial in range(600):
        d = rng.randint(1, 3)
        pts = [tuple(float(rng.randint(0, 4)) for _ in range(d)) for _ in range(rng.randint(1, 12))]
        f = RandomizedKDForest(pts, trees=rng.randint(1, 3), top_dims=rng.randint(1, 3),
                               leaf_size=rng.randint(1, 3), seed=trial)
        q = tuple(rng.randint(-1, 5) + rng.choice((0.0, 0.5)) for _ in range(d))
        k = rng.randint(1, 3)
        got, exact, _ = f.search(q, k)
        assert exact
        assert [g[0] for g in got] == [w[0] for w in brute_force(f.points, q, k)]


def test_insert_into_an_empty_forest():
    f = RandomizedKDForest([], trees=2, seed=0, dim=3)
    rng = random.Random(5)
    for _ in range(60):
        f.insert(tuple(rng.random() for _ in range(3)))
    f.check_invariant()
    q = (0.5, 0.5, 0.5)
    assert [g[0] for g in f.search(q, 4)[0]] == [w[0] for w in brute_force(f.points, q, 4)]


def test_each_point_is_checked_at_most_once():
    rng = random.Random(6)
    pts = cloud(rng, 150, 6)
    f = RandomizedKDForest(pts, trees=8, seed=7)
    for _ in range(20):
        q = tuple(rng.random() for _ in range(6))
        _, _, evals = f.search(q, 1)
        assert evals <= len(pts)
        _, _, evals = f.search(q, 1, checks=30)
        assert evals <= 30 + f.leaf_size


def test_more_checks_never_give_a_worse_answer_and_exact_flag_is_right():
    rng = random.Random(8)
    pts = cloud(rng, 500, 12)
    f = RandomizedKDForest(pts, trees=4, seed=9)
    for _ in range(15):
        q = tuple(rng.random() for _ in range(12))
        truth = brute_force(pts, q, 2)
        last = math.inf
        for c in (1, 5, 20, 80, 320):
            got, exact, _ = f.search(q, 2, checks=c)
            assert got[0][0] <= last
            last = got[0][0]
            if exact:
                assert [g[0] for g in got] == [w[0] for w in truth]


def test_duplicate_points_stay_in_one_leaf():
    f = RandomizedKDForest([(1.0, 2.0)] * 10 + [(3.0, 4.0)], trees=2, seed=1)
    f.check_invariant()
    got, exact, _ = f.search((1.0, 2.1), 3)
    assert exact and [round(g[0], 12) for g in got] == [0.01, 0.01, 0.01]


def test_bad_parameters():
    with pytest.raises(ValueError):
        RandomizedKDForest([(0.0,)], trees=0)
