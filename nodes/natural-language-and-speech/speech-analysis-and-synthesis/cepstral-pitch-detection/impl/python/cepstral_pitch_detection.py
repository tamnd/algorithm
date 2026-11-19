# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cepstral-pitch-detection/. The authors are listed in prov/AZJ97D.jsonl.

"""Cepstral pitch detection (Noll 1967) on one frame and on a whole signal.

The real cepstrum of a frame x of N samples, with the DFT length M >= N, is

    c[q] = (1 / M) sum_{k=0}^{M-1} ln |X[k]| exp(2 pi i k q / M),   q = 0 .. M - 1,

where X is the DFT of the windowed frame, zero padded to M. The index q is the
quefrency in samples. For voiced speech, the excitation adds a peak at the pitch
period P, and the vocal tract fills only the low quefrencies. The detector
returns fs / q* for the largest peak q* in [ceil(fs / fmax), floor(fs / fmin)].

Noll used the power spectrum of ln |X|^2, which is the square of 2 c[q] here,
so it has its largest peak at the same quefrency when that peak is positive.
"""

import math
from typing import List, Optional, Sequence, Tuple

from nlsdsp import fft, frames, hamming


def _log_magnitude(spec: Sequence[complex]) -> List[float]:
    """ln |X[k]| with a floor of 1e-12 times the largest magnitude, so that ln 0 never occurs."""
    mags = [abs(v) for v in spec]
    top = max(mags)
    if top == 0.0:
        raise ValueError("the frame is all zeros")
    floor = 1e-12 * top
    return [math.log(max(m, floor)) for m in mags]


def real_cepstrum(frame: Sequence[float], nfft: int, window: bool = True) -> List[float]:
    """The real cepstrum c[0 .. nfft - 1] of the frame, by two FFTs."""
    n = len(frame)
    if n > nfft:
        raise ValueError("the frame is longer than the FFT length")
    w = hamming(n) if window else [1.0] * n
    y = [w[i] * frame[i] for i in range(n)] + [0.0] * (nfft - n)  # @line L1
    spec = fft(y)  # @line L2
    logmag = _log_magnitude(spec)  # @line L3
    # ln |X| is real and even in k, so the inverse DFT equals the forward DFT divided by nfft
    return [v.real / nfft for v in fft(logmag)]  # @line L4


def real_cepstrum_direct(frame: Sequence[float], nfft: int, window: bool = True) -> List[float]:
    """The same cepstrum from the definition with O(nfft^2) cosine sums. For tests only."""
    n = len(frame)
    w = hamming(n) if window else [1.0] * n
    y = [w[i] * frame[i] for i in range(n)] + [0.0] * (nfft - n)
    spec = []
    for k in range(nfft):
        re = sum(y[t] * math.cos(2 * math.pi * k * t / nfft) for t in range(nfft))
        im = -sum(y[t] * math.sin(2 * math.pi * k * t / nfft) for t in range(nfft))
        spec.append(complex(re, im))
    logmag = _log_magnitude(spec)
    return [sum(logmag[k] * math.cos(2 * math.pi * k * q / nfft) for k in range(nfft)) / nfft for q in range(nfft)]


def quefrency_range(fs: float, fmin: float, fmax: float) -> Tuple[int, int]:
    """The integer quefrencies (in samples) of the pitch periods between fmin and fmax Hz."""
    if not 0 < fmin < fmax:
        raise ValueError("need 0 < fmin < fmax")
    return math.ceil(fs / fmax), math.floor(fs / fmin)


def cepstral_pitch(
    frame: Sequence[float],
    fs: float,
    fmin: float = 50.0,
    fmax: float = 500.0,
    nfft: Optional[int] = None,
    threshold: float = 0.0,
    window: bool = True,
) -> Tuple[Optional[float], int, float]:
    """Return (f0 in Hz or None for unvoiced, the peak quefrency q*, the peak value c[q*]).

    nfft defaults to the smallest power of 2 that is at least the frame length.
    The frame should hold at least two periods of fmin, and floor(fs / fmin) must
    be below nfft / 2. The threshold on c[q*] is a heuristic voicing decision.
    """
    if nfft is None:
        nfft = 1
        while nfft < len(frame):
            nfft *= 2
    c = real_cepstrum(frame, nfft, window)
    qmin, qmax = quefrency_range(fs, fmin, fmax)  # @line L5
    if qmin < 1 or qmax >= nfft // 2:
        raise ValueError("the quefrency range does not fit in half the FFT length")
    best = qmin
    for q in range(qmin, qmax + 1):  # @line L6
        if c[q] > c[best]:
            best = q
    if c[best] <= threshold:  # @line L7
        return None, best, c[best]
    return fs / best, best, c[best]  # @line L8


def track(
    x: Sequence[float],
    fs: float,
    frame_len: int,
    hop: int,
    fmin: float = 50.0,
    fmax: float = 500.0,
    threshold: float = 0.0,
) -> List[Optional[float]]:
    """Run the detector on each frame of x; None marks a frame judged unvoiced."""
    return [cepstral_pitch(f, fs, fmin, fmax, None, threshold)[0] for f in frames(x, frame_len, hop)]


def all_pole_cepstrum(a: Sequence[float], count: int) -> List[float]:
    """The complex cepstrum h^[0 .. count - 1] of 1 / A(z), A(z) = 1 - sum a_k z^-k, minimum phase.

    h^[0] = 0 and h^[n] = a_n + sum_{k=1}^{n-1} (k / n) h^[k] a_{n-k}, with a_n = 0 for n > p.
    It equals sum_i p_i^n / n over the poles p_i. The real cepstrum is h^[n] / 2 for n >= 1.
    """
    p = len(a)
    h = [0.0] * count
    for n in range(1, count):
        acc = a[n - 1] if n <= p else 0.0
        for k in range(max(1, n - p), n):
            acc += (k / n) * h[k] * a[n - k - 1]
        h[n] = acc
    return h
