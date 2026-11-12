# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cost-complexity-pruning/. The authors are listed in prov/V06HEB.jsonl.

import random
from fractions import Fraction

from cost_complexity_pruning import (Node, at_alpha, choose_by_cv, grow_regression, leaves, number,
                                     smallest_optimal, weakest_link)


def all_prunings(t):
    """Every pruned subtree of t as (R, number of leaves, set of internal node ids kept)."""
    out = [(t.risk, 1, frozenset())]
    if t.is_leaf():
        return out
    combos = [(0, 0, frozenset({t.id}))]
    for u in t.children:
        combos = [(r + r2, k + k2, s | s2) for r, k, s in combos for r2, k2, s2 in all_prunings(u)]
    return out + combos


def internal_kept(t, cut):
    if t.is_leaf() or t.id in cut:
        return set()
    return {t.id}.union(*(internal_kept(u, cut) for u in t.children))


def random_tree(rng, depth, arity):
    """A tree whose risks satisfy R(t) >= sum of R over the children."""
    if depth == 0 or rng.random() < 0.3:
        return Node(rng.randint(0, 4))
    kids = [random_tree(rng, depth - 1, arity) for _ in range(rng.choice(arity))]
    return Node(sum(k.risk for k in kids) + rng.choice([0, 0, 1, 2, 3, 5]), kids)


def check_against_brute_force(root):
    seq = weakest_link(root)
    number(root)
    P = all_prunings(root)
    alphas = [a for a, _ in seq]
    assert alphas[0] == 0 and all(a < b for a, b in zip(alphas, alphas[1:]))
    assert internal_kept(root, seq[-1][1]) == set()
    kept = [internal_kept(root, c) for _, c in seq]
    assert all(b <= a for a, b in zip(kept, kept[1:]))  # nested
    probes = alphas + [(a + b) / 2 for a, b in zip(alphas, alphas[1:])] + [alphas[-1] + 1, alphas[-1] * 3]
    for al in probes:
        best = min(r + al * k for r, k, _ in P)
        minimizers = [s for r, k, s in P if r + al * k == best]
        cost, cut = smallest_optimal(root, al)
        assert cost == best
        dp = internal_kept(root, cut)
        assert dp in minimizers and all(dp <= s for s in minimizers)
        assert internal_kept(root, at_alpha(seq, al)) == dp


def test_binary_trees_against_all_prunings():
    rng = random.Random(1984)
    for _ in range(400):
        check_against_brute_force(random_tree(rng, 4, [2]))


def test_multiway_trees_against_all_prunings():
    rng = random.Random(3)
    for _ in range(200):
        check_against_brute_force(random_tree(rng, 3, [2, 3]))


def test_page_example():
    b2 = Node(2, [Node(0), Node(1)])
    b = Node(5, [Node(2), b2])
    a = Node(4, [Node(1), Node(1)])
    root = Node(10, [a, b])
    seq = weakest_link(root)
    assert [a_ for a_, _ in seq] == [0, 1, Fraction(3, 2)]
    assert sorted(len(leaves(root, c)) for _, c in seq) == [1, 3, 5]
    assert sum(t.risk for t in leaves(root, seq[1][1])) == 7


def test_grown_regression_trees_against_all_prunings():
    rng = random.Random(9)
    for _ in range(60):
        n = rng.randint(2, 9)
        X = [(rng.randint(0, 9),) for _ in range(n)]
        y = [Fraction(rng.randint(0, 6)) for _ in range(n)]
        check_against_brute_force(grow_regression(X, y, list(range(n))))


def test_cross_validation_finds_the_step():
    rng = random.Random(4)
    X = [(rng.random(),) for _ in range(120)]
    y = [(10 if x[0] > 0.5 else 0) + rng.choice([-2, -1, 0, 1, 2]) for x in X]
    root, seq, k, cv = choose_by_cv(X, y, folds=5, rng=random.Random(5))
    assert k == min(range(len(seq)), key=lambda i: (cv[i], -i))
    assert len(leaves(root, seq[0][1])) > 50
    t = leaves(root, seq[k][1])
    assert len(t) == 2
    assert root.feature == 0 and abs(root.threshold - Fraction(1, 2)) < Fraction(1, 20)
