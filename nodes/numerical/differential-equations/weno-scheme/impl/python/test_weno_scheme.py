# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weno-scheme/. The authors are listed in prov/EF32M5.jsonl.

import math
from fractions import Fraction

import pytest

from weno_scheme import (LINEAR_WEIGHTS, candidates, cell_averages, nonlinear_weights, reconstruct,
                         smoothness, ssp_rk3_step, ssp_rk3_tableau, step_count, total_variation, weno,
                         weno_rhs)

GAUSS5 = [(-0.9061798459386640, 0.2369268850561891), (-0.5384693101056831, 0.4786286704993665),
          (0.0, 0.5688888888888889), (0.5384693101056831, 0.4786286704993665),
          (0.9061798459386640, 0.2369268850561891)]


def poly_averages(coeffs, m):
    """Exact Fraction cell averages of sum c_k x^k on cells [j, j+1], j = 0..m-1 (dx = 1)."""
    def antider(x):
        return sum(Fraction(c) * x ** (k + 1) / (k + 1) for k, c in enumerate(coeffs))
    return [antider(Fraction(j + 1)) - antider(Fraction(j)) for j in range(m)]


def test_linear_weights_give_the_fifth_order_upwind_formula():
    a, b, c, d, e = (Fraction(x) for x in (3, -1, 4, 1, -5))
    q = candidates([a, b, c, d, e])
    lin = sum(LINEAR_WEIGHTS[k] * q[k] for k in range(3))
    assert lin == (2 * a - 13 * b + 47 * c + 27 * d - 3 * e) / 60
    assert sum(LINEAR_WEIGHTS) == 1


def test_polynomial_exactness_of_candidates_and_of_the_linear_combination():
    # Cells [j, j+1] for j = 0..4; the reconstruction at the right edge of cell 2 is at x = 3.
    for deg in range(6):
        coeffs = [Fraction(k + 2, k + 1) for k in range(deg + 1)]
        v = poly_averages(coeffs, 5)
        exact = sum(c * Fraction(3) ** k for k, c in enumerate(coeffs))
        q = candidates(v)
        assert all(x == exact for x in q) == (deg <= 2)
        assert (reconstruct(v, variant="linear") == exact) == (deg <= 4)


def test_weights_form_a_convex_combination_and_are_near_linear_on_smooth_data():
    gaps = []
    for m in (40, 80, 160):
        v = cell_averages(lambda x: -math.cos(2 * math.pi * x) / (2 * math.pi), m)
        worst = 0.0
        for j in range(m):
            if abs(math.cos(2 * math.pi * (j + 1) / m)) < 0.2:
                continue  # stay away from the critical points of the sine
            w = nonlinear_weights(smoothness([v[(j + k) % m] for k in range(-2, 3)]))
            assert all(x >= 0 for x in w) and abs(sum(w) - 1) < 1e-14
            worst = max(worst, max(abs(w[k] - float(LINEAR_WEIGHTS[k])) for k in range(3)))
        gaps.append(worst)
    assert gaps[0] / gaps[1] > 3.5 and gaps[1] / gaps[2] > 3.5  # omega - d = O(dx^2)


def test_stencils_across_a_jump_get_negligible_weight():
    v = [0.0, 0.0, 0.0, 1.0, 1.0]
    w = nonlinear_weights(smoothness(v))
    assert w[1] < 1e-9 and w[2] < 1e-9
    assert abs(reconstruct(v)) < 1e-9
    assert abs(reconstruct(v, variant="z")) < 1e-9


def test_constant_state_is_preserved():
    r = weno([0.7] * 12, lambda u: 0.5 * u * u, 1.0, 0.1, 0.05, 0.3)
    assert max(abs(x - 0.7) for x in r.u) < 1e-14


