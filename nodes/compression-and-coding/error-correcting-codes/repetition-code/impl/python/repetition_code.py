# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/repetition-code/. The authors are listed in prov/8TYFGD.jsonl.
"""The repetition code [n, 1, n]: send each symbol n times, decode each block by majority vote.

Symbols can be any hashable values; for bits, use 0 and 1. A tie (possible for even n, or with
more than two symbols) is broken by the random generator given to the decoder, or reported as
None when no generator is given.
"""

import random
from collections import Counter
from math import comb
from typing import Hashable, List, Optional, Sequence


def encode(message: Sequence[Hashable], n: int) -> List[Hashable]:
    """Repeat each message symbol n times."""
    out: List[Hashable] = []
    for s in message:
        out.extend([s] * n)
    return out


def majority(block: Sequence[Hashable], rng: Optional[random.Random] = None) -> Optional[Hashable]:
    """The most frequent symbol of a block (the nearest codeword); ties go to rng or give None."""
    counts = Counter(block).most_common()
    top = counts[0][1]
    winners = [s for s, c in counts if c == top]
    if len(winners) == 1:
        return winners[0]
    if rng is None:
        return None
    return winners[rng.randrange(len(winners))]


def decode(received: Sequence[Hashable], n: int, rng: Optional[random.Random] = None) -> List[Optional[Hashable]]:
    """Majority decoding of each block of n received symbols. Cost: O(length)."""
    if len(received) % n:
        raise ValueError("the received length must be a multiple of n")
    return [majority(received[i:i + n], rng) for i in range(0, len(received), n)]


def error_probability(n: int, p: float) -> float:
    """Exact probability that majority decoding of one bit fails on BSC(p).

    For odd n it is sum_{i > n/2} C(n, i) p^i (1 - p)^(n - i). For even n, a tie of n/2 flips is
    broken by a fair coin and counts as half an error.
    """
    total = sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n // 2 + 1, n + 1))
    if n % 2 == 0:
        total += 0.5 * comb(n, n // 2) * p ** (n // 2) * (1 - p) ** (n // 2)
    return total


def chernoff_bound(n: int, p: float) -> float:
    """(4 p (1 - p))^(n / 2) = 2^(-n D(1/2 || p)), an upper bound on the error for p < 1/2."""
    return (4.0 * p * (1.0 - p)) ** (n / 2.0)


def shortest_length(p: float, target: float) -> int:
    """The least odd n with error_probability(n, p) <= target, for p < 1/2."""
    n = 1
    while error_probability(n, p) > target:
        n += 2
    return n


def simulate(n: int, p: float, bits: int, seed: int = 1) -> float:
    """Monte Carlo bit error rate of the repetition code on BSC(p)."""
    rng = random.Random(seed)
    message = [rng.getrandbits(1) for _ in range(bits)]
    sent = encode(message, n)
    received = [b ^ (rng.random() < p) for b in sent]
    decoded = decode(received, n, rng)
    return sum(a != b for a, b in zip(message, decoded)) / bits
