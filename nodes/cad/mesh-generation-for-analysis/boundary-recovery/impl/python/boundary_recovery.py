# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-recovery/. The authors are listed in prov/NKFBHW.jsonl.

"""Segment recovery by edge protection (Shewchuk 2002), with exact predicates.

The input is the 1-skeleton of a piecewise linear complex in R^3: vertices with
rational coordinates and straight segments that meet only at shared endpoints.
EDGE_PROTECT inserts Steiner points on the segments until every subsegment is
strongly Delaunay: some sphere passes through its two endpoints and has every
other vertex strictly outside. By Shewchuk's CDT theorem the augmented complex
then has a constrained Delaunay tetrahedralization, so its facets can be
recovered with no further Steiner points.

  step 1  at every vertex where two segments meet at less than 90 degrees, cut
          those segments with a sphere of radius r = min(lfs, l/3, 2d/3);
  step 2  split at its midpoint any subsegment that is not strongly Delaunay,
          until none is left.

STRONGLY_DELAUNAY decides the sphere condition exactly. The centre c of a sphere
through a and b lies in their bisector plane, and a vertex p is strictly outside
exactly when |p|^2 - |a|^2 - 2 c.(p - a) > 0, which is linear in c. So the test is
the feasibility of a system of strict linear inequalities in two unknowns, done
by Fourier-Motzkin elimination over Fraction. It returns a witness centre.

The module also builds a Schonhardt polyhedron and tests points against it
exactly, to show the case where no recovery without Steiner points exists.
"""

import math
from fractions import Fraction
from itertools import combinations
from typing import Dict, List, Optional, Sequence, Tuple

Point = Sequence


def sub(a: Point, b: Point) -> tuple:
    return tuple(x - y for x, y in zip(a, b))


def add(a: Point, b: Point) -> tuple:
    return tuple(x + y for x, y in zip(a, b))


def scale(k, a: Point) -> tuple:
    return tuple(k * x for x in a)


def dot(a: Point, b: Point):
    return sum(x * y for x, y in zip(a, b))


def cross(a: Point, b: Point) -> tuple:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dist2(a: Point, b: Point):
    d = sub(a, b)
    return dot(d, d)


def orient(a: Point, b: Point, c: Point, d: Point):
    """Six times the signed volume of abcd: positive if d is above the plane abc,
    seen with a, b, c counterclockwise."""
    return dot(cross(sub(b, a), sub(c, a)), sub(d, a))


def point_seg_dist2(p: Point, a: Point, b: Point) -> Fraction:
    d = sub(b, a)
    t = Fraction(dot(sub(p, a), d), dot(d, d))
    t = min(Fraction(1), max(Fraction(0), t))
    return dist2(p, add(a, scale(t, d)))


def seg_seg_dist2(a: Point, b: Point, c: Point, d: Point) -> Fraction:
    """Exact squared distance between segments ab and cd."""
    u, v, w = sub(b, a), sub(d, c), sub(a, c)
    A, B, C, D, E = dot(u, u), dot(u, v), dot(v, v), dot(u, w), dot(v, w)
    den = A * C - B * B
    best = min(point_seg_dist2(a, c, d), point_seg_dist2(b, c, d),
               point_seg_dist2(c, a, b), point_seg_dist2(d, a, b))
    if den != 0:
        s = Fraction(B * E - C * D, den)
        t = Fraction(A * E - B * D, den)
        if 0 <= s <= 1 and 0 <= t <= 1:
            best = min(best, dist2(add(a, scale(s, u)), add(c, scale(t, v))))
    return best


def check_complex(points: Sequence[Point], segments: Sequence[Tuple[int, int]]) -> None:
    """Raise ValueError unless the segments form a valid 1-complex."""
    pts = [tuple(Fraction(x) for x in p) for p in points]
    if any(len(p) != 3 for p in pts) or len(set(pts)) != len(pts):
        raise ValueError("points must be distinct and three-dimensional")
    seen = set()
    for u, v in segments:
        if not (0 <= u < len(pts) and 0 <= v < len(pts)) or u == v:
            raise ValueError("bad segment")
        key = (min(u, v), max(u, v))
        if key in seen:
            raise ValueError("repeated segment")
        seen.add(key)
        for k, p in enumerate(pts):
            if k not in (u, v) and point_seg_dist2(p, pts[u], pts[v]) == 0:
                raise ValueError("a vertex lies inside a segment")
    segs = list(seen)
    for (u, v), (x, y) in combinations(segs, 2):
        shared = {u, v} & {x, y}
        if not shared:
            if seg_seg_dist2(pts[u], pts[v], pts[x], pts[y]) == 0:
                raise ValueError("segments cross")
        else:
            o = shared.pop()
            p = v if u == o else u
            q = y if x == o else x
            d1, d2 = sub(pts[p], pts[o]), sub(pts[q], pts[o])
            if cross(d1, d2) == (0, 0, 0) and dot(d1, d2) > 0:
                raise ValueError("segments overlap")


