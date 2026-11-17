# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rna-velocity/. The authors are listed in prov/MT9F81.jsonl.

import math
import random

import pytest

from rna_velocity import extrapolate, fit_gamma, solution, velocity

ALPHA, BETA, GAMMA = 2.0, 1.0, 0.5


def rk4(alpha, beta, gamma, u, s, t, steps=2000):
    h = t / steps

    def f(u, s):
        return alpha - beta * u, beta * u - gamma * s

    for _ in range(steps):
        k1 = f(u, s)
        k2 = f(u + h / 2 * k1[0], s + h / 2 * k1[1])
        k3 = f(u + h / 2 * k2[0], s + h / 2 * k2[1])
        k4 = f(u + h * k3[0], s + h * k3[1])
        u += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        s += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return u, s


def page_cells():
    cells = [(0.0, 0.0)]
    cells += [solution(ALPHA, BETA, GAMMA, 0, 0, t) for t in (0.5, 1, 2, 10)]
    cells += [solution(0, BETA, GAMMA, ALPHA / BETA, ALPHA / GAMMA, t) for t in (0.5, 1, 2, 10)]
    cells.append((ALPHA / BETA, ALPHA / GAMMA))
    return cells


def test_page_example():
    cells = page_cells()
    u = [c[0] for c in cells]
    s = [c[1] for c in cells]
    assert fit_gamma(u, s, 0.1) == pytest.approx(0.5, abs=1e-12)
    assert fit_gamma(u, s, 0.2) == pytest.approx(0.5033, abs=5e-5)
    assert fit_gamma(u, s, 0.5) == pytest.approx(0.4129, abs=5e-5)
    _, V = velocity([[x] for x in u], [[y] for y in s], 0.1)
    v = [row[0] for row in V]
    want = [0.0, 0.689, 0.955, 0.930, 0.027, -0.689, -0.955, -0.930, -0.027, 0.0]
    assert all(math.isclose(a, b, abs_tol=5e-4) for a, b in zip(v, want))


def test_solution_matches_rk4():
    rng = random.Random(1)
    for _ in range(20):
        a, b, g = rng.uniform(0, 5), rng.uniform(0.2, 3), rng.uniform(0.2, 3)
        u0, s0, t = rng.uniform(0, 3), rng.uniform(0, 3), rng.uniform(0, 5)
        assert solution(a, b, g, u0, s0, t) == pytest.approx(rk4(a, b, g, u0, s0, t), abs=1e-9)
    # The case beta = gamma has its own formula.
    for g in (0.3, 1.0, 2.5):
        assert solution(1.5, g, g, 0.4, 0.9, 3.0) == pytest.approx(rk4(1.5, g, g, 0.4, 0.9, 3.0), abs=1e-9)


def test_steady_state_limit():
    u, s = solution(ALPHA, BETA, GAMMA, 0.3, 7.0, 60.0)
    assert u == pytest.approx(ALPHA / BETA, abs=1e-9)
    assert s == pytest.approx(ALPHA / GAMMA, abs=1e-9)
    assert u - GAMMA / BETA * s == pytest.approx(0.0, abs=1e-9)


def test_sign_of_velocity_in_the_two_phases():
    rng = random.Random(2)
    for _ in range(20):
        a, g = rng.uniform(0.5, 5), rng.uniform(0.2, 3)
        for t in (0.01, 0.3, 1.0, 4.0, 15.0):
            u, s = solution(a, 1.0, g, 0, 0, t)
            assert u - g * s > 0
            u, s = solution(0, 1.0, g, a, a / g, t)
            assert u - g * s < 0


def test_repression_mirrors_induction():
    for t in (0.2, 1.0, 3.0):
        ui, si = solution(ALPHA, BETA, GAMMA, 0, 0, t)
        ur, sr = solution(0, BETA, GAMMA, ALPHA / BETA, ALPHA / GAMMA, t)
        assert ur == pytest.approx(ALPHA / BETA - ui)
        assert sr == pytest.approx(ALPHA / GAMMA - si)


def test_fit_is_exact_when_extreme_cells_are_at_steady_state():
    rng = random.Random(3)
    for _ in range(20):
        g = rng.uniform(0.1, 3)
        hi = rng.uniform(1, 10)
        s = [0.0, 0.0, hi, hi] + [rng.uniform(0.1, hi * 0.9) for _ in range(16)]
        u = [0.0, 0.0, g * hi, g * hi] + [rng.uniform(0, 5) for _ in range(16)]
        assert fit_gamma(u, s, 0.1) == pytest.approx(g, rel=1e-12)
        # The fit is the least squares slope through the origin.
        chosen = [0, 1, 2, 3]
        best = fit_gamma(u, s, 0.1)
        for d in (-1e-3, 1e-3):
            assert sum((u[i] - (best + d) * s[i]) ** 2 for i in chosen) > sum((u[i] - best * s[i]) ** 2 for i in chosen)


def test_velocity_is_ds_dt_and_extrapolation_is_first_order():
    for t in (0.5, 2.0):
        u, s = solution(ALPHA, 1.0, GAMMA, 0, 0, t)
        v = u - GAMMA * s
        errs = []
        for dt in (0.1, 0.05, 0.025):
            _, s2 = solution(ALPHA, 1.0, GAMMA, 0, 0, t + dt)
            pred = extrapolate([[s]], [[v]], dt)[0][0]
            errs.append(abs(s2 - pred))
        # Halving dt divides the error by about 4.
        assert 3.5 < errs[0] / errs[1] < 4.5 and 3.5 < errs[1] / errs[2] < 4.5


def test_simulation_measured():
    """A measurement: 20 genes, 300 cells over an on and an off phase, Gaussian noise of 10 percent."""
    rng = random.Random(1)
    genes, ncells = 20, 300
    times = [rng.uniform(0, 20) for _ in range(ncells)]
    U = [[0.0] * genes for _ in range(ncells)]
    S = [[0.0] * genes for _ in range(ncells)]
    D = [[0.0] * genes for _ in range(ncells)]
    true = []
    for j in range(genes):
        a, g = rng.uniform(1, 5), rng.uniform(0.3, 1.5)
        true.append(g)
        uon, son = solution(a, 1, g, 0, 0, 10.0)
        for i, t in enumerate(times):
            uu, ss = solution(a, 1, g, 0, 0, t) if t < 10 else solution(0, 1, g, uon, son, t - 10)
            D[i][j] = uu - g * ss
            U[i][j] = max(0.0, uu + rng.gauss(0, 0.1 * a))
            S[i][j] = max(0.0, ss + rng.gauss(0, 0.1 * a / g))
    gammas, V = velocity(U, S, 0.1)
    rel = sorted(abs(x - y) / y for x, y in zip(gammas, true))
    assert rel[len(rel) // 2] < 0.2
    big = [(i, j) for j in range(genes) for i in range(ncells)
           if abs(D[i][j]) > 0.2 * max(abs(D[k][j]) for k in range(ncells))]
    agree = sum((V[i][j] > 0) == (D[i][j] > 0) for i, j in big) / len(big)
    assert agree > 0.9


def test_errors():
    with pytest.raises(ValueError):
        solution(1, 0, 1, 0, 0, 1)
    with pytest.raises(ValueError):
        fit_gamma([1, 2], [1], 0.1)
    with pytest.raises(ValueError):
        fit_gamma([1, 2], [1, 2], 0.0)
    with pytest.raises(ValueError):
        fit_gamma([0, 0], [0, 0], 0.5)
