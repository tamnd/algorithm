# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/additive-white-gaussian-noise-channel/. The authors are listed in prov/QYZ6QZ.jsonl.
"""The discrete-time additive white Gaussian noise channel y = x + z, z ~ N(0, sigma^2).

Conventions: real symbols, BPSK maps bit b to (1 - 2b) sqrt(Es), the noise variance per
real dimension is sigma^2 = N0 / 2, SNR = P / sigma^2 = 2 Es / N0, and Es = R Eb for a
code of rate R. Integrals use the composite Simpson rule; only the standard library is used.
"""

import math
import random
from typing import Callable, List, Sequence


def db(x: float) -> float:
    return 10.0 * math.log10(x)


def from_db(x_db: float) -> float:
    return 10.0 ** (x_db / 10.0)


def transmit(symbols: Sequence[float], sigma: float, rng: random.Random) -> List[float]:
    """Add independent N(0, sigma^2) noise to each real symbol."""
    return [x + rng.gauss(0.0, sigma) for x in symbols]


def q_function(x: float) -> float:
    """Q(x) = P(N(0, 1) > x) = erfc(x / sqrt 2) / 2."""
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def bpsk_bit_error_rate(ebn0: float) -> float:
    """Uncoded BPSK with a sign detector: Q(sqrt(2 Eb / N0)), for Eb/N0 as a ratio (not dB)."""
    return q_function(math.sqrt(2.0 * ebn0))


def gaussian_capacity(snr: float) -> float:
    """Capacity with a power limit, bits per real channel use: (1/2) log2(1 + SNR)."""
    return 0.5 * math.log2(1.0 + snr)


def shannon_limit_ebn0(rate: float) -> float:
    """Least Eb/N0 (ratio) for reliable rate R on the real AWGN channel: (2^(2R) - 1) / (2R).

    It decreases to ln 2 (about -1.59 dB) as R tends to 0.
    """
    return (2.0 ** (2.0 * rate) - 1.0) / (2.0 * rate)


def _log2_one_plus_exp(t: float) -> float:
    """log2(1 + e^t) without overflow."""
    if t > 0:
        return t / math.log(2.0) + math.log2(1.0 + math.exp(-t))
    return math.log2(1.0 + math.exp(t))


def simpson(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    """Composite Simpson rule with n (even) intervals."""
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3.0


def bi_awgn_capacity(sigma2: float, intervals: int = 2000) -> float:
    """Capacity of the binary-input AWGN channel with inputs +1, -1 and noise variance sigma2.

    By symmetry the uniform input is best and
    C = 1 - E[log2(1 + exp(-2 Y / sigma2))] with Y ~ N(1, sigma2).
    The integral is cut at 14 standard deviations, where the Gaussian density is below 1e-42.
    """
    s = math.sqrt(sigma2)

    def integrand(y: float) -> float:
        density = math.exp(-((y - 1.0) ** 2) / (2.0 * sigma2)) / math.sqrt(2.0 * math.pi * sigma2)
        return density * _log2_one_plus_exp(-2.0 * y / sigma2)

    return 1.0 - simpson(integrand, 1.0 - 14.0 * s, 1.0 + 14.0 * s, intervals)


def hard_decision_capacity(sigma2: float) -> float:
    """Capacity when the receiver keeps only the sign: a BSC with p = Q(1 / sigma)."""
    p = q_function(1.0 / math.sqrt(sigma2))
    if p <= 0.0:
        return 1.0
    return 1.0 + p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p)


def sigma2_for(rate: float, ebn0: float) -> float:
    """Noise variance for unit-energy BPSK symbols: sigma^2 = N0 / (2 Es) = 1 / (2 R Eb/N0)."""
    return 1.0 / (2.0 * rate * ebn0)


def required_ebn0_db(rate: float, capacity: Callable[[float], float]) -> float:
    """Least Eb/N0 in dB at which a binary-input capacity function reaches the rate (bisection)."""
    lo, hi = -10.0, 30.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if capacity(sigma2_for(rate, from_db(mid))) >= rate:
            hi = mid
        else:
            lo = mid
    return hi


def simulate_bpsk(nbits: int, ebn0_db: float, seed: int = 1) -> float:
    """Monte Carlo bit error rate of uncoded BPSK (Es = Eb = 1) with a sign detector."""
    rng = random.Random(seed)
    sigma = math.sqrt(1.0 / (2.0 * from_db(ebn0_db)))
    errors = 0
    for _ in range(nbits):
        b = rng.getrandbits(1)
        y = (1.0 - 2.0 * b) + rng.gauss(0.0, sigma)
        errors += (y < 0) != (b == 1)
    return errors / nbits
