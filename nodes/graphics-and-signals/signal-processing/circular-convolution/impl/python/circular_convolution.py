# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-convolution/. The authors are listed in prov/KFMA92.jsonl.

"""Circular (cyclic) convolution of length L, by the definition and by the DFT."""

import cmath
from typing import Sequence


def pad(x: Sequence, length: int) -> list:
    """Extend x with zeros to the given length. x must not be longer."""
    if len(x) > length:
        raise ValueError("the sequence is longer than the period")
    return list(x) + [0] * (length - len(x))


def circular_convolve(x: Sequence, h: Sequence, length: int) -> list:
    """y[n] = sum_{k=0}^{L-1} x[k] h[(n - k) mod L], for x and h padded with zeros to L.

    Exact for int and Fraction inputs. Costs L^2 multiplications.
    """
    xp, hp = pad(x, length), pad(h, length)
    return [sum(xp[k] * hp[(n - k) % length] for k in range(length)) for n in range(length)]


def time_alias(y: Sequence, length: int) -> list:
    """Fold a finite sequence onto one period: out[n] = sum over r of y[n + r L]."""
    out = [0] * length
    for i, v in enumerate(y):
        out[i % length] += v
    return out


def dft(x: Sequence) -> list[complex]:
    """Direct DFT, X[k] = sum_n x[n] e^(-2 pi i k n / L). O(L^2)."""
    n = len(x)
    return [sum(x[t] * cmath.exp(-2j * cmath.pi * k * t / n) for t in range(n)) for k in range(n)]


def idft(spectrum: Sequence[complex]) -> list[complex]:
    n = len(spectrum)
    return [sum(spectrum[k] * cmath.exp(2j * cmath.pi * k * t / n) for k in range(n)) / n for t in range(n)]


def circular_convolve_dft(x: Sequence, h: Sequence, length: int) -> list[complex]:
    """The same result through the DFT: IDFT(DFT(x) . DFT(h)). Floating point."""
    xs, hs = dft(pad(x, length)), dft(pad(h, length))
    return idft([a * b for a, b in zip(xs, hs)])
