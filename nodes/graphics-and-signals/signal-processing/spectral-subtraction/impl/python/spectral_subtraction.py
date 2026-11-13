# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-subtraction/. The authors are listed in prov/EPV4TJ.jsonl.

"""Spectral subtraction with oversubtraction and a spectral floor.

The signal is cut into frames of length L with hop H = L/2 and a periodic
Hann window, whose shifted copies add up to one. In every DFT bin of every
frame, the estimated noise spectrum N_hat (in |.|^gamma units) is subtracted:

    P = max(|Y|^gamma - alpha * N_hat, beta * N_hat),

the magnitude P^(1/gamma) is combined with the noisy phase, and the frames
are put back together by overlap-add. With gamma = 1, alpha = 1, beta = 0
this is Boll's magnitude subtraction with half-wave rectification; gamma = 2
with alpha > 1 and beta > 0 is the form of Berouti, Schwartz and Makhoul.
"""

import cmath
import math
from typing import Sequence


def periodic_hann(length: int) -> list[float]:
    """w[n] = (1 - cos(2 pi n / L)) / 2; w[n] + w[n + L/2] = 1 for even L."""
    return [0.5 - 0.5 * math.cos(2 * math.pi * n / length) for n in range(length)]


def dft(a: Sequence[complex], inverse: bool = False) -> list[complex]:
    """Radix-2 FFT for powers of two, the defining sum otherwise; the inverse has the 1/N."""
    n = len(a)
    sign = 1 if inverse else -1
    if n > 1 and n & (n - 1) == 0:
        out = _fft([complex(v) for v in a], sign)
    else:
        out = [sum(complex(a[t]) * cmath.exp(sign * 2j * math.pi * k * t / n) for t in range(n))
               for k in range(n)]
    return [v / n for v in out] if inverse else out


def _fft(a: list[complex], sign: int) -> list[complex]:
    n = len(a)
    if n == 1:
        return a
    even, odd = _fft(a[0::2], sign), _fft(a[1::2], sign)
    out = [0j] * n
    for k in range(n // 2):
        t = cmath.exp(sign * 2j * math.pi * k / n) * odd[k]
        out[k], out[k + n // 2] = even[k] + t, even[k] - t
    return out


def _frames(x: Sequence[float], length: int) -> tuple[list[float], int]:
    """Pad with L - H zeros at both ends so that every sample is covered by two frames."""
    hop = length // 2
    pad = length - hop
    padded = [0.0] * pad + [float(v) for v in x] + [0.0] * (pad + (-len(x)) % hop)
    count = (len(padded) - length) // hop + 1
    return padded, count


def noise_estimate(v: Sequence[float], length: int, gamma: float = 2.0) -> list[float]:
    """Average |V_j[m]|^gamma over the frames of a noise-only signal v."""
    if length < 2 or length % 2:
        raise ValueError("frame length must be even and at least 2")
    w, hop = periodic_hann(length), length // 2
    total = [0.0] * length
    count = (len(v) - length) // hop + 1
    if count < 1:
        raise ValueError("noise signal shorter than one frame")
    for j in range(count):
        spec = dft([w[n] * v[j * hop + n] for n in range(length)])  # @line L1
        total = [t + abs(s) ** gamma for t, s in zip(total, spec)]
    return [t / count for t in total]  # @line L2


def subtract_bins(spec: Sequence[complex], n_hat: Sequence[float], alpha: float, beta: float,
                  gamma: float = 2.0) -> list[complex]:
    """Lines L6 to L8 on one frame: subtract, floor, and keep the noisy phase."""
    out = []
    for y, n in zip(spec, n_hat):  # @line L6
        p = max(abs(y) ** gamma - alpha * n, beta * n)  # @line L7
        out.append(0j if y == 0 else p ** (1 / gamma) * y / abs(y))  # @line L8
    return out


def spectral_subtraction(y: Sequence[float], n_hat: Sequence[float], length: int,
                         alpha: float = 1.0, beta: float = 0.0, gamma: float = 2.0) -> list[float]:
    """Enhance y frame by frame; n_hat comes from noise_estimate with the same length and gamma."""
    if length < 2 or length % 2 or len(n_hat) != length:
        raise ValueError("need an even frame length equal to len(n_hat)")
    w, hop = periodic_hann(length), length // 2
    padded, count = _frames(y, length)
    out = [0.0] * len(padded)  # @line L3
    for j in range(count):  # @line L4
        spec = dft([w[n] * padded[j * hop + n] for n in range(length)])  # @line L5
        frame = dft(subtract_bins(spec, n_hat, alpha, beta, gamma), inverse=True)
        for n in range(length):  # @line L9
            out[j * hop + n] += frame[n].real
    pad = length - hop
    return out[pad:pad + len(y)]  # @line L10
