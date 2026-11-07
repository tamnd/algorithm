# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-fourier-transform/. The authors are listed in prov/14CJHC.jsonl.

from typing import Callable, TypeVar

S = TypeVar("S", int, complex)


def _reducer(p: int | None) -> Callable[[S], S]:
    """Return reduction modulo p, or the identity when p is None."""
    if p is None:
        return lambda a: a
    return lambda a: a % p


def fft(x: list[S], w: S, p: int | None = None) -> None:
    """Replace x by its DFT, X[k] = sum of x[j] * w**(j*k), in place.

    Precondition: n = len(x) is a power of two, and w is a principal n-th
    root of unity: a complex number such as exp(-2j*pi/n) when p is None,
    or an integer modulo the prime p when p is given (then every result is
    reduced modulo p). Cost: (n/2) lg n multiplications and n lg n
    additions in the ring for the butterflies, n/2 powers for the twiddle
    table, and O(n) index operations for the permutation.
    """
    red = _reducer(p)
    n = len(x)  # @line L1
    if n < 1 or n & (n - 1):
        raise ValueError("the length must be a power of two")
    t = n.bit_length() - 1
    table = [red(pow(w, k, p)) if p is not None else w**k for k in range(n // 2)]  # @line L2
    rev = [0] * n
    for j in range(1, n):
        rev[j] = (rev[j >> 1] >> 1) | ((j & 1) << (t - 1))
    for j in range(n):  # @line L3
        if j < rev[j]:  # @line L4
            x[j], x[rev[j]] = x[rev[j]], x[j]
    h = 1  # @line L5
    while h < n:  # @line L6
        step = n // (2 * h)
        for s in range(0, n, 2 * h):  # @line L7
            for k in range(h):  # @line L8
                u = x[s + k]  # @line L9
                v = red(table[k * step] * x[s + k + h])  # @line L10
                x[s + k] = red(u + v)  # @line L11
                x[s + k + h] = red(u - v)  # @line L12
        h *= 2  # @line L13


def inverse_fft(y: list[S], w: S, p: int | None = None) -> None:
    """Replace y by its inverse DFT, x[j] = (1/n) * sum of y[k] * w**(-j*k).

    Precondition: as for fft, with the same root w; n must be a unit (always
    true over the complex numbers, and true modulo a prime p > n). Cost: one
    fft plus n multiplications.
    """
    n = len(y)
    if p is None:
        fft(y, 1 / w)  # @line L14
        for j in range(n):  # @line L15
            y[j] = y[j] / n
    else:
        fft(y, pow(w, -1, p), p)  # @line L14
        n_inv = pow(n, -1, p)
        for j in range(n):  # @line L15
            y[j] = y[j] * n_inv % p
