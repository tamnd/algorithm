# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independent-contact-regions/. The authors are listed in prov/B0Z8Z4.jsonl.

"""Independent contact regions for two fingers with friction on a polygon.

Model: a rigid polygon in the plane, two point contacts with Coulomb
friction coefficient mu > 0, and Nguyen's condition: two contacts p1 and p2
give force closure if and only if the vector p2 - p1 is strictly inside the
friction cone at p1 and p1 - p2 is strictly inside the friction cone at p2.

The polygon is given in counterclockwise order, so the inward normal of the
edge from V_i to V_(i+1) is the edge direction turned by +90 degrees. A point
on edge i is V_i + t (V_(i+1) - V_i) with t in [0, 1]. A region is an
interval of t. The program finds two intervals [s1, u1] and [s2, u2] that
maximize the smaller of the widths u1 - s1 and u2 - s2, under the condition
that every pair of points of the two closed intervals has p2 - p1 in the
closed cone at p1 and p1 - p2 in the closed cone at p2. When the optimum z is
positive, the open intervals (s1, u1) and (s2, u2) are independent contact
regions: any choice of one contact in each gives force closure.

All arithmetic is exact, with fractions.Fraction. The linear program is
solved by the two-phase simplex method with Bland's rule.
"""

from fractions import Fraction


def _q(x):
    return x if isinstance(x, Fraction) else Fraction(x)


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def edge(polygon, i):
    """Return (A, D, n): the start point, the direction and the inward normal."""
    k = len(polygon)
    a = (_q(polygon[i][0]), _q(polygon[i][1]))
    b = (_q(polygon[(i + 1) % k][0]), _q(polygon[(i + 1) % k][1]))
    d = (b[0] - a[0], b[1] - a[1])
    n = (-d[1], d[0])
    return a, d, n


def cone_generators(n, d, mu):
    """The two edges of the friction cone, ordered so that cross(g0, g1) > 0.

    n and d have the same length, so n +- mu d make the angle atan(mu) with n.
    """
    g0 = (n[0] + mu * d[0], n[1] + mu * d[1])
    g1 = (n[0] - mu * d[0], n[1] - mu * d[1])
    return (g0, g1) if cross(g0, g1) > 0 else (g1, g0)


# ---------------------------------------------------------------------------
# Linear programming: maximize c x subject to A x <= b and x >= 0.


def _pivot(T, basis, r, col):
    piv = T[r][col]
    T[r] = [v / piv for v in T[r]]
    for i in range(len(T)):
        if i != r and T[i][col] != 0:
            f = T[i][col]
            T[i] = [v - f * w for v, w in zip(T[i], T[r])]
    basis[r] = col


def _run(T, basis, cost, allowed):
    """Minimize cost over the tableau T with Bland's rule. Returns False if
    the program is unbounded."""
    while True:
        red = []
        for j in range(len(cost)):
            if not allowed[j]:
                red.append(0)
                continue
            red.append(cost[j] - sum(cost[basis[i]] * T[i][j]
                                     for i in range(len(T))))
        q = next((j for j in range(len(cost)) if red[j] < 0), None)
        if q is None:
            return True
        best = None
        for i in range(len(T)):
            if T[i][q] > 0:
                ratio = T[i][-1] / T[i][q]
                key = (ratio, basis[i])
                if best is None or key < best[0]:
                    best = (key, i)
        if best is None:
            return False
        _pivot(T, basis, best[1], q)


def simplex_max(A, b, c):
    """Maximize c x subject to A x <= b and x >= 0, in exact arithmetic.

    Returns (value, x, basis) or None if the program is infeasible. basis
    lists the basic columns of [A | I] at the optimum, one per kept row.
    Raises ArithmeticError if the program is unbounded.
    """
    m, n = len(A), len(c)
    neg = [i for i in range(m) if b[i] < 0]
    na = len(neg)
    width = n + m + na
    T, basis = [], []
    for i in range(m):
        row = [_q(v) for v in A[i]] + [Fraction(int(i == k)) for k in range(m)]
        row += [Fraction(0)] * na
        rhs = _q(b[i])
        if rhs < 0:
            row = [-v for v in row]
            rhs = -rhs
            a = n + m + neg.index(i)
            row[a] = Fraction(1)
            basis.append(a)
        else:
            basis.append(n + i)
        T.append(row + [rhs])
    allowed = [True] * width
    if na:
        cost1 = [Fraction(0)] * (n + m) + [Fraction(1)] * na
        _run(T, basis, cost1, allowed)
        if sum(T[i][-1] for i in range(m) if basis[i] >= n + m) > 0:
            return None
        # Drive the artificial variables out of the basis or drop the row.
        keep = []
        for i in range(len(T)):
            if basis[i] >= n + m:
                col = next((j for j in range(n + m) if T[i][j] != 0), None)
                if col is None:
                    continue
                _pivot(T, basis, i, col)
            keep.append(i)
        T = [T[i] for i in keep]
        basis = [basis[i] for i in keep]
        for j in range(n + m, width):
            allowed[j] = False
    cost2 = [-_q(v) for v in c] + [Fraction(0)] * (m + na)
    if not _run(T, basis, cost2, allowed):
        raise ArithmeticError("unbounded program")
    x = [Fraction(0)] * n
    for i, j in enumerate(basis):
        if j < n:
            x[j] = T[i][-1]
    value = sum(_q(ci) * xi for ci, xi in zip(c, x))
    return value, x, list(basis)


