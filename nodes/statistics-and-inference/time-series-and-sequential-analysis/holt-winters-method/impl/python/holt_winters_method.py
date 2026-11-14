# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/holt-winters-method/. The authors are listed in prov/56FTG8.jsonl.
"""Holt's linear method and the Holt-Winters seasonal method.

Component form (Hyndman and Athanasopoulos), additive seasonality, period m:

    forecast  yhat_t = l_(t-1) + b_(t-1) + s_(t-m)
    level     l_t = alpha (y_t - s_(t-m)) + (1 - alpha)(l_(t-1) + b_(t-1))
    trend     b_t = beta (l_t - l_(t-1)) + (1 - beta) b_(t-1)
    season    s_t = gamma (y_t - l_(t-1) - b_(t-1)) + (1 - gamma) s_(t-m)

Multiplicative seasonality divides by the seasonal index instead of
subtracting it. With seasonal=None it is Holt's linear method. All the
arithmetic is generic, so Fractions in give Fractions out.
"""

import math


def initial_states(y, m=None, seasonal=None):
    """Classical start values.

    Holt: l_0 = y_1, b_0 = y_2 - y_1. Seasonal: l_0 is the mean of the first
    season, b_0 is the difference of the first two season means divided by m,
    and s is the first season minus (or divided by) l_0."""
    if seasonal is None:
        if len(y) < 2:
            raise ValueError("need at least 2 observations")
        return y[0], y[1] - y[0], []
    if m is None or m < 2 or len(y) < 2 * m:
        raise ValueError("need a period m >= 2 and at least two full seasons")
    first = sum(y[:m]) / m
    second = sum(y[m:2 * m]) / m
    level, trend = first, (second - first) / m
    if seasonal == "add":
        season = [y[i] - level for i in range(m)]
    elif seasonal == "mul":
        season = [y[i] / level for i in range(m)]
    else:
        raise ValueError("seasonal must be None, 'add' or 'mul'")
    return level, trend, season


def holt_winters(y, alpha, beta, gamma=0, m=None, seasonal=None, h=0, init=None):
    """Run the smoothing recursions and forecast h steps ahead.

    Returns a dict with the one-step forecasts and errors for t = 1..n, the
    final level, trend and seasonal states, the h forecasts and the sum of
    squared one-step errors. init = (l_0, b_0, s_(1-m..0)) overrides the
    classical start; the default classical start uses the data from t = 1."""
    if seasonal is not None and seasonal not in ("add", "mul"):
        raise ValueError("seasonal must be None, 'add' or 'mul'")
    level, trend, season = init if init is not None else initial_states(y, m, seasonal)
    season = list(season)
    period = len(season)
    fitted, errors = [], []
    for t, obs in enumerate(y):
        s = season[t % period] if period else None
        if seasonal == "add":
            yhat = level + trend + s  # @line L1
        elif seasonal == "mul":
            yhat = (level + trend) * s
        else:
            yhat = level + trend
        e = obs - yhat  # @line L2
        if seasonal == "add":
            new_level = alpha * (obs - s) + (1 - alpha) * (level + trend)  # @line L3
            season[t % period] = gamma * (obs - level - trend) + (1 - gamma) * s  # @line L5
        elif seasonal == "mul":
            new_level = alpha * (obs / s) + (1 - alpha) * (level + trend)
            season[t % period] = gamma * (obs / (level + trend)) + (1 - gamma) * s
        else:
            new_level = alpha * obs + (1 - alpha) * (level + trend)
        trend = beta * (new_level - level) + (1 - beta) * trend  # @line L4
        level = new_level
        fitted.append(yhat)
        errors.append(e)
    n = len(y)
    forecasts = []
    for k in range(1, h + 1):
        base = level + k * trend
        if seasonal == "add":
            base = base + season[(n + k - 1) % period]  # @line L6
        elif seasonal == "mul":
            base = base * season[(n + k - 1) % period]
        forecasts.append(base)
    sse = sum(e * e for e in errors)
    return {"fitted": fitted, "errors": errors, "level": level, "trend": trend,  # @line L7
            "season": season, "forecasts": forecasts, "sse": sse}


def fit(y, m=None, seasonal=None, grid=None):
    """Choose alpha, beta (and gamma) by the smallest sum of squared one-step
    errors over a grid, then refine by a finer grid around the best point.
    Returns (alpha, beta, gamma, sse)."""
    grid = grid or [i / 10 for i in range(1, 10)]
    gammas = grid if seasonal else [0.0]
    best = (math.inf, None)

    def search(alphas, betas, gs):
        nonlocal best
        for a in alphas:
            for b in betas:
                for g in gs:
                    if seasonal and not 0 <= g <= 1 - a:
                        continue
                    sse = holt_winters([float(v) for v in y], a, b, g, m, seasonal)["sse"]
                    if sse < best[0]:
                        best = (sse, (a, b, g))

    search(grid, grid, gammas)
    a0, b0, g0 = best[1]
    near = lambda c: [x for x in (c - 0.04, c - 0.02, c, c + 0.02, c + 0.04) if 0.0 < x < 1.0]
    search(near(a0), near(b0), near(g0) if seasonal else [0.0])
    a, b, g = best[1]
    return a, b, g, best[0]


def arima022_forecasts(y, theta1, theta2, f0, e0):
    """One-step forecasts of ARIMA(0, 2, 2) from its innovations recursion.

    f_t = 2 y_t - y_(t-1) + theta1 e_t + theta2 e_(t-1), started from the
    forecast f0 of y_2 made at t = 1 and the innovation e0 at t = 1."""
    fc, prev_e, e_t = [f0], e0, None
    for t in range(1, len(y) - 1):
        e_t = y[t] - fc[-1]
        fc.append(2 * y[t] - y[t - 1] + theta1 * e_t + theta2 * prev_e)
        prev_e = e_t
    return fc
