# SPDX-License-Identifier: MIT
# Shared helper of the si3 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Small B-spline tools for the si3 pages.

A point is a tuple of numbers of any fixed length. A B-spline curve of degree
p is a knot vector (a list of n + p + 2 non-decreasing numbers, clamped, that
is with p + 1 equal knots at each end) and a list of n + 1 control points.
Entries may be int or Fraction, and then every result here is exact. No
function here is the algorithm of a page: the basis functions, de Boor
evaluation, knot insertion and global interpolation are the standard tools of
the pages b-spline, de-boor-algorithm, boehm-knot-insertion and
curve-interpolation.
"""

from fractions import Fraction


# ---- points ----------------------------------------------------------------

def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(s, a):
    return tuple(s * x for x in a)


def lincomb(ws, ps):
    """Return the sum of ws[i] * ps[i]; ps is not empty."""
    out = [0] * len(ps[0])
    for w, p in zip(ws, ps):
        if w:
            for d in range(len(out)):
                out[d] += w * p[d]
    return tuple(out)


# ---- basis and evaluation --------------------------------------------------

def check_curve(knots, p, ctrl):
    if p < 0 or len(knots) != len(ctrl) + p + 1:
        raise ValueError("a curve of degree p with n + 1 control points needs n + p + 2 knots")
    if any(knots[i] > knots[i + 1] for i in range(len(knots) - 1)):
        raise ValueError("knots must not decrease")
    if knots[p] >= knots[len(ctrl)]:
        raise ValueError("the parameter interval is empty")


def find_span(knots, p, t):
    """The index k with knots[k] <= t < knots[k + 1], in p..n, and n at the right end."""
    n = len(knots) - p - 2
    if t >= knots[n + 1]:
        return n
    if t <= knots[p]:
        return p
    k = p
    while knots[k + 1] <= t:
        k += 1
    return k


def basis_funs(knots, p, k, t):
    """The values N_{k-p,p}(t), ..., N_{k,p}(t), by the Cox-de Boor recursion."""
    N = [Fraction(1)] + [Fraction(0)] * p
    left = [0] * (p + 1)
    right = [0] * (p + 1)
    for j in range(1, p + 1):
        left[j] = t - knots[k + 1 - j]
        right[j] = knots[k + j] - t
        saved = Fraction(0)
        for r in range(j):
            tmp = N[r] / (right[r + 1] + left[j - r])
            N[r] = saved + right[r + 1] * tmp
            saved = left[j - r] * tmp
        N[j] = saved
    return N


def basis_row(knots, p, t):
    """All n + 1 basis values at t, as one list."""
    n = len(knots) - p - 2
    k = find_span(knots, p, t)
    row = [Fraction(0)] * (n + 1)
    for r, val in enumerate(basis_funs(knots, p, k, t)):
        row[k - p + r] = val
    return row


def curve_point(knots, p, ctrl, t):
    """The point of the curve at t, as the basis combination of the control points."""
    k = find_span(knots, p, t)
    N = basis_funs(knots, p, k, t)
    return lincomb(N, ctrl[k - p:k + 1])


def derivative_curve(knots, p, ctrl):
    """The derivative as a B-spline of degree p - 1 on the knots without their ends."""
    if p == 0:
        raise ValueError("the degree must be positive")
    Q = []
    for i in range(len(ctrl) - 1):
        h = knots[i + p + 1] - knots[i + 1]
        Q.append(scale(Fraction(p) / h, sub(ctrl[i + 1], ctrl[i])) if h else
                 tuple(0 for _ in ctrl[0]))
    return knots[1:-1], p - 1, Q


# ---- knot insertion --------------------------------------------------------

def insert_knot(knots, p, ctrl, t):
    """Insert the inner knot t once (Boehm). The curve does not change."""
    if not knots[p] < t < knots[len(ctrl)]:
        raise ValueError("only inner knots can be inserted")
    if knots.count(t) + 1 > p:
        raise ValueError("an inner knot can have multiplicity at most p")
    k = find_span(knots, p, t)
    new = []
    for i in range(len(ctrl) + 1):
        if i <= k - p:
            new.append(ctrl[i])
        elif i > k:
            new.append(ctrl[i - 1])
        else:
            a = (t - knots[i]) / Fraction(knots[i + p] - knots[i])
            new.append(add(scale(1 - a, ctrl[i - 1]), scale(a, ctrl[i])))
    return knots[:k + 1] + [t] + knots[k + 1:], new


def missing_knots(knots, target):
    """The multiset target minus the multiset knots; raises if knots is not a part of target."""
    out = []
    for t in sorted(set(target)):
        d = target.count(t) - knots.count(t)
        if d < 0:
            raise ValueError("the target knot vector must contain the old one")
        out += [t] * d
    return out


def refine(knots, p, ctrl, target):
    """Insert knots until the knot vector equals target. The curve does not change."""
    for t in missing_knots(knots, target):
        knots, ctrl = insert_knot(knots, p, ctrl, t)
    return knots, ctrl


def merge_knots(vectors):
    """The least knot vector that contains each vector, as multisets."""
    vals = sorted(set(t for v in vectors for t in v))
    out = []
    for t in vals:
        out += [t] * max(v.count(t) for v in vectors)
    return out


# ---- tensor product surfaces -----------------------------------------------
# A surface is (U, V, p, q, P): degree p on the knots U in u, degree q on the
# knots V in v, and the control net P[k][l], k along u and l along v.

def surface_point(U, V, p, q, P, u, v):
    k = find_span(U, p, u)
    N = basis_funs(U, p, k, u)
    return lincomb(N, [curve_point(V, q, P[k - p + r], v) for r in range(p + 1)])


def iso_curve_u(U, p, P, u):
    """Control points over V of the curve v -> S(u, v) for a fixed u."""
    k = find_span(U, p, u)
    N = basis_funs(U, p, k, u)
    return [lincomb(N, [P[k - p + r][l] for r in range(p + 1)]) for l in range(len(P[0]))]


def iso_curve_v(V, q, P, v):
    """Control points over U of the curve u -> S(u, v) for a fixed v."""
    return [curve_point(V, q, row, v) for row in P]


def refine_surface(U, V, p, q, P, U2, V2):
    """The same surface on the finer knot vectors U2 and V2."""
    cols = [refine(U, p, [row[l] for row in P], U2)[1] for l in range(len(P[0]))]
    P = [[cols[l][k] for l in range(len(cols))] for k in range(len(cols[0]))]
    return [refine(V, q, row, V2)[1] for row in P]


# ---- interpolation ---------------------------------------------------------

def solve(A, B):
    """Solve A X = B by Gauss-Jordan elimination with exact pivots. B is a list of points."""
    n = len(A)
    M = [[Fraction(x) for x in A[i]] + [Fraction(x) for x in B[i]] for i in range(n)]
    w = len(M[0])
    for c in range(n):
        r = next((r for r in range(c, n) if M[r][c] != 0), None)
        if r is None:
            raise ValueError("singular system")
        M[c], M[r] = M[r], M[c]
        piv = M[c][c]
        M[c] = [x / piv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [tuple(M[i][n:w]) for i in range(n)]


def averaging_knots(params, p):
    """Clamped knots whose inner knots are means of p consecutive parameters."""
    n = len(params) - 1
    inner = [sum(params[j:j + p], Fraction(0)) / p for j in range(1, n - p + 1)]
    return [params[0]] * (p + 1) + inner + [params[-1]] * (p + 1)


def interpolate(params, points, p):
    """The B-spline of degree p through points[k] at params[k], with averaging knots."""
    if len(params) != len(points) or len(points) < p + 1:
        raise ValueError("need at least p + 1 points, one parameter each")
    if any(params[k] >= params[k + 1] for k in range(len(params) - 1)):
        raise ValueError("the parameters must increase")
    knots = averaging_knots(params, p)
    A = [basis_row(knots, p, t) for t in params]
    return knots, solve(A, points)
