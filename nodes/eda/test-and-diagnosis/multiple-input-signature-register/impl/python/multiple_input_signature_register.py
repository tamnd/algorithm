# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-input-signature-register/. The authors are listed in prov/CM81DK.jsonl.
"""A multiple-input signature register (MISR) with internal XOR feedback.

The register has k stages r_0, ..., r_(k-1). Read as a polynomial over GF(2),
r(x) = r_0 + r_1 x + ... + r_(k-1) x^(k-1). The feedback polynomial is
q(x) = x^k + q_(k-1) x^(k-1) + ... + q_0, stored as an int with bit i equal to
the coefficient of x^i (so bit k is set). One clock with the input word
w = (w_0, ..., w_(k-1)) does

    r <- (x * r(x) + w(x)) mod q(x),

which in hardware is a shift toward the high stage, an XOR of the low k bits
of q into the stages when the top stage was 1, and an XOR of the input word.
After m clocks from the seed s, the register holds
(x^m s(x) + sum_t x^(m-1-t) w_t(x)) mod q(x).

Each clock costs O(1) operations on k-bit words (O(k) bit operations).
"""

from __future__ import annotations

from typing import Iterable


class MISR:
    """A k-bit MISR with feedback polynomial q of degree k."""

    def __init__(self, k: int, q: int, seed: int = 0) -> None:
        """Precondition: k >= 1, q has degree exactly k, and 0 <= seed < 2^k."""
        if k < 1 or q >> k != 1:
            raise ValueError("q must have degree exactly k")
        self.k = k
        self.q = q
        self.mask = (1 << k) - 1
        self.low = q & self.mask  # q(x) - x^k
        self.r = 0
        self.reset(seed)

    def reset(self, seed: int = 0) -> None:
        """Load a seed into the stages. O(1)."""
        if not 0 <= seed <= self.mask:
            raise ValueError("the seed must have k bits")
        self.r = seed

    def clock(self, w: int) -> None:
        """One clock with the k-bit input word w (bit i enters stage i). O(1) word operations."""
        if not 0 <= w <= self.mask:
            raise ValueError("the input word must have k bits")
        msb = (self.r >> (self.k - 1)) & 1  # @line L1
        self.r = (self.r << 1) & self.mask  # @line L2
        if msb:
            self.r ^= self.low  # @line L3
        self.r ^= w  # @line L4

    def compact(self, words: Iterable[int]) -> int:
        """Clock every word of a response stream and return the signature. O(m) for m words."""
        for w in words:
            self.clock(w)
        return self.r

    def signature(self) -> int:
        """The current contents of the register."""
        return self.r

    def check_invariant(self) -> bool:
        return 0 <= self.r <= self.mask and self.q >> self.k == 1


def signature_of(k: int, q: int, words: Iterable[int], seed: int = 0) -> int:
    """The signature of a whole stream from a seed."""
    return MISR(k, q, seed).compact(words)
