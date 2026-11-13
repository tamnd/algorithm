# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitboard/. The authors are listed in prov/EHAYPB.jsonl.

"""Bitboards for tic-tac-toe and for Connect Four on a board of w columns and h rows.

A bitboard is an integer whose bit i says whether square i holds a stone.
Python integers have no fixed width, so the code masks a result only where
a C program would need it to drop bits that fall off the board.
"""

from typing import Iterator, List, Tuple

# ---------------------------------------------------------------- bit tools


def bits(b: int) -> Iterator[int]:
    """Yield the indices of the set bits of b >= 0, lowest first.

    Cost: O(1) word operations per set bit.
    """
    while b:
        low = b & -b  # @line L4
        yield low.bit_length() - 1  # @line L5
        b ^= low  # @line L6


def popcount(b: int) -> int:
    """Number of set bits of b >= 0."""
    return bin(b).count("1")


# ---------------------------------------------------------------- tic-tac-toe
# Square i is row i // 3, column i % 3; bit i stands for square i.

TTT_FULL = (1 << 9) - 1
TTT_LINES: Tuple[int, ...] = tuple(
    (1 << a) | (1 << b) | (1 << c)
    for a, b, c in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
)


def ttt_has_line(b: int) -> bool:
    """True if the stones b contain one of the 8 lines. Cost: 8 AND operations."""
    return any(b & w == w for w in TTT_LINES)  # @line L1


def ttt_empty(x: int, o: int) -> int:
    """The empty squares as a bitboard."""
    return ~(x | o) & TTT_FULL  # @line L2


def ttt_moves(x: int, o: int) -> List[int]:
    """The legal moves of the side to move, as square indices; none after a win."""
    if ttt_has_line(x) or ttt_has_line(o):
        return []
    return list(bits(ttt_empty(x, o)))


def ttt_play(x: int, o: int, i: int) -> Tuple[int, int]:
    """Put the stone of the side to move on square i. X moves when both have the same count."""
    if popcount(x) == popcount(o):
        return x | (1 << i), o  # @line L3
    return x, o | (1 << i)


# ---------------------------------------------------------------- Connect Four
# Column c uses the bits c*(h+1) to c*(h+1)+h-1, from the bottom up. Bit
# c*(h+1)+h is an empty guard bit, so that shifts do not carry a line from one
# column into the next. A position is (cur, mask): mask has all stones, and cur
# has the stones of the side to move.


class ConnectFour:
    """Bitboard rules of Connect Four (four in a row) on w columns and h rows.

    Precondition: w >= 1, h >= 1. Cost: O(1) word operations per move and per
    win test, with words of w*(h+1) bits.
    """

    def __init__(self, w: int = 7, h: int = 6):
        self.w, self.h = w, h
        self.bottom = [1 << (c * (h + 1)) for c in range(w)]
        self.top = [1 << (c * (h + 1) + h - 1) for c in range(w)]
        self.board = sum(((1 << h) - 1) << (c * (h + 1)) for c in range(w))

    def can_play(self, mask: int, c: int) -> bool:
        return mask & self.top[c] == 0  # @line L7

    def play(self, cur: int, mask: int, c: int) -> Tuple[int, int]:
        """Drop a stone of the side to move in column c; return the new (cur, mask)."""
        cur ^= mask  # @line L8  the stones of the opponent, who moves next
        mask |= mask + self.bottom[c]  # @line L9  the carry stops at the lowest empty cell
        return cur, mask

    def won(self, b: int) -> bool:
        """True if the stones b contain four in a row in some direction."""
        h = self.h
        for s in (1, h + 1, h, h + 2):  # @line L10  vertical, horizontal and the two diagonals
            m = b & (b >> s)  # @line L11  bit i: stones at i and i + s
            if m & (m >> (2 * s)):  # @line L12  bit i: stones at i, i + s, i + 2s and i + 3s
                return True
        return False  # @line L13

    def moves(self, cur: int, mask: int) -> List[int]:
        """Legal columns; none when the side that just moved has won."""
        if self.won(cur ^ mask):
            return []
        return [c for c in range(self.w) if self.can_play(mask, c)]

    def to_grid(self, cur: int, mask: int) -> List[List[int]]:
        """grid[c][r] is 0 (empty), 1 (the first player) or 2 (the second player)."""
        first = cur if popcount(mask) % 2 == 0 else cur ^ mask
        g = [[0] * self.h for _ in range(self.w)]
        for i in bits(mask):
            c, r = divmod(i, self.h + 1)
            g[c][r] = 1 if first >> i & 1 else 2
        return g
