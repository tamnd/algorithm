# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-entropy-leakage/. The authors are listed in prov/7HY8Q8.jsonl.

import math
from collections.abc import Callable, Hashable, Sequence
from fractions import Fraction

Prior = Sequence[Fraction]
Channel = Sequence[Sequence[Fraction]]


def prior_vulnerability(pi: Prior) -> Fraction:
    """V(pi) = max_x pi[x], the chance to guess the secret in one try. Cost: O(|X|)."""
    return max(pi)


def posterior_vulnerability(pi: Prior, c: Channel) -> Fraction:
    """V(pi, C) = sum_y max_x pi[x] C[x][y]. Precondition: each row of C sums to 1. Cost: O(|X| |Y|)."""
    total = Fraction(0)
    for y in range(len(c[0])):
        total += max(pi[x] * c[x][y] for x in range(len(pi)))
    return total


def leakage_ratio(pi: Prior, c: Channel) -> Fraction:
    """V(pi, C) / V(pi), exact. The leakage in bits is its base-2 logarithm."""
    return posterior_vulnerability(pi, c) / prior_vulnerability(pi)


def min_entropy_leakage(pi: Prior, c: Channel) -> float:
    """Min-entropy leakage L(pi, C) = log2(V(pi, C) / V(pi)) in bits.

    pi is a probability distribution on the secrets 0..|X|-1 and c[x][y] is
    P(Y = y | X = x). Precondition: pi sums to 1 and each row of c sums to 1.
    Cost: O(|X| |Y|) exact arithmetic operations.
    """
    v0 = max(pi)  # @line L1
    v1 = Fraction(0)  # @line L2
    for y in range(len(c[0])):  # @line L3
        v1 += max(pi[x] * c[x][y] for x in range(len(pi)))  # @line L4
    return math.log2(v1 / v0)  # @line L5


def min_capacity(c: Channel) -> float:
    """ML(C) = log2 sum_y max_x C[x][y], the largest min-entropy leakage over all priors."""
    return math.log2(sum(max(row[y] for row in c) for y in range(len(c[0]))))


def deterministic_channel(f: Callable[[int], Hashable], n: int) -> tuple[list[list[Fraction]], list[Hashable]]:
    """The channel matrix of a program y = f(x) on the secrets 0..n-1, and its outputs in order of first use."""
    outputs: list[Hashable] = []
    for x in range(n):
        if f(x) not in outputs:
            outputs.append(f(x))
    c = [[Fraction(1) if f(x) == y else Fraction(0) for y in outputs] for x in range(n)]
    return c, outputs
