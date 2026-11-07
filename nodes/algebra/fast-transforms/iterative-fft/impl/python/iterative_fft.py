# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-fft/. The authors are listed in prov/37TN4K.jsonl.

import cmath
from typing import TypeVar

S = TypeVar("S", int, complex)


def _check_length(n: int) -> int:
    """Return t = lg n, or raise ValueError when n is not a power of two."""
    if n < 1 or n & (n - 1):
        raise ValueError("the length must be a power of two")
    return n.bit_length() - 1


def _unit(r: int, n: int) -> complex:
    """Return exp(2*pi*i*r/n), exact when r/n is a multiple of 1/4."""
    r %= n
    if (4 * r) % n == 0:
        return (1 + 0j, 1j, -1 + 0j, -1j)[4 * r // n]
    return cmath.exp(2j * cmath.pi * r / n)


def twiddles(w: S, n: int, p: int | None = None) -> list[S]:
    """Return the table [w**k for k < n/2], modulo p when p is given.

    Over the complex numbers, w must be close to exp(2*pi*i*m/n) for an
    integer m, and the entries are taken from the exact angle 2*pi*m*k/n
    rather than by repeated multiplication, whose error grows with k.
    """
    if p is not None:
        return [pow(w, k, p) for k in range(n // 2)]
    m = round(cmath.phase(w) * n / (2 * cmath.pi)) % n
    if abs(w - _unit(m, n)) > 1e-9:
        raise ValueError("w is not close to a root of unity of order dividing n")
    return [_unit(m * k, n) for k in range(n // 2)]


def bit_reverse(x: list[S]) -> None:
    """Permute x in place so that x[j] and x[rev(j)] trade places."""
    n = len(x)
    t = _check_length(n)
    rev = [0] * n
    for j in range(1, n):
        rev[j] = (rev[j >> 1] >> 1) | ((j & 1) << (t - 1))
    for j in range(n):  # @line L11
        if j < rev[j]:  # @line L12
            x[j], x[rev[j]] = x[rev[j]], x[j]


def dif_stages(x: list[S], table: list[S], p: int | None = None) -> None:
    """Decimation in frequency: natural order in, DFT in bit-reversed order out."""
    n = len(x)
    _check_length(n)
    h = n // 2  # @line L3
    while h >= 1:  # @line L4
        step = n // (2 * h)
        for s in range(0, n, 2 * h):  # @line L5
            for k in range(h):  # @line L6
                a, b = x[s + k], x[s + k + h]  # @line L7
                if p is None:
                    x[s + k] = a + b  # @line L8
                    x[s + k + h] = table[k * step] * (a - b)  # @line L9
                else:
                    x[s + k] = (a + b) % p  # @line L8
                    x[s + k + h] = table[k * step] * (a - b) % p  # @line L9
        h //= 2  # @line L10


def dit_stages(y: list[S], table: list[S], p: int | None = None) -> None:
    """Decimation in time without the permutation: bit-reversed order in, DFT out."""
    n = len(y)
    _check_length(n)
    h = 1  # @line L16
    while h < n:  # @line L17
        step = n // (2 * h)
        for s in range(0, n, 2 * h):  # @line L18
            for k in range(h):  # @line L19
                u = y[s + k]  # @line L20
                v = table[k * step] * y[s + k + h]  # @line L20
                if p is not None:
                    v %= p
                    y[s + k], y[s + k + h] = (u + v) % p, (u - v) % p  # @line L21
                else:
                    y[s + k], y[s + k + h] = u + v, u - v  # @line L21
        h *= 2  # @line L22


def iterative_fft(x: list[S], w: S, p: int | None = None) -> None:
    """Replace x by its DFT, X[k] = sum of x[j] * w**(j*k), in place.

    Precondition: n = len(x) is a power of two and w is a principal n-th root
    of unity (complex, or an integer modulo the prime p). Cost: n lg n
    additions and (n/2) lg n multiplications, n/2 powers for the table, and
    O(n) index operations for the bit reversal.
    """
    n = len(x)  # @line L1
    _check_length(n)
    table = twiddles(w, n, p)  # @line L2
    dif_stages(x, table, p)
    bit_reverse(x)


def cyclic_convolution(a: list[S], b: list[S], w: S, p: int | None = None) -> list[S]:
    """Return c with c[m] = sum of a[j] * b[(m - j) mod n], with no bit reversal.

    Same preconditions as iterative_fft, and n must be a unit (always true
    over the complex numbers, and modulo a prime p > n). Cost: 3 n lg n
    additions and (3/2) n lg n + 2n multiplications.
    """
    n = len(a)
    if len(b) != n:
        raise ValueError("the two inputs must have the same length")
    _check_length(n)
    fa, fb = list(a), list(b)
    table = twiddles(w, n, p)
    dif_stages(fa, table, p)  # @line L13
    dif_stages(fb, table, p)  # @line L13
    if p is None:
        c = [u * v for u, v in zip(fa, fb)]  # @line L14
        inv_table = twiddles(1 / w, n)  # @line L15
    else:
        c = [u * v % p for u, v in zip(fa, fb)]  # @line L14
        inv_table = twiddles(pow(w, -1, p), n, p)  # @line L15
    dit_stages(c, inv_table, p)
    if p is None:
        return [v / n for v in c]  # @line L23
    n_inv = pow(n, -1, p)
    return [v * n_inv % p for v in c]  # @line L23
