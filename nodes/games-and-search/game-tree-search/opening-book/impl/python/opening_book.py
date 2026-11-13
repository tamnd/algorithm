# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/opening-book/. The authors are listed in prov/398VMX.jsonl.

"""An opening book for tic-tac-toe, keyed by Zobrist hash.

A board is a tuple of 9 cells, 0 for empty, 1 for X and 2 for O; X moves
first, so the side to move follows from the number of pieces. A move is the
index of a cell. The book maps the key of a position to its book moves, each
with a weight, the number of games and the points of the mover in them. Two
move orders that reach the same position share one entry, so the book is a
directed acyclic graph, not a tree.
"""

import random
from fractions import Fraction
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

Board = Tuple[int, ...]
EMPTY: Board = (0,) * 9
LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def to_move(board: Board) -> int:
    return 1 if board.count(1) == board.count(2) else 2


def winner(board: Board) -> int:
    for a, b, c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return 0


def legal_moves(board: Board) -> List[int]:
    if winner(board):
        return []
    return [i for i in range(9) if board[i] == 0]


def play(board: Board, move: int) -> Board:
    b = list(board)
    b[move] = to_move(board)
    return tuple(b)


def zobrist_table(rng: random.Random) -> List[List[int]]:
    """One random 64-bit word per (cell, piece); index 0 of each row is unused."""
    return [[0, rng.getrandbits(64), rng.getrandbits(64)] for _ in range(9)]


def zobrist_key(board: Board, table: List[List[int]]) -> int:
    """The XOR of the words of the pieces on the board. Cost O(9)."""
    k = 0
    for i, p in enumerate(board):
        if p:
            k ^= table[i][p]
    return k


class Entry:
    """One book move of one position."""

    __slots__ = ("move", "weight", "games", "points")

    def __init__(self, move: int) -> None:
        self.move, self.weight, self.games, self.points = move, Fraction(0), 0, Fraction(0)


class OpeningBook:
    """A table from Zobrist keys to book moves. Only positions with fewer than
    max_ply pieces are stored. The board of each position is kept beside the
    key so that the tests can check that no two positions share a key; a real
    book stores only the key."""

    def __init__(self, table: List[List[int]], max_ply: int) -> None:
        self.table, self.max_ply = table, max_ply
        self.entries: Dict[int, Dict[int, Entry]] = {}
        self.board_of: Dict[int, Board] = {}

    def probe(self, board: Board) -> List[Entry]:
        """The book moves of a position, empty if it is not in the book. O(1) expected."""
        return list(self.entries.get(zobrist_key(board, self.table), {}).values())  # @line L1

    def add_line(self, moves: Sequence[int], result: int) -> None:
        """Add one game. result is 1 if X won, 2 if O won and 0 for a draw.
        Each book move played gets one more game and the mover's points
        (1 for a win, 1/2 for a draw, 0 for a loss); its weight is set to the
        number of games. The key is updated by one XOR per move."""
        board, key = EMPTY, 0  # @line L2
        for ply, mv in enumerate(moves):  # @line L3
            if ply >= self.max_ply:
                break
            side = to_move(board)
            row = self.entries.setdefault(key, {})
            self.board_of.setdefault(key, board)
            e = row.get(mv)  # @line L4
            if e is None:
                e = row[mv] = Entry(mv)
            e.games += 1  # @line L5
            e.points += 1 if result == side else (Fraction(1, 2) if result == 0 else 0)
            e.weight = Fraction(e.games)
            key ^= self.table[mv][side]  # @line L6
            board = play(board, mv)

    def choose(self, board: Board, rng: random.Random) -> Optional[int]:
        """A book move drawn with probability proportional to its weight, or
        None if the position has no book move of positive weight."""
        es = [e for e in self.probe(board) if e.weight > 0]  # @line L7
        if not es:  # @line L8
            return None
        total = sum(e.weight for e in es)
        x = Fraction(rng.random()) * total
        for e in es:  # @line L9
            x -= e.weight
            if x < 0:
                return e.move
        return es[-1].move

    def learn(self, moves: Sequence[int], side: int, result: int, up: Fraction = Fraction(3, 2),
              down: Fraction = Fraction(1, 2), floor: Fraction = Fraction(1, 4)) -> None:
        """Result-based book learning for the program that played side.

        For each book move that side played in the game, multiply its weight by
        up after a win and by down after a loss; a draw changes nothing. A
        weight below floor becomes 0, so the move is no longer chosen.
        """
        if result == 0:  # @line L10
            return
        f = up if result == side else down
        board, key = EMPTY, 0
        for mv in moves:
            if key not in self.entries:
                break
            s = to_move(board)
            e = self.entries[key].get(mv)
            if e is None:
                break
            if s == side:
                e.weight *= f  # @line L11
                if e.weight < floor:
                    e.weight = Fraction(0)
            key ^= self.table[mv][s]
            board = play(board, mv)

    def edges(self) -> List[Tuple[int, int, int]]:
        """The arcs (key, move, child key) of the book graph."""
        out = []
        for k, row in self.entries.items():
            side = to_move(self.board_of[k])
            for mv in row:
                out.append((k, mv, k ^ self.table[mv][side]))
        return out

    def backup(self, leaf_value: Callable[[Board], int]) -> Dict[int, int]:
        """Negamax values of the book graph, for the side to move.

        A child that is not a book position is scored by leaf_value, from the
        view of its side to move. The positions are processed in decreasing
        number of pieces, a topological order of the graph, so each position
        is done after all its children. Cost O(V + E) with V positions and E
        book moves, plus the calls of leaf_value.
        """
        val: Dict[int, int] = {}
        for k in sorted(self.entries, key=lambda k: -sum(1 for p in self.board_of[k] if p)):  # @line L12
            board = self.board_of[k]
            side = to_move(board)
            best = None
            for mv in self.entries[k]:
                ck = k ^ self.table[mv][side]
                child = play(board, mv)
                v = -(val[ck] if ck in val else leaf_value(child))  # @line L13
                best = v if best is None else max(best, v)
            val[k] = best
        return val  # @line L14


def solve(board: Board, memo: Optional[Dict[Board, int]] = None) -> int:
    """The exact value of a tic-tac-toe position for the side to move: 1 win, 0 draw, -1 loss."""
    if memo is None:
        memo = {}
    if board in memo:
        return memo[board]
    w = winner(board)
    if w:
        v = 1 if w == to_move(board) else -1
    else:
        ms = legal_moves(board)
        v = 0 if not ms else max(-solve(play(board, m), memo) for m in ms)
    memo[board] = v
    return v


def noisy_game(rng: random.Random, memo: Dict[Board, int], noise: float) -> Tuple[List[int], int]:
    """A game in which each side plays a random best move, or with probability
    noise a random legal move. Returns the moves and the result."""
    board, moves = EMPTY, []
    while legal_moves(board):
        ms = legal_moves(board)
        if rng.random() < noise:
            mv = rng.choice(ms)
        else:
            best = max(-solve(play(board, m), memo) for m in ms)
            mv = rng.choice([m for m in ms if -solve(play(board, m), memo) == best])
        moves.append(mv)
        board = play(board, mv)
    return moves, winner(board)


def build_book(lines: Iterable[Tuple[List[int], int]], table: List[List[int]], max_ply: int) -> OpeningBook:
    book = OpeningBook(table, max_ply)
    for moves, result in lines:
        book.add_line(moves, result)
    return book
