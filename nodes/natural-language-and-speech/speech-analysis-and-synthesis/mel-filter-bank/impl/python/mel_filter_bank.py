# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mel-filter-bank/. The authors are listed in prov/3Y1ZJS.jsonl.

"""A bank of triangular filters spaced evenly on the mel scale, and the log mel spectrogram.

The mel scale is m = 2595 log_10(1 + f / 700) (O'Shaughnessy 1987, the HTK form).
The triangles are linear in Hz between their edge frequencies, and the filters
apply to the power spectrum |X[k]|^2, k = 0 to nfft / 2. The log is the natural log,
with a floor before the log.
"""

import math
from typing import List, Optional, Sequence

from nlsdsp import frames, hamming, power_spectrum


def hz_to_mel(f: float) -> float:
    """The mel value of f Hz: 2595 log_10(1 + f / 700)."""
    return 2595.0 * math.log10(1.0 + f / 700.0)


def mel_to_hz(m: float) -> float:
    """The inverse of hz_to_mel: 700 (10^(m / 2595) - 1)."""
    return 700.0 * (10.0 ** (m / 2595.0) - 1.0)


def edge_frequencies(num_filters: int, fmin: float, fmax: float) -> List[float]:
    """The num_filters + 2 frequencies f_0 < f_1 < ... < f_{M+1}, equally spaced in mel from fmin to fmax."""
    lo, hi = hz_to_mel(fmin), hz_to_mel(fmax)  # @line L2
    step = (hi - lo) / (num_filters + 1)
    return [mel_to_hz(lo + i * step) for i in range(num_filters + 2)]  # @line L3


def mel_filter_bank(
    num_filters: int, nfft: int, fs: float, fmin: float = 0.0, fmax: Optional[float] = None
) -> List[List[float]]:
    """The weights W[m][k] of filter m (0 based) on FFT bin k = 0 to nfft / 2.

    Filter m rises linearly from 0 at f_m to 1 at f_{m+1} and falls to 0 at f_{m+2}
    (0 based edges), so each filter starts at the center of the one before it.
    """
    if fmax is None:
        fmax = fs / 2.0
    if num_filters < 1 or not 0.0 <= fmin < fmax <= fs / 2.0:  # @line L1
        raise ValueError("need num_filters >= 1 and 0 <= fmin < fmax <= fs / 2")
    edges = edge_frequencies(num_filters, fmin, fmax)
    nbins = nfft // 2 + 1
    weights = []
    for m in range(1, num_filters + 1):  # @line L4
        left, center, right = edges[m - 1], edges[m], edges[m + 1]
        row = []
        for k in range(nbins):  # @line L5
            f = k * fs / nfft
            if left < f <= center:  # @line L6
                row.append((f - left) / (center - left))
            elif center < f < right:  # @line L7
                row.append((right - f) / (right - center))
            else:
                row.append(0.0)  # @line L8
        weights.append(row)
    return weights


def apply_filter_bank(weights: Sequence[Sequence[float]], spectrum: Sequence[float]) -> List[float]:
    """The band energies e_m = sum_k W[m][k] P[k] of one power spectrum P."""
    return [sum(w * p for w, p in zip(row, spectrum)) for row in weights]  # @line L9


def log_energies(energies: Sequence[float], floor: float = 1e-10) -> List[float]:
    """ln max(e_m, floor) for each band energy."""
    return [math.log(max(e, floor)) for e in energies]  # @line L10


def log_mel_spectrogram(
    x: Sequence[float],
    fs: float = 16000.0,
    num_filters: int = 40,
    frame_len: int = 400,
    hop: int = 160,
    nfft: int = 512,
    fmin: float = 0.0,
    fmax: Optional[float] = None,
    floor: float = 1e-10,
) -> List[List[float]]:
    """Frames without padding, the symmetric Hamming window, the power spectrum,
    the mel filter bank and the log. One row of num_filters values per frame."""
    weights = mel_filter_bank(num_filters, nfft, fs, fmin, fmax)
    win = hamming(frame_len)
    out = []
    for fr in frames(x, frame_len, hop):
        spec = power_spectrum([s * w for s, w in zip(fr, win)], nfft)
        out.append(log_energies(apply_filter_bank(weights, spec), floor))
    return out
