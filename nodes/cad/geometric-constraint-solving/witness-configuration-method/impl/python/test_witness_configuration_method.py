# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/witness-configuration-method/. The authors are listed in prov/JK8AA5.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from witness_configuration_method import (analyze, generic_rank, jacobian_rows, rank, random_witness,
                                          trivial_dimension)


def laman_sparse(n, edges):
    """Every set of k >= 2 vertices spans at most 2k - 3 of the edges (brute force over vertex subsets)."""
    for k in range(2, n + 1):
        for X in combinations(range(n), k):
            s = set(X)
            if sum(1 for u, v in edges if u in s and v in s) > 2 * k - 3:
                return False
    return True


def laman_rank(n, edges):
    """The rank of the generic 2D rigidity matroid by the Laman count: a greedy basis of sparse sets."""
    basis = []
    for e in edges:
        if laman_sparse(n, basis + [e]):
            basis.append(e)
    return len(basis)


def laman_rank_by_edge_subsets(n, edges):
    """The same rank as the largest sparse edge subset, by brute force over all edge subsets."""
    for size in range(len(edges), -1, -1):
        for S in combinations(edges, size):
            if laman_sparse(n, list(S)):
                return size
    return 0


def random_graph(rng, n, prob):
    return [e for e in combinations(range(n), 2) if rng.random() < prob]


def test_witness_rank_matches_laman_count():
    rng = random.Random(1)
    for _ in range(150):
        n = rng.randint(2, 7)
        edges = random_graph(rng, n, rng.choice([0.3, 0.5, 0.7, 0.9]))
        assert generic_rank(n, edges, 2, rng) == laman_rank(n, edges)


def test_greedy_laman_rank_is_the_brute_force_rank():
    rng = random.Random(2)
    for _ in range(40):
        n = rng.randint(2, 5)
        edges = random_graph(rng, n, 0.6)
        assert laman_rank(n, edges) == laman_rank_by_edge_subsets(n, edges)


def test_single_witness_with_large_box():
    rng = random.Random(3)
    for _ in range(60):
        n = rng.randint(3, 7)
        edges = random_graph(rng, n, 0.6)
        info = analyze(n, edges, 2, rng)
        assert info["rank"] == laman_rank(n, edges)
        assert len(info["redundant"]) == len(edges) - info["rank"]


def test_witness_rank_never_exceeds_generic_rank():
    """With a tiny box many witnesses are special, but the rank can only drop."""
    rng = random.Random(4)
    drops = 0
    for _ in range(150):
        n = rng.randint(3, 7)
        edges = random_graph(rng, n, 0.7)
        r = rank(jacobian_rows(edges, random_witness(n, 2, rng, 2)))
        lr = laman_rank(n, edges)
        assert r <= lr
        drops += r < lr
    assert drops > 0


def test_verdicts():
    triangle = [(0, 1), (1, 2), (0, 2)]
    assert analyze(3, triangle)["verdict"] == "well"
    square = [(0, 1), (1, 2), (2, 3), (0, 3)]
    info = analyze(4, square)
    assert info["verdict"] == "under" and info["flex"] == 1
    k4 = list(combinations(range(4), 2))
    info = analyze(4, k4)
    assert info["verdict"] == "over" and info["redundant"] == [(2, 3)]


def test_redundant_edges_are_dependent():
    rng = random.Random(5)
    for _ in range(40):
        n = rng.randint(4, 7)
        edges = random_graph(rng, n, 0.8)
        info = analyze(n, edges, 2, rng)
        kept = [e for e in edges if e not in info["redundant"]]
        rows = jacobian_rows(kept, info["witness"])
        assert rank(rows) == len(kept) == info["rank"]


def test_trivial_dimension():
    assert [trivial_dimension(2, n) for n in range(1, 5)] == [2, 3, 3, 3]
    assert [trivial_dimension(3, n) for n in range(1, 6)] == [3, 5, 6, 6, 6]


def test_line_rank_is_n_minus_components():
    rng = random.Random(6)
    for _ in range(40):
        n = rng.randint(2, 7)
        edges = random_graph(rng, n, 0.35)
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x
        for u, v in edges:
            parent[find(u)] = find(v)
        components = len({find(x) for x in range(n)})
        assert generic_rank(n, edges, 1, rng) == n - components


def test_double_banana_in_space():
    def banana(t):
        vs = [0, 1] + list(t)
        return [e for e in combinations(vs, 2) if e != (0, 1)]
    edges = banana((2, 3, 4)) + banana((5, 6, 7))
    assert len(edges) == 3 * 8 - 6
    info = analyze(8, edges, 3, random.Random(7))
    assert info["rank"] == 17 and info["flex"] == 1 and len(info["redundant"]) == 1
    assert info["verdict"] == "under"


def test_special_witness_on_a_circle():
    """K(3,3) with its six points on a circle has a stress and a flex; a random witness does not."""
    k33 = [(i, j) for i in range(3) for j in range(3, 6)]
    on_circle = [(5, 0), (0, 5), (-5, 0), (3, 4), (-4, -3), (4, -3)]
    assert all(x * x + y * y == 25 for x, y in on_circle)
    assert analyze(6, k33, witness=on_circle)["rank"] == 8
    assert analyze(6, k33, 2, random.Random(8))["rank"] == 9


def test_fractions_are_exact():
    rows = jacobian_rows([(0, 1)], [[1, 2], [4, 6]])
    assert rows == [[Fraction(-3), Fraction(-4), Fraction(3), Fraction(4)]]
