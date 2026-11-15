# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cbf-safety-filter/. The authors are listed in prov/3VWCBR.jsonl.

"""Control barrier function quadratic program (CBF-QP) with one barrier
constraint and optional box limits on the input.

At a state x of x' = f(x) + g(x) u with a control barrier function h and an
extended class K function alpha, put a = L_g h(x) (a row of m numbers) and
b = L_f h(x) + alpha(h(x)). The filter solves

    minimize |u - u_nom|^2  subject to  a . u + b >= 0,  lo <= u <= hi.

For fixed lambda >= 0, the Lagrangian is minimized over the box by
u(lambda) = clip(u_nom + lambda a). psi(lambda) = a . u(lambda) + b is
continuous, nondecreasing and piecewise linear, so the multiplier is 0 if
clip(u_nom) is feasible and otherwise the smallest root of psi, found by a
binary search over the sorted breakpoints and a linear solve on one piece.
With Fraction inputs the result is exact.

Precondition: u_nom and a are lists of m numbers; lo and hi are None or
lists of m entries, each a number or None (no bound), with lo_j <= hi_j.

Cost: O(m log m) time for the sort and O(log m) evaluations of psi, each
O(m); O(m) extra space.
"""

from fractions import Fraction

__all__ = ["clip", "cbf_qp", "cbf_filter", "INFEASIBLE"]

INFEASIBLE = None


def _div(p, q):
    # int / int would give a float; keep exact values exact.
    if isinstance(p, int) and isinstance(q, int):
        return Fraction(p, q)
    return p / q


def _bounds(lo, hi, m):
    lo = [None] * m if lo is None else list(lo)
    hi = [None] * m if hi is None else list(hi)
    return lo, hi


def clip(v, lo, hi):
    """Clamp each v_j to [lo_j, hi_j]; None means no bound."""
    out = []
    for vj, l, h in zip(v, lo, hi):
        if l is not None and vj < l:
            vj = l
        if h is not None and vj > h:
            vj = h
        out.append(vj)
    return out


def _dot(a, b):
    return sum((x * y for x, y in zip(a, b)), 0)


def cbf_qp(u_nom, a, b, lo=None, hi=None):
    """Return (u, lam): the solution of the CBF-QP and the multiplier of the
    barrier constraint, or (INFEASIBLE, None) if no u in the box satisfies
    a . u + b >= 0."""
    m = len(u_nom)
    lo, hi = _bounds(lo, hi, m)

    def u_of(lam):
        return clip([u + lam * aj for u, aj in zip(u_nom, a)], lo, hi)

    def psi(lam):
        return _dot(a, u_of(lam)) + b

    u = clip(u_nom, lo, hi)  # @line L1
    if _dot(a, u) + b >= 0:  # @line L2
        return u, 0  # @line L2
    best, unbounded = b, False  # @line L3
    for aj, l, h in zip(a, lo, hi):  # @line L3
        if aj > 0:
            if h is None:
                unbounded = True
            else:
                best += aj * h
        elif aj < 0:
            if l is None:
                unbounded = True
            else:
                best += aj * l
    if not unbounded and best < 0:  # @line L3
        return INFEASIBLE, None  # @line L3
    bps = set()  # @line L4
    for uj, aj, l, h in zip(u_nom, a, lo, hi):  # @line L4
        if aj != 0:
            for bound in (l, h):
                if bound is not None:
                    lam = _div(bound - uj, aj)
                    if lam > 0:
                        bps.add(lam)
    bps = sorted(bps)  # @line L4
    # Find the first breakpoint with psi >= 0; psi(0) < 0 here.
    lo_i, hi_i = 0, len(bps)  # @line L5
    while lo_i < hi_i:  # @line L5
        mid = (lo_i + hi_i) // 2
        if psi(bps[mid]) >= 0:
            hi_i = mid
        else:
            lo_i = mid + 1
    left = bps[lo_i - 1] if lo_i > 0 else 0  # @line L5
    p_left = psi(left)  # @line L5
    if lo_i < len(bps):  # @line L5
        right = bps[lo_i]
        p_right = psi(right)
        lam = left + _div((0 - p_left) * (right - left), p_right - p_left)
    else:
        # Past the last breakpoint, a coordinate moves only if it has no
        # bound in the direction of a_j, so psi has slope sum a_j^2 over
        # those coordinates. L3 ensures that this slope is positive.
        slope = 0
        for aj, l, h in zip(a, lo, hi):
            if (aj > 0 and h is None) or (aj < 0 and l is None):
                slope += aj * aj
        lam = left + _div(0 - p_left, slope)
    return u_of(lam), lam  # @line L6


def cbf_filter(f, g, h, grad_h, alpha, u_nom, lo=None, hi=None):
    """Return control(t, x) that applies the CBF-QP to u_nom(t, x).

    f(x) is a list of n numbers, g(x) a list of n rows of m numbers, h(x) a
    number, grad_h(x) a list of n numbers and alpha a function of one number.
    The control returns a list of m numbers, or INFEASIBLE.
    """
    def control(t, x):
        dh = grad_h(x)
        G = g(x)
        m = len(G[0])
        a = [sum(dh[i] * G[i][j] for i in range(len(dh))) for j in range(m)]
        b = _dot(dh, f(x)) + alpha(h(x))
        return cbf_qp(list(u_nom(t, x)), a, b, lo, hi)[0]
    return control
