# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomize-then-optimize/. The authors are listed in prov/27EKVH.jsonl.

import math
import random

from imgla import eye, matmul, matvec, solve, transpose
from randomize_then_optimize import (
    det,
    gauss_newton_map,
    linear_problem,
    log_weight,
    rto_mh,
    solve_projected,
    thin_qr_q,
)


def cubic_problem(c=1.0, sigma=0.5, y=1.5):
    """G(x) = x + c x^3, noise N(0, sigma^2), prior N(0, 1)."""

    def f(x):
        return [(x[0] + c * x[0] ** 3) / sigma, x[0]]

    def jac(x):
        return [[(1.0 + 3.0 * c * x[0] ** 2) / sigma], [1.0]]

    return f, jac, [y / sigma, 0.0]


def quadrature_moments(c=1.0, sigma=0.5, y=1.5):
    xs = [-4.0 + 8.0 * i / 40000 for i in range(40001)]
    p = [math.exp(-((y - x - c * x ** 3) ** 2) / (2.0 * sigma * sigma) - 0.5 * x * x) for x in xs]
    z = sum(p)
    m = sum(x * w for x, w in zip(xs, p)) / z
    v = sum((x - m) ** 2 * w for x, w in zip(xs, p)) / z
    return m, v


def moments(chain):
    k = len(chain)
    n = len(chain[0])
    m = [sum(c[i] for c in chain) / k for i in range(n)]
    cov = [[sum((c[i] - m[i]) * (c[j] - m[j]) for c in chain) / (k - 1) for j in range(n)] for i in range(n)]
    return m, cov


def test_determinant_and_orthonormal_basis():
    assert abs(det([[2.0, 1.0], [1.0, 3.0]]) - 5.0) < 1e-12
    assert abs(det([[0.0, 1.0], [1.0, 0.0]]) + 1.0) < 1e-12
    assert det([[1.0, 2.0], [2.0, 4.0]]) == 0.0
    j = [[1.0, 2.0], [0.5, -1.0], [3.0, 0.0], [0.0, 1.0]]
    q = thin_qr_q(j)
    qtq = matmul(transpose(q), q)
    for i in range(2):
        for k in range(2):
            assert abs(qtq[i][k] - (1.0 if i == k else 0.0)) < 1e-12
    # Every column of J is reproduced by its projection Q Q^T J.
    for col in transpose(j):
        proj = matvec(q, matvec(transpose(q), col))
        assert max(abs(a - b) for a, b in zip(proj, col)) < 1e-12
    try:
        thin_qr_q([[1.0, 2.0], [2.0, 4.0]])
    except ValueError:
        pass
    else:
        raise AssertionError("rank-deficient Jacobian was accepted")


def test_map_point_is_the_tikhonov_solution_for_a_linear_problem():
    a = [[1.0, 0.5], [0.2, 1.0], [0.3, 0.3]]
    y = [1.0, 0.5, 0.2]
    f, jac, ybar = linear_problem(a, y, 0.3, 1.0)
    xbar = gauss_newton_map(f, jac, ybar, [0.0, 0.0])
    # (A^T A + (sigma / prior_sd)^2 I) x = A^T y
    ata = matmul(transpose(a), a)
    lhs = [[ata[i][k] + (0.09 if i == k else 0.0) for k in range(2)] for i in range(2)]
    x = solve(lhs, matvec(transpose(a), y))
    assert max(abs(p - q) for p, q in zip(xbar, x)) < 1e-10


def test_linear_problem_has_constant_weight_and_accepts_everything():
    f, jac, ybar = linear_problem([[0.1]], [0.12], 0.05, 1.0)
    q = thin_qr_q(jac(None))
    w0 = log_weight(f, jac, q, ybar, [0.0])
    for x in (-3.0, 0.5, 0.96, 4.0):
        assert abs(log_weight(f, jac, q, ybar, [x]) - w0) < 1e-9
    chain, acc, xbar = rto_mh(f, jac, ybar, [0.0], 4000, random.Random(1))
    assert abs(xbar[0] - 0.96) < 1e-10
    assert acc > 0.999
    m, cov = moments(chain)
    assert abs(m[0] - 0.96) < 0.03
    assert abs(cov[0][0] - 0.2) < 0.02


def test_linear_two_dimensional_posterior_moments():
    a = [[1.0, 0.5], [0.2, 1.0], [0.3, 0.3]]
    y = [1.0, 0.5, 0.2]
    f, jac, ybar = linear_problem(a, y, 0.3, 1.0)
    h = jac(None)
    c_post = solve(matmul(transpose(h), h), eye(2))
    m_post = matvec(c_post, matvec(transpose(h), ybar))
    chain, _, _ = rto_mh(f, jac, ybar, [0.0, 0.0], 3000, random.Random(4))
    m, cov = moments(chain)
    for i in range(2):
        assert abs(m[i] - m_post[i]) < 0.03
        for k in range(2):
            assert abs(cov[i][k] - c_post[i][k]) < 0.02


def test_proposals_solve_the_projected_equation():
    f, jac, ybar = cubic_problem()
    xbar = gauss_newton_map(f, jac, ybar, [0.0])
    q = thin_qr_q(jac(xbar))
    qt = transpose(q)
    rng = random.Random(9)
    for _ in range(20):
        eps = [rng.gauss(0.0, 1.0) for _ in ybar]
        target = matvec(qt, [p + e for p, e in zip(ybar, eps)])
        x = solve_projected(f, jac, q, target, xbar)
        assert x is not None
        res = [p - t for p, t in zip(matvec(qt, f(x)), target)]
        assert max(abs(r) for r in res) < 1e-9


def test_nonlinear_posterior_matches_quadrature_and_correction_matters():
    f, jac, ybar = cubic_problem()
    m_true, v_true = quadrature_moments()
    chain, acc, xbar = rto_mh(f, jac, ybar, [0.0], 5000, random.Random(3))
    m, cov = moments(chain)
    assert 0.6 < acc < 0.99
    assert abs(m[0] - m_true) < 0.02
    assert abs(cov[0][0] - v_true) < 0.008
    # Without the Metropolis-Hastings step the proposals are biased.
    q = thin_qr_q(jac(xbar))
    qt = transpose(q)
    rng = random.Random(3)
    raw = []
    for _ in range(3000):
        eps = [rng.gauss(0.0, 1.0) for _ in ybar]
        raw.append(solve_projected(f, jac, q, matvec(qt, [p + e for p, e in zip(ybar, eps)]), xbar)[0])
    assert sum(raw) / len(raw) - m_true > 0.03
