# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/formant-synthesis/. The authors are listed in prov/D7ZPSZ.jsonl.

"""Cascade formant synthesis with the digital resonators of Klatt (1980).

A resonator with center frequency F and bandwidth BW at the sample period T is
    y[n] = A x[n] + B y[n - 1] + C y[n - 2],
    C = -exp(-2 pi BW T),  B = 2 exp(-pi BW T) cos(2 pi F T),  A = 1 - B - C,
so its gain at 0 Hz is A / (1 - B - C) = 1. An antiresonator inverts it:
    y[n] = A' x[n] + B' x[n - 1] + C' x[n - 2],  A' = 1 / A, B' = -B / A, C' = -C / A.

The synthesizer reads one frame of parameters every update period (5 ms in
Klatt's design): F0, the voicing amplitude AV, and the formants (F_k, BW_k).
The source is a train of unit impulses at F0 through a low-pass resonator at
0 Hz. The formant resonators are in cascade, and a first difference models the
radiation at the lips. Filter states carry over from frame to frame.
"""

import cmath
import math
from typing import List, Sequence, Tuple

Coeffs = Tuple[float, float, float]


def resonator_coeffs(f: float, bw: float, fs: float) -> Coeffs:
    """(A, B, C) of the resonator with center f and bandwidth bw in Hz at the sample rate fs."""
    t = 1.0 / fs
    c = -math.exp(-2.0 * math.pi * bw * t)
    b = 2.0 * math.exp(-math.pi * bw * t) * math.cos(2.0 * math.pi * f * t)
    return 1.0 - b - c, b, c


def antiresonator_coeffs(f: float, bw: float, fs: float) -> Coeffs:
    """(A', B', C') of the antiresonator, the inverse of the resonator with the same f and bw."""
    a, b, c = resonator_coeffs(f, bw, fs)
    return 1.0 / a, -b / a, -c / a


class Resonator:
    """y[n] = A x[n] + B y[n - 1] + C y[n - 2]. The coefficients can change between samples; the state stays."""

    def __init__(self) -> None:
        self.y1 = 0.0
        self.y2 = 0.0

    def step(self, x: float, k: Coeffs) -> float:
        y = k[0] * x + k[1] * self.y1 + k[2] * self.y2
        self.y2, self.y1 = self.y1, y
        return y


class Antiresonator:
    """y[n] = A' x[n] + B' x[n - 1] + C' x[n - 2]."""

    def __init__(self) -> None:
        self.x1 = 0.0
        self.x2 = 0.0

    def step(self, x: float, k: Coeffs) -> float:
        y = k[0] * x + k[1] * self.x1 + k[2] * self.x2
        self.x2, self.x1 = self.x1, x
        return y


def filter_signal(x: Sequence[float], k: Coeffs, anti: bool = False) -> List[float]:
    """Run a fixed resonator (or antiresonator) over x from a zero state."""
    r = Antiresonator() if anti else Resonator()
    return [r.step(v, k) for v in x]


def response(k: Coeffs, f: float, fs: float, anti: bool = False) -> complex:
    """The frequency response at f Hz: A / (1 - B z^-1 - C z^-2), or A' + B' z^-1 + C' z^-2, with z = exp(i 2 pi f / fs)."""
    zi = cmath.exp(-2j * math.pi * f / fs)
    if anti:
        return k[0] + k[1] * zi + k[2] * zi * zi
    return k[0] / (1.0 - k[1] * zi - k[2] * zi * zi)


def synthesize(
    frames: Sequence[Tuple[float, float, Sequence[Tuple[float, float]]]],
    fs: float,
    update: float = 0.005,
    glottal_bw: float = 100.0,
) -> List[float]:
    """Cascade synthesis. frames[i] = (F0 in Hz, AV, [(F_1, BW_1), ..., (F_K, BW_K)]); F0 = 0 gives silence.

    Each frame lasts update seconds. Returns the samples.
    """
    per_frame = round(update * fs)
    k_max = max(len(fr[2]) for fr in frames) if frames else 0
    formants = [Resonator() for _ in range(k_max)]
    glottis = Resonator()
    glottal = resonator_coeffs(0.0, glottal_bw, fs)
    last = 0.0  # for the radiation difference
    phase = 1.0  # a pulse at the first voiced sample
    out: List[float] = []
    for f0, av, fmts in frames:  # @line L1
        coeffs = [resonator_coeffs(f, bw, fs) for f, bw in fmts]  # @line L2
        for _ in range(per_frame):
            pulse = 0.0
            if f0 > 0:
                if phase >= 1.0:  # @line L3
                    pulse = av
                    phase -= 1.0
                phase += f0 / fs
            v = glottis.step(pulse, glottal)  # @line L4
            for res, k in zip(formants, coeffs):
                v = res.step(v, k)  # @line L5
            out.append(v - last)  # @line L6
            last = v
    return out
