# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vocabulary-tree/. The authors are listed in prov/3BRV2P.jsonl.

import math
import random

from vocabulary_tree import VocabularyTree, build, nearest, node, sq_dist


def example_tree():
    leaf = lambda c: node([c])
    root = node([3.5], [node([-1], [leaf(-6), leaf(4)]), node([10], [leaf(8), leaf(12)])])
    return VocabularyTree(root)


IMAGES = {"a": [[-6], [4]], "b": [[8], [12], [12]], "c": [[4], [9]]}


def depth_and_branching(nd, depth=0):
    if not nd["children"]:
        return depth, 0
    sub = [depth_and_branching(c, depth + 1) for c in nd["children"]]
    return max(s[0] for s in sub), max([len(nd["children"])] + [s[1] for s in sub])


def brute_vector(T, descriptors):
    n = {}
    for x in descriptors:
        for i in T.path(x):
            n[i] = n.get(i, 0) + 1
    v = [n.get(i, 0) * T.weights.get(i, 0.0) for i in range(len(T.nodes))]
    s = sum(v)
    return [t / s for t in v] if s > 0 else v


def test_greedy_descent_misses_the_nearest_leaf():
    T = example_tree()
    assert T.path([4.6]) == [0, 4, 5]
    assert T.leaves[T.quantize([4.6])]["center"] == [8]
    leaf_centers = [lf["center"] for lf in T.leaves]
    assert leaf_centers[nearest([4.6], leaf_centers)] == [4]


def test_example_of_the_page():
    T = example_tree()
    T.index(IMAGES)
    assert T.weights[0] == 0.0
    assert abs(T.weights[1] - math.log(1.5)) < 1e-12 and abs(T.weights[2] - math.log(3)) < 1e-12
    assert abs(T.inverted[2]["a"] - math.log(3) / (3 * math.log(1.5) + math.log(3))) < 1e-12
    ranked = T.query([[3], [5]])
    assert [d for _, d in ranked] == ["c", "a", "b"]
    assert abs(ranked[0][0]) < 1e-12
    assert abs(ranked[1][0] - 1.1497) < 1e-4 and abs(ranked[2][0] - 1.2877) < 1e-4


def test_inverted_files_equal_brute_force_l1():
    rng = random.Random(1)
    train = [[rng.uniform(0, 10), rng.uniform(0, 10)] for _ in range(300)]
    T = VocabularyTree(build(train, 3, 3, seed=1))
    images = {d: [[rng.uniform(0, 10), rng.uniform(0, 10)] for _ in range(rng.randint(1, 15))] for d in range(12)}
    T.index(images)
    for _ in range(5):
        q = [[rng.uniform(0, 10), rng.uniform(0, 10)] for _ in range(rng.randint(1, 15))]
        qv = brute_vector(T, q)
        s = T.scores(q)
        for d, xs in images.items():
            dv = brute_vector(T, xs)
            l1 = sum(abs(a - b) for a, b in zip(qv, dv))
            inter = sum(min(a, b) for a, b in zip(qv, dv))
            assert abs(s[d] - l1) < 1e-9
            assert abs(s[d] - (2 - 2 * inter)) < 1e-9 or sum(qv) == 0 or sum(dv) == 0


def test_build_respects_k_and_L_and_partitions():
    rng = random.Random(2)
    train = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(400)]
    for k, L in ((2, 4), (3, 3), (5, 2)):
        T = VocabularyTree(build(train, k, L, seed=3))
        depth, branch = depth_and_branching(T.root)
        assert depth <= L and branch <= k
        assert len(T.leaves) <= k ** L
        for x in train[:50]:
            p = T.path(x)
            assert len(p) <= L + 1 and not T.nodes[p[-1]]["children"]


def test_query_with_own_descriptors_scores_zero():
    rng = random.Random(4)
    train = [[rng.uniform(0, 5)] for _ in range(200)]
    T = VocabularyTree(build(train, 4, 3, seed=5))
    images = {d: [[rng.uniform(0, 5)] for _ in range(8)] for d in range(10)}
    T.index(images)
    for d in (0, 3, 7):
        assert abs(T.scores(images[d])[d]) < 1e-12


def test_greedy_leaf_is_nearest_child_at_each_step():
    rng = random.Random(6)
    train = [[rng.uniform(0, 1), rng.uniform(0, 1)] for _ in range(200)]
    T = VocabularyTree(build(train, 3, 3, seed=7))
    for _ in range(100):
        x = [rng.uniform(0, 1), rng.uniform(0, 1)]
        p = T.path(x)
        for a, b in zip(p, p[1:]):
            kids = T.nodes[a]["children"]
            assert min(sq_dist(x, c["center"]) for c in kids) == sq_dist(x, T.nodes[b]["center"])
