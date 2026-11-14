# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-cell-method/. The authors are listed in prov/DX2BFW.jsonl.

import math
import random

from finite_cell_method import (
    FiniteCellBar,
    condition_estimate,
    extension_constant,
    shapes,
    stiffness_parts,
)

A = 0.6
K = math.pi / (2 * A)
EXACT = lambda x: math.sin(K * x)
DEXACT = lambda x: K * math.cos(K * x)
LOAD = lambda x: K * K * math.sin(K * x)


def energy(M, c):
    n = len(c)
    return math.sqrt(max(0.0, sum(c[i] * M[i][j] * c[j] for i in range(n) for j in range(n))))


def test_shape_functions() -> None:
    rng = random.Random(11)
    for p in range(1, 9):
        for _ in range(20):
            xi = rng.uniform(-1, 1)
            val, der = shapes(xi, p)
            assert abs(val[0] + val[1] - 1) < 1e-15
            # the inner modes vanish at both ends
            for e in (-1.0, 1.0):
                v, _ = shapes(e, p)
                assert all(abs(t) < 1e-14 for t in v[2:])
            # derivative check by central differences
            h = 1e-6
            vp, _ = shapes(xi + h, p)
            vm, _ = shapes(xi - h, p)
            assert all(abs((s - t) / (2 * h) - d) < 1e-6 for s, t, d in zip(vp, vm, der))


def test_one_cell_closed_form() -> None:
    """One cell (0, 1), p = 2, a = 1/2, f = 1: u_h(a) - u(a) = alpha (1 - alpha) / (8 (1 + 14 alpha + alpha^2))."""
    for alpha in (0.0, 1e-6, 1e-3, 0.01, 0.1, 0.5, 1.0):
        bar = FiniteCellBar(1.0, 1, 2, 0.5, alpha, lambda x: 1.0)
        bar.solve()
        expect = alpha * (1 - alpha) / (8 * (1 + 14 * alpha + alpha * alpha))
        assert abs(bar.value(0.5) - 0.125 - expect) < 1e-14


def test_exact_in_space_and_linear_in_alpha() -> None:
    """u = a x - x^2 / 2 is in the space restricted to (0, a): alpha = 0 is exact, and the error is O(alpha)."""
    exact = lambda x: A * x - x * x / 2
    dexact = lambda x: A - x
    bar = FiniteCellBar(1.0, 4, 2, A, 0.0, lambda x: 1.0)
    bar.solve()
    assert max(bar.errors(exact, dexact)) < 1e-12
    errs = []
    for alpha in (1e-4, 1e-5, 1e-6):
        bar = FiniteCellBar(1.0, 4, 2, A, alpha, lambda x: 1.0)
        bar.solve()
        errs.append(bar.errors(exact, dexact)[1])
    assert 9 < errs[0] / errs[1] < 11 and 9 < errs[1] / errs[2] < 11


def test_alpha_bounds() -> None:
    """||u_alpha - u_0||_E <= min(alpha C_ext ||u_0||_E, sqrt(alpha)/2 ||u_0||_{E, fictitious})."""
    for p in (2, 4, 6):
        b0 = FiniteCellBar(1.0, 4, p, A, 0.0, LOAD)
        c0 = b0.solve()
        K0, K1 = stiffness_parts(b0)
        cext = extension_constant(b0)
        for alpha in (1e-2, 1e-4, 1e-6, 1e-8):
            c = FiniteCellBar(1.0, 4, p, A, alpha, LOAD).solve()
            e = energy(K0, [s - t for s, t in zip(c, c0)])
            bound = min(alpha * cext * energy(K0, c0), math.sqrt(alpha) / 2 * energy(K1, c0))
            assert e <= bound * (1 + 1e-6) + 1e-12, (p, alpha, e, bound)


def test_p_convergence_against_exact() -> None:
    prev = None
    for p in range(2, 9, 2):
        bar = FiniteCellBar(1.0, 4, p, A, 0.0, LOAD)
        bar.solve()
        _, en = bar.errors(EXACT, DEXACT)
        if prev is not None:
            assert en < prev / 15
        prev = en
    assert prev < 1e-9


def test_error_as_alpha_goes_to_zero() -> None:
    bar = FiniteCellBar(1.0, 4, 4, A, 0.0, LOAD)
    bar.solve()
    base = bar.errors(EXACT, DEXACT)[1]
    errs = []
    for alpha in (1e-2, 1e-4, 1e-6, 1e-8, 1e-10):
        bar = FiniteCellBar(1.0, 4, 4, A, alpha, LOAD)
        bar.solve()
        errs.append(bar.errors(EXACT, DEXACT)[1])
    assert errs[-1] < 1.01 * base + 1e-9
    assert errs[0] > 10 * base


def test_bisection_quadrature_converges() -> None:
    errs = {}
    for depth in (None, 4, 8, 16):
        bar = FiniteCellBar(1.0, 4, 4, A, 1e-8, LOAD, depth=depth)
        bar.solve()
        errs[depth] = bar.errors(EXACT, DEXACT)[0]
    assert errs[8] < errs[4] / 8
    assert abs(errs[16] - errs[None]) < 1e-7


def test_conditioning_and_alpha() -> None:
    k0, _ = FiniteCellBar(1.0, 4, 8, A, 0.0, LOAD).assemble()
    k8, _ = FiniteCellBar(1.0, 4, 8, A, 1e-8, LOAD).assemble()
    c0, c8 = condition_estimate(k0, 80), condition_estimate(k8, 80)
    assert c0 > 1e10 and c8 < c0 / 100
