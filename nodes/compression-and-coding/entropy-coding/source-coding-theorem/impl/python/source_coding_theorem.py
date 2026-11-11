# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/source-coding-theorem/. The authors are listed in prov/53WS0H.jsonl.
"""Both forms of the source coding theorem for a Bernoulli(p) source.

Fixed-length form: a block code that sends the index of a typical sequence in
about nR bits, and fails on the other sequences. Variable-length form: the
Shannon code lengths ceil(-log2 P(x)) on blocks of n symbols.
"""

import math
import random
from fractions import Fraction
from math import comb, log2
from typing import Sequence


def bernoulli_entropy(p: float) -> float:
    if p in (0.0, 1.0):
        return 0.0
    return -p * log2(p) - (1 - p) * log2(1 - p)


def rank_fixed_weight(x: Sequence[int]) -> int:
    """The rank of the bit string x among the strings of its length and weight, in lexicographic order."""
    n, k, r = len(x), sum(x), 0
    for i, b in enumerate(x):
        if b == 1:
            r += comb(n - i - 1, k)  # the strings with a 0 here come first
            k -= 1
    return r


def unrank_fixed_weight(n: int, k: int, r: int) -> list[int]:
    out = []
    for i in range(n):
        c = comb(n - i - 1, k)  # strings with a 0 at position i
        if r < c:
            out.append(0)
        else:
            out.append(1)
            r -= c
            k -= 1
    return out


class TypicalSetCode:
    """A fixed-length code of block length n for Bernoulli(p) at rate R > H(p).

    The codebook is the typical set A_eps^(n) with eps = R - H. A sequence in it
    is sent as its index in ceil(log2 |A|) bits; any other sequence is an error.
    """

    def __init__(self, n: int, p: float, R: float) -> None:
        H = bernoulli_entropy(p)
        if not 0 < p < 1 or R <= H:
            raise ValueError("need 0 < p < 1 and R > H(p)")
        self.n, self.p, self.eps = n, p, R - H
        self.weights = [k for k in range(n + 1) if abs(-(k * log2(p) + (n - k) * log2(1 - p)) / n - H) <= self.eps]
        self.offset = {}
        total = 0
        for k in self.weights:
            self.offset[k] = total
            total += comb(n, k)
        self.size = total
        self.bits = max(1, math.ceil(log2(total))) if total > 0 else 0

    def encode(self, x: Sequence[int]) -> int | None:
        """The index of x in the codebook, or None when x is not typical."""
        k = sum(x)
        if len(x) != self.n or k not in self.offset:
            return None
        return self.offset[k] + rank_fixed_weight(x)

    def decode(self, index: int) -> list[int]:
        for k in reversed(self.weights):
            if index >= self.offset[k]:
                return unrank_fixed_weight(self.n, k, index - self.offset[k])
        raise ValueError("index out of range")

    def error_probability(self) -> float:
        p = Fraction(self.p)
        ok = sum(comb(self.n, k) * p ** k * (1 - p) ** (self.n - k) for k in self.weights)
        return float(1 - ok)


def best_fixed_length_success(n: int, p: Fraction, bits: int) -> Fraction:
    """The largest probability that any code with 2^bits codewords gets right.

    The best code keeps the 2^bits most probable sequences. For p < 1/2 these
    are the sequences of smallest weight.
    """
    p = Fraction(p)
    if not 0 < p < Fraction(1, 2):
        raise ValueError("need 0 < p < 1/2")
    left, ok = 2 ** bits, Fraction(0)
    for k in range(n + 1):
        take = min(left, comb(n, k))
        ok += take * p ** k * (1 - p) ** (n - k)
        left -= take
        if left == 0:
            break
    return ok


def measured_error_rate(code: TypicalSetCode, trials: int, seed: int) -> float:
    """The fraction of random source blocks that the code cannot send."""
    rng = random.Random(seed)
    bad = 0
    for _ in range(trials):
        x = [1 if rng.random() < code.p else 0 for _ in range(code.n)]
        idx = code.encode(x)
        if idx is None:
            bad += 1
        elif code.decode(idx) != x:
            raise AssertionError("decoding failed on a typical sequence")
    return bad / trials


def shannon_block_rate(n: int, p: Fraction) -> float:
    """The mean code length per symbol of the Shannon code ceil(-log2 P(x)) on blocks of n symbols."""
    p = Fraction(p)
    total = Fraction(0)
    for k in range(n + 1):
        q = p ** k * (1 - p) ** (n - k)
        length = math.ceil(-log2(q)) if q < 1 else 0
        # Correct a rounding error of log2 at an exact power of two.
        while length > 0 and Fraction(1, 2 ** (length - 1)) <= q:
            length -= 1
        while Fraction(1, 2 ** length) > q:
            length += 1
        total += comb(n, k) * q * length
    return float(total) / n
