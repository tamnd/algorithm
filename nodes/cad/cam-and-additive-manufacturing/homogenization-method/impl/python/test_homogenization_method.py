# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/homogenization-method/. The authors are listed in prov/MKGHFA.jsonl.

import math
import random
from fractions import Fraction as F

from homogenization_method import (
    bar_lower_bound,
    bar_problem,
    best_angle,
    cell_tensor,
    complementary,
    density,
    hole_cell,
    homogenize,
    make_table,
    sensitivities,
    sink_problem,
    solve,
    tensors_of,
)

TABLE = make_table()


def harmonic(values):
    return len(values) / sum(1 / v for v in values)


def arithmetic(values):
    return sum(values) / len(values)


def test_laminate_is_harmonic_across_and_arithmetic_along() -> None:
    rng = random.Random(1)
    for _ in range(8):
        n = rng.randint(2, 6)
        cols = [F(rng.randint(1, 9), rng.randint(1, 3)) for _ in range(n)]
        layered_in_x = [[cols[c] for c in range(n)] for _ in range(n)]  # a depends on x only
        a = cell_tensor(layered_in_x)
        assert a[0][0] == harmonic(cols)  # across the layers
        assert a[1][1] == arithmetic(cols)  # along the layers
        assert a[0][1] == 0 and a[1][0] == 0
        layered_in_y = [[cols[r]] * n for r in range(n)]
        b = cell_tensor(layered_in_y)
        assert b[0][0] == arithmetic(cols) and b[1][1] == harmonic(cols)


def test_wiener_bounds_on_random_cells() -> None:
    rng = random.Random(2)
    for _ in range(30):
        n = rng.randint(2, 4)
        a = [[F(rng.randint(1, 20), rng.randint(1, 4)) for _ in range(n)] for _ in range(n)]
        values = [v for row in a for v in row]
        lo, hi = harmonic(values), arithmetic(values)
        t = cell_tensor(a)
        assert t[0][1] == t[1][0]
        # t - lo I and hi I - t are positive semidefinite (2 x 2: diagonal and determinant)
        for s, m in ((1, lo), (-1, hi)):
            d11, d22, d12 = s * (t[0][0] - m), s * (t[1][1] - m), s * t[0][1]
            assert d11 >= 0 and d22 >= 0 and d11 * d22 - d12 * d12 >= 0


