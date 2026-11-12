# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/center-star-method/. The authors are listed in prov/3K9D30.jsonl.

"""Gusfield's center-star method for sum-of-pairs multiple alignment (costs, minimized)."""

from typing import Callable

GAP = "-"
Cost = Callable[[str, str], int]


def unit_cost(x: str, y: str) -> int:
    """Edit-distance costs: 0 for equal symbols (also gap-gap), 1 otherwise."""
    return 0 if x == y else 1


def pairwise(s: str, t: str, cost: Cost) -> tuple[int, str, str]:
    """Optimal global alignment of s and t that minimizes the total cost.

    Ties prefer a diagonal step, then a gap in t, then a gap in s.
    Time and space O(|s| |t|).
    """
    n, m = len(s), len(t)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        d[i][0] = d[i - 1][0] + cost(s[i - 1], GAP)
    for j in range(1, m + 1):
        d[0][j] = d[0][j - 1] + cost(GAP, t[j - 1])
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j - 1] + cost(s[i - 1], t[j - 1]),
                          d[i - 1][j] + cost(s[i - 1], GAP),
                          d[i][j - 1] + cost(GAP, t[j - 1]))
    a, b = [], []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and d[i][j] == d[i - 1][j - 1] + cost(s[i - 1], t[j - 1]):
            a.append(s[i - 1])
            b.append(t[j - 1])
            i, j = i - 1, j - 1
        elif i > 0 and d[i][j] == d[i - 1][j] + cost(s[i - 1], GAP):
            a.append(s[i - 1])
            b.append(GAP)
            i -= 1
        else:
            a.append(GAP)
            b.append(t[j - 1])
            j -= 1
    return d[n][m], "".join(reversed(a)), "".join(reversed(b))


def merge(rows: list[str], center_row: int, c2: str, t2: str) -> list[str]:
    """Add the pairwise alignment (c2, t2) of the center and a new sequence to rows.

    rows[center_row] and c2 spell the same center sequence with gaps.
    A gap already in rows stays a gap ("once a gap, always a gap").
    Time O(k L) for k rows and a result of L columns.
    """
    cols: list[list[str]] = []
    p, q = 0, 0  # @line L8
    width = len(rows[0]) if rows else 0
    while p < width or q < len(c2):  # @line L9
        if p < width and q < len(c2) and (rows[center_row][p] == GAP) == (c2[q] == GAP):  # @line L10
            cols.append([r[p] for r in rows] + [t2[q]])
            p, q = p + 1, q + 1
        elif p < width and rows[center_row][p] == GAP:  # @line L11
            cols.append([r[p] for r in rows] + [GAP])
            p += 1
        else:  # @line L12
            cols.append([GAP] * len(rows) + [t2[q]])
            q += 1
    return ["".join(col[r] for col in cols) for r in range(len(rows) + 1)]  # @line L13


def center_star_method(seqs: list[str], cost: Cost = unit_cost) -> list[str]:
    """Return a multiple alignment of seqs (rows in input order).

    Precondition: cost is symmetric with cost(GAP, GAP) = 0. If cost is a
    metric, the SP cost of the result is at most (2 - 2/k) times optimal.
    Time O(k^2 n^2) for k sequences of length at most n.
    """
    k = len(seqs)
    if k == 0:
        return []
    dist = [[0] * k for _ in range(k)]
    for i in range(k):  # @line L1
        for j in range(i + 1, k):
            dist[i][j] = dist[j][i] = pairwise(seqs[i], seqs[j], cost)[0]
    c = min(range(k), key=lambda i: (sum(dist[i]), i))  # @line L2
    rows = [seqs[c]]  # @line L3
    order = [c]
    for i in range(k):  # @line L4
        if i == c:
            continue
        _, c2, t2 = pairwise(seqs[c], seqs[i], cost)  # @line L5
        rows = merge(rows, 0, c2, t2)  # @line L6
        order.append(i)
    result = [""] * k
    for pos, i in enumerate(order):
        result[i] = rows[pos]
    return result  # @line L7


def sp_cost(rows: list[str], cost: Cost = unit_cost) -> int:
    """Sum-of-pairs cost of an alignment, with gap-gap pairs scored by cost(GAP, GAP)."""
    total = 0
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            total += sum(cost(x, y) for x, y in zip(rows[i], rows[j]))
    return total
