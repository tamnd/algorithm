# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/separable-paraboloidal-surrogates/. The authors are listed in prov/DG54BX.jsonl.

import math
import random

import imgkit as ik
from separable_paraboloidal_surrogates import (
    back,
    forward,
    gradient,
    grid_edges,
    h,
    h_prime,
    objective,
    optimal_curvature,
    penalty,
    sps,
)

# The example of the page: a 2 x 2 image, 5 rays, background 0.5 in each bin.
A5 = [[1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 1]]
ROWS5 = [[(j, float(w)) for j, w in enumerate(r) if w] for r in A5]
Y5 = [3.0, 7.0, 4.0, 6.0, 5.0]
B5 = [0.5] * 5


def _random_problem(rng, n, zeros=0):
    rows = []
    for _ in range(3 * n * n):
        row = [(j, rng.uniform(0.1, 1.0)) for j in range(n * n) if rng.random() < 0.4]
        rows.append(row or [(rng.randrange(n * n), 0.5)])
    xt = [rng.uniform(0.5, 2.0) for _ in range(n * n)]
    for j in rng.sample(range(n * n), zeros):
        xt[j] = 0.0
    b = [rng.uniform(0.2, 1.0) for _ in rows]
    lam = forward(rows, xt)
    y = [ik.poisson_sample(rng, 3.0 * (li + bi)) / 3.0 for li, bi in zip(lam, b)]
    return rows, y, b


def _parabola(yi, bi, l, c, t):
    return h(yi, bi, l) + h_prime(yi, bi, l) * (t - l) + c / 2 * (t - l) ** 2


def test_optimal_curvature_majorizes_and_is_tight() -> None:
    rng = random.Random(3)
    grid = [0.02 * k for k in range(1500)]
    for _ in range(40):
        yi, bi, l = rng.uniform(0.5, 20.0), rng.uniform(0.05, 3.0), rng.choice([0.0, rng.uniform(0.01, 25.0)])
        c = optimal_curvature(yi, bi, l)
        for t in grid:
            assert _parabola(yi, bi, l, c, t) >= h(yi, bi, t) - 1e-9 * (1 + abs(h(yi, bi, t)))
        if l > 0:
            # tight: q(0) = h(0), so a smaller curvature fails at t = 0
            assert abs(_parabola(yi, bi, l, c, 0.0) - h(yi, bi, 0.0)) < 1e-9 * (1 + abs(h(yi, bi, 0.0)))
            assert _parabola(yi, bi, l, 0.99 * c, 0.0) < h(yi, bi, 0.0)
        else:
            assert c == yi / bi ** 2
    assert optimal_curvature(0.0, 1.0, 5.0) == 0.0


def test_separable_surrogate_lies_above_the_cost() -> None:
    rng = random.Random(4)
    rows, y, b = _random_problem(rng, 3)
    edges = [(j, k, rng.uniform(0.5, 2.0)) for j, k, _ in grid_edges(3)]
    beta = 0.7
    x = [rng.uniform(0.1, 3.0) for _ in range(9)]
    lines = forward(rows, x)
    curv = [optimal_curvature(yi, bi, li) for yi, bi, li in zip(y, b, lines)]
    asum = [sum(w for _, w in row) for row in rows]

    def surrogate(z):
        # De Pierro split: [A z]_i = sum_j (a_ij / a_i) (a_i (z_j - x_j) + l_i)
        total = 0.0
        for row, yi, bi, li, ci, ai in zip(rows, y, b, lines, curv, asum):
            total += sum(w / ai * _parabola(yi, bi, li, ci, ai * (z[j] - x[j]) + li) for j, w in row)
        for j, k, w in edges:
            m = x[j] + x[k]
            total += beta * w / 2 * ((2 * z[j] - m) ** 2 + (2 * z[k] - m) ** 2) / 2
        return total

    assert abs(surrogate(x) - objective(rows, y, x, beta, edges, b)) < 1e-9
    for _ in range(200):
        z = [rng.uniform(0.0, 4.0) for _ in range(9)]
        assert surrogate(z) >= objective(rows, y, z, beta, edges, b) - 1e-9
    # one SPS step is the minimizer of the surrogate over z >= 0
    x1 = sps(rows, 9, y, b, beta, edges, iters=1, x0=x)
    s1 = surrogate(x1)
    for _ in range(200):
        z = [max(0.0, v + rng.gauss(0.0, 0.05)) for v in x1]
        assert surrogate(z) >= s1 - 1e-9


