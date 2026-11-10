# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karlin-klein-oveis-gharan-algorithm/. The authors are listed in prov/879EXX.jsonl.

import itertools
import math
import random
from fractions import Fraction

from karlin_klein_oveis_gharan_algorithm import (
    kko_tour,
    marginals,
    max_entropy_distribution,
    spanning_trees,
    tour_cost,
    tree_to_tour,
)

# The six-vertex instance of the Held-Karp bound page: LP* = 21/2 and OPT = 11.
EXAMPLE = [
    [0, 3, 2, 3, 1, 2],
    [3, 0, 2, 2, 2, 1],
    [2, 2, 0, 2, 3, 2],
    [3, 2, 2, 0, 3, 3],
    [1, 2, 3, 3, 0, 3],
    [2, 1, 2, 3, 3, 0],
]


def brute_opt(cost):
    n = len(cost)
    return min(tour_cost(cost, (0,) + p) for p in itertools.permutations(range(1, n)))


def is_tour(tour, n):
    return sorted(tour) == list(range(n))


def kirchhoff_count(n, edges):
    """Number of spanning trees by the matrix-tree theorem, exact."""
    lap = [[Fraction(0)] * n for _ in range(n)]
    for u, v in edges:
        lap[u][u] += 1
        lap[v][v] += 1
        lap[u][v] -= 1
        lap[v][u] -= 1
    m = [row[1:] for row in lap[1:]]
    det = Fraction(1)
    size = n - 1
    for col in range(size):
        piv = next((r for r in range(col, size) if m[r][col] != 0), None)
        if piv is None:
            return 0
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = -det
        det *= m[col][col]
        for r in range(col + 1, size):
            f = m[r][col] / m[col][col]
            m[r] = [a - f * b for a, b in zip(m[r], m[col])]
    return det


def exact_expectations(cost):
    value, x, edges, z, trees, probs, gamma = max_entropy_distribution(cost)
    e_tree = e_join = e_alg = 0.0
    rows = []
    for t, p in zip(trees, probs):
        tree = [edges[k] for k in t]
        tour, matching = tree_to_tour(cost, tree)
        ct = sum(cost[u][v] for u, v in tree)
        cj = sum(cost[u][v] for u, v in matching)
        a = tour_cost(cost, tour)
        rows.append((tour, ct, cj, a, p))
        e_tree += p * ct
        e_join += p * cj
        e_alg += p * a
    return value, x, edges, z, trees, probs, gamma, rows, e_tree, e_join, e_alg


def test_example_lp_and_max_entropy_weights():
    value, x, edges, z, trees, probs, gamma = max_entropy_distribution(EXAMPLE)
    assert value == Fraction(21, 2)
    ones = {(0, 4), (1, 5), (2, 3)}
    assert {e for e, t in x.items() if t == 1} == ones
    assert all(t == Fraction(1, 2) for e, t in x.items() if e not in ones)
    assert len(x) == 9
    assert len(trees) == 75 == kirchhoff_count(6, edges)
    p = marginals(trees, probs, len(edges))
    assert all(abs(a - float(b)) < 1e-9 for a, b in zip(p, z))
    half = next(g for e, g in zip(edges, gamma) if e not in ones)
    for e, g in zip(edges, gamma):
        ratio = math.exp(g - half)
        assert abs(ratio - (4.5 if e in ones else 1.0)) < 1e-6


def test_example_exact_expectation():
    value, x, edges, z, trees, probs, gamma, rows, e_tree, e_join, e_alg = exact_expectations(EXAMPLE)
    assert abs(e_tree - 35 / 4) < 1e-9
    assert abs(e_join - 2651 / 864) < 1e-9
    assert abs(e_alg - 4871 / 432) < 1e-9
    assert abs(sum(p for _, _, _, a, p in rows if a == 11) - 73 / 96) < 1e-9
    assert brute_opt(EXAMPLE) == 11
    assert all(is_tour(t, 6) and a <= ct + cj and 2 * cj <= value for t, ct, cj, a, p in rows)


def test_random_metric_instances_against_brute_force():
    rng = random.Random(2021)
    for trial in range(14):
        n = 5 + trial % 3
        pts = [(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(n)]
        if len(set(pts)) < n:
            continue
        cost = [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in pts] for p in pts]
        value, x, edges, z, trees, probs, gamma, rows, e_tree, e_join, e_alg = exact_expectations(cost)
        opt = brute_opt(cost)
        assert value <= opt                                  # LP* <= OPT
        p = marginals(trees, probs, len(edges))
        assert all(abs(a - float(b)) < 1e-8 for a, b in zip(p, z))
        assert abs(e_tree - float(value) * (n - 1) / n) < 1e-8
        for tour, ct, cj, a, _ in rows:
            assert is_tour(tour, n)
            assert opt <= a <= ct + cj                       # shortcuts do not add cost
            assert 2 * cj <= value                           # Wolsey: the matching costs at most LP*/2
        assert e_alg <= 1.5 * float(value) + 1e-9            # E[ALG] <= 3/2 LP*
        assert e_alg <= float(value) * (n - 1) / n + float(value) / 2 + 1e-9


def gap_family(k):
    """Three paths of k unit edges; their left ends and their right ends form unit triangles."""
    n = 3 * (k + 1)
    inf = float("inf")
    d = [[0 if i == j else inf for j in range(n)] for i in range(n)]

    def link(a, b):
        d[a][b] = d[b][a] = 1

    for p in range(3):
        for i in range(k):
            link(p * (k + 1) + i, p * (k + 1) + i + 1)
    for p, q in ((0, 1), (0, 2), (1, 2)):
        link(p * (k + 1), q * (k + 1))
        link(p * (k + 1) + k, q * (k + 1) + k)
    for m in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][m] + d[m][j] < d[i][j]:
                    d[i][j] = d[i][m] + d[m][j]
    return [[int(v) for v in row] for row in d]


def test_four_thirds_family_k2():
    cost = gap_family(2)
    value, x, edges, z, trees, probs, gamma, rows, e_tree, e_join, e_alg = exact_expectations(cost)
    assert value == 9
    assert sorted(x.values()).count(Fraction(1)) == 6 and sorted(x.values()).count(Fraction(1, 2)) == 6
    assert brute_opt(cost) == 10
    assert 10 <= e_alg <= 13.5
    assert all(is_tour(t, 9) for t, *_ in rows)


def test_sampling_follows_the_marginals():
    value, x, edges, z, trees, probs, gamma = max_entropy_distribution(EXAMPLE)
    rng = random.Random(7)
    counts = [0] * len(edges)
    draws = 4000
    for _ in range(draws):
        t = rng.choices(range(len(trees)), weights=probs)[0]
        for k in trees[t]:
            counts[k] += 1
    assert all(abs(c / draws - float(q)) < 0.03 for c, q in zip(counts, z))
    tour = kko_tour(EXAMPLE, random.Random(2021))
    assert is_tour(tour, 6) and tour_cost(EXAMPLE, tour) >= 11


def test_spanning_tree_enumeration_matches_kirchhoff():
    k4 = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    assert len(spanning_trees(4, k4)) == 16 == kirchhoff_count(4, k4)
    cycle = [(i, (i + 1) % 6) for i in range(6)]
    assert len(spanning_trees(6, cycle)) == 6 == kirchhoff_count(6, cycle)
