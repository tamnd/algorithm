# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/theta-star/. The authors are listed in prov/1ZY6ZC.jsonl.

"""Basic Theta* (Nash, Daniel, Koenig and Felner) on a grid of square cells.

The vertices are the corners of the cells: (x, y) with 0 <= x <= w and
0 <= y <= h, and cell (i, j) is the unit square from corner (i, j) to corner
(i + 1, j + 1). The obstacle is the interior of the union of the blocked
cells, and everything outside the map counts as blocked. A segment between
two corners has line of sight if it does not meet that interior. Theta*
searches the 8-connected graph of corners like A*, but when it reaches a
neighbour y from x, it first tries to connect y straight to the parent of x.
"""

import heapq
import math


class Grid:
    def __init__(self, rows: list[str]):
        """rows[j][i] is '#' for a blocked cell (i, j) and any other character for a free cell."""
        self.rows = rows
        self.h = len(rows)
        self.w = len(rows[0]) if rows else 0

    def blocked(self, i: int, j: int) -> bool:
        return not (0 <= i < self.w and 0 <= j < self.h) or self.rows[j][i] == "#"

    def corner(self, x: int, y: int) -> bool:
        return 0 <= x <= self.w and 0 <= y <= self.h


def line_of_sight(grid: Grid, a: tuple[int, int], b: tuple[int, int]) -> bool:
    """True if the segment from corner a to corner b does not meet the interior of the obstacle."""
    (x0, y0), (x1, y1) = a, b
    if x0 == x1 or y0 == y1:  # @line L11
        if x0 == x1:  # a vertical segment: the cells left and right of each unit edge
            return not any(grid.blocked(x0 - 1, y) and grid.blocked(x0, y) for y in range(min(y0, y1), max(y0, y1)))
        return not any(grid.blocked(x, y0 - 1) and grid.blocked(x, y0) for x in range(min(x0, x1), max(x0, x1)))
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    dx, dy = x1 - x0, y1 - y0
    for i in range(x0, x1):  # @line L12
        # The segment over the strip i <= x <= i + 1 has y between n1 / dx and n2 / dx.
        n1 = y0 * dx + (i - x0) * dy
        n2 = n1 + dy
        lo, hi = min(n1, n2), max(n1, n2)
        for j in range(lo // dx, -(-hi // dx)):  # @line L13
            if grid.blocked(i, j):  # @line L14
                return False
    return True  # @line L15


def dist(a: tuple[int, int], b: tuple[int, int]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))


def theta_star(grid: Grid, start: tuple[int, int], goal: tuple[int, int]):
    """Return (the list of path corners, its length), or (None, None) if the goal cannot be reached."""
    if not (grid.corner(*start) and grid.corner(*goal)):
        raise ValueError("start and goal must be corners of the grid")
    g = {start: 0.0}  # @line L1
    parent = {start: start}
    heap = [(dist(start, goal), 0, start)]
    closed = set()
    tie = 0
    while heap:  # @line L2
        _, _, x = heapq.heappop(heap)  # @line L3
        if x in closed:
            continue
        closed.add(x)
        if x == goal:  # @line L4
            path = [x]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return path[::-1], g[x]
        for dx, dy in NEIGHBOURS:  # @line L5
            y = (x[0] + dx, x[1] + dy)
            if not grid.corner(*y) or y in closed or not line_of_sight(grid, x, y):
                continue
            p = parent[x]  # @line L6
            if line_of_sight(grid, p, y):  # @line L7
                cand, par = g[p] + dist(p, y), p  # @line L8
            else:
                cand, par = g[x] + dist(x, y), x  # @line L9
            if cand < g.get(y, math.inf):
                g[y] = cand
                parent[y] = par
                tie += 1
                heapq.heappush(heap, (cand + dist(y, goal), tie, y))
    return None, None  # @line L10
