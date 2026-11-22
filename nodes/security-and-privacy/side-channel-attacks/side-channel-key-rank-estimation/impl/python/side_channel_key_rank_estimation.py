# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/side-channel-key-rank-estimation/. The authors are listed in prov/BD5WM2.jsonl.
"""Key rank estimation by histogram convolution (Glowacz et al., FSE 2015).

The input is one list of scores for each independent part of the key, as
a side-channel attack gives them (for example log-likelihoods), and the
true key, which an evaluator knows. The output is a lower and an upper
bound on the rank of the true key in the full key space, with no
enumeration. The demo scores come from a stated synthetic model: Gaussian
log-likelihoods of Hamming weight leakage of the 4-bit PRESENT S-box
(Bogdanov et al., CHES 2007), with a seeded ``random.Random``.
"""

import itertools
import math
import random

PRESENT_SBOX: tuple[int, ...] = (
    0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
    0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2,
)


def hamming_weight(v: int) -> int:
    """Return the number of 1 bits of a non-negative integer."""
    return bin(v).count("1")


def synthetic_scores(
    rng: random.Random, key: list[int], m: int, sigma: float
) -> list[list[float]]:
    """Scores for each 4-bit part of the key from m synthetic traces each.

    For part i, the traces are HW(S(p xor key[i])) + N(0, sigma^2) for
    uniform inputs p, and the score of the guess x is the Gaussian log-
    likelihood sum of -(l - HW(S(p xor x)))^2 / (2 sigma^2).
    Cost: O(16 * m) for each part.
    """
    out = []
    for k in key:
        obs = []
        for _ in range(m):
            p = rng.randrange(16)
            obs.append((p, hamming_weight(PRESENT_SBOX[p ^ k]) + rng.gauss(0.0, sigma)))
        out.append([
            -sum((l - hamming_weight(PRESENT_SBOX[p ^ x])) ** 2 for p, l in obs) / (2 * sigma * sigma)
            for x in range(16)
        ])
    return out


def convolve(a: list[int], b: list[int]) -> list[int]:
    """Exact convolution of two integer histograms.

    out[s] = sum of a[i] * b[s - i]. Python integers do not overflow, so the
    counts are exact for any number of keys.
    Cost: O(len(a) * z + len(b)), with z the number of nonzero bins of b.
    """
    nonzero = [(j, y) for j, y in enumerate(b) if y]
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in nonzero:
                out[i + j] += x * y
    return out


def key_rank_bounds(scores: list[list[float]], key: list[int], width: float) -> tuple[int, int]:
    """Return (lower, upper) with lower <= rank <= upper, by Glowacz et al.

    The rank of the key is 1 plus the number of full keys whose total score
    (the sum of the scores of their parts) is strictly larger than the
    total score of the true key. Each part is shifted so that its smallest
    score is 0 and cut into bins of the given width; the histograms are
    convolved exactly, and the bounds follow from the bin of the true key.
    The bounds are exact for exact arithmetic, for example with
    fractions.Fraction scores and width; with floats a score that lies on a
    bin edge can be rounded into the next bin.

    Precondition: d >= 1 parts, each with at least one score, width > 0,
    and key[i] in range(len(scores[i])).
    Cost: O(d * K + d^2 * N * min(N, K)) time and O(d * N + d * K) extra
    space, for d parts of K scores each and at most N bins in each
    histogram.
    """
    d = len(scores)
    hists: list[list[int]] = []
    star = 0
    for i in range(d):  # @line L1
        lo = min(scores[i])
        shifted = [s - lo for s in scores[i]]  # @line L2
        idx = [math.floor(s / width) for s in shifted]
        hist = [0] * (max(idx) + 1)
        for b in idx:
            hist[b] += 1  # @line L3
        hists.append(hist)
        star += idx[key[i]]  # @line L4
    total = hists[0]  # @line L5
    for i in range(1, d):  # @line L6
        total = convolve(total, hists[i])
    lower = 1 + sum(total[max(star + d, 0):])  # @line L7
    upper = sum(total[max(star - d + 1, 0):])  # @line L8
    return lower, upper  # @line L9


def brute_force_rank(scores: list[list[float]], key: list[int]) -> int:
    """Rank by enumeration of all full keys. Cost: Theta(d * K^d)."""
    target = sum(scores[i][key[i]] for i in range(len(scores)))
    better = 0
    for combo in itertools.product(*scores):
        if sum(combo) > target:
            better += 1
    return 1 + better
