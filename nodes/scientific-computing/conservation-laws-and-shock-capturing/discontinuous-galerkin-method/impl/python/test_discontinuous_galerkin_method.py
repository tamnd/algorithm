# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discontinuous-galerkin-method/. The authors are listed in prov/TAT3SX.jsonl.

import math
import random

import pytest

from discontinuous_galerkin_method import (
    dg_operator, dg_solve, energy, gauss_legendre, godunov_flux_burgers, l2_error,
    legendre, legendre_deriv, project, total_mass, upwind_flux,
)

A = 1.0
f_lin = lambda u: A * u
u0 = lambda x: math.sin(2 * math.pi * x)


def run_advection(M, k, T=0.5, cfl=None):
    dx = 1.0 / M
    cfl = cfl or 0.9 / (2 * k + 1)
    U = project(u0, M, k, 0.0, 1.0)
    U = dg_solve(U, dx, cfl * dx / A, T, f_lin, upwind_flux(A))
    return l2_error(U, lambda x: u0(x - A * T), 0.0, 1.0)


def test_gauss_legendre_exact_for_degree_2q_minus_1():
    for q in range(1, 6):
        xs, ws = gauss_legendre(q)
        for p in range(2 * q):
            exact = 2 / (p + 1) if p % 2 == 0 else 0.0
            assert abs(sum(w * x ** p for x, w in zip(xs, ws)) - exact) < 1e-13


def test_legendre_derivative_matches_finite_difference():
    for l in range(6):
        for x in (-0.7, -0.1, 0.3, 0.9):
            h = 1e-6
            fd = (legendre(l, x + h) - legendre(l, x - h)) / (2 * h)
            assert abs(legendre_deriv(l, x) - fd) < 1e-7


def test_degree_zero_is_the_upwind_scheme():
    rng = random.Random(1)
    M, dx = 12, 1.0 / 12
    U = [[rng.uniform(-1, 1)] for _ in range(M)]
    R = dg_operator(U, dx, f_lin, upwind_flux(A))
    for j in range(M):
        assert abs(R[j][0] - (-(A / dx) * (U[j][0] - U[j - 1][0]))) < 1e-12


def test_exact_operator_on_a_quadratic_with_no_jumps():
    # u = x^2 on [0, 1] is not periodic, so test one inner cell of a long grid by hand:
    # with continuous data and the upwind flux, the DG operator returns the L2 projection of -u_x.
    M, k, dx = 8, 2, 0.125
    U = project(lambda x: x * x, M, k, 0.0, 1.0)
    R = dg_operator(U, dx, f_lin, upwind_flux(A))
    for j in range(1, M):
        xc = (j + 0.5) * dx
        assert abs(R[j][0] - (-2 * xc)) < 1e-12        # mean of -2x
        assert abs(R[j][1] - (-dx)) < 1e-12            # -2x = -2 xc - dx xi
        assert abs(R[j][2]) < 1e-12


@pytest.mark.parametrize("k,p_min", [(0, 0.85), (1, 1.85), (2, 2.85)])
def test_order_k_plus_one_on_smooth_advection(k, p_min):
    errs = [run_advection(M, k) for M in (8, 16, 32, 64)]
    rates = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
    assert rates[-1] > p_min, rates


def test_mass_is_conserved_for_burgers():
    rng = random.Random(7)
    M, k = 20, 2
    U = [[rng.uniform(-1, 1) for _ in range(k + 1)] for _ in range(M)]
    dx = 1.0 / M
    m0 = total_mass(U, dx)
    V = dg_solve(U, dx, 0.02 * dx, 0.01, lambda u: u * u / 2, godunov_flux_burgers)
    assert abs(total_mass(V, dx) - m0) < 1e-13


def test_semi_discrete_energy_identity_for_upwind_flux():
    rng = random.Random(3)
    M, k = 10, 3
    dx = 1.0 / M
    U = [[rng.uniform(-1, 1) for _ in range(k + 1)] for _ in range(M)]
    R = dg_operator(U, dx, f_lin, upwind_flux(A))
    rate = sum(dx / (2 * l + 1) * U[j][l] * R[j][l] for j in range(M) for l in range(k + 1))
    jumps = sum((sum(U[j]) - sum(c if l % 2 == 0 else -c for l, c in enumerate(U[(j + 1) % M]))) ** 2
                for j in range(M))
    assert abs(rate - (-(A / 2) * jumps)) < 1e-11


def test_energy_does_not_grow_under_a_small_step():
    rng = random.Random(5)
    M, k = 16, 2
    dx = 1.0 / M
    U = [[rng.uniform(-1, 1) for _ in range(k + 1)] for _ in range(M)]
    e0 = energy(U, dx)
    V = dg_solve(U, dx, 0.1 * dx, 0.2, f_lin, upwind_flux(A))
    assert energy(V, dx) <= e0 + 1e-14


def test_rejects_bad_steps():
    with pytest.raises(ValueError):
        dg_solve([[0.0]], 0.0, 0.1, 1.0, f_lin, upwind_flux(A))
