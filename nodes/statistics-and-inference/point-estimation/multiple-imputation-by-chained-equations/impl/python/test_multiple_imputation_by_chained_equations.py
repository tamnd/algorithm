# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-imputation-by-chained-equations/. The authors are listed in prov/XHM517.jsonl.

import math
import random
from fractions import Fraction

from multiple_imputation_by_chained_equations import bayes_regression_draw, mice
from stdist import t_ppf


def exact_ols(x, y):
    """Normal equations solved in exact rational arithmetic; returns (beta, (X'X)^-1, rss)."""
    p = len(x[0])
    fx = [[Fraction(v) for v in r] for r in x]
    fy = [Fraction(v) for v in y]
    a = [[sum(r[i] * r[j] for r in fx) for j in range(p)] + [Fraction(int(i == j)) for j in range(p)] for i in range(p)]
    for c in range(p):
        piv = next(r for r in range(c, p) if a[r][c] != 0)
        a[c], a[piv] = a[piv], a[c]
        pv = a[c][c]
        a[c] = [v / pv for v in a[c]]
        for r in range(p):
            if r != c:
                f = a[r][c]
                a[r] = [u - f * v for u, v in zip(a[r], a[c])]
    inv = [row[p:] for row in a]
    xty = [sum(r[i] * yi for r, yi in zip(fx, fy)) for i in range(p)]
    beta = [sum(inv[i][j] * xty[j] for j in range(p)) for i in range(p)]
    rss = sum((yi - sum(b * c for b, c in zip(beta, r))) ** 2 for r, yi in zip(fx, fy))
    return [float(b) for b in beta], [[float(v) for v in row] for row in inv], float(rss)


def make_table(seed, n, miss_cols=(0,), rate=0.3):
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        z = rng.gauss(0, 1)
        x = 0.5 * z + rng.gauss(0, 1)
        y = 1 + x - z + rng.gauss(0, 1)
        rows.append([y, x, z])
    for r in rows:
        for j in miss_cols:
            if rng.random() < rate:
                r[j] = None
    return rows


def test_one_incomplete_column_is_single_bayesian_regression_imputation():
    data = make_table(1, 40)
    res = mice(data, m=1, iters=1, seed=99)
    # reference: same random stream, independent arithmetic
    rng = random.Random(99)
    miss = [i for i, r in enumerate(data) if r[0] is None]
    obs = [i for i, r in enumerate(data) if r[0] is not None]
    pool = [data[i][0] for i in obs]
    for _ in miss:
        rng.choice(pool)
    x = [[1.0, data[i][1], data[i][2]] for i in obs]
    beta, inv, rss = exact_ols(x, [data[i][0] for i in obs])
    s2 = rss / (2.0 * rng.gammavariate((len(obs) - 3) / 2.0, 1.0))
    low = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(i + 1):
            t = inv[i][j] - sum(low[i][k] * low[j][k] for k in range(j))
            low[i][j] = math.sqrt(t) if i == j else t / low[j][j]
    zs = [rng.gauss(0, 1) for _ in range(3)]
    bstar = [beta[i] + math.sqrt(s2) * sum(low[i][j] * zs[j] for j in range(3)) for i in range(3)]
    for i in miss:
        expect = bstar[0] + bstar[1] * data[i][1] + bstar[2] * data[i][2] + math.sqrt(s2) * rng.gauss(0, 1)
        assert abs(res.imputations[0][i][0] - expect) < 1e-9


def test_observed_values_kept_and_all_filled():
    data = make_table(2, 60, miss_cols=(0, 1, 2), rate=0.2)
    for method in ("norm", "pmm"):
        res = mice(data, m=3, iters=4, seed=5, method=method)
        assert len(res.imputations) == 3 and len(res.chain_means[0]) == 4
        for table in res.imputations:
            for r0, r1 in zip(data, table):
                assert all(v is not None for v in r1)
                assert all(a == b for a, b in zip(r0, r1) if a is not None)


def test_pmm_imputes_only_observed_values():
    data = make_table(3, 50, miss_cols=(0, 1), rate=0.3)
    res = mice(data, m=2, iters=3, seed=6, method="pmm")
    for j in (0, 1):
        seen = {r[j] for r in data if r[j] is not None}
        for table in res.imputations:
            assert all(table[i][j] in seen for i in range(len(data)) if data[i][j] is None)


def test_posterior_draw_moments():
    rng = random.Random(7)
    x = [[1.0, float(v)] for v in range(12)]
    y = [0.5 + 0.8 * v + rng.gauss(0, 1) for v in range(12)]
    beta, inv, rss = exact_ols(x, y)
    r = 20000
    draws = [bayes_regression_draw(x, y, rng) for _ in range(r)]
    s2 = [d[2] ** 2 for d in draws]
    assert abs(sum(s2) / r / (rss / (12 - 2 - 2)) - 1) < 0.03  # E sigma^2 = RSS / (n - p - 2)
    for k in range(2):
        mk = sum(d[1][k] for d in draws) / r
        sd = math.sqrt(rss / 8 * inv[k][k])
        assert abs(mk - beta[k]) < 4 * sd / math.sqrt(r)
        assert abs(draws[0][0][k] - beta[k]) < 1e-9


def pool(qs, us):
    m = len(qs)
    qbar = sum(qs) / m
    w = sum(us) / m
    b = sum((q - qbar) ** 2 for q in qs) / (m - 1)
    t = w + (1 + 1 / m) * b
    df = (m - 1) * (1 + w / ((1 + 1 / m) * b)) ** 2
    return qbar, t, df


def test_coverage_two_incomplete_columns_measured():
    # Measured, not proved. y and x both incomplete, missingness depends on z (MAR).
    rng = random.Random(8)
    reps, n = 60, 150
    hits_mean = hits_slope = cc_hits = 0
    for rep in range(reps):
        rows = []
        for _ in range(n):
            z = rng.gauss(0, 1)
            x = 0.5 * z + rng.gauss(0, 1)
            y = 1 + x - 2 * z + rng.gauss(0, 1)
            py =1 / (1 + math.exp(-(-0.8 + 1.5 * z)))
            px = 1 / (1 + math.exp(-(-1.2 - 1.0 * z)))
            rows.append([None if rng.random() < py else y, None if rng.random() < px else x, z])
        res = mice(rows, m=5, iters=5, seed=rep)
        qs, us, qs2, us2 = [], [], [], []
        for t in res.imputations:
            ys = [r[0] for r in t]
            my = sum(ys) / n
            qs.append(my)
            us.append(sum((v - my) ** 2 for v in ys) / (n - 1) / n)
            beta, inv, rss = exact_ols([[1.0, r[1], r[2]] for r in t], ys)
            qs2.append(beta[1])
            us2.append(rss / (n - 3) * inv[1][1])
        qbar, tv, df = pool(qs, us)
        hits_mean += abs(qbar - 1) <= t_ppf(0.975, df) * math.sqrt(tv)
        qbar, tv, df = pool(qs2, us2)
        hits_slope += abs(qbar - 1) <= t_ppf(0.975, df) * math.sqrt(tv)
        obs_y = [r[0] for r in rows if r[0] is not None]
        mc = sum(obs_y) / len(obs_y)
        se = math.sqrt(sum((v - mc) ** 2 for v in obs_y) / (len(obs_y) - 1) / len(obs_y))
        cc_hits += abs(mc - 1) <= 1.96 * se
    assert hits_mean / reps > 0.85 and hits_slope / reps > 0.85
    assert cc_hits / reps < 0.5
