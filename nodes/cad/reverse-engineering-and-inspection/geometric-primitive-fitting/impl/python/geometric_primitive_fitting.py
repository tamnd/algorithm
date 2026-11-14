# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-primitive-fitting/. The authors are listed in prov/8FSGZT.jsonl.

"""Geometric (orthogonal distance) least-squares fitting of spheres and cylinders.

The fit minimizes the sum of the squared orthogonal distances from the points
to the surface, by Levenberg-Marquardt steps on a local parameterization:

- sphere: center c and radius r, distance |x - c| - r;
- cylinder: a point p on the axis, a unit axis direction u and a radius r,
  distance |(x - p) - ((x - p) . u) u| - r. A step moves p in the two
  directions normal to u, tilts u in those two directions and changes r,
  so the parameters have no gauge freedom.

The starting value comes from an algebraic fit (spheres) or from a search
over axis directions with an algebraic circle fit in the plane normal to the
axis (cylinders), or from the axis of the point normals when they are given.
"""

from math import cos, pi, sin, sqrt
from typing import Callable, List, Optional, Sequence, Tuple

from re1lin import add, cross, dot, gram, jacobi_eigen, norm, scale, solve, sub

Vec = Tuple[float, ...]


# ---- distances ----


def sphere_distance(c: Sequence[float], r: float, x: Sequence[float]) -> float:
    return norm(sub(x, c)) - r


def cylinder_distance(p: Sequence[float], u: Sequence[float], r: float, x: Sequence[float]) -> float:
    w = sub(x, p)
    return norm(sub(w, scale(dot(w, u), u))) - r


# ---- the Levenberg-Marquardt loop of the pseudocode ----


def levenberg_marquardt(theta, residuals: Callable, retract: Callable, mu: float = 1e-3, max_iter: int = 500,
                        tol: float = 1e-15) -> Tuple[object, List[float]]:
    """Minimize sum r_i(theta)^2 by Levenberg steps (J^T J + mu I) delta = -J^T r.

    residuals(theta) returns (r, J) with J the Jacobian in the local
    coordinates that retract(theta, delta) uses. Returns the final theta and
    the history of the accepted costs, which is strictly decreasing.
    Cost: Theta(m k^2 + k^3) per step for m residuals and k local parameters.
    """
    r, J = residuals(theta)
    cost = sum(v * v for v in r)
    history = [cost]
    k = len(J[0])
    for _ in range(max_iter):                                           # @line L2
        A = gram(J)
        for i in range(k):
            A[i][i] += mu
        g = [sum(J[t][i] * r[t] for t in range(len(r))) for i in range(k)]
        delta = solve(A, [-v for v in g])                               # @line L5
        if delta is None:
            break
        new = retract(theta, delta)                                     # @line L6
        r2, J2 = residuals(new)
        cost2 = sum(v * v for v in r2)
        if cost2 < cost:                                                # @line L7
            gain = cost - cost2
            theta, r, J, cost = new, r2, J2, cost2
            history.append(cost)
            mu = max(mu / 10, 1e-12)
            if gain <= tol * max(cost, 1e-300) or cost < 1e-28:         # @line L9
                break
        else:
            mu *= 10                                                    # @line L8
            if mu > 1e16:
                break
    return theta, history                                               # @line L10


# ---- sphere ----


def algebraic_sphere(points: Sequence[Sequence[float]]) -> Tuple[Vec, float]:
    """Kasa fit: least squares of |x|^2 + b . x + e over the points, a linear problem."""
    d = len(points[0])
    rows = [tuple(float(v) for v in x) + (1.0,) for x in points]
    rhs = [-sum(float(v) ** 2 for v in x) for x in points]
    A = gram(rows)
    b = [sum(row[i] * t for row, t in zip(rows, rhs)) for i in range(d + 1)]
    s = solve(A, b, 1e-300)
    if s is None:
        raise ValueError("degenerate points for a sphere")
    c = tuple(-v / 2 for v in s[:d])
    rr = dot(c, c) - s[d]
    return c, sqrt(max(rr, 0.0))


