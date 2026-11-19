# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vorticity-streamfunction-formulation/. The authors are listed in prov/8HPSC5.jsonl.

import random
from fractions import Fraction

import pytest

from vorticity_streamfunction_formulation import cavity, centerline_u, poisson_residual, thom, velocity

GHIA_U_HALF = -0.20581   # Ghia, Ghia and Shin 1982, Table I, Re = 100, u at (0.5, 0.5)
GHIA_PSI_MIN = -0.103423  # the same paper, Re = 100, primary vortex


def test_thom_is_exact_for_a_quadratic_streamfunction():
    # psi = a y^2 at the bottom (wall at rest) and psi = U (y - 1) + a (y - 1)^2 at the lid:
    # both have w = -psi_yy = -2a on the wall, and Thom's formula gives it exactly.
    n, a, U = 4, Fraction(3, 7), Fraction(5, 2)
    h = Fraction(1, n)
    psi = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n):
        psi[i][1] = a * h * h
        psi[i][n - 1] = U * (-h) + a * h * h
    w = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
    thom(psi, w, h, U)
    for i in range(1, n):
        assert w[i][0] == -2 * a
        assert w[i][n] == -2 * a


def test_velocity_from_streamfunction_is_exactly_divergence_free():
    rng = random.Random(5)
    n = 8
    h = Fraction(1, n)
    psi = [[Fraction(rng.randint(-9, 9)) for _ in range(n + 1)] for _ in range(n + 1)]
    u, v = velocity(psi, h)
    for i in range(2, n - 1):
        for j in range(2, n - 1):
            assert (u[i + 1][j] - u[i - 1][j]) / (2 * h) + (v[i][j + 1] - v[i][j - 1]) / (2 * h) == 0


def test_cavity_re100_on_16_cells_is_near_ghia():
    psi, w, steps = cavity(16, 100.0, 0.02, tol=1e-5)
    h = 1 / 16
    assert poisson_residual(psi, w, h) < 1e-5
    col = centerline_u(psi, h)
    pmin = min(min(r) for r in psi)
    assert abs(col[8] - (-0.17576)) < 1e-4 and abs(pmin - (-0.090978)) < 1e-5  # measured
    assert abs(col[8] - GHIA_U_HALF) < 0.035 and abs(pmin - GHIA_PSI_MIN) < 0.013
    # The steady state does not depend on the number of SOR sweeps per step.
    psi4, _, steps4 = cavity(16, 100.0, 0.02, tol=1e-5, sweeps=4)
    assert max(abs(psi4[i][j] - psi[i][j]) for i in range(17) for j in range(17)) < 1e-5


def test_explicit_step_above_the_limit_blows_up():
    with pytest.raises(OverflowError):
        cavity(16, 100.0, 0.1, maxsteps=2000)
