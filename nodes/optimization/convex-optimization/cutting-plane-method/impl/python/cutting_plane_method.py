# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cutting-plane-method/. The authors are listed in prov/6QC9VJ.jsonl.

"""Kelley's cutting-plane method for a convex function on a box.

    minimize f(x)  subject to  lo <= x <= hi.

The oracle returns f(x) and one subgradient g at x. Each answer gives a cut
f(y) >= f(x) + g^T (y - x), which holds for all y. The model is the maximum of the cuts. One iteration:

    add the cut at x;  U <- min(U, f(x));  (x, t) <- argmin { t : t >= every cut, lo <= x <= hi }.

The minimum t of the model is a lower bound L <= f*, and U is an upper bound, so U - L is a
certified gap. If every subgradient has norm at most G and every side of the box is at most D, the
method stops with U - L <= eps after at most (1 + G D sqrt(n) / eps)^n oracle calls.

Cost of one iteration: one oracle call and one linear program with n + 1 variables, k cuts and
n bounds. The linear program is solved exactly by a dense simplex method with Bland's rule.
"""

from dataclasses import dataclass, field
from fractions import Fraction


@dataclass
class KelleyResult:
    x: list  # the best point found
    upper: object  # U = f(x)
    lower: object  # L <= f*
    history: list = field(default_factory=list)  # (x_j, f_j, g_j, U_j, L_j, x_{j+1}) for j = 0, 1, ...


def kelley(oracle, lo, hi, x0, eps=0, max_iter=100) -> KelleyResult:
    """oracle(x) returns (f(x), g) with g a subgradient of f at x. Stops when U - L <= eps."""
    cuts = []  # @line L1
    x, best, upper = list(x0), None, None
    res = KelleyResult(None, None, None)
    for _ in range(max_iter):  # @line L2
        fx, g = oracle(x)  # @line L3
        cuts.append((x, fx, g))  # @line L4
        if upper is None or fx < upper:  # @line L5
            best, upper = x, fx
        x_new, lower = model_minimum(cuts, lo, hi)  # @line L6
        res.history.append((x, fx, g, upper, lower, x_new))
        res.x, res.upper, res.lower = best, upper, lower
        x = x_new  # @line L7
        if upper - lower <= eps:  # @line L8
            break
    return res  # @line L9


def model_minimum(cuts, lo, hi):
    """Exact minimizer (x, t) of t subject to t >= f_i + g_i^T (x - x_i) and lo <= x <= hi.

    Substitute x = lo + w with 0 <= w <= hi - lo, and t = M - s with s >= 0, where
    M = max_i (cut i at lo) is at least the optimal t. Then maximize s subject to
    g_i^T w + s <= M - (cut i at lo) and w_j <= hi_j - lo_j. The slack basis is feasible.
    """
    n = len(lo)
    lo = [Fraction(v) for v in lo]
    hi = [Fraction(v) for v in hi]
    data = [([Fraction(v) for v in xi], Fraction(fi), [Fraction(v) for v in gi]) for xi, fi, gi in cuts]
    at_lo = [fi + sum(gj * (lj - xj) for gj, lj, xj in zip(gi, lo, xi)) for xi, fi, gi in data]
    big = max(at_lo)
    rows = [gi + [Fraction(1)] for _, _, gi in data]
    rhs = [big - a for a in at_lo]
    for j in range(n):
        rows.append([Fraction(1) if i == j else Fraction(0) for i in range(n)] + [Fraction(0)])
        rhs.append(hi[j] - lo[j])
    v, _ = simplex_max(rows, rhs, [Fraction(0)] * n + [Fraction(1)])
    return [lo[j] + v[j] for j in range(n)], big - v[n]


def simplex_max(a, b, c):
    """Maximize c^T v subject to a v <= b, v >= 0, with b >= 0. Dense tableau, Bland's rule, exact."""
    m, n = len(a), len(c)
    tab = [list(a[i]) + [Fraction(1) if k == i else Fraction(0) for k in range(m)] + [b[i]] for i in range(m)]
    obj = [-cj for cj in c] + [Fraction(0)] * (m + 1)
    basis = [n + i for i in range(m)]
    while True:
        enter = next((j for j in range(n + m) if obj[j] < 0), None)
        if enter is None:
            break
        best = None
        for i in range(m):
            if tab[i][enter] > 0:
                ratio = tab[i][-1] / tab[i][enter]
                if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        if best is None:
            raise ValueError("unbounded linear program")
        r = best[1]
        piv = tab[r][enter]
        tab[r] = [v / piv for v in tab[r]]
        for i in range(m):
            if i != r and tab[i][enter] != 0:
                f = tab[i][enter]
                tab[i] = [p - f * q for p, q in zip(tab[i], tab[r])]
        f = obj[enter]
        obj = [p - f * q for p, q in zip(obj, tab[r])]
        basis[r] = enter
    v = [Fraction(0)] * n
    for i, j in enumerate(basis):
        if j < n:
            v[j] = tab[i][-1]
    return v, obj[-1]