def strongly_delaunay(a: Point, b: Point, pts: Sequence[Point]) -> Optional[tuple]:
    """Return the centre of a sphere through a and b that has every point of pts
    other than a and b strictly outside, or None if there is no such sphere."""
    a = tuple(Fraction(x) for x in a)
    b = tuple(Fraction(x) for x in b)
    d = sub(b, a)
    k = min(range(3), key=lambda i: abs(d[i]))
    axis = tuple(1 if i == k else 0 for i in range(3))
    e1 = cross(d, axis)
    e2 = cross(d, e1)
    m = scale(Fraction(1, 2), add(a, b))
    aa = dot(a, a)
    # constraint alpha + beta*s + gamma*t > 0 for the centre m + s*e1 + t*e2
    cons = []
    for p in pts:
        p = tuple(Fraction(x) for x in p)
        if p == a or p == b:
            continue
        pa = sub(p, a)
        cons.append((dot(p, p) - aa - 2 * dot(m, pa), -2 * dot(e1, pa), -2 * dot(e2, pa)))
    lower = [c for c in cons if c[2] > 0]
    upper = [c for c in cons if c[2] < 0]
    flat = [(c[0], c[1]) for c in cons if c[2] == 0]
    for al, bl, gl in lower:  # eliminate t: each lower bound below each upper bound
        for au, bu, gu in upper:
            flat.append((au * gl - al * gu, bu * gl - bl * gu))
    lo, hi = None, None  # open interval for s
    for A, B in flat:
        if B == 0:
            if A <= 0:
                return None
        elif B > 0:
            x = Fraction(-A, 1) / B
            lo = x if lo is None or x > lo else lo
        else:
            x = Fraction(-A, 1) / B
            hi = x if hi is None or x < hi else hi
    if lo is not None and hi is not None and lo >= hi:
        return None
    if lo is None and hi is None:
        s = Fraction(0)
    elif lo is None:
        s = hi - 1
    elif hi is None:
        s = lo + 1
    else:
        s = (lo + hi) / 2
    tl = max((-(al + bl * s) / gl for al, bl, gl in lower), default=None)
    tu = min((-(au + bu * s) / gu for au, bu, gu in upper), default=None)
    if tl is None and tu is None:
        t = Fraction(0)
    elif tl is None:
        t = tu - 1
    elif tu is None:
        t = tl + 1
    else:
        t = (tl + tu) / 2
    c = add(m, add(scale(s, e1), scale(t, e2)))
    r2 = dist2(c, a)
    assert all(dist2(c, p) > r2 for p in pts if tuple(Fraction(x) for x in p) not in (a, b))
    return c


def strongly_delaunay_brute(a: Point, b: Point, pts: Sequence[Point]) -> bool:
    """Reference test by Helly's theorem and Motzkin's transposition theorem.

    The open half-planes {alpha + beta*s + gamma*t > 0} have a common point
    exactly when every three of them do (Helly in the plane), and three fail
    exactly when a nonnegative, nonzero combination of them has zero beta and
    gamma parts and a nonpositive alpha part."""
    a = tuple(Fraction(x) for x in a)
    b = tuple(Fraction(x) for x in b)
    d = sub(b, a)
    k = min(range(3), key=lambda i: abs(d[i]))
    e1 = cross(d, tuple(1 if i == k else 0 for i in range(3)))
    e2 = cross(d, e1)
    m = scale(Fraction(1, 2), add(a, b))
    cons = []
    for p in pts:
        p = tuple(Fraction(x) for x in p)
        if p in (a, b):
            continue
        pa = sub(p, a)
        cons.append((dot(p, p) - dot(a, a) - 2 * dot(m, pa), -2 * dot(e1, pa), -2 * dot(e2, pa)))

    def dead(sub_cons) -> bool:
        n = len(sub_cons)
        # search the nonnegative combinations that cancel beta and gamma
        for size in range(1, n + 1):
            for idx in combinations(range(n), size):
                rows = [sub_cons[i] for i in idx]
                for lam in _kernel_rays(rows):
                    if all(x >= 0 for x in lam) and any(x > 0 for x in lam):
                        if sum(l * r[0] for l, r in zip(lam, rows)) <= 0:
                            return True
        return False

    for triple in combinations(range(len(cons)), min(3, len(cons))):
        if dead([cons[i] for i in triple]):
            return False
    return True