def fit_sphere(points: Sequence[Sequence[float]], start: Optional[Tuple[Vec, float]] = None
               ) -> Tuple[Vec, float, List[float]]:
    """Geometric sphere (or circle, in the plane) fit.

    Precondition: at least d + 1 points, not all on one hyperplane (else ValueError).
    Returns (center, radius, cost history).
    Cost: Theta(m) per step for m points in a fixed dimension d.
    """
    pts = [tuple(float(v) for v in x) for x in points]
    d = len(pts[0])
    if len(pts) < d + 1:
        raise ValueError("too few points")
    c, r = start if start is not None else algebraic_sphere(pts)        # @line L1
    theta = tuple(c) + (r,)

    def residuals(th):
        res, jac = [], []
        cc, rad = th[:d], th[d]
        for x in pts:
            w = sub(x, cc)
            n = norm(w) or 1e-300
            res.append(n - rad)                                         # @line L3
            jac.append(tuple(-v / n for v in w) + (-1.0,))              # @line L4
        return res, jac

    def retract(th, delta):
        return tuple(a + b for a, b in zip(th, delta))

    theta, hist = levenberg_marquardt(theta, residuals, retract)
    return theta[:d], abs(theta[d]), hist


# ---- cylinder ----


def frame(u: Sequence[float]) -> Tuple[Vec, Vec]:
    """Two unit vectors e1, e2 with (u, e1, e2) orthonormal, a fixed function of u."""
    k = min(range(3), key=lambda i: abs(u[i]))
    a = [0.0, 0.0, 0.0]
    a[k] = 1.0
    e1 = cross(u, a)
    e1 = scale(1 / norm(e1), e1)
    return e1, cross(u, e1)


def _circle_in_plane(pts, u):
    e1, e2 = frame(u)
    q = [(dot(x, e1), dot(x, e2)) for x in pts]
    (a, b), r = algebraic_sphere(q)
    cost = sum((sqrt((x - a) ** 2 + (y - b) ** 2) - r) ** 2 for x, y in q)
    return cost, add(scale(a, e1), scale(b, e2)), r


def start_cylinder(points: Sequence[Sequence[float]], normals: Optional[Sequence[Sequence[float]]] = None,
                   directions: int = 400) -> Tuple[Vec, Vec, float]:
    """A starting cylinder: axis from the normals, or the best of a set of directions on the half sphere."""
    pts = [tuple(float(v) for v in x) for x in points]
    if normals is not None:
        vals, vecs = jacobi_eigen(gram([tuple(float(v) for v in n) for n in normals]))
        cands = [tuple(vecs[0])]
    else:
        cands = []
        for i in range(directions):                   # Fibonacci points on the upper half sphere
            z = (i + 0.5) / directions
            t = i * pi * (3 - sqrt(5))
            s = sqrt(1 - z * z)
            cands.append((s * cos(t), s * sin(t), z))
    best = min((_circle_in_plane(pts, u) + (u,) for u in cands), key=lambda t: t[0])
    _, p, r, u = best
    return p, u, r


def fit_cylinder(points: Sequence[Sequence[float]], normals: Optional[Sequence[Sequence[float]]] = None,
                 start: Optional[Tuple[Vec, Vec, float]] = None) -> Tuple[Vec, Vec, float, List[float]]:
    """Geometric cylinder fit.

    Precondition: at least 5 points in space, not all on one line or circle.
    Returns (point on the axis nearest the centroid, unit axis, radius, cost history).
    Cost per step: Theta(m) for m points (5 local parameters).
    """
    pts = [tuple(float(v) for v in x) for x in points]
    if len(pts) < 5:
        raise ValueError("a cylinder needs at least 5 points")
    centroid = scale(1 / len(pts), tuple(sum(x[i] for x in pts) for i in range(3)))
    p, u, r = start if start is not None else start_cylinder(pts, normals)    # @line L1
    u = scale(1 / norm(u), u)
    p = add(p, scale(dot(sub(centroid, p), u), u))

    def residuals(th):
        p0, u0, rad = th
        e1, e2 = frame(u0)
        res, jac = [], []
        for x in pts:
            w = sub(x, p0)
            w1, w2, wu = dot(w, e1), dot(w, e2), dot(w, u0)
            rho = sqrt(w1 * w1 + w2 * w2) or 1e-300
            res.append(rho - rad)                                       # @line L3
            jac.append((-w1 / rho, -w2 / rho, -wu * w1 / rho, -wu * w2 / rho, -1.0))   # @line L4
        return res, jac

    def retract(th, delta):
        p0, u0, rad = th
        e1, e2 = frame(u0)
        p1 = add(p0, add(scale(delta[0], e1), scale(delta[1], e2)))
        u1 = add(u0, add(scale(delta[2], e1), scale(delta[3], e2)))
        u1 = scale(1 / norm(u1), u1)
        p1 = add(p1, scale(dot(sub(centroid, p1), u1), u1))
        return p1, u1, rad + delta[4]

    (p, u, r), hist = levenberg_marquardt((p, u, r), residuals, retract)
    return p, u, abs(r), hist
