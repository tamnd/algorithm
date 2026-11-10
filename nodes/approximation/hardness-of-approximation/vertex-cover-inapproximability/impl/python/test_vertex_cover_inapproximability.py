# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-cover-inapproximability/. The authors are listed in prov/DAHD4S.jsonl.

import random
from fractions import Fraction
from itertools import combinations, product

from vertex_cover_inapproximability import (
    clique_to_vertex_cover,
    complement,
    is_clique,
    is_vertex_cover,
    max_clique_size,
    max_satisfied,
    min_vertex_cover_size,
    sat_to_vertex_cover,
    vertex_cover_to_clique,
)


def random_graph(rng: random.Random, n: int, p: float) -> set[frozenset[int]]:
    return {frozenset((u, v)) for u, v in combinations(range(n), 2) if rng.random() < p}


def random_3cnf(rng: random.Random, num_vars: int, m: int) -> list[tuple[int, ...]]:
    out = []
    for _ in range(m):
        vs = rng.sample(range(1, num_vars + 1), 3)
        out.append(tuple(v if rng.random() < 0.5 else -v for v in vs))
    return out


def brute_tau(n: int, edges: set[frozenset[int]]) -> int:
    for k in range(n + 1):
        if any(is_vertex_cover(list(s), edges) for s in combinations(range(n), k)):
            return k
    return n


def test_branch_and_bound_matches_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(150):
        n = rng.randint(0, 9)
        edges = random_graph(rng, n, rng.random())
        assert min_vertex_cover_size(n, edges) == brute_tau(n, edges)


def test_clique_plus_cover_of_complement_is_n() -> None:
    rng = random.Random(2)
    for _ in range(150):
        n = rng.randint(1, 9)
        g = random_graph(rng, n, rng.random())
        h = complement(n, g)
        assert max_clique_size(n, g) + min_vertex_cover_size(n, h) == n


def test_solution_maps_both_ways() -> None:
    rng = random.Random(9)
    for _ in range(40):
        n = rng.randint(1, 7)
        g = random_graph(rng, n, 0.5)
        h = complement(n, g)
        for k in range(n + 1):
            for s in combinations(range(n), k):
                s = list(s)
                if is_clique(s, g):
                    cover = clique_to_vertex_cover(n, s)
                    assert is_vertex_cover(cover, h) and len(cover) == n - len(s)
                if is_vertex_cover(s, h):
                    clique = vertex_cover_to_clique(n, s)
                    assert is_clique(clique, g) and len(clique) == n - len(s)


def test_gap_transfer_for_clique() -> None:
    # omega >= c n implies tau(complement) <= (1 - c) n; omega <= s n implies tau >= (1 - s) n.
    rng = random.Random(4)
    for _ in range(100):
        n = rng.randint(2, 9)
        g = random_graph(rng, n, rng.random())
        w = max_clique_size(n, g)
        t = min_vertex_cover_size(n, complement(n, g))
        frac = Fraction(w, n)
        assert t <= (1 - frac) * n and t >= (1 - frac) * n


def test_sat_to_vertex_cover_completeness_and_soundness() -> None:
    rng = random.Random(8)
    for _ in range(120):
        num_vars = rng.randint(3, 4)
        m = rng.randint(1, 5)
        clauses = random_3cnf(rng, num_vars, m)
        n, edges = sat_to_vertex_cover(clauses)
        tau = min_vertex_cover_size(n, edges)
        opt = max_satisfied(clauses, num_vars)
        assert n == 3 * m
        assert tau == 3 * m - opt
        if opt == m:
            assert tau <= 2 * m
        else:
            eps = 1 - Fraction(opt, m)
            assert tau >= (2 + eps) * m


def test_all_eight_clauses_example() -> None:
    clauses = [tuple(s * v for s, v in zip(signs, (1, 2, 3))) for signs in product((1, -1), repeat=3)]
    n, edges = sat_to_vertex_cover(clauses)
    assert n == 24
    assert max_satisfied(clauses, 3) == 7
    assert min_vertex_cover_size(n, edges) == 17
