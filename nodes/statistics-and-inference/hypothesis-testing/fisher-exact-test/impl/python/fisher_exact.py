# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-exact-test/. The authors are listed in prov/PNP35A.jsonl.

import math
from fractions import Fraction


def hypergeometric_weights(r1: int, r2: int, c1: int) -> tuple[int, list[int]]:
    """Return (lo, w) with w[i] = C(r1, lo + i) * C(r2, c1 - lo - i) as exact integers.

    w[i] is the number of ways to choose the c1 items of the first column so
    that lo + i of them fall in the first row. The list covers every possible
    value of the top-left cell, from lo = max(0, c1 - r2) to min(r1, c1). Each
    term comes from the one before by the ratio of consecutive binomial
    coefficients, and the integer division is exact.
    """
    lo, hi = max(0, c1 - r2), min(r1, c1)
    w = [math.comb(r1, lo) * math.comb(r2, c1 - lo)]  # @line L2
    for k in range(lo, hi):  # @line L3
        w.append(w[-1] * (r1 - k) * (c1 - k) // ((k + 1) * (r2 - c1 + k + 1)))  # @line L4
    return lo, w


def fisher_exact(
    a: int,
    b: int,
    c: int,
    d: int,
    alternative: str = "two-sided",
    exact: bool = False,
) -> float | Fraction:
    """P-value of Fisher's exact test for the 2 x 2 table [[a, b], [c, d]].

    Under the null hypothesis of independence (or equal proportions in the
    two rows), the top-left cell has the hypergeometric law given the row and
    column totals. alternative is "greater" (odds ratio > 1, large a), "less"
    (odds ratio < 1, small a) or "two-sided", which sums the probabilities of
    the tables that are at most as likely as the observed one. The weights are
    exact integers, so the two-sided comparison needs no tolerance. With
    exact=True the result is a Fraction; otherwise it is the correctly rounded
    float of that Fraction.
    """
    for v in (a, b, c, d):
        if not isinstance(v, int) or v < 0:
            raise ValueError("table entries must be non-negative integers")
    if alternative not in ("two-sided", "greater", "less"):
        raise ValueError("unknown alternative")
    r1, r2, c1 = a + b, c + d, a + c  # @line L1
    lo, w = hypergeometric_weights(r1, r2, c1)
    total = sum(w)  # @line L5
    i = a - lo
    if alternative == "greater":  # @line L6
        num = sum(w[i:])
    elif alternative == "less":  # @line L7
        num = sum(w[: i + 1])
    else:
        num = sum(v for v in w if v <= w[i])  # @line L8
    return Fraction(num, total) if exact else num / total
