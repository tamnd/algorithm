# SPDX-License-Identifier: MIT
# Shared module of the constraint-based metabolic pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Exact linear algebra and an exact simplex method in Fraction.

The reference copy is in biology/systems-biology/flux-balance-analysis/
impl/python/. The other constraint-based pages hold byte-identical copies.

Contents:
- rref(M), rank(M), nullspace(M, ncols), solve_linear(A, b): Gaussian
  elimination over the rationals.
- simplex_standard(A, b, c): minimize c x subject to A x = b, x >= 0, by the
  two-phase simplex method with Bland's rule.
- solve_lp(c, ...): a linear program with bounds, equality rows and <= rows,
  reduced to the standard form and solved by simplex_standard.
- polytope_vertices(A, b, lb, ub): all vertices of {x : A x = b,
  lb <= x <= ub} with finite bounds, by brute force. Tests use it as an
  independent reference.

A bound of None means minus or plus infinity. Every number is converted to
Fraction, so the results are exact.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from typing import List, Optional, Sequence, Tuple

Matrix = List[List[Fraction]]


def frac(x) -> Fraction:
    """Convert an int, a Fraction, a float or a string to Fraction."""
    return x if isinstance(x, Fraction) else Fraction(x)


def rref(M: Sequence[Sequence]) -> Tuple[Matrix, List[int]]:
    """Return the reduced row echelon form of M and its pivot columns."""
    R = [[frac(x) for x in row] for row in M]
    pivots: List[int] = []
    if not R:
        return R, pivots
    rows, cols = len(R), len(R[0])
    r = 0
    for col in range(cols):
        if r == rows:
            break
        p = next((i for i in range(r, rows) if R[i][col] != 0), None)
        if p is None:
            continue
        R[r], R[p] = R[p], R[r]
        inv = 1 / R[r][col]
        R[r] = [x * inv for x in R[r]]
        for i in range(rows):
            if i != r and R[i][col] != 0:
                f = R[i][col]
                R[i] = [a - f * b for a, b in zip(R[i], R[r])]
        pivots.append(col)
        r += 1
    return R, pivots


def rank(M: Sequence[Sequence]) -> int:
    """The rank of M (0 for an empty matrix)."""
    if not M or not M[0]:
        return 0
    return len(rref(M)[1])


def nullspace(M: Sequence[Sequence], ncols: int) -> Matrix:
    """A basis of {x : M x = 0}, one vector for each free column.

    The vector of free column f has x_f = 1 and x_g = 0 at the other free
    columns. M may have no rows; then the basis is the unit vectors.
    """
    if not M:
        return [[Fraction(int(i == j)) for i in range(ncols)] for j in range(ncols)]
    R, piv = rref(M)
    free = [j for j in range(ncols) if j not in piv]
    basis = []
    for f in free:
        x = [Fraction(0)] * ncols
        x[f] = Fraction(1)
        for i, p in enumerate(piv):
            x[p] = -R[i][f]
        basis.append(x)
    return basis


def solve_linear(A: Sequence[Sequence], b: Sequence) -> Optional[List[Fraction]]:
    """One solution of A x = b (free variables set to 0), or None if none."""
    if not A:
        return None if any(frac(x) != 0 for x in b) else []
    n = len(A[0])
    aug = [list(row) + [bi] for row, bi in zip(A, b)]
    R, piv = rref(aug)
    if n in piv:
        return None
    x = [Fraction(0)] * n
    for i, p in enumerate(piv):
        x[p] = R[i][n]
    return x


class LPResult:
    """status is 'optimal', 'infeasible' or 'unbounded'."""

    def __init__(self, status: str, x=None, value=None):
        self.status = status
        self.x = x
        self.value = value

    def __repr__(self) -> str:
        return f"LPResult({self.status!r}, {self.x!r}, {self.value!r})"


