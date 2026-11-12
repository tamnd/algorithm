# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sankoff-rna-algorithm/. The authors are listed in prov/XKWWEX.jsonl.

"""Sankoff-style simultaneous alignment and folding of two RNA sequences.

The toy score of a joint solution (an alignment of x and y with a nested
structure on its columns) is

    sum over match columns of s(a, b)          (match or mismatch)
  - d for each gap column                      (linear gap penalty)
  + bonus for each consensus base pair.

A consensus base pair joins two match columns (x_i, y_k) and (x_h, y_q) with
i < h and k < q. Both x_i x_h and y_k y_q must be allowed pairs (Watson-Crick
or G-U), and each hairpin must hold at least hmin bases in each sequence:
h - i - 1 >= hmin and q - k - 1 >= hmin. Pseudoknots are not allowed.
"""

from typing import Optional

GAP = "-"
NEG = float("-inf")
PAIRS = {("A", "U"), ("U", "A"), ("G", "C"), ("C", "G"), ("G", "U"), ("U", "G")}


def can_pair(a: str, b: str) -> bool:
    """Return True when a and b form a Watson-Crick or G-U pair."""
    return (a, b) in PAIRS


def sankoff_table(x: str, y: str, match: int = 1, mismatch: int = -1, d: int = 1,
                  bonus: int = 3, hmin: int = 1) -> list:
    """Fill the table D[i][j][k][l]: the best score for x[i:j] against y[k:l].

    Cost: Theta(m^2 n^2) cells and O(m^3 n^3) time for |x| = m, |y| = n.
    """
    m, n = len(x), len(y)
    D = [[[[NEG] * (n + 1) for _ in range(n + 1)] for _ in range(m + 1)] for _ in range(m + 1)]
    for lx in range(m + 1):  # @line L1
        for ly in range(n + 1):  # @line L2
            for i in range(m - lx + 1):  # @line L3
                j = i + lx  # @line L4
                for k in range(n - ly + 1):
                    l = k + ly
                    if lx == 0 or ly == 0:  # @line L5
                        D[i][j][k][l] = -d * (lx + ly)
                        continue
                    sig = match if x[i] == y[k] else mismatch
                    best = D[i + 1][j][k][l] - d  # @line L6
                    v = D[i][j][k + 1][l] - d  # @line L7
                    if v > best:
                        best = v
                    v = D[i + 1][j][k + 1][l] + sig  # @line L8
                    if v > best:
                        best = v
                    for h in range(i + hmin + 1, j):  # @line L9
                        if not can_pair(x[i], x[h]):
                            continue
                        for q in range(k + hmin + 1, l):  # @line L10
                            if not can_pair(y[k], y[q]):
                                continue
                            sig2 = match if x[h] == y[q] else mismatch
                            v = sig + sig2 + bonus + D[i + 1][h][k + 1][q] + D[h + 1][j][q + 1][l]  # @line L11
                            if v > best:
                                best = v
                    D[i][j][k][l] = best  # @line L12
    return D  # @line L13: the score is D[0][m][0][n]


def sankoff(x: str, y: str, match: int = 1, mismatch: int = -1, d: int = 1,
            bonus: int = 3, hmin: int = 1) -> tuple:
    """Return (score, top row, bottom row, structure) of an optimal joint solution.

    The rows use "-" for a gap. The structure is a dot-bracket string over
    the alignment columns. Ties go to a gap in y, then a gap in x, then an
    unpaired match column, then the first pair found.
    """
    m, n = len(x), len(y)
    D = sankoff_table(x, y, match, mismatch, d, bonus, hmin)
    # Each task is a subproblem (i, j, k, l) or a literal column to output.
    top: list = []
    bot: list = []
    st: list = []
    stack: list = [("sub", 0, m, 0, n)]
    while stack:
        task = stack.pop()
        if task[0] == "col":
            top.append(task[1])
            bot.append(task[2])
            st.append(task[3])
            continue
        _, i, j, k, l = task
        if i == j or k == l:
            for p in range(i, j):
                top.append(x[p]); bot.append(GAP); st.append(".")
            for p in range(k, l):
                top.append(GAP); bot.append(y[p]); st.append(".")
            continue
        val = D[i][j][k][l]
        sig = match if x[i] == y[k] else mismatch
        if D[i + 1][j][k][l] - d == val:
            stack.append(("sub", i + 1, j, k, l))
            stack.append(("col", x[i], GAP, "."))
            continue
        if D[i][j][k + 1][l] - d == val:
            stack.append(("sub", i, j, k + 1, l))
            stack.append(("col", GAP, y[k], "."))
            continue
        if D[i + 1][j][k + 1][l] + sig == val:
            stack.append(("sub", i + 1, j, k + 1, l))
            stack.append(("col", x[i], y[k], "."))
            continue
        found: Optional[tuple] = None
        for h in range(i + hmin + 1, j):
            if found or not can_pair(x[i], x[h]):
                continue
            for q in range(k + hmin + 1, l):
                if not can_pair(y[k], y[q]):
                    continue
                sig2 = match if x[h] == y[q] else mismatch
                if sig + sig2 + bonus + D[i + 1][h][k + 1][q] + D[h + 1][j][q + 1][l] == val:
                    found = (h, q)
                    break
        assert found is not None
        h, q = found
        # Pushed in reverse order of output.
        stack.append(("sub", h + 1, j, q + 1, l))
        stack.append(("col", x[h], y[q], ")"))
        stack.append(("sub", i + 1, h, k + 1, q))
        stack.append(("col", x[i], y[k], "("))
    return D[0][m][0][n], "".join(top), "".join(bot), "".join(st)


def score_solution(top: str, bot: str, struct: str, match: int = 1, mismatch: int = -1,
                   d: int = 1, bonus: int = 3, hmin: int = 1) -> int:
    """Score a joint solution directly, and check that it is valid."""
    assert len(top) == len(bot) == len(struct)
    xpos, ypos, total, stack = [], [], 0, []
    px = py = 0
    for c in range(len(top)):
        a, b = top[c], bot[c]
        assert not (a == GAP and b == GAP)
        xpos.append(px if a != GAP else None)
        ypos.append(py if b != GAP else None)
        px += a != GAP
        py += b != GAP
        if a == GAP or b == GAP:
            total -= d
        else:
            total += match if a == b else mismatch
    for c, ch in enumerate(struct):
        if ch == "(":
            stack.append(c)
        elif ch == ")":
            o = stack.pop()
            assert top[o] != GAP and bot[o] != GAP and top[c] != GAP and bot[c] != GAP
            assert can_pair(top[o], top[c]) and can_pair(bot[o], bot[c])
            assert xpos[c] - xpos[o] - 1 >= hmin and ypos[c] - ypos[o] - 1 >= hmin
            total += bonus
    assert not stack
    return total
