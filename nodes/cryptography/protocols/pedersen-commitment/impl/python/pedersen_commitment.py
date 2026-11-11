# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pedersen-commitment/. The authors are listed in prov/VBNYFB.jsonl.
"""Pedersen commitments C = g^m h^r in the prime order subgroup of a safe prime group.

The group is the subgroup of squares in Z_p^* for a safe prime p = 2q + 1.
It has prime order q. The second generator h comes from hashing a public seed
to the group, so nobody knows log_g h. The vector form commits to (m_1..m_n)
as g_1^m_1 ... g_n^m_n h^r.

For study only. The code is not constant time and the groups here are far too
small for real use. Use a reviewed library (for example libsodium's Ristretto255
group) or a FIPS 140 validated module for real data.
"""

import hashlib
import secrets


class Group:
    """The subgroup of order q of Z_p^*, for a safe prime p = 2q + 1."""

    def __init__(self, p: int):
        self.p = p
        self.q = (p - 1) // 2
        self.g = self.hash_to_group(b"generator g")  # @line L1

    def hash_to_group(self, seed: bytes) -> int:
        """Map a seed to a square mod p other than 1. Its log base g is unknown."""
        ctr = 0
        while True:
            d = hashlib.sha256(seed + ctr.to_bytes(4, "big")).digest()
            x = int.from_bytes(d, "big") % self.p
            h = x * x % self.p
            if h not in (0, 1):
                return h
            ctr += 1

    def is_element(self, a: int) -> bool:
        """True if a is in the subgroup of order q."""
        return 0 < a < self.p and pow(a, self.q, self.p) == 1


# p = 2039 = 2 * 1019 + 1: small enough to enumerate in the tests.
TOY = Group(2039)
# A 128-bit safe prime: q = 2^126 + 1 + 2k is the first prime with 2q + 1 prime.
P128 = 170141183460469231731687303715884114527
MEDIUM = Group(P128)


class Pedersen:
    """Commitments g^m h^r to messages m in Z_q."""

    def __init__(self, group: Group, h: int = None):
        self.G = group
        self.h = group.hash_to_group(b"generator h") if h is None else h  # @line L2

    def commit(self, m: int, r: int = None):
        """Return (C, r)."""
        q = self.G.q
        if r is None:
            r = secrets.randbelow(q)
        c = pow(self.G.g, m % q, self.G.p) * pow(self.h, r % q, self.G.p) % self.G.p  # @line L3
        return c, r

    def open(self, c: int, m: int, r: int) -> bool:
        p = self.G.p
        if not 0 < c < p:  # @line L4
            return False
        if pow(c, self.G.q, p) != 1:  # @line L5
            return False
        return self.commit(m, r)[0] == c  # @line L6

    def add(self, c1: int, c2: int) -> int:
        """Commit(m1, r1) * Commit(m2, r2) = Commit(m1 + m2, r1 + r2)."""
        return c1 * c2 % self.G.p


def equivocate(q: int, trapdoor: int, m: int, r: int, m_new: int) -> int:
    """With t = log_g h, return r' such that g^m_new h^r' = g^m h^r.

    m + t r = m_new + t r' (mod q), so r' = r + (m - m_new) / t.
    """
    return (r + (m - m_new) * pow(trapdoor, -1, q)) % q


def dlog_from_two_openings(q: int, m1: int, r1: int, m2: int, r2: int) -> int:
    """Two openings of one commitment give log_g h = (m1 - m2) / (r2 - r1) mod q."""
    return (m1 - m2) * pow(r2 - r1, -1, q) % q


class VectorPedersen:
    """C = g_1^m_1 ... g_n^m_n h^r with independent generators from hashing."""

    def __init__(self, group: Group, n: int):
        self.G = group
        self.gens = [group.hash_to_group(b"vector g" + i.to_bytes(4, "big")) for i in range(n)]
        self.h = group.hash_to_group(b"vector h")

    def commit(self, ms, r: int = None):
        if len(ms) != len(self.gens):
            raise ValueError("wrong vector length")
        p, q = self.G.p, self.G.q
        if r is None:
            r = secrets.randbelow(q)
        c = pow(self.h, r, p)
        for gi, mi in zip(self.gens, ms):
            c = c * pow(gi, mi % q, p) % p
        return c, r

    def open(self, c: int, ms, r: int) -> bool:
        return self.G.is_element(c) and self.commit(ms, r)[0] == c