# ---------------------------------------------------------------------------
# Independent contact regions.

# Variables of the program, in this order.
S1, U1, S2, U2, Z = range(5)


def region_program(polygon, i, j, mu):
    """Build (A, b, c) for the regions on edges i and j of the polygon."""
    mu = _q(mu)
    A1, D1, n1 = edge(polygon, i)  # @line L1
    A2, D2, n2 = edge(polygon, j)  # @line L1
    a0, a1 = cone_generators(n1, D1, mu)  # @line L2
    b0, b1 = cone_generators(n2, D2, mu)  # @line L2
    A, b = [], []

    def at_least_zero(coef, const):
        # coef . x + const >= 0, written as -coef . x <= const.
        A.append([-v for v in coef])
        b.append(const)

    # p1 = A1 + t1 D1 and p2 = A2 + t2 D2, so d = p2 - p1 is
    # (A2 - A1) + t2 D2 - t1 D1, affine in (t1, t2).
    base = (A2[0] - A1[0], A2[1] - A1[1])  # @line L3
    for v1 in (S1, U1):  # @line L4
        for v2 in (S2, U2):  # @line L4
            for g, sign in ((a0, 1), (a1, -1), (b0, -1), (b1, 1)):
                # Cone at p1: cross(a0, d) >= 0 and cross(d, a1) >= 0.
                # Cone at p2, for -d: cross(b0, -d) >= 0, cross(-d, b1) >= 0.
                coef = [Fraction(0)] * 5
                coef[v1] = -sign * cross(g, D1)
                coef[v2] = sign * cross(g, D2)
                at_least_zero(coef, sign * cross(g, base))  # @line L5 @line L6
    for s, u in ((S1, U1), (S2, U2)):  # @line L7
        A.append([Fraction(int(k == u)) for k in range(5)])  # u <= 1
        b.append(Fraction(1))
        coef = [Fraction(0)] * 5  # u - s - z >= 0
        coef[u], coef[s], coef[Z] = Fraction(1), Fraction(-1), Fraction(-1)
        at_least_zero(coef, Fraction(0))
    c = [0, 0, 0, 0, 1]
    return A, b, c


def independent_regions(polygon, i, j, mu):
    """Nguyen's independent contact regions on edges i and j.

    Returns (z, (s1, u1), (s2, u2)) with z > 0, or None if no pair of points
    on the two edges gives force closure. Any contact in the open interval
    (s1, u1) of edge i and any contact in (s2, u2) of edge j give a
    force-closure grasp, and no pair of regions has both widths above z.
    """
    if i == j or _q(mu) <= 0:
        raise ValueError("two different edges and mu > 0 are needed")
    A, b, c = region_program(polygon, i, j, mu)
    res = simplex_max(A, b, c)  # @line L8
    if res is None or res[0] == 0:  # @line L9
        return None  # @line L9
    z, x, _ = res
    return z, (x[S1], x[U1]), (x[S2], x[U2])  # @line L10


def best_edge_pair(polygon, mu):
    """Try every pair of edges and return (z, i, j, r1, r2) with the largest z,
    or None if no pair of edges admits a force-closure grasp."""
    best = None
    k = len(polygon)
    for i in range(k):
        for j in range(i + 1, k):
            res = independent_regions(polygon, i, j, mu)
            if res is not None and (best is None or res[0] > best[0]):
                best = (res[0], i, j, res[1], res[2])
    return best


def point_on_edge(polygon, i, t):
    a, d, _ = edge(polygon, i)
    t = _q(t)
    return (a[0] + t * d[0], a[1] + t * d[1])
