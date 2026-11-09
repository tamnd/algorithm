# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-bracket-sequence-ranking/. The authors are listed in prov/6BDKZQ.jsonl.


def completion_table(m: int) -> list[list[int]]:
    """Return d with d[i][j] = the number of ways to finish from height j with i cells.

    A way to finish is a word of i brackets that, read from height j, never
    goes below height 0 and ends at height 0. Indices run over 0 <= i, j <= m + 1.
    """
    d = [[0] * (m + 2) for _ in range(m + 1)]
    d[0][0] = 1
    for i in range(1, m + 1):
        for j in range(0, m + 1):
            d[i][j] = d[i - 1][j + 1] + (d[i - 1][j - 1] if j >= 1 else 0)
    return d


def rank_balanced(s: str, d: list[list[int]] | None = None) -> int:
    """Return the 0-based position of the balanced word s in lexicographic order.

    The order uses '(' < ')' and compares only words of the same length.
    A table from completion_table(len(s)) may be passed in to reuse it.
    Raise ValueError if s is not a balanced word over '(' and ')'.
    """
    m = len(s)
    if d is None:
        d = completion_table(m)  # @line L1
    r = 0  # @line L2
    h = 0
    for i in range(m):  # @line L3: 0-based i is position i + 1
        if s[i] == "(":  # @line L4
            h += 1
        elif s[i] == ")":
            r += d[m - 1 - i][h + 1]  # @line L5: words with "(" here come first
            h -= 1  # @line L6
            if h < 0:
                raise ValueError("not a balanced bracket sequence")
        else:
            raise ValueError("unexpected character")
    if h != 0:
        raise ValueError("not a balanced bracket sequence")
    return r  # @line L7
