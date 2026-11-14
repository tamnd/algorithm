# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lee-maze-routing/. The authors are listed in prov/EQ37HH.jsonl.

from collections import deque
from typing import Optional, Sequence

Cell = tuple[int, int]

# Neighbor order: up, right, down, left. The backtrace uses the same order.
STEPS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def free_neighbors(grid: Sequence[str], cell: Cell) -> list[Cell]:
    """Free cells next to cell, in the fixed order up, right, down, left."""
    r, c = cell
    out = []
    for dr, dc in STEPS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] != "#":
            out.append((nr, nc))
    return out


def lee_wave(grid: Sequence[str], s: Cell, t: Cell) -> dict[Cell, int]:
    """Wave expansion: label each cell with its distance from s, until t is labeled."""
    label = {s: 0}
    wave = deque([s])  # @line L1
    while wave and t not in label:  # @line L2
        u = wave.popleft()  # @line L3
        for v in free_neighbors(grid, u):  # @line L4
            if v not in label:
                label[v] = label[u] + 1  # @line L5
                wave.append(v)
    return label


def lee_maze_routing(grid: Sequence[str], s: Cell, t: Cell) -> Optional[list[Cell]]:
    """Return a shortest path of cells from s to t on the grid, or None.

    grid is a list of equal-length strings, '#' marks a blocked cell. Moves go
    to the four neighbors. The path lists s first and t last.
    """
    for r, c in (s, t):
        if not (0 <= r < len(grid) and 0 <= c < len(grid[r])) or grid[r][c] == "#":
            return None
    label = lee_wave(grid, s, t)
    if t not in label:  # @line L6
        return None
    path = [t]  # @line L7
    while path[-1] != s:  # @line L8
        u = path[-1]
        for v in free_neighbors(grid, u):  # @line L9
            if label.get(v) == label[u] - 1:
                path.append(v)  # @line L10
                break
    path.reverse()
    return path  # @line L11
