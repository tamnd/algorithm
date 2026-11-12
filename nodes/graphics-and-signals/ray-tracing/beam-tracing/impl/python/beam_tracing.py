# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beam-tracing/. The authors are listed in prov/WFNCHK.jsonl.
"""Beam tracing (Heckbert and Hanrahan 1984) in the plane, with exact rational arithmetic.

The scene is a list of disjoint line segments, some of them mirrors. A beam is a wedge of
directions from an apex, narrower than a half turn, optionally with a window: a segment that
the beam starts from, so that only points beyond the window's line belong to the beam. A
direction in the beam is written v(s) = dl + s (dr - dl) for s in [0, 1].

The tracer clips every segment to the beam, visits the clipped segments in front-to-back order,
and gives each one the part of the remaining beam that it covers. A visible part of a mirror
spawns a reflected beam whose apex is the mirror image of the apex. The result is a beam tree.
"""

from fractions import Fraction as Q


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(k, a):
    return (k * a[0], k * a[1])


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def reflect_point(p, a, b):
    """Mirror image of p across the line through a and b."""
    m = sub(b, a)
    w = sub(p, a)
    proj = mul(dot(w, m) / dot(m, m), m)
    return add(a, sub(mul(2, proj), w))


def clip_segment(p, q, halfplanes):
    """Part of segment pq where n . x >= c for every (n, c), as (p', q') or None."""
    u0, u1 = Q(0), Q(1)
    e = sub(q, p)
    for n, c in halfplanes:
        f0, df = dot(n, p) - c, dot(n, e)  # f(u) = f0 + u df
        if df == 0:
            if f0 < 0:
                return None
        elif df > 0:
            u0 = max(u0, -f0 / df)
        else:
            u1 = min(u1, -f0 / df)
        if u0 > u1:
            return None
    return add(p, mul(u0, e)), add(p, mul(u1, e))


class Beam:
    def __init__(self, apex, dl, dr, window=None, skip=None, depth=0):
        assert cross(dl, dr) > 0, "the wedge turns counterclockwise from dl to dr"
        self.apex, self.dl, self.dr, self.window, self.skip, self.depth = apex, dl, dr, window, skip, depth
        self.fragments = []  # (segment index, s0, s1, point at s0, point at s1)
        self.children = {}  # fragment number -> reflected Beam

    def direction(self, s):
        return add(self.dl, mul(s, sub(self.dr, self.dl)))

    def param(self, x):
        """The s of the direction from the apex to the point x."""
        v = sub(x, self.apex)
        return cross(self.dl, v) / cross(sub(self.dl, self.dr), v)

    def halfplanes(self):
        left, right = (-self.dl[1], self.dl[0]), (self.dr[1], -self.dr[0])  # inward normals
        hp = [(left, dot(left, self.apex)), (right, dot(right, self.apex))]
        if self.window is not None:  # keep the side of the window line away from the apex
            a, b = self.window
            n = (a[1] - b[1], b[0] - a[0])
            if dot(n, self.apex) - dot(n, a) > 0:
                n = (-n[0], -n[1])
            hp.append((n, dot(n, a)))
        return hp

    def depth_at(self, seg, s):
        """Ray parameter lam where the direction v(s) from the apex meets the line of seg."""
        p, q = seg
        v = self.direction(s)
        e = sub(q, p)
        return cross(sub(p, self.apex), e) / cross(v, e)


def front_to_back(beam, pieces):
    """Order the clipped pieces so that a piece comes before every piece that it hides."""
    n = len(pieces)
    after = [set() for _ in range(n)]
    indeg = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            lo = max(pieces[i][1], pieces[j][1])
            hi = min(pieces[i][2], pieces[j][2])
            if lo < hi:
                mid = (lo + hi) / 2
                a, b = (i, j) if beam.depth_at(pieces[i][3], mid) < beam.depth_at(pieces[j][3], mid) else (j, i)
                after[a].add(b)
                indeg[b] += 1
    order = []
    ready = [i for i in range(n) if indeg[i] == 0]
    while ready:
        i = ready.pop()
        order.append(i)
        for j in after[i]:
            indeg[j] -= 1
            if indeg[j] == 0:
                ready.append(j)
    if len(order) != n:
        raise ValueError("cyclic overlap; split the segments")
    return [pieces[i] for i in order]


