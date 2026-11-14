# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kpss-test/. The authors are listed in prov/AWK28P.jsonl.
"""The KPSS test of the null of (level or trend) stationarity against a unit root.

Regress x_t on a constant (case "c") or on a constant and a trend (case "ct"),
form the partial sums S_t of the residuals, estimate the long-run variance
with Bartlett weights, and return

    eta = sum_t S_t^2 / (n^2 s^2(l)).

Large eta rejects stationarity. The arithmetic is generic: with Fraction
input every step except the bandwidth rule is exact.
The code is in this file and not in kpss_test.py, because tools treat a file
whose name ends in _test.py as a test file.
"""

import math
import random

# Kwiatkowski, Phillips, Schmidt and Shin (1992), Table 1 (upper tail).
KPSS_TABLE = {
    "c": {0.10: 0.347, 0.05: 0.463, 0.025: 0.574, 0.01: 0.739},
    "ct": {0.10: 0.119, 0.05: 0.146, 0.025: 0.176, 0.01: 0.216},
}


def detrend(x, case="c"):
    """Least squares residuals of x on 1 (case "c") or on 1 and t (case "ct")."""
    n = len(x)
    mean = sum(x) / n
    if case == "c":
        return [v - mean for v in x]
    if case != "ct":
        raise ValueError("case must be 'c' or 'ct'")
    tbar = (n + 1) / 2 if isinstance(mean, float) else type(mean)(n + 1, 2)
    tc = [t + 1 - tbar for t in range(n)]
    b = sum(c * v for c, v in zip(tc, x)) / sum(c * c for c in tc)
    return [v - mean - b * c for v, c in zip(x, tc)]


def bandwidth(n, rule="l4"):
    """The KPSS truncation lags: l4 = floor(4 (n/100)^(1/4)), l12 = floor(12 (n/100)^(1/4)),
    l0 = 0, or an integer given directly."""
    if isinstance(rule, int):
        return rule
    return {"l0": 0, "l4": int(4.0 * (n / 100.0) ** 0.25), "l12": int(12.0 * (n / 100.0) ** 0.25)}[rule]


def autocovariances(e, lags):
    """gamma_j = (1/n) sum_(t>j) e_t e_(t-j) for j = 0..lags."""
    n = len(e)
    return [sum(e[t] * e[t - j] for t in range(j, n)) / n for j in range(lags + 1)]


def bartlett(gam):
    """gamma_0 + 2 sum_(j=1..l) (1 - j/(l+1)) gamma_j, the Bartlett (Newey-West) weights."""
    lags = len(gam) - 1
    s2 = gam[0]
    for j in range(1, lags + 1):
        w = 1 - (j / (lags + 1) if isinstance(gam[0], float) else type(gam[0])(j, lags + 1))
        s2 = s2 + 2 * w * gam[j]
    return s2


def long_run_variance(e, lags):
    """The Bartlett estimate of the long-run variance of e with the given lags."""
    return bartlett(autocovariances(e, lags))


def kpss(x, case="c", lags="l4"):
    """The KPSS statistic eta, the lags used, and reject at 5% (eta > table value)."""
    n = len(x)
    if n < 3:
        raise ValueError("need at least 3 observations")
    ell = bandwidth(n, lags)
    if not 0 <= ell < n:
        raise ValueError("the number of lags must be in 0..n-1")
    e = detrend(x, case)  # @line L1
    s, ssum = 0, 0
    for v in e:  # @line L2
        s = s + v
        ssum = ssum + s * s
    gam = autocovariances(e, ell)  # @line L3
    s2 = bartlett(gam)  # @line L4
    if s2 == 0:
        raise ValueError("the residuals are all zero")
    eta = ssum / (n * n * s2)  # @line L5
    crit = KPSS_TABLE[case]  # @line L6
    return {"eta": eta, "lags": ell, "critical": crit, "reject": eta > crit[0.05],  # @line L7
            "p_value": table_p_value(float(eta), case)}


def table_p_value(eta, case="c"):
    """Linear interpolation in the KPSS table, clipped to [0.01, 0.10].
    A value of 0.10 means "0.10 or more" and 0.01 means "0.01 or less"."""
    pts = sorted(KPSS_TABLE[case].items(), key=lambda kv: kv[1])
    crit = [c for _, c in pts]
    lev = [a for a, _ in pts]
    if eta <= crit[0]:
        return lev[0]
    if eta >= crit[-1]:
        return lev[-1]
    for i in range(len(crit) - 1):
        if crit[i] <= eta <= crit[i + 1]:
            w = (eta - crit[i]) / (crit[i + 1] - crit[i])
            return lev[i] + w * (lev[i + 1] - lev[i])
    return lev[-1]


def simulate_null(n, case="c", lags=0, reps=1000, rng=None):
    """eta for reps iid N(0, 1) series of length n (the null, stationary)."""
    rng = rng or random.Random(0)
    return [kpss([rng.gauss(0.0, 1.0) for _ in range(n)], case, lags)["eta"] for _ in range(reps)]


def cvm_limit_sf(x, terms=200):
    """Asymptotic P(eta > x) in case "c": eta tends to sum_k Z_k^2 / (k^2 pi^2),
    the Cramer-von Mises limit. Computed by numerical inversion of the
    characteristic function (Imhof), truncated at terms and corrected for the
    mean of the tail. Accurate to about 1e-4."""
    lam = [1.0 / (k * k * math.pi * math.pi) for k in range(1, terms + 1)]
    x = x - (1.0 / 6.0 - sum(lam))

    def f(u):
        th = 0.5 * sum(math.atan(l * u) for l in lam) - 0.5 * x * u
        rho = math.exp(0.25 * sum(math.log1p((l * u) ** 2) for l in lam))
        return math.sin(th) / (u * rho)

    edges = [0.0] + [10 ** (k / 8.0) for k in range(-24, 41)]
    total = 0.0
    for lo, hi in zip(edges, edges[1:]):
        m = 24
        h = (hi - lo) / m
        acc = 0.0
        for i in range(m + 1):
            u = lo + i * h
            fu = 0.5 * (sum(lam) - x) if u == 0 else f(u)
            acc += fu * (1 if i in (0, m) else (4 if i % 2 else 2))
        total += acc * h / 3
    return 0.5 + total / math.pi
