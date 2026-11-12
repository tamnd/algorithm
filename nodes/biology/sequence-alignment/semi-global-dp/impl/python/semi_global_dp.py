# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-global-dp/. The authors are listed in prov/GQAPYM.jsonl.

from typing import Callable

GAP = "-"

Score = Callable[[str, str], int]


def match_mismatch(match: int, mismatch: int) -> Score:
    """Return the substitution score s(a, b) = match if a == b, else mismatch."""

    def s(a: str, b: str) -> int:
        return match if a == b else mismatch

    return s


def semi_global_dp(
    x: str,
    y: str,
    s: Score,
    d: int,
    free_x_prefix: bool = False,
    free_x_suffix: bool = False,
    free_y_prefix: bool = False,
    free_y_suffix: bool = False,
) -> tuple[int, str, str]:
    """Return an optimal semi-global alignment of x and y as (score, top, bottom).

    The alignment covers all of x and all of y. Each aligned pair scores
    s(a, b) and each gap symbol costs d, except the free end gaps:
    free_x_prefix makes the gaps opposite a prefix of x free (gaps in the
    bottom row before the first letter of y), free_x_suffix the gaps after
    the last letter of y, and free_y_prefix and free_y_suffix do the same for
    y. With all four flags False this is Needleman-Wunsch. Overlap alignment
    (a suffix of x against a prefix of y) is free_x_prefix and free_y_suffix;
    fitting y into x is free_x_prefix and free_x_suffix.

    Precondition: s returns integers; x and y do not contain "-".
    Cost: Theta(m n) time and Theta(m n) space for |x| = m and |y| = n.
    """
    m, n = len(x), len(y)
    f = [[0] * (n + 1) for _ in range(m + 1)]
    f[0][0] = 0  # @line L1
    for i in range(1, m + 1):  # @line L2
        f[i][0] = 0 if free_x_prefix else -i * d
    for j in range(1, n + 1):  # @line L3
        f[0][j] = 0 if free_y_prefix else -j * d
    for i in range(1, m + 1):  # @line L4
        row, up = f[i], f[i - 1]
        for j in range(1, n + 1):  # @line L5
            row[j] = max(up[j - 1] + s(x[i - 1], y[j - 1]), up[j] - d, row[j - 1] - d)  # @line L6
    ends = [(m, n)]  # @line L7
    if free_x_suffix:
        ends += [(i, n) for i in range(m + 1)]
    if free_y_suffix:
        ends += [(m, j) for j in range(n + 1)]
    ei, ej = max(ends, key=lambda c: f[c[0]][c[1]])  # @line L8
    top = [x[k] for k in range(m - 1, ei - 1, -1)] + [GAP] * (n - ej)
    bottom = [GAP] * (m - ei) + [y[k] for k in range(n - 1, ej - 1, -1)]
    i, j = ei, ej
    while i > 0 and j > 0:  # @line L9
        if f[i][j] == f[i - 1][j - 1] + s(x[i - 1], y[j - 1]):  # @line L10
            top.append(x[i - 1])
            bottom.append(y[j - 1])
            i, j = i - 1, j - 1
        elif f[i][j] == f[i - 1][j] - d:  # @line L11
            top.append(x[i - 1])
            bottom.append(GAP)
            i -= 1
        else:  # @line L12
            top.append(GAP)
            bottom.append(y[j - 1])
            j -= 1
    top += [x[k] for k in range(i - 1, -1, -1)] + [GAP] * j  # @line L13
    bottom += [GAP] * i + [y[k] for k in range(j - 1, -1, -1)]
    return f[ei][ej], "".join(reversed(top)), "".join(reversed(bottom))  # @line L14


def semi_global_score(
    top: str,
    bottom: str,
    s: Score,
    d: int,
    free_x_prefix: bool = False,
    free_x_suffix: bool = False,
    free_y_prefix: bool = False,
    free_y_suffix: bool = False,
) -> int:
    """Return the score of a given alignment with the stated end gaps free."""
    xs = [k for k, a in enumerate(top) if a != GAP]
    ys = [k for k, b in enumerate(bottom) if b != GAP]
    total = 0
    for k, (a, b) in enumerate(zip(top, bottom)):
        if b == GAP:
            free = (free_x_prefix and (not ys or k < ys[0])) or (free_x_suffix and (not ys or k > ys[-1]))
        elif a == GAP:
            free = (free_y_prefix and (not xs or k < xs[0])) or (free_y_suffix and (not xs or k > xs[-1]))
        else:
            total += s(a, b)
            continue
        if not free:
            total -= d
    return total
