# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binomial-test/. The authors are listed in prov/P6MXFM.jsonl.

import math

# Two outcomes whose probabilities differ by less than this relative amount
# count as equally likely in the two-sided rule. Exact ties (for example
# k and n - k when p0 = 1/2) can differ in the last bits after rounding.
RELATIVE_TOLERANCE = 1e-7


def binomial_pmf(n: int, p0: float) -> list[float]:
    """Return [P(X = k) for k = 0..n] for X ~ Binomial(n, p0).

    The terms are computed in log space with math.lgamma, so that neither
    the binomial coefficient nor the power of p0 overflows or underflows
    before the product is formed.
    """
    if p0 == 0.0:
        return [1.0] + [0.0] * n
    if p0 == 1.0:
        return [0.0] * n + [1.0]
    log_p, log_q = math.log(p0), math.log1p(-p0)
    log_n_fact = math.lgamma(n + 1)
    return [
        math.exp(
            log_n_fact
            - math.lgamma(k + 1)
            - math.lgamma(n - k + 1)
            + k * log_p
            + (n - k) * log_q
        )
        for k in range(n + 1)
    ]


def binomial_test(
    x: int,
    n: int,
    p0: float,
    alternative: str = "two-sided",
    rule: str = "minlike",
) -> float:
    """Exact p-value of the binomial test of H0: p = p0.

    x successes in n independent trials. alternative is "greater"
    (H1: p > p0), "less" (H1: p < p0) or "two-sided" (H1: p != p0).
    For the two-sided test, rule "minlike" sums the probabilities of the
    outcomes that are at most as likely as x (the default, as in R's
    binom.test), and rule "double" doubles the smaller one-sided p-value.
    """
    if not (isinstance(x, int) and isinstance(n, int)) or n < 0 or not 0 <= x <= n:
        raise ValueError("need integers with 0 <= x <= n")
    if not 0.0 <= p0 <= 1.0:
        raise ValueError("p0 must be in [0, 1]")
    if alternative not in ("two-sided", "greater", "less"):
        raise ValueError("unknown alternative")
    if rule not in ("minlike", "double"):
        raise ValueError("unknown two-sided rule")
    w = binomial_pmf(n, p0)  # @line L1
    upper = math.fsum(w[x:])  # @line L2
    lower = math.fsum(w[: x + 1])  # @line L3
    if alternative == "greater":  # @line L4
        return min(1.0, upper)
    if alternative == "less":  # @line L5
        return min(1.0, lower)
    if rule == "double":
        return min(1.0, 2.0 * min(lower, upper))
    t = w[x] * (1.0 + RELATIVE_TOLERANCE)  # @line L6
    p = math.fsum(v for v in w if v <= t)  # @line L7
    return min(1.0, p)  # @line L8
