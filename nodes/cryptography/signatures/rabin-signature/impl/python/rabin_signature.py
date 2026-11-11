# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabin-signature/. The authors are listed in prov/SMWJN1.jsonl.
"""Rabin-Williams signatures with the tweaks e and f (Williams 1980,
Bernstein 2008), and the fact that two essentially different square roots of
one value factor the modulus.

The key is N = p q with p = 3 (mod 8) and q = 7 (mod 8). A signature on M is
(e, f, s) with e in {1, -1}, f in {1, 2} and e f s^2 = H(M) (mod N). The
signer picks one of the four square roots by a secret function of H(M), so a
message always gets the same root ("fixed unstructured" in Bernstein's terms).

The page is about the signature, not the hash, so the hash is built from
hashlib.sha256 and the root choice from hmac.

For study only. The code is not constant time, the toy keys come from a
seeded non-cryptographic source, and the factoring demonstration runs only
on toy keys against a local signer. Nothing here may protect real data. Use
RSA-PSS or Ed25519 from the pyca/cryptography library or from a FIPS 140
validated module.
"""

import hashlib
import hmac
import math
import random
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class PrivateKey:
    p: int
    q: int
    secret: bytes  # selects one of the four square roots for each hash value

    @property
    def n(self) -> int:
        return self.p * self.q


# Keys ------------------------------------------------------------------------

_SMALL = [p for p in range(3, 2000) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
_SMALL_PRODUCT = math.prod(_SMALL)


def _is_probable_prime(n: int, rng: random.Random, rounds: int = 20) -> bool:
    if n in _SMALL:
        return True
    if n < 3 or n % 2 == 0 or math.gcd(n, _SMALL_PRODUCT) != 1:
        return False
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


def keygen(bits: int, seed: int) -> PrivateKey:
    """A toy key from a fixed seed: p = 3 (mod 8), q = 7 (mod 8), N of `bits` binary digits."""
    rng = random.Random(seed)

    def prime(nbits: int, residue: int) -> int:
        while True:
            c = (rng.getrandbits(nbits) | (3 << (nbits - 2))) & ~7 | residue
            if _is_probable_prime(c, rng):
                return c

    while True:
        p, q = prime(bits // 2, 3), prime(bits - bits // 2, 7)
        if (p * q).bit_length() == bits:
            return PrivateKey(p, q, rng.getrandbits(256).to_bytes(32, "big"))


# Hash ------------------------------------------------------------------------

def hash_to_int(message: bytes, n: int) -> int:
    """A full-domain style hash: SHA-256 in counter mode, cut to one binary digit fewer than N."""
    nbits = n.bit_length() - 1
    out, counter = b"", 0
    while len(out) * 8 < nbits:
        out += hashlib.sha256(counter.to_bytes(4, "big") + message).digest()
        counter += 1
    return int.from_bytes(out, "big") >> (len(out) * 8 - nbits)


# Signing and verification ---------------------------------------------------

def _legendre(a: int, p: int) -> int:
    """Euler's criterion: 1 if a is a nonzero square modulo p, -1 if not, 0 if p divides a."""
    t = pow(a, (p - 1) // 2, p)
    return -1 if t == p - 1 else t


def tweaks(h: int, p: int, q: int) -> Tuple[int, int]:
    """The unique (e, f) in {1, -1} x {1, 2} such that h / (e f) is a square modulo p and q."""
    e = _legendre(h, q)  # 2 is a square modulo q = 7 (mod 8), so only e matters modulo q
    f = 1 if _legendre(h, p) * e == 1 else 2  # -1 and 2 are both non-squares modulo p = 3 (mod 8)
    return e, f


def crt(a: int, p: int, b: int, q: int) -> int:
    return (a + p * ((b - a) * pow(p, -1, q) % q)) % (p * q)


def sign_hash(key: PrivateKey, h: int, choice: Optional[int] = None) -> Tuple[int, int, int]:
    """Sign the hash value h. `choice` (0 to 3) overrides the secret root choice;
    the tests use it only to show what happens if a signer leaks two roots."""
    p, q, n = key.p, key.q, key.n
    if math.gcd(h, n) != 1:
        raise ValueError("h shares a factor with N")
    e, f = tweaks(h, p, q)  # @line L2
    hp = h * pow(e * f, -1, n) % n  # @line L3
    sp, sq = pow(hp, (p + 1) // 4, p), pow(hp, (q + 1) // 4, q)  # @line L4
    if choice is None:
        choice = hmac.new(key.secret, h.to_bytes((n.bit_length() + 7) // 8, "big"), "sha256").digest()[0] & 3  # @line L5
    if choice & 1:
        sp = p - sp  # @line L5
    if choice & 2:
        sq = q - sq  # @line L5
    s = crt(sp, p, sq, q)  # @line L6
    return e, f, s  # @line L7


def sign(key: PrivateKey, message: bytes) -> Tuple[int, int, int]:
    h = hash_to_int(message, key.n)  # @line L1
    return sign_hash(key, h)


def verify_hash(n: int, h: int, signature: Tuple[int, int, int]) -> bool:
    e, f, s = signature
    if e not in (1, -1) or f not in (1, 2) or not 0 <= s < n:  # @line L8
        return False  # @line L8
    return e * f * s * s % n == h % n  # @line L10


def verify(n: int, message: bytes, signature: Tuple[int, int, int]) -> bool:
    if signature[0] not in (1, -1) or signature[1] not in (1, 2) or not 0 <= signature[2] < n:  # @line L8
        return False  # @line L8
    h = hash_to_int(message, n)  # @line L9
    return verify_hash(n, h, signature)  # @line L10


# Two roots factor N ---------------------------------------------------------

def factor_from_two_roots(n: int, s1: int, s2: int) -> Optional[int]:
    """If s1^2 = s2^2 (mod N) and s1 is not s2 or -s2, then gcd(s1 - s2, N) is p or q."""
    if (s1 * s1 - s2 * s2) % n != 0 or s1 % n in (s2 % n, (-s2) % n):
        return None
    g = math.gcd(s1 - s2, n)
    return g if 1 < g < n else None
