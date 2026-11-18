# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robust-cloth-collision/. The authors are listed in prov/QXMR1R.jsonl.

"""Collision handling for triangle cloth after Bridson, Fedkiw and Anderson (2002), in 3D.

The cloth is a triangle mesh with node positions x (the start of the step),
masses m and candidate mean velocities v for a step of length dt, so that
without contact the step would end at x + dt v. The function
handle_collisions returns new mean velocities with three stages (Section 5 of
the paper):

1. Repulsions (Section 7.2, 7.3). For each point-triangle and edge-edge pair
   closer than the thickness h at the start, an inelastic impulse stops the
   approach, a spring impulse pushes the pair apart, and Coulomb friction
   slows the sliding.
2. Collisions (Section 6, 7.4). A pair collides if its four nodes become
   coplanar on the straight paths (a cubic in t) and are within a rounding
   tolerance at that time. Each collision gets an inelastic impulse with the
   normal of that time. This is repeated a few times.
3. Failsafe (Section 7.5). The nodes of the collisions that remain are merged
   into rigid impact zones until no collision remains.

A contact is (nodes, coeffs, normal): four node indices and four weights with
sum 0, so that the relative position is sum c_j x_j and the relative velocity
is sum c_j v_j. A point-triangle pair (p; a, b, c) has the weights
(1, -w1, -w2, -w3) and an edge-edge pair (a, b; c, d) has the weights
(1 - s, s, -(1 - t), -t). An impulse j n on the contact changes v_j by
c_j j n / m_j, which keeps the momentum because the weights sum to 0.

Choices of this code (not fixed by the paper):
- The impulses are applied one pair at a time (Gauss-Seidel), not in parallel.
- The impulse that changes the relative velocity by dv uses the effective
  mass 1 / sum(c_j^2 / m_j). For equal masses this is the weighting of
  Section 7.1. The spring impulse is capped so that the relative normal
  velocity is at most 0.1 d / dt, the aim stated in Section 7.2.
- All pairs are tested, with a box test first, instead of a bounding volume
  hierarchy. There is no proximity test at the end of the step and no
  adaptive time step.
- If the cubic is zero for all t (the four nodes stay in one plane), the code
  tests 65 evenly spaced times. This can miss a short contact.
- In the failsafe a pair whose four nodes are in one zone is not tested,
  because a rigid zone has no internal contact (the proof).
"""

import math

from anim import add, cross, dot, norm, scale, solve, sub

ROUNDING_TOL = 1e-6  # the distance tolerance at a coplanar time (Section 6, 1e-6 m)
SPRING_FRACTION = 0.1  # the overlap may shrink by at most this fraction per step (Section 7.2)
COPLANAR_SAMPLES = 64  # tuning constant of this code for the degenerate cubic


# ---------------------------------------------------------------- mesh


def mesh_edges(triangles):
    """The sorted list of the edges (i, j), i < j, of a triangle list."""
    out = set()
    for a, b, c in triangles:
        for i, j in ((a, b), (b, c), (c, a)):
            out.add((min(i, j), max(i, j)))
    return sorted(out)


def pairs(n, triangles, edges):
    """All point-triangle pairs (p, tri) with p not in tri and edge-edge pairs with no shared node."""
    pt = [(p, t) for t in triangles for p in range(n) if p not in t]
    ee = [(e, f) for k, e in enumerate(edges) for f in edges[k + 1:] if len({e[0], e[1], f[0], f[1]}) == 4]
    return pt, ee


# ---------------------------------------------------------------- proximity (Section 6)


