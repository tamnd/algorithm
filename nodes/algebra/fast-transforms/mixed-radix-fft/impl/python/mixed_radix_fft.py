# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixed-radix-fft/. The authors are listed in prov/FR88CY.jsonl.

"""Mixed-radix Cooley-Tukey FFT: X_k = sum_j x_j w**(j*k) for n = r_1 r_2 ... r_t."""

from __future__ import annotations

import cmath
import math
from typing import TypeVar

S = TypeVar("S", int, complex)


def _unit(r: int, n: int) -> complex:
    """Return exp(2*pi*i*r/n), exact when r/n is a multiple of 1/4."""
    r %= n
    if (4 * r) % n == 0:
        return (1 + 0j, 1j, -1 + 0j, -1j)[4 * r // n]
    return cmath.exp(2j * math.pi * r / n)


def prime_factors(n: int) -> list[int]:
    """The prime factors of n >= 1, smallest first, with multiplicity."""
    out, d = [], 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def mixed_radix_fft(
    x: list[S],
    radices: list[int] | None = None,
    w: int | None = None,
    p: int | None = None,
    inverse: bool = False,
) -> list[S]:
    """Return the DFT of x, computed by splitting off the radices in order.

    Over C (p is None) the root is exp(-2*pi*i/n), or exp(+2*pi*i/n) with
    the factor 1/n when inverse is True. Modulo a prime p, w must be a
    principal n-th root of unity modulo p; inverse uses w**(-1) and 1/n.
    The radices must be integers >= 2 with product n (default: the prime
    factors of n). The recursion depth is the number of radices, at most lg n.
    """
    n = len(x)
    if n == 0:
        raise ValueError("the input must not be empty")
    rad = prime_factors(n) if radices is None else list(radices)
    if any(r < 2 for r in rad) or math.prod(rad) != n:
        raise ValueError("the radices must be at least 2 and multiply to n")
    if p is None:
        sign = 1 if inverse else -1
        table = [_unit(sign * e, n) for e in range(n)]
    else:
        if w is None or pow(w, n, p) != 1 or any(pow(w, n // q, p) == 1 for q in set(prime_factors(n))):
            raise ValueError("w must be a principal n-th root of unity modulo p")
        wi = pow(w, -1, p) if inverse else w
        table = [pow(wi, e, p) for e in range(n)]

    def mul(a: S, b: S) -> S:
        return a * b if p is None else a * b % p

    def add(a: S, b: S) -> S:
        return a + b if p is None else (a + b) % p

    def fft(start: int, stride: int, level: int) -> list[S]:
        """DFT of x[start], x[start + stride], ... of length n // stride, root table[stride]."""
        size = n // stride  # @line L1
        if size == 1:  # @line L2
            return [x[start]]
        r = rad[level]  # @line L3
        m = size // r
        sub = []
        for l in range(r):  # @line L4
            sub.append(fft(start + l * stride, stride * r, level + 1))  # @line L5
        out = [0] * size
        for k in range(m):  # @line L6
            t = [sub[0][k]] + [mul(table[(l * k * stride) % n], sub[l][k]) for l in range(1, r)]  # @line L7
            for s in range(r):  # @line L8
                acc = t[0]
                for l in range(1, r):  # @line L9
                    e = (l * s) % r
                    acc = add(acc, t[l] if e == 0 else mul(table[e * m * stride % n], t[l]))
                out[k + m * s] = acc
        return out  # @line L10

    y = fft(0, 1, 0)
    if inverse:
        if p is None:
            y = [v / n for v in y]
        else:
            ninv = pow(n, -1, p)
            y = [v * ninv % p for v in y]
    return y
