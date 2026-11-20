# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/element-free-galerkin-method/. The authors are listed in prov/MYQ8NE.jsonl.

import math
import random

import scimat
from element_free_galerkin_method import (
    EFG1D,
    cubic_spline_weight,
    errors,
    gauss_legendre,
    mls_shape,
    nodal_quadrature,
)

NODES = [i / 10 for i in range(11)]


def u_sin(x):
    return math.sin(math.pi * x)


def du_sin(x):
    return math.pi * math.cos(math.pi * x)


def f_sin(x):
    return math.pi ** 2 * math.sin(math.pi * x)


def test_gauss_legendre_is_exact_for_degree_2n_minus_1():
    for n in (2, 3, 5, 8):
        pts, wts = gauss_legendre(n)
        for k in range(2 * n):
            exact = 0.0 if k % 2 else 2 / (k + 1)
            assert abs(sum(w * x ** k for x, w in zip(pts, wts)) - exact) < 1e-13


def test_cubic_spline_weight_is_c2_with_compact_support():
    h = 1e-6
    for r in (0.5, 1.0):
        wl, dl = cubic_spline_weight(r - h)
        wr, dr = cubic_spline_weight(r + h)
        assert abs(wl - wr) < 1e-5 and abs(dl - dr) < 1e-5
    assert cubic_spline_weight(1.0) == (0.0, 0.0)
    assert abs(cubic_spline_weight(0.0)[0] - 2 / 3) < 1e-15


def test_mls_reproduces_linear_and_quadratic_fields():
    rng = random.Random(4)
    nodes = sorted([0.0, 1.0] + [rng.random() for _ in range(15)])
    for degree in (1, 2):
        for _ in range(30):
            x = rng.random()
            idx, phi, dphi = mls_shape(x, nodes, [0.3] * len(nodes), degree)
            for k in range(degree + 1):
                assert abs(sum(p * nodes[i] ** k for p, i in zip(phi, idx)) - x ** k) < 1e-11
                d_exact = k * x ** (k - 1) if k else 0.0
                assert abs(sum(p * nodes[i] ** k for p, i in zip(dphi, idx)) - d_exact) < 1e-9


def test_derivatives_match_finite_differences():
    radii = [0.25] * len(NODES)
    h = 1e-6
    for x in (0.137, 0.5, 0.71):
        idx, _, dphi = mls_shape(x, NODES, radii)
        ip, pp, _ = mls_shape(x + h, NODES, radii)
        im, pm, _ = mls_shape(x - h, NODES, radii)
        assert idx == ip == im
        for k in range(len(idx)):
            assert abs((pp[k] - pm[k]) / (2 * h) - dphi[k]) < 1e-6


def test_no_kronecker_delta_property():
    # at the node 0.5 the five supports overlap; with a symmetric neighbourhood phi_I = w_I / sum w
    idx, phi, _ = mls_shape(0.5, NODES, [0.25] * len(NODES))
    assert idx == [3, 4, 5, 6, 7]
    expected = [2 / 235, 53 / 235, 25 / 47, 53 / 235, 2 / 235]
    assert all(abs(p - e) < 1e-14 for p, e in zip(phi, expected))


def test_patch_test_depends_on_the_quadrature():
    exact = [(1 + 2 * x, 2.0) for x in [0.05 * k for k in range(21)]]

    def worst(model):
        return max(abs(model.value(0.05 * k)[0] - exact[k][0]) for k in range(21))

    # cells of width h/4 align with the breakpoints of the weights: passes to rounding
    fine = EFG1D(NODES, 0.25, lambda x: 0.0, 1.0, 3.0, ncells=40, order=8)
    assert worst(fine) < 1e-13
    # one cell per node interval with 3 Gauss points: an error from the quadrature only
    coarse = EFG1D(NODES, 0.25, lambda x: 0.0, 1.0, 3.0, ncells=10, order=3)
    assert 1e-6 < worst(coarse) < 1e-3
    # nodal integration fails clearly
    nodal = EFG1D(NODES, 0.25, lambda x: 0.0, 1.0, 3.0, quadrature=nodal_quadrature(NODES))
    assert worst(nodal) > 1e-3


def test_boundary_conditions_hold_through_the_multipliers():
    model = EFG1D(NODES, 0.25, f_sin, 0.5, -1.0, ncells=40, order=5)
    assert abs(model.value(0.0)[0] - 0.5) < 1e-12
    assert abs(model.value(1.0)[0] + 1.0) < 1e-12
    # the coefficients are not the nodal values
    assert abs(model.coef[0] - 0.5) > 1e-4


def test_convergence_rates_linear_basis():
    errs = []
    for n in (11, 21, 41, 81):
        h = 1 / (n - 1)
        nodes = [i * h for i in range(n)]
        model = EFG1D(nodes, 2.5 * h, f_sin, 0.0, 0.0, ncells=4 * (n - 1), order=5)
        errs.append(errors(model, u_sin, du_sin, 0.0, 1.0))
    r0 = scimat.observed_order([e[0] for e in errs])
    r1 = scimat.observed_order([e[1] for e in errs])
    assert r0[-1] > 1.9 and abs(r1[-1] - 1) < 0.15


def test_convergence_rates_quadratic_basis():
    errs = []
    for n in (11, 21, 41):
        h = 1 / (n - 1)
        nodes = [i * h for i in range(n)]
        model = EFG1D(nodes, 3.5 * h, f_sin, 0.0, 0.0, ncells=4 * (n - 1), order=5, degree=2)
        errs.append(errors(model, u_sin, du_sin, 0.0, 1.0))
    r0 = scimat.observed_order([e[0] for e in errs])
    r1 = scimat.observed_order([e[1] for e in errs])
    assert r0[-1] > 2.6 and r1[-1] > 1.7


def test_irregular_nodes():
    rng = random.Random(7)
    n = 21
    h = 1 / (n - 1)
    nodes = [0.0] + [i * h + rng.uniform(-0.3, 0.3) * h for i in range(1, n - 1)] + [1.0]
    model = EFG1D(nodes, 3.0 * h, f_sin, 0.0, 0.0, ncells=80, order=6)
    e0, e1 = errors(model, u_sin, du_sin, 0.0, 1.0)
    assert e0 < 1e-3 and e1 < 2e-2
