# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/engle-granger-test/. The authors are listed in prov/33J9EX.jsonl.
"""The Engle-Granger residual-based test for cointegration, and the two-step
error correction estimate.

Step 1 regresses y_t on deterministic terms and on the m regressors x_t by
least squares and keeps the residuals u_t. Step 2 runs a Dickey-Fuller
regression on u_t with no deterministic terms,

    du_t = rho u_(t-1) + sum_(i=1..p) g_i du_(t-i) + e_t,

and returns the t ratio tau of rho. Under the null of no cointegration tau has
a nonstandard law that depends on N = m + 1 and on the deterministic terms, so
it is compared with the MacKinnon (2010) response surface for N variables.
The code is in this file and not in engle_granger_test.py, because tools
treat a file whose name ends in _test.py as a test file.
"""

import math
import random

# MacKinnon (2010), Queen's Economics Department Working Paper 1227, Table 2.
# Keys: (case, N) -> {level: (b0, b1, b2, b3)}; critical value b0 + b1/T + b2/T^2 + b3/T^3.
MACKINNON_2010 = {
    ("c", 1): {0.01: (-3.43035, -6.5393, -16.786, -79.433), 0.05: (-2.86154, -2.8903, -4.234, -40.040),
               0.10: (-2.56677, -1.5384, -2.809, 0.0)},
    ("c", 2): {0.01: (-3.89644, -10.9519, -33.527, 0.0), 0.05: (-3.33613, -6.1101, -6.823, 0.0),
               0.10: (-3.04445, -4.2412, -2.720, 0.0)},
    ("c", 3): {0.01: (-4.29374, -14.4354, -33.195, 47.433), 0.05: (-3.74066, -8.5632, -10.852, 27.982),
               0.10: (-3.45218, -6.2143, -3.718, 0.0)},
    ("c", 4): {0.01: (-4.64332, -18.1031, -37.972, 0.0), 0.05: (-4.09600, -11.2349, -11.175, 0.0),
               0.10: (-3.81020, -8.3931, -4.137, 0.0)},
    ("c", 5): {0.01: (-4.95756, -21.8883, -45.142, 0.0), 0.05: (-4.41519, -14.0405, -12.575, 0.0),
               0.10: (-4.13157, -10.7417, -3.784, 0.0)},
    ("ct", 1): {0.01: (-3.95877, -9.0531, -28.428, -134.155), 0.05: (-3.41049, -4.3904, -9.036, -45.374),
                0.10: (-3.12705, -2.5856, -3.925, -22.380)},
    ("ct", 2): {0.01: (-4.32762, -15.4387, -35.679, 0.0), 0.05: (-3.78057, -9.5106, -12.074, 0.0),
                0.10: (-3.49631, -7.0815, -7.538, 21.892)},
    ("ct", 3): {0.01: (-4.66305, -18.7688, -49.793, 104.244), 0.05: (-4.11890, -11.8922, -19.031, 77.332),
                0.10: (-3.83511, -9.0723, -8.504, 35.403)},
    ("ct", 4): {0.01: (-4.96940, -22.4694, -52.599, 51.314), 0.05: (-4.42871, -14.5876, -18.228, 39.647),
                0.10: (-4.14633, -11.2500, -9.873, 54.109)},
    ("ct", 5): {0.01: (-5.25276, -26.2183, -59.631, 50.646), 0.05: (-4.71537, -17.3569, -22.660, 91.359),
                0.10: (-4.43422, -13.6078, -10.238, 76.781)},
}


def mackinnon_critical_value(case, nvars, level, nobs=None):
    """Lower-tail critical value for the residual t ratio with nvars = N series."""
    b = MACKINNON_2010[(case, nvars)][level]
    if nobs is None:
        return b[0]
    u = 1.0 / nobs
    return b[0] + b[1] * u + b[2] * u * u + b[3] * u * u * u


def ols(columns, y):
    """Least squares by modified Gram-Schmidt QR. Returns (coef, resid, se)."""
    n, k = len(y), len(columns)
    if n <= k:
        raise ValueError("need more observations than regressors")
    q, r = [], [[0.0] * k for _ in range(k)]
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
    rinv = [[0.0] * k for _ in range(k)]
    for c in range(k):
        for j in range(c, -1, -1):
            rhs = (1.0 if j == c else 0.0) - sum(r[j][l] * rinv[l][c] for l in range(j + 1, c + 1))
            rinv[j][c] = rhs / r[j][j]
    qty = [sum(a * float(b) for a, b in zip(qj, y)) for qj in q]
    coef = [sum(rinv[j][c] * qty[c] for c in range(j, k)) for j in range(k)]
    resid = [float(y[t]) - sum(coef[j] * float(columns[j][t]) for j in range(k)) for t in range(n)]
    s2 = sum(e * e for e in resid) / (n - k)
    se = [math.sqrt(s2 * sum(rinv[j][c] ** 2 for c in range(j, k))) for j in range(k)]
    return coef, resid, se


