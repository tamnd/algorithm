# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prioritized-multi-robot-planning/. The authors are listed in prov/9VT1PP.jsonl.

"""Prioritized multi-robot planning on a grid (Erdmann and Lozano-Perez 1987).

The grid is a list of strings; '#' is an obstacle and any other character is a
free cell. Cells are (row, col). Time is discrete: in each step a robot moves to
one of the 4 neighbor cells or waits. Two robots must never be in the same cell
at the same time (vertex conflict) and must never swap cells in one step (edge
conflict). A robot that reaches its goal stays there for ever.

The robots are planned one at a time in priority order. Robot i runs a
space-time A* search that treats the plans of robots planned before it as moving
obstacles. The method is not complete: it can report no plan for an instance
that has one.
"""

import heapq
from typing import Optional, Sequence

Cell = tuple
MOVES = ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))


def free_cells(grid: Sequence[str]) -> list:
    return [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch != "#"]


def neighbors(grid: Sequence[str], cell: Cell) -> list:
    """The cells a robot can be in after one step: wait, or move by one cell."""
    out = []
    for dr, dc in MOVES:
        r, c = cell[0] + dr, cell[1] + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[r]) and grid[r][c] != "#":
            out.append((r, c))
    return out


class Reservations:
    """The space-time cells and moves used by the robots planned so far."""

    def __init__(self):
        self.vertex = {}  # (cell, t) -> robot
        self.moves = set()  # (from cell, to cell, t): a move from time t to t + 1
        self.parked = {}  # cell -> first time from which a robot stays there
        self.last_use = {}  # cell -> last time t with a vertex reservation

    def add(self, path: list) -> None:
        for t, cell in enumerate(path):
            self.vertex[(cell, t)] = True
            self.last_use[cell] = max(self.last_use.get(cell, -1), t)
            if t > 0:
                self.moves.add((path[t - 1], cell, t - 1))
        self.parked[path[-1]] = len(path) - 1

    def blocked(self, cell: Cell, t: int) -> bool:
        if (cell, t) in self.vertex:
            return True
        p = self.parked.get(cell)
        return p is not None and t >= p

    def swap(self, a: Cell, b: Cell, t: int) -> bool:
        """True if an earlier robot moves from b to a while we move from a to b."""
        return (b, a, t) in self.moves

    def free_after(self, cell: Cell, t: int) -> bool:
        """True if no earlier robot uses the cell at time t or later."""
        if cell in self.parked:
            return False
        return self.last_use.get(cell, -1) < t


def space_time_astar(grid, start, goal, res: Reservations, horizon: int) -> Optional[list]:
    """Shortest path in (cell, time) that avoids the reservations, or None."""
    if res.blocked(start, 0):
        return None

    def h(cell):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    heap = [(h(start), 0, start)]
    parent = {(start, 0): None}
    while heap:
        f, t, cell = heapq.heappop(heap)
        if cell == goal and res.free_after(goal, t):
            path = []
            node = (cell, t)
            while node is not None:
                path.append(node[0])
                node = parent[node]
            return path[::-1]
        if t >= horizon:
            continue
        for nxt in neighbors(grid, cell):
            state = (nxt, t + 1)
            if state in parent or res.blocked(nxt, t + 1) or res.swap(cell, nxt, t):
                continue
            parent[state] = (cell, t)
            heapq.heappush(heap, (t + 1 + h(nxt), t + 1, nxt))
    return None


def prioritized_planning(
    grid: Sequence[str],
    starts: Sequence[Cell],
    goals: Sequence[Cell],
    order: Optional[Sequence[int]] = None,
    horizon: Optional[int] = None,
) -> Optional[list]:
    """Plan the robots in the given priority order.

    Returns one path per robot (path[t] is the cell at time t, and the robot
    stays at path[-1] afterwards), or None if some robot finds no path.
    """
    r = len(starts)
    order = list(range(r)) if order is None else list(order)
    if horizon is None:
        horizon = len(free_cells(grid)) * (r + 1)
    res = Reservations()  # @line L1
    paths = [None] * r
    for i in order:  # @line L2
        path = space_time_astar(grid, starts[i], goals[i], res, horizon)  # @line L3
        if path is None:  # @line L4
            return None
        res.add(path)  # @line L5
        paths[i] = path
    return paths  # @line L6


def position(path: list, t: int) -> Cell:
    return path[t] if t < len(path) else path[-1]


def check_plan(grid, starts, goals, paths) -> bool:
    """True if the paths are valid: moves to free neighbor cells, no conflicts."""
    r = len(paths)
    for i in range(r):
        if paths[i][0] != starts[i] or paths[i][-1] != goals[i]:
            return False
        for t in range(1, len(paths[i])):
            if paths[i][t] not in neighbors(grid, paths[i][t - 1]):
                return False
    end = max(len(p) for p in paths)
    for t in range(end):
        cells = [position(p, t) for p in paths]
        if len(set(cells)) < r:
            return False
        for i in range(r):
            for k in range(i + 1, r):
                if position(paths[i], t + 1) == position(paths[k], t) and position(paths[k], t + 1) == position(paths[i], t) and position(paths[i], t) != position(paths[i], t + 1):
                    return False
    return True