def _pivot(T: Matrix, basis: List[int], r: int, c: int) -> None:
    inv = 1 / T[r][c]
    T[r] = [x * inv for x in T[r]]
    for i in range(len(T)):
        if i != r and T[i][c] != 0:
            f = T[i][c]
            T[i] = [a - f * b for a, b in zip(T[i], T[r])]
    basis[r] = c


def _run(T: Matrix, basis: List[int], allowed: int) -> str:
    """Simplex iterations with Bland's rule on columns 0 .. allowed - 1.

    The last row of T holds the reduced costs and minus the objective value.
    Enter: the smallest column with a negative reduced cost. Leave: the row
    with the smallest ratio, ties broken by the smallest basic column.
    """
    m = len(T) - 1
    while True:
        obj = T[m]
        c = next((j for j in range(allowed) if obj[j] < 0), None)
        if c is None:
            return "optimal"
        best = None
        for i in range(m):
            if T[i][c] > 0:
                key = (T[i][-1] / T[i][c], basis[i])
                if best is None or key < best[0]:
                    best = (key, i)
        if best is None:
            return "unbounded"
        _pivot(T, basis, best[1], c)


def simplex_standard(A: Sequence[Sequence], b: Sequence, c: Sequence) -> LPResult:
    """Minimize c x subject to A x = b and x >= 0, exactly.

    Phase 1 minimizes the sum of one artificial variable per row. Phase 2
    starts from the basis that phase 1 finds. Bland's rule makes both phases
    terminate.
    """
    n = len(c)
    cc = [frac(x) for x in c]
    rows = []
    for row, bi in zip(A, b):
        r = [frac(x) for x in row]
        bi = frac(bi)
        if bi < 0:
            r, bi = [-x for x in r], -bi
        rows.append(r + [bi])
    m = len(rows)
    if m == 0:
        if any(x < 0 for x in cc):
            return LPResult("unbounded")
        return LPResult("optimal", [Fraction(0)] * n, Fraction(0))
    # Phase 1 tableau: [A | I | b], objective row = minus the sum of the rows.
    T = []
    for i, r in enumerate(rows):
        T.append(r[:n] + [Fraction(int(k == i)) for k in range(m)] + [r[n]])
    obj = [-sum(T[i][j] for i in range(m)) for j in range(n)] + [Fraction(0)] * m
    obj.append(-sum(T[i][-1] for i in range(m)))
    T.append(obj)
    basis = [n + i for i in range(m)]
    _run(T, basis, n + m)
    if T[m][-1] != 0:
        return LPResult("infeasible")
    # Drive the artificial variables out of the basis, or drop redundant rows.
    i = 0
    while i < len(T) - 1:
        if basis[i] >= n:
            j = next((j for j in range(n) if T[i][j] != 0), None)
            if j is None:
                del T[i]
                del basis[i]
                continue
            _pivot(T, basis, i, j)
        i += 1
    m = len(T) - 1
    T = [row[:n] + [row[-1]] for row in T]
    obj = list(cc) + [Fraction(0)]
    for i in range(m):
        cb = cc[basis[i]]
        if cb != 0:
            obj = [a - cb * t for a, t in zip(obj, T[i])]
    T[m] = obj
    status = _run(T, basis, n)
    if status == "unbounded":
        return LPResult("unbounded")
    x = [Fraction(0)] * n
    for i in range(m):
        x[basis[i]] = T[i][-1]
    return LPResult("optimal", x, sum(a * v for a, v in zip(cc, x)))


