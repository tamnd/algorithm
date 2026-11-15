# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zonotope-reachability/. The authors are listed in prov/XHB5KP.jsonl.

"""Zonotope reachability for x' = A x + u with ||u(t)||_inf <= mu (Girard 2005).

A zonotope is a pair (c, gens): the center c is a flat list of n floats and
gens is a list of p generators, each a flat list of n floats. It is the set
{c + sum_j a_j g_j : -1 <= a_j <= 1}.

reach(A, z0, mu, r, steps) returns zonotopes Q_0, ..., Q_(steps-1) with the
following guarantee: every solution x(t) that starts in z0 and uses an input
with ||u(t)||_inf <= mu for all t satisfies x(t) in Q_i for i r <= t <= (i+1) r.
The norm is the infinity norm everywhere: ||x|| = max_i |x_i| and ||A|| is
the largest absolute row sum. The ball of radius rho in this norm is the box
(0, rho I).

For a system x' = A x + B w with ||w||_inf <= mu', put u = B w. Then
||u||_inf <= ||B||_inf mu', and the guarantee holds with mu = ||B||_inf mu'.

Cost: Phi = e^(rA) once, O(n^3). Each step multiplies Phi by the p
generators, O(n^2 p), and adds n generators. Without reduction the order
grows by one per step; reduce_order keeps at most m generators, so with
reduction a step costs O(n^2 m + m log m).
"""

import math

from ctlmat import expm, matvec

__all__ = [
    "zonotope", "box", "linear_map", "minkowski_sum", "support",
    "interval_hull", "sup_norm", "norm_inf", "hull_with_map",
    "reduce_order", "reach", "contains_2d", "vertices_2d",
]


def zonotope(center, gens):
    """Return a zonotope with float entries; drop generators that are exactly zero."""
    c = [float(v) for v in center]
    g = [[float(v) for v in gj] for gj in gens if any(v != 0 for v in gj)]
    return (c, g)


def box(n, rho, center=None):
    """The infinity-norm ball of radius rho, as a zonotope with n axis generators."""
    c = [0.0] * n if center is None else [float(v) for v in center]
    if rho == 0:
        return (c, [])
    return (c, [[float(rho) if i == j else 0.0 for i in range(n)] for j in range(n)])


def linear_map(m, z):
    """Return M Z = (M c, [M g_j]). This is exact."""
    c, gens = z
    return (matvec(m, c), [matvec(m, g) for g in gens])


def minkowski_sum(z1, z2):
    """Return Z1 + Z2 = (c1 + c2, gens1 + gens2). This is exact."""
    c1, g1 = z1
    c2, g2 = z2
    return ([a + b for a, b in zip(c1, c2)], g1 + g2)


def support(z, d):
    """Return max over x in Z of d . x, which is d . c + sum_j |d . g_j|."""
    c, gens = z
    s = sum(di * ci for di, ci in zip(d, c))
    for g in gens:
        s += abs(sum(di * gi for di, gi in zip(d, g)))
    return s


def interval_hull(z):
    """Return (lo, hi), the smallest box that contains Z."""
    c, gens = z
    rad = [sum(abs(g[i]) for g in gens) for i in range(len(c))]
    return [ci - ri for ci, ri in zip(c, rad)], [ci + ri for ci, ri in zip(c, rad)]


def sup_norm(z):
    """Return max over x in Z of ||x||_inf, which is max_i (|c_i| + sum_j |g_j[i]|)."""
    c, gens = z
    return max(abs(c[i]) + sum(abs(g[i]) for g in gens) for i in range(len(c)))


def norm_inf(a):
    """Return the induced infinity norm of a matrix, the largest absolute row sum."""
    return max(sum(abs(v) for v in row) for row in a)


def hull_with_map(z, phi):
    """Return a zonotope that contains the convex hull of Z and Phi Z.

    The center is (c + Phi c) / 2, and the generators are (g_j + Phi g_j) / 2,
    (c - Phi c) / 2 and (g_j - Phi g_j) / 2 (Girard 2005). It has 2 p + 1
    generators for p generators of Z.
    """
    c, gens = z
    pc = matvec(phi, c)
    center = [(a + b) / 2 for a, b in zip(c, pc)]
    out = []
    pg = [matvec(phi, g) for g in gens]
    for g, q in zip(gens, pg):
        out.append([(a + b) / 2 for a, b in zip(g, q)])
    out.append([(a - b) / 2 for a, b in zip(c, pc)])
    for g, q in zip(gens, pg):
        out.append([(a - b) / 2 for a, b in zip(g, q)])
    return zonotope(center, out)


