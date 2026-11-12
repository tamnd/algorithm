# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-reweighted-belief-propagation/. The authors are listed in prov/638X2J.jsonl.

import math
import random
from fractions import Fraction

from tree_reweighted_belief_propagation import exact, grid_edges, ising, trw_bound, trw_bp, uniform_spanning_tree_rho

CYCLE = [(0, 1), (1, 2), (2, 3), (0, 3)]
K4 = [(i, j) for i in range(4) for j in range(i + 1, 4)]
GRID = grid_edges(3, 3)


def max_err(a, b):
    return max(abs(x - y) for u, v in zip(a, b) for x, y in zip(u, v))


def test_edge_appearance_probabilities():
    assert set(uniform_spanning_tree_rho(4, CYCLE).values()) == {Fraction(3, 4)}
    assert set(uniform_spanning_tree_rho(4, K4).values()) == {Fraction(1, 2)}
    rho = uniform_spanning_tree_rho(9, GRID)
    assert sum(rho.values()) == 8  # every spanning tree has n - 1 edges
    assert rho[(3, 4)] == Fraction(7, 12) and rho[(0, 1)] == Fraction(17, 24)
    tree = [(0, 1), (1, 2), (1, 3), (3, 4)]
    assert set(uniform_spanning_tree_rho(5, tree).values()) == {1}


def test_rho_one_on_a_tree_is_exact():
    rng = random.Random(1)
    tree = [(0, 1), (1, 2), (1, 3), (3, 4), (3, 5)]
    for _ in range(3):
        card, theta, pair = ising(6, [rng.uniform(-1, 1) for _ in range(6)],
                                  [(s, t, rng.uniform(-2, 2)) for s, t in tree])
        log_z, tau_x, _ = exact(card, theta, pair)
        b, tau, tau2, _, ok = trw_bp(card, theta, pair, tol=1e-13)
        assert ok and abs(b - log_z) < 1e-9 and max_err(tau, tau_x) < 1e-9


def test_upper_bound_by_enumeration():
    rng = random.Random(3)
    cases = [(4, CYCLE, 1.0), (4, K4, 2.0), (9, GRID, 2.0), (9, GRID, 0.5)]
    for n, edges, scale in cases:
        for _ in range(3):
            card, theta, pair = ising(n, [rng.uniform(-0.5, 0.5) for _ in range(n)],
                                      [(s, t, rng.uniform(-scale, scale)) for s, t in edges])
            log_z, tau_x, tau2_x = exact(card, theta, pair)
            b, _, _, _, ok = trw_bp(card, theta, pair)
            assert ok and b >= log_z - 1e-9
            # The exact marginals are feasible, and the tree-reweighted entropy is at least the true entropy.
            b_exact = trw_bound(card, theta, pair, uniform_spanning_tree_rho(n, edges), tau_x, tau2_x)
            assert log_z - 1e-9 <= b_exact <= b + 1e-7


def test_any_rho_in_the_spanning_tree_polytope_gives_a_bound():
    # Two spanning trees of the 4-cycle with probability 1/2: one without (0, 3), one without (1, 2).
    rho = {(0, 1): 1, (1, 2): 0.5, (2, 3): 1, (0, 3): 0.5}
    rng = random.Random(4)
    for _ in range(5):
        card, theta, pair = ising(4, [rng.uniform(-1, 1) for _ in range(4)],
                                  [(s, t, rng.uniform(-2, 2)) for s, t in CYCLE])
        b, _, _, _, ok = trw_bp(card, theta, pair, rho=rho)
        assert ok and b >= exact(card, theta, pair)[0] - 1e-9


def test_fixed_point_does_not_depend_on_the_start():
    rng = random.Random(6)
    card, theta, pair = ising(9, [rng.uniform(-0.5, 0.5) for _ in range(9)],
                              [(s, t, rng.uniform(-2, 2)) for s, t in GRID])
    b0, tau0, _, _, ok0 = trw_bp(card, theta, pair, tol=1e-12)
    nb = {}
    for s, t in pair:
        nb[(s, t)] = [rng.uniform(-3, 3), rng.uniform(-3, 3)]
        nb[(t, s)] = [rng.uniform(-3, 3), rng.uniform(-3, 3)]
    b1, tau1, _, _, ok1 = trw_bp(card, theta, pair, tol=1e-12, init=nb)
    assert ok0 and ok1 and abs(b0 - b1) < 1e-8 and max_err(tau0, tau1) < 1e-8


def test_page_example():
    card, theta, pair = ising(4, [0.2, -0.1, 0.3, 0.0], [(s, t, 1.0) for s, t in CYCLE])
    log_z, tau_x, _ = exact(card, theta, pair)
    b, tau, _, it, ok = trw_bp(card, theta, pair)
    assert ok and it == 165
    assert abs(log_z - 4.87295) < 1e-5 and abs(b - 4.96432) < 1e-5
    assert [round(p[1], 4) for p in tau] == [0.6609, 0.6478, 0.6693, 0.6564]
    assert [round(p[1], 4) for p in tau_x] == [0.6766, 0.6667, 0.6828, 0.6732]
    bethe, tau_b, _, _, ok_b = trw_bp(card, theta, pair, rho={e: 1 for e in pair})
    assert ok_b and abs(bethe - 4.64550) < 1e-5 and bethe < log_z  # not a bound
    assert round(tau_b[0][1], 4) == 0.7977
    assert math.isclose(sum(tau[0]), 1.0)
