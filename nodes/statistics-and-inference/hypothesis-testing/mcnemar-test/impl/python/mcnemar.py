# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcnemar-test/. The authors are listed in prov/H919BT.jsonl.

from fractions import Fraction

from stdist import chi2_sf


def mcnemar_statistic(b: int, c: int, corrected: bool = False) -> float:
    """McNemar's statistic (b - c)^2 / (b + c), or Edwards's corrected
    (|b - c| - 1)^2 / (b + c) with the difference floored at 0.

    b and c are the two discordant counts of a paired 2 x 2 table: pairs
    with (yes, no) and pairs with (no, yes). Returns 0 when b + c = 0.
    """
    m = b + c
    if m == 0:
        return 0.0
    diff = abs(b - c)
    if corrected:
        diff = max(0, diff - 1)
    return diff * diff / m


def mcnemar_test(b: int, c: int, method: str = "exact", exact: bool = False) -> float | Fraction:
    """Two-sided p-value of McNemar's test of marginal homogeneity.

    method "exact": given m = b + c discordant pairs, b ~ Binomial(m, 1/2)
    under the null, and the p-value is twice the smaller binomial tail, from
    exact integer sums (with exact=True it is returned as a Fraction).
    method "asymptotic": the chi-square tail with 1 degree of freedom of
    (b - c)^2 / (b + c). method "corrected": the same with Edwards's
    continuity correction. The concordant counts do not enter the test.
    """
    if not (isinstance(b, int) and isinstance(c, int)) or b < 0 or c < 0:
        raise ValueError("b and c must be non-negative integers")
    if method not in ("exact", "asymptotic", "corrected"):
        raise ValueError("unknown method")
    m = b + c  # @line L1
    if m == 0:
        return Fraction(1) if exact else 1.0
    if method == "exact":  # @line L2
        s, term = 0, 1  # term = C(m, k), updated by C(m, k + 1) = C(m, k) (m - k) / (k + 1)
        for k in range(min(b, c) + 1):  # @line L3
            s += term
            term = term * (m - k) // (k + 1)
        p = min(Fraction(1), Fraction(2 * s, 2**m))  # @line L4
        return p if exact else float(p)
    x2 = mcnemar_statistic(b, c, corrected=(method == "corrected"))  # @line L5
    return chi2_sf(x2, 1)  # @line L6
