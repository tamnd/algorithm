# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hadlock-algorithm/. The authors are listed in prov/Q7C4F1.jsonl.

from collections import deque
from typing import Optional, Sequence

Cell = tuple[int, int]

# Neighbor order: up, right, down, left.
STEPS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def is_free(grid: Sequence[str], cell: Cell) -> bool:
    r, c = cell
    return 0 <= r < len(grid) and 0 <= c < len(grid[r]) and grid[r][c] != "#"


def hadlock_search(grid: Sequence[str], s: Cell, t: Cell) -> tuple[dict[Cell, int], dict[Cell, Cell], list[Cell]]:
    """Label cells with their least detour number from s, in order of detour number.

    A step is a detour if it moves away from t. Returns the detour labels,
    the parent of each labeled cell and the cells in the order they were expanded.
    The search stops when t is expanded.
    """
    det = {s: 0}
    parent: dict[Cell, Cell] = {}
    done: set[Cell] = set()
    order: list[Cell] = []
    dq = deque([s])  # @line L1
    while dq:  # @line L2
        u = dq.popleft()  # @line L3
        if u in done:  # @line L4
            continue
        done.add(u)  # @line L5
        order.append(u)
        if u == t:  # @line L6
            break
        for dr, dc in STEPS:  # @line L7
            v = (u[0] + dr, u[1] + dc)
            if not is_free(grid, v) or v in done:
                continue
            away = 1 if manhattan(v, t) > manhattan(u, t) else 0  # @line L8
            if v not in det or det[u] + away < det[v]:  # @line L9
                det[v] = det[u] + away  # @line L10
                parent[v] = u
                if away:  # @line L11
                    dq.append(v)
                else:
                    dq.appendleft(v)
    return det, parent, order


def hadlock_algorithm(grid: Sequence[str], s: Cell, t: Cell) -> Optional[list[Cell]]:
    """Return a path from s to t with the fewest detours, which is a shortest path, or None.

    grid is a list of equal-length strings, '#' marks a blocked cell. The path
    lists s first and t last. Its length is manhattan(s, t) + 2 * detours.
    """
    if not is_free(grid, s) or not is_free(grid, t):
        return None
    det, parent, order = hadlock_search(grid, s, t)
    if not order or order[-1] != t:  # @line L12
        return None
    path = [t]
    while path[-1] != s:
        path.append(parent[path[-1]])
    path.reverse()
    return path
