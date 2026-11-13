# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strategy-stealing-argument/. The authors are listed in prov/G3BS01.jsonl.

"""Checks of the strategy-stealing argument on small games.

A positional game has cells 0 .. k - 1. Player 1 and player 2 claim empty
cells in turn, player 1 first. wins1(mask) and wins2(mask) say whether a set
of cells contains a winning set of that player. The first player to own a
winning set wins; a full board with no winner is a draw. Values are seen
from player 1: +1 win, 0 draw, -1 loss.

The module also holds Chomp, where the argument takes the form "the first
player has a move that the opponent cannot exploit"."""

from functools import lru_cache
from typing import Callable, Dict, List, Optional, Sequence, Tuple

Mask = int
WinTest = Callable[[Mask], bool]


class PositionalGame:
    def __init__(self, cells: int, wins1: WinTest, wins2: WinTest, sigma: Optional[Sequence[int]] = None):
        """sigma is a permutation of the cells that maps winning sets of
        player 1 to winning sets of player 2 and back; it is the symmetry
        that the argument needs. None means the identity."""
        self.cells = cells
        self.wins1 = wins1
        self.wins2 = wins2
        self.sigma = list(sigma) if sigma is not None else list(range(cells))
        self.full = (1 << cells) - 1
        self._memo: Dict[Tuple[Mask, Mask, int], int] = {}

    def value(self, a: Mask, b: Mask, mover: int) -> int:
        """Minimax value for player 1 when player 1 owns a, player 2 owns b
        and `mover` (1 or 2) is to move. Positions need not have the usual
        stone counts, so extra stones can be studied."""
        if self.wins1(a):
            return 1
        if self.wins2(b):
            return -1
        if a | b == self.full:
            return 0
        key = (a, b, mover)
        if key in self._memo:
            return self._memo[key]
        free = self.full & ~(a | b)
        best = -2 if mover == 1 else 2
        while free:
            v = free & -free
            free ^= v
            if mover == 1:
                best = max(best, self.value(a | v, b, 2))
                if best == 1:
                    break
            else:
                best = min(best, self.value(a, b | v, 1))
                if best == -1:
                    break
        self._memo[key] = best
        return best

    def map_mask(self, mask: Mask, perm: Sequence[int]) -> Mask:
        out = 0
        for i in range(self.cells):
            if mask >> i & 1:
                out |= 1 << perm[i]
        return out


Strategy = Callable[[Mask, Mask], int]


def play_stolen(game: PositionalGame, steal_from: Strategy, opponent: Strategy, first_cell: int):
    """Play the stolen strategy as player 1 against `opponent` (player 2).

    steal_from(x, y) is a strategy for the second player of the game: it gets
    the cells x of the first player and y of its own, and returns a cell.
    Player 1 imagines a game in which player 2 is the first player, with
    real move c seen as sigma^-1(c), and answers with sigma of what
    steal_from says, or with any free cell when that cell holds the extra
    stone. Return (real result, imagined winner), where the imagined winner
    is 1, 2 or 0 for the role that first completed a set in the imagined
    game (role 1 is real player 2)."""
    sig, inv = game.sigma, [0] * game.cells
    for i, s in enumerate(sig):
        inv[s] = i
    a = 1 << first_cell  # real cells of player 1
    b = 0  # real cells of player 2
    im1 = im2 = 0  # imagined cells: role 1 (the real opponent) and role 2 (us)
    extra = first_cell
    imagined = 0
    while True:
        if game.wins1(a):
            return 1, imagined
        if a | b == game.full:
            return 0, imagined
        c = opponent(a, b)
        assert not (a | b) >> c & 1
        b |= 1 << c
        im1 |= 1 << inv[c]
        if not imagined and game.wins1(im1):
            imagined = 1
        if game.wins2(b):
            return -1, imagined
        if a | b == game.full:
            return 0, imagined
        z = steal_from(im1, im2)
        im2 |= 1 << z
        if not imagined and game.wins2(im2):
            imagined = 2
        real = sig[z]
        if real == extra:
            free = game.full & ~(a | b)
            extra = (free & -free).bit_length() - 1
            real = extra
        a |= 1 << real


