# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wilber-algorithm/. The authors are listed in prov/BV1WAB.jsonl.

"""Wilber's algorithm: the concave least weight subsequence problem in O(n).

F(0) = 0 and F(j) = min over 0 <= i < j of F(i) + w(i, j), for j = 1 .. n,
where w(i, j) + w(i', j') <= w(i, j') + w(i', j) for all i <= i' < j <= j'
(concave in the word of Hirschberg and Larmore, the Monge or quadrangle
inequality). Let B(i, j) = F(i) + w(i, j) for i < j and +infinity for
i >= j. B is a Monge array, so its column minima can be found with SMAWK in
time linear in its size. SMAWK cannot run on all of B at once, because the
row i is known only after the column i is done. Wilber guesses the values of
a block of columns from the rows that are known, uses the guesses to check
them, and moves to the first column where the check fails.

The state is (c, r): F(0) .. F(c) are final, and for every column after c,
some row in r .. c is at least as good as every row before r.

w must be finite. If w(i, j) = math.inf marks a line that is too long, two
infinite entries compare equal and SMAWK can drop the wrong row. Use a large
finite penalty that keeps the inequality instead, for example
K * max(0, S_j - S_i - l_max) with K large: it is a convex function of the
width S_j - S_i, so the weight stays concave.
"""

import math
from typing import Callable, Dict, List, Optional, Sequence, Tuple

Weight = Callable[[int, int], float]


def smawk(rows: Sequence[int], cols: Sequence[int], f: Callable[[int, int], float]) -> Dict[int, int]:
    """Row minima of a totally monotone array: {row: the leftmost column of its minimum}.

    The array is given by f(row, col). Its rows and columns are in the order
    of the lists. The cost is O(len(rows) + len(cols)) evaluations of f.
    """
    result: Dict[int, int] = {}

    def solve(rows: Sequence[int], cols: Sequence[int]) -> None:
        if not rows:
            return
        stack: List[int] = []  # REDUCE: keep at most len(rows) columns
        for c in cols:
            while stack and f(rows[len(stack) - 1], stack[-1]) > f(rows[len(stack) - 1], c):
                stack.pop()
            if len(stack) < len(rows):
                stack.append(c)
        solve(rows[1::2], stack)
        k = 0
        for t in range(0, len(rows), 2):  # interpolate the even rows
            row = rows[t]
            stop = result[rows[t + 1]] if t + 1 < len(rows) else stack[-1]
            best, bv = stack[k], f(row, stack[k])
            while stack[k] != stop:
                k += 1
                v = f(row, stack[k])
                if v < bv:
                    best, bv = stack[k], v
            result[row] = best

    solve(list(rows), list(cols))
    return result


def wilber(n: int, w: Weight, stats: Optional[dict] = None) -> Tuple[List, List[int]]:
    """F[0..n] and the best predecessor P[1..n], with O(n) evaluations of w."""
    evals = 0
    F: List = [0] + [math.inf] * n
    P = [0] * (n + 1)
    G: List = list(F)  # the guesses: F for columns <= c, tentative values after c

    def B(j: int, i: int):  # the entry of row i and column j, from the guesses
        nonlocal evals
        if i >= j:
            return math.inf
        evals += 1
        return G[i] + w(i, j)

    c, r = 0, 0  # @line W1
    while c < n:  # @line W2
        p = min(2 * c - r + 1, n)  # @line W3
        # guesses for the columns c+1 .. p from the final rows r .. c
        cols = list(range(c + 1, p + 1))
        arg = smawk(cols, list(range(r, c + 1)), B)  # @line W4
        for j in cols:
            G[j], P[j] = B(j, arg[j]), arg[j]  # @line W5
        # check: can a row in c+1 .. p-1, with the guessed values, beat a guess?
        j0 = None
        if p >= c + 2:
            cols2 = list(range(c + 2, p + 1))
            arg2 = smawk(cols2, list(range(c + 1, p)), B)  # @line W6
            for j in cols2:
                if B(j, arg2[j]) < G[j]:  # @line W7
                    j0 = j
                    break
        if j0 is None:  # @line W8
            for j in cols:
                F[j] = G[j]
            c = p  # @line W9
        else:
            for j in range(c + 1, j0):
                F[j] = G[j]
            G[j0] = F[j0] = B(j0, arg2[j0])  # @line W10
            P[j0] = arg2[j0]
            r, c = c + 1, j0  # @line W11
    if stats is not None:
        stats["evals"] = evals
    return F, P  # @line W12
