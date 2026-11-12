# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-symmetric-channel/. The authors are listed in prov/F9CZ5N.jsonl.
"""The binary symmetric channel BSC(p): each bit is flipped with probability p, independently.

A block of n bits is a Python integer (bit i is position i). The module simulates the
channel, gives its transition probabilities and capacity, and decodes a block code by
maximum likelihood, which on this channel is the same as minimum distance decoding.
"""

import math
import random
from typing import Dict, List, Optional, Sequence, Tuple


def binary_entropy(p: float) -> float:
    """h(p) = -p log2 p - (1 - p) log2 (1 - p), with h(0) = h(1) = 0."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def transmit(word: int, n: int, p: float, rng: random.Random) -> int:
    """Send an n-bit word through BSC(p): flip each bit independently with probability p."""
    noise = 0
    for i in range(n):
        if rng.random() < p:
            noise |= 1 << i
    return word ^ noise


def transition(x: int, y: int, n: int, p: float) -> float:
    """P(y | x) = p^d (1 - p)^(n - d) for n uses of the channel, with d the Hamming distance."""
    d = (x ^ y).bit_count()
    return p ** d * (1.0 - p) ** (n - d)


def mutual_information(a: float, p: float) -> float:
    """I(X; Y) in bits when P(X = 1) = a: H(Y) - H(Y | X) = h(a(1 - p) + (1 - a)p) - h(p)."""
    return binary_entropy(a * (1.0 - p) + (1.0 - a) * p) - binary_entropy(p)


def capacity(p: float) -> float:
    """C = 1 - h(p) bits per channel use, reached by the uniform input."""
    return 1.0 - binary_entropy(p)


def cascade(p: float, q: float) -> float:
    """Crossover probability of BSC(p) followed by BSC(q): a bit ends flipped if exactly one flips it."""
    return p * (1.0 - q) + q * (1.0 - p)


def ml_decode(code: Sequence[int], y: int, n: int, p: float) -> List[int]:
    """All codewords x that maximize P(y | x): the maximum likelihood decisions (ties included)."""
    best = max(transition(x, y, n, p) for x in code)
    return [x for x in code if transition(x, y, n, p) == best]


def nearest_codewords(code: Sequence[int], y: int) -> List[int]:
    """All codewords at the least Hamming distance from y."""
    best = min((x ^ y).bit_count() for x in code)
    return [x for x in code if (x ^ y).bit_count() == best]


def block_error_rate(code: Sequence[int], n: int, p: float, trials: int, seed: int = 1) -> float:
    """Monte Carlo block error rate of minimum distance decoding (a tie counts as an error)."""
    rng = random.Random(seed)
    errors = 0
    for _ in range(trials):
        x = code[rng.randrange(len(code))]
        dec = nearest_codewords(code, transmit(x, n, p, rng))
        if dec != [x]:
            errors += 1
    return errors / trials


def exact_block_error_rate(code: Sequence[int], n: int, p: float) -> float:
    """Exact block error rate of the same decoder, summed over all 2^n received words."""
    total = 0.0
    for x in code:
        for y in range(1 << n):
            if nearest_codewords(code, y) != [x]:
                total += transition(x, y, n, p)
    return total / len(code)
