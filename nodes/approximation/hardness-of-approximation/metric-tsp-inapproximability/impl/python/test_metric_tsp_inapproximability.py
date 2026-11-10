# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metric-tsp-inapproximability/. The authors are listed in prov/XPTJYD.jsonl.

import random
from fractions import Fraction
from itertools import combinations, permutations

from metric_tsp_inapproximability import (
    gap_ratio,
    is_hamiltonian,
    one_two_instance,
    path_cover_number,
    paths_to_tour,
    tour_cost,
    tour_to_paths,
    tsp_opt,
)


def opt_by_identity(n, edges):
    return n if is_hamiltonian(n, edges) else n + path_cover_number(n, edges)


def test_examples() -> None:
    star = [(0, v) for v in range(1, 5)]
    assert path_cover_number(5, star) == 3
    assert tsp_opt(one_two_instance(5, star)) == 8
    triangles = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
    assert path_cover_number(6, triangles) == 2
    assert tsp_opt(one_two_instance(6, triangles)) == 8
    outer = [(i, (i + 1) % 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    petersen = outer + inner + [(i, i + 5) for i in range(5)]
    assert not is_hamiltonian(10, petersen)
    assert path_cover_number(10, petersen) == 1
    assert tsp_opt(one_two_instance(10, petersen)) == 11


def test_identity_on_random_graphs() -> None:
    rng = random.Random(7)
    for _ in range(150):
        n = rng.randint(3, 8)
        p = rng.choice([0.2, 0.4, 0.6])
        edges = [e for e in combinations(range(n), 2) if rng.random() < p]
        assert tsp_opt(one_two_instance(n, edges)) == opt_by_identity(n, edges)


def test_tours_and_paths_correspond() -> None:
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randint(3, 7)
        edges = [e for e in combinations(range(n), 2) if rng.random() < 0.4]
        c = one_two_instance(n, edges)
        for perm in permutations(range(1, n)):
            tour = [0, *perm]
            cost = tour_cost(c, tour)
            paths = tour_to_paths(c, tour)
            if cost > n:
                assert len(paths) == cost - n
                assert sorted(v for p in paths for v in p) == list(range(n))
                assert all(c[a][b] == 1 for p in paths for a, b in zip(p, p[1:]))
            assert tour_cost(c, paths_to_tour(paths)) <= n + len(paths)


def test_gap_ratio() -> None:
    assert gap_ratio(Fraction(0), Fraction(1, 100)) == Fraction(101, 100)
    assert gap_ratio(Fraction(1, 100), Fraction(2, 100)) == Fraction(102, 101)
