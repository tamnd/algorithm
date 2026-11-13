# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/overlap-add-method/. The authors are listed in prov/H1GGYR.jsonl.

"""Overlap-add block convolution of a long input x with a filter h of length M.

The input is cut into blocks of B = N - M + 1 samples. Each block is convolved
with h by a cyclic convolution of length N, which equals the linear block
convolution because B + M - 1 = N. The block outputs overlap by M - 1 samples
and are added.

overlap_add uses a radix-2 FFT of size N (a power of two) in floating point.
overlap_add_exact uses the same loop with an exact cyclic convolution of
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
    for i in range(1, n):  # bit reversal permutation
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


def _overlap_add(x: Sequence, h: Sequence, n: int, block_conv: Callable[[list], list]) -> list:
    m, length = len(h), len(x)
    if m == 0 or length == 0:
        return []
    if n < m:
        raise ValueError("the block length N must be at least the filter length M")
    b = n - m + 1  # @line L1: new input samples per block
    y = [0] * (length + m - 1)  # @line L3
    for s in range(0, length, b):  # @line L4
        u = list(x[s:s + b]) + [0] * (n - len(x[s:s + b]))  # @line L5
        v = block_conv(u)  # @line L6: v = u cyclic-conv h = u * h
        for j in range(n):  # @line L7
            if s + j < length + m - 1:  # @line L8
                y[s + j] += v[j]
    return y  # @line L9


def overlap_add(x: Sequence[float], h: Sequence[float], n: int) -> list[float]:
    """Overlap-add with FFTs of size n (a power of two, n >= len(h)).

    Real inputs give a real output. Cost: one FFT of h, then per block one
    forward FFT, n products and one inverse FFT.
    """
    if not h or not x:
        return []
    if n < len(h):
        raise ValueError("the block length N must be at least the filter length M")
    spec_h = fft(list(h) + [0] * (n - len(h)))  # @line L2

    def block_conv(u: list) -> list:
        prod = [a * c for a, c in zip(fft(u), spec_h)]
        return [v / n for v in fft(prod, invert=True)]

    y = _overlap_add(x, h, n, block_conv)
    if all(isinstance(v, (int, float)) for v in list(x) + list(h)):
        return [v.real for v in y]
    return y


def cyclic_convolve(u: Sequence, h: Sequence, n: int) -> list:
    """Exact cyclic convolution of length n by its definition."""
    hp = list(h) + [0] * (n - len(h))
    return [sum(u[k] * hp[(t - k) % n] for k in range(n)) for t in range(n)]


def overlap_add_exact(x: Sequence, h: Sequence, n: int) -> list:
    """Overlap-add with an exact cyclic convolution of any length n >= len(h)."""
    return _overlap_add(x, h, n, lambda u: cyclic_convolve(u, h, n))
