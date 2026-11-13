# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relaxation-heuristic/. The authors are listed in prov/2WVNT9.jsonl.

"""Relaxation heuristics for the sliding tile puzzles and for grid maps.

A relaxation keeps the states (or maps them to a larger space) and drops
some preconditions of the actions. The heuristic of a state is the exact
cost of the relaxed problem from that state. Every real solution is also a
relaxed solution, so the heuristic never overestimates.

The board is a tuple of length rows * cols in row-major order. The value 0
is the blank, and the goal used below is (1, 2, ..., rows * cols - 1, 0).

The real move: a tile goes from square A to square B if A is next to B and
B is the blank. Three relaxations of it:
- drop "B is the blank" and "A is next to B": misplaced_tiles,
- drop "B is the blank": manhattan_distance,
- drop "A is next to B": gaschnig (a tile may jump into the blank).

relaxed_distances computes the exact cost of any relaxed problem by a
breadth-first search, so the closed forms can be checked against it.
"""

from collections import deque
from collections.abc import Callable, Hashable, Iterable


def goal_board(rows: int, cols: int) -> tuple:
    """The goal (1, 2, ..., rows * cols - 1, 0) with the blank last."""
    return tuple(range(1, rows * cols)) + (0,)


def puzzle_moves(board: tuple, rows: int, cols: int) -> list[tuple]:
    """The boards one real move away: a tile next to the blank slides into it."""
    b = board.index(0)
    r, c = divmod(b, cols)
    out = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < rows and 0 <= cc < cols:
            t = rr * cols + cc
            nb = list(board)
            nb[b], nb[t] = nb[t], nb[b]
            out.append(tuple(nb))
    return out


def misplaced_tiles(board: tuple, goal: tuple) -> int:
    """Number of tiles (the blank not counted) that are not on their goal square.

    It is the exact cost when a tile may move from any square to any square.
    """
    return sum(1 for x, y in zip(board, goal) if x != 0 and x != y)


def manhattan_distance(board: tuple, goal: tuple, cols: int) -> int:
    """Sum over the tiles of the grid distance to the goal square.

    It is the exact cost when a tile may move to a next square, occupied or not.
    """
    where = {v: i for i, v in enumerate(goal)}
    total = 0
    for i, v in enumerate(board):
        if v != 0:
            j = where[v]
            total += abs(i // cols - j // cols) + abs(i % cols - j % cols)
    return total


def gaschnig(board: tuple, goal: tuple) -> int:
    """Exact cost when any tile may jump into the blank (Gaschnig 1979).

    A relaxed move swaps the blank with any tile. Take the permutation that
    sends each square to the square where its content belongs. A cycle of
    length L that holds the blank needs L - 1 swaps. A cycle of length L >= 2
    without the blank needs L + 1 swaps: one to bring the blank in, L - 1 to
    place the tiles, and the last one places the blank's visitor.
    """
    where = {v: i for i, v in enumerate(goal)}
    seen = [False] * len(board)
    total = 0
    for i in range(len(board)):
        if seen[i]:
            continue
        length, has_blank, j = 0, False, i
        while not seen[j]:
            seen[j] = True
            length += 1
            if board[j] == 0:
                has_blank = True
            j = where[board[j]]
        if length >= 2:
            total += length - 1 if has_blank else length + 1
    return total


def jump_into_blank_moves(board: tuple) -> list[tuple]:
    """Relaxed moves for gaschnig: swap the blank with any tile."""
    b = board.index(0)
    out = []
    for t in range(len(board)):
        if t != b:
            nb = list(board)
            nb[b], nb[t] = nb[t], nb[b]
            out.append(tuple(nb))
    return out


def relaxed_distances(
    goals: Iterable[Hashable], neighbours: Callable[[Hashable], Iterable[Hashable]]
) -> dict:
    """Exact unit-cost distances to the nearest goal in a relaxed space.

    neighbours must be symmetric (each relaxed move can be undone by one
    relaxed move), so a breadth-first search from the goals gives the
    distance from each state to a goal. The result maps each state that can
    reach a goal to its distance.
    """
    dist = {}
    queue = deque()
    for g in goals:
        if g not in dist:
            dist[g] = 0
            queue.append(g)
    while queue:
        u = queue.popleft()
        for v in neighbours(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


def grid_manhattan(cell: tuple, goal: tuple) -> int:
    """Exact cost on a 4-connected unit-cost grid with every obstacle removed."""
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def grid_octile(cell: tuple, goal: tuple) -> float:
    """Exact cost on an 8-connected grid (costs 1 and sqrt 2) with no obstacles."""
    dx, dy = abs(cell[0] - goal[0]), abs(cell[1] - goal[1])
    return max(dx, dy) + (2 ** 0.5 - 1) * min(dx, dy)
