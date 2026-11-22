# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/correlation-power-analysis/. The authors are listed in prov/H5FN0Q.jsonl.
"""Correlation power analysis on a synthetic Hamming weight leakage model.

The traces come from a stated statistical model, never from a device:
sample ``leak_sample`` of a trace is ``epsilon * HW(S(p xor k)) + noise`` and
every other sample is noise only. S is the 4-bit S-box of PRESENT
(Bogdanov et al., CHES 2007). The noise is Gaussian with a seeded
``random.Random``. This is a study model for defenders and students.
"""

import math
import random

PRESENT_SBOX: tuple[int, ...] = (
    0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
    0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2,
)

Trace = tuple[int, list[float]]


def hamming_weight(v: int) -> int:
    """Return the number of 1 bits of a non-negative integer."""
    return bin(v).count("1")


def simulate_traces(
    rng: random.Random,
    key: int,
    m: int,
    sigma: float,
    samples: int = 4,
    leak_sample: int = 2,
    epsilon: float = 1.0,
    sbox: tuple[int, ...] = PRESENT_SBOX,
) -> list[Trace]:
    """Draw m synthetic traces (input, samples) from the Hamming weight model.

    Each input p is uniform on the S-box domain. Sample ``leak_sample`` is
    epsilon * HW(sbox[p ^ key]) + N(0, sigma^2); the other samples are
    N(0, sigma^2). Cost: O(m * samples).
    """
    n = len(sbox)
    out: list[Trace] = []
    for _ in range(m):
        p = rng.randrange(n)
        row = [rng.gauss(0.0, sigma) if sigma > 0 else 0.0 for _ in range(samples)]
        row[leak_sample] += epsilon * hamming_weight(sbox[p ^ key])
        out.append((p, row))
    return out


def pearson(xs: list[float], ys: list[float]) -> float:
    """Pearson correlation of two lists of the same length, by two passes.

    Returns 0.0 when either list has zero variance. Cost: O(len(xs)).
    """
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sxx = syy = 0.0
    for x, y in zip(xs, ys):
        dx = x - mx
        dy = y - my
        sxy += dx * dy
        sxx += dx * dx
        syy += dy * dy
    if sxx == 0.0 or syy == 0.0:
        return 0.0
    return sxy / math.sqrt(sxx * syy)


def correlation_power_analysis(
    traces: list[Trace],
    sbox: tuple[int, ...] = PRESENT_SBOX,
    signed: bool = False,
) -> tuple[int, list[float]]:
    """Return (best guess, score of each guess) by the attack of Brier et al.

    For each key guess g the hypothesis of trace i is HW(sbox[p_i ^ g]).
    The score of g is the largest absolute Pearson correlation between the
    hypothesis and one sample of the traces (the largest signed value when
    ``signed`` is True). A sample or a hypothesis with zero variance gives
    correlation 0. The first guess with the top score wins; with no trace
    at all the call raises ValueError.

    Precondition: every trace has the same number of samples T >= 1, and
    every input is in range(len(sbox)).
    Cost: Theta(g * m * T) time for g = len(sbox) guesses and m traces,
    and Theta(m + T + g) extra space.
    """
    if not traces:
        raise ValueError("need at least one trace")
    t_len = len(traces[0][1])
    best, top = -1, -math.inf  # @line L1
    scores: list[float] = []
    for g in range(len(sbox)):  # @line L2
        h = [float(hamming_weight(sbox[p ^ g])) for p, _ in traces]  # @line L3
        rs = []
        for j in range(t_len):  # @line L4
            rs.append(pearson(h, [row[j] for _, row in traces]))  # @line L5
        score = max(rs) if signed else max(abs(r) for r in rs)  # @line L6
        scores.append(score)
        if score > top:  # @line L7
            best, top = g, score  # @line L8
    return best, scores  # @line L9


def traces_needed(rho: float, z: float = 3.719016485) -> float:
    """Rule of thumb for the number of traces to detect a correlation rho.

    n = 3 + 8 * z^2 / ln^2((1 + rho) / (1 - rho)), from the Fisher z
    transform (Mangard, Oswald and Popp, Chapter 6). The default z is the
    quantile for alpha = 0.0001. Precondition: 0 < rho < 1. Cost: O(1).
    """
    return 3.0 + 8.0 * (z / math.log((1.0 + rho) / (1.0 - rho))) ** 2
