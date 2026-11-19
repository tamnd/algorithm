# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mst-dependency-parsing/. The authors are listed in prov/Z4H7TB.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from mst_dependency_parsing import (
    arc_marginals,
    chu_liu_edmonds,
    is_tree,
    mst_parse,
    partition_function,
    tree_score,
)

JOHN_SAW_MARY = [
    [0, 9, 10, 9],
    [0, 0, 20, 3],
    [0, 30, 0, 30],
    [0, 11, 0, 0],
]


def all_trees(n):
    out = []
    for hs in itertools.product(range(n + 1), repeat=n):
        heads = [-1] + list(hs)
        if is_tree(heads):
            out.append(heads)
    return out


TREES = {n: all_trees(n) for n in range(1, 6)}


def root_children(heads):
    return sum(1 for h in heads[1:] if h == 0)


def product_weight(w, heads):
    p = F(1)
    for d in range(1, len(heads)):
        p *= w[heads[d]][d]
    return p


def test_tree_counts_by_enumeration_and_matrix_tree():
    assert [len(TREES[n]) for n in range(1, 6)] == [1, 3, 16, 125, 1296]
    for n in range(1, 8):
        ones = [[1] * (n + 1) for _ in range(n + 1)]
        assert partition_function(ones) == (n + 1) ** (n - 1)
        assert partition_function(ones, single_root=True) == n ** (n - 1)


def test_example_john_saw_mary():
    score, heads = mst_parse(JOHN_SAW_MARY)
    assert (score, heads) == (70, [-1, 2, 0, 2])
    # The greedy choice of the best head per word has the cycle John <-> saw.
    best_in = {d: max(range(4), key=lambda h: JOHN_SAW_MARY[h][d] if h != d else -1) for d in (1, 2, 3)}
    assert best_in == {1: 2, 2: 1, 3: 2}


@pytest.mark.parametrize("single_root", [False, True])
def test_against_brute_force(single_root):
    rng = random.Random(5)
    for n in range(1, 6):
        pool = [t for t in TREES[n] if not single_root or root_children(t) == 1]
        for _ in range(25 if n < 5 else 8):
            s = [[rng.randint(-10, 10) for _ in range(n + 1)] for _ in range(n + 1)]
            best = max(tree_score(s, t) for t in pool)
            score, heads = mst_parse(s, single_root=single_root)
            assert score == best
            assert is_tree(heads) and tree_score(s, heads) == score
            if single_root:
                assert root_children(heads) == 1


def test_finds_non_projective_tree():
    n = 4
    s = [[0] * (n + 1) for _ in range(n + 1)]
    s[0][2] = s[2][4] = s[4][1] = s[2][3] = 10
    assert mst_parse(s) == (40, [-1, 4, 0, 2, 2])


def test_general_graph_with_nested_cycles():
    # Two cycles; after the first contraction a second cycle appears.
    w = {(0, 1): 1, (1, 2): 10, (2, 1): 10, (2, 3): 9, (3, 4): 10, (4, 3): 10, (4, 1): 9, (0, 3): 2}
    heads = chu_liu_edmonds([0, 1, 2, 3, 4], 0, w)
    total = sum(w[(h, d)] for d, h in heads.items())
    best = None
    for hs in itertools.product(range(5), repeat=4):
        cand = [-1] + list(hs)
        if is_tree(cand) and all((cand[d], d) in w for d in range(1, 5)):
            t = sum(w[(cand[d], d)] for d in range(1, 5))
            best = t if best is None else max(best, t)
    assert total == best


def test_ties_and_negative_scores():
    rng = random.Random(9)
    for _ in range(40):
        n = rng.randint(1, 5)
        s = [[rng.choice([-3, -1, 0, 0, 2]) for _ in range(n + 1)] for _ in range(n + 1)]
        score, heads = mst_parse(s)
        assert score == max(tree_score(s, t) for t in TREES[n])


@pytest.mark.parametrize("single_root", [False, True])
def test_partition_and_marginals_against_brute_force(single_root):
    rng = random.Random(13)
    for n in range(1, 5):
        w = [[F(rng.randint(1, 6), rng.randint(1, 3)) for _ in range(n + 1)] for _ in range(n + 1)]
        pool = [t for t in TREES[n] if not single_root or root_children(t) == 1]
        z = sum(product_weight(w, t) for t in pool)
        assert partition_function(w, single_root=single_root) == z
        mu = arc_marginals(w, single_root=single_root)
        for d in range(1, n + 1):
            for h in range(n + 1):
                if h == d:
                    continue
                exact = sum(product_weight(w, t) for t in pool if t[d] == h) / z
                assert mu[h][d] == exact
            assert sum(mu[h][d] for h in range(n + 1) if h != d) == 1


def test_small_inputs():
    assert mst_parse([[0]]) == (0, [-1])
    assert mst_parse([[0, 4], [0, 0]]) == (4, [-1, 0])
    with pytest.raises(ValueError):
        mst_parse([[0, 1]])
