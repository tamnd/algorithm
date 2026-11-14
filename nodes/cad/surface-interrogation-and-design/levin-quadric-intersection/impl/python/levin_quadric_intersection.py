# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levin-quadric-intersection/. The authors are listed in prov/NA927X.jsonl.

"""Levin's pencil method for the intersection of two quadrics.

A quadric is a symmetric 4 x 4 matrix Q, with the surface X^T Q X = 0 for
X = (x, y, z, 1). Its upper left 3 x 3 block Q_u is the quadratic part, the
vector g = (Q[0][3], Q[1][3], Q[2][3]) the linear part, so that
Q(x) = x^T Q_u x + 2 g . x + Q[3][3].

The method finds a member R = alpha S + beta T of the pencil whose quadratic
part is singular and not semidefinite of rank 2. Its zero set is a plane, two
planes, a hyperbolic or parabolic cylinder, a hyperbolic paraboloid, or empty,
and it has sheets x = p(u) + v d(u), linear in v. On each line of a sheet the
partner quadric G (S or T) is a quadratic a v^2 + b v + c, whose real roots
give the points of the intersection.
"""

from math import cos, pi, sin, sqrt

from si1geom import add, cross, det, dot, jacobi_eigen, norm, real_roots, scale, solve, sub

TOL = 1e-9


def quadric_value(Q, x):
    X = (x[0], x[1], x[2], 1.0)
    return sum(Q[i][j] * X[i] * X[j] for i in range(4) for j in range(4))


def _upper(Q):
    return [[Q[i][j] for j in range(3)] for i in range(3)]


def _lin(Q):
    return (Q[0][3], Q[1][3], Q[2][3])


def _combo(a, S, b, T):
    return [[a * S[i][j] + b * T[i][j] for j in range(4)] for i in range(4)]


def _mat_vec(A, x):
    return tuple(A[i][0] * x[0] + A[i][1] * x[1] + A[i][2] * x[2] for i in range(3))


def _unit(x):
    return scale(1.0 / norm(x), x)


def _normalized(Q):
    m = max(abs(float(Q[i][j])) for i in range(4) for j in range(4))
    return [[float(Q[i][j]) / m for j in range(4)] for i in range(4)]


class Sheet:
    """One sheet x = point(u) + v * direction(u) of the ruled member, with
    param(x) the value of u of a point x on the sheet."""

    def __init__(self, kind, point, direction, param):
        self.kind = kind
        self.point = point
        self.direction = direction
        self.param = param


def pencil_cubic(S, T):
    """Coefficients c0, c1, c2, c3 of f(1, lam) = det(S_u + lam T_u)."""
    nodes = [-1.0, 0.0, 1.0, 2.0]
    vals = [det([[S[i][j] + t * T[i][j] for j in range(3)] for i in range(3)]) for t in nodes]
    return solve([[t ** k for k in range(4)] for t in nodes], vals)


def middle_eigenvalue_zero(S, T):
    """A point (cos th, sin th) where the middle eigenvalue of the quadratic
    part of the member changes sign. It exists because the member at th + pi
    is minus the member at th."""
    def mid(th):
        return jacobi_eigen(_upper(_combo(cos(th), S, sin(th), T)))[0][1]
    lo, hi = 0.0, pi
    flo = mid(lo)
    if flo == 0:
        return (1.0, 0.0)
    for _ in range(64):
        m = 0.5 * (lo + hi)
        fm = mid(m)
        if (fm > 0) == (flo > 0):
            lo, flo = m, fm
        else:
            hi = m
    th = 0.5 * (lo + hi)
    return (cos(th), sin(th))


def pencil_candidates(S, T, c):
    """The real projective roots of f(alpha, beta) = det(alpha S_u + beta T_u),
    with c the coefficients of f(1, lam), as unit vectors, or the middle
    eigenvalue zero when f vanishes."""
    if max(abs(x) for x in c) <= TOL:
        return [middle_eigenvalue_zero(S, T)]
    raw = [(1.0, t) for t in real_roots(c, -1.0, 1.0)]
    raw += [(t, 1.0) for t in real_roots(list(reversed(c)), -1.0, 1.0)]
    out = []
    for a, b in raw:
        n = sqrt(a * a + b * b)
        a, b = a / n, b / n
        if all(abs(a * b2 - b * a2) > 1e-7 for a2, b2 in out):
            out.append((a, b))
    return out


def _plane_sheet(x0, nrm, G):
    """The plane through x0 with normal nrm, with the ruling direction chosen
    so that G restricted to a ruling is not constant whenever possible."""
    nrm = _unit(nrm)
    e = _unit(cross(nrm, (1.0, 0.0, 0.0)) if abs(nrm[0]) < 0.9 else cross(nrm, (0.0, 1.0, 0.0)))
    f = cross(nrm, e)
    Gu = _upper(G)

    def q(d):
        return dot(d, _mat_vec(Gu, d))
    d = max([e, f, _unit(add(e, f))], key=lambda w: abs(q(w)))
    if abs(q(d)) <= TOL:
        grad = add(_mat_vec(Gu, x0), _lin(G))
        gp = sub(grad, scale(dot(grad, nrm), nrm))
        d = _unit(gp) if norm(gp) > TOL else e
    eu = cross(nrm, d)
    return Sheet("plane", lambda u: add(x0, scale(u, eu)), lambda u: d, lambda x: dot(sub(x, x0), eu))


