# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-bst-dynamic-programming/. The authors are listed in prov/5HF5N0.jsonl.

"""Optimal binary search trees by dynamic programming (CLRS OPTIMAL-BST)."""

from typing import Any, Sequence


def optimal_bst(p: Sequence[Any], q: Sequence[Any]) -> tuple[list[list[Any]], list[list[int]]]:
    """Return the tables (e, root) of the optimal BST dynamic program.

    p[1..n] are the key weights (p[0] is ignored) and q[0..n] the gap weights.
    e[i][j] is the minimum expected cost (CLRS form, dummy leaves counted) of a
    subtree on keys i..j, for 1 <= i <= n + 1 and i - 1 <= j <= n.
    root[i][j] is a root of an optimal subtree for 1 <= i <= j <= n; ties go to
    the smallest root. Weights may be int, Fraction or float. O(n^3) time.
    """
    n = len(q) - 1
    if len(p) != n + 1:
        raise ValueError("p must have length len(q), with p[0] unused")
    e: list[list[Any]] = [[0] * (n + 1) for _ in range(n + 2)]
    w: list[list[Any]] = [[0] * (n + 1) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 2):  # @line L1
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]
    for length in range(1, n + 1):  # @line L2
        for i in range(1, n - length + 2):  # @line L3
            j = i + length - 1  # @line L4
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            best = None
            for r in range(i, j + 1):  # @line L5
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]  # @line L6
                if best is None or t < best:  # @line L7
                    best = t
                    root[i][j] = r
            e[i][j] = best
    return e, root  # @line L8


def optimal_bst_knuth(p: Sequence[Any], q: Sequence[Any]) -> tuple[Any, list[list[int]]]:
    """Knuth's O(n^2) version: search r only in root[i][j-1] .. root[i+1][j].

    Ties go to the smallest root, so the tables match optimal_bst.
    """
    n = len(q) - 1
    e: list[list[Any]] = [[0] * (n + 1) for _ in range(n + 2)]
    w: list[list[Any]] = [[0] * (n + 1) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 2)]
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            lo = i if length == 1 else root[i][j - 1]
            hi = j if length == 1 else root[i + 1][j]
            best = None
            for r in range(lo, hi + 1):
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if best is None or t < best:
                    best = t
                    root[i][j] = r
            e[i][j] = best
    return (e[1][n] if n >= 1 else q[0]), root


def build_tree(root: list[list[int]], n: int) -> dict[int, tuple[int, int]]:
    """Return {key: (left child, right child)} of the tree in the root table (0 = none)."""
    children: dict[int, tuple[int, int]] = {}
    if n == 0:
        return children
    stack = [(1, n)]
    while stack:
        i, j = stack.pop()
        r = root[i][j]
        left = root[i][r - 1] if i <= r - 1 else 0
        right = root[r + 1][j] if r + 1 <= j else 0
        children[r] = (left, right)
        if i <= r - 1:
            stack.append((i, r - 1))
        if r + 1 <= j:
            stack.append((r + 1, j))
    return children


def tree_cost(children: dict[int, tuple[int, int]], top: int, p: Sequence[Any], q: Sequence[Any]) -> Any:
    """Expected cost (CLRS form) of a BST given as a child map with root top."""
    n = len(q) - 1
    if n == 0:
        return q[0]
    total: Any = 0
    stack = [(top, 0)]
    while stack:
        k, d = stack.pop()
        total += p[k] * (d + 1)
        left, right = children[k]
        if left:
            stack.append((left, d + 1))
        else:
            total += q[k - 1] * (d + 2)  # the gap d_{k-1} is a leaf below k
        if right:
            stack.append((right, d + 1))
        else:
            total += q[k] * (d + 2)  # the gap d_k
    return total
