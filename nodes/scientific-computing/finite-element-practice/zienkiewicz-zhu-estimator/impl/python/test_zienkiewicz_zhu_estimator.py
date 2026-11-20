# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zienkiewicz-zhu-estimator/. The authors are listed in prov/4WBQ50.jsonl.

import math
import random

import zienkiewicz_zhu_estimator as Z

PI = math.pi


def u(x, y):
    return math.sin(PI * x) * math.sin(PI * y)


def grad_u(x, y):
    return (PI * math.cos(PI * x) * math.sin(PI * y), PI * math.sin(PI * x) * math.cos(PI * y))


def f(x, y):
    return 2 * PI * PI * u(x, y)


def zero(x, y):
    return 0.0


def perturbed_grid(m, seed, amount=0.25):
    coords, elements = Z.square_grid(m)
    bnd = Z.boundary_nodes(coords, elements)
    rng = random.Random(seed)
    h = 1.0 / m
    coords = [p if v in bnd else (p[0] + rng.uniform(-amount, amount) * h, p[1] + rng.uniform(-amount, amount) * h)
              for v, p in enumerate(coords)]
    return coords, elements


def test_effectivity_near_one_on_regular_grid():
    for m in (16, 32):
        c, e = Z.square_grid(m)
        U = Z.solve_p1(c, e, f, zero)
        err = Z.energy_error(c, e, U, grad_u)
        _, eta_spr = Z.zz_estimator(c, e, U, "spr")
        _, eta_avg = Z.zz_estimator(c, e, U, "average")
        assert 0.98 < eta_spr / err < 1.02
        assert 0.97 < eta_avg / err < 1.03


def test_error_and_estimator_halve_with_h():
    rows = []
    for m in (8, 16):
        c, e = Z.square_grid(m)
        U = Z.solve_p1(c, e, f, zero)
        rows.append((Z.energy_error(c, e, U, grad_u), Z.zz_estimator(c, e, U)[1]))
    assert 1.9 < rows[0][0] / rows[1][0] < 2.1
    assert 1.9 < rows[0][1] / rows[1][1] < 2.1


def test_effectivity_on_perturbed_grid():
    c, e = perturbed_grid(16, seed=5)
    U = Z.solve_p1(c, e, f, zero)
    err = Z.energy_error(c, e, U, grad_u)
    _, eta = Z.zz_estimator(c, e, U)
    assert 0.9 < eta / err < 1.1


def test_linear_solution_gives_zero_estimate():
    for seed in range(3):
        c, e = perturbed_grid(6, seed=seed, amount=0.3)
        lin = lambda x, y: 1.0 + 2.0 * x - 3.0 * y
        U = Z.solve_p1(c, e, zero, lin)
        assert max(abs(U[v] - lin(*c[v])) for v in range(len(c))) < 1e-9
        for rec in ("spr", "average"):
            eta, total = Z.zz_estimator(c, e, U, rec)
            assert total < 1e-8
            assert len(eta) == len(e)


def test_least_squares_fit_reproduces_linear_data():
    rng = random.Random(11)
    for _ in range(50):
        pts = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(rng.randint(3, 8))]
        a, b, cc = rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-2, 2)
        fit = Z._fit_linear(pts, [a + b * x + cc * y for x, y in pts])
        assert fit is not None
        assert max(abs(p - q) for p, q in zip(fit, (a, b, cc))) < 1e-9
    assert Z._fit_linear([(0, 0), (1, 1), (2, 2)], [1.0, 2.0, 3.0]) is None  # collinear points


def test_indicator_is_exact_integral():
    # one triangle with prescribed nodal gradients G and a P1 function U
    coords = [(0.0, 0.0), (2.0, 0.0), (0.0, 1.0)]
    elements = [[0, 1, 2]]
    U = [0.0, 2.0, 0.0]  # u_h = x, gradient (1, 0)
    G = [(1.0, 0.0), (3.0, 0.0), (1.0, 0.0)]  # G - grad u_h = (x, 0)
    gx, gy = Z.element_gradients(coords, elements, U)[0]
    assert abs(gx - 1.0) < 1e-14 and abs(gy) < 1e-14
    # integral of x^2 over the triangle with legs 2 and 1 is 2/3
    original = Z.recover_spr
    try:
        Z.recover_spr = lambda c, e, v: G
        eta, total = Z.zz_estimator(coords, elements, U)
    finally:
        Z.recover_spr = original
    assert abs(eta[0] ** 2 - 2.0 / 3.0) < 1e-13