def point_triangle_proximity(x4, x1, x2, x3, tol):
    """Return (w1, w2, w3, normal, distance) if the point x4 is within tol of the triangle, else None.

    The normal points from the plane of the triangle to the point. The weights
    come from the normal equations and must lie in [-delta, 1 + delta], with
    delta = tol divided by a length of the triangle.
    """
    n = cross(sub(x2, x1), sub(x3, x1))
    nn = norm(n)
    if nn == 0.0:
        return None
    n = scale(n, 1.0 / nn)
    dist = dot(sub(x4, x1), n)
    if abs(dist) >= tol:
        return None
    x13, x23, x43 = sub(x1, x3), sub(x2, x3), sub(x4, x3)
    a11, a12, a22 = dot(x13, x13), dot(x13, x23), dot(x23, x23)
    det = a11 * a22 - a12 * a12
    if det <= 0.0:
        return None
    b1, b2 = dot(x13, x43), dot(x23, x43)
    w1 = (a22 * b1 - a12 * b2) / det
    w2 = (a11 * b2 - a12 * b1) / det
    w3 = 1.0 - w1 - w2
    delta = tol / math.sqrt(nn)
    if min(w1, w2, w3) < -delta or max(w1, w2, w3) > 1.0 + delta:
        return None
    if dist < 0.0:
        n, dist = scale(n, -1.0), -dist
    return w1, w2, w3, n, dist


def segment_closest(p1, q1, p2, q2):
    """Parameters (s, t) in [0, 1] of the closest points p1 + s (q1 - p1) and p2 + t (q2 - p2)."""
    d1, d2, r = sub(q1, p1), sub(q2, p2), sub(p1, p2)
    a, e, f = dot(d1, d1), dot(d2, d2), dot(d2, r)

    def clamp(z):
        return 0.0 if z < 0.0 else 1.0 if z > 1.0 else z

    if a == 0.0 and e == 0.0:
        return 0.0, 0.0
    if a == 0.0:
        return 0.0, clamp(f / e)
    c = dot(d1, r)
    if e == 0.0:
        return clamp(-c / a), 0.0
    b = dot(d1, d2)
    denom = a * e - b * b
    s = clamp((b * f - c * e) / denom) if denom > 1e-14 * a * e else 0.0  # parallel: any s
    t = (b * s + f) / e
    if t < 0.0:
        t, s = 0.0, clamp(-c / a)
    elif t > 1.0:
        t, s = 1.0, clamp((b - c) / a)
    return s, t


def edge_edge_proximity(x1, x2, x3, x4, tol):
    """Return (s, t, normal, distance) if the segments x1x2 and x3x4 are within tol, else None.

    The normal points from the closest point of the second edge to that of the
    first. If the segments touch, it is the normal of the two edges.
    """
    s, t = segment_closest(x1, x2, x3, x4)
    pa = add(x1, scale(sub(x2, x1), s))
    pb = add(x3, scale(sub(x4, x3), t))
    d = sub(pa, pb)
    dist = norm(d)
    if dist >= tol:
        return None
    if dist > 1e-300:
        return s, t, scale(d, 1.0 / dist), dist
    c = cross(sub(x2, x1), sub(x4, x3))
    if norm(c) == 0.0:
        return None
    return s, t, scale(c, 1.0 / norm(c)), dist


def proximity(x, kind, pair, tol):
    """A contact (nodes, coeffs, normal, distance) for a pair within tol at positions x, or None."""
    if kind == "pt":
        p, (a, b, c) = pair
        r = point_triangle_proximity(x[p], x[a], x[b], x[c], tol)
        if r is None:
            return None
        w1, w2, w3, n, dist = r
        return (p, a, b, c), (1.0, -w1, -w2, -w3), n, dist
    (a, b), (c, d) = pair
    r = edge_edge_proximity(x[a], x[b], x[c], x[d], tol)
    if r is None:
        return None
    s, t, n, dist = r
    return (a, b, c, d), (1.0 - s, s, -(1.0 - t), -t), n, dist


# ---------------------------------------------------------------- continuous collision detection (Section 6)


def coplanarity_cubic(p, u):
    """Coefficients (k3, k2, k1, k0) of f(s) = (x21 x x31) . x41 on x_j(s) = p_j + s u_j."""
    a, b, c = sub(p[1], p[0]), sub(p[2], p[0]), sub(p[3], p[0])
    da, db, dc = sub(u[1], u[0]), sub(u[2], u[0]), sub(u[3], u[0])
    ab = cross(a, b)
    ab1 = add(cross(a, db), cross(da, b))
    ab2 = cross(da, db)
    return (dot(ab2, dc), dot(ab1, dc) + dot(ab2, c), dot(ab, dc) + dot(ab1, c), dot(ab, c))


def _poly(k, s):
    return ((k[0] * s + k[1]) * s + k[2]) * s + k[3]


