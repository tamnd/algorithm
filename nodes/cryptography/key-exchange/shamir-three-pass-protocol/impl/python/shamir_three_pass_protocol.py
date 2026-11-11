# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shamir-three-pass-protocol/. The authors are listed in prov/76HQ6M.jsonl.
"""Shamir's three-pass protocol with the Massey-Omura exponent cipher.

Alice sends a secret m to Bob, and the two share no key. Each party has a
private exponent that is a unit mod p - 1. The cipher E_a(x) = x^a mod p
commutes: E_a(E_b(x)) = E_b(E_a(x)). So Alice locks m, Bob adds his lock,
Alice takes hers off, and Bob takes his off.

The prime is the 2048-bit safe prime of RFC 3526 Section 3. The module
also has the XOR version of the same three passes, which is broken: the
XOR of the three messages is m.

For study only. The code is not constant time, and the protocol has no
authentication: anyone who answers the first message can read m. Do not
use it to protect real data. Use an authenticated key exchange and an AEAD
from libsodium or the Python package cryptography instead.

Cost: three exponentiations mod p in the protocol, plus one modular
inverse per party, each O(m^3) bit operations with schoolbook arithmetic
for an m-bit prime.
"""

import math
import random
import secrets
from typing import Optional

# RFC 3526 Section 3, the 2048-bit MODP prime, copied by hand.
P = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74"
    "020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F1437"
    "4FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF05"
    "98DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB"
    "9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF695581718"
    "3995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF",
    16,
)


def make_lock(p: int = P, rng: Optional[random.Random] = None) -> tuple[int, int]:
    """A private exponent a with gcd(a, p - 1) = 1 and its inverse a' mod p - 1."""
    r = rng or secrets.SystemRandom()
    while True:
        a = r.randrange(3, p - 1)  # @line L2
        if math.gcd(a, p - 1) == 1:
            return a, pow(a, -1, p - 1)  # @line L3


def lock(x: int, e: int, p: int = P) -> int:
    """The Massey-Omura cipher x^e mod p (also used to unlock with the inverse exponent)."""
    return pow(x, e, p)


def three_pass(m: int, alice: tuple[int, int], bob: tuple[int, int], p: int = P) -> tuple[list[int], int]:
    """Run the three passes. Return the three messages on the wire and Bob's result."""
    if not 2 <= m <= p - 2:  # @line L1
        raise ValueError("the message must lie in [2, p - 2]")
    a, a_inv = alice
    b, b_inv = bob
    c1 = lock(m, a, p)  # @line L4
    c2 = lock(c1, b, p)  # @line L5
    c3 = lock(c2, a_inv, p)  # @line L6
    out = lock(c3, b_inv, p)  # @line L7
    return [c1, c2, c3], out


def legendre(x: int, p: int = P) -> int:
    """The Legendre symbol of x mod p, as 1, -1 or 0 (Euler's criterion)."""
    t = pow(x, (p - 1) // 2, p)
    return -1 if t == p - 1 else t


def xor_three_pass(m: bytes, ka: bytes, kb: bytes) -> list[bytes]:
    """The broken XOR version: c1 = m ^ ka, c2 = c1 ^ kb, c3 = c2 ^ ka."""
    if not len(m) == len(ka) == len(kb):
        raise ValueError("the pads must have the length of the message")
    c1 = bytes(x ^ y for x, y in zip(m, ka))
    c2 = bytes(x ^ y for x, y in zip(c1, kb))
    c3 = bytes(x ^ y for x, y in zip(c2, ka))
    return [c1, c2, c3]


def xor_eavesdrop(wire: list[bytes]) -> bytes:
    """c1 ^ c2 ^ c3 = (m ^ ka) ^ (m ^ ka ^ kb) ^ (m ^ kb) = m."""
    c1, c2, c3 = wire
    return bytes(x ^ y ^ z for x, y, z in zip(c1, c2, c3))
