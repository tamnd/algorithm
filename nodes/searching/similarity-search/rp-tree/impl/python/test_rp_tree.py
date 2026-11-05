# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rp-tree/. The authors are listed in prov/58J4K4.jsonl.

import math
import random

from rp_tree import RPTree, _dot

P = [(0, 0), (1, 1), (2, 1), (3, 2), (4, 4), (5, 4), (6, 5), (7, 7)]


def brute(points, q, k):
    return sorted((math.dist(q, p), i) for i, p in enumerate(points))[:k]


def check_structure(tree, n):
    leaves = tree.leaves()
    assert sorted(i for leaf in leaves for i in leaf) == list(range(n))

    def walk(node, idx):
        if node.items is not None:
            assert sorted(node.items) == sorted(idx)
            return
        assert abs(_dot(node.v, node.v) - 1) < 1e-9
        left = [i for i in idx if _dot(node.v, tree.points[i]) <= node.t]
        right = [i for i in idx if _dot(node.v, tree.points[i]) > node.t]
        assert left and right and len(left) == (len(idx) + 1) // 2
        walk(node.left, left)
        walk(node.right, right)

    walk(tree.root, list(range(n)))


def test_example() -> None:
    tree = RPTree(P, 2, directions=[(0.6, 0.8), (0.8, -0.6), (0, 1)])
    assert tree.leaves() == [[0, 1], [2, 3], [4, 5], [6, 7]]
    assert math.isclose(tree.root.t, 3.4) and math.isclose(tree.root.left.t, 0.2) and tree.root.right.t == 4
    assert tree.query((4.5, 3), 1) == [(math.sqrt(1.25), 4)] and tree.evaluations == 4
    assert tree.query((4.5, 3), 2) == [(math.sqrt(1.25), 4), (math.sqrt(1.25), 5)] and tree.evaluations == 4
    assert tree.leaf_of((4.5, 3)) == [4, 5]
    assert tree.depth() == 2


def test_edges() -> None:
    assert RPTree([], 2).query((0, 0), 3) == []
    one = RPTree([(1, 2)], 1)
    assert one.query((0, 0), 5) == [(math.sqrt(5), 0)]
    same = RPTree([(1, 1)] * 5, 1)
    assert same.leaves() == [[0, 1, 2, 3, 4]]
    assert same.query((1, 1), 2) == [(0.0, 0), (0.0, 1)]
    assert RPTree(P, 3).query((0, 0), 0) == []
    try:
        RPTree(P, 0)
        raise AssertionError("leaf_size 0 accepted")
    except ValueError:
        pass


def test_random_against_brute_force() -> None:
    rng = random.Random(2008)
    for _ in range(500):
        n = rng.randint(1, 60)
        dim = rng.randint(1, 5)
        if rng.random() < 0.2:
            pts = [tuple(float(rng.randint(0, 3)) for _ in range(dim)) for _ in range(n)]
        else:
            pts = [tuple(rng.uniform(-5, 5) for _ in range(dim)) for _ in range(n)]
        n0 = rng.randint(1, 6)
        tree = RPTree(pts, n0, seed=rng.randrange(10**6))
        if len(set(pts)) == n:
            check_structure(tree, n)
            assert all(len(leaf) <= n0 for leaf in tree.leaves())
            assert tree.depth() == (0 if n <= n0 else math.ceil(math.log2(n / n0) - 1e-12))
        else:
            assert sorted(i for leaf in tree.leaves() for i in leaf) == list(range(n))
        for _ in range(3):
            q = tuple(rng.uniform(-6, 6) for _ in range(dim))
            k = rng.randint(1, n + 1)
            got = tree.query(q, k)
            want = brute(pts, q, k)
            assert [round(x, 9) for x, _ in got] == [round(x, 9) for x, _ in want]
            assert tree.evaluations <= n
            assert tree.leaf_of(q) in tree.leaves()
