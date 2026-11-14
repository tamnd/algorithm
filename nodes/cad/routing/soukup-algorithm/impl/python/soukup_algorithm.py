# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soukup-algorithm/. The authors are listed in prov/34KRY7.jsonl.

from typing import Optional, Sequence

Cell = tuple[int, int]

# Neighbor order: up, right, down, left.
STEPS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def is_free(grid: Sequence[str], cell: Cell) -> bool:
    r, c = cell
    return 0 <= r < len(grid) and 0 <= c < len(grid[r]) and grid[r][c] != "#"


def soukup_search(grid: Sequence[str], s: Cell, t: Cell) -> tuple[dict[Cell, Cell], list[Cell]]:
    """Soukup's search. Returns the parent of each reached cell and the expansion order.

    From each cell of the current wave, the search goes depth-first through
    neighbors that are closer to t. A neighbor that is not closer to t goes to
    the next wave, as in a breadth-first search. Each cell is reached once.
    The search stops as soon as t is reached.
    """
    parent: dict[Cell, Cell] = {s: s}
    order: list[Cell] = []
    wave = [s]  # @line L1
    if s == t:
        return parent, [s]
    while wave:  # @line L2
        nxt: list[Cell] = []  # @line L3
        for c in wave:  # @line L4
            stack = [(c, None)]  # @line L5
            while stack:  # @line L6
                u, came = stack.pop()  # @line L7
                order.append(u)
                toward: list[tuple[Cell, tuple[int, int]]] = []
                for d in STEPS:  # @line L8
                    v = (u[0] + d[0], u[1] + d[1])
                    if not is_free(grid, v) or v in parent:
                        continue
                    parent[v] = u  # @line L9
                    if v == t:  # @line L10
                        order.append(v)
                        return parent, order
                    if manhattan(v, t) < manhattan(u, t):  # @line L11
                        toward.append((v, d))
                    else:
                        nxt.append(v)  # @line L12
                # Push so that a step in the same direction as the last one is popped first.
                toward.sort(key=lambda vd: vd[1] == came)
                for v, d in toward:
                    stack.append((v, d))
        wave = nxt  # @line L13
    return parent, order  # @line L14


def soukup_algorithm(grid: Sequence[str], s: Cell, t: Cell) -> Optional[list[Cell]]:
    """Return a path of cells from s to t found by Soukup's router, or None.

    grid is a list of equal-length strings, '#' marks a blocked cell. The path
    lists s first and t last. It exists whenever some path exists, but it need
    not be shortest.
    """
    if not is_free(grid, s) or not is_free(grid, t):
        return None
    parent, _ = soukup_search(grid, s, t)
    if t not in parent:
        return None
    path = [t]
    while path[-1] != s:
        path.append(parent[path[-1]])
    path.reverse()
    return path
