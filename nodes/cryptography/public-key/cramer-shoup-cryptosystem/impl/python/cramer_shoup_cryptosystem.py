# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cramer-shoup-cryptosystem/. The authors are listed in prov/DP6M6E.jsonl.
"""The Cramer-Shoup cryptosystem (1998) in the squares modulo a safe prime.

Public key: g1, g2, c = g1^x1 g2^x2, d = g1^y1 g2^y2, h = g1^z.
Ciphertext: (u1, u2, e, v) = (g1^r, g2^r, h^r m, c^r d^(r a)) with
a = H(u1, u2, e). Decryption rejects unless v = u1^(x1 + y1 a) u2^(x2 + y2 a).

H is SHA-256 reduced modulo q. The security proof needs H to be target
collision resistant; for SHA-256 that is an assumption.

For study only. This code is not constant time, and the default group (a
safe prime of 64 binary digits) is far too small for real use.
"""

import hashlib
import random
import secrets
from dataclasses import dataclass


@dataclass(frozen=True)
class Group:
    p: int  # a safe prime p = 2q + 1
    q: int  # the prime order of the group of squares modulo p
    g1: int
    g2: int


def _hash_to_square(p: int, label: bytes) -> int:
    h = int.from_bytes(hashlib.sha256(label).digest(), "big") % p
    return h * h % p


P_TOY = 9223372036854778487  # the smallest safe prime above 2^63
TOY = Group(P_TOY, (P_TOY - 1) // 2, 4, _hash_to_square(P_TOY, b"Cramer-Shoup g2"))


@dataclass(frozen=True)
class PublicKey:
    group: Group
    c: int
    d: int
    h: int


@dataclass(frozen=True)
class PrivateKey:
    group: Group
    x1: int
    x2: int
    y1: int
    y2: int
    z: int


Ciphertext = tuple[int, int, int, int]


def _rand(q: int, rng: random.Random | None) -> int:
    return rng.randrange(q) if rng is not None else secrets.randbelow(q)


def in_group(grp: Group, a: int) -> bool:
    """Membership in the order-q subgroup: 0 < a < p and a^q = 1. Cost: one exponentiation."""
    return 0 < a < grp.p and pow(a, grp.q, grp.p) == 1


def tcr_hash(grp: Group, u1: int, u2: int, e: int) -> int:
    """alpha = SHA-256(u1 || u2 || e) mod q, with fixed-length encodings."""
    n = (grp.p.bit_length() + 7) // 8
    data = b"".join(x.to_bytes(n, "big") for x in (u1, u2, e))
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % grp.q


def keygen(grp: Group = TOY, rng: random.Random | None = None) -> tuple[PublicKey, PrivateKey]:
    """Five random exponents and five exponentiations. Cost: Θ(b^3) for b-digit p."""
    p = grp.p
    x1, x2, y1, y2, z = (_rand(grp.q, rng) for _ in range(5))  # @line L1
    c = pow(grp.g1, x1, p) * pow(grp.g2, x2, p) % p  # @line L2
    d = pow(grp.g1, y1, p) * pow(grp.g2, y2, p) % p
    h = pow(grp.g1, z, p)
    return PublicKey(grp, c, d, h), PrivateKey(grp, x1, x2, y1, y2, z)  # @line L3


def encrypt(pk: PublicKey, m: int, rng: random.Random | None = None) -> Ciphertext:
    """Encrypt a group element m. Cost: five exponentiations, Θ(b^3)."""
    grp = pk.group
    p = grp.p
    if not in_group(grp, m):
        raise ValueError("the message must be an element of the group; use encode()")
    r = _rand(grp.q, rng)  # @line L4
    u1, u2 = pow(grp.g1, r, p), pow(grp.g2, r, p)  # @line L5
    e = pow(pk.h, r, p) * m % p  # @line L6
    alpha = tcr_hash(grp, u1, u2, e)  # @line L7
    v = pow(pk.c, r, p) * pow(pk.d, r * alpha % grp.q, p) % p  # @line L8
    return u1, u2, e, v  # @line L9


def decrypt(sk: PrivateKey, ct: Ciphertext) -> int | None:
    """Return the message, or None for a rejected ciphertext. Cost: Θ(b^3)."""
    grp = sk.group
    p, q = grp.p, grp.q
    u1, u2, e, v = ct
    if not all(in_group(grp, a) for a in ct):  # @line L10
        return None
    alpha = tcr_hash(grp, u1, u2, e)  # @line L11
    check = pow(u1, (sk.x1 + sk.y1 * alpha) % q, p) * pow(u2, (sk.x2 + sk.y2 * alpha) % q, p) % p
    if check != v:  # @line L12
        return None
    return e * pow(u1, (q - sk.z) % q, p) % p  # @line L13


def encode(grp: Group, m: int) -> int:
    """Map 1 <= m <= q to a square modulo p (p = 3 mod 4): m or p - m."""
    if not 1 <= m <= grp.q:
        raise ValueError("message out of range")
    return m if pow(m, grp.q, grp.p) == 1 else grp.p - m


def decode(grp: Group, a: int) -> int:
    """The inverse of encode."""
    return min(a, grp.p - a)
