# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shannon-entropy/. The authors are listed in prov/A13CS0.jsonl.
"""Shannon entropy of a distribution, and the empirical entropies H_0 and H_k of a string."""

from collections import Counter, defaultdict
from math import log
from typing import Hashable, Iterable, Sequence


def entropy(probs: Iterable[float], base: float = 2.0) -> float:
    """H = -sum p log p over the given probabilities. Terms with p = 0 add 0."""
    ps = list(probs)
    if any(p < 0 for p in ps):
        raise ValueError("a probability is negative")
    if abs(sum(ps) - 1.0) > 1e-9:
        raise ValueError("the probabilities do not sum to 1")
    return -sum(p * log(p, base) for p in ps if p > 0)


def counts_entropy_times_n(counts: Iterable[int]) -> float:
    """n * H_0 for a string with the given symbol counts: sum c log2(n / c)."""
    cs = [c for c in counts if c > 0]
    n = sum(cs)
    return sum(c * log(n / c, 2) for c in cs)


def empirical_h0(s: Sequence[Hashable]) -> float:
    """The zero-order empirical entropy H_0(s) in bits per symbol. H_0 of the empty string is 0."""
    if len(s) == 0:
        return 0.0
    return counts_entropy_times_n(Counter(s).values()) / len(s)


def empirical_hk(s: Sequence[Hashable], k: int) -> float:
    """The k-th order empirical entropy H_k(s) of Manzini (2001), in bits per symbol.

    For each context w of length k, w_s is the string of the symbols that follow
    the occurrences of w in s. Then |s| H_k(s) = sum over w of |w_s| H_0(w_s).
    """
    if k < 0:
        raise ValueError("k must be non-negative")
    n = len(s)
    if n == 0:
        return 0.0
    if k == 0:
        return empirical_h0(s)
    follow: dict = defaultdict(Counter)
    for i in range(k, n):
        follow[tuple(s[i - k:i])][s[i]] += 1
    total = sum(counts_entropy_times_n(c.values()) for c in follow.values())
    return total / n
