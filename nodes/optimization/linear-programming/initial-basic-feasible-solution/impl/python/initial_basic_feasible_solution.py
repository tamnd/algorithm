# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/initial-basic-feasible-solution/. The authors are listed in prov/1EQ5XZ.jsonl.

"""Find a feasible basis of A x + s = b, x >= 0, s >= 0, or prove that none exists.

This is the method with one artificial variable x0 (the INITIALIZE-SIMPLEX of CLRS):
subtract x0 from every row, pivot x0 into the row with the most negative b_i, and
minimize x0 with the simplex method. Columns 0..n-1 are x, columns n..n+m-1 are the
slacks s, and column n+m is x0. All arithmetic is exact (fractions.Fraction).
"""

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Sequence

Number = int | Fraction


@dataclass
class Result:
    """feasible: basis lists m columns of [A | I], and x (length n + m) is its basic solution, x >= 0.
    infeasible: y >= 0 with y^T A >= 0 and y^T b < 0, a proof that A x <= b, x >= 0 has no solution.
    pivots counts all pivots, including the first pivot of x0 and the pivot that takes x0 out.
    """

    feasible: bool
    basis: list[int] = field(default_factory=list)
    x: list[Fraction] = field(default_factory=list)
    y: list[Fraction] = field(default_factory=list)
    pivots: int = 0


def _pivot(t: list[list[Fraction]], r: list[Fraction], p: int, q: int) -> None:
    piv = t[p][q]
    t[p] = [v / piv for v in t[p]]
    for i in range(len(t)):
        if i != p and t[i][q] != 0:
            f = t[i][q]
            t[i] = [vi - f * vp for vi, vp in zip(t[i], t[p])]
    if r[q] != 0:
        f = r[q]
        r[:] = [rv - f * vp for rv, vp in zip(r, t[p])]


def initial_basic_feasible_solution(a: Sequence[Sequence[Number]], b: Sequence[Number]) -> Result:
    m = len(b)
    n = len(a[0]) if m else 0
    z = n + m  # the column of x0
    t = [[Fraction(v) for v in a[i]] + [Fraction(int(k == i)) for k in range(m)] + [Fraction(-1), Fraction(b[i])] for i in range(m)]
    basis = list(range(n, n + m))
    if all(row[-1] >= 0 for row in t):  # @line L1: the slack basis is feasible
        return Result(True, basis, _point(t, basis, z))
    r = [Fraction(0)] * z + [Fraction(1), Fraction(0)]  # @line L2: the objective is min x0
    k = min(range(m), key=lambda i: (t[i][-1], i))  # @line L3: the most negative b_k
    _pivot(t, r, k, z)
    basis[k] = z
    pivots = 1
    while True:  # @line L4: the simplex method with Bland's rule; x0 >= 0 bounds it below
        q = next((j for j in range(z + 1) if r[j] < 0), None)
        if q is None:
            break
        rows = [i for i in range(m) if t[i][q] > 0]
        p = min(rows, key=lambda i: (t[i][-1] / t[i][q], basis[i]))
        _pivot(t, r, p, q)
        basis[p] = q
        pivots += 1
    if r[-1] != 0:  # @line L5: the least x0 is -r[-1] > 0
        # r[n + i] = 0 - u_i for the slack of row i, where u is the optimal dual; y = -u
        return Result(False, y=[r[n + i] for i in range(m)], pivots=pivots)
    if z in basis:  # @line L6: x0 is basic at level 0, so pivot it out
        p = basis.index(z)
        q = next(j for j in range(z) if t[p][j] != 0)
        _pivot(t, r, p, q)
        basis[p] = q
        pivots += 1
    return Result(True, basis, _point(t, basis, z), pivots=pivots)  # @line L7: drop column x0


def _point(t: list[list[Fraction]], basis: list[int], z: int) -> list[Fraction]:
    x = [Fraction(0)] * z
    for i, j in enumerate(basis):
        x[j] = t[i][-1]
    return x
