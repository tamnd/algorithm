# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybridizable-discontinuous-galerkin/. The authors are listed in prov/EC181T.jsonl.

import math
import random
from fractions import Fraction as F

import scimat
from hybridizable_discontinuous_galerkin import hdg, residual, trace_matrix

# 5-point Gauss-Legendre rule on [-1, 1], independent of the code under test
GX = [-0.9061798459386640, -0.5384693101056831, 0.0, 0.5384693101056831, 0.9061798459386640]
GW = [0.2369268850561891, 0.4786286704993665, 0.5688888888888889, 0.4786286704993665, 0.2369268850561891]


def errors(cells, m, u, q):
    h = 1.0 / m
    eu = eq = 0.0
    for j, (qc, uc) in enumerate(cells):
        for xg, wg in zip(GX, GW):
            xi = (xg + 1) / 2
            x = j * h + xi * h
            uv = sum(float(c) * xi ** r for r, c in enumerate(uc))
            qv = sum(float(c) * xi ** r for r, c in enumerate(qc))
            eu += wg * h / 2 * (uv - u(x)) ** 2
            eq += wg * h / 2 * (qv - q(x)) ** 2
    return math.sqrt(eu), math.sqrt(eq)


def local_coefficients(p, x0, h, size):
    """Coefficients of p(x0 + xi h) in powers of xi, padded to size, for p in powers of x."""
    out = [F(0)] * size
    for n, pn in enumerate(p):
        for r in range(n + 1):
            out[r] += pn * math.comb(n, r) * x0 ** (n - r) * h ** r
    return out


def test_page_example_two_cells() -> None:
    uhat, cells = hdg(lambda x: F(2), 2, 1, F(1))
    assert uhat == [0, F(1, 4), 0]
    assert cells[0] == ([F(-25, 26), F(12, 13)], [F(1, 26), F(1, 4)])
    assert cells[1] == ([F(1, 26), F(12, 13)], [F(15, 52), F(-1, 4)])
    # the same data with k = 0 gives a trace that is not exact
    uhat, cells = hdg(lambda x: F(2), 2, 0, F(1))
    assert uhat == [0, F(1, 5), 0]
    assert cells == [([F(-2, 5)], [F(3, 5)]), ([F(2, 5)], [F(3, 5)])]


def test_trace_system_is_the_p1_stiffness_matrix() -> None:
    for m in (2, 4, 5):
        want = [[0] * (m - 1) for _ in range(m - 1)]
        for i in range(m - 1):
            want[i][i] = 2 * m
            if i > 0:
                want[i][i - 1] = -m
            if i < m - 2:
                want[i][i + 1] = -m
        for k in (1, 2, 3):
            for tau in (F(1, 3), F(1), F(7)):
                assert trace_matrix(m, k, tau) == want
    # for k = 0 the matrix depends on tau and is not the P1 matrix
    assert trace_matrix(4, 0, F(1))[0][:2] == [9, F(-9, 2)]
    assert trace_matrix(4, 0, F(1)) != trace_matrix(4, 0, F(2))


def test_trace_matrix_is_symmetric_positive_definite() -> None:
    for m in (2, 3, 6):
        for k in (0, 1, 2, 3):
            for tau in (F(1, 10), F(1), F(10)):
                S = trace_matrix(m, k, tau)
                n = len(S)
                assert all(S[i][j] == S[j][i] for i in range(n) for j in range(n))
                scimat.cholesky(S)  # raises if not positive definite


def test_traces_exact_at_nodes_for_k_at_least_one() -> None:
    # u = x^4 - x is not in P_1, but the traces are exact
    uhat, _ = hdg(lambda x: -12 * x * x, 4, 1, F(1))
    assert uhat == [F(e, 4) ** 4 - F(e, 4) for e in range(5)]
    # u = x^5 with k = 2 and tau = 3, nonzero boundary value at x = 1
    uhat, _ = hdg(lambda x: -20 * x ** 3, 3, 2, F(3), F(0), F(1))
    assert uhat == [F(e, 3) ** 5 for e in range(4)]


def test_traces_not_exact_for_k_zero() -> None:
    uhat, _ = hdg(lambda x: -12 * x * x, 4, 0, F(2))
    exact = [F(e, 4) ** 4 - F(e, 4) for e in range(5)]
    assert uhat[0] == exact[0] and uhat[4] == exact[4]
    assert all(uhat[e] != exact[e] for e in range(1, 4))


def test_global_rows_vanish_at_the_computed_traces() -> None:
    f = lambda x: F(1) + x - 3 * x * x
    for m, k, tau in ((3, 1, F(1)), (4, 2, F(1, 2)), (5, 3, F(4))):
        uhat, _ = hdg(f, m, k, tau)
        res = residual(f, m, k, tau, uhat)
        assert all(r == 0 for r in res[1:m])


def test_random_polynomials_against_closed_form() -> None:
    # oracle: the exact pair u = p, q = -p' for a random polynomial p of degree <= k
    rng = random.Random(13)
    for _ in range(500):
        k = rng.randint(1, 3)
        m = rng.randint(2, 4)
        p = [rng.randint(-5, 5) for _ in range(k + 1)]
        f2 = [-(n + 2) * (n + 1) * p[n + 2] for n in range(k - 1)]
        dp = [-(n + 1) * p[n + 1] for n in range(k)]

        def f(x, f2=f2):
            return sum(cn * x ** n for n, cn in enumerate(f2))

        def u(x, p=p):
            return sum(cn * x ** n for n, cn in enumerate(p))

        tau = rng.uniform(0.1, 10.0)
        uhat, cells = hdg(f, m, k, tau, u(0.0), u(1.0))
        h = F(1, m)
        for e in range(m + 1):
            assert abs(uhat[e] - u(e / m)) < 1e-9
        for j in range(m):
            wu = local_coefficients([F(v) for v in p], j * h, h, k + 1)
            wq = local_coefficients([F(v) for v in dp], j * h, h, k + 1)
            assert all(abs(float(a) - float(b)) < 1e-8 for a, b in zip(cells[j][1], wu))
            assert all(abs(float(a) - float(b)) < 1e-8 for a, b in zip(cells[j][0], wq))


def test_convergence_rates_of_u_and_q() -> None:
    u = lambda x: math.sin(math.pi * x)
    q = lambda x: -math.pi * math.cos(math.pi * x)
    f = lambda x: math.pi ** 2 * math.sin(math.pi * x)
    for k in (1, 2, 3):
        e = [errors(hdg(f, m, k, 1.0)[1], m, u, q) for m in (8, 16)]
        assert abs(math.log2(e[0][0] / e[1][0]) - (k + 1)) < 0.15
        assert abs(math.log2(e[0][1] / e[1][1]) - (k + 1)) < 0.15
    # k = 0: first order only
    e = [errors(hdg(f, m, 0, 1.0)[1], m, u, q) for m in (16, 32)]
    assert abs(math.log2(e[0][0] / e[1][0]) - 1) < 0.2
