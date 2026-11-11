# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elgamal-signature/. The authors are listed in prov/D1G2DP.jsonl.
"""The ElGamal signature scheme (ElGamal 1985; HAC Algorithms 11.63 and 11.64)
in the multiplicative group of integers modulo a prime p.

The hash h maps a message to Z_{p-1}. The page is about the signature, not
the hash, so sign_message and verify_message take SHA-256 from hashlib and
reduce it modulo p - 1; sign and verify take the hash value as an integer.

For study only. The code is not constant time, the group generator uses a
seeded non-cryptographic random source, and the code must not protect real
data. ElGamal signatures are not standardized; use Ed25519 or ECDSA from the
pyca/cryptography library or from a FIPS 140 validated module.
"""

import hashlib
import math
import random
import secrets
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Group:
    p: int  # a prime
    g: int  # a generator of the multiplicative group modulo p


def keygen(group: Group, rng: Optional[random.Random] = None) -> Tuple[int, int]:
    """Return (x, y) with x the private key and y = g^x mod p the public key."""
    p, g = group.p, group.g
    x = (rng.randrange(1, p - 1) if rng else 1 + secrets.randbelow(p - 2))  # @line L1
    y = pow(g, x, p)  # @line L2
    return x, y


def hash_to_exponent(group: Group, message: bytes) -> int:
    """h(m) = SHA-256(m) as an integer, reduced modulo p - 1."""
    return int.from_bytes(hashlib.sha256(message).digest(), "big") % (group.p - 1)


def sign(group: Group, x: int, h: int, k: Optional[int] = None,
         rng: Optional[random.Random] = None) -> Tuple[int, int]:
    """Sign the hash value h. A given k is used as is (for the worked example
    and the k reuse test); otherwise a fresh k is drawn for each signature."""
    p, g = group.p, group.g
    h %= p - 1  # @line L3
    while True:
        if k is None:
            kk = rng.randrange(1, p - 1) if rng else 1 + secrets.randbelow(p - 2)  # @line L4
        else:
            kk = k
        if math.gcd(kk, p - 1) != 1:  # @line L4
            if k is not None:
                raise ValueError("k must be coprime to p - 1")
            continue
        r = pow(g, kk, p)  # @line L5
        s = pow(kk, -1, p - 1) * (h - x * r) % (p - 1)  # @line L6
        if s == 0:  # @line L7
            if k is not None:
                raise ValueError("s = 0 for this k")
            continue
        return r, s  # @line L8


def verify(group: Group, y: int, h: int, signature: Tuple[int, int]) -> bool:
    p, g = group.p, group.g
    r, s = signature
    if not (1 <= r <= p - 1 and 1 <= s <= p - 2):  # @line L9
        return False  # @line L9
    h %= p - 1  # @line L10
    return pow(g, h, p) == pow(y, r, p) * pow(r, s, p) % p  # @line L11


def sign_message(group: Group, x: int, message: bytes, rng: Optional[random.Random] = None) -> Tuple[int, int]:
    return sign(group, x, hash_to_exponent(group, message), rng=rng)


def verify_message(group: Group, y: int, message: bytes, signature: Tuple[int, int]) -> bool:
    return verify(group, y, hash_to_exponent(group, message), signature)


def solve_linear_congruence(a: int, b: int, m: int) -> list:
    """All z in [0, m) with a*z = b (mod m)."""
    a, b = a % m, b % m
    d = math.gcd(a, m)
    if b % d:
        return []
    m1 = m // d
    z0 = (b // d) * pow(a // d, -1, m1) % m1 if m1 > 1 else 0
    return [z0 + i * m1 for i in range(d)]


def recover_key_from_reused_k(group: Group, y: int, h1: int, sig1: Tuple[int, int],
                              h2: int, sig2: Tuple[int, int]) -> Optional[int]:
    """HAC Note 11.66(ii). Two signatures with the same r (the same k) give
    (s1 - s2) k = h1 - h2 (mod p - 1), then x r = h1 - k s1 (mod p - 1).
    Each candidate is checked against r = g^k and y = g^x."""
    p, g = group.p, group.g
    (r1, s1), (r2, s2) = sig1, sig2
    if r1 != r2:
        return None
    for k in solve_linear_congruence(s1 - s2, h1 - h2, p - 1):
        if pow(g, k, p) != r1:
            continue
        for x in solve_linear_congruence(r1, h1 - k * s1, p - 1):
            if pow(g, x, p) == y:
                return x
    return None


def _is_probable_prime(n: int, rng: random.Random, rounds: int = 32) -> bool:
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(rounds):
        a = pow(rng.randrange(2, n - 1), d, n)
        if a in (1, n - 1):
            continue
        for _ in range(r - 1):
            a = a * a % n
            if a == n - 1:
                break
        else:
            return False
    return True


def toy_group(bits: int = 128, seed: int = 0) -> Group:
    """A safe prime p = 2q + 1 with q prime and the smallest generator g of
    Z_p^*, from a seeded random source. Toy size, not FIPS 186 parameters.
    A safe prime has p = 3 (mod 4), which avoids Bleichenbacher's weak case."""
    rng = random.Random(seed)
    while True:
        q = rng.getrandbits(bits - 1) | (1 << (bits - 2)) | 1
        if q % 3 != 2:  # p = 2q + 1 is divisible by 3 when q = 1 (mod 3)
            continue
        if _is_probable_prime(q, rng, 8) and _is_probable_prime(2 * q + 1, rng, 8):
            p = 2 * q + 1
            break
    g = 2
    while pow(g, 2, p) == 1 or pow(g, q, p) == 1:
        g += 1
    return Group(p, g)