def reduce_order(z, m):
    """Return a zonotope with at most m generators (m >= n) that contains Z.

    The generators are sorted by ||g||_1 - ||g||_inf. The m - n largest are
    kept. The others are replaced by their interval hull, which is n axis
    generators (Girard 2005 uses this sort key).
    """
    c, gens = z
    n = len(c)
    if m < n:
        raise ValueError("reduce_order: m must be at least n")
    if len(gens) <= m:
        return z
    key = sorted(gens, key=lambda g: sum(abs(v) for v in g) - max(abs(v) for v in g))
    small = key[: len(gens) - (m - n)]
    keep = key[len(gens) - (m - n):]
    rad = [sum(abs(g[i]) for g in small) for i in range(n)]
    boxed = [[rad[j] if i == j else 0.0 for i in range(n)] for j in range(n)]
    return zonotope(c, keep + boxed)


def reach(a, z0, mu, r, steps, max_gens=None):
    """Return [Q_0, ..., Q_(steps-1)] with Reach([i r, (i+1) r]) inside Q_i.

    a: the n by n matrix A. z0: the initial zonotope. mu: the bound on
    ||u||_inf. r: the time step. max_gens: if given, Q_i is reduced to at most
    max_gens generators after each step.
    """
    n = len(a)
    phi = expm([[r * v for v in row] for row in a])  # @line L1
    na = norm_inf(a)
    s = sup_norm(z0)
    if na == 0:  # @line L2
        alpha, beta = 0.0, r * mu
    else:
        alpha = (math.exp(r * na) - 1 - r * na) * s
        beta = (math.exp(r * na) - 1) * mu / na
    p0 = hull_with_map(z0, phi)  # @line L3
    q = minkowski_sum(p0, box(n, alpha + beta))  # @line L4
    if max_gens is not None:
        q = reduce_order(q, max_gens)
    out = [q]
    for _ in range(steps - 1):  # @line L5
        q = minkowski_sum(linear_map(phi, q), box(n, beta))  # @line L6
        if max_gens is not None:  # @line L7
            q = reduce_order(q, max_gens)
        out.append(q)  # @line L8
    return out  # @line L9


def contains_2d(z, x, tol=1e-9):
    """Exact membership test for a zonotope in the plane.

    In two dimensions every edge of Z is parallel to a generator, so Z is the
    set of points x with |d . (x - c)| <= sum_j |d . g_j| for each normal
    d = (-g_2, g_1) of a generator g. Points within tol (relative) count as
    inside.
    """
    c, gens = z
    if len(c) != 2:
        raise ValueError("contains_2d: the zonotope must be in the plane")
    if not gens:
        return abs(x[0] - c[0]) <= tol and abs(x[1] - c[1]) <= tol
    dx = [x[0] - c[0], x[1] - c[1]]
    normals = [[-g[1], g[0]] for g in gens]
    rank_one = all(abs(nm[0] * gens[0][0] + nm[1] * gens[0][1]) <= 1e-15 * (1 + abs(nm[0]) + abs(nm[1])) for nm in normals)
    if rank_one:
        # All generators are parallel: Z is a segment, so also test the extent along it.
        normals.append(list(gens[0]))
    for d in normals:
        width = sum(abs(d[0] * g[0] + d[1] * g[1]) for g in gens)
        if abs(d[0] * dx[0] + d[1] * dx[1]) > width + tol * (1 + width):
            return False
    return True


def vertices_2d(z):
    """Return the vertices of a zonotope in the plane, in counterclockwise order."""
    c, gens = z
    if not gens:
        return [list(c)]
    gs = []
    for g in gens:
        if g[1] < 0 or (g[1] == 0 and g[0] < 0):
            g = [-g[0], -g[1]]
        gs.append(g)
    gs.sort(key=lambda g: math.atan2(g[1], g[0]))
    start = [c[0] - sum(g[0] for g in gs), c[1] - sum(g[1] for g in gs)]
    pts = [start]
    p = start
    for g in gs + [[-v for v in g] for g in gs]:
        p = [p[0] + 2 * g[0], p[1] + 2 * g[1]]
        pts.append(p)
    return pts[:-1]
