# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subproduct-tree/. The authors are listed in prov/1HPPT6.jsonl.
"""The subproduct tree of n points, with remainder descent and linear combination.

Polynomials are coefficient lists, lowest degree first; the zero polynomial
is []. Coefficients may be of any type with +, -, * and == 0 that models a
commutative ring (int, Fraction, a class for Z/pZ). Only interpolate needs a
field. This file multiplies and divides with the schoolbook methods, so here
M(n) is O(n^2); the structure of the tree is the same with fast arithmetic.
"""

from __future__ import annotations

from typing import Any, Sequence

Poly = list[Any]
Tree = list[list[Poly]]


def _strip(a: Poly) -> Poly:
    while a and a[-1] == 0:
        a.pop()
    return a


def _mul(a: Sequence[Any], b: Sequence[Any]) -> Poly:
    if not a or not b:
        return []
    c = [a[0] * 0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            c[i + j] = c[i + j] + x * y
    return _strip(c)


def _add(a: Sequence[Any], b: Sequence[Any]) -> Poly:
    if len(a) < len(b):
        a, b = b, a
    c = list(a)
    for i, y in enumerate(b):
        c[i] = c[i] + y
    return _strip(c)


def _rem_monic(f: Sequence[Any], g: Sequence[Any]) -> Poly:
    """f rem g for a monic g of degree at least 1, by schoolbook division."""
    r = list(f)
    n = len(g) - 1
    for k in range(len(r) - 1, n - 1, -1):
        t = r[k]
        if t != 0:
            for j in range(n):
                r[k - n + j] = r[k - n + j] - t * g[j]
        r[k] = t * 0
    return _strip(r[:n])


def build(points: Sequence[Any]) -> Tree:
    """The levels T[0], T[1], ..., T[k] of the subproduct tree of the points.

    Precondition: at least one point. Node T[h][i] is the monic product of
    x - u_j over i 2^h <= j < min((i + 1) 2^h, n), and T[k] = [m] with
    m = prod (x - u_j). Cost: O(M(n) log n) ring operations, n ceil(log2 n)
    + O(n) stored coefficients; with this file's schoolbook product, O(n^2).
    """
    if not points:
        raise ValueError("the subproduct tree needs at least one point")
    one = points[0] - points[0] + 1
    tree: Tree = [[[-u, one] for u in points]]  # @line L1
    h = 0  # @line L2
    while len(tree[h]) > 1:  # @line L3
        level = tree[h]
        nxt: list[Poly] = []  # @line L4
        for i in range(0, len(level) - 1, 2):  # @line L5
            nxt.append(_mul(level[i], level[i + 1]))  # @line L6
        if len(level) % 2 == 1:  # @line L7
            nxt.append(level[-1])
        tree.append(nxt)
        h += 1  # @line L8
    return tree  # @line L9


def evaluate(tree: Tree, f: Sequence[Any]) -> list[Any]:
    """The values f(u_0), ..., f(u_{n-1}) by remainder descent down the tree.

    Precondition: tree comes from build. Cost: O(M(n) log n) ring operations
    with fast division when deg f < n, plus one division of f by the root.
    """
    leaves = tree[0]
    zero = leaves[0][1] * 0
    r = [_rem_monic(f, tree[-1][0])]
    for h in range(len(tree) - 2, -1, -1):
        level = tree[h]
        r = [r[i // 2] if len(level[i]) > len(r[i // 2]) else _rem_monic(r[i // 2], level[i])
             for i in range(len(level))]
    return [v[0] if v else zero for v in r]


def combine(tree: Tree, c: Sequence[Any]) -> Poly:
    """The polynomial sum of c_j m / (x - u_j), built up the tree.

    Precondition: tree comes from build and len(c) equals the number of
    points. Cost: O(M(n) log n) ring operations.
    """
    r: list[Poly] = [_strip([v]) for v in c]
    for h in range(len(tree) - 1):
        level = tree[h]
        nxt: list[Poly] = []
        for i in range(0, len(level) - 1, 2):
            nxt.append(_add(_mul(r[i], level[i + 1]), _mul(r[i + 1], level[i])))
        if len(level) % 2 == 1:
            nxt.append(r[-1])
        r = nxt
    return r[0]


def interpolate(points: Sequence[Any], values: Sequence[Any]) -> Poly:
    """The polynomial of degree less than n with f(u_j) = v_j.

    Precondition: the coefficients form a field and the points are distinct;
    a repeated point raises ZeroDivisionError. Cost: O(M(n) log n) field
    operations and n inversions.
    """
    tree = build(points)
    m = tree[-1][0]
    dm = _strip([k * m[k] for k in range(1, len(m))])
    s = evaluate(tree, dm)
    return combine(tree, [v / w for v, w in zip(values, s)])
