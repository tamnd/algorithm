# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mel-frequency-cepstral-coefficients/. The authors are listed in prov/85RNE7.jsonl.

"""Mel-frequency cepstral coefficients (MFCC) of a speech signal.

The steps, with the defaults of the page (HTK values where HTK has one):
pre-emphasis with alpha = 0.97 over the whole signal, frames of 400 samples with a
hop of 160 and no padding, the symmetric Hamming window, the power spectrum with
an FFT of 512 points, 26 triangular filters equally spaced on the mel scale
m = 2595 log_10(1 + f / 700) from 0 Hz to fs / 2, the natural log with a floor of
1e-10, the orthonormal DCT-II, coefficients c_0 to c_12, and the sine lifter with
L = 22.

The framing, the window, the FFT and the DCT come from the shared helper nlsdsp.
"""

import math
from typing import List, Optional, Sequence

from nlsdsp import dct2, frames, hamming, power_spectrum


def hz_to_mel(f: float) -> float:
    return 2595.0 * math.log10(1.0 + f / 700.0)


def mel_to_hz(m: float) -> float:
    return 700.0 * (10.0 ** (m / 2595.0) - 1.0)


def pre_emphasis(x: Sequence[float], alpha: float = 0.97) -> List[float]:
    """y[0] = x[0] and y[n] = x[n] - alpha x[n - 1] for n >= 1."""
    return [x[0]] + [x[n] - alpha * x[n - 1] for n in range(1, len(x))] if x else []


def mel_weights(num_filters: int, nfft: int, fs: float, fmin: float = 0.0, fmax: Optional[float] = None):
    """Triangular weights W[m][k], linear in Hz, with edges equally spaced in mel."""
    if fmax is None:
        fmax = fs / 2.0
    if num_filters < 1 or not 0.0 <= fmin < fmax <= fs / 2.0:
        raise ValueError("need num_filters >= 1 and 0 <= fmin < fmax <= fs / 2")
    lo, hi = hz_to_mel(fmin), hz_to_mel(fmax)
    step = (hi - lo) / (num_filters + 1)
    edges = [mel_to_hz(lo + i * step) for i in range(num_filters + 2)]
    weights = []
    for m in range(1, num_filters + 1):
        left, center, right = edges[m - 1], edges[m], edges[m + 1]
        row = []
        for k in range(nfft // 2 + 1):
            f = k * fs / nfft
            if left < f <= center:
                row.append((f - left) / (center - left))
            elif center < f < right:
                row.append((right - f) / (right - center))
            else:
                row.append(0.0)
        weights.append(row)
    return weights


def lifter(c: Sequence[float], q: int) -> List[float]:
    """The sine lifter c'_n = (1 + (q / 2) sin(pi n / q)) c_n. q = 0 leaves c unchanged."""
    if q <= 0:
        return list(c)
    return [(1.0 + 0.5 * q * math.sin(math.pi * n / q)) * v for n, v in enumerate(c)]


def mfcc_of_frame(
    frame: Sequence[float],
    weights: Sequence[Sequence[float]],
    window: Sequence[float],
    nfft: int = 512,
    num_ceps: int = 13,
    cep_lifter: int = 22,
    floor: float = 1e-10,
) -> List[float]:
    """The MFCC vector c_0 to c_{num_ceps - 1} of one frame (already pre-emphasized)."""
    u = [s * w for s, w in zip(frame, window)]  # @line L4
    p = power_spectrum(u, nfft)  # @line L5
    e = [sum(w * v for w, v in zip(row, p)) for row in weights]  # @line L6
    log_e = [math.log(max(v, floor)) for v in e]  # @line L7
    c = dct2(log_e, num_ceps)  # @line L8
    return lifter(c, cep_lifter)  # @line L9


def mfcc(
    x: Sequence[float],
    fs: float = 16000.0,
    num_filters: int = 26,
    num_ceps: int = 13,
    frame_len: int = 400,
    hop: int = 160,
    nfft: int = 512,
    alpha: float = 0.97,
    cep_lifter: int = 22,
    fmin: float = 0.0,
    fmax: Optional[float] = None,
    floor: float = 1e-10,
) -> List[List[float]]:
    """One row of num_ceps coefficients per frame. A signal of L >= frame_len samples
    gives 1 + (L - frame_len) // hop rows; a shorter signal gives none."""
    if num_ceps > num_filters:
        raise ValueError("num_ceps must be at most num_filters")
    y = pre_emphasis(x, alpha)  # @line L1
    weights = mel_weights(num_filters, nfft, fs, fmin, fmax)  # @line L2
    window = hamming(frame_len)
    return [
        mfcc_of_frame(fr, weights, window, nfft, num_ceps, cep_lifter, floor)
        for fr in frames(y, frame_len, hop)  # @line L3
    ]