def _deterministic(n, case):
    if case == "c":
        return [[1.0] * n]
    if case == "ct":
        return [[1.0] * n, [float(t + 1) for t in range(n)]]
    raise ValueError("case must be 'c' or 'ct'")


def residual_adf(u, lags):
    """t ratio of rho in du_t = rho u_(t-1) + sum g_i du_(t-i) + e_t (no constant)."""
    n = len(u)
    du = [0.0] + [u[t] - u[t - 1] for t in range(1, n)]
    rows = range(lags + 1, n)
    cols = [[u[t - 1] for t in rows]] + [[du[t - i] for t in rows] for i in range(1, lags + 1)]
    coef, resid, se = ols(cols, [du[t] for t in rows])
    return coef[0] / se[0], len(rows), sum(e * e for e in resid), len(cols)


def select_lags(u, max_lag, criterion="aic"):
    """AIC or BIC choice of the number of lagged differences, on common rows."""
    n = len(u)
    du = [0.0] + [u[t] - u[t - 1] for t in range(1, n)]
    rows = range(max_lag + 1, n)
    best, best_ic = 0, math.inf
    for p in range(max_lag + 1):
        cols = [[u[t - 1] for t in rows]] + [[du[t - i] for t in rows] for i in range(1, p + 1)]
        _, resid, _ = ols(cols, [du[t] for t in rows])
        rss, m = sum(e * e for e in resid), len(rows)
        pen = 2.0 if criterion == "aic" else math.log(m)
        ic = m * math.log(rss / m) + pen * len(cols)
        if ic < best_ic - 1e-12:
            best, best_ic = p, ic
    return best


def engle_granger(y, xs, case="c", lags=0, max_lag=None, criterion="aic"):
    """The Engle-Granger test of no cointegration between y and the series in xs.

    xs is a list of m regressor series. lags is the number of lagged differences
    in step 2, or None to choose it by criterion up to max_lag (default
    floor(12 (n/100)^(1/4))). Returns tau, the step-1 coefficients (deterministic
    terms first), the residuals, nobs, the critical values and reject (5%)."""
    n = len(y)
    m = len(xs)
    if not 1 <= m <= 4:
        raise ValueError("between 1 and 4 regressors are supported")
    cols = _deterministic(n, case) + [[float(v) for v in x] for x in xs]
    beta, u, _ = ols(cols, y)  # @line L1
    du = [u[t] - u[t - 1] for t in range(1, n)]  # @line L2
    if lags is None:
        if max_lag is None:
            max_lag = int(12.0 * (n / 100.0) ** 0.25)
        lags = select_lags(u, max(0, min(max_lag, (n - 4) // 3)), criterion)
    tau, nobs, _, _ = residual_adf(u, lags)  # @line L3
    crit = {a: mackinnon_critical_value(case, m + 1, a, nobs) for a in (0.01, 0.05, 0.10)}  # @line L5
    return {"tau": tau, "beta": beta, "resid": u, "dresid": du, "nobs": nobs, "lags": lags,  # @line L4
            "critical": crit, "reject": tau < crit[0.05]}  # @line L6


def error_correction(y, x, u, lags=0):
    """Engle-Granger step two: regress dy_t on 1, u_(t-1), dx_t and lags of dy and dx.

    Returns the coefficients (constant, alpha on u_(t-1), dx_t, then the lags)
    and their standard errors. alpha < 0 is the speed of adjustment."""
    n = len(y)
    dy = [0.0] + [y[t] - y[t - 1] for t in range(1, n)]
    dx = [0.0] + [x[t] - x[t - 1] for t in range(1, n)]
    rows = range(lags + 1, n)
    cols = [[1.0] * len(rows), [u[t - 1] for t in rows], [dx[t] for t in rows]]
    for i in range(1, lags + 1):
        cols.append([dy[t - i] for t in rows])
        cols.append([dx[t - i] for t in rows])
    coef, _, se = ols(cols, [dy[t] for t in rows])
    return coef, se


def simulate_null(n, nvars=2, case="c", reps=1000, rng=None):
    """tau for reps sets of nvars independent Gaussian random walks of length n."""
    rng = rng or random.Random(0)
    out = []
    for _ in range(reps):
        walks = []
        for _ in range(nvars):
            s, w = 0.0, []
            for _ in range(n):
                s += rng.gauss(0.0, 1.0)
                w.append(s)
            walks.append(w)
        out.append(engle_granger(walks[0], walks[1:], case, 0)["tau"])
    return out
