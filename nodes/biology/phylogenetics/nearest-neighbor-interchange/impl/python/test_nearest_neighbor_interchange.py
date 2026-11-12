# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-interchange/. The authors are listed in prov/57633W.jsonl.

import itertools
import random

from nearest_neighbor_interchange import (
    all_trees,
    leaf_count,
    nni_hill_climb,
    nni_neighbors,
    topology,
)


def double_factorial(k):
    r = 1
    while k > 1:
        r *= k
        k -= 2
    return r


def brute_parsimony(tree, n, columns):
    """Small parsimony by brute force over all internal labelings (oracle for Fitch)."""
    internal = sorted(v for v in tree if v >= n)
    edges = [(x, y) for x in tree for y in tree[x] if x < y]
    total = 0
    for col in columns:
        best = None
        for lab in itertools.product("ACGT", repeat=len(internal)):
            state = dict(zip(internal, lab))
            for i in range(n):
                state[i] = col[i]
            c = sum(state[x] != state[y] for x, y in edges)
            best = c if best is None or c < best else best
        total += best
    return total


def fitch(tree, n, columns):
    """Fitch parsimony length, rooted at leaf 0, with an explicit stack."""
    parent = {0: -1}
    order = [0]
    stack = [0]
    while stack:
        v = stack.pop()
        for w in tree[v]:
            if w not in parent:
                parent[w] = v
                order.append(w)
                stack.append(w)
    total = 0
    for col in columns:
        sets = {}
        for v in reversed(order[1:]):
            kids = [w for w in tree[v] if parent.get(w) == v]
            if not kids:
                sets[v] = {col[v]}
                continue
            a, b = sets[kids[0]], sets[kids[1]]
            if a & b:
                sets[v] = a & b
            else:
                sets[v] = a | b
                total += 1
        if col[0] not in sets[order[1]]:
            total += 1
    return total


def random_columns(rng, n, m):
    return ["".join(rng.choice("ACGT") for _ in range(n)) for _ in range(m)]


def test_count_and_distinct_on_all_trees():
    for n in range(4, 8):
        trees = all_trees(n)
        assert len(trees) == double_factorial(2 * n - 5)
        for t in trees:
            nb = nni_neighbors(t)
            keys = {topology(x, n) for x in nb}
            assert len(nb) == 2 * (n - 3)
            assert len(keys) == 2 * (n - 3)
            assert topology(t, n) not in keys


def test_neighbors_are_binary_trees_on_same_leaves():
    rng = random.Random(7)
    for n in range(4, 9):
        t = rng.choice(all_trees(n))
        for x in nni_neighbors(t):
            assert leaf_count(x) == n
            assert all(len(x[v]) == (1 if v < n else 3) for v in x)
            assert sum(len(nb) for nb in x.values()) == 2 * (2 * n - 3)


def test_neighbors_equal_trees_with_one_split_changed():
    # Brute force: scan all trees and keep those that differ in exactly one split.
    for n in range(4, 8):
        trees = all_trees(n)
        keys = [topology(t, n) for t in trees]
        step = max(1, len(trees) // 40)
        for i in range(0, len(trees), step):
            got = {topology(x, n) for x in nni_neighbors(trees[i])}
            want = {k for k in keys if len(k ^ keys[i]) == 2}
            assert got == want


def test_fitch_oracle_agrees_with_brute_force():
    rng = random.Random(3)
    for _ in range(30):
        n = 5
        t = rng.choice(all_trees(n))
        cols = random_columns(rng, n, 3)
        assert fitch(t, n, cols) == brute_parsimony(t, n, cols)


def test_hill_climb_reaches_local_optimum():
    rng = random.Random(11)
    for trial in range(40):
        n = rng.randint(4, 7)
        cols = random_columns(rng, n, 8)
        trees = all_trees(n)
        start = rng.choice(trees)

        def score(t):
            return fitch(t, n, cols)

        best, s = nni_hill_climb(start, score)
        assert s == score(best) <= score(start)
        assert all(score(x) >= s for x in nni_neighbors(best))
        assert s >= min(score(t) for t in trees)


def test_hill_climb_on_four_taxa_is_exact():
    # With four taxa every tree is one NNI from every other, so one step is exhaustive.
    rng = random.Random(5)
    for _ in range(100):
        cols = random_columns(rng, 4, 6)
        trees = all_trees(4)

        def score(t):
            return fitch(t, 4, cols)

        _, s = nni_hill_climb(trees[0], score)
        assert s == min(score(t) for t in trees)


def test_worked_example():
    # Leaves 0..4; the tree ((0,1),2,(3,4)) has two internal edges and four NNI neighbors.
    n = 5
    t = {0: {5}, 1: {5}, 5: {0, 1, 6}, 2: {6}, 6: {5, 2, 7}, 3: {7}, 4: {7}, 7: {6, 3, 4}}
    # Splits are stored as the side without leaf 0: {2, 3, 4} is the split 01|234.
    assert topology(t, n) == frozenset({frozenset({2, 3, 4}), frozenset({3, 4})})
    nb = {topology(x, n) for x in nni_neighbors(t)}
    as_text = sorted(sorted(sorted(s) for s in k) for k in nb)
    assert as_text == [
        [[1, 2], [3, 4]],  # ((1,2),0,(3,4))
        [[1, 3, 4], [3, 4]],  # ((0,2),1,(3,4))
        [[2, 3], [2, 3, 4]],  # ((0,1),4,(2,3))
        [[2, 3, 4], [2, 4]],  # ((0,1),3,(2,4))
    ]
