# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smith-waterman/. The authors are listed in prov/G3HRJ9.jsonl.

from typing import Callable, NamedTuple

GAP = "-"

Score = Callable[[str, str], int]


class LocalAlignment(NamedTuple):
    """An optimal local alignment: its score, its two rows, and the aligned parts.

    The top row aligns x[x_start:x_end] and the bottom row aligns
    y[y_start:y_end] (0-based, half-open). The empty alignment has score 0.
    """

    score: int
    top: str
    bottom: str
    x_start: int
    x_end: int
    y_start: int
    y_end: int


def match_mismatch(match: int, mismatch: int) -> Score:
    """Return the substitution score s(a, b) = match if a == b, else mismatch."""

    def s(a: str, b: str) -> int:
        return match if a == b else mismatch

    return s


def smith_waterman(x: str, y: str, s: Score, d: int) -> LocalAlignment:
    """Return an optimal local alignment of x and y.

    A local alignment is a global alignment of a substring of x with a
    substring of y. Its score is the sum of s(a, b) over the aligned pairs,
    minus d for each gap symbol. The best score is at least 0, the score of
    the empty alignment. Among the cells with the best score, the first one in
    row-major order is the end of the returned alignment.

    Precondition: s returns integers, d >= 0, and x and y do not contain "-".
    Cost: Theta(m n) time and Theta(m n) space for |x| = m and |y| = n.
    """
    m, n = len(x), len(y)
    h = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):  # @line L1
        h[i][0] = 0
    for j in range(n + 1):  # @line L2
        h[0][j] = 0
    best, bi, bj = 0, 0, 0  # @line L3
    for i in range(1, m + 1):  # @line L4
        row, up = h[i], h[i - 1]
        for j in range(1, n + 1):  # @line L5
            row[j] = max(0, up[j - 1] + s(x[i - 1], y[j - 1]), up[j] - d, row[j - 1] - d)  # @line L6
            if row[j] > best:  # @line L7
                best, bi, bj = row[j], i, j
    top: list[str] = []
    bottom: list[str] = []
    i, j = bi, bj  # @line L8
    while h[i][j] > 0:  # @line L9
        if h[i][j] == h[i - 1][j - 1] + s(x[i - 1], y[j - 1]):  # @line L10
            top.append(x[i - 1])
            bottom.append(y[j - 1])
            i, j = i - 1, j - 1
        elif h[i][j] == h[i - 1][j] - d:  # @line L11
            top.append(x[i - 1])
            bottom.append(GAP)
            i -= 1
        else:  # @line L12
            top.append(GAP)
            bottom.append(y[j - 1])
            j -= 1
    return LocalAlignment(best, "".join(reversed(top)), "".join(reversed(bottom)), i, bi, j, bj)  # @line L13


def alignment_score(top: str, bottom: str, s: Score, d: int) -> int:
    """Return the score of a given alignment under s and the linear gap penalty d."""
    total = 0
    for a, b in zip(top, bottom):
        total += -d if a == GAP or b == GAP else s(a, b)
    return total
