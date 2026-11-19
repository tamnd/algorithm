# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eisner-algorithm/. The authors are listed in prov/JTW3A2.jsonl.

"""Eisner's algorithm: the best projective dependency tree under arc-factored scores.

The words are 1..n and 0 is the artificial root. scores[h][d] is the score of
the arc h -> d; the matrix is (n + 1) x (n + 1), and column 0 and the diagonal
are not read. A tree is a head list heads of length n + 1 with heads[0] = -1 and
heads[d] the head of word d. The score of a tree is the sum of the scores of its
n arcs.

eisner() returns a best projective tree and its score. With single_root=True
the root gets exactly one child, as in Universal Dependencies. eisner_inside()
runs the same recursion in any semiring of nlslog: with COUNTING and all weights
1 it counts the projective trees, with LOG and log weights it gives the log of
the partition function, the sum over all projective trees of exp(score).

The scores can be ints, Fractions or floats. No item is stored as None, so
exact arithmetic never meets an infinity.
"""

from typing import List, Optional, Sequence, Tuple

from nlslog import Semiring

LEFT, RIGHT = 0, 1  # LEFT: the head is the right end j; RIGHT: the head is the left end i


def _check(scores: Sequence[Sequence]) -> int:
    n = len(scores) - 1
    if n < 0 or any(len(row) != n + 1 for row in scores):
        raise ValueError("scores must be an (n + 1) x (n + 1) matrix")
    return n


def _better(a, b) -> bool:
    return b is None or (a is not None and a > b)


def eisner(scores: Sequence[Sequence], single_root: bool = False) -> Tuple[object, List[int]]:
    """Return (best score, heads) over the projective trees of words 1..n.

    Ties are broken by the first split point r in increasing order.
    """
    n = _check(scores)
    if n == 0:
        return 0, [-1]
    # C[d][i][j] and I[d][i][j]: best complete and incomplete spans; bc and bi: split points.
    C = [[[None] * (n + 1) for _ in range(n + 1)] for _ in range(2)]
    I = [[[None] * (n + 1) for _ in range(n + 1)] for _ in range(2)]
    bc = [[[0] * (n + 1) for _ in range(n + 1)] for _ in range(2)]
    bi = [[[0] * (n + 1) for _ in range(n + 1)] for _ in range(2)]
    for i in range(n + 1):  # @line L1
        C[LEFT][i][i] = 0
        C[RIGHT][i][i] = 0
    for k in range(1, n + 1):  # @line L2
        for i in range(n - k + 1):  # @line L3
            j = i + k  # @line L4
            best, arg = None, i
            r_max = i if (single_root and i == 0) else j - 1
            for r in range(i, r_max + 1):
                a, b = C[RIGHT][i][r], C[LEFT][r + 1][j]
                if a is not None and b is not None and _better(a + b, best):
                    best, arg = a + b, r
            if best is not None:
                if i > 0:  # @line L5
                    I[LEFT][i][j] = best + scores[j][i]
                    bi[LEFT][i][j] = arg
                I[RIGHT][i][j] = best + scores[i][j]  # @line L6
                bi[RIGHT][i][j] = arg
            best, arg = None, i
            for r in range(i, j):  # @line L7
                a, b = C[LEFT][i][r], I[LEFT][r][j]
                if a is not None and b is not None and _better(a + b, best):
                    best, arg = a + b, r
            C[LEFT][i][j], bc[LEFT][i][j] = best, arg
            best, arg = None, j
            for r in range(i + 1, j + 1):  # @line L8
                a, b = I[RIGHT][i][r], C[RIGHT][r][j]
                if a is not None and b is not None and _better(a + b, best):
                    best, arg = a + b, r
            C[RIGHT][i][j], bc[RIGHT][i][j] = best, arg
    heads = [-1] * (n + 1)
    # Read the tree from the back pointers with an explicit stack.
    stack = [("C", RIGHT, 0, n)]
    while stack:
        kind, d, i, j = stack.pop()
        if i == j:
            continue
        if kind == "C":
            r = bc[d][i][j]
            if d == LEFT:
                stack.append(("C", LEFT, i, r))
                stack.append(("I", LEFT, r, j))
            else:
                stack.append(("I", RIGHT, i, r))
                stack.append(("C", RIGHT, r, j))
        else:
            r = bi[d][i][j]
            if d == LEFT:
                heads[i] = j
            else:
                heads[j] = i
            stack.append(("C", RIGHT, i, r))
            stack.append(("C", LEFT, r + 1, j))
    return C[RIGHT][0][n], heads  # @line L9


def eisner_inside(weights: Sequence[Sequence], sr: Semiring, single_root: bool = False):
    """Return the semiring sum over all projective trees of the product of their arc weights.

    weights[h][d] is the weight of the arc h -> d in the semiring sr. Every
    projective tree has exactly one derivation in the recursion, so nothing is
    counted twice.
    """
    n = _check(weights)
    if n == 0:
        return sr.one
    zero = sr.zero
    C = [[[zero] * (n + 1) for _ in range(n + 1)] for _ in range(2)]
    I = [[[zero] * (n + 1) for _ in range(n + 1)] for _ in range(2)]
    for i in range(n + 1):
        C[LEFT][i][i] = sr.one
        C[RIGHT][i][i] = sr.one
    for k in range(1, n + 1):
        for i in range(n - k + 1):
            j = i + k
            acc = zero
            r_max = i if (single_root and i == 0) else j - 1
            for r in range(i, r_max + 1):
                acc = sr.plus(acc, sr.times(C[RIGHT][i][r], C[LEFT][r + 1][j]))
            if i > 0:
                I[LEFT][i][j] = sr.times(acc, weights[j][i])
            I[RIGHT][i][j] = sr.times(acc, weights[i][j])
            acc = zero
            for r in range(i, j):
                acc = sr.plus(acc, sr.times(C[LEFT][i][r], I[LEFT][r][j]))
            C[LEFT][i][j] = acc
            acc = zero
            for r in range(i + 1, j + 1):
                acc = sr.plus(acc, sr.times(I[RIGHT][i][r], C[RIGHT][r][j]))
            C[RIGHT][i][j] = acc
    return C[RIGHT][0][n]


def tree_score(scores: Sequence[Sequence], heads: Sequence[int]):
    """Return the sum of scores[heads[d]][d] over the words d = 1..n."""
    total = 0
    for d in range(1, len(heads)):
        total = total + scores[heads[d]][d]
    return total


def is_tree(heads: Sequence[int]) -> bool:
    """Return True if every word reaches the root 0 by following heads, with no cycle."""
    n = len(heads) - 1
    if n < 0 or heads[0] != -1:
        return False
    for d in range(1, n + 1):
        if not 0 <= heads[d] <= n or heads[d] == d:
            return False
    for d in range(1, n + 1):
        seen = 0
        x = d
        while x != 0:
            x = heads[x]
            seen += 1
            if seen > n:
                return False
    return True


def is_projective(heads: Sequence[int]) -> bool:
    """Return True if each head dominates every word strictly between it and its dependent."""
    n = len(heads) - 1
    for d in range(1, n + 1):
        h = heads[d]
        lo, hi = min(h, d), max(h, d)
        for k in range(lo + 1, hi):
            x: Optional[int] = k
            while x != h and x != 0:
                x = heads[x]
            if x != h:
                return False
    return True
