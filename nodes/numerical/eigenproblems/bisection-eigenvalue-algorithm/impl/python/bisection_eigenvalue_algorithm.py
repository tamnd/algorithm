# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bisection-eigenvalue-algorithm/. The authors are listed in prov/SXNY4P.jsonl.

"""Bisection with Sturm counts for a real symmetric tridiagonal matrix T.

T has the diagonal a[0..n-1] and the off-diagonal b[0..n-2]. negcount(a, b, x) is the number of
eigenvalues of T that are smaller than x. kth_eigenvalue(a, b, k) returns the k-th smallest
eigenvalue (k = 1..n) and the number of bisection steps. Standard library only.
"""

import sys

U = 2.0 ** -53  # unit roundoff of IEEE double precision
SAFMIN = sys.float_info.min


def pivmin(b):
    return SAFMIN * max([1.0] + [t * t for t in b])


def negcount(a, b, x, pmin=None):
    """Number of negative pivots of T - xI = L D L^T, which is #{eigenvalues < x}."""
    if pmin is None:
        pmin = pivmin(b)
    c = 0  # @line L7
    d = 1.0
    for i in range(len(a)):  # @line L8
        d = (a[i] - x) - (b[i - 1] * b[i - 1] / d if i > 0 else 0.0)
        if abs(d) < pmin:
            d = -pmin
        if d < 0.0:  # @line L9
            c += 1
    return c  # @line L10


def gershgorin_interval(a, b):
    n = len(a)
    lo = min(a[i] - (abs(b[i - 1]) if i > 0 else 0.0) - (abs(b[i]) if i < n - 1 else 0.0) for i in range(n))
    hi = max(a[i] + (abs(b[i - 1]) if i > 0 else 0.0) + (abs(b[i]) if i < n - 1 else 0.0) for i in range(n))
    return lo, hi


def kth_eigenvalue(a, b, k, abstol=0.0):
    """The k-th smallest eigenvalue of T, to full relative accuracy by default."""
    n = len(a)
    if not 1 <= k <= n:
        raise ValueError("k out of range")
    pmin = pivmin(b)
    lo, hi = gershgorin_interval(a, b)  # @line L1
    pad = 2.0 * n * U * max(abs(lo), abs(hi)) + 2.0 * pmin
    lo, hi = lo - pad, hi + pad  # now negcount(lo) < k <= negcount(hi)
    steps = 0
    while hi - lo > max(abstol, 2.0 * U * max(abs(lo), abs(hi))):  # @line L2
        x = 0.5 * (lo + hi)
        if x <= lo or x >= hi:  # @line L3: no float strictly between
            break
        steps += 1
        if negcount(a, b, x, pmin) >= k:  # @line L4
            hi = x  # @line L5
        else:
            lo = x
    return 0.5 * (lo + hi), steps  # @line L6


def eigenvalues(a, b, abstol=0.0):
    """All eigenvalues of T in increasing order."""
    return [kth_eigenvalue(a, b, k, abstol)[0] for k in range(1, len(a) + 1)]
