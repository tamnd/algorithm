# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-radix-fft/. The authors are listed in prov/7Q1636.jsonl.

"""Split-radix FFT: X_k = sum_j x_j w**(j*k) for n a power of two.

One half-length transform of the even samples and two quarter-length
transforms of the samples 1 and 3 modulo 4. Over C the root is
w = exp(-2*pi*i/n). Over another ring, pass a table of powers and the
ring operations; the code uses only +, -, * on the entries.
"""

from __future__ import annotations

import cmath
import math
from typing import Any, Callable, Sequence


def _unit(r: int, n: int) -> complex:
    """Return exp(2*pi*i*r/n), exact when r/n is a multiple of 1/4."""
    r %= n
    if (4 * r) % n == 0:
        return (1 + 0j, 1j, -1 + 0j, -1j)[4 * r // n]
    return cmath.exp(2j * math.pi * r / n)


def _check(n: int) -> None:
    if n < 1 or n & (n - 1):
        raise ValueError("the length must be a power of two")


def split_radix_core(x: Sequence[Any], table: Sequence[Any]) -> list[Any]:
    """DFT of x with table[e] = w**e for 0 <= e < n, where w**(n/2) = -1.

    Uses only the operators +, -, * of the entries, so it runs over any
    commutative ring (and over a counting wrapper). The recursion depth is lg n.
    """
    N = len(x)

    def rec(start: int, stride: int) -> list[Any]:
        n = N // stride  # @line L1
        if n == 1:
            return [x[start]]
        if n == 2:  # @line L2
            a, b = x[start], x[start + stride]
            return [a + b, a - b]
        U = rec(start, 2 * stride)  # @line L3
        Z = rec(start + stride, 4 * stride)  # @line L4
        Zp = rec(start + 3 * stride, 4 * stride)  # @line L5
        J = table[(n // 4) * stride]  # @line L6  w_n**(n/4), -i over C
        q = n // 4
        out: list[Any] = [None] * n
        for k in range(q):  # @line L7
            if k == 0:  # @line L8
                a, b = Z[0], Zp[0]
            else:
                a, b = table[k * stride] * Z[k], table[3 * k * stride] * Zp[k]
            s, d = a + b, J * (a - b)  # @line L9
            out[k], out[k + 2 * q] = U[k] + s, U[k] - s  # @line L10
            out[k + q], out[k + 3 * q] = U[k + q] + d, U[k + q] - d  # @line L11
        return out  # @line L12

    return rec(0, 1)


def split_radix_fft(x: list, w: int | None = None, p: int | None = None, inverse: bool = False) -> list:
    """DFT of x (n a power of two) over C, or modulo a prime p with w**(n/2) = -1 (mod p).

    With inverse=True, use w**(-1) and the factor 1/n.
    """
    n = len(x)
    _check(n)
    if p is None:
        sign = 1 if inverse else -1
        table = [_unit(sign * e, n) for e in range(n)]
        y = split_radix_core([complex(v) for v in x], table)
        return [v / n for v in y] if inverse else y
    if w is None or pow(w, n, p) != 1 or (n > 1 and pow(w, n // 2, p) != p - 1):
        raise ValueError("w must satisfy w**(n/2) = -1 modulo p")
    base = pow(w, -1, p) if inverse else w
    table = [Mod(pow(base, e, p), p) for e in range(n)]
    y = [v.v for v in split_radix_core([Mod(v, p) for v in x], table)]
    if inverse:
        ninv = pow(n, -1, p)
        y = [v * ninv % p for v in y]
    return y


class Mod:
    """A residue modulo p with +, - and *."""

    __slots__ = ("v", "p")

    def __init__(self, v: int, p: int) -> None:
        self.v, self.p = v % p, p

    def __add__(self, o: "Mod") -> "Mod":
        return Mod(self.v + o.v, self.p)

    def __sub__(self, o: "Mod") -> "Mod":
        return Mod(self.v - o.v, self.p)

    def __mul__(self, o: "Mod") -> "Mod":
        return Mod(self.v * o.v, self.p)
