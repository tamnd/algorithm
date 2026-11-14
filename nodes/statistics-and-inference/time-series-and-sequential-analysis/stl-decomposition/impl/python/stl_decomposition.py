# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stl-decomposition/. The authors are listed in prov/GHRJ1G.jsonl.
"""STL: seasonal-trend decomposition by LOESS (Cleveland, Cleveland, McRae and
Terpenning 1990).

Y_t = T_t + S_t + R_t. The inner loop alternates a seasonal smoother (LOESS on
each cycle-subseries, then removal of its low-frequency part) and a trend
smoother (LOESS on the deseasonalized series). The outer loop computes
bisquare robustness weights from the remainder and repeats the inner loop
with them. All arithmetic is generic: Fraction input gives Fraction output.
"""


def tricube(u):
    return (1 - u * u * u) ** 3 if u < 1 else 0 * u


def bisquare(u):
    return (1 - u * u) ** 2 if u < 1 else 0 * u


def loess_at(y, x, q, degree=1, rob=None):
    """LOESS fit at position x (a number, maybe outside 1..n) of y at positions 1..n.

    Uses the q nearest positions (all n if q > n, with the bandwidth stretched
    by q/n), tricube weights times the robustness weights rob, and a weighted
    least squares fit of a line (degree 1) or a constant (degree 0)."""
    n = len(y)
    one = y[0] * 0 + 1
    if q >= n:
        lo, hi = 1, n
    else:
        lo = min(max(1, int(x) - (q - 1) // 2), n - q + 1)
        if x < 1:
            lo = 1
        # slide the window so that it holds the q positions nearest to x
        while lo + q <= n and abs(lo + q - x) < abs(x - lo):
            lo += 1
        while lo > 1 and abs(x - (lo - 1)) < abs(lo + q - 1 - x):
            lo -= 1
        hi = lo + q - 1
    lam = max(abs(x - lo), abs(hi - x)) * one
    if q > n:
        lam = lam * q / n
    w = []
    for i in range(lo, hi + 1):
        wi = tricube(abs(i - x) * one / lam) if lam > 0 else one
        if rob is not None:
            wi = wi * rob[i - 1]
        w.append(wi)
    sw = sum(w)
    if sw <= 0:
        return None
    idx = list(range(lo, hi + 1))
    xbar = sum(wi * i for wi, i in zip(w, idx)) / sw
    ybar = sum(wi * y[i - 1] for wi, i in zip(w, idx)) / sw
    if degree == 0:
        return ybar
    sxx = sum(wi * (i - xbar) ** 2 for wi, i in zip(w, idx))
    if sxx <= 0:
        return ybar
    sxy = sum(wi * (i - xbar) * y[i - 1] for wi, i in zip(w, idx))
    return ybar + sxy / sxx * (x - xbar)


def loess(y, q, degree=1, rob=None, extend=False):
    """LOESS at positions 1..n, or 0..n+1 when extend is True."""
    n = len(y)
    xs = range(0, n + 2) if extend else range(1, n + 1)
    out = []
    for x in xs:
        v = loess_at(y, x, q, degree, rob)
        if v is None:  # all weights zero: keep the nearest observation
            v = y[min(max(x, 1), n) - 1]
        out.append(v)
    return out


def moving_average(y, k):
    """Means of each run of k consecutive values; length len(y) - k + 1."""
    return [sum(y[i:i + k]) / k for i in range(len(y) - k + 1)]


def next_odd(v):
    """The smallest odd integer >= v."""
    k = int(v)
    if k < v:
        k += 1
    return k if k % 2 == 1 else k + 1


def default_spans(period, seasonal):
    """Cleveland's defaults: n_l = next odd >= period; n_t = next odd >= 1.5 period / (1 - 1.5 / n_s)."""
    return next_odd(period), next_odd(1.5 * period / (1.0 - 1.5 / seasonal))


def inner_loop(y, period, n_s, n_l, n_t, trend, rob, degrees=(1, 1, 1)):
    """One pass of the inner loop. Returns (seasonal, trend)."""
    n = len(y)
    detr = [a - b for a, b in zip(y, trend)]  # @line L3
    c = [None] * (n + 2 * period)
    for j in range(period):  # cycle-subseries smoothing
        pos = list(range(j, n, period))
        sub = [detr[t] for t in pos]
        rsub = [rob[t] for t in pos] if rob is not None else None
        sm = loess(sub, n_s, degrees[0], rsub, extend=True)  # @line L4
        for k, v in enumerate(sm):  # k = 0 is one period before pos[0]
            c[j + k * period] = v
    low = moving_average(moving_average(moving_average(c, period), period), 3)  # @line L5
    low = loess(low, n_l, degrees[1])
    seasonal = [c[t + period] - low[t] for t in range(n)]  # @line L6
    deseason = [a - b for a, b in zip(y, seasonal)]  # @line L7
    trend = loess(deseason, n_t, degrees[2], rob)  # @line L8
    return seasonal, trend


def robustness_weights(resid):
    """Bisquare weights B(|R_t| / h) with h = 6 median |R_t|."""
    a = sorted(abs(r) for r in resid)
    n = len(a)
    med = a[n // 2] if n % 2 else (a[n // 2 - 1] + a[n // 2]) / 2
    h = 6 * med
    if h == 0:
        return [1 if r == 0 else 0 for r in resid]
    return [bisquare(abs(r) / h) for r in resid]


def stl(y, period, seasonal=7, trend=None, low_pass=None, inner=None, outer=0, degrees=(1, 1, 1)):
    """Decompose y into (seasonal, trend, remainder, weights).

    seasonal is the cycle-subseries span n_s (odd, >= 7 recommended). trend and
    low_pass default to Cleveland's rules. inner defaults to 2 without and 1
    with robustness iterations; outer is the number of robustness passes."""
    n = len(y)
    if period < 2 or n < 2 * period:
        raise ValueError("need a period >= 2 and at least two full periods")
    if seasonal < 3 or seasonal % 2 == 0:
        raise ValueError("the seasonal span must be odd and at least 3")
    d_l, d_t = default_spans(period, seasonal)
    n_l = low_pass or d_l
    n_t = trend or d_t
    if inner is None:
        inner = 1 if outer > 0 else 2
    zero = y[0] * 0
    tr = [zero] * n  # @line L1
    rob = None
    for o in range(outer + 1):
        for _ in range(inner):  # @line L2
            seas, tr = inner_loop(y, period, seasonal, n_l, n_t, tr, rob, degrees)
        resid = [a - b - c for a, b, c in zip(y, seas, tr)]  # @line L9
        if o < outer:
            rob = robustness_weights(resid)  # @line L10
    weights = rob if rob is not None else [zero + 1] * n
    return {"seasonal": seas, "trend": tr, "remainder": resid, "weights": weights,  # @line L11
            "spans": {"seasonal": seasonal, "trend": n_t, "low_pass": n_l}}
