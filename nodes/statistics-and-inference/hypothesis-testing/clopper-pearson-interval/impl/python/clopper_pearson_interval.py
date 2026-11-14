# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clopper-pearson-interval/. The authors are listed in prov/X4CPDK.jsonl.

import math


def binomial_upper_tail(x: int, n: int, p: float) -> float:
    """P_p(X >= x) for X ~ Binomial(n, p), summed directly in log space."""
    if x <= 0:
        return 1.0
    if x > n:
        return 0.0
    if p <= 0.0:
        return 0.0
    if p >= 1.0:
        return 1.0
    log_p, log_q, log_n_fact = math.log(p), math.log1p(-p), math.lgamma(n + 1)
    return math.fsum(
        math.exp(log_n_fact - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * log_p + (n - k) * log_q)
        for k in range(x, n + 1)
    )


def binomial_lower_tail(x: int, n: int, p: float) -> float:
    """P_p(X <= x), from the upper tail of the failures: X <= x iff n - X >= n - x."""
    return binomial_upper_tail(n - x, n, 1.0 - p)


def _solve_increasing(f, target: float) -> float:
    """The root in [0, 1] of f(p) = target for a continuous increasing f, by bisection."""
    lo, hi = 0.0, 1.0
    while True:
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            return mid
        if f(mid) < target:
            lo = mid
        else:
            hi = mid


def clopper_pearson_interval(x: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """The Clopper-Pearson interval [L, U] for a binomial p at level 1 - alpha.

    L solves P_L(X >= x) = alpha/2 (L = 0 when x = 0), and U solves
    P_U(X <= x) = alpha/2 (U = 1 when x = n). Equivalently, L is the alpha/2
    quantile of Beta(x, n - x + 1) and U is the 1 - alpha/2 quantile of
    Beta(x + 1, n - x). Each endpoint is found by bisection to the last bit.
    """
    if not (isinstance(x, int) and isinstance(n, int)) or n < 1 or not 0 <= x <= n:
        raise ValueError("need integers with 0 <= x <= n and n >= 1")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0, 1)")
    if x == 0:  # @line L1
        lower = 0.0
    else:  # @line L2
        lower = _solve_increasing(lambda p: binomial_upper_tail(x, n, p), alpha / 2)
    if x == n:  # @line L3
        upper = 1.0
    else:  # @line L4
        upper = _solve_increasing(lambda p: -binomial_lower_tail(x, n, p), -alpha / 2)
    return lower, upper  # @line L5
