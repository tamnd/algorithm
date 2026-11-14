# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/augmented-dickey-fuller-test/. The authors are listed in prov/61BK07.jsonl.
"""Augmented Dickey-Fuller unit root test.

The test regression is

    dy_t = rho * y_(t-1) + [a] + [b t] + sum_(i=1..p) g_i dy_(t-i) + e_t,

with dy_t = y_t - y_(t-1). The statistic is tau = rho-hat / se(rho-hat), the
ordinary t ratio. Under H_0: rho = 0 (a unit root) tau has the nonstandard
Dickey-Fuller law, so it is compared with the MacKinnon (2010) response surface
critical values, not with a t table. trend is "n" (no deterministic terms),
"c" (a constant) or "ct" (a constant and a linear trend).
The code is in this file and not in augmented_dickey_fuller_test.py, because
tools treat a file whose name ends in _test.py as a test file.
"""

import math
import random

# MacKinnon (2010), Queen's Economics Department Working Paper 1227, Table 2,
# one variable (N = 1). Critical value at sample size T: b0 + b1/T + b2/T^2 + b3/T^3.
MACKINNON_2010 = {
    "n": {0.01: (-2.56574, -2.2358, -3.627, 0.0),
          0.05: (-1.94100, -0.2686, -3.365, 31.223),
          0.10: (-1.61682, 0.2656, -2.714, 25.364)},
    "c": {0.01: (-3.43035, -6.5393, -16.786, -79.433),
          0.05: (-2.86154, -2.8903, -4.234, -40.040),
          0.10: (-2.56677, -1.5384, -2.809, 0.0)},
    "ct": {0.01: (-3.95877, -9.0531, -28.428, -134.155),
           0.05: (-3.41049, -4.3904, -9.036, -45.374),
           0.10: (-3.12705, -2.5856, -3.925, -22.380)},
}


def mackinnon_critical_value(trend, level, nobs=None):
    """Lower-tail critical value of tau at the given level (0.01, 0.05 or 0.10).

    nobs=None gives the asymptotic value b0."""
    b = MACKINNON_2010[trend][level]
    if nobs is None:
        return b[0]
    u = 1.0 / nobs
    return b[0] + b[1] * u + b[2] * u * u + b[3] * u * u * u


def qr_mgs(columns):
    """Thin QR factorization of the n x k matrix with the given columns, by
    modified Gram-Schmidt. Returns (q, r) with q a list of k orthonormal columns."""
    k = len(columns)
    q = []
    r = [[0.0] * k for _ in range(k)]
    for j in range(k):
        v = [float(a) for a in columns[j]]
        norm0 = math.sqrt(sum(a * a for a in v))
        for i in range(j):
            d = sum(a * b for a, b in zip(q[i], v))
            r[i][j] = d
            v = [a - d * b for a, b in zip(v, q[i])]
        nrm = math.sqrt(sum(a * a for a in v))
        if norm0 == 0.0 or nrm <= 1e-12 * norm0:
            raise ValueError("the regressors are linearly dependent")
        r[j][j] = nrm
        q.append([a / nrm for a in v])
    return q, r


def upper_inverse(r):
    """Inverse of an upper triangular matrix by back substitution."""
    k = len(r)
    rinv = [[0.0] * k for _ in range(k)]
    for c in range(k):
        for j in range(c, -1, -1):
            rhs = (1.0 if j == c else 0.0) - sum(r[j][l] * rinv[l][c] for l in range(j + 1, c + 1))
            rinv[j][c] = rhs / r[j][j]
    return rinv


def ols(columns, y):
    """Least squares through the QR factorization. Returns (coef, resid, s2, se)
    with s2 = RSS / (n - k) and se the usual standard errors."""
    n, k = len(y), len(columns)
    if n <= k:
        raise ValueError("need more observations than regressors")
    q, r = qr_mgs(columns)
    rinv = upper_inverse(r)
    qty = [sum(a * float(b) for a, b in zip(qj, y)) for qj in q]
    coef = [sum(rinv[j][c] * qty[c] for c in range(j, k)) for j in range(k)]
    resid = [float(y[t]) - sum(coef[j] * float(columns[j][t]) for j in range(k)) for t in range(n)]
    s2 = sum(e * e for e in resid) / (n - k)
    se = [math.sqrt(s2 * sum(rinv[j][c] ** 2 for c in range(j, k))) for j in range(k)]
    return coef, resid, s2, se


