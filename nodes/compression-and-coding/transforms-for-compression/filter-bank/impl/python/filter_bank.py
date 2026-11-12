# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filter-bank/. The authors are listed in prov/A2J8ZX.jsonl.

"""Critically sampled M-channel FIR filter banks, in pure Python.

Analysis: channel k filters the input with h_k and keeps every M-th sample.
Synthesis: channel k puts M - 1 zeros after each sample, filters with f_k,
and the channels are added. Signals are finite lists; a signal x stands for
the sequence x[0], x[1], ... with zeros outside. Convolution is linear (not
circular), so the output is longer than the input by the filter lengths.

The two-channel filters below are the standard examples: Haar, the LeGall
5/3 biorthogonal pair and the 4-tap orthogonal filter of Daubechies.
"""

import math
from typing import List, Optional, Sequence, Tuple

Vector = List[float]


def convolve(x: Sequence[float], h: Sequence[float]) -> Vector:
    """Linear convolution: y[n] = sum_j h[j] x[n - j]. Cost Theta(len(x) len(h))."""
    if not x or not h:
        return []
    y = [0.0] * (len(x) + len(h) - 1)
    for i, xi in enumerate(x):
        if xi:
            for j, hj in enumerate(h):
                y[i + j] += xi * hj
    return y


def downsample(x: Sequence[float], m: int) -> Vector:
    """Keep x[0], x[M], x[2M], ..."""
    return list(x[::m])


def upsample(x: Sequence[float], m: int) -> Vector:
    """Put M - 1 zeros after each sample."""
    y = [0.0] * (len(x) * m)
    y[::m] = list(x)
    return y


def analysis(x: Sequence[float], filters: Sequence[Sequence[float]], m: int) -> List[Vector]:
    """Direct form: filter with each h_k, then keep every M-th sample. Cost Theta(M len(x) L)."""
    return [downsample(convolve(x, h), m) for h in filters]


def analysis_polyphase(x: Sequence[float], filters: Sequence[Sequence[float]], m: int) -> List[Vector]:
    """Same output as analysis, but computes only the samples that are kept.

    v_k[i] = sum_j h_k[j] x[iM - j]: each input sample meets each tap once per
    channel, so the cost is Theta(len(x) L) per channel, M times less than the direct form.
    """
    out = []
    for h in filters:
        total = len(x) + len(h) - 1
        count = (total + m - 1) // m if total > 0 else 0
        v = [0.0] * count
        for i in range(count):
            n = i * m
            s = 0.0
            lo = max(0, n - len(x) + 1)
            hi = min(len(h) - 1, n)
            for j in range(lo, hi + 1):
                s += h[j] * x[n - j]
            v[i] = s
        out.append(v)
    return out


def synthesis(subbands: Sequence[Sequence[float]], filters: Sequence[Sequence[float]], m: int) -> Vector:
    """Upsample each channel by M, filter with f_k and add the channels."""
    parts = [convolve(upsample(v, m), f) for v, f in zip(subbands, filters)]
    size = max(len(p) for p in parts)
    y = [0.0] * size
    for p in parts:
        for i, val in enumerate(p):
            y[i] += val
    return y


def reconstruction_delay(x: Sequence[float], y: Sequence[float], tol: float = 1e-9) -> Optional[Tuple[float, int]]:
    """Return (c, l) if y[n] = c x[n - l] for all n (within tol), else None."""
    i0 = next((i for i, v in enumerate(x) if abs(v) > tol), None)
    if i0 is None:
        return None
    scale = max(1.0, max(abs(v) for v in x))
    for lag in range(len(y) - i0):
        c = y[i0 + lag] / x[i0]
        if abs(c) <= tol:
            continue
        ok = all(abs(y[n] - (c * x[n - lag] if 0 <= n - lag < len(x) else 0.0)) <= tol * scale * max(1.0, abs(c)) for n in range(len(y)))
        if ok:
            return c, lag
    return None


def alias_cancelling_synthesis(h0: Sequence[float], h1: Sequence[float]) -> Tuple[Vector, Vector]:
    """Synthesis filters F0(z) = H1(-z) and F1(z) = -H0(-z), which cancel the alias term."""
    f0 = [((-1) ** n) * c for n, c in enumerate(h1)]
    f1 = [-((-1) ** n) * c for n, c in enumerate(h0)]
    return f0, f1


def two_channel(x: Sequence[float], h0: Sequence[float], h1: Sequence[float], f0: Sequence[float], f1: Sequence[float]) -> Vector:
    """Analysis with (h0, h1), decimation by 2, then synthesis with (f0, f1)."""
    return synthesis(analysis(x, [h0, h1], 2), [f0, f1], 2)


S2 = math.sqrt(2.0)
S3 = math.sqrt(3.0)

# Haar: orthogonal, two taps.
HAAR_H0 = [1 / S2, 1 / S2]
HAAR_H1 = [1 / S2, -1 / S2]

# LeGall 5/3 analysis pair (the reversible filter of JPEG 2000 without the lifting rounding).
LEGALL_H0 = [-1 / 8, 2 / 8, 6 / 8, 2 / 8, -1 / 8]
LEGALL_H1 = [-1 / 2, 1.0, -1 / 2]

# Daubechies 4-tap orthogonal lowpass filter and its conjugate quadrature highpass.
D4_H0 = [(1 + S3) / (4 * S2), (3 + S3) / (4 * S2), (3 - S3) / (4 * S2), (1 - S3) / (4 * S2)]
D4_H1 = [((-1) ** n) * D4_H0[3 - n] for n in range(4)]


def cqf_highpass(h0: Sequence[float]) -> Vector:
    """Smith-Barnwell conjugate quadrature highpass: h1[n] = (-1)^n h0[L - 1 - n]."""
    big_l = len(h0)
    return [((-1) ** n) * h0[big_l - 1 - n] for n in range(big_l)]


def qmf_pair(h0: Sequence[float]) -> Tuple[Vector, Vector, Vector, Vector]:
    """Croisier-Esteban-Galand QMF: H1(z) = H0(-z), F0 = H0, F1 = -H1. Returns (h0, h1, f0, f1)."""
    h1 = [((-1) ** n) * c for n, c in enumerate(h0)]
    return list(h0), h1, list(h0), [-c for c in h1]
