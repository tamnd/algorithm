# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyphase-resampling/. The authors are listed in prov/1Y8M5W.jsonl.

"""Rational sample-rate conversion by L/M with a polyphase filter.

The direct three-stage version upsamples x by L (inserting L - 1 zeros),
filters with h at the high rate and keeps every M-th sample:
y[n] = sum_k h[k] u[nM - k]. The polyphase version writes nM = qL + r with
0 <= r < L; only the taps h[iL + r] meet nonzero samples, so
y[n] = sum_i h[iL + r] x[q - i]. Signals start at index 0.
"""

import math
from typing import Sequence


def resample_poly(x: Sequence, h: Sequence, l: int, m: int) -> list:
    """y[n] for all n with nM < len(h) + L len(x) - 1, the same samples the three-stage version keeps."""
    if l < 1 or m < 1:
        raise ValueError("L and M must be positive")
    k = len(h)
    total = k + l * len(x) - 1
    count = (total - 1) // m + 1 if total > 0 else 0
    phases = [list(h[r::l]) for r in range(l)]  # @line L1: e_r[i] = h[iL + r]
    y = []
    q, r = 0, 0  # @line L2: n M = q L + r
    for _ in range(count):  # @line L3
        acc = 0
        for i, c in enumerate(phases[r]):  # @line L4
            if 0 <= q - i < len(x):
                acc += c * x[q - i]  # @line L5
        y.append(acc)  # @line L6
        r += m  # @line L7: step n by one, so n M grows by M
        q += r // l
        r %= l  # @line L8
    return y


def resample_direct(x: Sequence, h: Sequence, l: int, m: int) -> list:
    """The three-stage reference: upsample by L, filter, keep every M-th sample."""
    u = [0] * (len(x) * l)
    u[::l] = list(x)
    full = [0] * (len(h) + len(u) - 1) if h and u else []
    for i, a in enumerate(h):
        for j, b in enumerate(u):
            full[i + j] += a * b
    return full[::m]


def lowpass_design(l: int, m: int, half_width: int = 10) -> list[float]:
    """A windowed-sinc filter with cutoff pi / max(L, M) radians per sample at the high rate and gain L.

    It has K = 2 half_width max(L, M) + 1 taps and a Hamming window. The gain
    L makes up for the L - 1 zeros between the input samples.
    """
    d = max(l, m)
    k = 2 * half_width * d + 1
    c = (k - 1) / 2
    h = []
    for n in range(k):
        t = n - c
        s = 1 / d if t == 0 else math.sin(math.pi * t / d) / (math.pi * t)
        w = 0.54 - 0.46 * math.cos(2 * math.pi * n / (k - 1))
        h.append(l * s * w)
    return h


def resample(x: Sequence, l: int, m: int, half_width: int = 10) -> list:
    """Change the rate by L/M after reducing the fraction, with the default low-pass filter."""
    g = math.gcd(l, m)
    l, m = l // g, m // g
    return resample_poly(x, lowpass_design(l, m, half_width), l, m)
