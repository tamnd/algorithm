# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johansen-test/. The authors are listed in prov/AA2XYN.jsonl.

import math
import random
from fractions import Fraction

import pytest

from johansen_test import cholesky, critical_value, jacobi_eigen, johansen, simulate_trace

Y1 = [1, 3, 2, 4, 3, 5, 4]
Y2 = [0, 2, 3, 3, 5, 4, 6]


def walk(rng, n, drift=0.0):
    s, out = 0.0, []
    for _ in range(n):
        s += drift + rng.gauss(0.0, 1.0)
        out.append(s)
    return out


def matmul(a, b):
    return [[sum(a[i][m] * b[m][j] for m in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def inv2(m):
    d = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    return [[m[1][1] / d, -m[0][1] / d], [-m[1][0] / d, m[0][0] / d]]


def test_worked_example_exact() -> None:
    # K = 2, no lags, no deterministic terms, n = 7 (T = 6). T times the moment
    # matrices are integers, and the eigenvalues are the roots of
    # z^2 - (128672/110751) z + 19600/110751.
    r = johansen([Y1, Y2], "none", 0)
    r0 = [[Fraction(s[t] - s[t - 1]) for t in range(1, 7)] for s in (Y1, Y2)]
    r1 = [[Fraction(s[t - 1]) for t in range(1, 7)] for s in (Y1, Y2)]
    mom = lambda a, b: [[sum(x * y for x, y in zip(ai, bj)) for bj in b] for ai in a]
    s00, s01, s11 = mom(r0, r0), mom(r0, r1), mom(r1, r1)
    assert s00 == [[15, -3], [-3, 14]] and s01 == [[0, 7], [20, 11]] and s11 == [[64, 59], [59, 63]]
    for got, want in ((r["s00"], s00), (r["s01"], s01), (r["s11"], s11)):
        assert all(abs(got[i][j] - float(want[i][j]) / 6) < 1e-12 for i in range(2) for j in range(2))
    a = matmul(inv2(s11), matmul(transpose(s01), matmul(inv2(s00), s01)))
    tr, det = a[0][0] + a[1][1], a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert tr == Fraction(128672, 110751) and det == Fraction(19600, 110751)
    lam = r["eigenvalues"]
    assert abs(lam[0] + lam[1] - float(tr)) < 1e-12 and abs(lam[0] * lam[1] - float(det)) < 1e-12
    assert abs(lam[0] - 0.981505077) < 1e-9 and abs(lam[1] - 0.180308361) < 1e-9
    assert abs(r["trace"][0] - 25.1345164) < 1e-6 and abs(r["trace"][1] - 1.1929624) < 1e-6
    assert abs(r["max_eig"][0] - 23.9415540) < 1e-6
    assert r["rank"] == 1 and r["nobs"] == 6


def test_one_series_is_the_dickey_fuller_t_ratio() -> None:
    # K = 1, no lags, no constant: lambda = t^2 / (t^2 + T - 1), where t is the
    # Dickey-Fuller t ratio of dy_t = rho y_(t-1) + e_t. Exact in rationals.
    rng = random.Random(8)
    y = [0]
    for _ in range(29):
        y.append(y[-1] + rng.randint(-3, 3))
    big_t = 29
    num = sum(Fraction(y[t - 1]) * (y[t] - y[t - 1]) for t in range(1, 30))
    syy = sum(Fraction(y[t - 1]) ** 2 for t in range(1, 30))
    sdd = sum(Fraction(y[t] - y[t - 1]) ** 2 for t in range(1, 30))
    lam = num * num / (syy * sdd)
    rss = sdd - num * num / syy
    t2 = (num / syy) ** 2 * syy / (rss / (big_t - 1))
    assert lam == t2 / (t2 + big_t - 1)
    r = johansen([y], "none", 0)
    assert abs(r["eigenvalues"][0] - float(lam)) < 1e-12
    assert abs(r["trace"][0] + big_t * math.log(1 - float(lam))) < 1e-9


@pytest.mark.parametrize("lags,case", [(0, "none"), (1, "none"), (2, "c")])
def test_generalized_eigen_equation_and_normalization(lags, case) -> None:
    # S_10 S_00^(-1) S_01 beta_j = lambda_j S_11 beta_j and beta^T S_11 beta = I.
    rng = random.Random(lags + 10)
    data = [walk(rng, 60) for _ in range(3)]
    r = johansen(data, case, lags)
    s00, s01, s11 = r["s00"], r["s01"], r["s11"]
    k = 3
    s10 = transpose(s01)
    low = cholesky(s00)
    # s00^(-1) by solving with the Cholesky factor, column by column
    inv = [[0.0] * k for _ in range(k)]
    for c in range(k):
        z = [0.0] * k
        for i in range(k):
            z[i] = ((1.0 if i == c else 0.0) - sum(low[i][m] * z[m] for m in range(i))) / low[i][i]
        x = [0.0] * k
        for i in range(k - 1, -1, -1):
            x[i] = (z[i] - sum(low[m][i] * x[m] for m in range(i + 1, k))) / low[i][i]
        for i in range(k):
            inv[i][c] = x[i]
    m = matmul(s10, matmul(inv, s01))
    beta = r["beta"]
    btsb = matmul(transpose(beta), matmul(s11, beta))
    assert all(abs(btsb[i][j] - (1.0 if i == j else 0.0)) < 1e-9 for i in range(k) for j in range(k))
    for j in range(k):
        b = [beta[i][j] for i in range(k)]
        lhs = [sum(m[i][a] * b[a] for a in range(k)) for i in range(k)]
        rhs = [r["eigenvalues"][j] * sum(s11[i][a] * b[a] for a in range(k)) for i in range(k)]
        assert all(abs(p - q) < 1e-9 for p, q in zip(lhs, rhs))
    assert all(0.0 <= v < 1.0 for v in r["eigenvalues"])
    assert all(a >= b for a, b in zip(r["eigenvalues"], r["eigenvalues"][1:]))


def test_invariance_to_linear_maps() -> None:
    # Y -> A Y (A invertible) leaves the eigenvalues unchanged; with case "c" so does Y -> A Y + c.
    rng = random.Random(21)
    data = [walk(rng, 80) for _ in range(2)]
    a = [[2.0, -1.0], [0.5, 3.0]]
    mapped = [[a[i][0] * data[0][t] + a[i][1] * data[1][t] for t in range(80)] for i in range(2)]
    shifted = [[v + 7.0 * (i + 1) for v in mapped[i]] for i in range(2)]
    for lags in (0, 2):
        base = johansen(data, "none", lags)["eigenvalues"]
        assert all(abs(p - q) < 1e-9 for p, q in zip(base, johansen(mapped, "none", lags)["eigenvalues"]))
        base_c = johansen(data, "c", lags)["eigenvalues"]
        assert all(abs(p - q) < 1e-9 for p, q in zip(base_c, johansen(shifted, "c", lags)["eigenvalues"]))


def test_jacobi_against_known_spectrum() -> None:
    # A = Q diag(3, 1, -2) Q^T with a known orthogonal Q (a Householder reflector).
    v = [1.0, 2.0, 2.0]
    q = [[(1.0 if i == j else 0.0) - 2 * v[i] * v[j] / 9.0 for j in range(3)] for i in range(3)]
    d = [3.0, 1.0, -2.0]
    a = [[sum(q[i][m] * d[m] * q[j][m] for m in range(3)) for j in range(3)] for i in range(3)]
    vals, vecs = jacobi_eigen(a)
    assert all(abs(p - w) < 1e-12 for p, w in zip(vals, d))
    for j in range(3):
        col = [vecs[i][j] for i in range(3)]
        av = [sum(a[i][m] * col[m] for m in range(3)) for i in range(3)]
        assert all(abs(av[i] - vals[j] * col[i]) < 1e-12 for i in range(3))


def test_size_of_trace_test() -> None:
    # Two independent walks, n = 200, 600 samples: the rejection rate of r = 0 at
    # the 95% MHM point 12.3212 is within 4 binomial SE (0.036) of 0.05.
    reps = 600
    sims = simulate_trace(200, 2, "none", reps, random.Random(11))
    rate = sum(1 for s in sims if s > critical_value("trace", "none", 2)) / reps
    assert abs(rate - 0.05) < 4 * math.sqrt(0.05 * 0.95 / reps)


def test_finds_one_relation() -> None:
    # y = x1 - x2 + u with u an AR(1), so beta is proportional to (1, -1, 1).
    rng = random.Random(2026)
    x1, x2 = walk(rng, 200), walk(rng, 200)
    u, a = [], 0.0
    for _ in range(200):
        a = 0.5 * a + rng.gauss(0.0, 1.0)
        u.append(a)
    y = [p - q + e for p, q, e in zip(x1, x2, u)]
    r = johansen([y, x1, x2], "none", 0)
    assert r["rank"] == 1
    b = [r["beta"][i][0] / r["beta"][0][0] for i in range(3)]
    assert abs(b[1] + 1.0) < 0.05 and abs(b[2] - 1.0) < 0.05
    # The two tests can disagree: here the max-eigenvalue statistic for r = 1
    # (11.57) is just above its 95% point 11.2246, while the trace (11.64) is below 12.3212.
    assert r["trace"][1] < r["crit_trace"][1]
    assert r["max_eig"][0] > r["crit_max"][0] and r["max_eig"][1] > r["crit_max"][1]


def test_tables() -> None:
    for case in ("none", "c"):
        for table in ("trace", "max"):
            v = [critical_value(table, case, j) for j in range(1, 6)]
            assert all(x < y for x, y in zip(v, v[1:]))
    # With one common trend and an unrestricted constant the limit is chi-square(1).
    assert abs(critical_value("trace", "c", 1) - 1.959964 ** 2) < 1e-3
    # Trace and max-eigenvalue agree when K - r = 1.
    assert critical_value("trace", "none", 1) == critical_value("max", "none", 1)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        johansen([Y1, Y2], "ct", 0)
    with pytest.raises(ValueError):
        johansen([Y1, Y2], "none", 3)
    with pytest.raises(ValueError):
        cholesky([[1.0, 2.0], [2.0, 1.0]])
