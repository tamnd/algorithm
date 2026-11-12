# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hirschberg-algorithm/. The authors are listed in prov/WVTXEZ.jsonl.

from typing import Callable

GAP = "-"

Score = Callable[[str, str], int]


def match_mismatch(match: int, mismatch: int) -> Score:
    """Return the substitution score s(a, b) = match if a == b, else mismatch."""

    def s(a: str, b: str) -> int:
        return match if a == b else mismatch

    return s


def nw_last_row(
    x: str, i0: int, i1: int, y: str, j0: int, j1: int, s: Score, d: int, backward: bool
) -> list[int]:
    """Return the last row of the global alignment table of x[i0:i1] against y[j0:j1].

    Forward: r[j] is the best score of x[i0:i1] against y[j0:j0 + j].
    Backward (both parts read from the right): r[j] is the best score of
    x[i0:i1] against y[j1 - j:j1].
    Cost: Theta((i1 - i0) (j1 - j0)) time and Theta(j1 - j0) space.
    """
    n = j1 - j0
    r = [-j * d for j in range(n + 1)]  # @line L1
    rows = range(i1 - 1, i0 - 1, -1) if backward else range(i0, i1)
    for step, i in enumerate(rows, 1):  # @line L2
        a = x[i]
        diag, r[0] = r[0], -step * d  # @line L3
        for j in range(1, n + 1):  # @line L4
            b = y[j1 - j] if backward else y[j0 + j - 1]
            t = max(diag + s(a, b), r[j] - d, r[j - 1] - d)  # @line L5
            diag, r[j] = r[j], t
    return r  # @line L6


def _base(x: str, i0: int, i1: int, y: str, j0: int, j1: int, s: Score, d: int) -> list[tuple[str, str]]:
    """Columns of an optimal alignment when x[i0:i1] or y[j0:j1] is empty, or x[i0:i1] has one letter."""
    if i1 == i0:
        return [(GAP, y[j]) for j in range(j0, j1)]
    if j1 == j0:
        return [(x[i], GAP) for i in range(i0, i1)]
    # One letter a of x against y[j0:j1]: put a under the best letter of y, or
    # leave it out, whichever scores more. This is Needleman-Wunsch on one row:
    # the pair (a, y[j]) replaces the two gap columns (a, -) and (-, y[j]).
    a = x[i0]
    best_j = -1
    best = -2 * d
    for j in range(j0, j1):
        if s(a, y[j]) > best:
            best, best_j = s(a, y[j]), j
    if best_j < 0:
        return [(a, GAP)] + [(GAP, y[j]) for j in range(j0, j1)]
    return [(GAP, y[j]) for j in range(j0, best_j)] + [(a, y[best_j])] + [(GAP, y[j]) for j in range(best_j + 1, j1)]


def hirschberg_algorithm(x: str, y: str, s: Score, d: int, stats: dict | None = None) -> tuple[int, str, str]:
    """Return an optimal global alignment of x and y as (score, top, bottom), in linear space.

    The score is the sum of s(a, b) over aligned pairs minus d for each gap
    symbol. The table rows run over the shorter string, so the working space
    is O(min(m, n)) words for the rows plus O(log max(m, n)) for the stack of
    pending subproblems, beside the input and the output. If stats is a dict,
    stats["cells"] receives the number of table cells computed.

    Precondition: s returns integers, d >= 0, and x and y do not contain "-".
    Cost: Theta(m n) time; at most n (2 m + ceil(log2 m)) cells when m >= n.
    """
    swap = len(y) > len(x)
    if swap:
        x, y = y, x
        t = s
        s = lambda a, b: t(b, a)
    m, n = len(x), len(y)
    cells = 0
    columns: list[tuple[str, str]] = []
    stack = [(0, m, 0, n)]
    while stack:
        i0, i1, j0, j1 = stack.pop()
        if i1 == i0 or j1 == j0:  # @line L7
            columns += _base(x, i0, i1, y, j0, j1, s, d)
            continue
        if i1 - i0 == 1:  # @line L8
            cells += j1 - j0
            columns += _base(x, i0, i1, y, j0, j1, s, d)
            continue
        mid = (i0 + i1) // 2  # @line L9
        f = nw_last_row(x, i0, mid, y, j0, j1, s, d, False)  # @line L10
        b = nw_last_row(x, mid, i1, y, j0, j1, s, d, True)  # @line L11
        cells += (i1 - i0) * (j1 - j0)
        w = j1 - j0
        k = max(range(w + 1), key=lambda j: f[j] + b[w - j])  # @line L12
        stack.append((mid, i1, j0 + k, j1))  # @line L13
        stack.append((i0, mid, j0, j0 + k))
    if stats is not None:
        stats["cells"] = cells
    top = "".join(c[0] for c in columns)
    bottom = "".join(c[1] for c in columns)
    score = sum(-d if GAP in c else s(c[0], c[1]) for c in columns)
    if swap:
        top, bottom = bottom, top
    return score, top, bottom
