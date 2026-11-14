# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direction-parallel-toolpath/. The authors are listed in prov/ZR545D.jsonl.

"""Direction-parallel (zigzag) toolpath with exact rational geometry.

The input is the region C where the tool center may go, a polygon with holes
given as a list of rings. A point is in C by the even-odd rule, and C is closed
(its boundary belongs to it). In a CAM system C is the inward offset of the
pocket by the tool radius r, so the tool cuts C plus a disk of radius r.

The passes lie on the horizontal lines y = ymin + s/2 + k s. Each line meets C
in closed intervals. Greedy linking joins an interval to an unused interval on
the next line by a straight segment, but only if that segment lies in C.
When no link is possible, the tool retracts and a new zigzag starts at the
lowest unused interval. A last pass runs around every ring of C.

All coordinates are int or Fraction, and every test is exact.
"""

from fractions import Fraction

Point = tuple[Fraction, Fraction]


def _norm(rings):
    out = []
    for ring in rings:
        pts = [(Fraction(x), Fraction(y)) for x, y in ring]
        if len(pts) < 3:
            raise ValueError("a ring needs at least 3 vertices")
        out.append(pts)
    if not out:
        raise ValueError("the region needs at least one ring")
    return out


def edges(rings):
    for ring in rings:
        m = len(ring)
        for i in range(m):
            yield ring[i], ring[(i + 1) % m]


def cross(o: Point, a: Point, b: Point) -> Fraction:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def on_segment(p: Point, a: Point, b: Point) -> bool:
    return (cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def crossings(rings, y) -> list[Fraction]:
    """x of the edges that cross the line at height y, by the half-open rule."""
    xs = []
    for (x0, y0), (x1, y1) in edges(rings):
        if (y0 <= y < y1) or (y1 <= y < y0):
            xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
    xs.sort()
    return xs


def in_region(rings, p: Point) -> bool:
    """Closed point-in-polygon test: boundary points count as inside."""
    if any(on_segment(p, a, b) for a, b in edges(rings)):
        return True
    return sum(1 for x in crossings(rings, p[1]) if x > p[0]) % 2 == 1


def intervals(rings, y) -> list[tuple[Fraction, Fraction]]:
    """The intervals of the line at height y inside C, without the points of zero length."""
    xs = crossings(rings, y)
    return [(xs[i], xs[i + 1]) for i in range(0, len(xs), 2) if xs[i] < xs[i + 1]]


def segment_in_region(rings, a: Point, b: Point) -> bool:
    """True if the closed segment ab lies in C.

    The segment is cut at every point where it meets an edge, including the
    ends of collinear overlaps. Each open piece then lies wholly inside or
    wholly outside, so the test of its midpoint decides it.
    """
    if not (in_region(rings, a) and in_region(rings, b)):
        return False
    d = (b[0] - a[0], b[1] - a[1])
    dd = d[0] * d[0] + d[1] * d[1]
    if dd == 0:
        return True
    ts = {Fraction(0), Fraction(1)}
    for c, e in edges(rings):
        f = (e[0] - c[0], e[1] - c[1])
        den = d[0] * f[1] - d[1] * f[0]
        w = (c[0] - a[0], c[1] - a[1])
        if den != 0:
            t = (w[0] * f[1] - w[1] * f[0]) / den
            u = (w[0] * d[1] - w[1] * d[0]) / den
            if 0 <= t <= 1 and 0 <= u <= 1:
                ts.add(t)
        elif cross(a, b, c) == 0:
            for q in (c, e):
                t = ((q[0] - a[0]) * d[0] + (q[1] - a[1]) * d[1]) / dd
                if 0 <= t <= 1:
                    ts.add(t)
    ts = sorted(ts)
    for t0, t1 in zip(ts, ts[1:]):
        m = (t0 + t1) / 2
        if not in_region(rings, (a[0] + m * d[0], a[1] + m * d[1])):
            return False
    return True


def scanlines(rings, s):
    """The pass lines y_k = ymin + s/2 + k s below ymax, each with its intervals."""
    ys = [p[1] for ring in rings for p in ring]
    ymin, ymax = min(ys), max(ys)
    lines = []
    y = ymin + s / 2
    while y < ymax:
        lines.append((y, intervals(rings, y)))
        y += s
    return lines


def direction_parallel(rings, s, contour=True) -> list[list[Point]]:
    """The strokes of a zigzag toolpath; the tool retracts between strokes.

    Each stroke is a polyline that the tool center follows without lifting.
    With contour=False the last pass around the rings is left out, which is
    only useful to show what goes wrong without it.
    """
    rings = _norm(rings)
    s = Fraction(s)
    if s <= 0:
        raise ValueError("the step-over must be positive")
    lines = scanlines(rings, s)  # @line L1
    used = [[False] * len(iv) for _, iv in lines]
    strokes = []
    while True:  # @line L2
        start = next(((k, j) for k in range(len(lines)) for j in range(len(lines[k][1]))
                      if not used[k][j]), None)
        if start is None:
            break
        k, j = start  # @line L3
        stroke = [(lines[k][1][j][0], lines[k][0])]
        rightward = True
        while True:  # @line L4
            used[k][j] = True  # @line L5
            lo, hi = lines[k][1][j]
            end = (hi, lines[k][0]) if rightward else (lo, lines[k][0])
            stroke.append(end)
            if k + 1 == len(lines):
                break
            ny, niv = lines[k + 1]
            cands = []
            for jj, (a, b) in enumerate(niv):  # @line L6
                if not used[k + 1][jj]:
                    q = (b, ny) if rightward else (a, ny)
                    cands.append((abs(q[0] - end[0]), jj, q))
            cands.sort()
            nxt = next(((jj, q) for _, jj, q in cands if segment_in_region(rings, end, q)), None)
            if nxt is None:  # @line L7
                break
            jj, q = nxt  # @line L8
            stroke.append(q)
            k, j = k + 1, jj
            rightward = not rightward
        strokes.append(stroke)
    if contour:
        for ring in rings:  # @line L9
            strokes.append(ring + [ring[0]])
    return strokes  # @line L10


def path_segments(strokes) -> list[tuple[Point, Point]]:
    """The segments that the tool center cuts along."""
    return [(st[i], st[i + 1]) for st in strokes for i in range(len(st) - 1)]
