# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/birkhoff-von-neumann-decomposition/. The authors are listed in prov/YCNDFQ.jsonl.

"""Birkhoff-von Neumann decomposition with exact rational arithmetic.

decompose(M) writes a doubly stochastic matrix M as a convex combination
sum_k w_k P_k of permutation matrices. Each step finds a perfect matching on
the support of M (it exists by Hall's theorem), takes the smallest entry w on
it, and subtracts w times that permutation. At least one entry becomes zero
in each step. The matching of the previous step is kept, the edges that
became zero are dropped, and augmenting paths repair it.

A permutation is a list perm with perm[i] = the column of row i.
"""

from fractions import Fraction

Matrix = list[list[Fraction]]


def is_doubly_stochastic(m: Matrix) -> bool:
    n = len(m)
    return (
        all(len(row) == n for row in m)
        and all(x >= 0 for row in m for x in row)
        and all(sum(row) == 1 for row in m)
        and all(sum(m[i][j] for i in range(n)) == 1 for j in range(n))
    )


def _augment(adj: list[list[int]], row_of: list[int], col_of: list[int], start: int) -> bool:
    """Find an augmenting path from the free row start (iterative DFS)."""
    n = len(adj)
    seen = [False] * n
    parent_col = {}  # column -> row from which we reached it
    stack = [(start, 0)]
    while stack:
        r, k = stack.pop()
        if k >= len(adj[r]):
            continue
        stack.append((r, k + 1))
        c = adj[r][k]
        if seen[c]:
            continue
        seen[c] = True
        parent_col[c] = r
        if col_of[c] < 0:
            # Flip the path that ends at the free column c.
            while True:
                r = parent_col[c]
                prev = row_of[r]
                row_of[r], col_of[c] = c, r
                if r == start:
                    return True
                c = prev
        stack.append((col_of[c], 0))
    return False


def perfect_matching(support: list[list[bool]], row_of: list[int] | None = None) -> list[int] | None:
    """A perfect matching inside support, grown from a partial matching row_of."""
    n = len(support)
    adj = [[j for j in range(n) if support[i][j]] for i in range(n)]
    row_of = [-1] * n if row_of is None else list(row_of)
    col_of = [-1] * n
    for i, j in enumerate(row_of):
        if j >= 0:
            col_of[j] = i
    for i in range(n):  # greedy start: take the first free column
        if row_of[i] < 0:
            for j in adj[i]:
                if col_of[j] < 0:
                    row_of[i], col_of[j] = j, i
                    break
    for i in range(n):
        if row_of[i] < 0 and not _augment(adj, row_of, col_of, i):
            return None
    return row_of


def decompose(m: Matrix) -> list[tuple[Fraction, list[int]]]:
    """Return [(w_k, perm_k)] with w_k > 0, sum w_k = 1 and sum w_k P_k = m."""
    if not is_doubly_stochastic(m):
        raise ValueError("matrix is not doubly stochastic")
    n = len(m)
    r = [row[:] for row in m]  # r = m - (the terms so far); its row sums are `left`
    left = Fraction(1)
    terms = []
    perm = None
    while left > 0:
        support = [[r[i][j] > 0 for j in range(n)] for i in range(n)]
        if perm is not None:
            perm = [j if r[i][j] > 0 else -1 for i, j in enumerate(perm)]
        perm = perfect_matching(support, perm)
        if perm is None:  # cannot happen, by Hall's theorem
            raise AssertionError("no perfect matching on the support")
        w = min(r[i][perm[i]] for i in range(n))
        for i in range(n):
            r[i][perm[i]] -= w
        left -= w
        terms.append((w, perm[:]))
    return terms


def recompose(terms: list[tuple[Fraction, list[int]]], n: int) -> Matrix:
    m = [[Fraction(0)] * n for _ in range(n)]
    for w, perm in terms:
        for i, j in enumerate(perm):
            m[i][j] += w
    return m


def complete_substochastic(m: Matrix) -> Matrix:
    """Raise entries of a matrix with row and column sums <= 1 to make it doubly stochastic.

    While some row i and some column j have a deficit, add the smaller of the two
    deficits to entry (i, j). Each step fills a row or a column, so there are
    at most 2n - 1 steps.
    """
    n = len(m)
    a = [row[:] for row in m]
    row_def = [1 - sum(a[i]) for i in range(n)]
    col_def = [1 - sum(a[i][j] for i in range(n)) for j in range(n)]
    if any(d < 0 for d in row_def + col_def) or any(x < 0 for row in a for x in row):
        raise ValueError("matrix is not doubly substochastic")
    i = j = 0
    while True:
        while i < n and row_def[i] == 0:
            i += 1
        while j < n and col_def[j] == 0:
            j += 1
        if i == n or j == n:
            break
        d = min(row_def[i], col_def[j])
        a[i][j] += d
        row_def[i] -= d
        col_def[j] -= d
    return a


def frame_schedule(k: list[list[int]], frame: int) -> list[list[int]]:
    """Slots of a frame that serve k[i][j] cells from input i to output j.

    The row and column sums of k must be at most frame. The result is a list
    of frame permutations; pair (i, perm[i]) is used k[i][j] times in total,
    plus idle uses that come from the completion step.
    """
    n = len(k)
    m = [[Fraction(x, frame) for x in row] for row in k]
    terms = decompose(complete_substochastic(m))
    slots = []
    for w, perm in terms:
        count = w * frame
        if count.denominator != 1:  # integer input gives integer weights
            raise AssertionError("weight is not a multiple of 1/frame")
        slots.extend([perm] * count.numerator)
    return slots
