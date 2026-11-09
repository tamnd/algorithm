# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weiler-atherton-algorithm/. The authors are listed in prov/TS2VAV.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]


def orient(p: Point, q: Point, r: Point) -> Number:
    """Twice the signed area of pqr: positive when r is to the left of the line pq."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def on_segment(a: Point, b: Point, q: Point) -> bool:
    return (
        orient(a, b, q) == 0
        and min(a[0], b[0]) <= q[0] <= max(a[0], b[0])
        and min(a[1], b[1]) <= q[1] <= max(a[1], b[1])
    )


def segments_meet(a: Point, b: Point, c: Point, d: Point) -> bool:
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0)) and ((o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0)):
        return True
    return on_segment(a, b, c) or on_segment(a, b, d) or on_segment(c, d, a) or on_segment(c, d, b)


def twice_area(poly: Sequence[Point]) -> Number:
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))


def is_simple(poly: Sequence[Point]) -> bool:
    """All-pairs test: distinct vertices, adjacent edges meet only at their shared vertex,
    other edges do not meet, and the area is nonzero. Time O(n^2)."""
    n = len(poly)
    if n < 3 or len(set(poly)) < n or twice_area(poly) == 0:
        return False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for j in range(i + 1, n):
            c, d = poly[j], poly[(j + 1) % n]
            if j == i + 1:
                if on_segment(a, b, d) or on_segment(c, d, a):
                    return False
            elif i == 0 and j == n - 1:
                if on_segment(a, b, c) or on_segment(c, d, b):
                    return False
            elif segments_meet(a, b, c, d):
                return False
    return True


def inside(poly: Sequence[Point], q: Point) -> bool:
    """Strict point in polygon by crossing parity, for q not on the boundary."""
    result = False
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if (a[1] > q[1]) != (b[1] > q[1]):
            if (orient(a, b, q) > 0) == (b[1] > a[1]):
                result = not result
    return result


def weiler_atherton(subject: Sequence[Point], clip: Sequence[Point], op: str = "intersection") -> list[list[Point]]:
    """Boolean operation of two simple polygons by walking their boundaries.

    op is "intersection", "union" or "difference" (subject minus clip). Both inputs must be
    simple; either orientation is accepted. The algorithm assumes general position: no vertex
    of one polygon lies on the boundary of the other, so the boundaries meet only in proper
    crossings. Inputs that break this raise ValueError. The result is a list of closed
    contours, outer boundaries counterclockwise and holes clockwise, so the sum of their
    winding numbers is 1 inside the result and 0 outside. Time O(n m + k log k) for n and m
    vertices and k crossings.
    """
    if op not in ("intersection", "union", "difference"):
        raise ValueError("unknown operation")
    if not is_simple(subject) or not is_simple(clip):
        raise ValueError("both polygons must be simple")
    S = list(subject) if twice_area(subject) > 0 else list(reversed(subject))
    C = list(clip) if twice_area(clip) > 0 else list(reversed(clip))
    n, m = len(S), len(C)
    for q in S:
        if any(on_segment(C[j], C[(j + 1) % m], q) for j in range(m)):
            raise ValueError("a subject vertex lies on the clip boundary")
    for q in C:
        if any(on_segment(S[i], S[(i + 1) % n], q) for i in range(n)):
            raise ValueError("a clip vertex lies on the subject boundary")

    # Crossings of every subject edge with every clip edge.
    points: list[Point] = []  # @line L1
    entering: list[bool] = []
    on_s: list[list[tuple[Fraction, int]]] = [[] for _ in range(n)]
    on_c: list[list[tuple[Fraction, int]]] = [[] for _ in range(m)]
    for i in range(n):
        a, b = S[i], S[(i + 1) % n]
        for j in range(m):
            c, d = C[j], C[(j + 1) % m]
            if not segments_meet(a, b, c, d):
                continue
            den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
            t = Fraction((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0]), den)
            u = Fraction((c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0]), den)
            k = len(points)
            points.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
            # The subject edge enters the clip polygon when it points to the left of the clip edge.
            entering.append(den < 0)  # @line L2
            on_s[i].append((t, k))
            on_c[j].append((u, k))

    if not points:  # @line L3
        s_in_c, c_in_s = inside(C, S[0]), inside(S, C[0])
        if op == "intersection":
            return [S] if s_in_c else [C] if c_in_s else []
        if op == "union":
            return [C] if s_in_c else [S] if c_in_s else [S, C]
        return [] if s_in_c else [S, C[::-1]] if c_in_s else [S]

    # The two vertex lists with the crossings inserted in order along each edge.
    def build(poly, cuts):
        nodes, pos = [], {}
        for i, p in enumerate(poly):
            nodes.append((p, -1))
            for _, k in sorted(cuts[i]):
                pos[k] = len(nodes)
                nodes.append((points[k], k))
        return nodes, pos

    s_nodes, s_pos = build(S, on_s)  # @line L4
    c_nodes, c_pos = build(C, on_c)
    c_step = -1 if op == "difference" else 1
    start_on_entry = op == "intersection"

    result: list[list[Point]] = []
    visited = [False] * len(points)
    for k0 in range(len(points)):  # @line L5
        if visited[k0] or entering[k0] != start_on_entry:
            continue
        contour: list[Point] = []
        k, on_subject = k0, True
        while True:
            visited[k] = True  # @line L6
            contour.append(points[k])
            nodes, pos, step = (s_nodes, s_pos, 1) if on_subject else (c_nodes, c_pos, c_step)
            idx = (pos[k] + step) % len(nodes)
            while nodes[idx][1] < 0:  # @line L7
                contour.append(nodes[idx][0])
                idx = (idx + step) % len(nodes)
            k = nodes[idx][1]
            if k == k0:  # @line L8
                break
            on_subject = not on_subject  # @line L9
        result.append(contour)
    return result  # @line L10