def subtract(remaining, s0, s1):
    """Split the remaining intervals into the parts inside [s0, s1] and the parts outside."""
    inside, outside = [], []
    for a, b in remaining:
        lo, hi = max(a, s0), min(b, s1)
        if lo < hi:
            inside.append((lo, hi))
            if a < lo:
                outside.append((a, lo))
            if hi < b:
                outside.append((hi, b))
        else:
            outside.append((a, b))
    return inside, outside


def trace_beam(beam, segments, mirrors, max_depth):
    """Fill beam.fragments and beam.children recursively; return the beam."""
    pieces = []
    for idx, (p, q) in enumerate(segments):  # @line L1
        if idx == beam.skip:
            continue
        c = clip_segment(p, q, beam.halfplanes())  # @line L2
        if c is None:
            continue
        s0, s1 = sorted((beam.param(c[0]), beam.param(c[1])))
        if s0 < s1:
            pieces.append((idx, s0, s1, (p, q)))
    remaining = [(Q(0), Q(1))]  # @line L3
    for idx, s0, s1, seg in front_to_back(beam, pieces):  # @line L4
        visible, remaining = subtract(remaining, s0, s1)  # @line L5
        for a, b in visible:  # @line L6
            pa = add(beam.apex, mul(beam.depth_at(seg, a), beam.direction(a)))
            pb = add(beam.apex, mul(beam.depth_at(seg, b), beam.direction(b)))
            beam.fragments.append((idx, a, b, pa, pb))
            if idx in mirrors and beam.depth < max_depth:  # @line L7
                apex2 = reflect_point(beam.apex, *seg)  # @line L8
                d1, d2 = sub(pa, apex2), sub(pb, apex2)
                if cross(d1, d2) < 0:
                    d1, d2 = d2, d1
                child = Beam(apex2, d1, d2, window=(pa, pb), skip=idx, depth=beam.depth + 1)
                beam.children[len(beam.fragments) - 1] = trace_beam(child, segments, mirrors, max_depth)  # @line L9
        if not remaining:
            break
    return beam  # @line L10


def beam_path(beam, s):
    """Follow the beam tree along the direction v(s): the list of (segment, hit point)."""
    path = []
    while True:
        for k, (idx, a, b, pa, pb) in enumerate(beam.fragments):
            if a < s < b:
                hit = add(beam.apex, mul(beam.depth_at((pa, pb), s), beam.direction(s)))
                path.append((idx, hit))
                child = beam.children.get(k)
                if child is None:
                    return path
                s, beam = child.param(hit), child
                break
        else:
            return path


def trace_ray(o, d, segments, mirrors, max_depth, skip=None, window_line=None):
    """Reference: follow one ray exactly through the segments; the list of (segment, hit point)."""
    path = []
    for depth in range(max_depth + 1):
        best = None
        for idx, (p, q) in enumerate(segments):
            if idx == skip:
                continue
            e = sub(q, p)
            den = cross(d, e)
            if den == 0:
                continue
            lam = cross(sub(p, o), e) / den
            u = cross(sub(p, o), d) / den
            if lam > 0 and 0 <= u <= 1 and (best is None or lam < best[0]):
                best = (lam, idx)
        if best is None:
            return path
        lam, idx = best
        hit = add(o, mul(lam, d))
        path.append((idx, hit))
        if idx not in mirrors or depth == max_depth:
            return path
        p, q = segments[idx]
        m = sub(q, p)
        d = sub(mul(2 * dot(d, m) / dot(m, m), m), d)
        o, skip = hit, idx
    return path