def _quadratic_roots(a, b, c):
    if a == 0.0:
        return [] if b == 0.0 else [-c / b]
    disc = b * b - 4.0 * a * c
    if disc < 0.0:
        return []
    q = -0.5 * (b + math.copysign(math.sqrt(disc), b))
    out = [q / a]
    if q != 0.0:
        out.append(c / q)
    return out


def candidate_times(k):
    """Sorted times in [0, 1] to test: the roots of the cubic k and its critical points.

    The cubic is monotone between its critical points, so each root is found
    by bisection on a sign change. The critical points are kept too, so that a
    root of even multiplicity (a graze) is tested. If k is zero, the code
    returns evenly spaced times.
    """
    if k == (0.0, 0.0, 0.0, 0.0):
        return [i / COPLANAR_SAMPLES for i in range(COPLANAR_SAMPLES + 1)]
    crit = sorted(s for s in _quadratic_roots(3.0 * k[0], 2.0 * k[1], k[2]) if 0.0 < s < 1.0)
    knots = [0.0] + crit + [1.0]
    out = list(crit)
    for lo, hi in zip(knots, knots[1:]):
        flo, fhi = _poly(k, lo), _poly(k, hi)
        if flo == 0.0:
            out.append(lo)
        if fhi == 0.0:
            out.append(hi)
        if (flo < 0.0) != (fhi < 0.0) and flo != 0.0 and fhi != 0.0:
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if mid <= lo or mid >= hi:
                    break
                fm = _poly(k, mid)
                if fm == 0.0:
                    lo = hi = mid
                    break
                if (fm < 0.0) == (flo < 0.0):
                    lo = mid
                else:
                    hi = mid
            out.append(hi)
    return sorted(set(out))


def pair_nodes(kind, pair):
    if kind == "pt":
        p, (a, b, c) = pair
        return (a, b, c, p)  # triangle first, as in f(s)
    (a, b), (c, d) = pair
    return (a, b, c, d)


def collision_time(x0, x1, kind, pair, tol=ROUNDING_TOL):
    """The first s in [0, 1] at which the pair is within tol on the straight paths x0 -> x1, or None."""
    nodes = pair_nodes(kind, pair)
    p = [x0[i] for i in nodes]
    u = [sub(x1[i], x0[i]) for i in nodes]
    for s in candidate_times(coplanarity_cubic(p, u)):
        xs = {i: add(x0[i], scale(sub(x1[i], x0[i]), s)) for i in nodes}
        if proximity(xs, kind, pair, tol) is not None:
            return s
    return None


def _box(points, pad):
    lo = tuple(min(q[k] for q in points) - pad for k in range(3))
    hi = tuple(max(q[k] for q in points) + pad for k in range(3))
    return lo, hi


def _overlap(b1, b2):
    return all(b1[0][k] <= b2[1][k] and b2[0][k] <= b1[1][k] for k in range(3))


def all_collisions(x0, x1, pt, ee, skip=None):
    """All (kind, pair, s) that collide on the straight paths x0 -> x1, by box tests then the cubic."""
    out = []
    vbox = [_box((x0[i], x1[i]), ROUNDING_TOL) for i in range(len(x0))]
    cache = {}

    def box_of(nodes):
        if nodes not in cache:
            cache[nodes] = (tuple(min(vbox[i][0][k] for i in nodes) for k in range(3)),
                            tuple(max(vbox[i][1][k] for i in nodes) for k in range(3)))
        return cache[nodes]

    for kind, plist in (("pt", pt), ("ee", ee)):
        for pair in plist:
            if kind == "pt":
                first, second = (pair[0],), pair[1]
            else:
                first, second = pair
            if not _overlap(box_of(first), box_of(second)):
                continue
            if skip is not None and skip(pair_nodes(kind, pair)):
                continue
            s = collision_time(x0, x1, kind, pair)
            if s is not None:
                out.append((kind, pair, s))
    return out


# ---------------------------------------------------------------- impulses (Section 7.1 to 7.4)


def relative_velocity(v, nodes, coeffs):
    out = (0.0, 0.0, 0.0)
    for i, c in zip(nodes, coeffs):
        out = add(out, scale(v[i], c))
    return out


