# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/big-m-method/. The authors are listed in prov/XN1HFE.jsonl.

"""The big-M method in exact rational arithmetic.

Solve: minimize c^T x subject to A x = b and x >= 0. Each row gets an artificial
variable a_i, and the objective becomes c^T x + M (a_1 + ... + a_m). With M=None the
method treats M as a symbol larger than every number: each cost is a pair
(coefficient of M, constant), and pairs compare lexicographically. With a number M
the method uses that number, and it can give a wrong answer if M is too small.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Sequence

Number = int | Fraction


@dataclass
class Result:
    """status is "optimal", "unbounded" or "infeasible".

    optimal: x and value = c^T x. unbounded: a feasible x and a ray d >= 0 with A d = 0,
    c^T d < 0. infeasible: farkas, a vector z with A^T z <= 0 and b^T z > 0 (symbolic M
    only). artificial is the sum of the artificial variables at the end of the main run.
    """

    status: str
    x: list[Fraction] = field(default_factory=list)
    value: Fraction | None = None
    ray: list[Fraction] = field(default_factory=list)
    farkas: list[Fraction] = field(default_factory=list)
    artificial: Fraction = Fraction(0)
    pivots: int = 0
    rerun: bool = False  # True if line L6 ran (a ray was found while an artificial was positive)


def _pivot(t: list[list[Fraction]], rows: list[list[Fraction]], p: int, q: int) -> None:
    """Gauss-Jordan step on (p, q) for the tableau t and each cost row in rows."""
    piv = t[p][q]
    t[p] = [v / piv for v in t[p]]
    for i in range(len(t)):
        if i != p and t[i][q] != 0:
            f = t[i][q]
            t[i] = [vi - f * vp for vi, vp in zip(t[i], t[p])]
    for r in rows:
        if r[q] != 0:
            f = r[q]
            r[:] = [rv - f * vp for rv, vp in zip(r, t[p])]


def _run(t, basis, rows, key, cols):
    """Simplex with Bland's rule; column j improves if key(j) < 0. Return (status, column, pivots)."""
    pivots = 0
    while True:
        q = next((j for j in range(cols) if key(j) < (0,) * len(rows)), None)
        if q is None:
            return "optimal", None, pivots
        cand = [i for i in range(len(t)) if t[i][q] > 0]
        if not cand:
            return "unbounded", q, pivots
        p = min(cand, key=lambda i: (t[i][-1] / t[i][q], basis[i]))
        _pivot(t, rows, p, q)
        basis[p] = q
        pivots += 1


def big_m_method(a: Sequence[Sequence[Number]], b: Sequence[Number], c: Sequence[Number], M: Number | None = None) -> Result:
    m, n = len(a), len(c)
    t, sign = [], []
    for i in range(m):  # @line L1: make b >= 0 and add the artificial a_i
        s = -1 if b[i] < 0 else 1
        sign.append(s)
        t.append([Fraction(s * v) for v in a[i]] + [Fraction(int(k == i)) for k in range(m)] + [Fraction(s * b[i])])
    basis = list(range(n, n + m))  # @line L2
    rc = [Fraction(v) for v in c] + [Fraction(0)] * (m + 1)  # the constant part of the costs
    rM = [Fraction(0)] * n + [Fraction(1)] * m + [Fraction(0)]  # the M part of the costs
    for row in t:  # price out the artificial basis
        rM = [u - v for u, v in zip(rM, row)]
    if M is None:
        rows = [rM, rc]
        key = lambda j: (rM[j], rc[j])  # noqa: E731
    else:
        rows = [[u + M * v for u, v in zip(rc, rM)]]
        key = lambda j: (rows[0][j],)  # noqa: E731
    status, q, pivots = _run(t, basis, rows, key, n + m)  # @line L3: minimize c^T x + M 1^T a
    x = _point(t, basis, n + m)
    art = sum(x[n:], Fraction(0))
    res = Result(status, x=x[:n], artificial=art, pivots=pivots)
    if status == "unbounded":  # @line L4
        res.ray = [Fraction(0)] * n
        res.ray[q] = Fraction(1)
        for i, j in enumerate(basis):
            if j < n:
                res.ray[j] = -t[i][q]
        if art > 0 and M is None:  # @line L5: a ray, but is the program feasible?
            _, _, extra = _run(t, basis, [rM], lambda j: (rM[j],), n + m)  # @line L6: minimize 1^T a alone
            res.pivots += extra
            res.rerun = True
            x = _point(t, basis, n + m)
            if sum(x[n:], Fraction(0)) > 0:
                return Result("infeasible", farkas=_farkas(rM, sign, n), artificial=art, pivots=res.pivots, rerun=True)
            res.x = x[:n]
        return res
    if art > 0:  # @line L7: a positive artificial at the optimum
        res.status = "infeasible"
        if M is None:
            res.farkas = _farkas(rM, sign, n)
        res.x = []
        return res
    res.value = sum((Fraction(cj) * xj for cj, xj in zip(c, x)), Fraction(0))  # @line L8
    return res


def _point(t, basis, cols):
    x = [Fraction(0)] * cols
    for i, j in enumerate(basis):
        x[j] = t[i][-1]
    return x


def _farkas(rM, sign, n):
    """At an optimum of min 1^T a, the reduced cost of a_i is 1 - u_i; z = D u."""
    return [(1 - rM[n + i]) * s for i, s in enumerate(sign)]