def test_worked_example() -> None:
    x1 = sps(ROWS5, 4, Y5, B5, iters=1, x0=[1.0] * 4)
    for got, want in zip(x1, [1.1853137810, 1.2196311478, 1.2695473178, 1.2882658815]):
        assert abs(got - want) < 1e-9
    # these data are consistent: A x + b = y at x = (0.75, 1.75, 2.75, 3.75)
    x = sps(ROWS5, 4, Y5, B5, iters=600, x0=[1.0] * 4)
    assert max(abs(p - q) for p, q in zip(x, [0.75, 1.75, 2.75, 3.75])) < 1e-9


def test_cost_does_not_increase_on_a_phantom() -> None:
    n = 12
    rows = ik.parallel_beam_matrix(n, [math.pi * a / 10 for a in range(10)], 17)
    xt = ik.flatten(ik.disk_phantom(n, 0.6))
    rows = [[(j, 50.0 * w) for j, w in row] for row in rows]
    b = [1.0] * len(rows)
    rng = random.Random(7)
    y = [ik.poisson_sample(rng, li + 1.0) for li in forward(rows, xt)]
    edges = grid_edges(n)
    for beta in (0.0, 20.0):
        costs = []
        sps(rows, n * n, y, b, beta, edges, iters=60,
            callback=lambda k, x: costs.append((objective(rows, y, x, beta, edges, b), min(x))))
        assert all(m >= 0.0 for _, m in costs)
        assert all(q <= p + 1e-9 * abs(p) for (p, _), (q, _) in zip(costs, costs[1:]))


def test_limit_satisfies_the_kkt_conditions() -> None:
    rng = random.Random(5)
    rows, y, b = _random_problem(rng, 3, zeros=4)
    edges = grid_edges(3)
    beta = 0.3
    x = sps(rows, 9, y, b, beta, edges, iters=3000)
    g = gradient(rows, y, x, beta, edges, b)
    assert any(v == 0.0 for v in x)
    for xj, gj in zip(x, g):
        if xj > 0:
            assert abs(gj) < 1e-7
        else:
            assert gj > -1e-7


def test_gradient_by_finite_differences() -> None:
    rng = random.Random(1)
    rows, y, b = _random_problem(rng, 3)
    edges = [(j, k, rng.uniform(0.5, 2.0)) for j, k, _ in grid_edges(3)]
    x = [rng.uniform(0.2, 3.0) for _ in range(9)]
    g = gradient(rows, y, x, 0.8, edges, b)
    eps = 1e-6
    for j in range(9):
        xp, xm = list(x), list(x)
        xp[j] += eps
        xm[j] -= eps
        fd = (objective(rows, y, xp, 0.8, edges, b) - objective(rows, y, xm, 0.8, edges, b)) / (2 * eps)
        assert abs(fd - g[j]) < 1e-5 * (1 + abs(g[j]))
    assert penalty([1.0, 3.0], [(0, 1, 2.0)]) == 4.0


def test_counts_without_background_are_rejected() -> None:
    try:
        sps(ROWS5, 4, Y5, [0.0] * 5, iters=1)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_projector_adjoint() -> None:
    rng = random.Random(2)
    rows = ik.parallel_beam_matrix(8, [math.pi * a / 6 for a in range(6)], 11)
    x = [rng.gauss(0.0, 1.0) for _ in range(64)]
    v = [rng.gauss(0.0, 1.0) for _ in range(len(rows))]
    ax, atv = forward(rows, x), back(rows, v, 64)
    gap = abs(sum(p * q for p, q in zip(ax, v)) - sum(p * q for p, q in zip(x, atv)))
    assert gap <= 1e-10 * math.sqrt(sum(p * p for p in ax) * sum(q * q for q in v))
