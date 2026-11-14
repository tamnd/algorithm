# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mesh-arrangements/. The authors are listed in prov/NG1GH7.jsonl.

"""Mesh arrangements for solid geometry (Zhou, Grinspun, Zorin and Jacobson 2016), in the plane.

The 3D method cuts all triangles of all input meshes against each other,
labels every cell of the arrangement with one winding number per input, and
keeps the faces between cells that a Boolean rule puts on different sides.
This file does the same one dimension lower: the input is a list of closed
polygons (any closed polylines, which may cross themselves or each other,
overlap or touch), each tagged with the input it belongs to. Edges play the
role of triangles and faces of the planar arrangement play the role of cells.

All coordinates are int or Fraction and every test is exact. A polygon is
oriented counterclockwise, so its outward normal is on the right of each
edge; this is the 2D form of the right-hand rule for faces.
"""

from collections import deque
from fractions import Fraction
from functools import cmp_to_key

from mp3geom import orient2d, sub


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def segment_split_points(p1, p2, q1, q2):
    """The points where segment p1p2 meets q1q2: one crossing point, or the ends of a collinear overlap."""
    r, s = sub(p2, p1), sub(q2, q1)
    d = cross(r, s)
    qp = sub(q1, p1)
    if d != 0:
        t, u = Fraction(cross(qp, s), d), Fraction(cross(qp, r), d)
        if 0 <= t <= 1 and 0 <= u <= 1:
            return [tuple(a + t * b for a, b in zip(p1, r))]
        return []
    if cross(qp, r) != 0:
        return []                              # parallel, on different lines
    out = []
    for x, (a, b) in ((q1, (p1, p2)), (q2, (p1, p2)), (p1, (q1, q2)), (p2, (q1, q2))):
        if min(a, b) <= x <= max(a, b):        # collinear, so the order of tuples is the order on the line
            out.append(x)
    return out


def input_edges(polygons):
    """(start, end, input) for each nonzero edge of each closed polygon."""
    out = []
    for poly, k in polygons:
        pts = [tuple(Fraction(c) for c in p) for p in poly]
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            if a != b:
                out.append((a, b, k))
    return out


def angle_cmp(d1, d2):
    """Counterclockwise order of directions, starting at the positive x axis. Exact."""
    h1 = 0 if (d1[1] > 0 or (d1[1] == 0 and d1[0] > 0)) else 1
    h2 = 0 if (d2[1] > 0 or (d2[1] == 0 and d2[0] > 0)) else 1
    if h1 != h2:
        return h1 - h2
    c = cross(d1, d2)
    return -1 if c > 0 else (1 if c < 0 else 0)


def winding_at(point, edges, n_inputs, skip=None):
    """Exact winding number of each input around a point not on the counted edges (the half-open crossing rule)."""
    w = [0] * n_inputs
    for a, b, k in edges:
        if skip is not None and skip(a, b, k):
            continue
        if a[1] <= point[1] < b[1] and orient2d(a, b, point) > 0:
            w[k] += 1
        elif b[1] <= point[1] < a[1] and orient2d(a, b, point) < 0:
            w[k] -= 1
    return tuple(w)


class Arrangement:
    """The planar arrangement of the input edges, with a winding number vector for the face left of each half-edge."""

    def __init__(self, polygons, n_inputs):
        self.n = n_inputs
        self.edges = input_edges(polygons)
        cuts = [{a, b} for a, b, _ in self.edges]
        for i in range(len(self.edges)):  # @line L1
            a, b, _ = self.edges[i]
            for j in range(i + 1, len(self.edges)):
                c, d, _ = self.edges[j]
                for x in segment_split_points(a, b, c, d):
                    cuts[i].add(x)
                    cuts[j].add(x)
        # multiplicity m[(u, v)][k]: the number of input-k edges that run from u to v, minus those from v to u
        mult = {}
        for (a, b, k), pts in zip(self.edges, cuts):  # @line L2
            r = sub(b, a)
            chain = sorted(pts, key=lambda x: (x[0] - a[0]) * r[0] + (x[1] - a[1]) * r[1])
            for u, v in zip(chain, chain[1:]):
                key, sgn = ((u, v), 1) if u < v else ((v, u), -1)
                mult.setdefault(key, [0] * n_inputs)[k] += sgn
        self.mult = mult
        out = {}
        for u, v in mult:
            out.setdefault(u, []).append(v)
            out.setdefault(v, []).append(u)
        for u in out:  # @line L3
            out[u].sort(key=cmp_to_key(lambda x, y, u=u: angle_cmp(sub(x, u), sub(y, u))))
        self.out = out
        self.position = {(u, v): i for u in out for i, v in enumerate(out[u])}
        self.label = self.propagate()

    def m(self, u, v):
        """Signed multiplicity vector of the half-edge u -> v."""
        if u < v:
            return self.mult[(u, v)]
        return [-x for x in self.mult[(v, u)]]

    def next(self, u, v):
        """The next half-edge of the face left of u -> v: at v, the outgoing edge just clockwise of v -> u."""
        ring = self.out[v]
        return v, ring[(self.position[(v, u)] - 1) % len(ring)]

    def components(self):
        seen, comps = set(), []
        for s in self.out:
            if s in seen:
                continue
            comp, queue = [], deque([s])
            seen.add(s)
            while queue:
                u = queue.popleft()
                comp.append(u)
                for v in self.out[u]:
                    if v not in seen:
                        seen.add(v)
                        queue.append(v)
            comps.append(comp)
        return comps

    def propagate(self):
        label = {}
        for comp in self.components():
            members = set(comp)
            v = min(comp)                      # leftmost, then lowest: on the outer boundary of the component
            # the outgoing half-edge whose left wedge contains the direction (-1, 0)
            h = max(((v, x) for x in self.out[v]), key=cmp_to_key(lambda e, f: -1 if cross(sub(e[1], v), sub(f[1], v)) > 0 else 1))
            # the component is a union of whole closed polygons, which wind 0 around a point just left of v
            label[h] = winding_at(v, self.edges, self.n, skip=lambda a, b, k: a in members)  # @line L4
            queue = deque([h])
            while queue:  # @line L5
                u, x = queue.popleft()
                w = label[(u, x)]
                twin = tuple(a - b for a, b in zip(w, self.m(u, x)))
                for g, val in ((self.next(u, x), w), ((x, u), twin)):
                    if g in label:
                        if label[g] != val:
                            raise AssertionError("inconsistent winding numbers")
                    else:
                        label[g] = val
                        queue.append(g)
        return label

    def boundary(self, rule):
        """The half-edges with an inside face on the left and an outside face on the right, for a rule on winding vectors."""
        return [(u, v) for (u, v), w in self.label.items() if rule(w) and not rule(self.label[(v, u)])]  # @line L6


def area(halfedges):
    """Area enclosed by a set of boundary half-edges with the inside on the left (the shoelace formula). Exact."""
    return Fraction(sum(cross(u, v) for u, v in halfedges)) / 2


def UNION(w):
    return w[0] > 0 or w[1] > 0


def INTERSECTION(w):
    return w[0] > 0 and w[1] > 0


def DIFFERENCE(w):
    return w[0] > 0 and not w[1] > 0


def boolean(polygons_a, polygons_b, rule):
    """Boolean of two inputs, each a list of closed polygons. Returns the boundary half-edges and the area."""
    arr = Arrangement([(p, 0) for p in polygons_a] + [(p, 1) for p in polygons_b], 2)
    edges = arr.boundary(rule)
    return edges, area(edges)  # @line L7
