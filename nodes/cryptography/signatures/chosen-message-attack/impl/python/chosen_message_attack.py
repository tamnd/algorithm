# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chosen-message-attack/. The authors are listed in prov/Z5A66M.jsonl.
"""Chosen-message attacks on textbook RSA, and the e = 3 forgery of
Bleichenbacher (2006) against a flawed PKCS #1 v1.5 verifier.

1. Textbook RSA is multiplicative: (m1 m2)^d = m1^d m2^d (mod N). Two signing
   queries give a signature on the product (a generic chosen-message attack),
   and one blinded query gives a signature on any target (a directed one).
2. A PKCS #1 v1.5 verifier that parses the block from the left and ignores the
   bytes after the hash accepts a cube that the forger computes with no key
   and no query at all. The right verifier rebuilds the whole block and
   compares; the forgery fails against it.

For study only. The code is not constant time, the attacks run only on toy
keys made from a fixed seed against the local verifiers in this file, and
nothing here may protect real data. Use RSA-PSS or Ed25519 from the
pyca/cryptography library or from a FIPS 140 validated module.
"""

import hashlib
import math
import random
from typing import Callable, List, Tuple

# RFC 8017, Section 9.2, Note 1: the DER prefix of DigestInfo for SHA-256.
SHA256_DIGEST_INFO = bytes.fromhex("3031300d060960864801650304020105000420")


# A toy RSA key ---------------------------------------------------------------

_SMALL = [p for p in range(3, 2000) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
_SMALL_PRODUCT = math.prod(_SMALL)


def _is_probable_prime(n: int, rng: random.Random, rounds: int = 16) -> bool:
    if n < 2 or n % 2 == 0 or math.gcd(n, _SMALL_PRODUCT) != 1:
        return n in (2,) or n in _SMALL
    d, a = n - 1, 0
    while d % 2 == 0:
        d, a = d // 2, a + 1
    for _ in range(rounds):
        x = pow(rng.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(a - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def toy_rsa_key(bits: int, e: int, seed: int) -> Tuple[int, int, int]:
    """Return (N, e, d) with N of exactly `bits` binary digits, from a fixed seed."""
    rng = random.Random(seed)

    def prime(nbits: int) -> int:
        while True:
            c = rng.getrandbits(nbits) | (3 << (nbits - 2)) | 1
            if (c - 1) % e and _is_probable_prime(c, rng):
                return c

    while True:
        p, q = prime(bits // 2), prime(bits - bits // 2)
        n = p * q
        if p != q and n.bit_length() == bits:
            return n, e, pow(e, -1, (p - 1) * (q - 1))


# Textbook RSA and the signing oracle ---------------------------------------

def textbook_sign(n: int, d: int, m: int) -> int:
    return pow(m, d, n)


def textbook_verify(n: int, e: int, m: int, s: int) -> bool:
    return 0 <= m < n and 0 <= s < n and pow(s, e, n) == m


class SigningOracle:
    """Signs integers with the private key and records every query."""

    def __init__(self, n: int, d: int) -> None:
        self._n, self._d = n, d
        self.queries: List[int] = []

    def __call__(self, m: int) -> int:
        self.queries.append(m)
        return textbook_sign(self._n, self._d, m)


def generic_product_forgery(n: int, oracle: Callable[[int], int], m1: int, m2: int) -> Tuple[int, int]:
    """Generic attack: the queries m1 and m2 are fixed before the key is known.
    Returns a signature on m1 m2 mod n, a message that was not queried."""
    return m1 * m2 % n, oracle(m1) * oracle(m2) % n


def directed_blinding_forgery(n: int, e: int, oracle: Callable[[int], int], target: int,
                              r: int) -> Tuple[int, int]:
    """Directed attack: one query m' = target r^e mod n, chosen after seeing (n, e).
    Then s = s' r^(-1) = target^d mod n."""
    s_blind = oracle(target * pow(r, e, n) % n)
    return target, s_blind * pow(r, -1, n) % n


# PKCS #1 v1.5 encoding with SHA-256, a right verifier, and a flawed one -------

def _k(n: int) -> int:
    return (n.bit_length() + 7) // 8


def emsa_pkcs1_v15(message: bytes, k: int) -> bytes:
    """RFC 8017, Section 9.2: 00 01 FF ... FF 00 || DigestInfo || H(M)."""
    t = SHA256_DIGEST_INFO + hashlib.sha256(message).digest()
    if k < len(t) + 11:
        raise ValueError("modulus too short")
    return b"\x00\x01" + b"\xff" * (k - len(t) - 3) + b"\x00" + t


def pkcs1_sign(n: int, d: int, message: bytes) -> int:
    return pow(int.from_bytes(emsa_pkcs1_v15(message, _k(n)), "big"), d, n)


def pkcs1_verify(n: int, e: int, message: bytes, s: int) -> bool:
    """The right check (RFC 8017, Section 8.2.2): rebuild the block and compare all of it."""
    if not 0 <= s < n:
        return False
    k = _k(n)
    return pow(s, e, n).to_bytes(k, "big") == emsa_pkcs1_v15(message, k)


def flawed_pkcs1_verify(n: int, e: int, message: bytes, s: int) -> bool:
    """A parser of the kind that Bleichenbacher attacked in 2006. It reads
    00 01, skips the FF bytes, reads 00, DigestInfo and the 32 hash bytes,
    and then stops: it does not check that the hash ends the block."""
    if not 0 <= s < n:
        return False
    em = pow(s, e, n).to_bytes(_k(n), "big")
    if em[:2] != b"\x00\x01":
        return False
    i = 2
    while i < len(em) and em[i] == 0xFF:
        i += 1
    if i == 2 or i >= len(em) or em[i] != 0:
        return False
    i += 1
    if em[i:i + len(SHA256_DIGEST_INFO)] != SHA256_DIGEST_INFO:
        return False
    i += len(SHA256_DIGEST_INFO)
    return em[i:i + 32] == hashlib.sha256(message).digest()  # the bug: em[i + 32:] is never checked


def icbrt(x: int) -> int:
    """The floor of the cube root of x >= 0, by Newton's method on integers."""
    if x < 2:
        return x
    y = 1 << ((x.bit_length() + 2) // 3)
    while True:
        z = (2 * y + x // (y * y)) // 3
        if z >= y:
            return y
        y = z


def bleichenbacher_e3_forgery(n: int, message: bytes) -> int:
    """Return s such that s^3 is an integer below n whose top bytes are
    00 01 FF 00 || DigestInfo || SHA-256(message) and whose other bytes are garbage.
    It uses only n: no private key and no signing query."""
    k = _k(n)
    prefix = b"\x00\x01\xff\x00" + SHA256_DIGEST_INFO + hashlib.sha256(message).digest()
    free = 8 * (k - len(prefix))
    low = int.from_bytes(prefix, "big") << free
    high = low + (1 << free) - 1
    s = icbrt(high)
    if s ** 3 < low:
        raise ValueError("no cube in the range; the modulus is too short for this simple variant")
    return s
