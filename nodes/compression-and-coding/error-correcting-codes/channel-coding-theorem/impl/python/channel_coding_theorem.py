# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/channel-coding-theorem/. The authors are listed in prov/VK14Z9.jsonl.
"""Random coding on a binary symmetric channel: the experiment behind the coding theorem.

A codebook of M = 2^round(nR) random n-bit words is drawn for each trial, one codeword is
sent through BSC(p), and the receiver decodes by maximum likelihood (nearest codeword, ties
broken at random) or by joint typicality as in the proof. Words are Python integers.
The functions also give the union bound of the proof and the converse bound from Fano.
"""

import math
import random
from math import comb
from typing import List, Optional


def binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def bsc_capacity(p: float) -> float:
    return 1.0 - binary_entropy(p)


def bsc_noise(n: int, p: float, rng: random.Random) -> int:
    z = 0
    for i in range(n):
        if rng.random() < p:
            z |= 1 << i
    return z


def ml_decode(code: List[int], y: int, rng: random.Random) -> int:
    """Index of a nearest codeword to y; among several at the least distance, pick one at random."""
    best = min((c ^ y).bit_count() for c in code)
    ties = [i for i, c in enumerate(code) if (c ^ y).bit_count() == best]
    return ties[rng.randrange(len(ties))]


def typicality_decode(code: List[int], y: int, n: int, p: float, delta: float) -> Optional[int]:
    """The joint typicality decoder for BSC(p) with the uniform input.

    For the uniform input every x and y is typical, and (x, y) is jointly typical exactly when
    the fraction of flipped positions d(x, y)/n is within delta of p. The decoder returns the
    unique such codeword, and None if there is none or more than one.
    """
    hits = [i for i, c in enumerate(code) if abs((c ^ y).bit_count() / n - p) <= delta]
    return hits[0] if len(hits) == 1 else None


def random_code_error_rate(n: int, rate: float, p: float, trials: int, seed: int,
                           decoder: str = "ml", delta: float = 0.1) -> float:
    """Block error rate averaged over random codebooks and noise (a new codebook in each trial)."""
    rng = random.Random(seed)
    m = 2 ** round(n * rate)
    errors = 0
    for _ in range(trials):
        code = [rng.getrandbits(n) for _ in range(m)]
        sent = rng.randrange(m)
        y = code[sent] ^ bsc_noise(n, p, rng)
        if decoder == "ml":
            out: Optional[int] = ml_decode(code, y, rng)
        else:
            out = typicality_decode(code, y, n, p, delta)
        errors += out != sent
    return errors / trials


def union_bound(n: int, m: int, p: float) -> float:
    """Upper bound on the ensemble error of nearest codeword decoding (ties counted as errors).

    If w bits flip, each of the other m - 1 random codewords is at distance <= w from y with
    probability sum_{j <= w} C(n, j) / 2^n; a union bound over them, capped at 1, gives
    sum_w C(n, w) p^w (1 - p)^(n - w) min(1, (m - 1) sum_{j <= w} C(n, j) / 2^n).
    """
    total = 0.0
    ball = 0
    for w in range(n + 1):
        ball += comb(n, w)
        total += comb(n, w) * p ** w * (1 - p) ** (n - w) * min(1.0, (m - 1) * ball / 2 ** n)
    return total


def fano_lower_bound(n: int, rate: float, capacity: float) -> float:
    """Weak converse: every code of rate R has average error at least 1 - C/R - 1/(nR)."""
    return 1.0 - capacity / rate - 1.0 / (n * rate)
