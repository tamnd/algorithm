# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/impact-zones/. The authors are listed in prov/BJ4E1Y.jsonl.

"""Rigid impact zones (Provot 1997, with the rigid motion of Bridson, Fedkiw and Anderson 2002), in 2D.

The cloth is a set of nodes and edges in the plane. In a step of length dt each
node moves on the straight line x_i(s) = x_i + s dt v_i, s in [0, 1]. A
collision is a time s at which a node lies on an edge that does not contain it
(in 2D this point-edge test covers all contacts of a curve).

The failsafe merges the nodes of every collision into one zone (a disjoint-set
structure) and gives each zone the rigid motion with the same linear and
angular momentum, until the paths have no collision. In 2D the rotation of a
zone is a scalar angle, and the 3D fixed component of Bridson et al. is empty.

Choices of this code:
- Only the zones that took part in a collision in this pass get a new rigid
  motion. Other zones keep their velocities.
- If the rotation angle dt |omega| of a zone is pi or more, the zone gets the
  pure translation with its mean velocity. Both motions keep the linear
  momentum; the translation does not keep the angular momentum.
"""

import math

from anim import add, cross2, dot, rot2, scale, sub


# ---------------------------------------------------------------- continuous point-edge test


def _roots_01(a, b, c):
    """Real roots of a s^2 + b s + c in [0, 1], sorted. None if the polynomial is zero."""
    if a == 0.0:
        if b == 0.0:
            return None if c == 0.0 else []
        roots = [-c / b]
    else:
        disc = b * b - 4.0 * a * c
        if disc < 0.0:
            return []
        q = -0.5 * (b + math.copysign(math.sqrt(disc), b))
        roots = [q / a]
        if q != 0.0:
            roots.append(c / q)
        else:
            roots.append(0.0)
    return sorted(s for s in roots if 0.0 <= s <= 1.0)


def _on_segment(p, a, b):
    e = sub(b, a)
    t = dot(sub(p, a), e)
    return 0.0 <= t <= dot(e, e)


def point_edge_time(p0, p1, a0, a1, b0, b1):
    """The first s in [0, 1] at which the moving point p lies on the moving segment ab, or None.

    The point is on the line of the segment where cross(b - a, p - a) = 0, which
    is a quadratic in s, and on the segment where 0 <= (p - a) . (b - a) <= |b - a|^2.
    """
    e0, q0 = sub(b0, a0), sub(p0, a0)
    de, dq = sub(sub(b1, a1), e0), sub(sub(p1, a1), q0)
    roots = _roots_01(cross2(de, dq), cross2(e0, dq) + cross2(de, q0), cross2(e0, q0))
    if roots is None:
        # the three points stay on one line: test where the order along the line can change
        cand = [0.0, 1.0]
        ee = (dot(de, de), 2.0 * dot(e0, de), dot(e0, e0))
        qe = (dot(dq, de), dot(q0, de) + dot(dq, e0), dot(q0, e0))
        for coef in (qe, (qe[0] - ee[0], qe[1] - ee[1], qe[2] - ee[2])):
            r = _roots_01(*coef)
            cand.extend(r or [])
        roots = sorted(cand)
    for s in roots:
        p, a, b = (lerp_point(u, w, s) for u, w in ((p0, p1), (a0, a1), (b0, b1)))
        if _on_segment(p, a, b):
            return s
    return None


def lerp_point(u, w, s):
    return (u[0] + s * (w[0] - u[0]), u[1] + s * (w[1] - u[1]))


def collisions(x0, x1, edges):
    """All (node, edge index, s) with a point-edge collision on the straight paths from x0 to x1."""
    out = []
    for k, (a, b) in enumerate(edges):
        for i in range(len(x0)):
            if i == a or i == b:
                continue
            s = point_edge_time(x0[i], x1[i], x0[a], x1[a], x0[b], x1[b])
            if s is not None:
                out.append((i, k, s))
    return out


# ---------------------------------------------------------------- zones


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
    """New velocities {i: v_i} that move the zone rigidly with its linear and angular momentum."""
    m = sum(mass[i] for i in nodes)
    xcm = scale(sum_vec(scale(x0[i], mass[i]) for i in nodes), 1.0 / m)
    vcm = scale(sum_vec(scale(v[i], mass[i]) for i in nodes), 1.0 / m)
    ang = 0.0
    inertia = 0.0
    for i in nodes:
        r = sub(x0[i], xcm)
        ang += mass[i] * cross2(r, sub(v[i], vcm))
        inertia += mass[i] * dot(r, r)  # @line L7
    omega = ang / inertia if inertia > 0.0 else 0.0  # @line L8
    phi = dt * omega
    if abs(phi) >= math.pi:
        phi = 0.0
    rot = rot2(phi)
    out = {}
    for i in nodes:
        r = sub(x0[i], xcm)
        rr = (rot[0][0] * r[0] + rot[0][1] * r[1], rot[1][0] * r[0] + rot[1][1] * r[1])
        end = add(add(xcm, scale(vcm, dt)), rr)  # @line L9
        out[i] = scale(sub(end, x0[i]), 1.0 / dt)  # @line L10
    return out


def sum_vec(vs):
    s = (0.0, 0.0)
    for w in vs:
        s = (s[0] + w[0], s[1] + w[1])
    return s


def impact_zones(x0, v, mass, edges, dt, max_passes=None, record=None):
    """Apply rigid impact zones until the paths x0 + s dt v have no collision.

    x0 must be free of contacts (no node on an edge that does not contain it).
    Return (v, zones, passes): the new velocities, the list of zones with more
    than one node, and the number of passes that found collisions. If record
    is a list, the collisions of each pass are appended to it.
    """
    n = len(x0)
    v = [tuple(w) for w in v]
    zones = DisjointSet(n)  # @line L1
    passes = 0
    limit = n if max_passes is None else max_passes
    while True:  # @line L2
        x1 = [add(x0[i], scale(v[i], dt)) for i in range(n)]
        found = collisions(x0, x1, edges)  # @line L3
        if record is not None:
            record.append(found)
        if not found:
            break  # @line L4
        if passes >= limit:
            raise RuntimeError("impact zones did not resolve the collisions")
        passes += 1
        touched = set()
        for i, k, _ in found:
            a, b = edges[k]
            touched.add(zones.union(zones.union(i, a), b))  # @line L5
        groups = zones.groups()
        for root in {zones.find(r) for r in touched}:  # @line L6
            v_new = rigid_zone_motion(x0, v, mass, groups[root], dt)
            for i, w in v_new.items():
                v[i] = w
    multi = [g for g in zones.groups().values() if len(g) > 1]
    return v, multi, passes
