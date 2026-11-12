# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/needleman-wunsch/. The authors are listed in prov/2FKWQD.jsonl.

from typing import Callable

GAP = "-"

Score = Callable[[str, str], int]


def match_mismatch(match: int, mismatch: int) -> Score:
    """Return the substitution score s(a, b) = match if a == b, else mismatch."""

    def s(a: str, b: str) -> int:
        return match if a == b else mismatch

    return s


def needleman_wunsch(x: str, y: str, s: Score, d: int) -> tuple[int, str, str]:
    """Return an optimal global alignment of x and y.

    The score of an alignment is the sum of s(a, b) over its aligned pairs,
    minus d for each gap symbol (a linear gap penalty g(L) = d L). The result
    is (score, top row, bottom row); the rows have the same length and use
    "-" for a gap. Ties go to the diagonal step, then to a gap in y, then to
    a gap in x.

    Precondition: s returns integers; x and y do not contain "-".
    Cost: Theta(m n) time and Theta(m n) space for |x| = m and |y| = n.
    """
    m, n = len(x), len(y)
    f = [[0] * (n + 1) for _ in range(m + 1)]
    f[0][0] = 0  # @line L1
    for i in range(1, m + 1):  # @line L2
        f[i][0] = -i * d
    for j in range(1, n + 1):  # @line L3
        f[0][j] = -j * d
    for i in range(1, m + 1):  # @line L4
        row, up = f[i], f[i - 1]
        for j in range(1, n + 1):  # @line L5
            row[j] = max(up[j - 1] + s(x[i - 1], y[j - 1]), up[j] - d, row[j - 1] - d)  # @line L6
    top: list[str] = []
    bottom: list[str] = []
    i, j = m, n  # @line L7
    while i > 0 or j > 0:  # @line L8
        if i > 0 and j > 0 and f[i][j] == f[i - 1][j - 1] + s(x[i - 1], y[j - 1]):  # @line L9
            top.append(x[i - 1])
            bottom.append(y[j - 1])
            i, j = i - 1, j - 1
        elif i > 0 and f[i][j] == f[i - 1][j] - d:  # @line L10
            top.append(x[i - 1])
            bottom.append(GAP)
            i -= 1
        else:  # @line L11
            top.append(GAP)
            bottom.append(y[j - 1])
            j -= 1
    return f[m][n], "".join(reversed(top)), "".join(reversed(bottom))  # @line L12


def alignment_score(top: str, bottom: str, s: Score, d: int) -> int:
    """Return the score of a given alignment under s and the linear gap penalty d."""
    total = 0
    for a, b in zip(top, bottom):
        total += -d if a == GAP or b == GAP else s(a, b)
    return total
