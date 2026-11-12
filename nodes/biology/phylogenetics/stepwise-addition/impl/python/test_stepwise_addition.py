# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stepwise-addition/. The authors are listed in prov/3VNTRD.jsonl.

import itertools
import random

from stepwise_addition import (
    all_trees_by_addition,
    edges,
    fitch_score,
    insert_leaf,
    random_addition,
    stepwise_addition,
    topology,
)


def double_factorial(k):
    r = 1
    while k > 1:
        r *= k
        k -= 2
    return r


def brute_parsimony(tree, n, seqs):
    internal = sorted(v for v in tree if v >= n)
    es = edges(tree)
    total = 0
    for j in range(len(seqs[0])):
        best = None
        for lab in itertools.product("ACGT", repeat=len(internal)):
            st = dict(zip(internal, lab))
            for v in tree:
                if v < n:
                    st[v] = seqs[v][j]
            c = sum(st[x] != st[y] for x, y in es)
            best = c if best is None or c < best else best
        total += best
    return total


def rand_seqs(rng, n, m, alphabet="ACGT"):
    return ["".join(rng.choice(alphabet) for _ in range(m)) for _ in range(n)]


def test_full_addition_gives_each_tree_once():
    for n in range(3, 9):
        trees = all_trees_by_addition(n)
        assert len(trees) == double_factorial(2 * n - 5)
        assert len({topology(t, n) for t in trees}) == len(trees)


def test_edge_count_of_partial_trees():
    t = {0: {5}, 1: {5}, 2: {5}, 5: {0, 1, 2}}
    for k, leaf in enumerate([3, 4], start=4):
        assert len(edges(t)) == 2 * k - 5
        t = insert_leaf(t, edges(t)[0], leaf, 5 + k - 3)


def test_fitch_on_partial_trees_matches_brute_force():
    rng = random.Random(1)
    for _ in range(40):
        n = 6
        seqs = rand_seqs(rng, n, 3)
        order = list(range(n))
        rng.shuffle(order)
        k = rng.randint(3, 5)
        tree, _ = stepwise_addition(order[:k], n, lambda t: fitch_score(t, n, seqs))
        assert fitch_score(tree, n, seqs) == brute_parsimony(tree, n, seqs)


def test_each_step_takes_a_best_position():
    rng = random.Random(2)
    for _ in range(60):
        n = rng.randint(4, 8)
        seqs = rand_seqs(rng, n, 8)
        order = list(range(n))
        rng.shuffle(order)
        score = lambda t: fitch_score(t, n, seqs)
        for k in range(4, n + 1):
            prev, _ = stepwise_addition(order[: k - 1], n, score)
            cur, s = stepwise_addition(order[:k], n, score)
            options = [score(insert_leaf(prev, e, order[k - 1], 10 * n)) for e in edges(prev)]
            assert len(options) == 2 * k - 5
            assert s == min(options) == score(cur)


def test_never_better_than_exhaustive_optimum():
    rng = random.Random(3)
    misses = 0
    for _ in range(60):
        n = 6
        seqs = rand_seqs(rng, n, 10)
        score = lambda t: fitch_score(t, n, seqs)
        opt = min(score(t) for t in all_trees_by_addition(n))
        _, s = stepwise_addition(list(range(n)), n, score)
        assert s >= opt
        misses += s > opt
        _, r = random_addition(n, score, 10, random.Random(4))
        assert opt <= r
    assert misses > 0  # the greedy order alone is not exact on random data


def test_worked_example():
    seqs = ["AAAAAA", "AAACCC", "CCAAAC", "CCCCCA", "ACACAC"]
    n = 5
    score = lambda t: fitch_score(t, n, seqs)
    tree, s = stepwise_addition([0, 1, 2, 3, 4], n, score)
    assert s == min(score(t) for t in all_trees_by_addition(n))
