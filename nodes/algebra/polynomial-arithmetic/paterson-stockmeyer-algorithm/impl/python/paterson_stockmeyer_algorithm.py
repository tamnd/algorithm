# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paterson-stockmeyer-algorithm/. The authors are listed in prov/E2T01W.jsonl.

"""The Paterson-Stockmeyer algorithm for evaluating a polynomial at an algebra element.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n], lowest
degree first; the zero polynomial is []. The coefficients are scalars from a
commutative ring R (int, Fraction, a modular class), and the point X is an
element of an R-algebra A with + and *, for example a square matrix. A scalar
c times an element P of A is written scale(c, P), by default c * P.

A product of two elements of A is a nonscalar multiplication, and is the
expensive operation. The algorithm computes the baby steps X^0, ..., X^k,
forms the blocks B_j = sum_i a_(jk+i) X^i with scalar multiplications only,
and combines the blocks by Horner's rule in Y = X^k. With k about sqrt(n + 1)
it does at most 2 ceil(sqrt(n + 1)) - 2 nonscalar multiplications.
"""

from __future__ import annotations

from math import isqrt
from typing import Any, Callable, List, Optional, Sequence, Tuple


def _default_scale(c: Any, p: Any) -> Any:
    return c * p


def block_size(n: int) -> int:
    """Return ceil(sqrt(n + 1)), the default block size for degree n."""
    k = isqrt(n + 1)
    return k if k * k == n + 1 else k + 1


def paterson_stockmeyer(
    a: Sequence[Any],
    x: Any,
    one: Any = 1,
    k: Optional[int] = None,
    scale: Callable[[Any, Any], Any] = _default_scale,
) -> Any:
    """Return a_0 one + a_1 x + ... + a_n x^n.

    one is the unit of the algebra (1 for scalars, the identity matrix for
    matrices). k is the block size; the default is ceil(sqrt(n + 1)).
    """
    a = list(a)
    if not a:
        return scale(0, one)
    n = len(a) - 1
    if k is None:
        k = block_size(n)  # @line L1
    if k < 1:
        raise ValueError("the block size must be at least 1")
    m = -(-(n + 1) // k)
    powers = [one, x]  # @line L2
    for _ in range(2, min(k, n) + 1):  # @line L3
        powers.append(powers[-1] * x)
    blocks = []
    for j in range(m):  # @line L4
        b = scale(a[j * k], one)
        for i in range(1, k):
            t = j * k + i
            if t > n:
                break
            b = b + scale(a[t], powers[i])
        blocks.append(b)
    s = blocks[m - 1]  # @line L5
    for j in range(m - 2, -1, -1):  # @line L6
        s = s * powers[k] + blocks[j]  # @line L7
    return s  # @line L8


def horner(a: Sequence[Any], x: Any, one: Any = 1, scale: Callable[[Any, Any], Any] = _default_scale) -> Any:
    """Return a(x) by Horner's rule, with n nonscalar multiplications."""
    a = list(a)
    if not a:
        return scale(0, one)
    s = scale(a[-1], one)
    for c in reversed(a[:-1]):
        s = s * x + scale(c, one)
    return s


def nonscalar_count(n: int, k: Optional[int] = None) -> int:
    """Return the number of nonscalar products PATERSON-STOCKMEYER does for degree n."""
    if n < 1:
        return 0
    if k is None:
        k = block_size(n)
    m = -(-(n + 1) // k)
    return max(min(k, n) - 1, 0) + (m - 1)


class Counted:
    """An algebra element that counts nonscalar and scalar multiplications."""

    stats = {"nonscalar": 0, "scalar": 0}

    def __init__(self, v: Any) -> None:
        self.v = v

    def __add__(self, o: "Counted") -> "Counted":
        return Counted(self.v + o.v)

    def __mul__(self, o: "Counted") -> "Counted":
        Counted.stats["nonscalar"] += 1
        return Counted(self.v * o.v)

    @staticmethod
    def scale(c: Any, p: "Counted") -> "Counted":
        Counted.stats["scalar"] += 1
        return Counted(c * p.v)


def counted_run(a: Sequence[Any], x: Any, k: Optional[int] = None, method: str = "ps") -> Tuple[Any, int, int]:
    """Run a method on a scalar point and return (value, nonscalar, scalar)."""
    Counted.stats = {"nonscalar": 0, "scalar": 0}
    if method == "ps":
        r = paterson_stockmeyer(a, Counted(x), Counted(1), k, Counted.scale)
    else:
        r = horner(a, Counted(x), Counted(1), Counted.scale)
    return r.v, Counted.stats["nonscalar"], Counted.stats["scalar"]


def trace(a: Sequence[Any], x: Any, k: Optional[int] = None) -> Tuple[List[Any], List[Any], List[Any]]:
    """Return (powers, blocks, Horner partial values) for a scalar point."""
    n = len(a) - 1
    if k is None:
        k = block_size(n)
    m = -(-(n + 1) // k)
    powers = [x**i for i in range(k + 1)]
    blocks = [sum(a[t] * powers[t - j * k] for t in range(j * k, min(j * k + k, n + 1))) for j in range(m)]
    s = blocks[-1]
    partial = [s]
    for j in range(m - 2, -1, -1):
        s = s * powers[k] + blocks[j]
        partial.append(s)
    return powers, blocks, partial


class Mat:
    """A small square matrix over a commutative ring, for matrix arguments."""

    def __init__(self, rows: Sequence[Sequence[Any]]) -> None:
        self.r = [list(row) for row in rows]

    @staticmethod
    def identity(d: int, one: Any = 1, zero: Any = 0) -> "Mat":
        return Mat([[one if i == j else zero for j in range(d)] for i in range(d)])

    def __add__(self, o: "Mat") -> "Mat":
        return Mat([[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(self.r, o.r)])

    def __mul__(self, o: "Mat") -> "Mat":
        d = len(self.r)
        cols = list(zip(*o.r))
        out = []
        for i in range(d):
            row = []
            for j in range(d):
                s = self.r[i][0] * cols[j][0]
                for t in range(1, d):
                    s = s + self.r[i][t] * cols[j][t]
                row.append(s)
            out.append(row)
        return Mat(out)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Mat) and self.r == o.r

    def __repr__(self) -> str:
        return f"Mat({self.r})"

    @staticmethod
    def scale(c: Any, p: "Mat") -> "Mat":
        return Mat([[c * x for x in row] for row in p.r])


if __name__ == "__main__":
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(trace(a, 2))
    print(counted_run(a, 2), counted_run(a, 2, method="horner"))
    j = Mat([[1, 1], [0, 1]])
    print(paterson_stockmeyer(a, j, Mat.identity(2), scale=Mat.scale))
