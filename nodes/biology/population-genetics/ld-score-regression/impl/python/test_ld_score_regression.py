# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ld-score-regression/. The authors are listed in prov/E6NC45.jsonl.

import math
import random
from fractions import Fraction
from statistics import correlation

from ld_score_regression import ld_scores, ldsc, r2_unbiased

# Regions of 40 SNPs; within a region the next allele on a haplotype copies the
# previous one with this probability, so LD (and the LD score) varies by region.
COPY = [0.0, 0.5, 0.8, 0.9]
REGION = 40
SPACING = 0.1  # cM between neighbouring SNPs
WINDOW = 2.0  # cM; r2 at 20 SNPs is at most 0.81^20, about 0.015


def snp_design(rng, M):
    """Allele frequencies and copy probabilities of the SNPs."""
    freqs = [0.15 + 0.7 * rng.random() for _ in range(M)]
    copy = [COPY[(j // REGION) % len(COPY)] for j in range(M)]
    return freqs, copy


def haplotype(rng, freqs, copy):
    h = []
    for j, f in enumerate(freqs):
        if j > 0 and rng.random() < copy[j]:
            h.append(h[-1])
        else:
            h.append(1 if rng.random() < f else 0)
    return h


def genotypes(rng, n, freqs, copy):
    G = []
    for _ in range(n):
        a, b = haplotype(rng, freqs, copy), haplotype(rng, freqs, copy)
        G.append([x + y for x, y in zip(a, b)])
    return G


def gwas_chi2(G, y):
    """chi2_j = N r_j^2, the trend statistic of each SNP."""
    n = len(y)
    my = sum(y) / n
    cy = [v - my for v in y]
    syy = sum(v * v for v in cy)
    out = []
    for j in range(len(G[0])):
        x = [G[i][j] for i in range(n)]
        mx = sum(x) / n
        sxy = sum((a - mx) * b for a, b in zip(x, cy))
        sxx = sum((a - mx) ** 2 for a in x)
        out.append(n * sxy * sxy / (sxx * syy))
    return out


def polygenic_trait(rng, G, h2):
    n, M = len(G), len(G[0])
    p = [sum(G[i][j] for i in range(n)) / (2.0 * n) for j in range(M)]
    sd = [math.sqrt(2.0 * q * (1.0 - q)) for q in p]
    beta = [rng.gauss(0.0, math.sqrt(h2 / M)) for _ in range(M)]
    y = []
    for i in range(n):
        g = sum((G[i][j] - 2.0 * p[j]) / sd[j] * beta[j] for j in range(M) if sd[j] > 0)
        y.append(g + rng.gauss(0.0, math.sqrt(1.0 - h2)))
    return y


def simulate(rng, N, M, n_ref, h2):
    """GWAS chi2 of N people and LD scores from a separate panel of n_ref people."""
    freqs, copy = snp_design(rng, M)
    G = genotypes(rng, N, freqs, copy)
    y = polygenic_trait(rng, G, h2)
    ref = genotypes(rng, n_ref, freqs, copy)
    pos = [SPACING * j for j in range(M)]
    return gwas_chi2(G, y), ld_scores(ref, pos, WINDOW)


def test_ld_scores_match_all_pairs_brute_force():
    rng = random.Random(21)
    n, M = 30, 25
    freqs, copy = snp_design(rng, M)
    G = genotypes(rng, n, freqs, copy)
    pos = sorted(rng.uniform(0.0, 3.0) for _ in range(M))
    l = ld_scores(G, pos, 0.5)
    for j in range(M):
        xj = [G[i][j] for i in range(n)]
        want = 0.0
        for k in range(M):
            if abs(pos[k] - pos[j]) <= 0.5:
                xk = [G[i][k] for i in range(n)]
                r = correlation(xj, xk)
                want += r * r - (1 - r * r) / (n - 2)
        assert abs(l[j] - want) < 1e-9


def test_r2_correction_is_exact_at_the_null_mean():
    # For independent SNPs, E[r^2] = 1/(n - 1), and the correction maps it to 0.
    for n in (5, 50, 1000):
        assert r2_unbiased(Fraction(1, n - 1), n) == 0
    assert r2_unbiased(Fraction(1), 10) == 1


def test_corrected_r2_of_independent_snps_averages_zero():
    rng = random.Random(22)
    n, reps = 20, 3000
    vals = []
    for _ in range(reps):
        x = [rng.gauss(0, 1) for _ in range(n)]
        z = [rng.gauss(0, 1) for _ in range(n)]
        r = correlation(x, z)
        vals.append(r2_unbiased(r * r, n))
    m = sum(vals) / reps
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (reps - 1))
    assert abs(m) <= 4 * sd / math.sqrt(reps)


def test_statistics_that_follow_equation_one_exactly():
    rng = random.Random(23)
    J, N, M, h2, a = 400, 5000, 400, 0.3, 0.002
    l = [1.0 + 20.0 * rng.random() for _ in range(J)]
    chi2 = [N * h2 * lj / M + N * a + 1.0 for lj in l]
    res = ldsc(chi2, l, N, M)
    assert abs(res["h2"] - h2) < 1e-9
    assert abs(res["intercept"] - (1.0 + N * a)) < 1e-9
    assert res["se_h2"] < 1e-9 and res["se_intercept"] < 1e-9


def wls_by_normal_equations(x, y, w):
    s0 = sum(w)
    s1 = sum(wi * xi for wi, xi in zip(w, x))
    s2 = sum(wi * xi * xi for wi, xi in zip(w, x))
    t0 = sum(wi * yi for wi, yi in zip(w, y))
    t1 = sum(wi * xi * yi for wi, xi, yi in zip(w, x, y))
    det = s0 * s2 - s1 * s1
    return (s2 * t0 - s1 * t1) / det, (s0 * t1 - s1 * t0) / det


def test_one_round_and_jackknife_against_direct_refits():
    rng = random.Random(24)
    J, N, M, B = 200, 3000, 200, 10
    l = [1.0 + 15.0 * rng.random() for _ in range(J)]
    chi2 = [(1.0 + N * 0.4 * lj / M) * rng.gammavariate(0.5, 2.0) for lj in l]
    res = ldsc(chi2, l, N, M, n_blocks=B, rounds=1)
    h0 = min(max(M * (sum(chi2) / J - 1.0) / (N * sum(l) / J), 0.0), 1.0)
    w = [1.0 / (max(lj, 1.0) * max(1.0 + N * h0 * lj / M, 1.0) ** 2) for lj in l]
    a, b = wls_by_normal_equations(l, chi2, w)
    assert abs(res["intercept"] - a) < 1e-9
    assert abs(res["h2"] - b * M / N) < 1e-12
    hs = []
    for t in range(B):
        idx = [j for j in range(J) if j // (J // B) != t]
        hs.append(wls_by_normal_equations([l[j] for j in idx], [chi2[j] for j in idx],
                                          [w[j] for j in idx])[1] * M / N)
    mean = sum(hs) / B
    se = math.sqrt((B - 1) / B * sum((v - mean) ** 2 for v in hs))
    assert abs(res["se_h2"] - se) < 1e-12


def test_polygenic_trait_slope_gives_h2_and_intercept_near_one():
    rng = random.Random(25)
    h2 = 0.5
    chi2, l = simulate(rng, N=1500, M=480, n_ref=300, h2=h2)
    res = ldsc(chi2, l, 1500, 480)
    z = 4.0
    assert abs(res["h2"] - h2) <= z * res["se_h2"]
    assert abs(res["intercept"] - 1.0) <= z * res["se_intercept"]


def summary_statistics(rng, N, M, h2, a, reach=60):
    """z statistics drawn from their joint law, with a confounding term.

    The correlation of SNPs j < k is the product of the copy probabilities
    from j + 1 to k, so R is known. z = sqrt(N) R beta + eps + sqrt(N a) s with
    beta_j ~ N(0, h2 / M), eps ~ N(0, R) (an autoregressive recursion) and s_j
    independent standard normal. Then E[z_j^2] = N h2 l_j / M + N a + 1 with
    l_j = sum_k R_jk^2, which is returned (to reach SNPs on each side).
    """
    copy = [COPY[(j // REGION) % len(COPY)] for j in range(M)]
    beta = [rng.gauss(0.0, math.sqrt(h2 / M)) for _ in range(M)]
    chi2, l = [], []
    eps = 0.0
    for j in range(M):
        eps = copy[j] * eps + math.sqrt(1.0 - copy[j] ** 2) * rng.gauss(0.0, 1.0) if j else rng.gauss(0.0, 1.0)
        rb, lj = beta[j], 1.0
        r = 1.0
        for k in range(j + 1, min(M, j + reach + 1)):
            r *= copy[k]
            rb += r * beta[k]
            lj += r * r
        r = 1.0
        for k in range(j - 1, max(-1, j - reach - 1), -1):
            r *= copy[k + 1]
            rb += r * beta[k]
            lj += r * r
        zj = math.sqrt(N) * rb + eps + math.sqrt(N * a) * rng.gauss(0.0, 1.0)
        chi2.append(zj * zj)
        l.append(lj)
    return chi2, l


def test_summary_level_simulation_without_confounding():
    rng = random.Random(27)
    N, M, h2 = 5000, 4000, 0.3
    chi2, l = summary_statistics(rng, N, M, h2, 0.0)
    res = ldsc(chi2, l, N, M)
    z = 4.0
    assert abs(res["h2"] - h2) <= z * res["se_h2"]
    assert abs(res["intercept"] - 1.0) <= z * res["se_intercept"]


def test_confounding_raises_the_intercept_not_the_slope():
    rng = random.Random(28)
    N, M, h2, a = 5000, 4000, 0.3, 2e-4
    chi2, l = summary_statistics(rng, N, M, h2, a)
    res = ldsc(chi2, l, N, M)
    z = 4.0
    assert res["intercept"] > 1.0 + z * res["se_intercept"]
    assert abs(res["intercept"] - (1.0 + N * a)) <= z * res["se_intercept"]
    assert abs(res["h2"] - h2) <= z * res["se_h2"]
