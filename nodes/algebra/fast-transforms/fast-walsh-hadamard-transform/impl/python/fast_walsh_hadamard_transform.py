# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-walsh-hadamard-transform/. The authors are listed in prov/E3XY86.jsonl.

from typing import TypeVar

S = TypeVar("S", int, float, complex)


def fwht(x: list[S], p: int | None = None) -> None:
    """Replace x by H x in place, (H x)[k] = sum of (-1)**popcount(j & k) * x[j].

    Precondition: n = len(x) is a power of two. With p given, the entries
    are integers and every result is reduced modulo p. Cost: (n/2) lg n
    additions and (n/2) lg n subtractions, no multiplications.
    """
    n = len(x)  # @line L1
    if n < 1 or n & (n - 1):
        raise ValueError("the length must be a power of two")
    h = 1  # @line L2
    while h < n:  # @line L3
        for s in range(0, n, 2 * h):  # @line L4
            for j in range(s, s + h):  # @line L5
                u, v = x[j], x[j + h]  # @line L6
                if p is None:
                    x[j], x[j + h] = u + v, u - v  # @line L7
                else:
                    x[j], x[j + h] = (u + v) % p, (u - v) % p
        h *= 2  # @line L8


def inverse_fwht(y: list[S], p: int | None = None) -> None:
    """Replace y by the inverse transform (1/n) H y, in place.

    Precondition: as for fwht, and n must be a unit (an odd modulus p, or
    p None). Over the integers with p None, the division is exact when y is
    the transform of an integer vector. Cost: one fwht and n divisions.
    """
    n = len(y)
    fwht(y, p)  # @line L9
    if p is not None:
        n_inv = pow(n, -1, p)
        for j in range(n):  # @line L10
            y[j] = y[j] * n_inv % p
    else:
        for j in range(n):  # @line L10
            v = y[j]
            y[j] = v // n if isinstance(v, int) and v % n == 0 else v / n


def xor_convolution(a: list[int], b: list[int], p: int | None = None) -> list[int]:
    """Return c with c[k] = sum of a[i] * b[j] over i XOR j = k.

    Precondition: len(a) == len(b) is a power of two; p is None (exact
    integers) or an odd modulus. Cost: three transforms and n products.
    """
    fa, fb = list(a), list(b)
    fwht(fa, p)
    fwht(fb, p)
    fc = [u * v if p is None else u * v % p for u, v in zip(fa, fb)]
    inverse_fwht(fc, p)
    return fc
