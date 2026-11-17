# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snp-heritability-estimation/. The authors are listed in prov/Q44QVJ.jsonl.

import math
import random
from fractions import Fraction

from pg4lmm import chol_logdet, chol_solve, cholesky, eigh, grm, standardize
from snp_heritability_estimation import greml, reml_loglik


def profile_reml(K, y, X, delta):
    """REML with sigma_g^2 profiled out, at V = sigma_g^2 (K + delta I), by a Cholesky factor."""
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
    R = sum(a * b for a, b in zip(r, chol_solve(L, r)))
    df = n - p
    return 0.5 * (df * math.log(df / (2 * math.pi * R)) - df - chol_logdet(L) - chol_logdet(LA))


def simulate(rng, n, m, h2, pmin=0.1, pmax=0.9):
    """Unrelated people, m unlinked SNPs, y = W b + e with Var(W b) about h2 and Var(e) = 1 - h2."""
    freqs = [pmin + (pmax - pmin) * rng.random() for _ in range(m)]
    G = [[(rng.random() < f) + (rng.random() < f) for f in freqs] for _ in range(n)]
    W = standardize(G)
    b = [rng.gauss(0.0, math.sqrt(h2 / m)) for _ in range(m)]
    y = [sum(w * e for w, e in zip(row, b)) + rng.gauss(0.0, math.sqrt(1.0 - h2)) for row in W]
    return G, y


def test_balanced_one_way_layout_gives_the_anova_estimates():
    # With A = blocks of ones (clones in g groups of size k) and an intercept, REML
    # equals the ANOVA estimators: s_e = MSW and s_g = (MSB - MSW) / k when positive.
    rng = random.Random(11)
    g, k = 8, 4
    y = []
    for _ in range(g):
        u = rng.gauss(0.0, 1.0)
        y += [u + rng.gauss(0.0, 0.7) for _ in range(k)]
    n = g * k
    A = [[1.0 if i // k == j // k else 0.0 for j in range(n)] for i in range(n)]
    X = [[1.0] for _ in range(n)]
    fy = [Fraction(v) for v in y]
    grand = sum(fy) / n
    means = [sum(fy[a * k:(a + 1) * k]) / k for a in range(g)]
    msb = k * sum((mu - grand) ** 2 for mu in means) / (g - 1)
    msw = sum((fy[i] - means[i // k]) ** 2 for i in range(n)) / (n - g)
    assert msb > msw
    fit = greml([A], y, X)
    sg, se = fit["theta"]
    assert abs(se - float(msw)) < 1e-7
    assert abs(sg - float((msb - msw) / k)) < 1e-7


def test_estimate_equals_the_maximum_of_the_profile_likelihood():
    rng = random.Random(12)
    n, m = 40, 80
    G, y = simulate(rng, n, m, 0.5)
    K = grm(G)
    X = [[1.0] for _ in range(n)]
    fit = greml([K], y, X)
    sg, se = fit["theta"]
    # The same likelihood, maximized over delta = s_e / s_g by a grid and golden-section search.
    s_min = eigh(K)[0][0]
    lo = math.log(max(-s_min, 0.0) + 1e-3)
    grid = [lo + 0.05 * t for t in range(int((6.0 - lo) / 0.05) + 1)]
    vals = [profile_reml(K, y, X, math.exp(t)) for t in grid]
    j = max(range(len(grid)), key=lambda i: vals[i])
    assert 0 < j < len(grid) - 1
    a, b = grid[j - 1], grid[j + 1]
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    for _ in range(60):
        c, d = b - gr * (b - a), a + gr * (b - a)
        if profile_reml(K, y, X, math.exp(c)) >= profile_reml(K, y, X, math.exp(d)):
            b = d
        else:
            a = c
    delta = math.exp((a + b) / 2)
    best = profile_reml(K, y, X, delta)
    assert abs(se / sg - delta) < 1e-5 * delta
    assert abs(fit["h2"] - 1.0 / (1.0 + delta)) < 1e-5
    # l_R at the estimate, with the constant -(n - p)/2 log(2 pi), equals the profile maximum.
    assert abs(fit["loglik"] - 0.5 * (n - 1) * math.log(2 * math.pi) - best) < 1e-8


def test_two_components_give_a_stationary_point_and_a_local_maximum():
    rng = random.Random(15)
    n, m = 40, 120
    G, y = simulate(rng, n, m, 0.5)
    # Relationship matrices W W^T / m, positive semidefinite, from two halves of the SNPs.
    As = []
    for part in ([row[:m // 2] for row in G], [row[m // 2:] for row in G]):
        W = standardize(part)
        As.append([[sum(a * b for a, b in zip(wi, wj)) / len(wi) for wj in W] for wi in W])
    X = [[1.0, float(i % 2)] for i in range(n)]
    fit = greml(As, y, X)
    th = fit["theta"]
    assert all(v > 1e-3 for v in th)
    f0 = reml_loglik(As, y, X, th)
    for k in range(3):
        h = 1e-4 * th[k]
        up = list(th)
        dn = list(th)
        up[k] += h
        dn[k] -= h
        fu, fd = reml_loglik(As, y, X, up), reml_loglik(As, y, X, dn)
        assert abs(fu - fd) / (2 * h) < 1e-5
        assert fu <= f0 + 1e-12 and fd <= f0 + 1e-12


def test_simulated_heritability_within_four_standard_errors():
    rng = random.Random(14)
    n, m, h2 = 100, 50, 0.6
    G, y = simulate(rng, n, m, h2)
    fit = greml([grm(G)], y, [[1.0] for _ in range(n)])
    z = 4.0
    assert fit["se_h2"] < 0.2
    assert abs(fit["h2"] - h2) <= z * fit["se_h2"]


def test_null_trait_estimate_within_four_standard_errors_of_zero():
    rng = random.Random(15)
    n, m = 100, 50
    G, _ = simulate(rng, n, m, 0.5)
    y = [rng.gauss(0.0, 1.0) for _ in range(n)]
    fit = greml([grm(G)], y, [[1.0] for _ in range(n)])
    z = 4.0
    assert 0.0 <= fit["h2"] <= z * fit["se_h2"]
