# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slab-method-point-location/. The authors are listed in prov/T6VRZV.jsonl.

"""Slab method (Dobkin and Lipton 1976) for planar point location.

The input is a list of segments with integer (or Fraction) end points. Two segments may share an
end point, and otherwise they must be disjoint. Vertical segments are allowed.

Degenerate input is handled by a symbolic shear (x, y) -> (x + eps * y, y) with eps > 0 tiny.
The shear has determinant 1, so orient is unchanged, and the sheared x-order of points is the
lexicographic order of (x, y). So points are compared as Python tuples, no two end points have
the same sheared x, and no segment is vertical after the shear.

A query returns one of
    ("vertex", p)                 q is the end point p,
    ("edge", i)                   q lies on segment i but is not an end point,
    ("face", above, below)        q lies in a face; above and below are the indices of the
                                  segments hit by the upward and the downward vertical rays
                                  (in the sheared plane), or None.
"""

from bisect import bisect_left
from functools import cmp_to_key

Point = tuple[int, int]
Segment = tuple[Point, Point]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of pqr: positive for a counterclockwise turn. Exact for int and Fraction."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def normalize(seg: Segment) -> Segment:
    """Return the segment with its lexicographically smaller end point first."""
    a, b = seg
    return (a, b) if a < b else (b, a)


def seg_cmp(s: Segment, t: Segment) -> int:
    """Compare two normalized segments that both span one open lexicographic interval.

    Returns -1 if s is below t there, 1 if s is above t, 0 if s == t. The segments must not cross.
    """
    if s == t:
        return 0
    a, b = s
    c, d = t
    if c >= a:
        o = orient(a, b, c)
        if o == 0:
            o = orient(a, b, d)
        return -1 if o > 0 else 1
    o = orient(c, d, a)
    if o == 0:
        o = orient(c, d, b)
    return 1 if o > 0 else -1


class SlabLocator:
    """Point location by vertical slabs: O(n^2) build time and space, O(log n) query, worst case."""

    def __init__(self, segments: list[Segment]) -> None:
        segs = [normalize(s) for s in segments]
        for a, b in segs:
            if a == b:
                raise ValueError("a segment must have two distinct end points")
        self.segs = segs
        self.X: list[Point] = sorted({p for s in segs for p in s})  # @line L1
        starts: dict[Point, list[int]] = {}
        ends: dict[Point, list[int]] = {}
        for i, (a, b) in enumerate(segs):
            starts.setdefault(a, []).append(i)
            ends.setdefault(b, []).append(i)
        key = cmp_to_key(lambda i, j: seg_cmp(segs[i], segs[j]))
        active: list[int] = []  # segment indices, sorted from bottom to top
        self.slabs: list[list[int]] = []
        for x in self.X[:-1]:  # @line L2
            # Just left of x, the segments ending at x are still valid in the order; remove them.
            gone = set(ends.get(x, ()))
            if gone:
                active = [i for i in active if i not in gone]
            # Just right of x, insert the segments that start at x.
            for i in starts.get(x, ()):
                k = bisect_left([key(j) for j in active], key(i))
                active.insert(k, i)
            self.slabs.append(list(active))  # @line L3

    def storage(self) -> int:
        """The total number of segment entries in all slabs."""
        return sum(len(s) for s in self.slabs)

    def locate(self, q: Point):
        X = self.X
        j = bisect_left(X, q)
        if j < len(X) and X[j] == q:  # @line L4
            return ("vertex", q)
        i = j - 1  # the slab (X[i], X[i+1]) contains q
        if i < 0 or i >= len(self.slabs):  # @line L5
            return ("face", None, None)
        slab = self.slabs[i]
        lo, hi = 0, len(slab)
        while lo < hi:  # @line L6
            mid = (lo + hi) // 2
            a, b = self.segs[slab[mid]]
            o = orient(a, b, q)
            if o == 0:  # @line L7
                return ("edge", slab[mid])
            if o > 0:
                lo = mid + 1
            else:
                hi = mid
        below = slab[lo - 1] if lo > 0 else None
        above = slab[lo] if lo < len(slab) else None
        return ("face", above, below)  # @line L8


