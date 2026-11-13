# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/overlap-save-method/. The authors are listed in prov/6E7154.jsonl.

"""Overlap-save block convolution of a long input x with a filter h of length M.

The input gets M - 1 leading zeros. Blocks of N samples overlap by M - 1
samples, so each block starts B = N - M + 1 samples after the one before.
A cyclic convolution of length N of each block with h is correct at the
indices M - 1 to N - 1, which are kept; the first M - 1 outputs are wrapped
and are discarded.

overlap_save uses a radix-2 FFT of size N (a power of two) in floating point.
overlap_save_exact uses the same loop with an exact cyclic convolution of
length N (the defining sum), so it works on int and Fraction inputs.
"""

import cmath
from typing import Callable, Sequence


def fft(a: Sequence[complex], invert: bool = False) -> list[complex]:
    """Iterative radix-2 FFT. len(a) must be a power of two. The inverse is not scaled."""
    n = len(a)
    if n & (n - 1):
        raise ValueError("FFT size must be a power of two")
    out = list(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            out[i], out[j] = out[j], out[i]
    size = 2
    sign = 1 if invert else -1
    while size <= n:
        w_step = cmath.exp(sign * 2j * cmath.pi / size)
        for start in range(0, n, size):
            w = 1 + 0j
            for k in range(size // 2):
                u = out[start + k]
                v = out[start + k + size // 2] * w
                out[start + k] = u + v
                out[start + k + size // 2] = u - v
                w *= w_step
        size *= 2
    return out


def _overlap_save(x: Sequence, h: Sequence, n: int, block_conv: Callable[[list], list]) -> list:
    m, length = len(h), len(x)
    if m == 0 or length == 0:
        return []
    if n < m:
        raise ValueError("the block length N must be at least the filter length M")
    b = n - m + 1  # @line L1: new outputs per block
    out_len = length + m - 1

    def xp(t: int):  # @line L3: x' = (M - 1 zeros, then x, then zeros)
        i = t - (m - 1)
        return x[i] if 0 <= i < length else 0

    y = [0] * out_len  # @line L4
    for s in range(0, out_len, b):  # @line L5
        u = [xp(s + j) for j in range(n)]  # @line L6
        v = block_conv(u)  # @line L7: v = u cyclic-conv h
        for j in range(m - 1, n):  # @line L8: keep the unwrapped outputs
            t = s + j - (m - 1)
            if t < out_len:  # @line L9
                y[t] = v[j]
    return y  # @line L10


def overlap_save(x: Sequence[float], h: Sequence[float], n: int) -> list[float]:
    """Overlap-save with FFTs of size n (a power of two, n >= len(h))."""
    if not h or not x:
        return []
    if n < len(h):
        raise ValueError("the block length N must be at least the filter length M")
    spec_h = fft(list(h) + [0] * (n - len(h)))  # @line L2

    def block_conv(u: list) -> list:
        prod = [a * c for a, c in zip(fft(u), spec_h)]
        return [v / n for v in fft(prod, invert=True)]

    y = _overlap_save(x, h, n, block_conv)
    if all(isinstance(v, (int, float)) for v in list(x) + list(h)):
        return [v.real for v in y]
    return y


def cyclic_convolve(u: Sequence, h: Sequence, n: int) -> list:
    """Exact cyclic convolution of length n by its definition."""
    hp = list(h) + [0] * (n - len(h))
    return [sum(u[k] * hp[(t - k) % n] for k in range(n)) for t in range(n)]


def overlap_save_exact(x: Sequence, h: Sequence, n: int) -> list:
    """Overlap-save with an exact cyclic convolution of any length n >= len(h)."""
    return _overlap_save(x, h, n, lambda u: cyclic_convolve(u, h, n))
