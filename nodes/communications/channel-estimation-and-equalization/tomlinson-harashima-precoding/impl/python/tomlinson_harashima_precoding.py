# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tomlinson-harashima-precoding/. The authors are listed in prov/T1E2A7.jsonl.

"""Tomlinson-Harashima precoding for M-PAM and square M^2-QAM.

The symbols use the raw amplitudes M-1-2m, m = 0..M-1 (the odd integers
-(M-1), ..., M-1 for even M), on each real dimension. The modulo maps each real
dimension into [-M, M), an interval of length 2M that holds M points at spacing 2.

The channel h is known at the transmitter. The precoder works with the monic
channel h / h[0]; the receiver divides by h[0]. With the precoder
x[k] = mod(a[k] - sum_{j>=1} (h[j]/h[0]) x[k-j]), the noiseless received sample
divided by h[0] is a[k] plus a multiple of 2M on each dimension, so the receiver
needs only a modulo and a slicer: no feedback filter and no decisions in a loop.
"""

import math


def pam(m: int) -> list[int]:
    """The raw M-PAM amplitudes M-1-2i for i = 0..M-1."""
    if m < 2:
        raise ValueError("need M >= 2")
    return [m - 1 - 2 * i for i in range(m)]


def mod_real(v: float, m: int) -> float:
    """v reduced into [-M, M) by adding a multiple of 2M."""
    return v - 2 * m * math.floor((v + m) / (2 * m))


def mod(v: complex, m: int) -> complex:
    """The modulo on each real dimension of a complex number."""
    return complex(mod_real(v.real, m), mod_real(v.imag, m))


def slice_real(v: float, m: int) -> int:
    """The M-PAM point nearest to v on the circle of length 2M."""
    idx = round((m - 1 - mod_real(v, m)) / 2) % m
    return m - 1 - 2 * idx


def thp_encode(a: list[complex], h: list[complex], m: int) -> list[complex]:
    """The precoded sequence x for the symbols a and the channel h, h[0] != 0."""
    if not h or h[0] == 0:
        raise ValueError("need h[0] != 0")
    g = [complex(v) / h[0] for v in h]  # @line L1
    x: list[complex] = []
    for k, ak in enumerate(a):  # @line L2
        fb = sum(g[j] * x[k - j] for j in range(1, len(g)) if k - j >= 0)  # @line L3
        x.append(mod(complex(ak) - fb, m))  # @line L4
    return x  # @line L5


def thp_receive(y: list[complex], h0: complex, m: int, real: bool = False) -> list[complex]:
    """The decisions: divide by h[0], reduce modulo 2M on each dimension and slice."""
    out = []
    for v in y:  # @line L6
        u = complex(v) / h0  # @line L7
        re = slice_real(u.real, m)  # @line L8
        out.append(complex(re, 0) if real else complex(re, slice_real(u.imag, m)))
    return out  # @line L9


def channel(x: list[complex], h: list[complex]) -> list[complex]:
    """The noiseless channel output sum_l h[l] x[k-l] for k = 0..len(x)-1."""
    return [sum(h[l] * x[k - l] for l in range(len(h)) if k - l >= 0) for k in range(len(x))]


def power_loss(m: int) -> float:
    """M^2 / (M^2 - 1): the uniform power M^2/3 over the PAM power (M^2-1)/3."""
    return m * m / (m * m - 1)


def ser_per_dimension(m: int, sigma: float, wraps: int = 4) -> float:
    """The exact symbol error rate of one real dimension after the modulo.

    The noise is real Gaussian with standard deviation sigma. A decision is right
    when the noise lands in one of the intervals [2Mi - 1, 2Mi + 1), i an integer.
    """
    ok = 0.0
    for i in range(-wraps, wraps + 1):
        lo, hi = (2 * m * i - 1) / sigma, (2 * m * i + 1) / sigma
        ok += 0.5 * (math.erf(hi / math.sqrt(2)) - math.erf(lo / math.sqrt(2)))
    return 1.0 - ok
