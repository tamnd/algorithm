# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/serial-search-code-acquisition/. The authors are listed in prov/3AJ158.jsonl.

"""Serial search for the code phase of a direct-sequence signal.

Model of one dwell: a fresh block of N chips
    r[n] = sqrt(Es) c[(n - tau) mod N] + w[n],  w[n] ~ CN(0, N0),
with sum |c[n]|^2 = 1. The dwell at the cell k computes
    z = sum over n of conj(c[(n - k) mod N]) r[n]
and compares |z|^2 with a threshold gamma. A crossing is checked by a
verification that costs K dwells when it is a false alarm. The cells are
visited in the order start, start + 1, ... modulo q.
"""

import math
import random
from typing import Callable

from cbb import cn


def correlate(r: list[complex], c: list[complex], k: int) -> complex:
    """z = sum over n of conj(c[(n - k) mod N]) r[n]: the correlator output at the code phase k."""
    n = len(c)
    return sum(c[(i - k) % n].conjugate() * r[i] for i in range(n))


def received_block(rng: random.Random, c: list[complex], tau: int, es: float, n0: float) -> list[complex]:
    """One block of N chips with the code at phase tau and CN(0, N0) noise per chip."""
    n = len(c)
    a = math.sqrt(es)
    if n0 == 0:
        return [a * c[(i - tau) % n] for i in range(n)]
    return [a * c[(i - tau) % n] + cn(rng, n0) for i in range(n)]


def serial_search(
    dwell: Callable[[int], complex],
    q: int,
    gamma: float,
    verify: Callable[[int], bool],
    k_penalty: int,
    start: int = 0,
    max_dwells: int = 10**7,
) -> tuple[int | None, int]:
    """Search the cells start, start + 1, ... (mod q) until a crossing passes verification.

    dwell(k) returns the correlator output for a fresh block at cell k.
    Returns (cell, time), where time counts dwells, plus k_penalty dwells for
    each crossing that fails verification. Returns (None, time) if the
    time reaches max_dwells first.
    """
    k = start % q  # @line L1
    time = 0
    while time < max_dwells:  # @line L2
        z = dwell(k)  # @line L3
        time += 1
        if abs(z) ** 2 > gamma:  # @line L4
            if verify(k):  # @line L5
                return k, time
            time += k_penalty
        k = (k + 1) % q  # @line L6
    return None, time


def marcum_q1(a: float, b: float, tol: float = 1e-16) -> float:
    """Q1(a, b) = P(|X| > b) for X complex Gaussian with |E X| = a and variance 1 per real part.

    Series: Q1(a, b) = sum over j >= 0 of Poisson(j; a^2/2) * P(Gamma(j + 1) > b^2/2), with
    P(Gamma(m) > x) = e^(-x) sum over i < m of x^i / i!.
    """
    lam = a * a / 2.0
    x = b * b / 2.0
    pois = math.exp(-lam)
    term = math.exp(-x)
    tail = term
    total = pois * tail
    j = 0
    while True:
        j += 1
        pois *= lam / j
        term *= x / j
        tail += term
        total += pois * min(tail, 1.0)
        if j > lam and pois < tol:
            break
    return min(total, 1.0)


def dwell_probabilities(es: float, n0: float, n: int, gamma: float, off_peak: float | None = None) -> tuple[float, float]:
    """(Pd, Pfa) for one dwell with threshold gamma on |z|^2.

    Under H1, z ~ CN(sqrt(Es), N0). Under H0, z ~ CN(sqrt(Es) R, N0), where R is the
    off-peak periodic autocorrelation of the code (-1/N for an m-sequence by default).
    With z ~ CN(mu, N0), P(|z|^2 > gamma) = Q1(sqrt(2 |mu|^2 / N0), sqrt(2 gamma / N0)).
    """
    if off_peak is None:
        off_peak = -1.0 / n
    b = math.sqrt(2.0 * gamma / n0)
    pd = marcum_q1(math.sqrt(2.0 * es / n0), b)
    pfa = marcum_q1(math.sqrt(2.0 * es * off_peak * off_peak / n0), b)
    return pd, pfa


def mean_acquisition_time(q: int, pd: float, pfa: float, k_penalty: int, tau_d: float = 1.0) -> float:
    """E[T] = (2 + (2 - Pd)(q - 1)(1 + K Pfa)) / (2 Pd) * tau_d, for a uniformly random true cell."""
    return (2.0 + (2.0 - pd) * (q - 1) * (1.0 + k_penalty * pfa)) / (2.0 * pd) * tau_d


def mseq_code(exps: list[int]) -> list[complex]:
    """One period of an m-sequence as unit-energy chips: bit 0 -> +1/sqrt(N), bit 1 -> -1/sqrt(N)."""
    n = max(exps)
    s = [1] + [0] * (n - 1)
    taps = [i for i in exps if i < n]
    while len(s) < (1 << n) - 1:
        k = len(s) - n
        bit = 0
        for i in taps:
            bit ^= s[k + i]
        s.append(bit)
    scale = 1.0 / math.sqrt(len(s))
    return [complex((1 - 2 * v) * scale) for v in s]
