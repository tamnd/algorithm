# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixed-model-association/. The authors are listed in prov/HRTZ5C.jsonl.

import math
import random
from statistics import NormalDist

from mixed_model_association import fit_null, reml_profile, scan, weighted_ls
from pg4lmm import (
    chol_inverse,
    chol_logdet,
    chol_solve,
    cholesky,
    eigh,
    grm,
    matmul,
    simulate_two_populations,
    transpose,
)

MEDIAN = NormalDist().inv_cdf(0.75) ** 2


def lambda_sd(m):
    x = MEDIAN
    dens = math.exp(-x / 2) / math.sqrt(2 * math.pi * x)
    return 1.0 / (2 * dens * math.sqrt(m)) / x


def direct_reml(K, y, X, delta):
    """REML profile likelihood from V = K + delta I by a Cholesky factor."""
    n, p = len(y), len(X[0])
    V = [[K[i][j] + (delta if i == j else 0.0) for j in range(n)] for i in range(n)]
    L = cholesky(V)
    Vinv_X = [chol_solve(L, [X[i][a] for i in range(n)]) for a in range(p)]
    Vinv_y = chol_solve(L, y)
    A = [[sum(X[i][a] * Vinv_X[c][i] for i in range(n)) for c in range(p)] for a in range(p)]
    rhs = [sum(X[i][a] * Vinv_y[i] for i in range(n)) for a in range(p)]
    LA = cholesky(A)
    beta = chol_solve(LA, rhs)
    r = [y[i] - sum(X[i][a] * beta[a] for a in range(p)) for i in range(n)]
    Vr = chol_solve(L, r)
    R = sum(a * b for a, b in zip(r, Vr))
    df = n - p
    return 0.5 * (df * math.log(df / (2 * math.pi * R)) - df - chol_logdet(L) - chol_logdet(LA))


def direct_gls(K, y, X, g, sg2, se2):
    """GLS of y on [X, g] with V = sg2 K + se2 I, by a dense inverse."""
    n = len(y)
    V = [[sg2 * K[i][j] + (se2 if i == j else 0.0) for j in range(n)] for i in range(n)]
    Vi = chol_inverse(cholesky(V))
    Z = [X[i] + [g[i]] for i in range(n)]
    Zt = transpose(Z)
    A = matmul(matmul(Zt, Vi), Z)
    LA = cholesky(A)
    rhs = [sum(Zt[a][i] * sum(Vi[i][k] * y[k] for k in range(n)) for i in range(n)) for a in range(len(Zt))]
    coef = chol_solve(LA, rhs)
    Ainv = chol_inverse(LA)
    return coef[-1], Ainv[-1][-1]


def small_data(rng, n=30, m=60):
    G, pop = simulate_two_populations(rng, n // 2, n - n // 2, m, 0.1)
    K = grm(G)
    X = [[1.0, rng.gauss(0, 1)] for _ in range(n)]
    y = [0.5 * pop[i] + 0.3 * X[i][1] + rng.gauss(0, 1) for i in range(n)]
    return G, K, X, y


def test_eigh_reconstructs_matrix():
    rng = random.Random(1)
    n = 12
    B = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    A = [[(B[i][j] + B[j][i]) / 2 for j in range(n)] for i in range(n)]
    d, V = eigh(A)
    assert all(d[k] <= d[k + 1] for k in range(n - 1))
    for i in range(n):
        for j in range(n):
            a = sum(V[i][k] * d[k] * V[j][k] for k in range(n))
            o = sum(V[k][i] * V[k][j] for k in range(n))
            assert abs(a - A[i][j]) < 1e-10
            assert abs(o - (1.0 if i == j else 0.0)) < 1e-10


def test_spectral_reml_equals_direct_reml():
    rng = random.Random(2)
    G, K, X, y = small_data(rng)
    fit = fit_null(K, y, X)
    for delta in (0.05, 0.3, 1.0, 4.0, 30.0):
        a = reml_profile(fit["s"], fit["yt"], fit["Xt"], delta)
        b = direct_reml(K, y, X, delta)
        assert abs(a - b) < 1e-8


def test_reml_maximum_beats_a_fine_grid():
    rng = random.Random(3)
    G, K, X, y = small_data(rng)
    fit = fit_null(K, y, X)
    # The GRM has a slightly negative eigenvalue (about -0.03), so K + delta I
    # is positive definite only for delta above it.
    lo = math.log(-min(fit["s"]) + 1e-3)
    best = max(direct_reml(K, y, X, math.exp(lo + 0.01 * k)) for k in range(1201))
    assert fit["reml"] >= best - 1e-9
    assert abs(direct_reml(K, y, X, fit["delta"]) - fit["reml"]) < 1e-8


def test_scan_equals_dense_gls():
    rng = random.Random(4)
    G, K, X, y = small_data(rng)
    fit = fit_null(K, y, X)
    snps = [[float(G[i][j]) for i in range(len(G))] for j in range(5)]
    res = scan(fit, snps)
    for g, (b, se, T, p) in zip(snps, res):
        b2, v2 = direct_gls(K, y, X, g, fit["sigma_g2"], fit["sigma_e2"])
        assert abs(b - b2) < 1e-8 * max(1.0, abs(b2))
        assert abs(se * se - v2) < 1e-8 * v2
        assert abs(T - b2 * b2 / v2) < 1e-6 * max(1.0, T)


def test_identity_kinship_gives_weighted_ols():
    # With K = I the model is ordinary least squares with variance sg2 + se2.
    rng = random.Random(6)
    n = 25
    K = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    X = [[1.0] for _ in range(n)]
    y = [rng.gauss(2.0, 1.5) for _ in range(n)]
    fit = fit_null(K, y, X)
    g = [float(rng.randint(0, 2)) for _ in range(n)]
    (b, se, T, p), = scan(fit, [g])
    coef, inv, rss = weighted_ls([[1.0, gi] for gi in g], y, [1.0] * n)
    total = fit["sigma_g2"] + fit["sigma_e2"]
    assert abs(b - coef[1]) < 1e-9
    assert abs(se * se - total * inv[1][1]) < 1e-9


def ols_wald(y, X, g):
    n = len(y)
    Z = [X[i] + [g[i]] for i in range(n)]
    coef, inv, rss = weighted_ls(Z, y, [1.0] * n)
    s2 = rss / (n - len(Z[0]))
    return coef[-1] ** 2 / (s2 * inv[-1][-1])


def test_structured_sample_ols_inflated_mixed_model_calibrated():
    rng = random.Random(8)
    n, m, m_test = 100, 400, 400
    G, pop = simulate_two_populations(rng, 50, 50, m + m_test, 0.1)
    K = grm([row[:m] for row in G])
    X = [[1.0] for _ in range(n)]
    # The trait differs between the populations; no tested SNP has an effect.
    y = [1.5 * pop[i] + rng.gauss(0, 1) for i in range(n)]
    snps = [[float(G[i][j]) for i in range(n)] for j in range(m, m + m_test)]
    ols = sorted(ols_wald(y, X, g) for g in snps)
    lam_ols = (ols[m_test // 2 - 1] + ols[m_test // 2]) / 2 / MEDIAN
    fit = fit_null(K, y, X)
    T = sorted(r[2] for r in scan(fit, snps))
    lam_mm = (T[m_test // 2 - 1] + T[m_test // 2]) / 2 / MEDIAN
    assert lam_ols > 1.0 + 4 * lambda_sd(m_test)
    assert abs(lam_mm - 1.0) <= 4 * lambda_sd(m_test)