def _kernel_rays(rows):
    """Vectors lam (up to sign) with sum lam_i*(beta_i, gamma_i) = 0, one per
    one-dimensional kernel, for one, two or three rows."""
    n = len(rows)
    B = [r[1] for r in rows]
    G = [r[2] for r in rows]
    out = []
    if n == 1:
        if B[0] == 0 and G[0] == 0:
            out.append((1,))
    elif n == 2:
        if B[0] * G[1] - B[1] * G[0] == 0:
            lam = (B[1], -B[0]) if (B[0], B[1]) != (0, 0) else (G[1], -G[0])
            if lam != (0, 0):
                out.append(lam)
    else:
        lam = cross(tuple(B), tuple(G))
        if lam != (0, 0, 0):
            out.append(lam)
    return out + [tuple(-x for x in lam) for lam in out]


def lfs2(p: Point, points: Sequence[Point], segments: Sequence[Tuple[int, int]]) -> Fraction:
    """Squared local feature size at p: the smallest r^2 such that the ball of
    radius r around p meets two disjoint vertices or segments of the input."""
    feats = [("v", i) for i in range(len(points))] + [("s", s) for s in segments]

    def d2(f):
        if f[0] == "v":
            return dist2(p, points[f[1]])
        u, v = f[1]
        return point_seg_dist2(p, points[u], points[v])

    def verts(f):
        return {f[1]} if f[0] == "v" else set(f[1])

    vals = [d2(f) for f in feats]
    best = None
    for i, j in combinations(range(len(feats)), 2):
        if verts(feats[i]) & verts(feats[j]):
            continue
        x = max(vals[i], vals[j])
        best = x if best is None or x < best else best
    return best


class Protection:
    def __init__(self, points, chains, ends, radii, stats):
        self.points = points  # all vertices, input first, as Fraction tuples
        self.chains = chains  # per input segment, vertex indices from u to v
        self.ends = ends  # set of (i, j) subsegments cut off in step 1
        self.radii2 = radii  # vertex -> squared protecting sphere radius (exact)
        self.radii = {v: math.sqrt(r2) for v, r2 in radii.items()}
        self.stats = stats  # counts of Steiner points by step

    def subsegments(self) -> List[Tuple[int, int]]:
        return [(c[k], c[k + 1]) for c in self.chains for k in range(len(c) - 1)]


