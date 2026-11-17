# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ricker-model/. The authors are listed in prov/ZBTGC3.jsonl.
"""The Ricker model N_(t+1) = N_t exp(r (1 - N_t / K)).

orbit gives the trajectory. The other functions convert between the
growth form (r, K) and the stock-recruitment form R = a S exp(-b S), find
the 2-cycle u = 1 -/+ d of the scaled map u -> u exp(r (1 - u)), the value
of r where the 2-cycle loses stability, the period of the attractor, the
Lyapunov exponent, and the least-squares fit of ln(R / S) = ln a - b S.
Cost: Theta(T) operations for T steps.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple


def step(r: float, u: float, K: float = 1.0) -> float:
    """One generation of the model."""
    return u * math.exp(r * (1 - u / K))


def orbit(r: float, n0: float, steps: int, K: float = 1.0) -> List[float]:
    """The values N_1, ..., N_steps from the start n0."""
    if steps < 0 or K <= 0:
        raise ValueError("need steps >= 0 and K > 0")
    n = n0  # @line L1
    out: List[float] = []
    for _ in range(steps):  # @line L2
        n = n * math.exp(r * (1 - n / K))  # @line L3
        out.append(n)  # @line L4
    return out  # @line L5


def to_stock_recruitment(r: float, K: float) -> Tuple[float, float]:
    """(a, b) with a S exp(-b S) = S exp(r (1 - S / K))."""
    return math.exp(r), r / K


def from_stock_recruitment(a: float, b: float) -> Tuple[float, float]:
    """(r, K) for R = a S exp(-b S), with a > 1 and b > 0."""
    if a <= 1 or b <= 0:
        raise ValueError("need a > 1 and b > 0")
    r = math.log(a)
    return r, r / b


def multiplier(r: float, cycle: Sequence[float]) -> float:
    """The product of f'(u) = exp(r (1 - u)) (1 - r u) over a cycle of the scaled map."""
    m = 1.0
    for u in cycle:
        m *= math.exp(r * (1 - u)) * (1 - r * u)
    return m


def two_cycle(r: float) -> Optional[Tuple[float, float]]:
    """The 2-cycle (1 - d, 1 + d), where ln((1 + d) / (1 - d)) = r d, or None for r <= 2."""
    if r <= 2:
        return None
    g = lambda d: math.log((1 + d) / (1 - d)) - r * d
    lo, hi = 1e-12, 1 - 1e-15
    for _ in range(200):
        mid = (lo + hi) / 2
        if g(mid) < 0:
            lo = mid
        else:
            hi = mid
    d = (lo + hi) / 2
    return 1 - d, 1 + d


def two_cycle_limit() -> float:
    """The r > 2 where the multiplier (1 - r)^2 - r^2 d^2 of the 2-cycle is -1."""
    lo, hi = 2.1, 3.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if multiplier(mid, two_cycle(mid)) > -1:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def attractor(r: float, u0: float = 0.3, burn: int = 100000,
              max_period: int = 64, tol: float = 1e-9) -> Optional[List[float]]:
    """The sorted cycle the scaled orbit settles on, or None if no period <= max_period."""
    u = u0
    for _ in range(burn):
        u = step(r, u)
    path = [u]
    for _ in range(max_period):
        u = step(r, u)
        path.append(u)
    for p in range(1, max_period + 1):
        if abs(path[p] - path[0]) < tol:
            return sorted(path[:p])
    return None


def lyapunov(r: float, u0: float = 0.3, steps: int = 100000, burn: int = 1000) -> float:
    """The mean of log |f'(u_t)| along the scaled orbit."""
    u = u0
    for _ in range(burn):
        u = step(r, u)
    total = 0.0
    for _ in range(steps):
        total += math.log(abs(math.exp(r * (1 - u)) * (1 - r * u)))
        u = step(r, u)
    return total / steps


def fit_stock_recruitment(stock: Sequence[float], recruits: Sequence[float]) -> Tuple[float, float]:
    """Least squares of ln(R / S) on S. Returns (a, b) of R = a S exp(-b S)."""
    if len(stock) != len(recruits) or len(stock) < 2:
        raise ValueError("need two or more pairs")
    ys = [math.log(rr / s) for s, rr in zip(stock, recruits)]
    n = len(stock)
    mx = sum(stock) / n
    my = sum(ys) / n
    sxx = sum((s - mx) ** 2 for s in stock)
    if sxx == 0:
        raise ValueError("the stock values must not all be equal")
    slope = sum((s - mx) * (y - my) for s, y in zip(stock, ys)) / sxx
    return math.exp(my - slope * mx), -slope