def ruled_sheets(R, G):
    """Return (kind, sheets) for the member R, or None when its quadratic part
    is regular or semidefinite of rank 2. kind is 'empty' when R = 0 has no
    real point."""
    vals, vecs = jacobi_eigen(_upper(R))
    vecs = [tuple(v) for v in vecs]
    big = max(1.0, max(abs(v) for v in vals))
    zero = [abs(v) <= TOL * big for v in vals]
    rank = 3 - sum(zero)
    r, c = _lin(R), R[3][3]
    if rank == 3:
        return None
    if rank == 2:
        i0 = zero.index(True)
        ia, ib = [i for i in range(3) if i != i0]
        if vals[ia] * vals[ib] > 0:
            return None
        if vals[ia] < 0:
            ia, ib = ib, ia
        ma, mb = vals[ia], vals[ib]
        ea, eb, e3 = vecs[ia], vecs[ib], vecs[i0]
        ra, rb, r3 = dot(r, ea), dot(r, eb), dot(r, e3)
        center = add(scale(-ra / ma, ea), scale(-rb / mb, eb))
        cp = c - ra * ra / ma - rb * rb / mb
        sa, sb = sqrt(ma), sqrt(-mb)

        def at(p, q, w):
            return add(center, add(scale(p / sa, ea), add(scale(q / sb, eb), scale(w, e3))))

        def pmq(x):
            y = sub(x, center)
            return sa * dot(y, ea) - sb * dot(y, eb)
        if abs(r3) > TOL * big:
            # p^2 - q^2 + 2 r3 w + cp = 0 with u = p - q and v = p + q
            sheet = Sheet("hyperbolic paraboloid",
                          lambda u: at(u / 2, -u / 2, -cp / (2 * r3)),
                          lambda u: add(add(scale(0.5 / sa, ea), scale(0.5 / sb, eb)), scale(-u / (2 * r3), e3)),
                          pmq)
            return "hyperbolic paraboloid", [sheet]
        if abs(cp) > TOL * big:
            k = -cp  # p^2 - q^2 = k, with p - q = t and p + q = k / t
            sheet = Sheet("hyperbolic cylinder",
                          lambda t: at((t + k / t) / 2, (k / t - t) / 2, 0.0),
                          lambda t: e3,
                          pmq)
            return "hyperbolic cylinder", [sheet]
        n1 = sub(scale(sa, ea), scale(sb, eb))
        n2 = add(scale(sa, ea), scale(sb, eb))
        return "intersecting planes", [_plane_sheet(center, n1, G), _plane_sheet(center, n2, G)]
    if rank == 1:
        i1 = zero.index(False)
        m1, e1 = vals[i1], vecs[i1]
        r1 = dot(r, e1)
        c0 = scale(-r1 / m1, e1)
        cp = c - r1 * r1 / m1
        rn = sub(r, scale(r1, e1))
        n = norm(rn)
        if n > TOL * big:
            g = scale(1.0 / n, rn)
            h = cross(e1, g)
            sheet = Sheet("parabolic cylinder",
                          lambda u: add(c0, add(scale(u, e1), scale(-(m1 * u * u + cp) / (2 * n), g))),
                          lambda u: h,
                          lambda x: dot(sub(x, c0), e1))
            return "parabolic cylinder", [sheet]
        if abs(cp) <= TOL * big:
            return "double plane", [_plane_sheet(c0, e1, G)]
        s2 = -cp / m1
        if s2 < 0:
            return "empty", []
        s = sqrt(s2)
        return "parallel planes", [_plane_sheet(add(c0, scale(s, e1)), e1, G),
                                   _plane_sheet(add(c0, scale(-s, e1)), e1, G)]
    n = norm(r)
    if n <= TOL * big:
        return "empty", []
    return "plane", [_plane_sheet(scale(-c / (2 * n * n), r), r, G)]


def ruling_quadratic(G, p, d):
    """G(p + v d) = a v^2 + b v + c."""
    Gu = _upper(G)
    a = dot(d, _mat_vec(Gu, d))
    b = 2 * dot(d, add(_mat_vec(Gu, p), _lin(G)))
    return a, b, quadric_value(G, p)


def ruling_roots(G, p, d):
    """Real roots v of G(p + v d) = 0, or None when the whole line lies in G."""
    a, b, c = ruling_quadratic(G, p, d)
    m = max(abs(a), abs(b), abs(c))
    if m <= TOL:
        return None
    if abs(a) > 1e-12 * m:
        disc = b * b - 4 * a * c
        if disc < 0:
            if disc < -1e-12 * (b * b + abs(4 * a * c)):
                return []
            disc = 0.0
        q = -0.5 * (b + (sqrt(disc) if b >= 0 else -sqrt(disc)))
        if q == 0:
            return [0.0]
        return sorted({q / a, c / q})
    if abs(b) > 1e-12 * m:
        return [-c / b]
    return []


def levin_intersection(S, T, us):
    S, T = _normalized(S), _normalized(T)
    c = pencil_cubic(S, T)  # @line L1
    cands = pencil_candidates(S, T, c)  # @line L2
    cands.append(middle_eigenvalue_zero(S, T))  # a safeguard against rounding; the proof needs no more
    for alpha, beta in cands:  # @line L3
        R = _combo(alpha, S, beta, T)
        G = S if abs(beta) >= abs(alpha) else T  # @line L4
        found = ruled_sheets(R, G)  # @line L5
        if found is not None:
            break
    kind, sheets = found
    points, lines = [], []
    for sheet in sheets:  # @line L6
        for u in us:
            if sheet.kind == "hyperbolic cylinder" and u == 0:
                continue
            p, d = sheet.point(u), sheet.direction(u)
            roots = ruling_roots(G, p, d)  # @line L7
            if roots is None:
                lines.append((p, d))
                continue
            for v in roots:  # @line L8
                points.append(add(p, scale(v, d)))
    return {"member": R, "kind": kind, "partner": G, "sheets": sheets, "points": points, "lines": lines}  # @line L9
