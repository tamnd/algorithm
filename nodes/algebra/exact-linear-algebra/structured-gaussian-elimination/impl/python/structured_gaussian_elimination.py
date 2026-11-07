# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structured-gaussian-elimination/. The authors are listed in prov/FPBFNE.jsonl.

"""Structured Gaussian elimination (LaMacchia and Odlyzko) for a sparse system A x = c over Q or Z/pZ.

Light columns are pivoted away with rules that create fill-in only in a growing set of heavy
columns; the small remaining system on the heavy columns is solved densely, then the pivots
are back-substituted.
"""

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
Row = dict[int, Number]


class Inconsistent(ValueError):
    """Raised when A x = c has no solution."""


def _field(p: Optional[int]):
    if p is None:
        return Fraction, lambda a: Fraction(1) / a
    return (lambda a: a % p), (lambda a: pow(a, -1, p))


def dense_solve(rows: list[Row], rhs: list[Number], cols: list[int], p: Optional[int]) -> dict[int, Number]:
    """Gauss-Jordan elimination on the given rows restricted to cols; free variables are set to 0."""
    norm, inv = _field(p)
    m = [[norm(r.get(j, 0)) for j in cols] + [norm(v)] for r, v in zip(rows, rhs)]
    k = len(cols)
    where: list[int] = []
    top = 0
    for col in range(k):
        piv = next((i for i in range(top, len(m)) if m[i][col] != 0), None)
        if piv is None:
            continue
        m[top], m[piv] = m[piv], m[top]
        s = inv(m[top][col])
        m[top] = [norm(v * s) for v in m[top]]
        for i in range(len(m)):
            if i != top and m[i][col] != 0:
                f = m[i][col]
                m[i] = [norm(a - f * b) for a, b in zip(m[i], m[top])]
        where.append(col)
        top += 1
    if any(row[k] != 0 for row in m[top:]):
        raise Inconsistent("the dense part is inconsistent")
    x = {j: norm(0) for j in cols}
    for i, col in enumerate(where):
        x[cols[col]] = m[i][k]
    return x


def structured_solve(a: list[Row], c: list[Number], n: int, p: Optional[int] = None,
                     stats: Optional[dict] = None) -> list[Number]:
    """Return one solution x of A x = c, where A has n columns and row i is the sparse dict a[i].

    Arithmetic is exact over Q (p is None) or over Z/pZ for a prime p. Raises Inconsistent when
    there is no solution. If stats is a dict, it receives the number of heavy columns and pivots.
    """
    if len(a) != len(c):
        raise ValueError("a and c must have the same length")
    norm, inv = _field(p)
    rows = [{j: norm(v) for j, v in r.items() if norm(v) != 0} for r in a]
    rhs = [norm(v) for v in c]
    if any(not 0 <= j < n for r in rows for j in r):
        raise ValueError("column index out of range")
    active = set(range(len(rows)))  # @line L1
    light = set(range(n))
    heavy: list[int] = []
    pivots: list[tuple[int, int]] = []
    x: list[Number] = [norm(0)] * n
    colrows: dict[int, set[int]] = {j: set() for j in range(n)}
    for i, r in enumerate(rows):
        for j in r:
            colrows[j].add(i)

    def light_entries(i: int) -> list[int]:
        return [j for j in rows[i] if j in light]

    while light:  # @line L2
        empty = next((j for j in sorted(light) if not colrows[j]), None)
        if empty is not None:  # @line L3
            light.discard(empty)  # a free variable, x_j = 0
            continue
        single = next((j for j in sorted(light) if len(colrows[j]) == 1), None)
        if single is not None:  # @line L4
            r = next(iter(colrows[single]))
            pivots.append((r, single))
            active.discard(r)
            light.discard(single)
            for j in rows[r]:
                colrows[j].discard(r)
            continue
        cand = next((i for i in sorted(active) if len(light_entries(i)) == 1), None)
        if cand is not None:  # @line L5
            r, j = cand, light_entries(cand)[0]
            pivots.append((r, j))
            active.discard(r)
            light.discard(j)
            for k in rows[r]:
                colrows[k].discard(r)
            s = inv(rows[r][j])
            for i in sorted(colrows[j]):  # the other active rows meeting column j
                f = norm(rows[i][j] * s)
                for k, v in rows[r].items():  # row r lives in column j and the heavy columns only
                    nv = norm(rows[i].get(k, 0) - f * v)
                    if nv == 0:
                        if k in rows[i]:
                            del rows[i][k]
                            colrows[k].discard(i)
                    else:
                        if k not in rows[i]:
                            colrows[k].add(i)
                        rows[i][k] = nv
                rhs[i] = norm(rhs[i] - f * rhs[r])
            continue
        j = max(sorted(light), key=lambda col: len(colrows[col]))  # @line L6
        light.discard(j)
        heavy.append(j)
    act = sorted(active)  # @line L7
    xh = dense_solve([rows[i] for i in act], [rhs[i] for i in act], sorted(heavy), p)
    for j, v in xh.items():
        x[j] = v
    for r, j in reversed(pivots):  # @line L8
        s = rhs[r] - sum(v * x[k] for k, v in rows[r].items() if k != j)
        x[j] = norm(s * inv(rows[r][j]))
    if stats is not None:
        stats["heavy"] = len(heavy)
        stats["pivots"] = len(pivots)
        stats["dense_rows"] = len(act)
    return x  # @line L9
