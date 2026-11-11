# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asymptotic-equipartition-property/. The authors are listed in prov/02QMVF.jsonl.
"""The typical set of a Bernoulli(p) source, computed exactly by grouping sequences by weight."""

from fractions import Fraction
from math import comb, log2


def bernoulli_entropy(p: float) -> float:
    if p in (0.0, 1.0):
        return 0.0
    return -p * log2(p) - (1 - p) * log2(1 - p)


def sample_entropy(n: int, k: int, p: float) -> float:
    """-(1/n) log2 P(x) for any n-bit x with k ones, under Bernoulli(p) with 0 < p < 1."""
    return -(k * log2(p) + (n - k) * log2(1 - p)) / n


def typical_weights(n: int, p: float, eps: float) -> list[int]:
    """The weights k whose sequences lie in A_eps^(n) = {x : |-(1/n) log2 P(x) - H| <= eps}."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    H = bernoulli_entropy(p)
    return [k for k in range(n + 1) if abs(sample_entropy(n, k, p) - H) <= eps]


def typical_set(n: int, p: Fraction, eps: float) -> tuple[Fraction, int]:
    """The exact probability and the exact size of A_eps^(n) for Bernoulli(p).

    All sequences of the same weight k have the same probability, so the set is
    a union of whole weight classes, and the sums run over n + 1 weights.
    """
    p = Fraction(p)
    ks = typical_weights(n, float(p), eps)
    prob = sum((comb(n, k) * p ** k * (1 - p) ** (n - k) for k in ks), Fraction(0))
    size = sum(comb(n, k) for k in ks)
    return prob, size
