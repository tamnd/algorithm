# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oslo-algorithm/. The authors are listed in prov/MGGW0D.jsonl.

"""The Oslo algorithm: refine the knot vector of a B-spline curve in one pass.

The old curve has degree p, control points c_0, ..., c_n and knots
tau_0, ..., tau_(n+p+1). The fine knot vector t_0, ..., t_(N+p+1) contains
every old knot, with the same multiplicity or more. For each new control point
d_j the algorithm computes the row alpha_j of the knot insertion matrix, the
discrete B-splines of Cohen, Lyche and Riesenfeld, by the Cox-de Boor
triangle in which step r uses the knot t_(j+r) in place of the parameter.
Then d_j is the sum over i of alpha_j[i] c_i.
"""

from bisect import bisect_right
from collections import Counter
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple, Union

Number = Union[int, Fraction]
Point = Tuple[Number, ...]


def check_refinement(tau: Sequence[Number], t: Sequence[Number], p: int) -> None:
    """Raise ValueError unless t is a valid refinement of tau for the Oslo algorithm.

    Conditions: both vectors are sorted; t contains tau as a multiset; each
    new knot lies strictly inside the domain (tau_p, tau_(n+1)); the end
    spans of the domain are nonempty (tau_p < tau_(p+1) and tau_n < tau_(n+1));
    and no knot of t has multiplicity above p + 1.
    """
    n = len(tau) - p - 2
    if n < p or list(tau) != sorted(tau) or list(t) != sorted(t):
        raise ValueError("knot vectors must be sorted, with at least p + 1 control points")
    if Counter(tau) - Counter(t):
        raise ValueError("t must contain every knot of tau")
    if any(not tau[p] < x < tau[n + 1] for x in (Counter(t) - Counter(tau)).elements()):
        raise ValueError("new knots must lie strictly inside (tau_p, tau_(n+1))")
    if not (tau[p] < tau[p + 1] and tau[n] < tau[n + 1]):
        raise ValueError("the first and last spans of the domain must be nonempty")
    if max(Counter(t).values()) > p + 1:
        raise ValueError("no knot may have multiplicity above p + 1")


def oslo_row(tau: Sequence[Number], t: Sequence[Number], p: int, j: int) -> Tuple[int, List[Fraction]]:
    """Return (mu, row) with row[s] = alpha_(mu-p+s, p)(j) for s = 0, ..., p.

    All other alpha_(i, p)(j) are zero. Precondition: check_refinement(tau, t, p)
    passes and 0 <= j <= N. Cost: O(log n) for the span and p(p + 1)/2 steps.
    """
    n = len(tau) - p - 2
    mu = min(max(bisect_right(tau, t[j]) - 1, p), n)  # @line L2
    row = [Fraction(1)]  # @line L3
    for r in range(1, p + 1):  # @line L4
        x = t[j + r]  # @line L5
        nxt = [Fraction(0)] * (r + 1)
        for s in range(r):  # @line L6
            lo, hi = tau[mu - r + 1 + s], tau[mu + 1 + s]
            a = Fraction(x - lo) / (hi - lo)  # @line L7
            nxt[s] += (1 - a) * row[s]  # @line L8
            nxt[s + 1] += a * row[s]
        row = nxt
    return mu, row


def oslo_refine(
    tau: Sequence[Number], t: Sequence[Number], p: int, ctrl: Sequence[Point]
) -> List[Tuple[Fraction, ...]]:
    """Return the N + 1 control points of the same curve on the fine knot vector t.

    Precondition: len(tau) == len(ctrl) + p + 1 and check_refinement(tau, t, p)
    passes. Cost: O(N (log n + p^2 + p d)) arithmetic operations for N + 1 new
    points in dimension d, and O(p) extra space besides the output.
    """
    if len(tau) != len(ctrl) + p + 1:
        raise ValueError("need len(tau) == len(ctrl) + p + 1")
    check_refinement(tau, t, p)
    big_n = len(t) - p - 2
    out = []
    for j in range(big_n + 1):  # @line L1
        mu, row = oslo_row(tau, t, p, j)
        dim = len(ctrl[0])
        d = [Fraction(0)] * dim
        for s, a in enumerate(row):  # @line L9
            for k in range(dim):
                d[k] += a * ctrl[mu - p + s][k]
        out.append(tuple(d))  # @line L10
    return out


def oslo_matrix(tau: Sequence[Number], t: Sequence[Number], p: int) -> List[Dict[int, Fraction]]:
    """Return the knot insertion matrix as one sparse row {i: alpha_(i,p)(j)} per new index j."""
    check_refinement(tau, t, p)
    rows = []
    for j in range(len(t) - p - 1):
        mu, row = oslo_row(tau, t, p, j)
        rows.append({mu - p + s: a for s, a in enumerate(row) if a != 0})
    return rows
