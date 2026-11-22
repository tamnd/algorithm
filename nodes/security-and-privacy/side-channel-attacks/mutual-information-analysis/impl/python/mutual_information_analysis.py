# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-information-analysis/. The authors are listed in prov/DNRK95.jsonl.
"""Mutual information analysis with a histogram estimator, on synthetic traces.

The traces come from a stated statistical model, never from a device:
sample ``leak_sample`` of a trace is ``leak(HW(S(p xor k))) + noise`` and
every other sample is noise only. S is the 4-bit S-box of PRESENT
(Bogdanov et al., CHES 2007). The noise is Gaussian with a seeded
``random.Random``. This is a study model for defenders and students.
"""

import math
import random
from collections.abc import Callable

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
    leak: Callable[[int], float] = float,
    sbox: tuple[int, ...] = PRESENT_SBOX,
) -> list[Trace]:
    """Draw m synthetic traces (input, samples).

    Each input p is uniform on the S-box domain. Sample ``leak_sample`` is
    leak(HW(sbox[p ^ key])) + N(0, sigma^2); the other samples are
    N(0, sigma^2). The default leak is the Hamming weight itself.
    Cost: O(m * samples).
    """
    n = len(sbox)
    out: list[Trace] = []
    for _ in range(m):
        p = rng.randrange(n)
        row = [rng.gauss(0.0, sigma) if sigma > 0 else 0.0 for _ in range(samples)]
        row[leak_sample] += leak(hamming_weight(sbox[p ^ key]))
        out.append((p, row))
    return out


def equal_width_bins(column: list[float], bins: int) -> list[int]:
    """Map each value to one of ``bins`` equal bins from min to max.

    The maximum goes to the last bin. A constant column goes to bin 0.
    Cost: O(len(column)).
    """
    lo = min(column)
    hi = max(column)
    if hi == lo:
        return [0] * len(column)
    width = (hi - lo) / bins
    return [min(int((v - lo) / width), bins - 1) for v in column]


def plug_in_entropy(counts: list[int], total: int) -> float:
    """Shannon entropy in bits of the empirical distribution of the counts."""
    h = 0.0
    for c in counts:
        if c:
            q = c / total
            h -= q * math.log2(q)
    return h


def mutual_information_analysis(
    traces: list[Trace],
    bins: int = 8,
    sbox: tuple[int, ...] = PRESENT_SBOX,
    model: Callable[[int], int] = hamming_weight,
) -> tuple[int, list[float]]:
    """Return (best guess, score of each guess) by the MIA of Gierlichs et al.

    Each sample is cut into ``bins`` equal-width bins. For a key guess g
    the model value of trace i is model(sbox[p_i ^ g]). The score of g is
    the largest plug-in estimate, over the samples, of the mutual
    information in bits between the bin of the sample and the model value.
    The first guess with the top score wins.

    Precondition: at least one trace, every trace has the same number of
    samples T >= 1, bins >= 1, and every input is in range(len(sbox)).
    Cost: Theta(m * T) to bin and Theta(g * T * (m + V * B)) for the
    guesses, with V model values and B bins; Theta(m * T + V * B) extra
    space.
    """
    if not traces:
        raise ValueError("need at least one trace")
    m = len(traces)
    t_len = len(traces[0][1])
    best, top = -1, -math.inf  # @line L1
    binned = [equal_width_bins([row[j] for _, row in traces], bins) for j in range(t_len)]  # @line L2
    scores: list[float] = []
    for g in range(len(sbox)):  # @line L3
        h = [model(sbox[p ^ g]) for p, _ in traces]  # @line L4
        values = sorted(set(h))
        index = {v: a for a, v in enumerate(values)}
        mis = []
        for j in range(t_len):  # @line L5
            joint = [[0] * bins for _ in values]
            for i in range(m):
                joint[index[h[i]]][binned[j][i]] += 1  # @line L6
            row_counts = [sum(r) for r in joint]
            col_counts = [sum(joint[a][b] for a in range(len(values))) for b in range(bins)]
            flat = [c for r in joint for c in r]
            mis.append(
                plug_in_entropy(col_counts, m)
                + plug_in_entropy(row_counts, m)
                - plug_in_entropy(flat, m)
            )  # @line L7
        score = max(mis)  # @line L8
        scores.append(score)
        if score > top:  # @line L9
            best, top = g, score  # @line L10
    return best, scores  # @line L11