def apply_impulse(v, mass, nodes, coeffs, dv):
    """Change the relative velocity sum c_j v_j by the vector dv. Change v in place.

    The impulse j = dv / sum(c_j^2 / m_j) acts on node j as c_j j, so the
    momentum change is j sum c_j = 0.
    """
    w = sum(c * c / mass[i] for i, c in zip(nodes, coeffs))
    for i, c in zip(nodes, coeffs):
        v[i] = add(v[i], scale(dv, c / (mass[i] * w)))


def repulsion(v, mass, contact, h, dt, k, mu):
    """Inelastic, spring and friction impulses of one close pair (Section 7.2, 7.3).

    Return the change of the relative normal velocity.
    """
    nodes, coeffs, n, dist = contact
    d = h - dist  # @line L2
    vn = dot(relative_velocity(v, nodes, coeffs), n)
    vn0 = vn
    if vn < 0.0:
        apply_impulse(v, mass, nodes, coeffs, scale(n, -vn))  # @line L3
        vn = 0.0
    target = SPRING_FRACTION * d / dt
    if vn < target:
        m_eff = 1.0 / sum(c * c / mass[i] for i, c in zip(nodes, coeffs))
        apply_impulse(v, mass, nodes, coeffs, scale(n, min(dt * k * d / m_eff, target - vn)))  # @line L4
    dvn = dot(relative_velocity(v, nodes, coeffs), n) - vn0
    if mu > 0.0:
        vr = relative_velocity(v, nodes, coeffs)
        vt = sub(vr, scale(n, dot(vr, n)))
        nt = norm(vt)
        if nt > 0.0:
            cut = min(mu * dvn, nt)
            apply_impulse(v, mass, nodes, coeffs, scale(vt, -cut / nt))  # @line L5
    return dvn


def collision_contact(x0, x1, kind, pair, s):
    """The contact of a collision at time s, with the normal of that time.

    The normal is oriented so that the relative position at the start of the
    step has a positive normal component.
    """
    nodes = pair_nodes(kind, pair)
    xs = {i: add(x0[i], scale(sub(x1[i], x0[i]), s)) for i in nodes}
    con = proximity(xs, kind, pair, ROUNDING_TOL)
    nodes, coeffs, n, _ = con
    if kind == "pt":
        a, b, c = pair[1]
        tn = cross(sub(xs[b], xs[a]), sub(xs[c], xs[a]))
    else:
        (a, b), (c, d) = pair
        tn = cross(sub(xs[b], xs[a]), sub(xs[d], xs[c]))
    if norm(tn) > 0.0:
        n = scale(tn, 1.0 / norm(tn))
    if dot(relative_velocity(x0, nodes, coeffs), n) < 0.0:
        n = scale(n, -1.0)
    return nodes, coeffs, n


# ---------------------------------------------------------------- rigid impact zones (Section 7.5)


class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i):
        while self.parent[i] != i:
            self.parent[i] = self.parent[self.parent[i]]  # path halving
            i = self.parent[i]
        return i

    def union(self, i, j):
        i, j = self.find(i), self.find(j)
        if i == j:
            return i
        if self.size[i] < self.size[j]:
            i, j = j, i
        self.parent[j] = i
        self.size[i] += self.size[j]
        return i

    def groups(self):
        out = {}
        for i in range(len(self.parent)):
            out.setdefault(self.find(i), []).append(i)
        return out


