# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shifting-technique/. The authors are listed in prov/MCW6TZ.jsonl.

"""The shifting technique of Hochbaum and Maass for covering points with closed unit squares [x, x+1] x [y, y+1].

The strip boundaries are integer lines; shift s uses the lines c with c = s (mod l). A point with coordinate t
belongs to the strip [b, b + l) with b <= t < b + l. Coordinates are ints or Fractions."""

from math import floor
from typing import Callable, Optional, Sequence

Point = tuple
Square = tuple  # the lower left corner (x, y) of [x, x + 1] x [y, y + 1]


def covers(q: Square, p: Point) -> bool:
    return q[0] <= p[0] <= q[0] + 1 and q[1] <= p[1] <= q[1] + 1


def cover_exact(points: Sequence[Point], stats: Optional[dict] = None) -> list[Square]:
    """A least set of unit squares that covers the points, by branch and bound.

    The uncovered point p with the least (x, y) is covered by some square. That square can be moved so that its left
    side is at x = p.x and its bottom side is at the least y of the uncovered points it covers; it still covers them.
    So the branches are the squares (p.x, y) for the y values of uncovered points in [p.y - 1, p.y]."""
    pts = sorted(set(points))
    best: list[list[Square]] = [[(p[0], p[1]) for p in pts]]
    nodes = 0
    stack: list[tuple[tuple[Point, ...], list[Square]]] = [(tuple(pts), [])]
    while stack:
        rest, chosen = stack.pop()
        nodes += 1
        if not rest:
            if len(chosen) < len(best[0]):
                best[0] = chosen
            continue
        if len(chosen) + 1 >= len(best[0]):
            continue
        p = rest[0]
        for y in sorted({q[1] for q in rest if p[1] - 1 <= q[1] <= p[1]}):
            sq = (p[0], y)
            stack.append((tuple(q for q in rest if not covers(sq, q)), chosen + [sq]))
    if stats is not None:
        stats["nodes"] = stats.get("nodes", 0) + nodes
    return best[0]


def strips(points: Sequence[Point], ell: int, shift: int, axis: int) -> list[list[Point]]:
    """The non-empty groups of points by the strip [b, b + ell) along axis, with b = shift (mod ell)."""
    groups: dict[int, list[Point]] = {}
    for p in points:
        groups.setdefault(floor((p[axis] - shift) / ell), []).append(p)  # @line L3
    return [groups[g] for g in sorted(groups)]


def shift_and_solve(points: Sequence[Point], ell: int, axis: int,
                    solve: Callable[[list[Point]], list[Square]]) -> tuple[list[Square], list[int]]:
    """The shifting lemma: try the ell shifts, solve each strip with solve, keep the best union.

    Return (the best cover, the cost of each shift)."""
    best: Optional[list[Square]] = None
    costs = []
    for s in range(ell):  # @line L1
        cover = []
        for group in strips(points, ell, s, axis):  # @line L2
            cover.extend(solve(group))  # @line L4
        costs.append(len(cover))
        if best is None or len(cover) < len(best):  # @line L5
            best = cover
    return best or [], costs  # @line L6


def shifting_cover(points: Sequence[Point], ell: int, stats: Optional[dict] = None) -> list[Square]:
    """Hochbaum-Maass for unit squares in the plane: shift vertical strips, inside each strip shift horizontal strips,
    and solve each ell x ell cell exactly. At most (1 + 1/ell)^2 OPT squares."""
    def solve_strip(group: list[Point]) -> list[Square]:
        return shift_and_solve(group, ell, 1, lambda cell: cover_exact(cell, stats))[0]
    return shift_and_solve(points, ell, 0, solve_strip)[0]
