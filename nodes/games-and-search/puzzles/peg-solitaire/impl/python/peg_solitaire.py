# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peg-solitaire/. The authors are listed in prov/ZW9A3T.jsonl.
"""Peg solitaire: boards, jumps, a depth-first solver, position classes and pagoda functions.

A board is a list of holes (x, y). A position is an integer bit mask over the
holes: bit i is set when hole i holds a peg. A jump (a, b, c) takes the peg in
hole a over the peg in hole b into the empty hole c and removes the peg in b.
"""

from collections import deque
from typing import Callable, Dict, List, Optional, Sequence, Set, Tuple

Cell = Tuple[int, int]
Jump = Tuple[int, int, int]

ORTHOGONAL = ((1, 0), (-1, 0), (0, 1), (0, -1))
# Directions on a triangular board whose hole (x, r) is hole x of row r:
# along a row, down-left (same x, next row) and down-right (x + 1, next row).
TRIANGULAR = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1))


def english_board() -> List[Cell]:
    """The 33-hole cross-shaped board, centre at (0, 0)."""
    return [(x, y) for y in range(-3, 4) for x in range(-3, 4) if abs(x) <= 1 or abs(y) <= 1]


def french_board() -> List[Cell]:
    """The 37-hole European board: the English board plus four holes at (+-2, +-2)."""
    return english_board() + [(x, y) for x in (-2, 2) for y in (-2, 2)]


def rectangle_board(w: int, h: int) -> List[Cell]:
    return [(x, y) for y in range(h) for x in range(w)]


def triangle_board(n: int) -> List[Cell]:
    """A triangle with n holes on a side, in axial coordinates (row r, column 0 .. r)."""
    return [(x, r) for r in range(n) for x in range(r + 1)]


def jumps(board: Sequence[Cell], directions: Sequence[Cell] = ORTHOGONAL) -> List[Jump]:
    index = {cell: i for i, cell in enumerate(board)}
    out = []
    for (x, y), a in index.items():
        for dx, dy in directions:
            b = index.get((x + dx, y + dy))
            c = index.get((x + 2 * dx, y + 2 * dy))
            if b is not None and c is not None:
                out.append((a, b, c))
    return out


def full(board: Sequence[Cell]) -> int:
    return (1 << len(board)) - 1


def legal(pos: int, jump: Jump) -> bool:
    a, b, c = jump
    return bool(pos >> a & 1 and pos >> b & 1 and not pos >> c & 1)


def apply(pos: int, jump: Jump) -> int:
    a, b, c = jump
    return pos ^ (1 << a) ^ (1 << b) ^ (1 << c)


def solve(jump_list: Sequence[Jump], start: int, goal: int,
          prune: Optional[Callable[[int], bool]] = None) -> Optional[List[Jump]]:
    """A sequence of jumps from start to goal, by depth-first search.

    Every jump removes one peg, so the search tree has depth
    popcount(start) - popcount(goal). Positions already shown to fail are
    stored, so each position is expanded at most once. prune(pos) may return
    True to cut a position that cannot reach the goal.
    """
    target = bin(start).count("1") - bin(goal).count("1")
    dead: Set[int] = set()
    path: List[Jump] = []

    def dfs(pos: int, left: int) -> bool:
        if left == 0:
            return pos == goal
        if pos in dead or (prune is not None and prune(pos)):
            return False
        for j in jump_list:
            if legal(pos, j):
                path.append(j)
                if dfs(apply(pos, j), left - 1):
                    return True
                path.pop()
        dead.add(pos)
        return False

    if target < 0:
        return None
    return list(path) if dfs(start, target) else None


def reachable(jump_list: Sequence[Jump], start: int) -> Set[int]:
    """Every position that some sequence of jumps reaches from start (breadth-first)."""
    seen = {start}
    queue = deque([start])
    while queue:
        pos = queue.popleft()
        for j in jump_list:
            if legal(pos, j):
                nxt = apply(pos, j)
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return seen


def single_peg_finishes(board: Sequence[Cell], jump_list: Sequence[Jump], start: int) -> Set[int]:
    """The holes in which a game from start can end with one peg."""
    return {p.bit_length() - 1 for p in reachable(jump_list, start) if p & (p - 1) == 0 and p}


def position_class(board: Sequence[Cell], pos: int) -> Tuple[int, int, int, int]:
    """The position class of a position on a square-grid board.

    Count pegs by (x + y) mod 3 and by (x - y) mod 3. A jump along a row or a
    column touches three holes that lie in three different classes of each
    kind, so it changes the parity of all three counts of each kind. The
    parities of n0 + n1 and n1 + n2 of each kind are therefore invariant:
    four bits, sixteen classes.
    """
    s = [0, 0, 0]
    d = [0, 0, 0]
    for i, (x, y) in enumerate(board):
        if pos >> i & 1:
            s[(x + y) % 3] += 1
            d[(x - y) % 3] += 1
    return ((s[0] + s[1]) & 1, (s[1] + s[2]) & 1, (d[0] + d[1]) & 1, (d[1] + d[2]) & 1)


def moves(solution: Sequence[Jump]) -> int:
    """The number of moves: a run of jumps by the same peg counts as one move."""
    count = 0
    last = None
    for a, _, c in solution:
        if a != last:
            count += 1
        last = c
    return count


def is_pagoda(weights: Sequence[float], jump_list: Sequence[Jump], eps: float = 1e-12) -> bool:
    """True if w(a) + w(b) >= w(c) for every jump (a, b, c)."""
    return all(weights[a] + weights[b] + eps >= weights[c] for a, b, c in jump_list)


def pagoda_value(weights: Sequence[float], pos: int) -> float:
    return sum(w for i, w in enumerate(weights) if pos >> i & 1)


def golden_pagoda(board: Sequence[Cell], target: Cell) -> List[float]:
    """Conway's weights phi^(-d), d the grid distance to the target, phi^2 = phi + 1."""
    phi = (1 + 5 ** 0.5) / 2
    tx, ty = target
    return [phi ** -(abs(x - tx) + abs(y - ty)) for x, y in board]


def cell_index(board: Sequence[Cell]) -> Dict[Cell, int]:
    return {cell: i for i, cell in enumerate(board)}
