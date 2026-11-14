# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leaps-and-bounds/. The authors are listed in prov/EKM5SR.jsonl.
"""Leaps and bounds: the best subsets of each size for least squares, by branch and bound.

The model is y = b0 + X_S b_S + e with an intercept that is always in the
model and a subset S of the p columns of X. For each size s = 0, ..., p the
search returns the nbest subsets of size s with the smallest residual sum of
squares RSS(S), the same answer as the check of all 2^p subsets.

The search tree is binary. A node is a pair (F, C): every subset T with
F <= T <= F | C is below it. The node keeps two swept copies of the centered
cross-product matrix: R is swept on F and holds RSS(F), and B is swept on
F | C and holds RSS(F | C). Since a subset never has a smaller RSS than a
superset, RSS(F | C) is a lower bound for every subset below the node. If no
size in [|F|, |F| + |C|] can still use a subset with RSS at or above this
bound, the node is cut. Otherwise the node branches on one column c of C:
the "in" child sweeps c into R, the "out" child sweeps c out of B, so each
child costs one sweep of a (p + 1) x (p + 1) matrix (Furnival and Wilson 1974
use a pair of such trees; this is the same bound with a binary tree).
The arithmetic is generic, so Fraction input gives exact results.
"""

import math
from fractions import Fraction
from typing import NamedTuple

COLLINEAR_TOL = 1e-10


def _total(values):
    values = list(values)
    if values and all(isinstance(v, float) for v in values):
        return math.fsum(values)
    return sum(values, Fraction(0) if values and isinstance(values[0], Fraction) else 0)


def centered_sscp(x, y):
    """The (p + 1) x (p + 1) matrix of centered sums of squares and cross products of [X, y]."""
    n = len(y)
    if n == 0 or len(x) != n:
        raise ValueError("X and y need the same positive number of rows")
    cols = [[row[j] for row in x] for j in range(len(x[0]))] + [list(y)]
    means = [_total(c) / n for c in cols]
    dev = [[v - m for v in c] for c, m in zip(cols, means)]
    m = len(cols)
    a = [[None] * m for _ in range(m)]
    for i in range(m):
        for j in range(i, m):
            a[i][j] = a[j][i] = _total(u * v for u, v in zip(dev[i], dev[j]))
    return a


def sweep(a, k, reverse=False):
    """Sweep (or reverse sweep) the symmetric matrix a on index k, in place (Goodnight 1979)."""
    d = a[k][k]
    if d == 0:
        raise ZeroDivisionError("zero pivot in sweep")
    m = len(a)
    s = -1 if reverse else 1
    col = [a[i][k] for i in range(m)]
    for i in range(m):
        if i == k:
            continue
        f = col[i] / d
        if f != 0:
            row_i = a[i]
            for j in range(m):
                if j != k:
                    row_i[j] -= f * col[j]
    for i in range(m):
        if i != k:
            a[i][k] = s * col[i] / d
            a[k][i] = s * col[i] / d
    a[k][k] = -1 / d


class LeapsResult(NamedTuple):
    best: list    # best[s] = list of (rss, subset) for size s, smallest RSS first, at most nbest items
    nodes: int    # nodes of the search tree that were visited
    sweeps: int   # sweeps done, including the p sweeps of the root bound matrix


def leaps_and_bounds(x, y, nbest=1):
    """The nbest subsets of each size with the smallest RSS, in a model with an intercept."""
    if nbest < 1:
        raise ValueError("nbest must be at least 1")
    a = centered_sscp(x, y)  # @line L1
    p = len(a) - 1
    yy = p
    if len(y) < p + 2:
        raise ValueError("need n >= p + 2")
    d0 = [a[j][j] for j in range(p)]
    full = [row[:] for row in a]
    for j in range(p):
        if not full[j][j] > COLLINEAR_TOL * d0[j]:
            raise ValueError("the columns of X (with the intercept) are linearly dependent")
        sweep(full, j)  # @line L2
    best = [[] for _ in range(p + 1)]
    seen = set()
    stats = {"nodes": 0, "sweeps": p}

    def record(subset, rss):
        key = tuple(sorted(subset))
        if key in seen:
            return
        seen.add(key)
        lst = best[len(key)]
        if len(lst) < nbest or rss < lst[-1][0]:
            lst.append((rss, key))
            lst.sort(key=lambda t: t[0])
            if len(lst) > nbest:
                lst.pop()

    def cutoff(s):
        lst = best[s]
        return lst[-1][0] if len(lst) == nbest else math.inf

    def visit(f, c, r, b):
        stats["nodes"] += 1
        if not c:  # @line L6
            return
        bound = b[yy][yy]
        if all(cutoff(s) <= bound for s in range(len(f), len(f) + len(c) + 1)):  # @line L7
            return
        # Branch on the column whose removal from F | C raises the RSS most.
        j = max(c, key=lambda k: b[k][yy] * b[k][yy] / -b[k][k])  # @line L8
        rest = [k for k in c if k != j]
        r_in = [row[:] for row in r]
        sweep(r_in, j)  # @line L9
        stats["sweeps"] += 1
        record(f + [j], r_in[yy][yy])  # @line L9
        visit(f + [j], rest, r_in, b)  # @line L10
        b_out = [row[:] for row in b]
        sweep(b_out, j, reverse=True)  # @line L11
        stats["sweeps"] += 1
        record(f + rest, b_out[yy][yy])  # @line L11
        visit(f, rest, r, b_out)  # @line L12

    record([], a[yy][yy])  # @line L3
    record(list(range(p)), full[yy][yy])  # @line L3
    visit([], list(range(p)), a, full)  # @line L4
    return LeapsResult(best, stats["nodes"], stats["sweeps"])  # @line L5
