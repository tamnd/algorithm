# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fountain-codes/. The authors are listed in prov/BM90XJ.jsonl.
"""The random linear fountain over GF(2), with an online Gaussian elimination decoder.

Encoded symbol j is the XOR of the source symbols selected by a uniform random k-bit mask
drawn from a generator seeded with j. The decoder adds each received symbol to a reduced
basis and stops as soon as the k masks have full rank.
"""

import random
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple


def mask_of(seed: int, k: int) -> int:
    return random.Random(seed).getrandbits(k)


def encode_symbol(source: Sequence[int], seed: int) -> Tuple[int, int]:
    """Returns (mask, value). A mask of 0 is allowed; it carries no information."""
    m = mask_of(seed, len(source))
    v = 0
    for i, s in enumerate(source):
        if m >> i & 1:
            v ^= s
    return m, v


class OnlineDecoder:
    """Keeps rows (mask, value) with distinct leading bits; solves when the rank is k."""

    def __init__(self, k: int):
        self.k = k
        self.rows: Dict[int, Tuple[int, int]] = {}  # leading bit -> (mask, value)
        self.received = 0

    def add(self, mask: int, value: int) -> bool:
        """Add one symbol. Returns True if it raised the rank."""
        self.received += 1
        while mask:
            top = mask.bit_length() - 1
            if top not in self.rows:
                self.rows[top] = (mask, value)
                return True
            m2, v2 = self.rows[top]
            mask, value = mask ^ m2, value ^ v2
        return False

    def done(self) -> bool:
        return len(self.rows) == self.k

    def solve(self) -> Optional[List[int]]:
        if not self.done():
            return None
        out = [0] * self.k
        for top in range(self.k):  # rows with smaller leading bits are solved first
            mask, value = self.rows[top]
            for i in range(top):
                if mask >> i & 1:
                    value ^= out[i]
            out[top] = value
        return out


def symbols_needed(source: Sequence[int], first_seed: int) -> Tuple[int, List[int]]:
    """Receive symbols with seeds first_seed, first_seed + 1, ... until decodable."""
    dec = OnlineDecoder(len(source))
    seed = first_seed
    while not dec.done():
        dec.add(*encode_symbol(source, seed))
        seed += 1
    return dec.received, dec.solve()


def full_rank_probability(k: int, n: int) -> Fraction:
    """P(a uniform random n x k binary matrix has rank k) = prod_(i<k) (1 - 2^(i - n))."""
    p = Fraction(1)
    for i in range(k):
        p *= 1 - Fraction(1, 2 ** (n - i))
    return p


def expected_symbols(k: int) -> Fraction:
    """E[number of uniform random masks until rank k] = sum_(j=1..k) 2^j / (2^j - 1)."""
    return sum((Fraction(2 ** j, 2 ** j - 1) for j in range(1, k + 1)), Fraction(0))
