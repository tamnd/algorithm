# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sutherland-hodgman/. The authors are listed in prov/2W87VM.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def orient(p: Point, q: Point, r: Point) -> Number:
    """Twice the signed area of pqr: positive when r is to the left of the line pq."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def line_intersection(p: Point, s: Point, c: Point, d: Point) -> Point:
    """The point where the segment ps crosses the line cd. Requires p and s on opposite sides."""
    op, os_ = orient(c, d, p), orient(c, d, s)
    t = Fraction(op) / (op - os_)
    return (p[0] + t * (s[0] - p[0]), p[1] + t * (s[1] - p[1]))


def clip_half_plane(poly: Sequence[Point], c: Point, d: Point) -> list[Point]:
    """Clip a closed polygon to the closed half-plane to the left of the directed line cd."""
    out: list[Point] = []  # @line L3
    m = len(poly)
    for i in range(m):  # @line L4
        p, s = poly[i - 1], poly[i]  # @line L5
        sp, ss = orient(c, d, p), orient(c, d, s)
        if (sp > 0 and ss < 0) or (sp < 0 and ss > 0):  # @line L6
            out.append(line_intersection(p, s, c, d))
        if ss >= 0:  # @line L7
            out.append(s)
    return out


def is_convex_ccw(poly: Sequence[Point]) -> bool:
    """True when poly, of positive signed area, is convex: it never turns right, never reverses,
    and its edge directions turn around exactly once. Time O(m)."""
    pts = [p for i, p in enumerate(poly) if p != poly[i - 1]]
    m = len(pts)
    if m < 3:
        return False
    dirs = [(pts[(i + 1) % m][0] - pts[i][0], pts[(i + 1) % m][1] - pts[i][1]) for i in range(m)]
    for i in range(m):
        (ax, ay), (bx, by) = dirs[i - 1], dirs[i]
        cr = ax * by - ay * bx
        if cr < 0 or (cr == 0 and ax * bx + ay * by < 0):
            return False
    signs = [1 if dy > 0 else -1 for _, dy in dirs if dy != 0]
    changes = sum(1 for i in range(len(signs)) if signs[i] != signs[i - 1])
    return changes == 2


def sutherland_hodgman(subject: Sequence[Point], clip: Sequence[Point]) -> list[Point]:
    """Clip the subject polygon to the convex clip polygon.

    subject is any closed polygon (it may be concave or self-intersecting). clip must be a convex
    polygon with nonzero area, in either orientation. The result is one closed polygon, possibly
    empty, whose winding number is that of the subject at every point inside the clip polygon and
    0 at every point outside it (points on the boundaries aside). When the subject is concave the
    result can contain edges of zero width along the clip boundary. Time O(n m) for n subject
    vertices and m clip vertices; coordinates of the output are exact Fractions or ints.
    """
    m = len(clip)
    if m < 3:
        raise ValueError("the clip polygon needs at least 3 vertices")
    area2 = sum(clip[i][0] * clip[(i + 1) % m][1] - clip[(i + 1) % m][0] * clip[i][1] for i in range(m))
    if area2 == 0:
        raise ValueError("the clip polygon has zero area")
    window = list(clip) if area2 > 0 else list(reversed(clip))
    if not is_convex_ccw(window):
        raise ValueError("the clip polygon is not convex")
    out = list(subject)  # @line L1
    for i in range(m):  # @line L2
        if not out:
            break
        out = clip_half_plane(out, window[i], window[(i + 1) % m])
    return out  # @line L8
