# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/g-leakage/. The authors are listed in prov/XKQ40D.jsonl.

import itertools
import math
from collections.abc import Sequence
from fractions import Fraction

Prior = Sequence[Fraction]
Channel = Sequence[Sequence[Fraction]]
Gain = Sequence[Sequence[Fraction]]  # gain[w][x] for guess w and secret x


def g_vulnerability(pi: Prior, gain: Gain) -> Fraction:
    """V_g(pi) = max_w sum_x pi[x] gain[w][x]. Cost: O(|W| |X|)."""
    return max(sum(pi[x] * row[x] for x in range(len(pi))) for row in gain)


def posterior_g_vulnerability(pi: Prior, c: Channel, gain: Gain) -> Fraction:
    """V_g(pi, C) = sum_y max_w sum_x pi[x] C[x][y] gain[w][x]. Cost: O(|Y| |W| |X|)."""
    total = Fraction(0)
    for y in range(len(c[0])):
        total += max(sum(pi[x] * c[x][y] * row[x] for x in range(len(pi))) for row in gain)
    return total


def g_leakage(pi: Prior, c: Channel, gain: Gain) -> float:
    """g-leakage L_g(pi, C) = log2(V_g(pi, C) / V_g(pi)) in bits.

    Precondition: pi is a distribution on the secrets 0..|X|-1, each row of c
    sums to 1, every gain value is in [0, 1], and V_g(pi) > 0. Cost: O(|Y| |W| |X|)
    exact arithmetic operations for |W| guesses.
    """
    vg0 = max(sum(pi[x] * row[x] for x in range(len(pi))) for row in gain)  # @line L1
    vg1 = Fraction(0)  # @line L2
    for y in range(len(c[0])):  # @line L3
        vg1 += max(sum(pi[x] * c[x][y] * row[x] for x in range(len(pi))) for row in gain)  # @line L4
    return math.log2(vg1 / vg0)  # @line L5


def identity_gain(n: int) -> list[list[Fraction]]:
    """The gain of one exact guess: 1 when w = x, else 0. It gives min-entropy leakage."""
    return [[Fraction(int(w == x)) for x in range(n)] for w in range(n)]


def k_tries_gain(n: int, k: int) -> list[list[Fraction]]:
    """The gain of k guesses: one guess per set of k secrets, worth 1 when the secret is in the set."""
    return [[Fraction(int(x in s)) for x in range(n)] for s in itertools.combinations(range(n), k)]


def partition_gain(blocks: Sequence[Sequence[int]], n: int) -> list[list[Fraction]]:
    """The gain of guessing the block of a partition that holds the secret."""
    return [[Fraction(int(x in b)) for x in range(n)] for b in blocks]
