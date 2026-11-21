# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-step-late-algorithm/. The authors are listed in prov/J6NCZD.jsonl.

import math
import random
from fractions import Fraction as F

from one_step_late_algorithm import back, forward, grid_edges, objective, osl, penalty, penalty_grad

# The two-pixel example of the page: A = I, y = (1, 3), one edge of weight 1.
ROWS2 = [[(0, F(1))], [(1, F(1))]]
Y2 = [F(1), F(3)]
E2 = [(0, 1, 1)]


def _iterates(beta, iters):
    seen = []
    try:
        osl(ROWS2, 2, Y2, beta, E2, iters=iters, callback=lambda k, x: seen.append(x))
    except ValueError:
        return seen, True
    return seen, False


def _random_problem(rng, n):
    rows = []
    for _ in range(3 * n * n):
        row = [(j, rng.uniform(0.1, 1.0)) for j in range(n * n) if rng.random() < 0.4]
        rows.append(row or [(rng.randrange(n * n), 0.5)])
    xt = [rng.uniform(0.5, 2.0) for _ in range(n * n)]
    lam = forward(rows, xt)
    y = []
    for v in lam:
        # Poisson sample by the product method; the means here are small
        k, p, limit = 0, rng.random(), math.exp(-5.0 * v)
        while p > limit:
            k += 1
            p *= rng.random()
        y.append(k)
    return [[(j, 5.0 * w) for j, w in row] for row in rows], y


def test_small_beta_exact_iterates_and_limit() -> None:
    seen, failed = _iterates(F(1, 10), 4)
    assert not failed
    assert seen == [[F(1), F(3)], [F(5, 4), F(5, 2)], [F(8, 7), F(8, 3)], [F(105, 89), F(315, 121)]]
    x = osl([[(0, 1.0)], [(1, 1.0)]], 2, [1.0, 3.0], 0.1, E2, iters=200)
    assert abs(x[0] - 1.1696403991) < 1e-9 and abs(x[1] - 2.6200041112) < 1e-9
    # the penalized KKT equations: y_j / x_j - 1 - beta dR/dx_j = 0
    g = penalty_grad(x, E2)
    assert abs(1 / x[0] - 1 - 0.1 * g[0]) < 1e-12 and abs(3 / x[1] - 1 - 0.1 * g[1]) < 1e-12


def test_medium_beta_oscillates_and_fails() -> None:
    seen, failed = _iterates(F(3, 10), 10)
    assert seen[:4] == [[F(1), F(3)], [F(5, 2), F(15, 8)], [F(16, 19), F(48, 13)], [F(1235, 179), F(3705, 2291)]]
    assert failed and len(seen) == 4
    obj = [objective(ROWS2, Y2, x, F(3, 10), E2) for x in seen]
    assert obj[1] < obj[0] and obj[3] < obj[2]


def test_large_beta_gives_a_nonpositive_denominator() -> None:
    seen, failed = _iterates(F(1), 5)
    assert failed and seen == [[F(1), F(3)]]
    x = seen[0]
    den0 = 1 + 1 * penalty_grad(x, E2)[0]
    assert den0 == -1 and x[0] * (Y2[0] / x[0]) / den0 == -1
    seen, failed = _iterates(F(1, 2), 5)
    assert failed and 1 + F(1, 2) * penalty_grad(seen[0], E2)[0] == 0


def test_beta_zero_is_mlem() -> None:
    a = [[1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 1]]
    rows = [[(j, F(w)) for j, w in enumerate(r) if w] for r in a]
    x = osl(rows, 4, [F(v) for v in (3, 7, 4, 6, 5)], F(0), grid_edges(2), iters=1, x0=[F(1)] * 4)
    assert x == [F(2), F(9, 4), F(11, 4), F(3)]


def test_fixed_point_satisfies_the_penalized_kkt_conditions() -> None:
    rng = random.Random(6)
    n = 4
    rows, y = _random_problem(rng, n)
    edges = grid_edges(n)
    beta = 0.05
    x = osl(rows, n * n, y, beta, edges, iters=2500)
    assert all(v > 0 for v in x)
    ybar = forward(rows, x)
    grad_l = back(rows, [yi / li for yi, li in zip(y, ybar)], n * n)
    s = back(rows, [1.0] * len(rows), n * n)
    u = penalty_grad(x, edges)
    for gj, sj, uj in zip(grad_l, s, u):
        assert abs(gj - sj - beta * uj) < 1e-8 * sj


def test_penalty_gradient_by_finite_differences() -> None:
    rng = random.Random(1)
    edges = [(j, k, rng.uniform(0.5, 2.0)) for j, k, _ in grid_edges(3)]
    x = [rng.uniform(0.0, 3.0) for _ in range(9)]
    g = penalty_grad(x, edges)
    h = 1e-6
    for j in range(9):
        xp, xm = list(x), list(x)
        xp[j] += h
        xm[j] -= h
        assert abs((penalty(xp, edges) - penalty(xm, edges)) / (2 * h) - g[j]) < 1e-6


def test_projector_adjoint() -> None:
    rng = random.Random(2)
    rows, _ = _random_problem(rng, 3)
    x = [rng.gauss(0.0, 1.0) for _ in range(9)]
    v = [rng.gauss(0.0, 1.0) for _ in range(len(rows))]
    ax, atv = forward(rows, x), back(rows, v, 9)
    gap = abs(sum(p * q for p, q in zip(ax, v)) - sum(p * q for p, q in zip(x, atv)))
    assert gap <= 1e-10 * math.sqrt(sum(p * p for p in ax) * sum(q * q for q in v))
