# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delay-locked-loop/. The authors are listed in prov/WXMG9W.jsonl.

"""A noncoherent delay-locked loop that tracks the code delay of a spread-spectrum signal.

Model: time is measured in chips. One block holds one code period of N chips,
sampled M times at t_k = k N / M, with M and N coprime so that the chip
edges fall at many different sample offsets:
    r_k = A e^(j phi) c[floor(t_k - tau) mod N] + w_k,  w_k ~ CN(0, n0).
The early and late replicas are the code delayed by tau_hat - delta and tau_hat + delta.
"""

import cmath
import math
import random
from typing import Iterable

from cbb import cn


def replica(c: list[int], d: float, m: int) -> list[int]:
    """The code delayed by d chips, sampled at t_k = k N / M."""
    n = len(c)
    return [c[math.floor(k * n / m - d) % n] for k in range(m)]


def correlate(r: list[complex], c: list[int], d: float) -> complex:
    """(1/M) sum over k of r_k times the replica delayed by d (the replica is real)."""
    m = len(r)
    rep = replica(c, d, m)
    return sum(rk * v for rk, v in zip(r, rep)) / m


def received_block(
    rng: random.Random, c: list[int], tau: float, m: int, amp: float = 1.0, phase: float = 0.0, n0: float = 0.0
) -> list[complex]:
    """One code period with the code delayed by tau chips, a carrier phase, and CN(0, n0) noise per sample."""
    sig = [amp * cmath.exp(1j * phase) * v for v in replica(c, tau, m)]
    if n0 > 0:
        sig = [v + cn(rng, n0) for v in sig]
    return sig


def discriminator(e: complex, l: complex) -> float:
    """The normalized early minus late envelope (|L| - |E|) / (|L| + |E|)."""
    s = abs(l) + abs(e)
    return 0.0 if s == 0 else (abs(l) - abs(e)) / s


def dll(blocks: Iterable[list[complex]], c: list[int], tau0: float, delta: float, g: float, kd: float) -> list[float]:
    """Run the loop over the blocks. Returns the estimate after each block, starting with tau0."""
    tau_hat = tau0  # @line L1
    history = [tau_hat]
    for r in blocks:  # @line L2
        e, l = correlate(r, c, tau_hat - delta), correlate(r, c, tau_hat + delta)  # @line L3
        d = discriminator(e, l)  # @line L4
        tau_hat = tau_hat + g * d / kd  # @line L5
        history.append(tau_hat)
    return history  # @line L6


def mseq_autocorrelation(x: float, n: int) -> float:
    """The periodic autocorrelation of an m-sequence with rectangular chips at a lag of x chips."""
    x = (x + n / 2) % n - n / 2
    if abs(x) <= 1:
        return 1 - abs(x) * (n + 1) / n
    return -1 / n


def s_curve(eps: float, delta: float, n: int) -> float:
    """The noiseless discriminator output at the error eps = tau - tau_hat, for continuous time."""
    e = mseq_autocorrelation(eps + delta, n)
    l = mseq_autocorrelation(eps - delta, n)
    return discriminator(complex(e), complex(l))


def slope(delta: float, n: int) -> float:
    """k_d: the slope of the S-curve at eps = 0, (N + 1) / (N - (N + 1) delta), for 0 < delta < N / (N + 1)."""
    return (n + 1) / (n - (n + 1) * delta)


def mseq_bits(exps: list[int]) -> list[int]:
    """One period of an m-sequence as chips +1 and -1."""
    n = max(exps)
    s = [1] + [0] * (n - 1)
    taps = [i for i in exps if i < n]
    while len(s) < (1 << n) - 1:
        k = len(s) - n
        bit = 0
        for i in taps:
            bit ^= s[k + i]
        s.append(bit)
    return [1 - 2 * v for v in s]
