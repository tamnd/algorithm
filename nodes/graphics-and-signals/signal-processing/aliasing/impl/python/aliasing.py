# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aliasing/. The authors are listed in prov/2AWSJX.jsonl.

"""Aliasing of sampled sinusoids.

Frequencies are in Hz and the sampling rate fs is in samples per second.
Pass frequencies as int or Fraction to get exact phase reduction: the phase
f n / fs is reduced modulo one cycle before the cosine is taken, so two
frequencies that differ by a multiple of fs give bit-for-bit equal samples.
"""

import cmath
import math
from fractions import Fraction
from typing import Callable

Number = int | Fraction


def _cycles(f: Number, fs: Number, n: int, phase: Number) -> Fraction:
    """Return the phase of sample n in cycles, reduced to [0, 1)."""
    return (Fraction(f) * n / Fraction(fs) + Fraction(phase)) % 1


def sample_cos(f: Number, fs: Number, count: int, phase: Number = 0) -> list[float]:
    """Return cos(2 pi (f n / fs + phase)) for n = 0 .. count - 1; phase is in cycles."""
    return [math.cos(2 * math.pi * float(_cycles(f, fs, n, phase))) for n in range(count)]


def sample_sin(f: Number, fs: Number, count: int, phase: Number = 0) -> list[float]:
    """Return sin(2 pi (f n / fs + phase)) for n = 0 .. count - 1; phase is in cycles."""
    return [math.sin(2 * math.pi * float(_cycles(f, fs, n, phase))) for n in range(count)]


def sample_exp(f: Number, fs: Number, count: int) -> list[complex]:
    """Return exp(2 pi i f n / fs) for n = 0 .. count - 1."""
    return [cmath.exp(2j * math.pi * float(_cycles(f, fs, n, 0))) for n in range(count)]


def alias_frequency(f: Number, fs: Number) -> Fraction:
    """Return the frequency in [-fs/2, fs/2) that a complex tone at f appears at."""
    f, fs = Fraction(f), Fraction(fs)
    if fs <= 0:
        raise ValueError("fs must be positive")
    return (f + fs / 2) % fs - fs / 2


def folded_frequency(f: Number, fs: Number) -> Fraction:
    """Return the frequency in [0, fs/2] that a real tone at f appears at."""
    return abs(alias_frequency(f, fs))


def sampled_spectrum(spectrum: Callable[[float], complex], f: float, fs: float, terms: int) -> complex:
    """Return fs times the sum of spectrum(f - k fs) for |k| <= terms.

    This is the DTFT of the samples x(n / fs) at omega = 2 pi f / fs, the sum of
    the shifted copies of the spectrum of x (the Poisson summation formula).
    """
    return fs * sum(spectrum(f - k * fs) for k in range(-terms, terms + 1))
