# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roberts-hidden-line-algorithm/. The authors are listed in prov/T1KFDC.jsonl.

"""Roberts' hidden line algorithm for a scene of convex polyhedra.

Each body is convex and is given by its vertices and its faces. Each face
gives a plane a . x = b with the outward normal a, so the body is the set
where every f(x) = a . x - b is at most 0.

The viewer is a homogeneous point e = (ex, ey, ez, ew):
  ew = 1: an eye at the point (ex, ey, ez) (perspective view),
  ew = 0: the direction (ex, ey, ez) toward the viewer (orthographic view).

A point p of an edge is hidden by a body when the segment from p toward
the viewer enters the interior of the body. Points of that segment are
p + alpha * e in homogeneous form, so the test f < 0 is linear in the edge
parameter t and in alpha. This is the observation that Roberts used.

1. Each edge whose two faces both face away from the viewer is hidden by
   its own body (the back face test).
2. Each other edge is tested against each other body. The pairs (t, alpha)
   with 0 <= t <= 1 and alpha >= 0 that satisfy all the inequalities of the
   body form a convex polygon. Its projection on the t axis, as an open
   interval, is the part of the edge that the body hides.
3. The visible part of the edge is [0, 1] minus the union of those open
   intervals.

All arithmetic uses Fraction, so the result is exact.
"""

from fractions import Fraction


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


class ConvexBody:
    """A convex polyhedron from its vertices and its faces.

    faces: lists of vertex indices, one list per face, in any orientation.
    """

    def __init__(self, vertices, faces):
        self.vertices = [tuple(Fraction(c) for c in v) for v in vertices]
        n = len(self.vertices)
        center = tuple(sum(v[k] for v in self.vertices) / n for k in range(3))
        self.faces = [list(f) for f in faces]
        self.planes = []
        for f in self.faces:
            p0, p1, p2 = (self.vertices[f[0]], self.vertices[f[1]], self.vertices[f[2]])
            a = cross(sub(p1, p0), sub(p2, p0))
            b = dot(a, p0)
            if dot(a, center) - b > 0:  # make the normal point outward
                a, b = (-a[0], -a[1], -a[2]), -b
            self.planes.append((a, b))
        edge_faces = {}
        for fi, f in enumerate(self.faces):
            for k in range(len(f)):
                u, v = f[k], f[(k + 1) % len(f)]
                edge_faces.setdefault((min(u, v), max(u, v)), []).append(fi)
        self.edges = sorted(edge_faces.items())

    def value(self, k, h):
        """f_k at the homogeneous point h = (x, y, z, w): a . xyz - b w."""
        a, b = self.planes[k]
        return a[0] * h[0] + a[1] * h[1] + a[2] * h[2] - b * h[3]


def faces_front(body, eye):
    """For each face: 1 if it faces the viewer, -1 if it faces away, 0 if edge on."""
    out = []
    for k in range(len(body.planes)):
        s = body.value(k, eye)
        out.append((s > 0) - (s < 0))
    return out


def _clip(poly, ct, ca, c0):
    """Clip a convex polygon in the (t, alpha) plane by ct t + ca alpha + c0 <= 0."""
    out = []
    m = len(poly)
    for i in range(m):
        p, q = poly[i], poly[(i + 1) % m]
        fp = ct * p[0] + ca * p[1] + c0
        fq = ct * q[0] + ca * q[1] + c0
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            r = fp / (fp - fq)
            out.append((p[0] + r * (q[0] - p[0]), p[1] + r * (q[1] - p[1])))
    return out


def _area2(poly):
    s = 0
    for i in range(len(poly)):
        s += poly[i - 1][0] * poly[i][1] - poly[i][0] * poly[i - 1][1]
    return s


def hidden_interval(p0, p1, body, eye):
    """Open t interval of the edge p0 p1 that body hides, or None."""
    h0 = (p0[0], p0[1], p0[2], Fraction(1))
    d = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2], Fraction(0))
    rows = []
    for k in range(len(body.planes)):
        # f_k(h0 + t d + alpha e) = f_k(h0) + t f_k(d) + alpha f_k(e)
        rows.append((body.value(k, d), body.value(k, eye), body.value(k, h0)))
    # An upper bound on alpha: some face has f_k(e) > 0, and for larger
    # alpha that inequality fails on the whole edge.
    amax = None
    for ct, ca, c0 in rows:
        if ca > 0:
            amax = max(Fraction(1), (-c0) / ca + 1, (-(c0 + ct)) / ca + 1)
            break
    if amax is None:
        raise ValueError("the viewer is inside a body")
    poly = [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)),  # @line L7
            (Fraction(1), amax), (Fraction(0), amax)]
    for ct, ca, c0 in rows:  # @line L8
        poly = _clip(poly, ct, ca, c0)  # @line L9
        if not poly:
            return None
    if _area2(poly) == 0:  # @line L10
        return None  # only touches the body, does not enter it
    ts = [p[0] for p in poly]
    lo, hi = min(ts), max(ts)
    return (lo, hi) if lo < hi else None


def _subtract(intervals):
    """[0, 1] minus a union of open intervals, as closed pieces of positive length."""
    pieces = []
    pos = Fraction(0)
    for lo, hi in sorted(intervals):
        if lo > pos:
            pieces.append((pos, lo))
        pos = max(pos, hi)
    if pos < 1:
        pieces.append((pos, Fraction(1)))
    return pieces


def roberts_hidden_lines(bodies, eye):
    """Return the visible parts of all edges.

    bodies: list of ConvexBody. eye: homogeneous viewer (ex, ey, ez, ew).
    The result is a list of (body index, (u, v), [(t0, t1), ...]) where
    the pairs are the visible parameter ranges of the edge from vertex u
    to vertex v. Edges that are fully hidden have an empty list.
    """
    eye = tuple(Fraction(c) for c in eye)
    fronts = []
    for body in bodies:  # @line L1
        fronts.append(faces_front(body, eye))  # @line L2
    result = []
    for bi, body in enumerate(bodies):
        for (u, v), fs in body.edges:  # @line L3
            if all(fronts[bi][f] < 0 for f in fs):  # @line L4
                result.append((bi, (u, v), []))  # hidden by its own body
                continue
            p0, p1 = body.vertices[u], body.vertices[v]
            gaps = []  # @line L5
            for bj, other in enumerate(bodies):  # @line L6
                if bj == bi:
                    continue
                gap = hidden_interval(p0, p1, other, eye)
                if gap is not None:
                    gaps.append(gap)
            result.append((bi, (u, v), _subtract(gaps)))  # @line L11
    return result


def box(lo, hi):
    """An axis-parallel box as a ConvexBody."""
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    verts = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    faces = [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]
    return ConvexBody(verts, faces)


if __name__ == "__main__":
    big = box((0, 0, 0), (4, 4, 1))
    small = box((1, 1, 2), (2, 2, 3))
    view = (0, 0, 1, 0)  # look down from z = +infinity
    scene = [big, small]
    for bi, (u, v), parts in roberts_hidden_lines(scene, view):
        p, q = scene[bi].vertices[u], scene[bi].vertices[v]
        print(bi, [str(c) for c in p], [str(c) for c in q], [(str(a), str(b)) for a, b in parts])
