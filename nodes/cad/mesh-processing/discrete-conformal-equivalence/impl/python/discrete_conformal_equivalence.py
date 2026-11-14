# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-conformal-equivalence/. The authors are listed in prov/VG00WC.jsonl.

"""Discrete conformal maps by conformal equivalence (Springborn, Schroder and Pinkall 2008).

Two metrics on the same triangle mesh are discretely conformally equivalent
if there are vertex values u with  l~_ij = exp((u_i + u_j) / 2) l_ij  on every
edge. Given target angle sums Theta_i at the free vertices, the code finds u
by Newton's method with a backtracking line search on the convex energy

    E(u) = sum_t ( 2 f_t(u) - pi (u_i + u_j + u_k) ) + sum_i Theta_i u_i,
    f_t = sum_corners ( alpha x_opposite + Lob(alpha) ),   x = log l~,

where Lob is Milnor's Lobachevsky function. The gradient of E is
Theta_i - (angle sum at i), and its Hessian is the cotangent Laplacian of the
new metric. A triangle whose new lengths break the triangle inequality gets
the angles (pi, 0, 0), which extends E to a convex C^1 function on all of R^n.
"""

import math

from mx2geom import corner_angle, solve, undirected_edges

# zeta(2n) for n = 1..4 in closed form; larger n by direct sums (error far below 1e-16 after scaling).
_ZETA = [0.0, math.pi ** 2 / 6, math.pi ** 4 / 90, math.pi ** 6 / 945, math.pi ** 8 / 9450]
for _n in range(5, 60):
    _ZETA.append(sum(k ** (-2.0 * _n) for k in range(1, 40)))


def lobachevsky(x):
    """Milnor's Lobachevsky function  Lob(x) = -integral_0^x log|2 sin t| dt  (odd, period pi)."""
    x = math.fmod(x, math.pi)
    if x < 0:
        x += math.pi
    sign = 1.0
    if x > math.pi / 2:
        x, sign = math.pi - x, -1.0
    if x == 0.0:
        return 0.0
    # log(2 sin t) = log(2 t) - sum_n zeta(2n) t^(2n) / (n pi^(2n)), integrated from 0 to x.
    s = x * math.log(2 * x) - x
    r = (x / math.pi) ** 2
    p = r
    for n in range(1, 60):
        term = _ZETA[n] * p * x / (n * (2 * n + 1))
        s -= term
        if term < 1e-18:
            break
        p *= r
    return -sign * s


def triangle_angles(l0, l1, l2):
    """Angles opposite the sides l0, l1, l2, and True; (pi, 0, 0)-type angles and False if degenerate."""
    if l0 >= l1 + l2:
        return (math.pi, 0.0, 0.0), False
    if l1 >= l0 + l2:
        return (0.0, math.pi, 0.0), False
    if l2 >= l0 + l1:
        return (0.0, 0.0, math.pi), False
    return (corner_angle(l0, l1, l2), corner_angle(l1, l2, l0), corner_angle(l2, l0, l1)), True


def edge_lengths(vertices, faces):
    """The length of every edge (a sorted vertex pair) of a mesh with vertex positions."""
    return {e: math.dist(vertices[e[0]], vertices[e[1]]) for e in undirected_edges(faces)}


def new_lengths(lengths, u):
    """The lengths exp((u_i + u_j) / 2) l_ij of the conformally equivalent metric."""
    return {e: math.exp((u[e[0]] + u[e[1]]) / 2) * l for e, l in lengths.items()}


def _key(i, j):
    return (i, j) if i < j else (j, i)


def corner_data(faces, lengths, u):
    """For each face: the new lengths opposite its corners, the angles, and whether it is a valid triangle."""
    nl = new_lengths(lengths, u)  # @line L3
    out = []
    for a, b, c in faces:
        ls = (nl[_key(b, c)], nl[_key(c, a)], nl[_key(a, b)])
        ang, ok = triangle_angles(*ls)
        out.append((ls, ang, ok))
    return out


def energy(faces, lengths, u, theta):
    """E(u) for the target angle sums theta (a dict from vertex to target)."""
    total = 0.0
    for (a, b, c), (ls, ang, ok) in zip(faces, corner_data(faces, lengths, u)):
        f = sum(al * math.log(l) + lobachevsky(al) for al, l in zip(ang, ls))
        total += 2 * f - math.pi * (u[a] + u[b] + u[c])
    return total + sum(t * u[i] for i, t in theta.items())


