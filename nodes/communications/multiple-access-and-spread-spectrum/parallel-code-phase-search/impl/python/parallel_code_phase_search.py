# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-code-phase-search/. The authors are listed in prov/NZHGJE.jsonl.

"""Parallel code phase search: all code phases of one block at once with FFTs.

Model of the received block, one sample per chip:
    x[n] = A e^(j 2 pi nu n / N) c[(n - tau) mod N] + w[n],  n = 0, ..., N - 1,
where nu is the carrier offset in cycles per block. For each candidate offset
nu_i, the search removes the carrier and computes the circular cross-correlation
    R_i[t] = sum over n of y[n] conj(c[(n - t) mod N]),  y[n] = x[n] e^(-j 2 pi nu_i n / N),
for all t at once as IFFT(FFT(y) * conj(FFT(c))).
"""

import cmath
import math
import random

from cbb import cn


def _smallest_factor(n: int) -> int:
    p = 2
    while p * p <= n:
        if n % p == 0:
            return p
        p += 1
    return n


def fft(x: list[complex]) -> list[complex]:
    """X[k] = sum over n of x[n] e^(-j 2 pi k n / N), by a mixed-radix decimation in time.

    The length is split by its smallest prime factor p into p interleaved parts.
    A prime length uses the direct sum.
    """
    n = len(x)
    if n == 1:
        return [complex(x[0])]
    p = _smallest_factor(n)
    if p == n:
        w = [cmath.exp(-2j * math.pi * k / n) for k in range(n)]
        return [sum(x[m] * w[(k * m) % n] for m in range(n)) for k in range(n)]
    m = n // p
    parts = [fft(x[r::p]) for r in range(p)]
    w = [cmath.exp(-2j * math.pi * k / n) for k in range(n)]
    return [sum(w[(r * k) % n] * parts[r][k % m] for r in range(p)) for k in range(n)]


def ifft(xf: list[complex]) -> list[complex]:
    """x[n] = (1/N) sum over k of X[k] e^(j 2 pi k n / N), through fft of the conjugate."""
    n = len(xf)
    return [v.conjugate() / n for v in fft([v.conjugate() for v in xf])]


def pcps(x: list[complex], c: list[complex], nus: list[float]) -> tuple[int, int, float, list[list[complex]]]:
    """Search all code phases and the carrier offsets in nus.

    Returns (i, t, peak, rows): the index of the best offset, the best code phase,
    the peak power |R_i[t]|^2, and the correlations R_i for every offset.
    """
    n = len(x)
    cf = [v.conjugate() for v in fft(c)]  # @line L1
    best = (-1, -1, -1.0)
    rows = []
    for i, nu in enumerate(nus):  # @line L2
        y = [x[k] * cmath.exp(-2j * math.pi * nu * k / n) for k in range(n)]  # @line L3
        xf = fft(y)
        r = ifft([xf[k] * cf[k] for k in range(n)])  # @line L4
        rows.append(r)
        t = max(range(n), key=lambda s: abs(r[s]))  # @line L5
        if abs(r[t]) ** 2 > best[2]:
            best = (i, t, abs(r[t]) ** 2)
    return best[0], best[1], best[2], rows  # @line L6


def received_block(rng: random.Random, c: list[complex], tau: int, nu: float, amp: float, n0: float) -> list[complex]:
    """One block with the code at phase tau, a carrier offset of nu cycles per block, and CN(0, n0) noise."""
    n = len(c)
    out = [amp * cmath.exp(2j * math.pi * nu * k / n) * c[(k - tau) % n] for k in range(n)]
    if n0 > 0:
        out = [v + cn(rng, n0) for v in out]
    return out


def dirichlet(dnu: float, n: int) -> float:
    """|sum over k < n of e^(j 2 pi dnu k / n)| / n, the amplitude loss of a carrier error of dnu cycles per block."""
    if abs(math.sin(math.pi * dnu / n)) < 1e-15:
        return 1.0
    return abs(math.sin(math.pi * dnu) / (n * math.sin(math.pi * dnu / n)))


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
