# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/calinski-harabasz-index/. The authors are listed in prov/8Z3PGC.jsonl.
"""The Calinski-Harabasz variance ratio criterion, with the scatter matrices W, B and T.

Use Fraction or int coordinates for exact results; floats work too.
"""

from fractions import Fraction
from typing import Hashable, Sequence

Matrix = list


def _mean(rows: list) -> list:
    m = len(rows)
    return [Fraction(sum(r[t] for r in rows), m) for t in range(len(rows[0]))]


def _outer_add(acc: Matrix, u: list, w=1) -> None:
    for s in range(len(u)):
        for t in range(len(u)):
            acc[s][t] += w * u[s] * u[t]


def scatter_matrices(points: Sequence[Sequence], labels: Sequence[Hashable]):
    """Return (W, B, T) as d x d matrices.

    W = sum_c sum_{x in c} (x - m_c)(x - m_c)^T     the within-cluster scatter
    B = sum_c n_c (m_c - m)(m_c - m)^T               the between-cluster scatter
    T = sum_x (x - m)(x - m)^T                       the total scatter
    """
    d = len(points[0])
    groups: dict = {}
    for x, c in zip(points, labels):
        groups.setdefault(c, []).append(list(x))
    m = _mean([list(x) for x in points])
    W = [[Fraction(0)] * d for _ in range(d)]
    B = [[Fraction(0)] * d for _ in range(d)]
    T = [[Fraction(0)] * d for _ in range(d)]
    for rows in groups.values():
        mc = _mean(rows)
        for x in rows:
            _outer_add(W, [x[t] - mc[t] for t in range(d)])
        _outer_add(B, [mc[t] - m[t] for t in range(d)], len(rows))
    for x in points:
        _outer_add(T, [x[t] - m[t] for t in range(d)])
    return W, B, T


def trace(a: Matrix):
    return sum(a[i][i] for i in range(len(a)))


def calinski_harabasz(points: Sequence[Sequence], labels: Sequence[Hashable]) -> Fraction:
    """CH = [tr(B) / (k - 1)] / [tr(W) / (n - k)]. Needs 2 <= k <= n - 1 and tr(W) > 0.

    tr(W) and tr(B) are computed in O(n d) time from the cluster means; the full
    matrices of scatter_matrices are only needed for the identity T = W + B.
    """
    n = len(points)
    groups: dict = {}
    for x, c in zip(points, labels):
        groups.setdefault(c, []).append(list(x))
    k = len(groups)
    if not 2 <= k <= n - 1:
        raise ValueError("CH needs 2 <= k <= n - 1")
    d = len(points[0])
    m = _mean([list(x) for x in points])
    tw = Fraction(0)
    tb = Fraction(0)
    for rows in groups.values():
        mc = _mean(rows)
        tw += sum((x[t] - mc[t]) ** 2 for x in rows for t in range(d))
        tb += len(rows) * sum((mc[t] - m[t]) ** 2 for t in range(d))
    if tw == 0:
        raise ValueError("CH is undefined when every cluster is a single repeated point")
    return (tb / (k - 1)) / (tw / (n - k))