def test_ssp_rk3_order_conditions_and_stability_polynomial_exactly():
    A, b, c = ssp_rk3_tableau()
    s = 3
    assert sum(b) == 1
    assert sum(b[i] * c[i] for i in range(s)) == Fraction(1, 2)
    assert sum(b[i] * c[i] ** 2 for i in range(s)) == Fraction(1, 3)
    assert sum(b[i] * A[i][j] * c[j] for i in range(s) for j in range(s)) == Fraction(1, 6)
    Ac = [sum(A[i][j] * c[j] for j in range(s)) for i in range(s)]
    assert sum(b[i] * A[i][j] * Ac[j] for i in range(s) for j in range(s)) != Fraction(1, 24)  # order exactly 3
    for i in range(s):
        assert sum(A[i]) == c[i]
    for z in (Fraction(-1, 3), Fraction(2), Fraction(-5, 2)):
        R = ssp_rk3_step([Fraction(1)], lambda u: [z * x for x in u], Fraction(1))[0]
        assert R == 1 + z + z ** 2 / 2 + z ** 3 / 6


@pytest.mark.parametrize("variant", ["js", "z"])
def test_observed_fifth_order_on_smooth_advection(variant):
    errs = []
    for m in (20, 40, 80):
        dx = 1.0 / m
        dt = 0.5 * dx * (dx / 0.1) ** (2.0 / 3.0)  # dt ~ dx^(5/3) so RK3 error is O(dx^5)
        u0 = cell_averages(lambda x: -math.cos(2 * math.pi * x) / (2 * math.pi), m)
        r = weno(u0, lambda u: u, 1.0, dx, dt, 0.5, variant=variant)
        ex = cell_averages(lambda x: -math.cos(2 * math.pi * (x - 0.5)) / (2 * math.pi), m)
        errs.append(max(abs(a - b) for a, b in zip(r.u, ex)))
    assert math.log2(errs[1] / errs[2]) > 4.6
    assert errs[2] < 3e-6


def test_jiang_shu_weights_lose_order_at_critical_points_without_eps():
    def f(x):
        return math.sin(math.pi * x - math.sin(math.pi * x) / math.pi)
    errs = {"js": [], "z": []}
    for m in (160, 320, 640):
        dx = 2.0 / m
        v = [sum(w * f(-1 + (j + 0.5) * dx + 0.5 * dx * s) for s, w in GAUSS5) / 2 for j in range(m)]
        for var in errs:
            e = max(abs(reconstruct([v[(j + k) % m] for k in range(-2, 3)], 1e-40, var) - f(-1 + (j + 1) * dx))
                    for j in range(m))
            errs[var].append(e)
    js, z = errs["js"], errs["z"]
    assert math.log2(js[1] / js[2]) < 4.3  # about 4: the Henrick et al. loss of order
    assert math.log2(z[1] / z[2]) > 4.8


def test_square_wave_is_essentially_non_oscillatory():
    m = 100
    dx = 1.0 / m
    sq = [1.0 if 0.25 <= (j + 0.5) * dx < 0.5 else 0.0 for j in range(m)]
    r = weno(sq, lambda u: u, 1.0, dx, 0.5 * dx, 1.0)
    lin = weno(sq, lambda u: u, 1.0, dx, 0.5 * dx, 1.0, variant="linear")
    assert max(r.u) < 1.001 and min(r.u) > -0.001
    assert total_variation(r.u) < 2.01
    assert max(lin.u) > 1.05 and total_variation(lin.u) > 2.5
    assert abs(sum(r.u) - sum(sq)) < 1e-12  # periodic: conservative
    assert sum(abs(a - b) for a, b in zip(r.u, sq)) * dx < 0.035


