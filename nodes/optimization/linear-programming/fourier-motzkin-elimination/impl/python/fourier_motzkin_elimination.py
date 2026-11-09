# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fourier-motzkin-elimination/. The authors are listed in prov/JK7PSR.jsonl.

"""Fourier-Motzkin elimination with exact rational arithmetic.

A row is a triple (a, beta, y) that stands for the inequality a . x <= beta.
The vector y >= 0 records how the row was built from the input rows:
y . A = a and y . b = beta. So a row 0 <= beta with beta < 0 gives a
Farkas certificate y.
"""

from fractions import Fraction
from typing import Sequence

Row = tuple[list[Fraction], Fraction, list[Fraction]]
Number = int | Fraction


def _combine(p: Row, q: Row, k: int) -> Row:
    """Return (-q.a[k]) * p + p.a[k] * q, where p.a[k] > 0 > q.a[k]."""
    s, t = -q[0][k], p[0][k]
    a = [s * u + t * v for u, v in zip(p[0], q[0])]
    a[k] = Fraction(0)
    y = [s * u + t * v for u, v in zip(p[2], q[2])]
    return a, s * p[1] + t * q[1], y


def _clean(rows: list[Row]) -> list[Row]:
    """Drop rows 0 <= beta with beta >= 0, scale each row so that its first
    nonzero coefficient is +1 or -1, and keep only the tightest row of each
    direction. The set of solutions does not change."""
    best: dict[tuple[Fraction, ...], Row] = {}
    for a, beta, y in rows:
        lead = next((abs(c) for c in a if c != 0), None)
        if lead is None:
            if beta >= 0:
                continue
            lead = -beta  # scale 0 <= beta to 0 <= -1
        a = [c / lead for c in a]
        beta, y = beta / lead, [c / lead for c in y]
        key = tuple(a)
        if key not in best or beta < best[key][1]:
            best[key] = (a, beta, y)
    return list(best.values())


def eliminate(rows: list[Row], k: int) -> list[Row]:
    """Eliminate x_k (0-based) from the system. The result has a zero
    coefficient on x_k, and its solutions are the projections of the old ones."""
    pos = [r for r in rows if r[0][k] > 0]  # @line L3
    neg = [r for r in rows if r[0][k] < 0]
    out = [r for r in rows if r[0][k] == 0]  # @line L5
    for p in pos:  # @line L6
        for q in neg:
            out.append(_combine(p, q, k))  # @line L7
    return _clean(out)  # @line L8


def fourier_motzkin(
    A: Sequence[Sequence[Number]], b: Sequence[Number], n: int | None = None
) -> tuple[bool, list[Fraction]]:
    """Decide whether A x <= b has a real solution.

    Return (True, x) with A x <= b, or (False, y) with y >= 0, y A = 0 and
    y b < 0. The number of variables n is taken from A unless A is empty.
    """
    m = len(A)
    if n is None:
        n = len(A[0]) if m else 0
    rows: list[Row] = [
        ([Fraction(c) for c in A[i]], Fraction(b[i]), [Fraction(int(i == t)) for t in range(m)])
        for i in range(m)
    ]  # @line L1
    systems: list[list[Row]] = [[] for _ in range(n)]
    for k in range(n - 1, -1, -1):  # @line L2
        systems[k] = rows  # @line L4: the system in x_0 .. x_k
        rows = eliminate(rows, k)
    for a, beta, y in rows:  # @line L9: every coefficient is now 0
        if beta < 0:
            return False, y
    x: list[Fraction] = []
    for k in range(n):  # @line L10
        lo: Fraction | None = None
        hi: Fraction | None = None
        for a, beta, _ in systems[k]:  # @line L11
            if a[k] == 0:
                continue
            bound = (beta - sum((a[j] * x[j] for j in range(k)), Fraction(0))) / a[k]
            if a[k] > 0:
                hi = bound if hi is None else min(hi, bound)
            else:
                lo = bound if lo is None else max(lo, bound)
        x.append(lo if lo is not None else hi if hi is not None else Fraction(0))  # @line L12
    return True, x  # @line L13
