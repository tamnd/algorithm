# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-phase-shift-keying/. The authors are listed in prov/3Q2A6K.jsonl.

"""M-ary differential PSK: the differential encoder, the differential detector, and coherent
detection followed by differential decoding, for comparison.

Each group of log2(M) bits is a Gray label u. The phase step is 2 pi m / M, where m is the
index whose Gray code is u, so that neighboring steps differ in one bit. The first transmitted
symbol is the reference 1. All symbols have unit energy.
"""

import cmath
import math


def bits_per_symbol(m: int) -> int:
    k = m.bit_length() - 1
    if m < 2 or 1 << k != m:
        raise ValueError("M must be a power of 2, at least 2")
    return k


def gray(m: int) -> int:
    return m ^ (m >> 1)


def gray_inverse(u: int) -> int:
    m = 0
    while u:
        m ^= u
        u >>= 1
    return m


def _labels(bits: list[int], k: int) -> list[int]:
    if len(bits) % k:
        raise ValueError("the number of bits must be a multiple of log2(M)")
    out = []
    for i in range(0, len(bits), k):
        u = 0
        for b in bits[i : i + k]:
            u = 2 * u + b
        out.append(u)
    return out


def _bits(u: int, k: int) -> list[int]:
    return [(u >> (k - 1 - i)) & 1 for i in range(k)]


def encode(bits: list[int], m: int) -> list[complex]:
    """The symbols s_0 = 1, s_k = s_(k-1) e^(j 2 pi m_k / M); one more symbol than labels."""
    k = bits_per_symbol(m)
    s = [1 + 0j]  # @line L1
    for u in _labels(bits, k):
        step = gray_inverse(u)  # @line L2
        s.append(s[-1] * cmath.exp(2j * math.pi * step / m))  # @line L3
    return s  # @line L4


def detect(r: list[complex], m: int) -> list[int]:
    """Differential detection: the phase of r_k conj(r_(k-1)) to the nearest step."""
    k = bits_per_symbol(m)
    bits = []
    for prev, cur in zip(r, r[1:]):
        z = cur * prev.conjugate()  # @line L5
        step = round(m * cmath.phase(z) / (2 * math.pi)) % m  # @line L6
        bits.extend(_bits(gray(step), k))  # @line L7
    return bits


def detect_coherent(r: list[complex], m: int, theta: float = 0.0) -> list[int]:
    """Coherent detection with the reference phase theta, then differential decoding."""
    k = bits_per_symbol(m)
    rot = cmath.exp(-1j * theta)
    idx = [round(m * cmath.phase(v * rot) / (2 * math.pi)) % m for v in r]
    bits = []
    for a, b in zip(idx, idx[1:]):
        bits.extend(_bits(gray((b - a) % m), k))
    return bits


def rotate(s: list[complex], theta: float, nu: float = 0.0) -> list[complex]:
    """The channel s_k e^(j (theta + 2 pi nu k)): an unknown phase and a frequency offset nu/T."""
    return [v * cmath.exp(1j * (theta + 2 * math.pi * nu * n)) for n, v in enumerate(s)]


def asymptotic_loss_db(m: int) -> float:
    """The high-SNR loss of M-DPSK against coherent M-PSK, 10 log10(sin^2(pi/M) / (2 sin^2(pi/(2M))))."""
    return 10 * math.log10(math.sin(math.pi / m) ** 2 / (2 * math.sin(math.pi / (2 * m)) ** 2))
