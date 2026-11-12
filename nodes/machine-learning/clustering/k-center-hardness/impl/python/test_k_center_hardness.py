# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-center-hardness/. The authors are listed in prov/MEYRRB.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from k_center_hardness import (
    clique_cover_number,
    domination_number,
    farthest_first,
    graph_metric,
    max_diameter,
    opt_diameter,
    opt_radius,
    radius,
)


def random_metric(rng, n):
    """Shortest-path metric of a complete graph with random Fraction weights."""
    D = [[Fraction(0)] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        D[i][j] = D[j][i] = Fraction(rng.randint(1, 20), rng.randint(1, 4))
    for m in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][m] + D[m][j] < D[i][j]:
                    D[i][j] = D[i][m] + D[m][j]
    return lambda i, j: D[i][j]


def is_metric(n, d):
    for i in range(n):
        for j in range(n):
            if d(i, j) != d(j, i) or (d(i, j) == 0) != (i == j):
                return False
            for m in range(n):
                if d(i, j) > d(i, m) + d(m, j):
                    return False
    return True


def test_two_approximation_for_radius_and_diameter():
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randint(2, 6)
        d = random_metric(rng, n)
        assert is_metric(n, d)
        for k in range(1, n):
            o_rad, o_diam = opt_radius(n, k, d), opt_diameter(n, k, d)
            for first in range(n):
                centers, labels = farthest_first(n, k, d, first)
                r = radius(n, centers, d)
                assert o_rad <= r <= 2 * o_rad
                assert max_diameter(n, labels, d) <= 2 * r
                assert r <= o_diam
                assert max_diameter(n, labels, d) <= 2 * o_diam


def test_tight_example():
    pts = [0, 1, 2]
    d = lambda i, j: abs(pts[i] - pts[j])
    centers, labels = farthest_first(3, 1, d, first=0)
    assert radius(3, centers, d) == 2 == 2 * opt_radius(3, 1, d)


def random_graph(rng, n, p):
    return [e for e in combinations(range(n), 2) if rng.random() < p]


def test_reductions():
    rng = random.Random(11)
    for _ in range(80):
        n = rng.randint(2, 6)
        edges = random_graph(rng, n, rng.choice([0.3, 0.5, 0.7]))
        d = graph_metric(n, edges)
        assert is_metric(n, d)
        gamma = domination_number(n, edges)
        theta = clique_cover_number(n, edges)
        for k in range(1, n):
            assert opt_radius(n, k, d) == (1 if gamma <= k else 2)
            assert opt_diameter(n, k, d) == (1 if theta <= k else 2)


def test_examples_on_the_page():
    # the 5-cycle: domination number 2, clique cover number 3
    c5 = [(i, (i + 1) % 5) for i in range(5)]
    d = graph_metric(5, c5)
    assert domination_number(5, c5) == 2
    assert clique_cover_number(5, c5) == 3
    assert [opt_radius(5, k, d) for k in (1, 2, 3)] == [2, 1, 1]
    assert [opt_diameter(5, k, d) for k in (1, 2, 3)] == [2, 2, 1]