def rigid_zone_motion(x0, v, mass, nodes, dt):
    """Mean velocities {i: v_i} of the rigid motion of a zone (the formula of Section 7.5).

    omega = I^-1 L keeps the angular momentum. The end position is
    x_cm + dt v_cm + x_F + cos(dt |omega|) x_R + sin(dt |omega|) (omega_hat x x_R).
    If the inertia tensor is singular (collinear nodes) or dt |omega| >= pi,
    the zone only translates.
    """
    m = sum(mass[i] for i in nodes)
    xcm, vcm = (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)
    for i in nodes:
        xcm = add(xcm, scale(x0[i], mass[i] / m))
        vcm = add(vcm, scale(v[i], mass[i] / m))
    ang = (0.0, 0.0, 0.0)
    inertia = [[0.0] * 3 for _ in range(3)]
    for i in nodes:
        r = sub(x0[i], xcm)
        ang = add(ang, scale(cross(r, sub(v[i], vcm)), mass[i]))
        rr = dot(r, r)
        for a in range(3):
            for b in range(3):
                inertia[a][b] += mass[i] * ((rr if a == b else 0.0) - r[a] * r[b])
    tr = inertia[0][0] + inertia[1][1] + inertia[2][2]
    omega = (0.0, 0.0, 0.0)
    if tr > 0.0:
        try:
            omega = tuple(solve(inertia, ang))
        except ValueError:
            omega = (0.0, 0.0, 0.0)
        if not all(math.isfinite(w) for w in omega) or abs(_det3(inertia)) <= 1e-12 * tr ** 3:
            omega = (0.0, 0.0, 0.0)
    wn = norm(omega)
    theta = dt * wn
    if theta >= math.pi:
        theta = 0.0
    out = {}
    for i in nodes:
        r = sub(x0[i], xcm)
        if theta > 0.0:
            axis = scale(omega, 1.0 / wn)
            xf = scale(axis, dot(r, axis))
            xr = sub(r, xf)
            r = add(add(xf, scale(xr, math.cos(theta))), scale(cross(axis, xr), math.sin(theta)))
        end = add(add(xcm, scale(vcm, dt)), r)
        out[i] = scale(sub(end, x0[i]), 1.0 / dt)
    return out


def _det3(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


# ---------------------------------------------------------------- the pipeline (Section 5)


def end_positions(x0, v, dt):
    return [add(p, scale(w, dt)) for p, w in zip(x0, v)]


def handle_collisions(x0, v, mass, triangles, dt, h, k, mu=0.0, collision_passes=5, record=None):
    """New mean velocities for the step x0 -> x0 + dt v with no cloth collision.

    x0 must be free of intersections. h is the cloth thickness, k the
    repulsion stiffness (Bridson et al. match it to the stretch stiffness), mu
    the friction coefficient and collision_passes the number of impulse passes
    before the failsafe. If record is a dict, it gets the counts of each stage.
    Return (v, zones), where zones lists the impact zones with more than one node.
    """
    n = len(x0)
    v = [tuple(w) for w in v]
    edges = mesh_edges(triangles)
    pt, ee = pairs(n, triangles, edges)
    info = {"proximities": 0, "collisions": [], "zone_passes": 0}
    # stage 1: repulsions at the start positions
    for kind, plist in (("pt", pt), ("ee", ee)):  # @line L1
        for pair in plist:
            con = proximity(x0, kind, pair, h)
            if con is not None:
                info["proximities"] += 1
                repulsion(v, mass, con, h, dt, k, mu)
    # stage 2: iterated collision impulses
    for _ in range(collision_passes):  # @line L6
        x1 = end_positions(x0, v, dt)
        found = all_collisions(x0, x1, pt, ee)  # @line L7
        info["collisions"].append(len(found))
        if not found:
            break  # @line L8
        for kind, pair, s in found:
            nodes, coeffs, nrm = collision_contact(x0, x1, kind, pair, s)
            vn = dot(relative_velocity(v, nodes, coeffs), nrm)
            if vn < 0.0:
                apply_impulse(v, mass, nodes, coeffs, scale(nrm, -vn))  # @line L9
    # stage 3: rigid impact zones
    zones = DisjointSet(n)
    while True:  # @line L10
        x1 = end_positions(x0, v, dt)
        found = all_collisions(x0, x1, pt, ee,
                               skip=lambda nd: len({zones.find(i) for i in nd}) == 1)  # @line L11
        if not found:
            break  # @line L12
        if info["zone_passes"] >= n:
            raise RuntimeError("impact zones did not resolve the collisions")
        info["zone_passes"] += 1
        touched = set()
        for kind, pair, _ in found:
            a, b, c, d = pair_nodes(kind, pair)
            touched.add(zones.union(zones.union(a, b), zones.union(c, d)))  # @line L13
        groups = zones.groups()
        for root in {zones.find(r) for r in touched}:
            for i, w in rigid_zone_motion(x0, v, mass, groups[root], dt).items():
                v[i] = w
    if record is not None:
        record.update(info)
    return v, [g for g in zones.groups().values() if len(g) > 1]
