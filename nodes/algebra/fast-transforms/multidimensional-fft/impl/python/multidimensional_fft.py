# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multidimensional-fft/. The authors are listed in prov/98S7CV.jsonl.

import cmath
from math import prod
from typing import TypeVar

S = TypeVar("S", int, complex)


def _unit(r: int, n: int) -> complex:
    """Return exp(2*pi*i*r/n), exact when r/n is a multiple of 1/4."""
    r %= n
    if (4 * r) % n == 0:
        return (1 + 0j, 1j, -1 + 0j, -1j)[4 * r // n]
    return cmath.exp(2j * cmath.pi * r / n)


def _table(w: S, n: int, p: int | None) -> list[S]:
    """Powers w**k for k < n/2: exact modulo p, from the angle over C."""
    if p is not None:
        return [pow(w, k, p) for k in range(n // 2)]
    m = round(cmath.phase(w) * n / (2 * cmath.pi)) % n
    if abs(w - _unit(m, n)) > 1e-9:
        raise ValueError("w is not close to a root of unity of order dividing n")
    return [_unit(m * k, n) for k in range(n // 2)]


def fft_1d(x: list[S], table: list[S], p: int | None = None) -> None:
    """In-place radix-2 decimation-in-time FFT of x with the given twiddle table."""
    n = len(x)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            x[i], x[j] = x[j], x[i]
    h = 1
    while h < n:
        step = n // (2 * h)
        for s in range(0, n, 2 * h):
            for k in range(h):
                u = x[s + k]
                v = table[k * step] * x[s + k + h]
                if p is None:
                    x[s + k], x[s + k + h] = u + v, u - v
                else:
                    x[s + k], x[s + k + h] = (u + v) % p, (u - v) % p
        h *= 2


def multidimensional_fft(x: list[S], shape: list[int], roots: list[S], p: int | None = None) -> None:
    """Replace the row-major array x of the given shape by its d-dimensional DFT.

    X[k_1, ..., k_d] = sum over j of x[j_1, ..., j_d] * prod of roots[a]**(j_a * k_a).
    Precondition: len(x) = prod(shape), every shape[a] is a power of two, and
    roots[a] is a principal shape[a]-th root of unity (complex, or modulo the
    prime p). Cost with N = prod(shape): N lg N additions and (N/2) lg N
    multiplications in the ring, and O(N log N) index operations.
    """
    if len(shape) != len(roots):
        raise ValueError("one root per axis is needed")
    for n_a in shape:
        if n_a < 1 or n_a & (n_a - 1):
            raise ValueError("every length must be a power of two")
    total = prod(shape)  # @line L1
    if len(x) != total:
        raise ValueError("the array does not have the given shape")
    d = len(shape)
    for a in range(d):  # @line L2
        n_a = shape[a]
        stride = prod(shape[a + 1 :])  # @line L3
        table = _table(roots[a], n_a, p)  # @line L4
        block = n_a * stride
        for q in range(0, total, block):  # @line L5
            for r in range(stride):  # @line L5
                s = q + r
                line = [x[s + i * stride] for i in range(n_a)]  # @line L6
                fft_1d(line, table, p)  # @line L7
                for i in range(n_a):  # @line L8
                    x[s + i * stride] = line[i]
