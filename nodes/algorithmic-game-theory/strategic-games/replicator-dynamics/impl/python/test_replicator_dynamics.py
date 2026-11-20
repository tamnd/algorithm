# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/replicator-dynamics/. The authors are listed in prov/DA7ATV.jsonl.

import math
import random
from fractions import Fraction as F

from replicator_dynamics import fitness, mean_fitness, replicator_field, replicator_rk4, rk4_step

HAWK_DOVE = [[-1, 2], [0, 1]]
PRISONERS_DILEMMA = [[3, 0], [5, 1]]  # strategies C, D
RPS = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
ZEEMAN = [[0, 6, -4], [-3, 0, 5], [-1, 3, 0]]


def dist(x, y):
    return max(abs(a - b) for a, b in zip(x, y))


def test_logistic_closed_form() -> None:
    # With A = [[1, 1], [0, 0]], x_1' = x_1 (1 - x_1), the logistic equation.
    A = [[1, 1], [0, 0]]
    h, steps = 0.01, 500
    for x0 in (0.01, 0.3, 0.9):
        path = replicator_rk4(A, [x0, 1 - x0], h, steps, record=True)
        for k in (100, 250, 500):
            t = k * h
            exact = x0 * math.exp(t) / (1 - x0 + x0 * math.exp(t))
            assert abs(path[k][0] - exact) < 1e-9
            assert abs(sum(path[k]) - 1) < 1e-12


def test_hawk_dove_goes_to_the_ess() -> None:
    # q' = q (1 - q) (1 - 2q), so every interior start goes to q = 1/2.
    for q0 in (0.05, 0.4, 0.9):
        x = replicator_rk4(HAWK_DOVE, [q0, 1 - q0], 0.05, 1200)
        assert dist(x, [0.5, 0.5]) < 1e-9
    # The vertices are rest points, but not stable.
    assert replicator_field(HAWK_DOVE, [1.0, 0.0]) == [0.0, 0.0]


def test_prisoners_dilemma_cooperation_dies_out() -> None:
    path = replicator_rk4(PRISONERS_DILEMMA, [0.99, 0.01], 0.05, 800, record=True)
    shares = [x[0] for x in path]
    assert all(b < a for a, b in zip(shares, shares[1:]))
    assert shares[-1] < 1e-6


def test_rock_paper_scissors_keeps_the_product() -> None:
    x0 = [0.5, 0.3, 0.2]
    p0 = x0[0] * x0[1] * x0[2]
    path = replicator_rk4(RPS, x0, 0.01, 3000, record=True)
    for x in path[::100]:
        assert abs(x[0] * x[1] * x[2] - p0) < 1e-8 * p0
    # The orbit is closed and does not approach the centre.
    assert min(dist(x, [1 / 3] * 3) for x in path) > 0.05


def test_rock_paper_scissors_with_a_cost_or_bonus_for_ties() -> None:
    for eps in (0.2, -0.2):
        A = [[RPS[i][j] - (eps if i == j else 0) for j in range(3)] for i in range(3)]
        path = replicator_rk4(A, [0.5, 0.3, 0.2], 0.05, 8000, record=True)
        prods = [x[0] * x[1] * x[2] for x in path]
        if eps > 0:  # the centre is an ESS: the product rises to 1/27
            assert all(b >= a - 1e-13 for a, b in zip(prods, prods[1:]))
            assert dist(path[-1], [1 / 3] * 3) < 1e-6
        else:  # the product falls and the orbit moves to the boundary
            assert all(b <= a + 1e-13 for a, b in zip(prods, prods[1:]))
            assert prods[-1] < 1e-3


def test_fisher_mean_fitness_rises_at_twice_the_variance() -> None:
    rng = random.Random(3)
    for _ in range(5):
        n = 4
        A = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                A[i][j] = A[j][i] = rng.uniform(-1, 1)
        w = [rng.uniform(0.1, 1) for _ in range(n)]
        x = [v / sum(w) for v in w]
        h = 1e-3
        for _ in range(4):
            f, phi = fitness(A, x), mean_fitness(A, x)
            var = sum(xi * (fi - phi) ** 2 for xi, fi in zip(x, f))
            slope = (mean_fitness(A, rk4_step(A, x, h)) - mean_fitness(A, rk4_step(A, x, -h))) / (2 * h)
            assert abs(slope - 2 * var) < 1e-6
            x = replicator_rk4(A, x, 0.05, 100)
        path = replicator_rk4(A, x, 0.05, 400, record=True)
        phis = [mean_fitness(A, y) for y in path]
        assert all(b >= a - 1e-12 for a, b in zip(phis, phis[1:]))


def test_zeeman_stable_rest_point_that_is_not_an_ess() -> None:
    c = [F(1, 3)] * 3
    Ac = [sum(F(a) * x for a, x in zip(row, c)) for row in ZEEMAN]
    assert Ac == [F(2, 3)] * 3  # the centre is a rest point and a Nash equilibrium
    # The mutant y = c + d z with z = (1, 0, -1) does better against itself:
    # u(c, y) - u(y, y) = -d^2 z^T A z, and z^T A z = 5.
    z = [1, 0, -1]
    for d in (F(1, 10), F(1, 100)):
        y = [ci + d * zi for ci, zi in zip(c, z)]
        Ay = [sum(F(a) * v for a, v in zip(row, y)) for row in ZEEMAN]
        gap = sum((ci - yi) * v for ci, yi, v in zip(c, y, Ay))
        assert gap == -5 * d * d
    # Yet the centre attracts nearby orbits, and e_1, a strict equilibrium, attracts others.
    x = replicator_rk4(ZEEMAN, [0.4, 0.3, 0.3], 0.05, 2000)
    assert dist(x, [1 / 3] * 3) < 1e-9
    x = replicator_rk4(ZEEMAN, [0.8, 0.1, 0.1], 0.05, 2000)
    assert dist(x, [1.0, 0.0, 0.0]) < 1e-9


def test_rk4_order_four() -> None:
    # Halving the step divides the error at t = 2 by about 16.
    A = [[1, 1], [0, 0]]
    x0 = 0.2
    exact = x0 * math.exp(2) / (1 - x0 + x0 * math.exp(2))
    e1 = abs(replicator_rk4(A, [x0, 1 - x0], 0.2, 10)[0] - exact)
    e2 = abs(replicator_rk4(A, [x0, 1 - x0], 0.1, 20)[0] - exact)
    assert 12 < e1 / e2 < 20
