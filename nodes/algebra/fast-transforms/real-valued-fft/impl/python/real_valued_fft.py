# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/real-valued-fft/. The authors are listed in prov/C9SKTZ.jsonl.

"""DFT of real input of length n through one complex FFT of length n/2.

Over C the root is w = exp(-2*pi*i/n). The same code runs exactly over the
ring Z_p[i] = Z_p[t]/(t^2 + 1), p an odd prime, where conjugation is
a + b i -> a - b i and the "real" numbers are Z_p; there w must satisfy
w**n = 1, w**(n/2) = -1 and w * conj(w) = 1.
"""

from __future__ import annotations

import cmath
import math
from typing import Union


class GaussMod:
    """The element a + b i of Z_p[i]."""

    __slots__ = ("a", "b", "p")

    def __init__(self, a: int, b: int, p: int) -> None:
        self.a, self.b, self.p = a % p, b % p, p

    def __add__(self, o: "GaussMod") -> "GaussMod":
        return GaussMod(self.a + o.a, self.b + o.b, self.p)

    def __sub__(self, o: "GaussMod") -> "GaussMod":
        return GaussMod(self.a - o.a, self.b - o.b, self.p)

    def __mul__(self, o: "GaussMod | int") -> "GaussMod":
        if isinstance(o, int):
            return GaussMod(self.a * o, self.b * o, self.p)
        return GaussMod(self.a * o.a - self.b * o.b, self.a * o.b + self.b * o.a, self.p)

    __rmul__ = __mul__

    def __eq__(self, o: object) -> bool:
        return isinstance(o, GaussMod) and (self.a, self.b, self.p) == (o.a, o.b, o.p)

    def __hash__(self) -> int:
        return hash((self.a, self.b, self.p))

    def __repr__(self) -> str:
        return f"GaussMod({self.a}, {self.b}, {self.p})"

    def conjugate(self) -> "GaussMod":
        return GaussMod(self.a, -self.b, self.p)

    def __pow__(self, e: int) -> "GaussMod":
        r, b = GaussMod(1, 0, self.p), self
        if e < 0:
            n = (self.a * self.a + self.b * self.b) % self.p
            b, e = b.conjugate() * pow(n, -1, self.p), -e
        while e:
            if e & 1:
                r = r * b
            b, e = b * b, e >> 1
        return r


Num = Union[complex, GaussMod]


def _unit(r: int, n: int) -> complex:
    """Return exp(2*pi*i*r/n), exact when r/n is a multiple of 1/4."""
    r %= n
    if (4 * r) % n == 0:
        return (1 + 0j, 1j, -1 + 0j, -1j)[4 * r // n]
    return cmath.exp(2j * math.pi * r / n)


def _check(n: int) -> None:
    if n < 1 or n & (n - 1):
        raise ValueError("the length must be a power of two")


def _powers(n: int, w: GaussMod | None, sign: int) -> list[Num]:
    """W[k] = w**(sign*k) for 0 <= k <= n/2 (w = exp(-2*pi*i/n) over C)."""
    if w is None:
        return [_unit(-sign * k, n) for k in range(n // 2 + 1)]
    if w ** n != GaussMod(1, 0, w.p) or (n > 1 and w ** (n // 2) != GaussMod(-1, 0, w.p)):
        raise ValueError("w must satisfy w**n = 1 and w**(n/2) = -1")
    if w * w.conjugate() != GaussMod(1, 0, w.p):
        raise ValueError("w must satisfy w * conj(w) = 1")
    base = w if sign > 0 else w ** -1
    out, cur = [], GaussMod(1, 0, w.p)
    for _ in range(n // 2 + 1):
        out.append(cur)
        cur = cur * base
    return out


def _fft(z: list[Num], table: list[Num]) -> None:
    """In-place radix-2 DIT FFT of length h; table[k] is the k-th power of a root of order h, k < h/2."""
    h = len(z)
    j = 0
    for i in range(1, h):
        bit = h >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            z[i], z[j] = z[j], z[i]
    size = 1
    while size < h:
        step = h // (2 * size)
        for s in range(0, h, 2 * size):
            for k in range(size):
                u, v = z[s + k], table[k * step] * z[s + k + size]
                z[s + k], z[s + k + size] = u + v, u - v
        size *= 2


def real_fft(x: list, w: GaussMod | None = None) -> list[Num]:
    """Return X_0, ..., X_{n/2} of the DFT of the real sequence x, n = len(x) a power of two."""
    n = len(x)
    _check(n)
    if w is None:
        one, i, half = 1 + 0j, 1j, 0.5
    else:
        p = w.p
        one, i, half = GaussMod(1, 0, p), GaussMod(0, 1, p), (p + 1) // 2
    if n == 1:
        return [one * x[0]]
    W = _powers(n, w, 1)  # W[k] = w**k
    h = n // 2  # @line L1
    z = [one * x[2 * j] + i * x[2 * j + 1] for j in range(h)]  # @line L2
    _fft(z, [W[2 * k] for k in range(h // 2)])  # @line L3
    z.append(z[0])  # @line L4  Z_h = Z_0
    minus_i_half = i * (-half if w is None else (w.p - half))
    out = []
    for k in range(h + 1):  # @line L5
        c = z[h - k].conjugate()
        e = (z[k] + c) * half  # @line L6
        o = (z[k] - c) * minus_i_half  # @line L7  divide by 2i
        out.append(e + W[k] * o)  # @line L8
    return out  # @line L9


def inverse_real_fft(X: list[Num], w: GaussMod | None = None) -> list:
    """Return the real sequence x of length n = 2 (len(X) - 1) with real_fft(x, w) = X."""
    n = 2 * (len(X) - 1) if len(X) > 1 else 1
    _check(n)
    if w is None:
        i, half = 1j, 0.5
    else:
        p = w.p
        i, half = GaussMod(0, 1, p), (p + 1) // 2
    if n == 1:
        return [X[0].real if w is None else X[0].a]
    h = n // 2
    Winv = _powers(n, w, -1)  # w**(-k)
    Z = []
    for k in range(h):
        c = X[h - k].conjugate()
        e = (X[k] + c) * half
        o = (X[k] - c) * half * Winv[k]
        Z.append(e + i * o)
    _fft(Z, [Winv[2 * k] for k in range(h // 2)])
    inv_h = 1 / h if w is None else pow(h, -1, w.p)
    out = []
    for v in Z:
        v = v * inv_h
        out.extend([v.real, v.imag] if w is None else [v.a, v.b])
    return out
