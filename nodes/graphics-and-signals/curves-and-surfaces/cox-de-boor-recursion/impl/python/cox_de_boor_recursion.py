# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cox-de-boor-recursion/. The authors are listed in prov/GGMD1V.jsonl.

"""The Cox-de Boor recursion for B-spline basis functions.

A knot vector is a non-decreasing list u_0, ..., u_m. With degree p there are
n + 1 = m - p basis functions N_{0,p}, ..., N_{n,p}. Knots and parameters may
be int or Fraction; with Fraction every result is exact.

basis_functions is the triangular scheme of the page: it raises the degree one
step at a time on one knot span and returns the p + 1 values that can be
nonzero there, in O(p^2) arithmetic operations. cox_de_boor is the recursion
as written, with the rule 0/0 = 0; it makes about 2^(p+1) calls and serves as
a definition to test against.
"""

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]


def find_span(knots: Sequence[Number], p: int, u: Number) -> int:
    """Return mu with p <= mu <= n and u_mu <= u < u_(mu+1).

    At the right end u = u_(n+1), return the last nonempty span mu <= n, so
    that the basis is closed on the right. Precondition: u_p <= u <= u_(n+1)
    and u_p < u_(n+1). Cost: O(log m) comparisons by binary search.
    """
    n = len(knots) - p - 2
    if p < 0 or n < p:
        raise ValueError("need at least p + 1 basis functions")
    if not knots[p] <= u <= knots[n + 1] or knots[p] == knots[n + 1]:
        raise ValueError("u must lie in the domain [u_p, u_(n+1)]")
    if u == knots[n + 1]:
        mu = n
        while knots[mu] == knots[mu + 1]:
            mu -= 1
        return mu
    lo, hi = p, n + 1  # invariant: u_lo <= u < u_hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if u < knots[mid]:
            hi = mid
        else:
            lo = mid
    return lo


def basis_functions(knots: Sequence[Number], p: int, mu: int, u: Number) -> list:
    """Return [N_(mu-p,p)(u), ..., N_(mu,p)(u)] for u in the span [u_mu, u_(mu+1)).

    The right end point u = u_(mu+1) is also accepted: the values are then the
    limits from the left, which is the closed-span rule at the end of the
    domain. Precondition: u_mu < u_(mu+1) and mu - p >= 0, mu + p + 1 <= m.
    Cost: p(p + 1)/2 steps of one division and four products or sums each.
    """
    if not knots[mu] < knots[mu + 1]:
        raise ValueError("the span [u_mu, u_(mu+1)) must be nonempty")
    if mu - p < 0 or mu + p + 1 > len(knots) - 1:
        raise ValueError("the span needs p knots on each side")
    big_n = [Fraction(1)]  # @line L1
    for r in range(1, p + 1):  # @line L2
        m = [Fraction(0)] * (r + 1)  # @line L3
        for s in range(r):  # @line L4
            lo, hi = knots[mu - r + 1 + s], knots[mu + 1 + s]
            a = Fraction(u - lo) / (hi - lo)  # @line L5
            m[s] += (1 - a) * big_n[s]  # @line L6
            m[s + 1] += a * big_n[s]  # @line L7
        big_n = m  # @line L8
    return big_n  # @line L9


def cox_de_boor(knots: Sequence[Number], i: int, p: int, u: Number) -> Fraction:
    """N_(i,p)(u) by the recursion as written, with 0/0 = 0 and half-open spans.

    The value at u = u_m (the last knot) is 0, as the half-open definition
    gives; use basis_functions with the closed last span for the end point.
    """
    if p == 0:
        return Fraction(1) if knots[i] <= u < knots[i + 1] else Fraction(0)
    total = Fraction(0)
    d1 = knots[i + p] - knots[i]
    if d1 != 0:
        total += Fraction(u - knots[i]) / d1 * cox_de_boor(knots, i, p - 1, u)
    d2 = knots[i + p + 1] - knots[i + 1]
    if d2 != 0:
        total += Fraction(knots[i + p + 1] - u) / d2 * cox_de_boor(knots, i + 1, p - 1, u)
    return total


def all_basis_values(knots: Sequence[Number], p: int, u: Number) -> list:
    """Return [N_(0,p)(u), ..., N_(n,p)(u)] for u in the domain [u_p, u_(n+1)].

    Uses find_span and basis_functions, so it costs O(log m + p^2 + n).
    """
    n = len(knots) - p - 2
    mu = find_span(knots, p, u)
    values = [Fraction(0)] * (n + 1)
    for s, v in enumerate(basis_functions(knots, p, mu, u)):
        values[mu - p + s] = v
    return values