def angle_sums(faces, lengths, u, n):
    """The sum of the corner angles at each of the n vertices in the metric with scale factors u."""
    s = [0.0] * n
    for tri, (ls, ang, ok) in zip(faces, corner_data(faces, lengths, u)):
        for k in range(3):
            s[tri[k]] += ang[k]
    return s


def gradient_and_hessian(faces, lengths, u, theta, free):
    """Gradient Theta_i - angle sum and Hessian (cotangent Laplacian of the new metric) on the free vertices."""
    n = len(u)
    idx = {v: k for k, v in enumerate(free)}
    h = [[0.0] * len(free) for _ in free]
    s = [0.0] * n
    for tri, (ls, ang, ok) in zip(faces, corner_data(faces, lengths, u)):
        for k in range(3):
            s[tri[k]] += ang[k]
            if not ok:
                continue
            w = 0.5 / math.tan(ang[k])  # @line L8
            i, j = tri[(k + 1) % 3], tri[(k + 2) % 3]
            for x, y, val in ((i, i, w), (j, j, w), (i, j, -w), (j, i, -w)):
                if x in idx and y in idx:
                    h[idx[x]][idx[y]] += val
    g = [theta[v] - s[v] for v in free]  # @line L4
    return g, h


def conformal_scale_factors(faces, lengths, theta, n, u0=None, tol=1e-12, max_steps=100):
    """Newton's method with backtracking for the u that gives the angle sums theta at the free vertices.

    theta maps each free vertex to its target angle sum; the other vertices keep u fixed (u0, default 0).
    Returns (u, steps). Raises ValueError if the minimum makes a triangle degenerate (no solution
    without changing the triangulation) or if Newton does not converge in max_steps steps.
    """
    u = list(u0) if u0 is not None else [0.0] * n  # @line L1
    free = sorted(theta)
    for step in range(max_steps):  # @line L2
        g, h = gradient_and_hessian(faces, lengths, u, theta, free)
        if max(abs(x) for x in g) < tol:  # @line L5
            if not all(ok for _, _, ok in corner_data(faces, lengths, u)):
                raise ValueError("the minimum has a degenerate triangle")  # @line L6
            return u, step  # @line L7
        try:
            d = [x[0] for x in solve(h, [[-x] for x in g], 1e-14)]  # @line L9
        except ValueError:
            # Degenerate triangles make H singular; step down the gradient instead.
            d = [-x for x in g]
        e0 = energy(faces, lengths, u, theta)
        slope = sum(gi * di for gi, di in zip(g, d))
        t = 1.0
        # When the predicted decrease is at the level of rounding, energy values cannot rank
        # the steps, and the full Newton step is taken.
        exact_enough = -slope < 1e-12 * max(1.0, abs(e0))
        while True:  # @line L10
            trial = list(u)
            for v, dv in zip(free, d):
                trial[v] += t * dv
            if exact_enough or energy(faces, lengths, trial, theta) <= e0 + 1e-4 * t * slope or t < 1e-12:
                break
            t /= 2
        u = trial  # @line L11
    raise ValueError("Newton did not converge")  # @line L12


def layout(faces, lengths, u):
    """Lay out a disk with the new lengths: place one triangle, then the others across shared edges."""
    nl = new_lengths(lengths, u)
    pos = {}
    a, b, c = faces[0]
    pos[a] = (0.0, 0.0)
    pos[b] = (nl[_key(a, b)], 0.0)
    pos[c] = _third(pos[a], pos[b], nl[_key(a, c)], nl[_key(b, c)])
    by_edge = {}
    for f, tri in enumerate(faces):
        for k in range(3):
            by_edge[(tri[k], tri[(k + 1) % 3])] = f
    done = {0}
    queue = [0]
    while queue:
        f = queue.pop()
        tri = faces[f]
        for k in range(3):
            i, j = tri[k], tri[(k + 1) % 3]
            g = by_edge.get((j, i))
            if g is None or g in done:
                continue
            done.add(g)
            other = [v for v in faces[g] if v not in (i, j)][0]
            if other not in pos:
                # Triangle (j, i, other) is counterclockwise.
                pos[other] = _third(pos[j], pos[i], nl[_key(j, other)], nl[_key(i, other)])
            queue.append(g)
    return pos


def _third(p, q, lp, lq):
    """The point r left of the directed segment pq with |r - p| = lp and |r - q| = lq."""
    d = math.dist(p, q)
    x = (lp * lp - lq * lq + d * d) / (2 * d)
    y = math.sqrt(max(0.0, lp * lp - x * x))
    ex, ey = (q[0] - p[0]) / d, (q[1] - p[1]) / d
    return (p[0] + x * ex - y * ey, p[1] + x * ey + y * ex)
