# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/macaulay-matrix/. The authors are listed in prov/G8MNQA.jsonl.

"""The Macaulay matrix of a list of polynomials up to a degree bound.

A polynomial in K[x_1, ..., x_n] is a dict from exponent tuples to nonzero
coefficients (Fraction, or any field type). Columns are monomials sorted from
largest to smallest in a monomial order (lex, grlex or grevlex), so the
leftmost nonzero entry of a row is the leading monomial of its polynomial.
"""

from fractions import Fraction
from itertools import combinations_with_replacement
from typing import Callable, Dict, List, Sequence, Tuple

Exp = Tuple[int, ...]
Poly = Dict[Exp, Fraction]


def order_key(order: str) -> Callable[[Exp], tuple]:
    """A sort key: a larger key means a larger monomial."""
    if order == "lex":
        return lambda a: tuple(a)
    if order == "grlex":
        return lambda a: (sum(a), tuple(a))
    if order == "grevlex":
        return lambda a: (sum(a), tuple(-e for e in reversed(a)))
    raise ValueError("order must be lex, grlex or grevlex")


def monomials(n: int, degree: int) -> List[Exp]:
    """All exponent tuples in n variables of total degree exactly degree."""
    out = []
    for combo in combinations_with_replacement(range(n), degree):
        e = [0] * n
        for v in combo:
            e[v] += 1
        out.append(tuple(e))
    return out


class MacaulayMatrix:
    """Rows are the products m * f_i with deg(m * f_i) <= D, or = D if homogeneous."""

    def __init__(self, polys: Sequence[Poly], n: int, D: int, order: str = "grevlex", homogeneous: bool = False):
        key = order_key(order)
        degs = range(D, D + 1) if homogeneous else range(D + 1)
        cols = [m for d in degs for m in monomials(n, d)]  # @line L4
        cols.sort(key=key, reverse=True)
        self.columns: List[Exp] = cols
        self.index = {m: j for j, m in enumerate(cols)}
        self.labels: List[Tuple[Exp, int]] = []
        self.rows: List[List[Fraction]] = []  # @line L1
        for i, f in enumerate(polys):
            if not f:
                continue
            df = max(sum(a) for a in f)
            if homogeneous and any(sum(a) != df for a in f):
                raise ValueError("homogeneous mode needs homogeneous polynomials")
            for d in degs:  # @line L2
                if d < df:
                    continue
                for m in monomials(n, d - df):
                    row = [Fraction(0)] * len(cols)
                    for a, c in f.items():
                        row[self.index[tuple(x + y for x, y in zip(a, m))]] = Fraction(c)
                    self.rows.append(row)  # @line L3
                    self.labels.append((m, i))
        self.echelon: List[List[Fraction]] = []
        self.pivots: List[int] = []  # @line L5

    def reduce_to_echelon(self) -> None:
        """Reduced row echelon form by Gauss-Jordan elimination, columns left to right."""
        A = [list(r) for r in self.rows]
        pivots = []
        top = 0
        for j in range(len(self.columns)):  # @line L6
            p = next((r for r in range(top, len(A)) if A[r][j] != 0), None)
            if p is None:
                continue
            A[top], A[p] = A[p], A[top]
            inv = 1 / A[top][j]
            A[top] = [inv * a for a in A[top]]
            for r in range(len(A)):
                if r != top and A[r][j] != 0:
                    c = A[r][j]
                    A[r] = [a - c * b for a, b in zip(A[r], A[top])]
            pivots.append(j)
            top += 1
        self.echelon = A[:top]
        self.pivots = pivots  # @line L7

    def rank(self) -> int:
        return len(self.pivots)

    def leading_monomials(self) -> List[Exp]:
        """The leading monomials of the nonzero polynomials of the row space."""
        return [self.columns[j] for j in self.pivots]

    def as_polys(self) -> List[Poly]:
        """The rows of the echelon form as polynomials."""
        return [{self.columns[j]: c for j, c in enumerate(r) if c != 0} for r in self.echelon]

    def vector(self, g: Poly) -> List[Fraction]:
        v = [Fraction(0)] * len(self.columns)
        for a, c in g.items():
            if a not in self.index:
                raise ValueError("g has a monomial outside the columns")
            v[self.index[a]] = Fraction(c)
        return v

    def member(self, g: Poly) -> bool:
        """True when g lies in the row space."""
        v = self.vector(g)
        for row, j in zip(self.echelon, self.pivots):  # @line L8
            if v[j] != 0:
                c = v[j]
                v = [a - c * b for a, b in zip(v, row)]
        return all(a == 0 for a in v)  # @line L9
