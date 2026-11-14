# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cluster-robust-standard-errors/. The authors are listed in prov/X126D2.jsonl.

import math
import random
from fractions import Fraction

import pytest

from cluster_robust_standard_errors import (KINDS, cluster_covariance, confidence_intervals,
                                            wild_cluster_bootstrap)
from stdist import t_ppf

EX_X = [[1, v] for v in [1, 2, 3, 4, 5, 6]]
EX_Y = [2, 3, 2, 4, 7, 8]
EX_G = ["a", "a", "b", "b", "c", "c"]


def solve(a, b):
    k = len(a)
    m = [[Fraction(v) for v in row] + [Fraction(b[i])] for i, row in enumerate(a)]
    for c in range(k):
        piv = next(r for r in range(c, k) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [m[i][k] / m[i][i] for i in range(k)]


def inverse(a):
    n = len(a)
    cols = [solve(a, [int(i == j) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def gram(x):
    p = len(x[0])
    return [[sum(Fraction(r[i]) * r[j] for r in x) for j in range(p)] for i in range(p)]


def fit_exact(x, y):
    p = len(x[0])
    b = solve(gram(x), [sum(Fraction(r[i]) * v for r, v in zip(x, y)) for i in range(p)])
    e = [v - sum(Fraction(a) * c for a, c in zip(r, b)) for r, v in zip(x, y)]
    return b, e


def direct(x, y, groups, kind):
    """(X^T X)^(-1) (sum_g s_g s_g^T) (X^T X)^(-1) times the factor, with explicit exact matrices."""
    n, p = len(x), len(x[0])
    gi = inverse(gram(x))
    b, e = fit_exact(x, y)
    labels = list(dict.fromkeys(groups))
    s = [[sum(Fraction(x[i][j]) * e[i] for i in range(n) if groups[i] == g) for j in range(p)] for g in labels]
    big_g = len(labels)
    factor = 1 if kind == "CR0" else Fraction(big_g, big_g - 1) * Fraction(n - 1, n - p)
    meat = [[factor * sum(sg[i] * sg[j] for sg in s) for j in range(p)] for i in range(p)]
    v = [[sum(gi[i][k] * meat[k][l] * gi[l][j] for k in range(p) for l in range(p)) for j in range(p)]
         for i in range(p)]
    return b, e, s, v


def hc_direct(x, y, kind):
    """HC0 or HC1 with explicit exact matrices."""
    n, p = len(x), len(x[0])
    gi = inverse(gram(x))
    _, e = fit_exact(x, y)
    factor = 1 if kind == "HC0" else Fraction(n, n - p)
    meat = [[factor * sum(ei * ei * r[i] * r[j] for ei, r in zip(e, x)) for j in range(p)] for i in range(p)]
    return [[sum(gi[i][k] * meat[k][l] * gi[l][j] for k in range(p) for l in range(p)) for j in range(p)]
            for i in range(p)]


def close(a, b):
    for row_a, row_b in zip(a, b):
        assert row_a == pytest.approx([float(t) for t in row_b], rel=1e-9, abs=1e-12)


def test_page_example_exact():
    b, e, s, v0 = direct(EX_X, EX_Y, EX_G, "CR0")
    assert b == [Fraction(-1, 15), Fraction(44, 35)]
    assert all(e[i] > 0 for i in (0, 1, 4, 5)) and e[2] < 0 and e[3] < 0  # residuals share signs in clusters
    assert sum(sg[0] for sg in s) == 0 and sum(sg[1] for sg in s) == 0  # the scores add to X^T e = 0
    v1 = direct(EX_X, EX_Y, EX_G, "CR1")[3]
    assert v1[1][1] == v0[1][1] * Fraction(3, 2) * Fraction(5, 4)
    for kind, v in (("CR0", v0), ("CR1", v1)):
        fit = cluster_covariance(EX_X, EX_Y, EX_G, kind)
        close(fit.cov, v)
        assert fit.clusters == 3 and fit.df == 2
    assert cluster_covariance(EX_X, EX_Y, EX_G, "CR0").se[1] == pytest.approx(0.2171, abs=1e-4)
    assert cluster_covariance(EX_X, EX_Y, EX_G, "CR1").se[1] == pytest.approx(0.2972, abs=1e-4)
    assert math.sqrt(float(hc_direct(EX_X, EX_Y, "HC1")[1][1])) == pytest.approx(0.2079, abs=1e-4)


def test_matches_direct_matrices_on_random_designs_exact():
    rng = random.Random(11)
    done = 0
    while done < 10:
        n = rng.randint(8, 14)
        x = [[1, rng.randint(-4, 4), rng.randint(0, 5)] for _ in range(n)]
        y = [rng.randint(-9, 9) for _ in range(n)]
        groups = [rng.randint(0, 3) for _ in range(n)]
        if len(set(groups)) < 2:
            continue
        try:
            ref = {k: direct(x, y, groups, k)[3] for k in KINDS}
        except StopIteration:
            continue  # singular design
        for kind in KINDS:
            close(cluster_covariance(x, y, groups, kind).cov, ref[kind])
        done += 1


def test_singleton_clusters_give_hc0_and_hc1_exact():
    """With one row per cluster s_i = x_i e_i, so CR0 = HC0, and G = n turns the CR1 factor into n/(n - p)."""
    rng = random.Random(12)
    for _ in range(5):
        n = 9
        x = [[1, rng.randint(-5, 5), rng.randint(-5, 5)] for _ in range(n)]
        y = [rng.randint(-9, 9) for _ in range(n)]
        try:
            hc0, hc1 = hc_direct(x, y, "HC0"), hc_direct(x, y, "HC1")
        except StopIteration:
            continue
        groups = list(range(n))
        assert direct(x, y, groups, "CR0")[3] == hc0
        assert direct(x, y, groups, "CR1")[3] == hc1
        close(cluster_covariance(x, y, groups, "CR0").cov, hc0)
        close(cluster_covariance(x, y, groups, "CR1").cov, hc1)


def test_rank_is_at_most_g_minus_one_exact():
    """The cluster scores sum to X^T e = 0, so the middle matrix has rank at most G - 1."""
    rng = random.Random(13)
    x = [[1, rng.randint(-5, 5), rng.randint(-5, 5)] for _ in range(10)]
    y = [rng.randint(-9, 9) for _ in range(10)]
    groups = [0] * 5 + [1] * 5
    _, _, s, v = direct(x, y, groups, "CR0")
    assert [s[0][j] + s[1][j] for j in range(3)] == [0, 0, 0]
    det = (v[0][0] * (v[1][1] * v[2][2] - v[1][2] * v[2][1]) - v[0][1] * (v[1][0] * v[2][2] - v[1][2] * v[2][0])
           + v[0][2] * (v[1][0] * v[2][1] - v[1][1] * v[2][0]))
    assert det == 0
    with pytest.raises(ValueError):
        cluster_covariance(x, y, [7] * 10)  # one cluster: the estimate would be the zero matrix
    with pytest.raises(ValueError):
        cluster_covariance(x, y, groups, "CR9")


def test_labels_and_row_order_do_not_matter():
    perm = [3, 0, 5, 1, 4, 2]
    a = cluster_covariance(EX_X, EX_Y, EX_G, "CR1")
    b = cluster_covariance([EX_X[i] for i in perm], [EX_Y[i] for i in perm], [{"a": 9, "b": 4, "c": 1}[EX_G[i]] for i in perm])
    close(b.cov, [[Fraction(t) for t in row] for row in a.cov])


def draw(rng, big_g, m):
    """Random intercepts in the errors and a cluster component in x: both intraclass correlations are 1/2."""
    x, y, grp = [], [], []
    for g in range(big_g):
        zg, ag = rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)
        for _ in range(m):
            xv = zg + rng.gauss(0.0, 1.0)
            x.append([1.0, xv])
            y.append(1.0 + xv + ag + rng.gauss(0.0, 1.0))
            grp.append(g)
    return x, y, grp


def test_coverage_measured():
    """G = 20 clusters of 10. Measured with r = 1000: CR1 with t_19 covered 0.920, the usual and
    HC1 intervals 0.707 and 0.691. Here r = 300 (4 SE about 0.06 near 0.9): CR1 at least 0.86, the usual
    interval at most 0.80."""
    rng = random.Random(20261114)
    r, hit_cr, hit_naive = 300, 0, 0
    for _ in range(r):
        x, y, grp = draw(rng, 20, 10)
        f = cluster_covariance(x, y, grp, "CR1")
        lo, hi = confidence_intervals(f)[1]
        hit_cr += lo <= 1.0 <= hi
        n = len(y)
        xb = sum(row[1] for row in x) / n
        se = math.sqrt(sum(t * t for t in f.residuals) / (n - 2) / sum((row[1] - xb) ** 2 for row in x))
        hit_naive += abs(f.b[1] - 1.0) <= t_ppf(0.975, n - 2) * se
    assert hit_cr / r >= 0.86
    assert hit_naive / r <= 0.80


def test_wild_cluster_bootstrap_size_and_power_measured():
    """G = 6 clusters of 10. Measured with r = 200 and B = 99: rejection rate 0.050 at the 5% level,
    while CR1 with t_5 covered only 0.905. Here r = 100 (4 SE about 0.09): rate at most 0.14."""
    rng = random.Random(20261116)
    r, rej = 100, 0
    for rep in range(r):
        x, y, grp = draw(rng, 6, 10)
        _, pv = wild_cluster_bootstrap(x, y, grp, 1, 1.0, reps=99, seed=rep + 1)
        rej += pv <= 0.05
    assert rej / r <= 0.14
    x, y, grp = draw(random.Random(5), 12, 10)
    t, pv = wild_cluster_bootstrap(x, y, grp, 1, 0.0, reps=199, seed=3)  # the true slope is 1
    assert abs(t) > 4 and pv <= 0.01