def test_burgers_shock_speed_and_conservation():
    m = 100
    dx = 1.0 / m
    xs = [(j + 0.5) * dx for j in range(m)]
    u0 = [1.0 if x < 0.3 else 0.0 for x in xs]
    r = weno(u0, lambda u: 0.5 * u * u, 1.0, dx, 0.4 * dx, 0.4, bc="transmissive")
    # mass changes only by the boundary fluxes f(1) - f(0) = 1/2 over T = 0.4
    assert abs((sum(r.u) - sum(u0)) * dx - 0.2) < 1e-9
    cross = [xs[j] for j in range(m - 1) if r.u[j] >= 0.5 > r.u[j + 1]]
    assert len(cross) == 1 and abs(cross[0] - 0.5) <= dx  # Rankine-Hugoniot speed 1/2
    assert max(r.u) < 1.001 and min(r.u) > -0.001


def test_burgers_rarefaction_against_the_similarity_solution():
    m = 100
    dx = 1.0 / m
    xs = [(j + 0.5) * dx for j in range(m)]
    u0 = [-0.5 if x < 0.5 else 1.0 for x in xs]  # sonic rarefaction
    r = weno(u0, lambda u: 0.5 * u * u, 1.0, dx, 0.4 * dx, 0.2, bc="transmissive")
    ex = [max(-0.5, min(1.0, (x - 0.5) / 0.2)) for x in xs]
    assert sum(abs(a - b) for a, b in zip(r.u, ex)) * dx < 0.01


def test_zero_steps_long_step_and_off_grid_final_step():
    u0 = [0.0, 1.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0]
    r = weno(u0, lambda u: u, 1.0, 0.125, 0.05, 0.0)
    assert r.steps == 0 and r.u == u0 and r.flux_evals == 0
    r = weno(u0, lambda u: u, 1.0, 0.125, 1.0, 0.05)  # dt larger than the interval: one short step
    assert r.steps == 1 and r.t == 0.05
    r = weno(u0, lambda u: u, 1.0, 0.125, 0.04, 0.1)  # 0.04, 0.08, then a step of 0.02
    assert r.steps == 3 and abs(r.t - 0.1) < 1e-15
    assert r.flux_evals == 3 * 3 * (len(u0) + 6)
    assert step_count(Fraction(1), Fraction(1, 3)) == 3 and step_count(0.3, 0.1) == 3


def test_courant_numbers_below_and_above_the_limit():
    m = 40
    dx = 1.0 / m
    u0 = cell_averages(lambda x: -math.cos(2 * math.pi * x) / (2 * math.pi), m)
    ok = weno(u0, lambda u: u, 1.0, dx, 1.0 * dx, 5.0)
    assert max(abs(x) for x in ok.u) <= 1.0
    bad = weno(u0, lambda u: u, 1.0, dx, 2.0 * dx, 5.0)
    assert max(abs(x) for x in bad.u) > 1e6


def test_rhs_of_linear_advection_matches_the_derivative():
    m = 64
    dx = 1.0 / m
    u = cell_averages(lambda x: -math.cos(2 * math.pi * x) / (2 * math.pi), m)
    L = weno_rhs(u, lambda v: v, 1.0, dx)
    ex = cell_averages(lambda x: -math.sin(2 * math.pi * x), m)  # -(u_x) averaged
    assert max(abs(a - b) for a, b in zip(L, ex)) < 1e-4


def test_input_validation():
    with pytest.raises(ValueError):
        weno([1.0], lambda u: u, 1.0, 0.0, 0.1, 1.0)
    with pytest.raises(ValueError):
        weno([], lambda u: u, 1.0, 0.1, 0.1, 1.0)
    with pytest.raises(ValueError):
        weno([1.0], lambda u: u, -1.0, 0.1, 0.1, 1.0)
    with pytest.raises(ValueError):
        step_count(1.0, 0.0)
    with pytest.raises(ValueError):
        step_count(-1.0, 0.1)
    with pytest.raises(ValueError):
        weno([1.0] * 5, lambda u: u, 1.0, 0.1, 0.1, 0.1, bc="reflect")
    with pytest.raises(ValueError):
        nonlinear_weights([0.0, 0.0, 0.0], variant="other")
