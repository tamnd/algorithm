# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ball-tree/. The authors are listed in prov/DT55WY.jsonl.

import math
import random

from ball_tree import BallTree, euclidean

PTS = [(1, 1), (2, 3), (3, 1), (6, 5), (7, 7), (8, 4), (2, 2), (7, 5)]


def check(tree, t, depth=0):
    ids = t.points if t.points is not None else collect(t)
    assert all(tree.dist(tree.points[t.center], tree.points[i]) <= t.radius + 1e-12 for i in ids)
    if t.points is None:
        a, b = collect(t.left), collect(t.right)
        assert abs(len(a) - len(b)) <= 1
        return max(check(tree, t.left, depth + 1), check(tree, t.right, depth + 1))
    assert len(t.points) <= tree.b
    return depth + 1


def collect(t):
    if t.points is not None:
        return list(t.points)
    return collect(t.left) + collect(t.right)


def test_example() -> None:
    tree = BallTree(PTS, leaf_size=2)
    assert tree.root.center == 0
    assert math.isclose(tree.root.radius, math.sqrt(72))
    assert sorted(collect(tree.root.left)) == [3, 4, 5, 7]
    assert check(tree, tree.root) == 3
    assert tree.knn((5, 4), 2) == [(math.sqrt(2), 3), (math.sqrt(5), 7)]
    assert tree.knn((6, 6), 1) == [(1.0, 3)]


def test_random_against_brute_force() -> None:
    rng = random.Random(8)
    for _ in range(500):
        d = rng.randint(1, 5)
        n = rng.randint(1, 40)
        pts = [tuple(float(rng.randint(-6, 6)) for _ in range(d)) for _ in range(n)]
        tree = BallTree(pts, leaf_size=rng.randint(1, 4))
        h = check(tree, tree.root)
        assert h <= math.ceil(math.log2(max(1, n))) + 1
        q = tuple(rng.uniform(-7, 7) for _ in range(d))
        k = rng.randint(1, 6)
        want = sorted(euclidean(q, p) for p in pts)[:k]
        got = tree.knn(q, k)
        assert [a for a, _ in got] == want
        assert all(euclidean(q, pts[i]) == a for a, i in got)
        r = rng.uniform(0, 8)
        assert sorted(tree.range(q, r)) == [i for i, p in enumerate(pts) if euclidean(q, p) <= r]


def test_string_metric() -> None:
    rng = random.Random(5)
    words = ["".join(rng.choice("ab") for _ in range(8)) for _ in range(60)]
    ham = lambda x, y: sum(a != b for a, b in zip(x, y))
    tree = BallTree(words, dist=ham, leaf_size=3)
    for _ in range(100):
        q = "".join(rng.choice("ab") for _ in range(8))
        assert [a for a, _ in tree.knn(q, 3)] == sorted(ham(q, w) for w in words)[:3]
