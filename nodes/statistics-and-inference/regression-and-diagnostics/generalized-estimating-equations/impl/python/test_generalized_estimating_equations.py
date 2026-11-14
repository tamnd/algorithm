# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-estimating-equations/. The authors are listed in prov/F7TMV3.jsonl.

import math
import random
from fractions import Fraction

import pytest

from generalized_estimating_equations import gee, glm_independence_score, working_correlation

F = Fraction
EX_X = [1, 2, 3, 4, 5, 6]
EX_Y = [2, 3, 2, 4, 7, 8]


def ex_clusters(conv=F):
    return [([[conv(1), conv(EX_X[i])] for i in (2 * g, 2 * g + 1)], [conv(EX_Y[i]) for i in (2 * g, 2 * g + 1)])
            for g in range(3)]


def mat_solve(a, b):
    """Plain Gauss-Jordan on Fractions, written separately from the module."""
    k = len(a)
    m = [[F(v) for v in row] + [F(b[i])] for i, row in enumerate(a)]
    for c in range(k):
        piv = next(r for r in range(c, k) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [m[i][k] / m[i][i] for i in range(k)]


def mat_inv(a):
    k = len(a)
    cols = [mat_solve(a, [1 if i == j else 0 for i in range(k)]) for j in range(k)]
    return [[cols[j][i] for j in range(k)] for i in range(k)]


def matmul(a, b):
    return [[sum(a[i][t] * b[t][j] for t in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def cr0_direct(clusters):
    """(X^T X)^-1 (sum_g X_g^T e_g e_g^T X_g) (X^T X)^-1 with OLS residuals, all in Fractions."""
    x = [row for xs, _ in clusters for row in xs]
    y = [v for _, ys in clusters for v in ys]
    xtx = matmul(transpose(x), x)
    b = mat_solve(xtx, [sum(r[j] * v for r, v in zip(x, y)) for j in range(len(x[0]))])
    meat = [[F(0)] * len(b) for _ in b]
    for xs, ys in clusters:
        e = [v - sum(c * t for c, t in zip(b, r)) for r, v in zip(xs, ys)]
        s = [sum(r[j] * ei for r, ei in zip(xs, e)) for j in range(len(b))]
        for i in range(len(b)):
            for j in range(len(b)):
                meat[i][j] += s[i] * s[j]
    inv = mat_inv(xtx)
    return b, matmul(matmul(inv, meat), inv)


def gls_direct(clusters, kind, alpha):
    """GLS with the block diagonal covariance built from R(alpha), solved on the full n x n matrix."""
    x = [row for xs, _ in clusters for row in xs]
    y = [v for _, ys in clusters for v in ys]
    n = len(y)
    sigma = [[F(0)] * n for _ in range(n)]
    off = 0
    for _, ys in clusters:
        m = len(ys)
        for i in range(m):
            for j in range(m):
                if kind == "exchangeable":
                    sigma[off + i][off + j] = F(1) if i == j else alpha
                else:
                    sigma[off + i][off + j] = alpha ** abs(i - j)
        off += m
    sinv = mat_inv(sigma)
    xt_si = matmul(transpose(x), sinv)
    return mat_solve(matmul(xt_si, x), [sum(r * v for r, v in zip(row, y)) for row in xt_si])


def test_page_example_exact():
    r = gee(ex_clusters(), "gaussian", "independence")
    assert r.b == [F(-1, 15), F(44, 35)]  # the least squares line
    assert r.phi == F(149, 105)  # residual sum of squares over n - p
    b, cov = cr0_direct(ex_clusters())
    assert r.cov == cov  # independence GEE sandwich = CR0 cluster-robust covariance
    assert r.se[1] == pytest.approx(0.2171, abs=1e-4)
    assert math.sqrt(r.naive[1][1]) == pytest.approx(0.2848, abs=1e-4)
    fixed = gee(ex_clusters(), "gaussian", "exchangeable", alpha=F(1, 2))
    assert fixed.b == [F(-13, 123), F(52, 41)]
    est = gee(ex_clusters(float), "gaussian", "exchangeable")
    assert est.converged
    assert est.alpha == pytest.approx(0.5871, abs=1e-4)
    assert est.b == pytest.approx([-0.1189, 1.2721], abs=1e-4)
    assert est.se[1] == pytest.approx(0.1903, abs=1e-4)


def test_gaussian_fixed_alpha_is_gls_exact():
    rng = random.Random(41)
    for kind, alpha in (("exchangeable", F(1, 3)), ("exchangeable", F(-1, 5)), ("ar1", F(2, 5)), ("ar1", F(-1, 2))):
        for _ in range(3):
            clusters = []
            for _ in range(rng.randint(3, 5)):
                m = rng.randint(1, 4)
                xs = [[F(1), F(rng.randint(-4, 4)), F(rng.randint(0, 3))] for _ in range(m)]
                ys = [F(rng.randint(-9, 9)) for _ in range(m)]
                clusters.append((xs, ys))
            try:
                expect = gls_direct(clusters, kind, alpha)
            except StopIteration:
                continue
            assert gee(clusters, "gaussian", kind, alpha=alpha).b == expect


def test_singleton_clusters_give_hc0_exact():
    rng = random.Random(42)
    rows = [([[F(1), F(rng.randint(-5, 5))]], [F(rng.randint(-9, 9))]) for _ in range(7)]
    r = gee(rows, "gaussian", "exchangeable", alpha=F(1, 3))  # alpha has no effect with m_i = 1
    b, cov = cr0_direct(rows)
    assert r.b == b and r.cov == cov


def test_independence_equals_glm_fit():
    rng = random.Random(43)
    for family in ("poisson", "binomial"):
        clusters = []
        for _ in range(25):
            u = rng.gauss(0.0, 0.5)
            xs = [[1.0, rng.gauss(0.0, 1.0)] for _ in range(3)]
            ys = []
            for row in xs:
                eta = 0.3 + 0.6 * row[1] + u
                if family == "poisson":
                    lam, k, pr = math.exp(-math.exp(eta)), 0, 1.0
                    while True:
                        pr *= rng.random()
                        if pr <= lam:
                            break
                        k += 1
                    ys.append(float(k))
                else:
                    ys.append(1.0 if rng.random() < 1.0 / (1.0 + math.exp(-eta)) else 0.0)
            clusters.append((xs, ys))
        r = gee(clusters, family, "independence")
        assert r.converged
        # The GLM score is 0 at the GEE estimate, and the log-likelihood is strictly concave for a
        # canonical link, so this is the GLM maximum likelihood fit.
        assert max(abs(s) for s in glm_independence_score(clusters, r.b, family)) < 1e-8
        # Pooling the clusters into singletons changes the variance but not the estimate.
        singles = [([row], [v]) for xs, ys in clusters for row, v in zip(xs, ys)]
        assert gee(singles, family, "independence").b == pytest.approx(r.b, abs=1e-9)


def test_estimating_equation_and_invariance():
    rng = random.Random(44)
    clusters = []
    for _ in range(20):
        u = rng.gammavariate(2.0, 0.5)
        xs = [[1.0, rng.random(), t / 3.0] for t in range(4)]
        ys = []
        for row in xs:
            lam, k, pr = math.exp(-u * math.exp(0.5 + 0.4 * row[1] + 0.3 * row[2])), 0, 1.0
            while True:
                pr *= rng.random()
                if pr <= lam:
                    break
                k += 1
            ys.append(float(k))
        clusters.append((xs, ys))
    for kind in ("exchangeable", "ar1"):
        r = gee(clusters, "poisson", kind)
        assert r.converged
        fixed = gee(clusters, "poisson", kind, alpha=r.alpha, b0=r.b)
        assert fixed.b == pytest.approx(r.b, abs=1e-8)
        assert gee(list(reversed(clusters)), "poisson", kind).b == pytest.approx(r.b, abs=1e-8)
    r = working_correlation(3, "ar1", F(1, 2))
    assert r == [[1, F(1, 2), F(1, 4)], [F(1, 2), 1, F(1, 2)], [F(1, 4), F(1, 2), 1]]


def test_coverage_and_efficiency_measured():
    """Random intercept model, G = 30 clusters of 4, intra-cluster correlation 0.5. With r = 1000 the
    95% coverage for the cluster-level slope was: independence model-based 0.777, independence
    sandwich 0.921, exchangeable sandwich 0.921; the standard deviation of the within-cluster slope
    was 0.1317 (independence) and 0.1055 (exchangeable). Here r = 120 (4 SE of a coverage near 0.92
    is about 0.10)."""
    rng = random.Random(11)
    g_count, m, r = 30, 4, 120
    xs = [(g % 10) / 9.0 for g in range(g_count)]
    ws = [[rng.gauss(0, 1) for _ in range(m)] for _ in range(g_count)]
    z = 1.959963984540054
    naive = sand = 0
    w_ind, w_exc = [], []
    for _ in range(r):
        cl = []
        for g in range(g_count):
            a = rng.gauss(0, 1)
            cl.append(([[1.0, xs[g], ws[g][j]] for j in range(m)],
                       [1.0 + 0.5 * xs[g] + 0.5 * ws[g][j] + a + rng.gauss(0, 1) for j in range(m)]))
        ri = gee(cl, "gaussian", "independence")
        re = gee(cl, "gaussian", "exchangeable")
        naive += abs(ri.b[1] - 0.5) <= z * math.sqrt(ri.naive[1][1])
        sand += abs(re.b[1] - 0.5) <= z * re.se[1]
        w_ind.append(ri.b[2])
        w_exc.append(re.b[2])

    def sd(v):
        mu = sum(v) / len(v)
        return math.sqrt(sum((t - mu) ** 2 for t in v) / (len(v) - 1))

    assert sand / r >= 0.83
    assert naive / r <= 0.88
    assert sd(w_exc) < 0.92 * sd(w_ind)


def test_bad_inputs():
    with pytest.raises(ValueError):
        gee(ex_clusters(), "gamma", "independence")
    with pytest.raises(ValueError):
        gee(ex_clusters(), "gaussian", "unstructured")
    with pytest.raises(ValueError):
        gee([], "gaussian", "independence")
    with pytest.raises(ValueError):
        gee([([[1, 2]], [1, 2])], "gaussian", "independence")
    with pytest.raises(ValueError):
        gee([([[1, 2]], [1])], "gaussian", "independence")  # n = 1 <= p = 2
