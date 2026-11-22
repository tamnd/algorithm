# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-power-analysis/. The authors are listed in prov/NV7DCA.jsonl.
"""Differential power analysis (difference of means) on a synthetic leakage model.

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


def differential_power_analysis(
    traces: list[Trace],
    sbox: tuple[int, ...] = PRESENT_SBOX,
    bit: int = 1,
    signed: bool = True,
) -> tuple[int, list[float]]:
    """Return (best guess, score of each guess) by Kocher's difference of means.

    For each key guess g, the traces are split by bit ``bit`` of
    sbox[p ^ g]. The differential trace is the mean of the 1 group minus
    the mean of the 0 group, sample by sample. The score of g is the
    largest value of the differential trace (its largest absolute value
    when ``signed`` is False). A guess with an empty group scores -inf.
    The first guess with the top score wins. If no guess has a finite
    score (for example with one trace), the best guess is -1.

    Precondition: every trace has the same number of samples T >= 1, and
    every input is in range(len(sbox)).
    Cost: Theta(g * m * T) time for g = len(sbox) guesses and m traces,
    and Theta(g + T) extra space.
    """
    if not traces:
        raise ValueError("need at least one trace")
    t_len = len(traces[0][1])
    best, top = -1, -math.inf  # @line L1
    scores: list[float] = []
    for g in range(len(sbox)):  # @line L2
        sum1 = [0.0] * t_len
        sum0 = [0.0] * t_len
        n1 = n0 = 0
        for p, row in traces:  # @line L3
            if (sbox[p ^ g] >> bit) & 1:  # @line L4
                n1 += 1
                for j in range(t_len):
                    sum1[j] += row[j]
            else:
                n0 += 1  # @line L5
                for j in range(t_len):
                    sum0[j] += row[j]
        if n1 == 0 or n0 == 0:  # @line L6
            score = -math.inf
        else:
            delta = [sum1[j] / n1 - sum0[j] / n0 for j in range(t_len)]  # @line L7
            score = max(delta) if signed else max(abs(x) for x in delta)  # @line L8
        scores.append(score)
        if score > top:  # @line L9
            best, top = g, score  # @line L10
    return best, scores  # @line L11
