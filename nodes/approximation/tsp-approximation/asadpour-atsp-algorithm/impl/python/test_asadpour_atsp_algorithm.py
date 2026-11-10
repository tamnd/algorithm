# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asadpour-atsp-algorithm/. The authors are listed in prov/7DRJZ2.jsonl.

import itertools
import random
from fractions import Fraction

from asadpour_atsp_algorithm import (
    asadpour_tour,
    atsp_lp,
    balance_arcs,
    edge_cost,
    euler_circuit_directed,
    marginals,
    max_entropy_distribution,
    tour_cost,
    tree_to_tour,
)

# The example of the page: shortest path costs of a random complete digraph (seed 23).
EXAMPLE = [
    [0, 3, 2, 1, 5, 6],
    [4, 0, 6, 5, 3, 4],
    [2, 3, 0, 1, 4, 5],
    [1, 2, 2, 0, 5, 6],
    [1, 2, 3, 2, 0, 1],
    [4, 1, 5, 3, 4, 0],
]


def brute_opt(cost):
    n = len(cost)
    return min(tour_cost(cost, (0,) + p) for p in itertools.permutations(range(1, n)))


def closure(n, w):
    d = [row[:] for row in w]
    for m in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][m] + d[m][j] < d[i][j]:
                    d[i][j] = d[i][m] + d[m][j]
    return d


def random_instance(rng, n):
    w = [[0 if i == j else rng.randint(1, 9) for j in range(n)] for i in range(n)]
    return closure(n, w)


def thinness(n, tree, edges, z):
    """The least alpha with |T cut U| <= alpha z(cut U) for each cut, exact."""
    worst = Fraction(0)
    for mask in range(1, 1 << (n - 1)):
        side = mask << 1 | 1
        if side == (1 << n) - 1:
            continue
        crossing = sum(1 for u, v in tree if (side >> u & 1) != (side >> v & 1))
        zcut = sum(t for (u, v), t in zip(edges, z) if (side >> u & 1) != (side >> v & 1))
        worst = max(worst, Fraction(crossing) / zcut)
    return worst


def kirchhoff_count(n, edges):
    lap = [[Fraction(0)] * n for _ in range(n)]
    for u, v in edges:
        lap[u][u] += 1
        lap[v][v] += 1
        lap[u][v] -= 1
        lap[v][u] -= 1
    m = [row[1:] for row in lap[1:]]
    det = Fraction(1)
    for col in range(n - 1):
        piv = next((r for r in range(col, n - 1) if m[r][col] != 0), None)
        if piv is None:
            return 0
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = -det
        det *= m[col][col]
        for r in range(col + 1, n - 1):
            f = m[r][col] / m[col][col]
            m[r] = [a - f * b for a, b in zip(m[r], m[col])]
    return det


def is_tour(tour, n):
    return sorted(tour) == list(range(n))


def check_instance(cost):
    n = len(cost)
    value, x, edges, z, trees, probs = max_entropy_distribution(cost)
    opt = brute_opt(cost)
    assert value <= opt                                                   # LP* <= OPT
    p = marginals(trees, probs, len(edges))
    assert all(abs(a - float(b)) < 1e-8 for a, b in zip(p, z))
    e_tree = sum(q * sum(edge_cost(cost, edges[k]) for k in t) for t, q in zip(trees, probs))
    assert e_tree <= float(value) * (n - 1) / n + 1e-9                    # E[c(T)] <= (1 - 1/n) LP*
    for t in trees:
        tree = [edges[k] for k in t]
        tour, oriented, extra = tree_to_tour(cost, tree)
        assert is_tour(tour, n)
        circ = sum(cost[u][v] for u, v in oriented + extra)
        alpha = thinness(n, tree, edges, z)
        assert opt <= tour_cost(cost, tour) <= circ                       # shortcuts do not add cost
        assert circ <= sum(edge_cost(cost, e) for e in tree) + 2 * alpha * value  # the thin tree bound
    return value, opt


def test_example_values():
    value, x, edges, z, trees, probs = max_entropy_distribution(EXAMPLE)
    assert value == Fraction(25, 2)
    assert brute_opt(EXAMPLE) == 13
    assert {a for a, t in x.items() if t == 1} == {(0, 2), (4, 5)}
    assert all(t == Fraction(1, 2) for a, t in x.items() if a not in {(0, 2), (4, 5)})
    assert len(trees) == 130 == kirchhoff_count(6, edges)
    assert sorted(set(z)) == [Fraction(5, 12), Fraction(5, 6)]
    e_tree = sum(q * sum(edge_cost(EXAMPLE, edges[k]) for k in t) for t, q in zip(trees, probs))
    assert abs(e_tree - 55 / 6) < 1e-9
    check_instance(EXAMPLE)


def test_example_run():
    tree = [(0, 1), (0, 2), (1, 3), (1, 5), (4, 5)]
    tour, oriented, extra = tree_to_tour(EXAMPLE, tree)
    assert oriented == [(0, 1), (0, 2), (3, 1), (5, 1), (4, 5)]
    assert sorted(extra) == [(1, 0), (1, 0), (1, 4), (2, 3)]
    assert sum(EXAMPLE[u][v] for u, v in extra) == 12
    assert tour == [0, 1, 2, 3, 4, 5] and tour_cost(EXAMPLE, tour) == 20
    value, x, edges, z, trees, probs = max_entropy_distribution(EXAMPLE)
    assert thinness(6, tree, edges, z) == Fraction(9, 5)
    assert asadpour_tour(EXAMPLE, random.Random(2010)) == [0, 1, 2, 3, 4, 5]


def test_random_instances_against_brute_force():
    rng = random.Random(2017)
    for trial in range(12):
        n = 4 + trial % 3
        cost = random_instance(rng, n)
        value, opt = check_instance(cost)
        tour = asadpour_tour(cost, random.Random(trial))
        assert is_tour(tour, n) and tour_cost(cost, tour) >= opt


def test_balance_is_a_least_cost_transport():
    rng = random.Random(5)
    for _ in range(20):
        n = 6
        cost = random_instance(rng, n)
        arcs = [(rng.randrange(n), rng.randrange(n)) for _ in range(5)]
        arcs = [(u, v) for u, v in arcs if u != v]
        extra = balance_arcs(cost, arcs)
        bal = [0] * n
        for u, v in arcs + extra:
            bal[u] -= 1
            bal[v] += 1
        assert bal == [0] * n
        senders = sorted(u for u, _ in extra)
        takers = [v for v in range(n) for _ in range(max(0, sum(1 for a in arcs if a[0] == v) - sum(1 for a in arcs if a[1] == v)))]
        best = min((sum(cost[s][t] for s, t in zip(senders, perm)) for perm in itertools.permutations(takers)), default=0)
        assert sum(cost[u][v] for u, v in extra) == best


def test_lp_of_a_directed_cycle_and_its_reverse():
    n = 5
    cost = [[0 if i == j else (1 if j == (i + 1) % n else 10) for j in range(n)] for i in range(n)]
    value, x = atsp_lp(cost)
    assert value == 5 and x == {(i, (i + 1) % n): 1 for i in range(n)}


def test_directed_euler_circuit():
    arcs = [(0, 1), (1, 2), (2, 0), (0, 2), (2, 1), (1, 0)]
    walk = euler_circuit_directed(3, arcs)
    assert walk[0] == walk[-1] == 0 and len(walk) == 7
    assert sorted(zip(walk, walk[1:])) == sorted(arcs)