def _sqrt_floor(q: Fraction, bits: int = 50) -> Fraction:
    """sqrt(q) exactly when it is rational, else the largest k/2^bits below it."""
    q = Fraction(q)
    rn, rd = math.isqrt(q.numerator), math.isqrt(q.denominator)
    if rn * rn == q.numerator and rd * rd == q.denominator:
        return Fraction(rn, rd)
    return Fraction(math.isqrt(q.numerator * 4 ** bits // q.denominator), 2 ** bits)


def edge_protect(points: Sequence[Point], segments: Sequence[Tuple[int, int]],
                 max_points: int = 2000, check: bool = True) -> Protection:
    if check:
        check_complex(points, segments)
    pts = [tuple(Fraction(x) for x in p) for p in points]
    segs = [(u, v) for u, v in segments]
    inc: Dict[int, List[int]] = {}
    for e, (u, v) in enumerate(segs):
        inc.setdefault(u, []).append(e)
        inc.setdefault(v, []).append(e)

    def other(e, v):
        u, w = segs[e]
        return w if u == v else u

    clipped = set()  # (segment, vertex): the segment is cut by the sphere at vertex
    for v, es in inc.items():
        for e, f in combinations(es, 2):
            if dot(sub(pts[other(e, v)], pts[v]), sub(pts[other(f, v)], pts[v])) > 0:  # @line L1
                clipped.add((e, v))
                clipped.add((f, v))
    len2 = [dist2(pts[u], pts[v]) for u, v in segs]
    radii2: Dict[int, Fraction] = {}  # squared radii, exact
    for v in sorted({v for _, v in clipped}):
        near = [dist2(pts[v], pts[u]) for u in range(len(pts)) if u != v]
        near += [point_seg_dist2(pts[v], pts[a], pts[b]) for a, b in segs if v not in (a, b)]
        ell2 = min(len2[e] for e in inc[v] if (e, v) in clipped)
        cands = near + [Fraction(ell2, 9)]
        cands += [Fraction(4 * len2[e], 9) for e in inc[v] if (e, other(e, v)) in clipped]
        radii2[v] = min(cands)  # @line L2
    chains = []
    ends = set()
    for e, (u, v) in enumerate(segs):
        chain = [u]
        for x, y in ((u, v), (v, u)):
            if (e, x) in clipped:
                lam = _sqrt_floor(Fraction(radii2[x]) / len2[e])
                pts.append(add(pts[x], scale(lam, sub(pts[y], pts[x]))))  # @line L3
                if x == u:
                    chain.append(len(pts) - 1)
                    ends.add((u, len(pts) - 1))
                else:
                    tail = len(pts) - 1
                    ends.add((tail, v))
        if (e, v) in clipped:
            chain.append(tail)
        chain.append(v)
        chains.append(chain)
    step1 = len(pts) - len(points)
    # witness[(i, j)] = (centre, r^2) of an empty sphere through i and j, or None
    witness: Dict[Tuple[int, int], Optional[tuple]] = {}

    def test(i, j):
        c = strongly_delaunay(pts[i], pts[j], pts)
        witness[(i, j)] = None if c is None else (c, dist2(c, pts[i]))

    for c in chains:
        for k in range(len(c) - 1):
            test(c[k], c[k + 1])  # @line L4
    while True:
        bad = next((s for c in chains for s in zip(c, c[1:]) if witness[s] is None), None)  # @line L5
        if bad is None:
            break
        if len(pts) >= max_points:
            raise RuntimeError("too many Steiner points")
        i, j = bad
        pts.append(scale(Fraction(1, 2), add(pts[i], pts[j])))  # @line L6
        m = len(pts) - 1
        for c in chains:
            for k in range(len(c) - 1):
                if (c[k], c[k + 1]) == bad:
                    c.insert(k + 1, m)
                    break
        del witness[bad]
        test(i, m)
        test(m, j)
        for s, w in list(witness.items()):
            if w is not None and dist2(w[0], pts[m]) <= w[1]:
                test(*s)
    stats = {"step1": step1, "step2": len(pts) - len(points) - step1}
    return Protection(pts, chains, ends, radii2, stats)  # @line L7


def schonhardt(R: int = 100, h: int = 100, twist: int = 30):
    """A Schonhardt polyhedron with integer coordinates: a triangular prism whose
    top is turned by `twist` degrees, each side split along its reflex diagonal.

    Returns (points, faces, reflex, outside): faces are outward triangles,
    reflex the three reflex edges, outside the three vertex pairs whose
    segment leaves the polyhedron."""
    pts = []
    for k in range(3):
        t = math.radians(90 + 120 * k)
        pts.append((round(R * math.cos(t)), round(R * math.sin(t)), 0))
    for k in range(3):
        t = math.radians(90 + 120 * k + twist)
        pts.append((round(R * math.cos(t)), round(R * math.sin(t)), h))
    centroid = tuple(Fraction(sum(p[i] for p in pts), 6) for i in range(3))
    faces, reflex, outside = [], [], []
    for k in range(3):
        a0, a1, b0, b1 = k, (k + 1) % 3, 3 + k, 3 + (k + 1) % 3
        # the diagonal a0-b1 is reflex when b0 lies outside the plane of a0 a1 b1
        if orient(pts[a0], pts[a1], pts[b1], pts[b0]) * orient(pts[a0], pts[a1], pts[b1], centroid) < 0:
            diag, other_pair, tris = (a0, b1), (a1, b0), [(a0, a1, b1), (a0, b1, b0)]
        else:
            diag, other_pair, tris = (a1, b0), (a0, b1), [(a0, a1, b0), (a1, b1, b0)]
        reflex.append(diag)
        outside.append(other_pair)
        faces.extend(tris)
    faces.append((0, 2, 1))
    faces.append((3, 4, 5))
    # orient every face outward, using the centroid, which sees every face
    out = []
    for f in faces:
        if orient(pts[f[0]], pts[f[1]], pts[f[2]], centroid) > 0:
            f = (f[0], f[2], f[1])
        out.append(f)
    return pts, out, reflex, outside


def edges_of(faces) -> set:
    return {tuple(sorted((f[i], f[(i + 1) % 3]))) for f in faces for i in range(3)}


def inside_polyhedron(q: Point, pts: Sequence[Point], faces) -> bool:
    """Exact ray-parity test for a point not on the boundary."""
    q = tuple(Fraction(x) for x in q)
    for r in ((1, Fraction(3, 7), Fraction(5, 11)), (Fraction(2, 13), 1, Fraction(7, 17)),
              (Fraction(5, 19), Fraction(3, 23), 1)):
        hits, degenerate = 0, False
        for f in faces:
            p0, p1, p2 = (pts[i] for i in f)
            n = cross(sub(p1, p0), sub(p2, p0))
            den = dot(n, r)
            if den == 0:
                continue
            t = Fraction(dot(n, sub(p0, q))) / den
            if t <= 0:
                if t == 0:
                    degenerate = True
                continue
            x = add(q, scale(t, r))
            s = [dot(n, cross(sub(pts[f[(i + 1) % 3]], pts[f[i]]), sub(x, pts[f[i]]))) for i in range(3)]
            if any(v == 0 for v in s):
                degenerate = True
                break
            if all(v > 0 for v in s):
                hits += 1
        if not degenerate:
            return hits % 2 == 1
    raise ValueError("point on the boundary or degenerate rays")
