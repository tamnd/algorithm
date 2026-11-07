# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-fft/. The authors are listed in prov/BWBTC5.jsonl.

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


def _complex_table(w: complex, n: int, sign: int) -> list[complex]:
    """Return the powers w**(sign*k), 0 <= k < n/2, computed from the angle.

    w must be close to exp(2*pi*i*m/n) for an integer m. The powers are taken
    from the exact angle 2*pi*m*k/n and not by repeated multiplication, whose
    error grows with k (see the page on twiddle factors).
    """
    m = round(cmath.phase(w) * n / (2 * cmath.pi)) % n
    if abs(w - _unit(m, n)) > 1e-9:
        raise ValueError("w is not close to a root of unity of order dividing n")
    return [_unit(sign * m * k, n) for k in range(n // 2)]


def inverse_fft(y: list[S], w: S, p: int | None = None, scale: bool = True) -> None:
    """Replace y by its inverse DFT, x[j] = (1/n) * sum of y[k] * w**(-j*k), in place.

    Precondition: n = len(y) is a power of two and w is a principal n-th root
    of unity, the same root the forward transform used: a complex number such
    as exp(-2j*pi/n) when p is None, or an integer modulo the odd prime p.
    The stages of the radix-2 decimation-in-time FFT are undone in reverse
    order, each by the butterfly (a, b) -> (a + b, w**(-k) * (a - b)), which
    gives back twice the stage input; then the bit-reversal permutation is
    undone. With scale=False the result is n * x, and no division by n is done.

    Cost: n lg n additions and (n/2) lg n multiplications in the ring, plus n
    multiplications by 1/n when scale is True, n/2 powers for the table, and
    O(n) index operations for the permutation.
    """
    n = len(y)  # @line L1
    t = _check_length(n)
    if p is None:
        table = _complex_table(w, n, -1)  # @line L2
    else:
        w_inv = pow(w, -1, p)
        table = [pow(w_inv, k, p) for k in range(n // 2)]  # @line L2
    h = n // 2  # @line L3
    while h >= 1:  # @line L4
        step = n // (2 * h)
        for s in range(0, n, 2 * h):  # @line L5
            for k in range(h):  # @line L6
                a, b = y[s + k], y[s + k + h]  # @line L7
                if p is None:
                    y[s + k] = a + b  # @line L8
                    y[s + k + h] = table[k * step] * (a - b)  # @line L9
                else:
                    y[s + k] = (a + b) % p  # @line L8
                    y[s + k + h] = table[k * step] * (a - b) % p  # @line L9
        h //= 2  # @line L10
    rev = [0] * n
    for j in range(1, n):
        rev[j] = (rev[j >> 1] >> 1) | ((j & 1) << (t - 1))
    for j in range(n):  # @line L11
        if j < rev[j]:  # @line L12
            y[j], y[rev[j]] = y[rev[j]], y[j]
    if not scale:
        return
    if p is None:
        for j in range(n):  # @line L13
            y[j] = y[j] / n
    else:
        n_inv = pow(n, -1, p)
        for j in range(n):  # @line L13
            y[j] = y[j] * n_inv % p


def forward_fft(x: list[S], w: S, p: int | None = None) -> None:
    """Replace x by its DFT, X[k] = sum of x[j] * w**(j*k), in place.

    The radix-2 decimation-in-time FFT whose stages inverse_fft undoes, given
    here so that the two can be tested together. Same preconditions.
    """
    n = len(x)
    t = _check_length(n)
    if p is None:
        table = _complex_table(w, n, 1)
    else:
        table = [pow(w, k, p) for k in range(n // 2)]
    rev = [0] * n
    for j in range(1, n):
        rev[j] = (rev[j >> 1] >> 1) | ((j & 1) << (t - 1))
    for j in range(n):
        if j < rev[j]:
            x[j], x[rev[j]] = x[rev[j]], x[j]
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
