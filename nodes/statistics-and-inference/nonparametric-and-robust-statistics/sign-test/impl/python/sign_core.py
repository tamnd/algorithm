# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sign-test/. The authors are listed in prov/R4JDYX.jsonl.

import math
from fractions import Fraction

ALTERNATIVES = ("two-sided", "greater", "less")


def sign_counts(d: list[float], mu0: float = 0.0) -> tuple[int, int]:
    """Return (s, n): the number of d_i - mu0 > 0 and the number of nonzero d_i - mu0."""
    kept = [v - mu0 for v in d if v != mu0]
    return sum(1 for v in kept if v > 0), len(kept)


def sign_test(
    d: list[float], alternative: str = "two-sided", mu0: float = 0.0, exact: bool = False
) -> float | Fraction:
    """Exact p-value of the sign test of H0: P(D > mu0) = P(D < mu0).

    d holds the paired differences, or the sample itself for a test of the
    median mu0. Values equal to mu0 are dropped. "greater" is the alternative
    P(D > mu0) > 1/2, "less" the alternative P(D > mu0) < 1/2. The two-sided
    p-value doubles the smaller tail, which is the same as the rule that sums
    all outcomes at most as likely as the observed one, because the null law
    Binomial(n, 1/2) is symmetric. The tails are exact integer sums divided by
    2^n; exact=True returns the Fraction, otherwise the correctly rounded float.
    """
    if alternative not in ALTERNATIVES:
        raise ValueError("unknown alternative")
    kept = [v - mu0 for v in d if v != mu0]  # @line L1
    s, n = sum(1 for v in kept if v > 0), len(kept)  # @line L2
    w = [1] * (n + 1)  # @line L3
    for k in range(n):
        w[k + 1] = w[k] * (n - k) // (k + 1)  # w[k] = C(n, k), exact integers
    upper, lower = sum(w[s:]), sum(w[: s + 1])  # @line L4
    total = 2**n
    if alternative == "greater":  # @line L5
        p = Fraction(upper, total)
    elif alternative == "less":  # @line L6
        p = Fraction(lower, total)
    else:
        p = min(Fraction(1), Fraction(2 * min(upper, lower), total))  # @line L7
    return p if exact else float(p)


def sign_test_normal(
    d: list[float], alternative: str = "two-sided", mu0: float = 0.0, correction: bool = True
) -> float:
    """Normal approximation to the sign test, with an optional continuity correction of 1/2."""
    if alternative not in ALTERNATIVES:
        raise ValueError("unknown alternative")
    s, n = sign_counts(d, mu0)
    if n == 0:
        return 1.0
    c = 0.5 if correction else 0.0
    sd = math.sqrt(n) / 2.0
    if alternative == "greater":
        z = (s - n / 2.0 - c) / sd
        return 0.5 * math.erfc(z / math.sqrt(2.0))
    if alternative == "less":
        z = (s - n / 2.0 + c) / sd
        return 0.5 * math.erfc(-z / math.sqrt(2.0))
    z = max(0.0, abs(s - n / 2.0) - c) / sd
    return min(1.0, math.erfc(z / math.sqrt(2.0)))


def median_interval(x: list[float], alpha: float) -> tuple[float, float, Fraction]:
    """Distribution-free interval [x_(k), x_(n+1-k)] for the median, from the sign test.

    k is the largest index with 2 P(Binomial(n, 1/2) <= k - 1) <= alpha. Returns
    the two ends and the exact coverage 1 - 2 P(Binomial(n, 1/2) <= k - 1) for a
    continuous distribution. Raises ValueError if n is too small for alpha.
    """
    n = len(x)
    xs = sorted(x)
    k, tail = 0, 0
    while 2 * (tail + math.comb(n, k)) <= alpha * 2**n:
        tail += math.comb(n, k)
        k += 1
    if k == 0:
        raise ValueError("n is too small for this alpha")
    return xs[k - 1], xs[n - k], 1 - Fraction(2 * tail, 2**n)