def solve_lp(c, A_eq=(), b_eq=(), A_le=(), b_le=(), lb=None, ub=None,
             maximize=False) -> LPResult:
    """Optimize c x subject to A_eq x = b_eq, A_le x <= b_le, lb <= x <= ub.

    lb defaults to 0 for every variable and ub to None (no upper bound). A
    bound of None is infinite. The result holds x and the value in the
    original variables.
    """
    n = len(c)
    lb = [0] * n if lb is None else lb
    ub = [None] * n if ub is None else ub
    # x_j = off_j + sum over k of coef[j][k] * y_k with y >= 0.
    cols: List[List[Tuple[int, int]]] = []
    off: List[Fraction] = []
    ny = 0
    for j in range(n):
        lo = None if lb[j] is None else frac(lb[j])
        hi = None if ub[j] is None else frac(ub[j])
        if lo is not None and hi is not None and lo > hi:
            return LPResult("infeasible")
        if lo is not None:
            off.append(lo)
            cols.append([(ny, 1)])
            ny += 1
        elif hi is not None:
            off.append(hi)
            cols.append([(ny, -1)])
            ny += 1
        else:
            off.append(Fraction(0))
            cols.append([(ny, 1), (ny + 1, -1)])
            ny += 2
    caps = [(j, frac(ub[j]) - frac(lb[j])) for j in range(n)
            if lb[j] is not None and ub[j] is not None]
    nslack = len(A_le) + len(caps)
    N = ny + nslack
    A: List[List[Fraction]] = []
    b: List[Fraction] = []

    def expand(row) -> Tuple[List[Fraction], Fraction]:
        out = [Fraction(0)] * N
        shift = Fraction(0)
        for j in range(n):
            a = frac(row[j])
            if a == 0:
                continue
            shift += a * off[j]
            for k, s in cols[j]:
                out[k] += a * s
        return out, shift

    for row, bi in zip(A_eq, b_eq):
        r, s = expand(row)
        A.append(r)
        b.append(frac(bi) - s)
    s_idx = ny
    for row, bi in zip(A_le, b_le):
        r, s = expand(row)
        r[s_idx] = Fraction(1)
        s_idx += 1
        A.append(r)
        b.append(frac(bi) - s)
    for j, cap in caps:
        r = [Fraction(0)] * N
        r[cols[j][0][0]] = Fraction(1)
        r[s_idx] = Fraction(1)
        s_idx += 1
        A.append(r)
        b.append(cap)
    sign = -1 if maximize else 1
    cy, _ = expand([sign * frac(x) for x in c])
    res = simplex_standard(A, b, cy)
    if res.status != "optimal":
        return LPResult(res.status)
    x = []
    for j in range(n):
        x.append(off[j] + sum(s * res.x[k] for k, s in cols[j]))
    return LPResult("optimal", x, sum(frac(a) * v for a, v in zip(c, x)))


def polytope_vertices(A: Sequence[Sequence], b: Sequence, lb: Sequence,
                      ub: Sequence) -> List[Tuple[Fraction, ...]]:
    """All vertices of {x : A x = b, lb <= x <= ub}, with finite bounds.

    A point is a vertex if and only if the columns of A at the coordinates
    strictly between their bounds are linearly independent. So try every set
    F of such columns and every choice of a bound for the other coordinates.
    The cost is exponential; use it only on small examples.
    """
    n = len(lb)
    lo = [frac(x) for x in lb]
    hi = [frac(x) for x in ub]
    r = rank(A) if A else 0
    found = set()
    for size in range(r + 1):
        for F in combinations(range(n), size):
            AF = [[row[j] for j in F] for row in A]
            if size and rank(AF) < size:
                continue
            rest = [j for j in range(n) if j not in F]
            for choice in product((0, 1), repeat=len(rest)):
                x = [Fraction(0)] * n
                for j, ch in zip(rest, choice):
                    x[j] = hi[j] if ch else lo[j]
                rhs = [frac(bi) - sum(frac(row[j]) * x[j] for j in rest)
                       for row, bi in zip(A, b)]
                if size:
                    sol = solve_linear(AF, rhs)
                    if sol is None:
                        continue
                    for j, v in zip(F, sol):
                        x[j] = v
                elif any(v != 0 for v in rhs):
                    continue
                if all(lo[j] <= x[j] <= hi[j] for j in range(n)):
                    found.add(tuple(x))
    return sorted(found)
