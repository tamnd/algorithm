# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roam-terrain/. The authors are listed in prov/5KAMME.jsonl.

"""ROAM: a triangle bintree over a height grid, kept as a conforming mesh
by forced splits and diamond merges, with split and merge queues.

The domain is the square [0, M] x [0, M] with M = 2^k. A domain point is a
pair (x, y) of integers; the height of a grid vertex is h[(x, y)]. (The world
of this site is y up; here the pair names a point of the ground plane and the
height is a separate value, as in Duchaineau et al., who call it z.)

A triangle is a tuple (a, v0, v1): the apex a is the right-angle vertex and
(v0, v1) is the base (the hypotenuse). All triangles are counterclockwise.
The children of T = (a, v0, v1) with base midpoint c are T0 = (c, a, v0) and
T1 = (c, v1, a). All arithmetic on heights and priorities is exact.
"""

import heapq
from fractions import Fraction


def midpoint(T):
    _, v0, v1 = T
    sx, sy = v0[0] + v1[0], v0[1] + v1[1]
    if sx % 2 or sy % 2:
        return None
    return (sx // 2, sy // 2)


def base(T):
    return frozenset((T[1], T[2]))


def edges_of(T):
    a, v0, v1 = T
    return (frozenset((a, v0)), frozenset((v0, v1)), frozenset((v1, a)))


class Bintree:
    """The full triangle bintree of the grid and the wedgie thickness of every triangle."""

    def __init__(self, k, h):
        m = 2 ** k
        self.m = m
        self.h = h
        self.roots = (((0, 0), (m, 0), (0, m)), ((m, m), (0, m), (m, 0)))
        self.children = {}
        self.parent = {}
        self.all = []
        stack = list(self.roots)
        while stack:
            t = stack.pop()
            self.all.append(t)
            c = midpoint(t)
            if c is None:
                continue
            a, v0, v1 = t
            kids = ((c, a, v0), (c, v1, a))
            self.children[t] = kids
            for u in kids:
                self.parent[u] = t
                stack.append(u)
        self.err = {}
        for t in reversed(self.all):  # @line L10
            if t in self.children:
                t0, t1 = self.children[t]
                _, v0, v1 = t
                c = midpoint(t)
                gap = abs(h[c] - Fraction(h[v0] + h[v1], 2))
                self.err[t] = max(self.err[t0], self.err[t1]) + gap  # @line L11
            else:
                self.err[t] = Fraction(0)

    def partner(self, t):
        """The triangle of the same level that shares the base of t, or None on the border."""
        a, v0, v1 = t
        b = (v0[0] + v1[0] - a[0], v0[1] + v1[1] - a[1])
        if 0 <= b[0] <= self.m and 0 <= b[1] <= self.m:
            return (b, v1, v0)
        return None


def dist2_point_triangle(p, t):
    """Exact squared distance from the point p to the closed triangle t."""
    a, b, c = t

    def cross(o, u, v):
        return (u[0] - o[0]) * (v[1] - o[1]) - (u[1] - o[1]) * (v[0] - o[0])

    if cross(a, b, p) >= 0 and cross(b, c, p) >= 0 and cross(c, a, p) >= 0:
        return Fraction(0)
    best = None
    for u, v in ((a, b), (b, c), (c, a)):
        dx, dy = v[0] - u[0], v[1] - u[1]
        s = Fraction((p[0] - u[0]) * dx + (p[1] - u[1]) * dy, dx * dx + dy * dy)
        s = min(max(s, Fraction(0)), Fraction(1))
        qx, qy = u[0] + s * dx - p[0], u[1] + s * dy - p[1]
        d = qx * qx + qy * qy
        best = d if best is None else min(best, d)
    return best


def make_priority(tree, eye, d0):
    """The squared priority (e_T / max(dist(eye, T), d0))^2 of each triangle."""
    cache = {}

    def prio(t):
        if t not in cache:
            e = tree.err[t]
            cache[t] = e * e / max(dist2_point_triangle(eye, t), Fraction(d0) ** 2)  # @line L12
        return cache[t]

    return prio


class Mesh:
    """A conforming triangulation made of bintree triangles, with an edge map."""

    def __init__(self, tree, active=None):
        self.tree = tree
        self.active = set()
        self.edges = {}
        self.added = []
        for t in (tree.roots if active is None else active):
            self._add(t)

    def _add(self, t):
        self.active.add(t)
        self.added.append(t)
        for e in edges_of(t):
            self.edges.setdefault(e, set()).add(t)

    def _remove(self, t):
        self.active.remove(t)
        for e in edges_of(t):
            s = self.edges[e]
            s.discard(t)
            if not s:
                del self.edges[e]

    def split(self, t):
        self._remove(t)
        for u in self.tree.children[t]:
            self._add(u)

    def base_neighbor(self, t):
        others = self.edges.get(base(t), set()) - {t}
        return next(iter(others)) if others else None

    def force_split(self, t):
        stack = [t]  # @line L1
        while stack:  # @line L2
            t = stack[-1]
            if t not in self.active:
                stack.pop()
                continue
            b = self.base_neighbor(t)  # @line L3
            if b is not None and base(b) != base(t):
                stack.append(b)  # @line L4
                continue
            self.split(t)  # @line L5
            if b is not None:
                self.split(b)
            stack.pop()

    def mergeable(self, t):
        tree = self.tree
        if t not in tree.children or t in self.active:
            return False
        for u in (t, tree.partner(t)):
            if u is not None and not all(k in self.active for k in tree.children[u]):
                return False
        return True

    def merge(self, t):
        for u in (t, self.tree.partner(t)):
            if u is None:
                continue
            for k in self.tree.children[u]:
                self._remove(k)
            self._add(u)


def update(mesh, prio, eps):
    """One frame: split every leaf whose priority is above eps, then merge
    every diamond whose priority is at most eps. Returns the mesh."""
    tree = mesh.tree
    eps2 = Fraction(eps) ** 2
    qs = [(-prio(t), t) for t in mesh.active]  # @line L6
    heapq.heapify(qs)
    while qs:  # @line L7
        p, t = heapq.heappop(qs)
        if t not in mesh.active:
            continue
        if -p <= eps2:
            break
        mesh.added = []
        mesh.force_split(t)
        for u in mesh.added:
            heapq.heappush(qs, (-prio(u), u))

    def diamond(t):
        u = tree.partner(t)
        key = min(t, u) if u is not None else t
        return (max(prio(t), prio(u)) if u is not None else prio(t), key)

    qm = []
    for t in {tree.parent[u] for u in mesh.active if u in tree.parent}:
        if mesh.mergeable(t):
            heapq.heappush(qm, diamond(t))
    while qm:  # @line L8
        mp, t = heapq.heappop(qm)
        if not mesh.mergeable(t):
            continue
        if mp > eps2:
            break
        mesh.merge(t)
        for u in (t, tree.partner(t)):
            if u is not None and u in tree.parent and mesh.mergeable(tree.parent[u]):
                heapq.heappush(qm, diamond(tree.parent[u]))
    return mesh  # @line L9


def target(tree, prio, eps):
    """A second method: the leaves of the closure of {T : priority > eps}
    under the parent and same-level partner relations."""
    eps2 = Fraction(eps) ** 2
    stack = [t for t in tree.children if prio(t) > eps2]
    closed = set()
    while stack:
        t = stack.pop()
        if t in closed:
            continue
        closed.add(t)
        for u in (tree.parent.get(t), tree.partner(t)):
            if u is not None:
                stack.append(u)
    return {t for t in tree.all if t not in closed and (t not in tree.parent or tree.parent[t] in closed)}


def interpolate(t, h, p):
    """The height at domain point p of the plane through the corners of t."""
    a, b, c = t
    det = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
    wb = Fraction((p[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (p[1] - a[1]), det)
    wc = Fraction((b[0] - a[0]) * (p[1] - a[1]) - (p[0] - a[0]) * (b[1] - a[1]), det)
    return (1 - wb - wc) * h[a] + wb * h[b] + wc * h[c]


def contains(t, p):
    a, b, c = t

    def cross(o, u, v):
        return (u[0] - o[0]) * (v[1] - o[1]) - (u[1] - o[1]) * (v[0] - o[0])

    return cross(a, b, p) >= 0 and cross(b, c, p) >= 0 and cross(c, a, p) >= 0


def random_heights(rng, m, amp=10):
    return {(x, y): rng.randint(0, amp) for x in range(m + 1) for y in range(m + 1)}
