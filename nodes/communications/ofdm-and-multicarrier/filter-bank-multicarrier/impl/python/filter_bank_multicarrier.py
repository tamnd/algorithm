# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filter-bank-multicarrier/. The authors are listed in prov/E8S9AK.jsonl.

"""FBMC with offset QAM (OFDM/OQAM), written as a direct synthesis and analysis.

Each complex QAM symbol c[i][k] becomes two real symbols, a[2i][k] = Re c and
a[2i+1][k] = Im c, sent half a symbol period apart. The real symbol a[m][k]
rides on the pulse

    g_{k,m}[n] = g[n - m M/2] e^(j 2 pi k (n - D/2) / M) j^(k+m),

where g is a real symmetric prototype filter of length D + 1 and unit energy.
The pulses are orthogonal in the real sense: Re <g_{k,m}, g_{k',m'}> = 1 if
(k, m) = (k', m') and 0 otherwise, exactly for the half-sine prototype with
length M and nearly for the PHYDYAS prototype with overlap K = 4. The
receiver takes the real part of the correlation with each pulse. The code
is a direct O(M^2 S) form for checking; real systems use an FFT and a
polyphase network.
"""

import cmath
import math
from typing import Sequence

PHYDYAS_K4 = [1.0, 0.97195983, math.sqrt(2) / 2, 0.23514695]


def half_sine(m: int) -> list[float]:
    """The half-sine prototype of length M with unit energy (overlap factor 1)."""
    return [math.sqrt(2.0 / m) * math.sin(math.pi * (n + 0.5) / m) for n in range(m)]


def phydyas(m: int) -> list[float]:
    """The PHYDYAS prototype with overlap K = 4, length 4M - 1, scaled to unit energy."""
    k = 4
    h = PHYDYAS_K4
    g = [h[0] + 2 * sum((-1) ** i * h[i] * math.cos(2 * math.pi * i * (n + 1) / (k * m)) for i in range(1, k)) for n in range(k * m - 1)]
    e = math.sqrt(sum(v * v for v in g))
    return [v / e for v in g]


def pulse(k: int, m: int, g: Sequence[float], M: int, length: int) -> list[complex]:
    """The pulse g_{k,m} as a vector of the given length."""
    d = len(g) - 1
    out = [0j] * length
    ph = 1j ** ((k + m) % 4)
    for i, v in enumerate(g):
        n = i + m * M // 2
        out[n] = v * cmath.exp(2j * math.pi * k * (n - d / 2) / M) * ph
    return out


def signal_length(slots: int, g: Sequence[float], M: int) -> int:
    """The number of samples for the given number of real symbol slots."""
    return (slots - 1) * (M // 2) + len(g)


def oqam_stagger(c: Sequence[Sequence[complex]]) -> list[list[float]]:
    """QAM symbols c[i][k] to real symbols a[2i][k] = Re c[i][k] and a[2i+1][k] = Im c[i][k]."""
    a = []
    for row in c:  # @line L1
        a.append([v.real for v in row])
        a.append([v.imag for v in row])
    return a


def oqam_destagger(a: Sequence[Sequence[float]]) -> list[list[complex]]:
    """The inverse of oqam_stagger."""
    return [[complex(u, v) for u, v in zip(a[2 * i], a[2 * i + 1])] for i in range(len(a) // 2)]  # @line L4


def synthesize(a: Sequence[Sequence[float]], g: Sequence[float], M: int) -> list[complex]:
    """The transmitted samples: the sum of a[m][k] times g_{k,m}."""
    length = signal_length(len(a), g, M)
    s = [0j] * length
    for m, row in enumerate(a):
        for k, v in enumerate(row):
            if v:
                p = pulse(k, m, g, M, length)
                for n in range(m * M // 2, m * M // 2 + len(g)):
                    s[n] += v * p[n]  # @line L2
    return s


def analyze(s: Sequence[complex], slots: int, g: Sequence[float], M: int) -> list[list[float]]:
    """The real symbols Re <s, g_{k,m}> for every slot m and subcarrier k."""
    a = []
    for m in range(slots):
        row = []
        for k in range(M):
            p = pulse(k, m, g, M, len(s))
            row.append(sum(s[n] * p[n].conjugate() for n in range(m * M // 2, m * M // 2 + len(g))).real)  # @line L3
        a.append(row)
    return a
