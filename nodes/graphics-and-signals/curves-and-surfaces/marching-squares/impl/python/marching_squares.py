# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marching-squares/. The authors are listed in prov/YVD13Y.jsonl.

"""Marching squares: the contour f = c of a sampled 2D field, one cell at a time.

The field is a list of rows: grid[j][i] is the sample at the point (i, j).
A sample is "inside" when it is less than the iso value c, and "outside"
when it is at least c. Each cell gets a 4-bit case number from its corners,
and a 16-entry table gives the segments of the case. The two saddle cases
(5 and 10) are decided with the asymptotic decider, which reads the saddle
value of the bilinear interpolant of the cell. With int or Fraction samples
and iso value, every crossing point is an exact Fraction.
"""

from fractions import Fraction
from typing import Union

Number = Union[int, float, Fraction]
Point = tuple[Number, Number]
Segment = tuple[Point, Point]

# Corners of cell (i, j), counted counterclockwise in the (x, y) plane:
# 0 = (i, j), 1 = (i + 1, j), 2 = (i + 1, j + 1), 3 = (i, j + 1).
CORNER = ((0, 0), (1, 0), (1, 1), (0, 1))
# Edge e joins corner e and corner e + 1 (mod 4): 0 bottom, 1 right, 2 top, 3 left.
EDGE = ((0, 1), (1, 2), (2, 3), (3, 0))

# For each case, the segments as (edge, edge) pairs, oriented so that the
# inside lies on the left of each segment. Bit k of the case is set when
# corner k is inside. Cases 5 and 10 have two entries: index 0 when the two
# inside corners are separated, index 1 when they are joined.
TABLE: dict[int, tuple[tuple[int, int], ...]] = {
    0: (),
    1: ((0, 3),),
    2: ((1, 0),),
    3: ((1, 3),),
    4: ((2, 1),),
    6: ((2, 0),),
    7: ((2, 3),),
    8: ((3, 2),),
    9: ((0, 2),),
    11: ((1, 2),),
    12: ((3, 1),),
    13: ((0, 1),),
    14: ((3, 0),),
    15: (),
}
SADDLE = {
    5: (((0, 3), (2, 1)), ((0, 1), (2, 3))),
    10: (((1, 0), (3, 2)), ((1, 2), (3, 0))),
}


def _lerp(pa: Point, pb: Point, fa: Number, fb: Number, c: Number) -> Point:
    """The point where the linear interpolant from (pa, fa) to (pb, fb) equals c."""
    if isinstance(fa, float) or isinstance(fb, float) or isinstance(c, float):
        t: Number = (c - fa) / (fb - fa)
    else:
        t = Fraction(c - fa) / (fb - fa)  # @line L13
    return (pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1]))  # @line L14


def saddle_joins_inside(f0: Number, f1: Number, f2: Number, f3: Number, c: Number) -> bool:
    """Asymptotic decider for a saddle cell with corner values f0..f3 (counterclockwise).

    The bilinear interpolant has its saddle value (f0 f2 - f1 f3) / (f0 + f2 - f1 - f3).
    Return True when the inside corners 0 and 2 (case 5) or 1 and 3 (case 10) are
    joined, that is when the saddle value is below c. A saddle value equal to c is
    counted as outside, the same rule as for samples.
    """
    den = f0 + f2 - f1 - f3
    num = f0 * f2 - f1 * f3
    # saddle < c  <=>  num / den < c ; den is never 0 in a saddle case.
    return num < c * den if den > 0 else num > c * den


def marching_squares(grid: list[list[Number]], c: Number) -> list[Segment]:
    """Return the oriented contour segments of the level set grid = c.

    Precondition: grid is a rectangle of at least 2 by 2 numbers. The result lists
    each segment once, with the inside (values below c) on its left. A segment
    endpoint lies on a cell edge whose two samples are on different sides of c,
    and segments of neighboring cells share their endpoints exactly.
    Cost: O(W H) time for a W by H grid, and O(W H) space for the output.
    """
    h = len(grid)
    w = len(grid[0])
    out: list[Segment] = []  # @line L1
    for j in range(h - 1):  # @line L2
        for i in range(w - 1):  # @line L3
            f = [grid[j + dy][i + dx] for dx, dy in CORNER]  # @line L4
            case = sum(1 << k for k in range(4) if f[k] < c)  # @line L5
            if case in SADDLE:  # @line L6
                joined = saddle_joins_inside(*f, c)  # @line L7
                pairs = SADDLE[case][1 if joined else 0]  # @line L8
            else:
                pairs = TABLE[case]  # @line L9
            for ea, eb in pairs:  # @line L10
                pts = []
                for e in (ea, eb):
                    a, b = EDGE[e]
                    pa = (i + CORNER[a][0], j + CORNER[a][1])
                    pb = (i + CORNER[b][0], j + CORNER[b][1])
                    pts.append(_lerp(pa, pb, f[a], f[b], c))
                out.append((pts[0], pts[1]))  # @line L11
    return out  # @line L12


def chain_loops(segments: list[Segment]) -> list[list[Point]]:
    """Join oriented segments into polylines that follow the segment directions.

    A closed contour comes back as a list whose first and last points are equal.
    Precondition: each point starts at most one segment and ends at most one.
    """
    nxt = {a: b for a, b in segments}
    starts = set(nxt) - set(nxt.values())
    out: list[list[Point]] = []
    seen: set[Point] = set()
    for s in list(starts) + list(nxt):
        if s in seen:
            continue
        line = [s]
        seen.add(s)
        p = s
        while p in nxt:
            p = nxt[p]
            line.append(p)
            if p in seen:
                break
            seen.add(p)
        out.append(line)
    return out
