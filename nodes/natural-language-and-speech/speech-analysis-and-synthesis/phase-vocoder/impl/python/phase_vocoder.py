# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-vocoder/. The authors are listed in prov/M9RGV0.jsonl.

"""The phase vocoder: time stretching by the STFT with phase propagation.

Analysis frames start every Ha samples, synthesis frames every Hs samples, so the
duration changes by the factor Hs / Ha. Each bin keeps its magnitude. Its phase
is advanced by Hs times its instantaneous frequency, estimated from the phase
change between two analysis frames:

    omega_k = 2 pi k / N                                (the bin center)
    delta   = princarg(phi_t[k] - phi_{t-1}[k] - Ha omega_k)
    omega   = omega_k + delta / Ha                      (the instantaneous frequency)
    psi_t[k] = psi_{t-1}[k] + Hs omega                  (the synthesis phase)

where princarg maps an angle to [-pi, pi). The frames are put back by weighted
overlap-add: y = sum_t w(n - t Hs) frame_t(n - t Hs) / sum_t w(n - t Hs)^2.
"""

import cmath
import math
from typing import List, Sequence

from nlsdsp import fft


def princarg(phase: float) -> float:
    """The principal argument: phase + 2 pi m in [-pi, pi) for the integer m that puts it there."""
    return phase - 2.0 * math.pi * math.floor((phase + math.pi) / (2.0 * math.pi))


def periodic_hann(n: int) -> List[float]:
    """w[i] = 0.5 - 0.5 cos(2 pi i / n): the Hann window whose shifts by n / 4 add to a constant."""
    return [0.5 - 0.5 * math.cos(2.0 * math.pi * i / n) for i in range(n)]


def ifft(spec: Sequence[complex]) -> List[complex]:
    """The inverse DFT by the forward FFT of the conjugate."""
    n = len(spec)
    return [v.conjugate() / n for v in fft([s.conjugate() for s in spec])]


def stft(x: Sequence[float], n: int, hop: int, window: Sequence[float]) -> List[List[complex]]:
    """The DFTs of the windowed frames x[t hop .. t hop + n - 1]; the last partial frame is dropped."""
    out = []
    for start in range(0, len(x) - n + 1, hop):
        out.append(fft([x[start + i] * window[i] for i in range(n)]))
    return out


def instantaneous_frequency(prev: complex, cur: complex, k: int, n: int, hop: int) -> float:
    """omega_k + princarg(arg cur - arg prev - hop omega_k) / hop, in radians per sample."""
    omega_k = 2.0 * math.pi * k / n
    delta = princarg(cmath.phase(cur) - cmath.phase(prev) - hop * omega_k)  # @line L4
    return omega_k + delta / hop  # @line L5


def overlap_add(frames: Sequence[Sequence[float]], hop: int, window: Sequence[float]) -> List[float]:
    """Weighted overlap-add: sum of window * frame at t hop, divided by the sum of window^2 where it is not tiny."""
    n = len(window)
    length = (len(frames) - 1) * hop + n if frames else 0
    y = [0.0] * length
    norm = [0.0] * length
    for t, fr in enumerate(frames):
        for i in range(n):
            y[t * hop + i] += window[i] * fr[i]
            norm[t * hop + i] += window[i] ** 2
    return [v / z if z > 1e-8 else 0.0 for v, z in zip(y, norm)]


def time_stretch(x: Sequence[float], ratio: float, n: int = 1024, ha: int = 256) -> List[float]:
    """Stretch the duration of x by about ratio (> 1 is slower) and keep its pitch. n must be a power of 2."""
    hs = round(ha * ratio)
    window = periodic_hann(n)
    spectra = stft(x, n, ha, window)  # @line L1
    if not spectra:
        return []
    psi = [cmath.phase(v) for v in spectra[0]]  # @line L2
    frames = [[v.real for v in ifft(spectra[0])]]
    for t in range(1, len(spectra)):  # @line L3
        prev, cur = spectra[t - 1], spectra[t]
        for k in range(n):
            psi[k] += hs * instantaneous_frequency(prev[k], cur[k], k, n, ha)  # @line L6
        spec = [abs(cur[k]) * cmath.exp(1j * psi[k]) for k in range(n)]  # @line L7
        frames.append([v.real for v in ifft(spec)])
    return overlap_add(frames, hs, window)  # @line L8


def resample_linear(x: Sequence[float], factor: float) -> List[float]:
    """Read x at the positions i * factor by linear interpolation: factor > 1 makes it shorter and higher."""
    out = []
    pos = 0.0
    while pos <= len(x) - 1:
        i = int(pos)
        frac = pos - i
        nxt = x[i + 1] if i + 1 < len(x) else x[i]
        out.append((1 - frac) * x[i] + frac * nxt)
        pos += factor
    return out


def pitch_shift(x: Sequence[float], factor: float, n: int = 1024, ha: int = 256) -> List[float]:
    """Raise the pitch by factor and keep the duration: stretch by factor, then resample by factor."""
    hs = round(ha * factor)
    return resample_linear(time_stretch(x, hs / ha, n, ha), hs / ha)
