# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bottleneck-tsp-approximation/. The authors are listed in prov/PT0SHC.jsonl.

import itertools
import random

from bottleneck_tsp_approximation import (
    bottleneck,
    bottleneck_tsp_2approx,
    hamiltonian_cycle,
    is_biconnected,
    square,
    threshold_graph,
)

# A(2,4) B(1,1) C(2,5) D(0,1) E(5,1) F(3,2) with the Manhattan distance.
POINTS = [(2, 4), (1, 1), (2, 5), (0, 1), (5, 1), (3, 2)]


def manhattan(points):
    return [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in points] for p in points]


def brute_force_opt(cost):
    n = len(cost)
    if n <= 1:
        return 0
    return min(bottleneck(cost, [0, *p]) for p in itertools.permutations(range(1, n)))


def random_metric(rng):
    n = rng.randrange(3, 8)
    kind = rng.randrange(3)
    if kind == 0:
        return manhattan([(rng.randrange(8), rng.randrange(8)) for _ in range(n)])
    if kind == 1:
        c = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                c[i][j] = c[j][i] = rng.choice((1, 2))
        return c
    inf = float("inf")
    d = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for v in range(1, n):
        u = rng.randrange(v)
        d[u][v] = d[v][u] = rng.randrange(1, 6)
    for _ in range(n):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v:
            d[u][v] = d[v][u] = min(d[u][v], rng.randrange(1, 6))
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


def test_example() -> None:
    cost = manhattan(POINTS)
    assert not is_biconnected(threshold_graph(cost, 3))
    assert is_biconnected(threshold_graph(cost, 4))
    tour, t = bottleneck_tsp_2approx(cost)
    assert t == 4
    assert sorted(tour) == list(range(6))
    assert "".join("ABCDEF"[v] for v in tour) == "AFEDCB"
    assert bottleneck(cost, tour) == 6
    assert brute_force_opt(cost) == 5
    assert hamiltonian_cycle(threshold_graph(cost, 4)) is None


def test_edges() -> None:
    assert bottleneck_tsp_2approx([]) == ([], 0)
    assert bottleneck_tsp_2approx([[0]]) == ([0], 0)
    assert bottleneck_tsp_2approx([[0, 3], [3, 0]]) == ([0, 1], 3)
    tour, t = bottleneck_tsp_2approx([[0, 1, 2], [1, 0, 2], [2, 2, 0]])
    assert t == 2 and sorted(tour) == [0, 1, 2]


def test_against_brute_force() -> None:
    rng = random.Random(1984)
    for _ in range(500):
        cost = random_metric(rng)
        n = len(cost)
        tour, t = bottleneck_tsp_2approx(cost)
        assert sorted(tour) == list(range(n))
        values = sorted({cost[u][v] for u in range(n) for v in range(u + 1, n)})
        least = next(x for x in values if is_biconnected(threshold_graph(cost, x)))
        assert t == least
        opt = brute_force_opt(cost)
        alg = bottleneck(cost, tour)
        assert t <= opt <= alg <= 2 * t


def test_hardness_and_tightness() -> None:
    # K_{2,3} with costs 1 and 2: G_1 is biconnected but not Hamiltonian, so t = 1 and OPT = 2.
    left, right = {0, 1}, {2, 3, 4}
    k23 = [[0 if i == j else (1 if (i in left) != (j in left) else 2) for j in range(5)] for i in range(5)]
    tour, t = bottleneck_tsp_2approx(k23)
    assert t == 1 and brute_force_opt(k23) == 2 and bottleneck(k23, tour) == 2
    # The cycle C_6 with its path metric: t = OPT = 1, and the square has a cycle of bottleneck 2.
    n = 6
    ring = [[min(abs(i - j), n - abs(i - j)) for j in range(n)] for i in range(n)]
    tour, t = bottleneck_tsp_2approx(ring)
    assert t == 1 and brute_force_opt(ring) == 1
    s = square(threshold_graph(ring, 1))
    bad = [0, 2, 4, 5, 3, 1]
    assert all(bad[(i + 1) % n] in s[bad[i]] for i in range(n))
    assert bottleneck(ring, bad) == 2