def build_dcel(segments: list[Segment]):
    """Build a doubly connected edge list of the subdivision formed by the segments.

    Returns a dict with lists origin, twin, next, prev, face (one entry per half-edge), the
    vertex list, and the face count. Half-edge 2i goes from the smaller to the larger end point
    of segment i and half-edge 2i + 1 goes back. Each face lies to the left of its half-edges.
    Face 0 is the unbounded face. The hole of a face is attached by a vertical ray from the
    lexicographically smallest vertex of the hole component.
    """
    segs = [normalize(s) for s in segments]
    m = 2 * len(segs)
    origin: list[Point] = [None] * m  # type: ignore[list-item]
    for i, (a, b) in enumerate(segs):
        origin[2 * i], origin[2 * i + 1] = a, b
    twin = [h ^ 1 for h in range(m)]
    out: dict[Point, list[int]] = {}
    for h in range(m):
        out.setdefault(origin[h], []).append(h)

    def half(v: Point) -> int:
        # 0 for directions in [0, pi), 1 for [pi, 2 pi)
        return 0 if v[1] > 0 or (v[1] == 0 and v[0] > 0) else 1

    def ang_cmp(h: int, g: int) -> int:
        p = origin[h]
        u = (origin[twin[h]][0] - p[0], origin[twin[h]][1] - p[1])
        w = (origin[twin[g]][0] - p[0], origin[twin[g]][1] - p[1])
        hu, hw = half(u), half(w)
        if hu != hw:
            return hu - hw
        c = u[0] * w[1] - u[1] * w[0]
        return -1 if c > 0 else (1 if c < 0 else 0)

    pos: dict[int, int] = {}
    for v, hs in out.items():
        hs.sort(key=cmp_to_key(ang_cmp))  # counterclockwise
        for k, h in enumerate(hs):
            pos[h] = k
    nxt = [0] * m
    for h in range(m):
        t = twin[h]
        hs = out[origin[t]]
        nxt[h] = hs[(pos[t] - 1) % len(hs)]  # just clockwise from twin(h)
    prev = [0] * m
    for h in range(m):
        prev[nxt[h]] = h
    # cycles
    cyc = [-1] * m
    cycles: list[list[int]] = []
    for h in range(m):
        if cyc[h] == -1:
            c: list[int] = []
            g = h
            while cyc[g] == -1:
                cyc[g] = len(cycles)
                c.append(g)
                g = nxt[g]
            cycles.append(c)

    def area2(c: list[int]) -> int:
        s = 0
        for g in c:
            p, q = origin[g], origin[twin[g]]
            s += p[0] * q[1] - p[1] * q[0]
        return s

    face_of_cycle = [-1] * len(cycles)
    nfaces = 1
    for k, c in enumerate(cycles):
        if area2(c) > 0:
            face_of_cycle[k] = nfaces
            nfaces += 1
    # Attach each hole cycle (area <= 0) by the segment directly above its smallest vertex.
    for k, c in enumerate(cycles):
        if face_of_cycle[k] != -1:
            continue
        v = min(origin[g] for g in c)
        best = None
        for i, (a, b) in enumerate(segs):
            if a < v < b and orient(a, b, v) < 0:
                if best is None or seg_cmp(segs[i], segs[best]) < 0:
                    best = i
        face_of_cycle[k] = -2 - best if best is not None else 0
    # A hole may hang below a segment of another hole, so resolve the chain of references.
    def resolve(k: int) -> int:
        seen = 0
        while face_of_cycle[k] < -1:
            k = cyc[2 * (-2 - face_of_cycle[k]) + 1]
            seen += 1
            if seen > len(cycles):
                raise RuntimeError("cyclic hole references")
        return face_of_cycle[k]

    face_cycle = [resolve(k) for k in range(len(cycles))]
    face = [face_cycle[cyc[h]] for h in range(m)]
    return {
        "origin": origin,
        "twin": twin,
        "next": nxt,
        "prev": prev,
        "face": face,
        "vertices": sorted(out),
        "faces": nfaces,
        "cycles": cycles,
    }