def test_one_element_checkerboard_is_as_stiff_as_the_arithmetic_mean() -> None:
    a = [[F(1), F(10)], [F(10), F(1)]]
    t = cell_tensor(a)
    assert t[0][0] == t[1][1] == F(11, 2) and t[0][1] == 0
    # Refining by 2 nests the element spaces, so the values fall. The exact value is sqrt(10).
    vals = []
    for m in (1, 2, 4, 8):
        n = 2 * m
        cell = [[1.0 if (r // m + c // m) % 2 == 0 else 10.0 for c in range(n)] for r in range(n)]
        vals.append(cell_tensor(cell)[0][0])
    assert all(x > y for x, y in zip(vals, vals[1:]))
    assert vals[-1] > math.sqrt(10)
    assert abs(vals[-1] - 3.444) < 1e-3  # measured: still 9% above sqrt(10) at 16 x 16


def test_hole_cell_symmetry_bounds_and_monotonicity() -> None:
    g = TABLE["grid"]
    a11, a22, void = TABLE["a11"], TABLE["a22"], TABLE["void"]
    for i in range(g + 1):
        for j in range(g + 1):
            mu, ga = i / g, j / g
            rho = density(mu, ga)
            assert a11[i][j] <= rho + (1 - rho) * void + 1e-12
            assert a22[i][j] <= rho + (1 - rho) * void + 1e-12
            assert a11[i][j] >= 1 / (rho + (1 - rho) / void) - 1e-12
            if i < g:
                assert a11[i + 1][j] >= a11[i][j] - 1e-12 and a22[i + 1][j] >= a22[i][j] - 1e-12
            if j < g:
                assert a11[i][j + 1] >= a11[i][j] - 1e-12 and a22[i][j + 1] >= a22[i][j] - 1e-12
    t = cell_tensor(hole_cell(0.6, 0.2, 10))
    s = cell_tensor(hole_cell(0.2, 0.6, 10))
    assert abs(t[0][1]) < 1e-12 and abs(t[0][0] - s[1][1]) < 1e-12 and abs(t[1][1] - s[0][0]) < 1e-12


def test_sensitivities_against_central_differences() -> None:
    rng = random.Random(3)
    prob = sink_problem(5, 4)
    n = prob.nx * prob.ny
    mu = [rng.choice([0.1, 0.3, 0.5, 0.7]) for _ in range(n)]
    ga = [rng.choice([0.1, 0.3, 0.5, 0.7]) for _ in range(n)]
    th = [rng.uniform(0, math.pi) for _ in range(n)]
    u, _ = solve(prob, tensors_of(TABLE, mu, ga, th))
    dmu, dga = sensitivities(prob, TABLE, u, mu, ga, th)
    h = 1e-6  # stays inside one interpolation cell
    for e in range(n):
        for d, var in ((dmu, mu), (dga, ga)):
            vp, vm = list(var), list(var)
            vp[e] += h
            vm[e] -= h
            if var is mu:
                cp = solve(prob, tensors_of(TABLE, vp, ga, th))[1]
                cm = solve(prob, tensors_of(TABLE, vm, ga, th))[1]
            else:
                cp = solve(prob, tensors_of(TABLE, mu, vp, th))[1]
                cm = solve(prob, tensors_of(TABLE, mu, vm, th))[1]
            fd = (cp - cm) / (2 * h)
            assert abs(d[e] - fd) <= 1e-4 * abs(fd) + 1e-6


def test_angle_step_minimizes_the_complementary_energy_and_never_raises_the_compliance() -> None:
    rng = random.Random(4)
    for _ in range(100):
        ue = [rng.uniform(-1, 1) for _ in range(4)]
        b = (rng.uniform(0.1, 1), rng.uniform(-0.05, 0.05), rng.uniform(0.1, 1))
        a11, a22 = rng.uniform(0.01, 1), rng.uniform(0.01, 1)
        best = complementary(ue, b, a11, a22, best_angle(ue, b, a11, a22))
        for k in range(64):
            assert best <= complementary(ue, b, a11, a22, k * math.pi / 32) + 1e-12
    prob = sink_problem(8, 6)
    n = prob.nx * prob.ny
    mu = [rng.choice([0.0, 0.2, 0.4, 0.6]) for _ in range(n)]
    ga = [rng.choice([0.0, 0.2, 0.4]) for _ in range(n)]
    th = [rng.uniform(0, math.pi) for _ in range(n)]
    last = math.inf
    for _ in range(8):
        tens = tensors_of(TABLE, mu, ga, th)
        u, c = solve(prob, tens)
        assert c <= last * (1 + 1e-12)
        last = c
        th = []
        for e, ids in prob.elements():
            a11 = TABLE["a11"][round(mu[e] * 5)][round(ga[e] * 5)]
            a22 = TABLE["a22"][round(mu[e] * 5)][round(ga[e] * 5)]
            th.append(best_angle([u[p] for p in ids], tens[e], a11, a22))


def test_bar_reaches_the_laminate_bound() -> None:
    prob = bar_problem(12, 6)
    fraction = 0.4
    volume = fraction * 72
    mu, ga, th, hist = homogenize(prob, fraction, TABLE)
    assert sum(density(a, b) for a, b in zip(mu, ga)) <= volume + 1e-9
    c = solve(prob, tensors_of(TABLE, mu, ga, th))[1]
    bound = bar_lower_bound(prob, 1.0, volume, TABLE["void"])
    assert c >= bound * (1 - 1e-12)  # proved: no design does better
    assert c <= bound * 1.001  # measured: the method finds the laminate along the flux
    assert hist[0] > 1.5 * c  # the start (square holes) is much softer


def test_sink_problem_feasible_and_improves() -> None:
    prob = sink_problem(10, 6)
    mu, ga, th, hist = homogenize(prob, 0.4, TABLE, maxit=30)
    assert all(0 <= v <= 1 for v in mu + ga)
    assert sum(density(a, b) for a, b in zip(mu, ga)) <= 0.4 * 60 + 1e-9
    assert solve(prob, tensors_of(TABLE, mu, ga, th))[1] < 0.6 * hist[0]
