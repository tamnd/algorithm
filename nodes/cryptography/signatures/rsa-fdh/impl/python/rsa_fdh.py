# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-fdh/. The authors are listed in prov/0866Z3.jsonl.
"""RSA full-domain hash signatures (Bellare and Rogaway 1993, 1996).

The full-domain hash is H_FDH(M) = OS2IP(MGF1-SHA-256(M, k + 16)) mod N: the
mask generation function MGF1 of RFC 8017 Appendix B.2.1, with SHA-256 and the
message as its seed, stretched to 16 bytes more than the modulus and reduced
mod N. The extra 128 bits make the result statistically close (distance at
most 2^-128) to uniform on Z_N. This choice of hash is ours: no standard fixes
a full-domain hash for RSA-FDH, and there are no official test vectors.

The file also contains Coron's reduction (CRYPTO 2000) as code, so that the
tests can run the proof on a toy forger.

For study only. The code is not constant time, the key generator uses a
seeded non-cryptographic random source, and the code must not protect real
data. Use RSA-PSS from the pyca/cryptography library or from a FIPS 140
validated module instead.
"""

import hashlib
import math
import random
from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class PrivateKey:
    n: int
    e: int
    d: int
    p: int
    q: int


def byte_length(n: int) -> int:
    return (n.bit_length() + 7) // 8


def mgf1(seed: bytes, length: int, hash_name: str = "sha256") -> bytes:
    """MGF1 of RFC 8017 Appendix B.2.1."""
    out = bytearray()
    counter = 0
    while len(out) < length:
        out += hashlib.new(hash_name, seed + counter.to_bytes(4, "big")).digest()
        counter += 1
    return bytes(out[:length])


def fdh_hash(n: int, message: bytes) -> int:
    """H_FDH(M) in Z_N, from MGF1-SHA-256 with 16 extra bytes."""
    k = byte_length(n)
    return int.from_bytes(mgf1(message, k + 16), "big") % n  # @line L2


def sign(key: PrivateKey, message: bytes) -> bytes:
    k = byte_length(key.n)  # @line L1
    y = fdh_hash(key.n, message)  # @line L2
    s1 = pow(y, key.d % (key.p - 1), key.p)  # @line L3
    s2 = pow(y, key.d % (key.q - 1), key.q)  # @line L3
    s = s2 + key.q * ((pow(key.q, -1, key.p) * (s1 - s2)) % key.p)  # @line L3
    return s.to_bytes(k, "big")  # @line L4


def verify(n: int, e: int, message: bytes, signature: bytes) -> bool:
    k = byte_length(n)
    if len(signature) != k:  # @line L5
        return False  # @line L5
    s = int.from_bytes(signature, "big")
    if s >= n:  # @line L5
        return False  # @line L5
    return pow(s, e, n) == fdh_hash(n, message)  # @line L6


def _is_probable_prime(n: int, rng: random.Random, rounds: int = 32) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(rounds):
        x = pow(rng.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_key(bits: int = 1024, e: int = 65537, seed: int = 0) -> PrivateKey:
    """A toy key from a seeded random source (not FIPS 186-5 Appendix A.1)."""
    rng = random.Random(seed)

    def prime(nbits: int) -> int:
        while True:
            c = rng.getrandbits(nbits) | (3 << (nbits - 2)) | 1
            if math.gcd(c - 1, e) == 1 and _is_probable_prime(c, rng):
                return c

    while True:
        p, q = prime(bits // 2), prime(bits - bits // 2)
        if p != q and (p * q).bit_length() == bits:
            break
    d = pow(e, -1, (p - 1) * (q - 1) // math.gcd(p - 1, q - 1))
    return PrivateKey(p * q, e, d, p, q)


class Abort(Exception):
    """The reduction cannot answer a signing query and gives up."""


@dataclass
class CoronReduction:
    """Coron's inverter I: it gets (N, e, y) and simulates the random oracle
    and the signing oracle for a forger, without the private key.

    Each new hash query m gets a random r in Z_N^*; with probability p_zero
    the answer is r^e (type 0, signable), else y * r^e (type 1, useful).
    """

    n: int
    e: int
    y: int
    p_zero: float
    rng: random.Random
    table: Dict[bytes, Tuple[int, int, int]] = field(default_factory=dict)

    def hash(self, m: bytes) -> int:
        if m not in self.table:
            while True:
                r = self.rng.randrange(1, self.n)
                if math.gcd(r, self.n) == 1:
                    break
                # A non-unit r would factor N; it has negligible probability.
            kind = 0 if self.rng.random() < self.p_zero else 1
            h = pow(r, self.e, self.n) if kind == 0 else self.y * pow(r, self.e, self.n) % self.n
            self.table[m] = (h, r, kind)
        return self.table[m][0]

    def sign(self, m: bytes) -> int:
        self.hash(m)
        _, r, kind = self.table[m]
        if kind == 1:
            raise Abort
        return r

    def extract(self, m_star: bytes, sigma_star: int) -> int:
        """From a forgery on a type-1 message, return x with x^e = y mod N."""
        self.hash(m_star)
        h, r, kind = self.table[m_star]
        if kind == 0 or pow(sigma_star, self.e, self.n) != h:
            raise Abort
        return sigma_star * pow(r, -1, self.n) % self.n


def coron_optimal_p(q_s: int) -> float:
    """The p that maximizes p^q_s (1 - p): p = q_s / (q_s + 1)."""
    return q_s / (q_s + 1)
