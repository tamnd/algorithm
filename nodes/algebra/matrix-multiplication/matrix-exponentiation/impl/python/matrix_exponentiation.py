# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matrix-exponentiation/. The authors are listed in prov/VTJXE5.jsonl.

from typing import Any, Callable, NamedTuple

Matrix = list[list[Any]]


class Semiring(NamedTuple):
    """The operations of a semiring: add, mul, its zero and its one."""

    add: Callable[[Any, Any], Any]
    mul: Callable[[Any, Any], Any]
    zero: Any
    one: Any


INTEGERS = Semiring(lambda x, y: x + y, lambda x, y: x * y, 0, 1)
MIN_PLUS = Semiring(min, lambda x, y: x + y, float("inf"), 0)
BOOLEAN = Semiring(lambda x, y: x or y, lambda x, y: x and y, False, True)


def modular(q: int) -> Semiring:
    """The ring Z/qZ."""
    return Semiring(lambda x, y: (x + y) % q, lambda x, y: (x * y) % q, 0, 1 % q)


def identity(n: int, s: Semiring = INTEGERS) -> Matrix:
    return [[s.one if i == j else s.zero for j in range(n)] for i in range(n)]


def multiply(x: Matrix, y: Matrix, s: Semiring = INTEGERS) -> Matrix:
    """The triple-loop product over the semiring s, into a new matrix."""
    n = len(x)
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            acc = s.zero
            for k in range(n):
                acc = s.add(acc, s.mul(x[i][k], y[k][j]))
            row.append(acc)
        out.append(row)
    return out


def matrix_exponentiation(a: Matrix, k: int, s: Semiring = INTEGERS) -> Matrix:
    """Return a^k for an n x n matrix a and k >= 0, over the semiring s.

    Uses the left-to-right binary method: floor(lg k) squarings and nu(k) - 1
    further products, each by the triple loop, so Theta(n^3 log k) semiring
    operations. Each product goes to a new matrix.
    """
    if k < 0:
        raise ValueError("the exponent must be nonnegative")
    n = len(a)
    if k == 0:  # @line L1
        return identity(n, s)
    bits = bin(k)[2:]  # @line L2: bits[0] is the leading digit 1
    r = [row[:] for row in a]  # @line L3
    for bit in bits[1:]:  # @line L4
        r = multiply(r, r, s)  # @line L5
        if bit == "1":  # @line L6
            r = multiply(r, a, s)
    return r  # @line L7


def count_products(k: int) -> int:
    """The number of products that matrix_exponentiation makes for exponent k."""
    return 0 if k == 0 else (k.bit_length() - 1) + bin(k).count("1") - 1
