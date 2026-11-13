# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pattern-database/. The authors are listed in prov/KA46D3.jsonl.

"""Pattern databases for the sliding tile puzzles.

A pattern is a set of tiles. The abstraction of a board keeps the squares of
the pattern tiles and of the blank, and forgets which other tile is where.
The database stores the exact cost of each abstract state, found by one
search backward from the abstract goal. The real moves are reversible, so a
search from the goal gives the distance to the goal.

Two kinds of database:
- counting all moves (Culberson and Schaeffer 1998): every move costs 1,
  and the table is a plain breadth-first search;
- counting pattern moves only (Korf and Felner 2002): a move of a tile that
  is not in the pattern costs 0, so the search is a 0-1 breadth-first search.
  For disjoint patterns the values of these tables can be added.

The table maps (squares of the pattern tiles, square of the blank) to the
cost. With blank_free=True the blank square is dropped from the key, and the
stored value is the least cost over the blank squares, which is the smaller
table of Korf and Felner. The board is a tuple in row-major order, 0 is the
blank, and the goal is (1, 2, ..., rows * cols - 1, 0).
"""

from collections import deque
from math import factorial


def goal_board(rows: int, cols: int) -> tuple:
    return tuple(range(1, rows * cols)) + (0,)


def puzzle_moves(board: tuple, rows: int, cols: int) -> list[tuple]:
    """Boards one real move away, with the tile that moved."""
    b = board.index(0)
    r, c = divmod(b, cols)
    out = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < rows and 0 <= cc < cols:
            t = rr * cols + cc
            nb = list(board)
            nb[b], nb[t] = nb[t], nb[b]
            out.append((tuple(nb), board[t]))
    return out


def neighbours(square: int, rows: int, cols: int) -> list[int]:
    r, c = divmod(square, cols)
    return [rr * cols + cc for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)) if 0 <= rr < rows and 0 <= cc < cols]


def abstract(board: tuple, pattern: tuple) -> tuple:
    """The abstract state: squares of the pattern tiles, in pattern order, then the blank."""
    where = {v: i for i, v in enumerate(board)}
    return tuple(where[t] for t in pattern) + (where[0],)


def abstract_moves(state: tuple, rows: int, cols: int, additive: bool):
    """Abstract moves (next state, cost). The blank swaps with a next square.

    If that square holds a pattern tile, the tile moves (cost 1). Otherwise a
    tile outside the pattern moves, which costs 1 when all moves count and 0
    when only pattern moves count.
    """
    *tiles, blank = state
    for sq in neighbours(blank, rows, cols):
        if sq in tiles:
            i = tiles.index(sq)
            nt = tiles[:i] + [blank] + tiles[i + 1:]
            yield tuple(nt) + (sq,), 1
        else:
            yield tuple(tiles) + (sq,), 0 if additive else 1


def build_pdb(pattern: tuple, rows: int, cols: int, additive: bool, blank_free: bool = False) -> dict:
    """Search backward from the abstract goal; return the table of exact costs.

    A deque with 0-cost moves at the front and 1-cost moves at the back is a
    breadth-first search when all moves cost 1 and a 0-1 search otherwise.
    """
    goal = goal_board(rows, cols)
    start = abstract(goal, pattern)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        du = dist[u]
        for v, c in abstract_moves(u, rows, cols, additive):
            if du + c < dist.get(v, du + c + 1):
                dist[v] = du + c
                if c == 0:
                    queue.appendleft(v)
                else:
                    queue.append(v)
    if not blank_free:
        return dist
    table = {}
    for key, d in dist.items():
        k = key[:-1]
        if d < table.get(k, d + 1):
            table[k] = d
    return table


def lookup(table: dict, board: tuple, pattern: tuple, blank_free: bool = False) -> int:
    key = abstract(board, pattern)
    return table[key[:-1] if blank_free else key]


def table_size(n_squares: int, k: int, with_blank: bool) -> int:
    """Number of abstract states: ordered placements of k tiles, and the blank."""
    used = k + (1 if with_blank else 0)
    return factorial(n_squares) // factorial(n_squares - used)


class PatternDatabaseHeuristic:
    """h(board) as the maximum of several tables, or the sum of disjoint additive ones."""

    def __init__(self, rows: int, cols: int, patterns: list[tuple], additive: bool, blank_free: bool = False):
        if additive:
            tiles = [t for p in patterns for t in p]
            if len(tiles) != len(set(tiles)):
                raise ValueError("additive patterns must be disjoint")
        self.patterns = patterns
        self.additive = additive
        self.blank_free = blank_free
        self.tables = [build_pdb(p, rows, cols, additive, blank_free) for p in patterns]

    def __call__(self, board: tuple) -> int:
        vals = [lookup(t, board, p, self.blank_free) for t, p in zip(self.tables, self.patterns)]
        return sum(vals) if self.additive else max(vals)
