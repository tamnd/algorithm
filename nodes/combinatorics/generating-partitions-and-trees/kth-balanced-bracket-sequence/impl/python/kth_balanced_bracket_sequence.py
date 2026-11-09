# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kth-balanced-bracket-sequence/. The authors are listed in prov/4XTB6R.jsonl.


def completion_table(m: int) -> list[list[int]]:
    """Return d with d[i][j] = the number of ways to finish from height j with i cells.

    A way to finish is a word of i brackets that, read from height j, never
    goes below height 0 and ends at height 0. Indices run over 0 <= i <= m
    and 0 <= j <= m + 1.
    """
    d = [[0] * (m + 2) for _ in range(m + 1)]
    d[0][0] = 1
    for i in range(1, m + 1):
        for j in range(0, m + 1):
            d[i][j] = d[i - 1][j + 1] + (d[i - 1][j - 1] if j >= 1 else 0)
    return d


def kth_balanced(n: int, k: int, d: list[list[int]] | None = None) -> str:
    """Return the balanced word of n bracket pairs at 0-based position k.

    The order is lexicographic with '(' < ')'. A table from
    completion_table(2 * n) may be passed in to reuse it.
    Raise ValueError unless 0 <= k < C(n), the Catalan number.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    m = 2 * n
    if d is None:
        d = completion_table(m)  # @line L1
    if not 0 <= k < d[m][0]:  # @line L2
        raise ValueError("k is out of range")
    out: list[str] = []
    h = 0  # @line L3
    for i in range(m):  # @line L4: 0-based i is position i + 1
        c = d[m - 1 - i][h + 1]  # @line L5: words that put "(" here
        if k < c:  # @line L6
            out.append("(")  # @line L7
            h += 1
        else:
            k -= c  # @line L8
            out.append(")")  # @line L9
            h -= 1
    return "".join(out)  # @line L10
