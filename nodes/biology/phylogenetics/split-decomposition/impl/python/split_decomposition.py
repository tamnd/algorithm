# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-decomposition/. The authors are listed in prov/C536CB.jsonl.

"""Split decomposition of Bandelt and Dress (1992).

The input is a symmetric matrix d with zero diagonal on the taxa 0..n-1. The
isolation index of a split A|B is

    alpha(A|B) = 1/2 * min over a, a' in A and b, b' in B of
                 max{d(a,b) + d(a',b'), d(a,b') + d(a',b), d(a,a') + d(b,b')}
                 - d(a,a') - d(b,b'),

where a = a' and b = b' are allowed. The d-splits are the splits with a
positive index. The algorithm adds the taxa one at a time. A d-split of the
first k taxa restricts to a d-split of the first k - 1 taxa, or it separates
the new taxon from the rest, so the candidates at each step come from the
previous d-splits. The index of a candidate is the old index, combined by a
minimum with the terms that use the new taxon.

A split is stored as the frozenset of its side that does not hold taxon 0.
Use Fraction entries for exact results.
"""

from fractions import Fraction
from typing import Dict, FrozenSet, List, Sequence

Matrix = Sequence[Sequence[Fraction]]
Split = FrozenSet[int]


def _beta(d: Matrix, a: int, a2: int, b: int, b2: int):
    m = max(d[a][b] + d[a2][b2], d[a][b2] + d[a2][b], d[a][a2] + d[b][b2])
    return m - d[a][a2] - d[b][b2]


def isolation_index(d: Matrix, side_a, side_b) -> Fraction:
    """The index by its definition, in O(|A|^2 |B|^2) time."""
    best = None
    for a in side_a:
        for a2 in side_a:
            for b in side_b:
                for b2 in side_b:
                    v = _beta(d, a, a2, b, b2)
                    if best is None or v < best:
                        best = v
    return Fraction(best) / 2


def _with_new(d: Matrix, side_x, side_o, x: int) -> Fraction:
    """Half the min of beta over the terms that use x, where x is in side_x."""
    best = None
    for a in side_x:  # a2 = x, and by symmetry this covers a = x
        for b in side_o:
            for b2 in side_o:
                v = _beta(d, a, x, b, b2)
                if best is None or v < best:
                    best = v
    return Fraction(best) / 2


def split_decomposition(d: Matrix) -> Dict[Split, Fraction]:
    """Return the d-splits with their isolation indices."""
    n = len(d)
    if n < 2:
        return {}
    for i in range(n):
        if d[i][i] != 0 or any(d[i][j] != d[j][i] for j in range(n)):
            raise ValueError("d must be symmetric with a zero diagonal")
    # each entry: (A, B) as lists, and the index on the current taxa
    cur: List = []
    if d[0][1] > 0:
        cur.append(([0], [1], Fraction(d[0][1])))  # @line L1
    for k in range(2, n):  # @line L2
        x = k
        old = list(range(k))
        nxt: List = []  # @line L3
        alpha = _with_new(d, [x], old, x)  # @line L4
        if alpha > 0:
            nxt.append((old, [x], alpha))  # @line L6
        for side_a, side_b, a_old in cur:  # @line L4
            for grow_a in (True, False):
                if grow_a:
                    na, nb = side_a + [x], side_b
                    extra = _with_new(d, na, nb, x)  # @line L5
                else:
                    na, nb = side_a, side_b + [x]
                    extra = _with_new(d, nb, na, x)  # @line L5
                alpha = min(a_old, extra)  # @line L5
                if alpha > 0:
                    nxt.append((na, nb, alpha))  # @line L6
        cur = nxt  # @line L7
    out: Dict[Split, Fraction] = {}
    for side_a, side_b, alpha in cur:
        key = frozenset(side_b) if 0 in side_a else frozenset(side_a)
        out[key] = alpha
    return out  # @line L8


def split_metric(n: int, side: Split, i: int, j: int) -> int:
    return 1 if (i in side) != (j in side) else 0


def residue(d: Matrix, splits: Dict[Split, Fraction]) -> List[List[Fraction]]:
    """d0 = d - sum of alpha_S * delta_S, the split-prime part of d."""
    n = len(d)
    return [[Fraction(d[i][j]) - sum((a * split_metric(n, s, i, j) for s, a in splits.items()), Fraction(0)) for j in range(n)] for i in range(n)]
