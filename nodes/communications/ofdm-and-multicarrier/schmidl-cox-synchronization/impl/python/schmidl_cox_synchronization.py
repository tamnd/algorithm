# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schmidl-cox-synchronization/. The authors are listed in prov/HGVMCQ.jsonl.

"""Schmidl-Cox timing and frequency synchronization for OFDM.

The first training symbol carries symbols only on the even subcarriers, so its
N time samples are two equal halves of length L = N / 2. A carrier frequency
offset epsilon (in subcarrier spacings) multiplies sample n by
e^(j 2 pi epsilon n / N), so the second half is the first half times
e^(j pi epsilon). The timing metric M(d) = |P(d)|^2 / R(d)^2 finds the symbol,
and the angle of P gives the fractional offset in (-1, 1]. A second training
symbol, with a known differential code v on the even subcarriers, gives the
even integer part 2g.

The DFT pair is the unitary one, as on the OFDM page.
"""

import cmath
import math
import random

import cbb


def training_symbols(n: int, rng: random.Random) -> tuple[list[complex], list[complex], list[complex]]:
    """The two training symbols (subcarrier values) and the code v on the even subcarriers.

    The first symbol has sqrt(2) times a random 4-QAM value on each even
    subcarrier and zero on the odd ones; the second has a random 4-QAM value on
    every subcarrier. v[k] = X2[k] / X1[k] for even k (zero for odd k).
    """
    if n % 2:
        raise ValueError("N must be even")
    s = 1 / math.sqrt(2)

    def q() -> complex:
        return complex(rng.choice((s, -s)), rng.choice((s, -s)))

    x1 = [math.sqrt(2) * q() if k % 2 == 0 else 0j for k in range(n)]
    x2 = [q() for _ in range(n)]
    v = [x2[k] / x1[k] if k % 2 == 0 else 0j for k in range(n)]
    return x1, x2, v


def timing_metric(r: list[complex], half: int) -> tuple[list[complex], list[float], list[float]]:
    """P(d), R(d) and M(d) = |P(d)|^2 / R(d)^2 for d = 0, ..., len(r) - 2 half.

    P and R are updated in O(1) per step from the previous value.
    """
    count = len(r) - 2 * half + 1
    if count < 1:
        raise ValueError("need at least N samples")
    p = sum(r[m].conjugate() * r[m + half] for m in range(half))
    e = sum(abs(r[m + half]) ** 2 for m in range(half))
    ps, rs, ms = [], [], []
    for d in range(count):  # @line L1
        if d > 0:
            p += r[d - 1 + half].conjugate() * r[d - 1 + 2 * half] - r[d - 1].conjugate() * r[d - 1 + half]  # @line L2
            e += abs(r[d - 1 + 2 * half]) ** 2 - abs(r[d - 1 + half]) ** 2  # @line L3
        ps.append(p)
        rs.append(e)
        ms.append(abs(p) ** 2 / (e * e) if e > 0 else 0.0)  # @line L4
    return ps, rs, ms


def timing_estimate(ms: list[float], method: str = "max") -> int:
    """The index of the largest M(d), or the middle of the 90 percent plateau around it."""
    dmax = max(range(len(ms)), key=ms.__getitem__)  # @line L5
    if method == "max":
        return dmax
    if method != "plateau":
        raise ValueError("method is max or plateau")
    level = 0.9 * ms[dmax]
    lo = dmax
    while lo > 0 and ms[lo - 1] >= level:
        lo -= 1
    hi = dmax
    while hi < len(ms) - 1 and ms[hi + 1] >= level:
        hi += 1
    return (lo + hi) // 2


def fractional_offset(p: complex) -> float:
    """epsilon_f = angle(P) / pi, in (-1, 1]."""
    return cmath.phase(p) / math.pi  # @line L6


def integer_offset(y1: list[complex], y2: list[complex], v: list[complex], gmax: int) -> int:
    """The g in [-gmax, gmax] that maximizes |sum over even k of conj(Y1[k+2g] v[k]) Y2[k+2g]|^2."""
    n = len(y1)
    norm = sum(abs(y2[k]) ** 2 for k in range(0, n, 2))
    best, best_g = -1.0, 0
    for g in range(-gmax, gmax + 1):  # @line L9
        acc = sum((y1[(k + 2 * g) % n] * v[k]).conjugate() * y2[(k + 2 * g) % n] for k in range(0, n, 2))
        b = abs(acc) ** 2 / (2 * norm * norm) if norm > 0 else 0.0
        if b > best:
            best, best_g = b, g
    return best_g


def synchronize(r: list[complex], n: int, ncp: int, v: list[complex], method: str = "max", gmax: int | None = None) -> tuple[int, float]:
    """Estimate the timing d and the offset epsilon from a stream that holds the two training symbols.

    The first training symbol is followed directly by the second, each with a
    prefix of ncp samples. The returned d is an FFT start in the first symbol.
    """
    half = n // 2
    if gmax is None:
        gmax = n // 4
    ps, _, ms = timing_metric(r[: len(r) - n - ncp], half)
    d = timing_estimate(ms, method)
    eps_f = fractional_offset(ps[d])
    z = [r[i] * cmath.exp(-2j * math.pi * eps_f * i / n) for i in range(len(r))]  # @line L7
    y1 = cbb.udft(z[d:d + n])  # @line L8
    y2 = cbb.udft(z[d + n + ncp:d + 2 * n + ncp])
    g = integer_offset(y1, y2, v, gmax)
    return d, eps_f + 2 * g  # @line L10


def apply_cfo(r: list[complex], eps: float, n: int) -> list[complex]:
    """Multiply sample i by e^(j 2 pi eps i / N): a carrier offset of eps subcarrier spacings."""
    return [x * cmath.exp(2j * math.pi * eps * i / n) for i, x in enumerate(r)]