def optimal_second_player(game: PositionalGame) -> Strategy:
    """A strategy for the second player of the game, from the minimax values."""

    def strategy(x: Mask, y: Mask) -> int:
        free = [i for i in range(game.cells) if not (x | y) >> i & 1]
        return min(free, key=lambda i: game.value(x, y | 1 << i, 1))

    return strategy


def random_strategy(rng, cells: int) -> Strategy:
    def strategy(x: Mask, y: Mask) -> int:
        return rng.choice([i for i in range(cells) if not (x | y) >> i & 1])

    return strategy


# Tic-tac-toe on a 3 x 3 board, cell 3 * r + c.

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]
LINE_MASKS = [sum(1 << i for i in line) for line in LINES]


def has_line(mask: Mask) -> bool:
    return any(mask & m == m for m in LINE_MASKS)


def tic_tac_toe() -> PositionalGame:
    return PositionalGame(9, has_line, has_line)


# Hex on an m x n board: m rows, n columns, cell n * r + c. Player 1 joins
# the top and bottom rows, player 2 the left and right columns.

def hex_connects(m: int, n: int, mask: Mask, vertical: bool) -> bool:
    steps = ((-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0))
    if vertical:
        stack = [c for c in range(n) if mask >> c & 1]
    else:
        stack = [r * n for r in range(m) if mask >> (r * n) & 1]
    seen = set(stack)
    while stack:
        v = stack.pop()
        r, c = divmod(v, n)
        if (vertical and r == m - 1) or (not vertical and c == n - 1):
            return True
        for dr, dc in steps:
            rr, cc = r + dr, c + dc
            w = rr * n + cc
            if 0 <= rr < m and 0 <= cc < n and mask >> w & 1 and w not in seen:
                seen.add(w)
                stack.append(w)
    return False


def hex_game(m: int, n: int) -> PositionalGame:
    sigma = None
    if m == n:
        # the reflection (r, c) -> (c, r) swaps the two goals
        sigma = [c * n + r for r in range(n) for c in range(n)]
    return PositionalGame(
        m * n,
        lambda s: hex_connects(m, n, s, True),
        lambda s: hex_connects(m, n, s, False),
        sigma,
    )


# Chomp: a board is a tuple of row lengths, longest first. Square (0, 0) is
# poisoned; a move picks a square (i, j) other than (0, 0) and removes every
# square (k, l) with k >= i and l >= j. The player with no move must eat the
# poison and loses.

Board = Tuple[int, ...]


def chomp_moves(board: Board) -> List[Tuple[Tuple[int, int], Board]]:
    out = []
    for i, length in enumerate(board):
        for j in range(length):
            if (i, j) == (0, 0):
                continue
            rows = [min(r, j) if k >= i else r for k, r in enumerate(board)]
            out.append(((i, j), tuple(r for r in rows if r > 0)))
    return out


@lru_cache(maxsize=None)
def chomp_mover_wins(board: Board) -> bool:
    return any(not chomp_mover_wins(nxt) for _, nxt in chomp_moves(board))


def rectangle(rows: int, cols: int) -> Board:
    return (cols,) * rows


def chomp_winning_moves(board: Board) -> List[Tuple[int, int]]:
    return [mv for mv, nxt in chomp_moves(board) if not chomp_mover_wins(nxt)]


def chomp_steal_holds(board: Board) -> bool:
    """The argument for Chomp: let c be the move that takes only the corner
    square opposite the poison. Every position reachable after c is reachable
    from the board in one move, so either c wins, or the winning reply to c
    is a winning first move."""
    corner_row = len(board) - 1
    corner = (corner_row, board[corner_row] - 1)
    after = dict(chomp_moves(board))[corner]
    direct = {nxt for _, nxt in chomp_moves(board)}
    replies = {nxt for _, nxt in chomp_moves(after)}
    if not replies <= direct:
        return False
    return not chomp_mover_wins(after) or any(not chomp_mover_wins(q) for q in replies & direct)
