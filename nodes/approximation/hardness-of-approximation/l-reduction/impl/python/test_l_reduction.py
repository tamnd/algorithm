# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/l-reduction/. The authors are listed in prov/VK0B3P.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from l_reduction import (
    check_l_reduction,
    max_degree,
    mis_to_vc_constants,
    random_bounded_degree_graph,
    sat_to_mis_constants,
    vc_to_mis_constants,
)


def test_check_l_reduction_on_hand_values() -> None:
    assert check_l_reduction(4, 8, [(8, 4), (6, 3)]) == (Fraction(2), Fraction(1, 2))
    assert check_l_reduction(3, 3, [(3, 2)])[1] == Fraction(10**9)


def test_max_3sat_to_independent_set() -> None:
    rng = random.Random(1)
    for _ in range(60):
        num_vars = rng.randint(3, 4)
        clauses = []
        for _ in range(rng.randint(1, 5)):
            vs = rng.sample(range(1, num_vars + 1), 3)
            clauses.append(tuple(v if rng.random() < 0.5 else -v for v in vs))
        alpha, beta = sat_to_mis_constants(clauses, num_vars)
        assert alpha == 1
        assert beta <= 1


def test_independent_set_to_vertex_cover_bounded_degree() -> None:
    rng = random.Random(2)
    for _ in range(80):
        b = rng.randint(1, 4)
        n = rng.randint(1, 8)
        edges = random_bounded_degree_graph(rng, n, b, 3 * n) if n > 1 else set()
        assert max_degree(n, edges) <= b
        alpha, beta = mis_to_vc_constants(n, edges)
        assert alpha <= b
        assert beta <= 1


def test_alpha_b_is_attained_by_the_complete_graph() -> None:
    for b in range(1, 6):
        n = b + 1
        edges = {frozenset(e) for e in combinations(range(n), 2)}
        alpha, beta = mis_to_vc_constants(n, edges)
        assert alpha == b and beta == 1


def test_vertex_cover_to_independent_set_bounded_degree() -> None:
    rng = random.Random(3)
    seen = 0
    for _ in range(200):
        b = rng.randint(1, 4)
        n = rng.randint(2, 8)
        edges = random_bounded_degree_graph(rng, n, b, 4 * n)
        if any(all(v not in e for e in edges) for v in range(n)):
            continue  # an isolated vertex breaks (L1)
        seen += 1
        alpha, beta = vc_to_mis_constants(n, edges)
        assert alpha <= b
        assert beta <= 1
    assert seen > 20


def test_perfect_matching_has_alpha_1() -> None:
    edges = {frozenset((2 * i, 2 * i + 1)) for i in range(4)}
    alpha, beta = vc_to_mis_constants(8, edges)
    assert alpha == 1 and beta == 1


def test_star_attains_alpha_b_so_unbounded_degree_breaks_l1() -> None:
    for k in range(1, 8):
        edges = {frozenset((0, i)) for i in range(1, k + 1)}
        alpha, _ = vc_to_mis_constants(k + 1, edges)
        assert alpha == k
