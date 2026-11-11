# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-alphabetic-code/. The authors are listed in prov/GS71SB.jsonl.

"""Optimal alphabetic codes by dynamic programming over intervals.

An alphabetic code for symbols 0..n-1 in a fixed order is a full binary
tree whose leaves, read from left to right, are the symbols in that
order. Its cost is sum(w[i] * depth[i]). With W(i, j) = w[i] + ... + w[j]:

    c(i, i) = 0
    c(i, j) = W(i, j) + min over i <= k < j of c(i, k) + c(k + 1, j)

where k is the last leaf of the left subtree.

alphabetic_cubic tries every k: O(n^3) time (Gilbert and Moore 1959).
alphabetic_knuth only tries cut[i][j - 1] <= k <= cut[i + 1][j]: O(n^2)
time (Knuth 1971). This is valid because the cost W is additive over
intervals, so it satisfies the quadrangle inequality with equality and
is monotone under inclusion (Yao 1980); it is also the optimal binary
search tree problem with all key weights zero, which Knuth's theorem
covers directly.
"""

from typing import Sequence


def _prefix(weights: Sequence[int]) -> list[int]:
    pre = [0]
    for w in weights:
        pre.append(pre[-1] + w)
    return pre


def _depths(cut: list[list[int]], n: int) -> list[int]:
    depth = [0] * n
    stack = [(0, n - 1, 0)]
    while stack:
        i, j, d = stack.pop()
        if i == j:
            depth[i] = d
            continue
        k = cut[i][j]
        stack.append((i, k, d + 1))
        stack.append((k + 1, j, d + 1))
    return depth


def alphabetic_cubic(weights: Sequence[int]) -> tuple[int, list[int]]:
    """Least cost and the leaf depths, trying every split: O(n^3)."""
    n = len(weights)
    if n == 0:
        raise ValueError("need at least one symbol")
    pre = _prefix(weights)
    c = [[0] * n for _ in range(n)]
    cut = [[i] * n for i in range(n)]
    for size in range(2, n + 1):
        for i in range(n - size + 1):
            j = i + size - 1
            best, arg = None, i
            for k in range(i, j):
                v = c[i][k] + c[k + 1][j]
                if best is None or v < best:
                    best, arg = v, k
            c[i][j] = best + pre[j + 1] - pre[i]
            cut[i][j] = arg
    return c[0][n - 1], _depths(cut, n)


def alphabetic_knuth(weights: Sequence[int]) -> tuple[int, list[int], list[list[int]]]:
    """Least cost, leaf depths and the table of best splits: O(n^2).

    cut[i][j] is the smallest best split of the interval i..j. The search
    for it is limited to cut[i][j - 1] .. cut[i + 1][j]; the total work for
    each interval size telescopes to O(n).
    """
    n = len(weights)
    if n == 0:
        raise ValueError("need at least one symbol")
    pre = _prefix(weights)
    c = [[0] * n for _ in range(n)]
    cut = [[i] * n for i in range(n)]
    for i in range(n - 1):
        c[i][i + 1] = weights[i] + weights[i + 1]
        cut[i][i + 1] = i
    for size in range(3, n + 1):
        for i in range(n - size + 1):
            j = i + size - 1
            lo, hi = cut[i][j - 1], min(cut[i + 1][j], j - 1)
            best, arg = None, lo
            for k in range(lo, hi + 1):
                v = c[i][k] + c[k + 1][j]
                if best is None or v < best:
                    best, arg = v, k
            c[i][j] = best + pre[j + 1] - pre[i]
            cut[i][j] = arg
    return c[0][n - 1], _depths(cut, n), cut


def codewords(depths: Sequence[int]) -> list[str]:
    """The codewords of an alphabetic tree from its leaf depths, left to right."""
    if len(depths) == 1:
        return [""]
    words, code, prev = [], 0, None
    for d in depths:
        if prev is not None:
            code = (code + 1) << (d - prev) if d >= prev else (code + 1) >> (prev - d)
        words.append(format(code, "0{}b".format(d)))
        prev = d
    return words


def brute_force(weights: Sequence[int]) -> int:
    """Least cost over all full binary trees with the leaves in order."""

    def trees(i: int, j: int):
        if i == j:
            yield [0]
            return
        for k in range(i, j):
            for left in trees(i, k):
                for right in trees(k + 1, j):
                    yield [d + 1 for d in left + right]

    return min(sum(w * d for w, d in zip(weights, ds)) for ds in trees(0, len(weights) - 1))
