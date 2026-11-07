# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rader-fft/. The authors are listed in prov/8K6AGB.jsonl.

"""Rader's algorithm: the DFT of prime length n as a cyclic convolution of length n - 1.

X_k = sum_j x_j w**(j*k). Over C, w = exp(-2*pi*i/n). Modulo a prime P, w must
have order n modulo P, and P - 1 must be divisible by a power of two L >= 2n - 3,
which is used for the inner convolution by a number-theoretic transform.
"""

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


def _prime_divisors(m: int) -> list[int]:
    out, d = [], 2
    while d * d <= m:
        if m % d == 0:
            out.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        out.append(m)
    return out


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def primitive_root(q: int) -> int:
    """The least primitive root modulo the prime q."""
    if q == 2:
        return 1
    ps = _prime_divisors(q - 1)
    for g in range(2, q):
        if all(pow(g, (q - 1) // r, q) != 1 for r in ps):
            return g
    raise ValueError("no primitive root")


def _fft(a: list[S], table: list[S], P: int | None) -> None:
    """In-place radix-2 DIT FFT; table[k] = (root of order len(a))**k for k < len(a)/2."""
    L = len(a)
    j = 0
    for i in range(1, L):
        bit = L >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    h = 1
    while h < L:
        step = L // (2 * h)
        for s in range(0, L, 2 * h):
            for k in range(h):
                u, v = a[s + k], table[k * step] * a[s + k + h]
                if P is None:
                    a[s + k], a[s + k + h] = u + v, u - v
                else:
                    a[s + k], a[s + k + h] = (u + v) % P, (u - v) % P
        h *= 2


def cyclic_convolution(a: list[S], b: list[S], P: int | None = None) -> list[S]:
    """c_p = sum_q a_q b_{(p - q) mod N} for N = len(a) = len(b), by FFTs of length L >= 2N - 1."""
    N = len(a)
    L = 1
    while L < 2 * N - 1:
        L *= 2
    if P is None:
        fwd = [_unit(-k, L) for k in range(L // 2)]
        inv = [_unit(k, L) for k in range(L // 2)]
    else:
        if (P - 1) % L:
            raise ValueError("P - 1 must be divisible by the convolution length")
        r = pow(primitive_root(P), (P - 1) // L, P)
        fwd = [pow(r, k, P) for k in range(L // 2)]
        inv = [pow(r, -k, P) for k in range(L // 2)]
    A = list(a) + [0] * (L - N)
    B = list(b) + [0] * (L - N)
    _fft(A, fwd, P)
    _fft(B, fwd, P)
    C = [u * v if P is None else u * v % P for u, v in zip(A, B)]
    _fft(C, inv, P)
    scale = 1 / L if P is None else pow(L, -1, P)
    lin = [v * scale if P is None else v * scale % P for v in C]
    out = lin[:N]
    for p in range(N - 1):
        out[p] = out[p] + lin[p + N] if P is None else (out[p] + lin[p + N]) % P
    return out


def rader_fft(x: list[S], w: int | None = None, P: int | None = None, inverse: bool = False) -> list[S]:
    """Return the DFT of x, whose length n must be prime.

    Over C (P is None) the root is exp(-2*pi*i/n), or exp(+2*pi*i/n) with the
    factor 1/n when inverse is True. Modulo P, w must have order n; inverse
    uses w**(-1) and the factor 1/n.
    """
    n = len(x)
    if not is_prime(n):
        raise ValueError("the length must be prime")
    if P is not None and (w is None or w % P == 1 or pow(w, n, P) != 1):
        raise ValueError("w must have order n modulo P")
    sign = 1 if inverse else -1
    if P is None:
        root = lambda r: _unit(sign * r, n)  # noqa: E731  w**r over C
    else:
        wi = pow(w, -1, P) if inverse else w
        root = lambda r: pow(wi, r, P)  # noqa: E731
    g = primitive_root(n)  # @line L1
    N = n - 1
    a = [x[pow(g, q, n)] for q in range(N)]  # @line L2
    b = [root(pow(g, N - m, n)) for m in range(N)]  # @line L3  w**(g**(-m))
    c = cyclic_convolution(a, b, P)  # @line L4
    out = [0] * n
    out[0] = sum(x) if P is None else sum(x) % P  # @line L5
    for p in range(N):  # @line L6
        k = pow(g, N - p, n)
        out[k] = x[0] + c[p] if P is None else (x[0] + c[p]) % P  # @line L7
    if inverse:
        out = [v / n for v in out] if P is None else [v * pow(n, -1, P) % P for v in out]
    return out  # @line L8
