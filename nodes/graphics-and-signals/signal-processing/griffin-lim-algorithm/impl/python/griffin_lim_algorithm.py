# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/griffin-lim-algorithm/. The authors are listed in prov/KC8JAJ.jsonl.

"""The Griffin-Lim algorithm: a real signal whose STFT magnitude is close to a target.

The STFT has frames at s = m R for -N < s < L, window w of length N and an
N-point DFT, as on the short-time Fourier transform page. Each iteration takes
the target magnitude with the current phase, then the least squares signal
(weighted overlap-add). The spectral distance

    D(x) = sum over m, k of (|X_m[k]| - A_m[k])^2

does not increase from one iteration to the next.
"""

import cmath
import math
import random
from typing import Optional, Sequence


def fft(a: Sequence[complex]) -> list[complex]:
    """Radix-2 iterative FFT. The length must be a power of two."""
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


def ifft(a: Sequence[complex]) -> list[complex]:
    n = len(a)
    return [v.conjugate() / n for v in fft([v.conjugate() for v in a])]


def hann_periodic(n: int) -> list[float]:
    return [0.5 - 0.5 * math.cos(2 * math.pi * j / n) for j in range(n)]


def frame_starts(length: int, n: int, hop: int) -> list[int]:
    return [m * hop for m in range(-((n - 1) // hop), (length - 1) // hop + 1)]


def stft(x: Sequence[float], w: Sequence[float], hop: int) -> list[list[complex]]:
    n, length = len(w), len(x)
    return [fft([x[s + j] * w[j] if 0 <= s + j < length else 0.0 for j in range(n)]) for s in frame_starts(length, n, hop)]


def istft_ls(spec: Sequence[Sequence[complex]], w: Sequence[float], hop: int, length: int) -> list[float]:
    """The real signal on 0 .. length-1 whose STFT is nearest to spec in the sum of squares.

    x[n] = sum_m w[n - s_m] Re y_m[n - s_m] / sum_m w[n - s_m]^2, with y_m the inverse DFT of frame m.
    """
    n = len(w)
    num = [0.0] * length  # @line L8
    den = [0.0] * length
    for s, row in zip(frame_starts(length, n, hop), spec):  # @line L9
        seg = ifft(row)  # @line L10
        for j in range(n):  # @line L11
            i = s + j
            if 0 <= i < length:
                num[i] += w[j] * seg[j].real
                den[i] += w[j] * w[j]
    if min(den) <= 0:
        raise ValueError("the squared window does not cover every sample")
    return [a / b for a, b in zip(num, den)]  # @line L12


def spectral_distance(spec: Sequence[Sequence[complex]], mag: Sequence[Sequence[float]]) -> float:
    return sum((abs(v) - a) ** 2 for row, arow in zip(spec, mag) for v, a in zip(row, arow))


def with_magnitude(spec: Sequence[Sequence[complex]], mag: Sequence[Sequence[float]]) -> list[list[complex]]:
    """The nearest array with the target magnitude: keep each phase. A zero bin gets phase 0."""
    return [[a * (v / abs(v)) if v != 0 else complex(a) for v, a in zip(row, arow)] for row, arow in zip(spec, mag)]


def griffin_lim(
    mag: Sequence[Sequence[float]],
    w: Sequence[float],
    hop: int,
    length: int,
    iterations: int,
    rng: Optional[random.Random] = None,
) -> tuple[list[float], list[float]]:
    """Run the iteration from a random phase (or zero phase if rng is None).

    Return the last signal and the distance D after each projection onto
    consistent STFTs: history[0] is D of the first estimate.
    """
    if rng is None:  # @line L1
        spec = [[complex(a) for a in row] for row in mag]
    else:
        spec = [[a * cmath.exp(2j * math.pi * rng.random()) for a in row] for row in mag]
    x = istft_ls(spec, w, hop, length)  # @line L2
    history = []
    for _ in range(iterations):  # @line L3
        cur = stft(x, w, hop)  # @line L4
        history.append(spectral_distance(cur, mag))
        x = istft_ls(with_magnitude(cur, mag), w, hop, length)  # @line L5 L6
    history.append(spectral_distance(stft(x, w, hop), mag))
    return x, history  # @line L7
