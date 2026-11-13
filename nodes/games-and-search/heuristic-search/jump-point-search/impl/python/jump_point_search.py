# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jump-point-search/. The authors are listed in prov/RQYJH2.jsonl.

"""Jump point search (Harabor and Grastien) on an 8-connected grid without corner cutting.

A straight move costs 1 and a diagonal move costs sqrt(2). A diagonal move
from (x, y) to (x + dx, y + dy) is allowed only if the target and both cells
(x + dx, y) and (x, y + dy) are free. The search is A* over jump points: from a
node it tries only the pruned directions, and in each direction it scans until
it finds the goal, a cell with a forced neighbour, or (for a diagonal scan) a
cell from which a straight scan finds one of these.

A node is a pair (cell, direction of arrival), so that two arrivals at the
same cell from different directions keep their own pruned directions. A cost
is a pair (a, b) that stands for a + b * sqrt(2); this keeps cost comparisons
of the tests exact.
"""

import heapq
import math

SQRT2 = math.sqrt(2)
DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))


class Grid:
    def __init__(self, rows: list[str]):
        """rows[y][x] is '#' for a wall and any other character for a free cell."""
        self.rows = rows
        self.h = len(rows)
        self.w = len(rows[0]) if rows else 0

    def free(self, x: int, y: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h and self.rows[y][x] != "#"

    def can_move(self, x: int, y: int, dx: int, dy: int) -> bool:
        """The move from a free cell (x, y) by (dx, dy), with no corner cutting."""
        if not self.free(x + dx, y + dy):
            return False
        if dx and dy:
            return self.free(x + dx, y) and self.free(x, y + dy)
        return True


def value(cost: tuple[int, int]) -> float:
    return cost[0] + cost[1] * SQRT2


def octile(a: tuple[int, int], b: tuple[int, int]) -> float:
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return SQRT2 * min(dx, dy) + abs(dx - dy)


def forced_moves(grid: Grid, x: int, y: int, d: tuple[int, int]) -> list[tuple[int, int]]:
    """The forced moves of a straight arrival at (x, y) in direction d."""
    dx, dy = d
    out = []
    for qx, qy in ((dy, dx), (-dy, -dx)):  # the two perpendicular directions
        if not grid.free(x - dx + qx, y - dy + qy) and grid.free(x + qx, y + qy):
            out.append((qx, qy))
            if grid.can_move(x, y, dx + qx, dy + qy):
                out.append((dx + qx, dy + qy))
    return out


def pruned(grid: Grid, x: int, y: int, d) -> list[tuple[int, int]]:
    if d is None:  # @line L10
        return [m for m in DIRECTIONS if grid.can_move(x, y, *m)]
    dx, dy = d
    if dx and dy:  # @line L11
        return [m for m in (d, (dx, 0), (0, dy)) if grid.can_move(x, y, *m)]
    natural = [d] if grid.can_move(x, y, dx, dy) else []  # @line L12
    return natural + forced_moves(grid, x, y, d)


def jump(grid: Grid, x: int, y: int, m: tuple[int, int], goal: tuple[int, int]):
    """Scan from (x, y) in direction m. Return the jump point and the number of steps, or None."""
    dx, dy = m
    steps = 0
    while True:  # @line L13
        if not grid.can_move(x, y, dx, dy):  # @line L14
            return None
        x, y = x + dx, y + dy  # @line L15
        steps += 1
        if (x, y) == goal:  # @line L16
            return (x, y), steps
        if not (dx and dy) and forced_moves(grid, x, y, m):  # @line L17
            return (x, y), steps
        if dx and dy and (jump(grid, x, y, (dx, 0), goal) or jump(grid, x, y, (0, dy), goal)):  # @line L18
            return (x, y), steps


def jump_point_search(grid: Grid, start: tuple[int, int], goal: tuple[int, int]):
    """Return (the list of jump points from start to goal, the cost pair (a, b)), or (None, None).

    Also return the number of expanded nodes as a third value.
    """
    if not (grid.free(*start) and grid.free(*goal)):
        raise ValueError("start and goal must be free cells")
    root = (start, None)
    g = {root: (0, 0)}  # @line L1
    parent = {root: None}
    heap = [(octile(start, goal), 0, root)]
    closed = set()
    tie = 0
    expanded = 0
    while heap:  # @line L2
        _, _, node = heapq.heappop(heap)  # @line L3
        if node in closed:
            continue
        closed.add(node)
        expanded += 1
        cell, d = node
        if cell == goal:  # @line L4
            path = []
            while node is not None:
                path.append(node[0])
                node = parent[node]
            return path[::-1], g[(cell, d)], expanded
        for m in pruned(grid, cell[0], cell[1], d):  # @line L5
            found = jump(grid, cell[0], cell[1], m, goal)  # @line L6
            if found is None:
                continue
            y, steps = found
            a, b = g[node]
            new = (a + steps, b) if not (m[0] and m[1]) else (a, b + steps)
            child = (y, m)
            if child not in g or value(new) < value(g[child]):  # @line L7
                g[child] = new  # @line L8
                parent[child] = node
                tie += 1
                heapq.heappush(heap, (value(new) + octile(y, goal), tie, child))
    return None, None, expanded  # @line L9


def expand(path: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """The cells of the grid path between consecutive jump points."""
    cells = [path[0]]
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        dx = (x1 > x0) - (x1 < x0)
        dy = (y1 > y0) - (y1 < y0)
        x, y = x0, y0
        while (x, y) != (x1, y1):
            x, y = x + dx, y + dy
            cells.append((x, y))
    return cells
