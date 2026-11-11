# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fair-coin-flipping/. The authors are listed in prov/5SB3X8.jsonl.
"""Blum's coin flip by telephone, with a hash commitment, and the abort attack.

Alice commits to a bit a with c = SHA-256(r || a). Bob answers with a bit b in
the clear. Alice opens (a, r). Both output a xor b. If Alice does not open,
Bob outputs a bit of his own choice (here a fresh random bit).

The module also computes the exact bias that an aborting Alice gets against
the protocol that runs r such flips and outputs the majority.

For study only. The code is not constant time and the parties are local
simulated objects. Use a reviewed protocol and library for real randomness
generation between parties.
"""

import hashlib
import secrets
from fractions import Fraction
from math import comb


# ------------------------------------------------------------ commitment
def commit(bit: int, r: bytes = None):
    if r is None:
        r = secrets.token_bytes(32)
    return hashlib.sha256(r + bytes([bit])).digest(), r


def check_open(c: bytes, bit: int, r: bytes) -> bool:
    return bit in (0, 1) and hashlib.sha256(r + bytes([bit])).digest() == c


# ------------------------------------------------------------ parties
class HonestAlice:
    def __init__(self, rng):
        self.rng = rng

    def first(self):
        self.a = self.rng.getrandbits(1)
        self.c, self.r = commit(self.a, self.rng.getrandbits(256).to_bytes(32, "big"))
        return self.c

    def second(self, b):
        """Return the opening (a, r), or None to abort."""
        return self.a, self.r


class AbortingAlice(HonestAlice):
    """Learns the result a xor b first and aborts if it is not her wish."""

    def __init__(self, rng, wish: int):
        super().__init__(rng)
        self.wish = wish

    def second(self, b):
        if self.a ^ b != self.wish:
            return None
        return self.a, self.r


class LyingAlice(HonestAlice):
    """Tries to open her commitment to the other bit when the result is wrong."""

    def __init__(self, rng, wish: int):
        super().__init__(rng)
        self.wish = wish

    def second(self, b):
        if self.a ^ b != self.wish:
            return 1 - self.a, self.r
        return self.a, self.r


def blum_flip(alice, rng) -> int:
    """Run one flip; Bob is honest. Return the bit Bob outputs."""
    c = alice.first()                       # @line L1
    b = rng.getrandbits(1)                  # @line L2
    opening = alice.second(b)               # @line L3
    if opening is None:                     # @line L4
        return rng.getrandbits(1)           # @line L5
    a, r = opening
    if not check_open(c, a, r):             # @line L6
        return rng.getrandbits(1)           # Bob treats a bad opening as an abort
    return a ^ b                            # @line L7


def no_commitment_flip(alice_bit: int, bob_wish: int) -> int:
    """The broken protocol: Alice sends a in the clear, Bob then picks b."""
    b = alice_bit ^ bob_wish
    return alice_bit ^ b


# ------------------------------------------------------------ majority of r flips
def majority_attack_value(r: int) -> Fraction:
    """Exact Pr[output = 1] when Alice aborts at most once, optimally.

    The protocol runs r Blum flips (r odd) and outputs the majority. Alice
    learns each coin before Bob. If she aborts in round i, Bob tosses the
    coins i..r himself and outputs the majority. Dynamic programming over
    (round, number of ones so far).
    """
    if r % 2 == 0:
        raise ValueError("r must be odd")
    need = (r + 1) // 2

    def tail(k: int, s: int) -> Fraction:
        # Pr[s + Binomial(k, 1/2) >= need]
        good = sum(comb(k, j) for j in range(k + 1) if s + j >= need)
        return Fraction(good, 2 ** k)

    value = [Fraction(1 if s >= need else 0) for s in range(r + 1)]
    for i in range(r, 0, -1):          # round i, with i - 1 coins already fixed
        new = []
        for s in range(i):
            abort = tail(r - i + 1, s)
            cont0 = value[s]
            cont1 = value[s + 1]
            new.append((max(cont0, abort) + max(cont1, abort)) / 2)
        value = new
    return value[0]
