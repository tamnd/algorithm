# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/network-simplex/. The authors are listed in prov/SJBDWT.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from network_simplex import network_simplex

# s, a, b, t = 0 .. 3; edges (u, v, capacity, cost)
EXAMPLE = [(0, 1, 3, 1), (0, 2, 2, 4), (1, 2, 2, 1), (1, 3, 2, 5), (2, 3, 3, 1)]


def check(n, edges, supply, cost, flow):
    net = [0] * n
    for (u, v, c, k), x in zip(edges, flow):
        assert 0 <= x <= c
        net[u] += x
        net[v] -= x
    assert net == list(supply)
    assert cost == sum(k * x for (_, _, _, k), x in zip(edges, flow))


def brute(n, edges, supply):
    """Independent oracle: try every integral flow; integer data has an integral optimum."""
    best = None
    for flow in itertools.product(*(range(c + 1) for _, _, c, _ in edges)):
        net = [0] * n
        for (u, v, _, _), x in zip(edges, flow):
            net[u] += x
            net[v] -= x
        if net == list(supply):
            cost = sum(k * x for (_, _, _, k), x in zip(edges, flow))
            best = cost if best is None else min(best, cost)
    return best


def test_example_by_value() -> None:
    costs = []
    for d in range(6):
        cost, flow = network_simplex(4, EXAMPLE, [d, 0, 0, -d])
        check(4, EXAMPLE, [d, 0, 0, -d], cost, flow)
        costs.append(cost)
    assert costs == [0, 3, 6, 11, 17, 25]
    assert network_simplex(4, EXAMPLE, [6, 0, 0, -6]) is None


def test_zero_capacity_no_path_and_bad_input() -> None:
    assert network_simplex(2, [(0, 1, 0, -5)], [0, 0]) == (0, [0])
    assert network_simplex(2, [(0, 1, 0, 1)], [1, -1]) is None
    assert network_simplex(3, [(0, 1, 4, 1)], [1, 0, -1]) is None
    assert network_simplex(2, [(0, 1, 4, 1)], [1, 0]) is None
    with pytest.raises(ValueError):
        network_simplex(2, [(0, 1, -1, 1)], [0, 0])


def test_negative_cycle_antiparallel_and_loops() -> None:
    edges = [(0, 1, 2, -3), (1, 0, 3, 1), (0, 0, 4, -1), (1, 1, 2, 2)]
    cost, flow = network_simplex(2, edges, [0, 0])
    assert cost == -4 - 4
    assert flow == [2, 2, 4, 0]
    check(2, edges, [0, 0], cost, flow)


def test_real_data() -> None:
    edges = [(0, 1, Fraction(3, 2), Fraction(1, 3)), (0, 2, Fraction(1, 2), Fraction(-1, 7)), (2, 1, 2, Fraction(1, 5)), (1, 3, 3, 1)]
    supply = [Fraction(2), 0, 0, Fraction(-2)]
    cost, flow = network_simplex(4, edges, supply)
    assert flow == [Fraction(3, 2), Fraction(1, 2), Fraction(1, 2), 2]
    check(4, edges, supply, cost, flow)


def test_random_against_brute_force() -> None:
    rng = random.Random(77)
    for _ in range(600):
        n = rng.randint(2, 5)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 3), rng.randint(-4, 6)) for _ in range(rng.randint(0, 6))]
        supply = [0] * n
        for _ in range(rng.randint(0, 3)):
            u, v = rng.randrange(n), rng.randrange(n)
            supply[u] += 1
            supply[v] -= 1
        result = network_simplex(n, edges, supply)
        expected = brute(n, edges, supply)
        if expected is None:
            assert result is None
        else:
            cost, flow = result
            assert cost == expected
            check(n, edges, supply, cost, flow)