def adf_regression(y, lags=0, trend="c", first=None):
    """Fit the ADF regression with a fixed number of lagged differences, on the
    rows t = first .. n-1 (0-based; default first = lags + 1).

    Returns a dict with tau, rho (the coefficient of y_(t-1)), nobs, rss and k."""
    if trend not in MACKINNON_2010:
        raise ValueError("trend must be 'n', 'c' or 'ct'")
    y = [float(v) for v in y]
    n = len(y)
    if first is None:
        first = lags + 1
    dy = [0.0] + [y[t] - y[t - 1] for t in range(1, n)]  # @line L1
    nobs = n - first  # @line L2
    k = 1 + {"n": 0, "c": 1, "ct": 2}[trend] + lags
    cols = [[] for _ in range(k)]
    resp = []
    for t in range(first, n):  # @line L3
        row = [y[t - 1]] + {"n": [], "c": [1.0], "ct": [1.0, float(t)]}[trend] + [dy[t - i] for i in range(1, lags + 1)]
        for j in range(k):
            cols[j].append(row[j])
        resp.append(dy[t])  # @line L4
    if nobs <= k:
        raise ValueError("need more observations than regressors")
    q, r = qr_mgs(cols)  # @line L5
    rinv = upper_inverse(r)
    qty = [sum(a * b for a, b in zip(qj, resp)) for qj in q]
    coef = [sum(rinv[j][c] * qty[c] for c in range(j, k)) for j in range(k)]
    resid = [resp[t] - sum(coef[j] * cols[j][t] for j in range(k)) for t in range(nobs)]
    rss = sum(e * e for e in resid)
    s2 = rss / (nobs - k)  # @line L6
    se = math.sqrt(s2 * sum(v * v for v in rinv[0]))  # @line L7
    tau = coef[0] / se  # @line L8
    return {"tau": tau, "rho": coef[0], "nobs": nobs, "rss": rss, "k": k, "lags": lags}


def schwert_max_lag(n):
    """Schwert (1989) rule: floor(12 (n/100)^(1/4))."""
    return int(12.0 * (n / 100.0) ** 0.25)


def select_lags(y, max_lag, trend="c", criterion="aic"):
    """Choose the number of lagged differences.

    "aic" and "bic" fit every order 0..max_lag on the same rows and minimise
    nobs log(RSS/nobs) + penalty * k. "t-stat" starts at max_lag and drops the
    last lag while its |t| is below 1.645 (general to specific)."""
    y = [float(v) for v in y]
    first = max_lag + 1
    if criterion in ("aic", "bic"):
        best, best_ic = 0, math.inf
        for p in range(max_lag + 1):
            f = adf_regression(y, p, trend, first)
            pen = 2.0 if criterion == "aic" else math.log(f["nobs"])
            ic = f["nobs"] * math.log(f["rss"] / f["nobs"]) + pen * f["k"]
            if ic < best_ic - 1e-12:
                best, best_ic = p, ic
        return best
    if criterion == "t-stat":
        n = len(y)
        for p in range(max_lag, 0, -1):
            rows = range(first, n)
            cols = [[y[t - 1] for t in rows]]
            if trend != "n":
                cols.append([1.0] * len(rows))
            if trend == "ct":
                cols.append([float(t) for t in rows])
            for i in range(1, p + 1):
                cols.append([y[t - i] - y[t - i - 1] for t in rows])
            coef, _, _, se = ols(cols, [y[t] - y[t - 1] for t in rows])
            if abs(coef[-1] / se[-1]) >= 1.645:
                return p
        return 0
    raise ValueError("criterion must be 'aic', 'bic' or 't-stat'")


def augmented_dickey_fuller_test(y, trend="c", lags=None, max_lag=None, criterion="aic"):
    """The ADF test. lags=None selects the order by criterion up to max_lag
    (default: the Schwert rule), then refits on all usable rows.

    Returns tau, the chosen lags, nobs, the 1%, 5% and 10% critical values at
    that nobs, and reject (at 5%). Reject the unit root at level a when tau < critical[a]."""
    y = [float(v) for v in y]
    if lags is None:
        if max_lag is None:
            max_lag = schwert_max_lag(len(y))
        max_lag = max(0, min(max_lag, (len(y) - 4) // 3))
        lags = select_lags(y, max_lag, trend, criterion)
    fit = adf_regression(y, lags, trend)
    fit["critical"] = {a: mackinnon_critical_value(trend, a, fit["nobs"]) for a in (0.01, 0.05, 0.10)}  # @line L9
    fit["reject"] = fit["tau"] < fit["critical"][0.05]  # @line L10
    return fit


def simulate_null(n, trend="c", lags=0, reps=1000, rng=None):
    """tau for reps Gaussian random walks of length n (y_0 = 0, unit variance)."""
    rng = rng or random.Random(0)
    out = []
    for _ in range(reps):
        y, s = [], 0.0
        for _ in range(n):
            s += rng.gauss(0.0, 1.0)
            y.append(s)
        out.append(adf_regression(y, lags, trend)["tau"])
    return out


def monte_carlo_p_value(tau, n, trend="c", lags=0, reps=999, rng=None):
    """(1 + #{simulated tau <= tau}) / (1 + reps), from Gaussian random walks.

    With trend "c" or "ct" and lags = 0, tau does not depend on the start value,
    the drift (for "ct") or the scale, so for Gaussian errors this p-value is
    exact up to Monte Carlo error at every n."""
    sims = simulate_null(n, trend, lags, reps, rng)
    return (1 + sum(1 for s in sims if s <= tau)) / (1 + reps)
