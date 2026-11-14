# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alpha-spending-function/. The authors are listed in prov/9MKH4V.jsonl.
"""Lan-DeMets alpha spending: two-sided group sequential boundaries from a spending function.

A spending function f maps the information fraction t in [0, 1] to the type I
error spent so far, with f(0) = 0, f(1) = alpha, and f nondecreasing. At
analysis k, with information fraction t_k, the boundary c_k solves

    P0(|Z_j| < c_j for j < k, |Z_k| >= c_k) = f(t_k) - f(t_(k-1)).

Z_k is the standardized statistic. The score S_k = Z_k sqrt(t_k) is a standard
Brownian motion at the times t_1 < ... < t_K. The sub-density of S_k on the
continuation event is carried on a Simpson grid (recursive numerical
integration), and c_k is found by bisection. Cost O(K (m^2 + b m)) for m grid
points per stage and b bisection steps.
"""

import math
from collections.abc import Callable, Sequence

_SQRT2 = math.sqrt(2.0)
_INV_SQRT_2PI = 1.0 / math.sqrt(2.0 * math.pi)


def norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / _SQRT2)


def norm_sf(x: float) -> float:
    return 0.5 * math.erfc(x / _SQRT2)


def norm_pdf(x: float) -> float:
    return _INV_SQRT_2PI * math.exp(-0.5 * x * x)


def norm_quantile(p: float) -> float:
    """The lower p-quantile of the standard normal, by bisection to 1e-15."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-15:
            break
    return 0.5 * (lo + hi)


def obf_spending(alpha: float) -> Callable[[float], float]:
    """Lan-DeMets O'Brien-Fleming type: f(t) = 2 - 2 Phi(z_(1 - alpha/2) / sqrt(t))."""
    zq = norm_quantile(1.0 - alpha / 2.0)
    return lambda t: 0.0 if t <= 0.0 else 2.0 * norm_sf(zq / math.sqrt(t))


def pocock_spending(alpha: float) -> Callable[[float], float]:
    """Lan-DeMets Pocock type: f(t) = alpha log(1 + (e - 1) t)."""
    return lambda t: alpha * math.log(1.0 + (math.e - 1.0) * t)


def power_spending(alpha: float, rho: float) -> Callable[[float], float]:
    """Kim-DeMets power family: f(t) = alpha t^rho, rho > 0."""
    if rho <= 0:
        raise ValueError("rho must be positive")
    return lambda t: alpha * t ** rho


def hsd_spending(alpha: float, gamma: float) -> Callable[[float], float]:
    """Hwang-Shih-DeCani family: f(t) = alpha (1 - e^(-gamma t)) / (1 - e^(-gamma)); gamma = 0 is linear."""
    if gamma == 0:
        return lambda t: alpha * t
    return lambda t: alpha * (1.0 - math.exp(-gamma * t)) / (1.0 - math.exp(-gamma))


def _simpson_grid(b: float, step: float) -> tuple[list[float], list[float]]:
    n = max(2, 2 * math.ceil(b / step))
    h = 2.0 * b / n
    xs = [-b + i * h for i in range(n + 1)]
    ws = [(1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)) * h / 3.0 for i in range(n + 1)]
    return xs, ws


def spending_boundaries(spend: Callable[[float], float], times: Sequence[float], r: int = 16,
                        tol: float = 1e-10) -> list[float]:
    """The z-scale two-sided boundaries c_1, ..., c_K for the spending function spend.

    Precondition: 0 < times[0] < ... < times[-1] <= 1, and spend increases
    strictly on the times. A zero increment would need c_k = +inf, so it is rejected.
    """
    if not times or any(b <= a for a, b in zip(times, times[1:])) or times[0] <= 0:
        raise ValueError("times must be positive and increasing")
    out = []
    t0 = times[0]
    inc = spend(t0)
    if inc <= 0:
        raise ValueError("each stage must spend a positive amount")
    c = norm_quantile(1.0 - inc / 2.0)  # @line L1
    out.append(c)
    b = c * math.sqrt(t0)
    xs, ws = _simpson_grid(b, math.sqrt(t0) / r)
    g = [norm_pdf(x / math.sqrt(t0)) / math.sqrt(t0) for x in xs]  # @line L1
    for k in range(1, len(times)):  # @line L2
        target = spend(times[k]) - spend(times[k - 1])  # @line L3
        if target <= 0:
            raise ValueError("each stage must spend a positive amount")
        sd = math.sqrt(times[k] - times[k - 1])
        wg = [w * gu for w, gu in zip(ws, g)]
        st = math.sqrt(times[k])

        def cross(ck: float) -> float:
            bk = ck * st
            return sum(a * (norm_sf((bk - u) / sd) + norm_cdf((-bk - u) / sd)) for u, a in zip(xs, wg))

        lo, hi = 0.0, 40.0
        if cross(lo) < target:
            raise ValueError("the spending increment is larger than the mass that is still in play")
        while hi - lo > tol:  # @line L4
            mid = 0.5 * (lo + hi)
            if cross(mid) > target:
                lo = mid
            else:
                hi = mid
        c = 0.5 * (lo + hi)  # @line L4
        out.append(c)
        if k + 1 < len(times):
            b = c * st
            step = min(sd, math.sqrt(times[k + 1] - times[k])) / r
            nxs, nws = _simpson_grid(b, step)
            g = [sum(a * norm_pdf((s - u) / sd) for u, a in zip(xs, wg)) / sd for s in nxs]  # @line L5
            xs, ws = nxs, nws
    return out  # @line L6


def crossing_by_stage(c: Sequence[float], times: Sequence[float], r: int = 16) -> list[float]:
    """P0 of the first crossing at each analysis, for given z-scale boundaries c."""
    out = []
    t0 = times[0]
    out.append(2.0 * norm_sf(c[0]))
    b = c[0] * math.sqrt(t0)
    xs, ws = _simpson_grid(b, math.sqrt(t0) / r)
    g = [norm_pdf(x / math.sqrt(t0)) / math.sqrt(t0) for x in xs]
    for k in range(1, len(times)):
        sd = math.sqrt(times[k] - times[k - 1])
        bk = c[k] * math.sqrt(times[k])
        wg = [w * gu for w, gu in zip(ws, g)]
        out.append(sum(a * (norm_sf((bk - u) / sd) + norm_cdf((-bk - u) / sd)) for u, a in zip(xs, wg)))
        if k + 1 < len(times):
            step = min(sd, math.sqrt(times[k + 1] - times[k])) / r
            nxs, nws = _simpson_grid(bk, step)
            g = [sum(a * norm_pdf((s - u) / sd) for u, a in zip(xs, wg)) / sd for s in nxs]
            xs, ws = nxs, nws
    return out
