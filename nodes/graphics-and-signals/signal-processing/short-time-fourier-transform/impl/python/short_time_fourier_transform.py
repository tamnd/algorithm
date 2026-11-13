# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/short-time-fourier-transform/. The authors are listed in prov/YJH16Z.jsonl.

"""The short-time Fourier transform and its two overlap-add inverses.

A frame starts at s = m R for every integer m with -N < s < L, so each sample
of x[0 .. L-1] lies in the same number of frames, and the samples of x outside
0 .. L-1 are zero. Frame m holds X_m[k] = sum_j x[s + j] w[j] e^(-2 pi i j k / N),
k = 0 .. N-1, in radians per sample omega_k = 2 pi k / N (Hz: k fs / N).
"""

import cmath
import math
from fractions import Fraction
from typing import Sequence


def fft(a: Sequence[complex]) -> list[complex]:
    """Radix-2 iterative FFT, A[k] = sum of a[j] e^(-2 pi i j k / n). n must be a power of two."""
    n = len(a)
    if n == 0 or n & (n - 1):
        raise ValueError("length must be a power of two")
    out = [complex(v) for v in a]
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
    while size <= n:
        step = cmath.exp(-2j * math.pi / size)
        half = size // 2
        for start in range(0, n, size):
            tw = 1 + 0j
            for k in range(start, start + half):
                u, v = out[k], out[k + half] * tw
                out[k], out[k + half] = u + v, u - v
                tw *= step
        size *= 2
    return out


def dft(a: Sequence[complex]) -> list[complex]:
    """The defining sum, O(n^2). Works for every length."""
    n = len(a)
    return [sum(a[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def transform(a: Sequence[complex]) -> list[complex]:
    n = len(a)
    return fft(a) if n and not n & (n - 1) else dft(a)


def inverse_transform(a: Sequence[complex]) -> list[complex]:
    """Inverse DFT with the 1/n factor, by conjugation of the forward transform."""
    n = len(a)
    return [v.conjugate() / n for v in transform([v.conjugate() for v in a])]


def hann_periodic(n: int) -> list[float]:
    """w[j] = 1/2 - 1/2 cos(2 pi j / n), the DFT-even Hann window."""
    return [0.5 - 0.5 * math.cos(2 * math.pi * j / n) for j in range(n)]


def hann_symmetric(n: int) -> list[float]:
    """w[j] = 1/2 - 1/2 cos(2 pi j / (n - 1)), the symmetric Hann window (w[0] = w[n-1] = 0)."""
    return [0.5 - 0.5 * math.cos(2 * math.pi * j / (n - 1)) for j in range(n)]


def frame_starts(length: int, n: int, hop: int) -> list[int]:
    """All s = m hop with -n < s < length, in increasing order."""
    m_lo = -((n - 1) // hop)
    m_hi = (length - 1) // hop
    return [m * hop for m in range(m_lo, m_hi + 1)]


def overlap_sums(w: Sequence, hop: int) -> list:
    """S[r] = sum of w[r + m hop] over m, r = 0 .. hop-1. The window is COLA for this hop iff S is constant."""
    return [sum(w[j] for j in range(r, len(w), hop)) for r in range(hop)]


def is_cola(w: Sequence, hop: int, tol: float = 0.0) -> bool:
    s = overlap_sums(w, hop)
    return max(s) - min(s) <= tol


def stft(x: Sequence[float], w: Sequence[float], hop: int) -> tuple[list[int], list[list[complex]]]:
    """Return the frame starts and the N-point spectrum of each windowed frame."""
    n, length = len(w), len(x)
    starts = frame_starts(length, n, hop)
    frames = []  # @line L1
    for s in starts:  # @line L2 L3
        seg = [x[s + j] * w[j] if 0 <= s + j < length else 0.0 for j in range(n)]  # @line L4
        frames.append(transform(seg))  # @line L5
    return starts, frames  # @line L6


def stft_direct(x: Sequence[float], w: Sequence[float], hop: int) -> list[list[complex]]:
    """The defining double sum, one term at a time, as a reference."""
    n, length = len(w), len(x)
    out = []
    for s in frame_starts(length, n, hop):
        row = []
        for k in range(n):
            acc = 0j
            for j in range(n):
                if 0 <= s + j < length:
                    acc += x[s + j] * w[j] * cmath.exp(-2j * math.pi * j * k / n)
            row.append(acc)
        out.append(row)
    return out


def istft_ola(starts: Sequence[int], frames: Sequence[Sequence[complex]], length: int, gain: float) -> list[float]:
    """Overlap-add: invert each frame, add the windowed frames, divide by the COLA constant gain."""
    y = [0.0] * length  # @line L7
    for s, spec in zip(starts, frames):  # @line L8
        seg = inverse_transform(spec)  # @line L9
        for j, v in enumerate(seg):  # @line L10
            if 0 <= s + j < length:  # @line L11: the division by gain is done once, at the end
                y[s + j] += v.real
    return [v / gain for v in y]  # @line L12


def istft_wola(starts: Sequence[int], frames: Sequence[Sequence[complex]], w: Sequence[float], length: int) -> list[float]:
    """Weighted overlap-add, the least squares inverse: sum of w y_m over sum of w^2.

    It inverts any window whose shifted squares never sum to zero on 0 .. length-1.
    """
    num = [0.0] * length
    den = [0.0] * length
    for s, spec in zip(starts, frames):
        seg = inverse_transform(spec)
        for j, v in enumerate(seg):
            if 0 <= s + j < length:
                num[s + j] += w[j] * v.real
                den[s + j] += w[j] * w[j]
    if min(den) <= 0:
        raise ValueError("the squared window does not cover every sample")
    return [a / b for a, b in zip(num, den)]


def triangle_periodic(n: int) -> list[Fraction]:
    """w[j] = 1 - |j - n/2| / (n/2), exact; COLA with gain 1 for hop n/2 (n even)."""
    h = Fraction(n, 2)
    return [1 - abs(j - h) / h for j in range(n)]
