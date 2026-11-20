# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rake-receiver/. The authors are listed in prov/MRC17X.jsonl.

"""A rake receiver for one direct-sequence symbol on a known multipath channel.

Model (one symbol, with a cyclic prefix so that the delays are cyclic):
    r[n] = sqrt(Es) b sum over l of h[l] c[(n - d[l]) mod N] + w[n],  n = 0, ..., N - 1,
where c is the chip code with sum |c[n]|^2 = 1, b the symbol, h[l] and d[l]
the gain and the delay (in chips) of path l, and w[n] ~ CN(0, N0).

Finger l despreads at delay d[l]:  z[l] = sum over n of conj(c[(n - d[l]) mod N]) r[n].
The combiner forms y = sum over l of conj(h[l]) z[l] (maximal ratio weights).
"""

import math
import random

from cbb import cn, qfunc


def shifted(c: list[complex], d: int) -> list[complex]:
    """The code delayed by d chips, cyclically: (c[(n - d) mod N])_n."""
    n = len(c)
    return [c[(k - d) % n] for k in range(n)]


def rake(r: list[complex], c: list[complex], delays: list[int], gains: list[complex]) -> complex:
    """The rake output y = sum over fingers of conj(h[l]) times the despread value at delay d[l]."""
    if len(delays) != len(gains):
        raise ValueError("one gain per delay")
    n = len(c)
    y = 0j  # @line L1
    for d, h in zip(delays, gains):  # @line L2
        z = sum(c[(k - d) % n].conjugate() * r[k] for k in range(n))  # @line L3
        y += h.conjugate() * z  # @line L4
    return y  # @line L5


def composite(c: list[complex], delays: list[int], gains: list[complex]) -> list[complex]:
    """The received pulse g = sum over l of h[l] times the code delayed by d[l]."""
    n = len(c)
    g = [0j] * n
    for d, h in zip(delays, gains):
        for k, v in enumerate(shifted(c, d)):
            g[k] += h * v
    return g


def code_gram(c: list[complex], delays: list[int]) -> list[list[complex]]:
    """R[l][m] = sum over n of conj(c[n - d[l]]) c[n - d[m]], the correlations of the finger codes."""
    cs = [shifted(c, d) for d in delays]
    return [[sum(x.conjugate() * y for x, y in zip(a, b)) for b in cs] for a in cs]


def energy(c: list[complex], delays: list[int], gains: list[complex]) -> float:
    """||g||^2 = h^H R h, the energy of the received pulse per unit Es."""
    rr = code_gram(c, delays)
    total = 0j
    for i, hi in enumerate(gains):
        for k, hk in enumerate(gains):
            total += hi.conjugate() * rr[i][k] * hk
    return total.real


def output_snr(c: list[complex], delays: list[int], gains: list[complex], weights: list[complex], es: float, n0: float) -> float:
    """Es |a^H R h|^2 / (N0 a^H R a): the SNR at the combiner output for weights a."""
    rr = code_gram(c, delays)
    num = sum(weights[i].conjugate() * rr[i][k] * gains[k] for i in range(len(gains)) for k in range(len(gains)))
    den = sum(weights[i].conjugate() * rr[i][k] * weights[k] for i in range(len(gains)) for k in range(len(gains)))
    return es * abs(num) ** 2 / (n0 * den.real)


def bpsk_error_probability(c: list[complex], delays: list[int], gains: list[complex], es: float, n0: float) -> float:
    """Pb = Q(sqrt(2 Es h^H R h / N0)) for BPSK with the rake receiver."""
    return qfunc(math.sqrt(2.0 * es * energy(c, delays, gains) / n0))


def receive(rng: random.Random, b: complex, c: list[complex], delays: list[int], gains: list[complex], es: float, n0: float) -> list[complex]:
    """One received block of N chips, with noise CN(0, N0) per chip (N0 = 0 for no noise)."""
    g = composite(c, delays, gains)
    a = math.sqrt(es) * b
    if n0 == 0:
        return [a * v for v in g]
    return [a * v + cn(rng, n0) for v in g]


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
