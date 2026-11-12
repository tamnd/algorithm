# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/residual-belief-propagation/. The authors are listed in prov/BP947G.jsonl.

import random

from residual_belief_propagation import (candidate, exact_marginals, ising, neighbors, residual, residual_bp,
                                         synchronous_bp)

CYCLE = [(0, 1, 0.5), (1, 3, 0.5), (3, 2, 0.5), (2, 0, 0.5)]
K4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def grid(rng, side, hs, js):
    idx = lambda r, c: r * side + c
    edges = [(idx(r, c), idx(r, c + 1)) for r in range(side) for c in range(side - 1)]
    edges += [(idx(r, c), idx(r + 1, c)) for r in range(side - 1) for c in range(side)]
    return [rng.uniform(-hs, hs) for _ in range(side * side)], [(i, j, rng.uniform(-js, js)) for i, j in edges]


def max_err(a, b):
    return max(abs(x - y) for u, v in zip(a, b) for x, y in zip(u, v))


def test_same_fixed_point_as_synchronous_bp():
    rng = random.Random(11)
    for js in (0.5, 1.0):
        for _ in range(5):
            fields, couplings = grid(rng, 3, 0.5, js)
            card, unary, pair = ising(9, fields, couplings)
            b1, _, _, ok1 = residual_bp(card, unary, pair, tol=1e-12)
            b2, _, _, ok2 = synchronous_bp(card, unary, pair, tol=1e-12)
            assert ok1 and ok2
            assert max_err(b1, b2) < 1e-9


def test_exact_and_finite_on_a_tree():
    rng = random.Random(3)
    for _ in range(5):
        fields = [rng.uniform(-1, 1) for _ in range(7)]
        couplings = [(0, 1, 0.8), (1, 2, -0.6), (1, 3, 1.2), (3, 4, 0.4), (0, 5, -1.0), (5, 6, 0.9)]
        card, unary, pair = ising(7, fields, couplings)
        # With tol = 0 the loop stops only when every residual is exactly 0.
        b, _, updates, ok = residual_bp(card, unary, pair, tol=0.0)
        assert ok and updates < 100
        assert max_err(b, exact_marginals(card, unary, pair)) < 1e-12


def test_all_residuals_are_small_at_the_end():
    rng = random.Random(4)
    fields, couplings = grid(rng, 3, 0.5, 1.0)
    card, unary, pair = ising(9, fields, couplings)
    _, m, _, ok = residual_bp(card, unary, pair, tol=1e-9)
    assert ok
    nb = neighbors(card, pair)
    assert max(residual(candidate(card, unary, pair, nb, m, *e), m[e]) for e in m) <= 1e-9


def test_update_counts_on_the_page_example():
    card, unary, pair = ising(4, [0.3, -0.2, 0.1, 0.0], CYCLE)
    assert residual_bp(card, unary, pair, tol=1e-6)[2:] == (56, True)
    assert synchronous_bp(card, unary, pair, tol=1e-6)[2:] == (120, True)
    b, _, n, ok = residual_bp(card, unary, pair, tol=1e-10)
    assert ok and n == 102
    assert abs(b[0][1] - 0.6315) < 1e-4


def test_fewer_updates_than_synchronous_on_seeded_grids():
    rng = random.Random(11)
    for _ in range(10):
        fields, couplings = grid(rng, 3, 0.5, 0.5)
        card, unary, pair = ising(9, fields, couplings)
        _, _, n1, ok1 = residual_bp(card, unary, pair)
        _, _, n2, ok2 = synchronous_bp(card, unary, pair)
        assert ok1 and ok2 and n1 < n2


def test_reports_failure_on_a_frustrated_k4():
    card, unary, pair = ising(4, [0.5, 0.0, 0.0, 0.0], [(i, j, -2.0) for i, j in K4])
    _, _, updates, ok = residual_bp(card, unary, pair, max_updates=5000)
    assert not ok and updates == 5000
