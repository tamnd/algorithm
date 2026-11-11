# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dsa/. The authors are listed in prov/J4WE85.jsonl.
"""The Digital Signature Algorithm of FIPS 186-4: domain parameters by
Appendix A.1.1.2 (p and q from an approved hash), A.1.1.3 (their validation)
and A.2.1 (unverifiable generator g); key pairs by Appendix B.1; signing and
verification by Sections 4.6 and 4.7.

FIPS 186-5 (February 2023) no longer approves DSA for signature generation and
keeps it only to verify old signatures. The page is about DSA, not the hash,
so the hash comes from hashlib.

For study only. The code is not constant time, and the random choices in the
parameter generator use a seeded non-cryptographic source unless secrets is
used. It must not protect real data. Use ECDSA or EdDSA from the
pyca/cryptography library or from a FIPS 140 validated module.
"""

import hashlib
import math
import random
import secrets
from dataclasses import dataclass
from typing import Optional, Tuple

APPROVED_LN = {(1024, 160), (2048, 224), (2048, 256), (3072, 256)}  # FIPS 186-4 Section 4.2


@dataclass(frozen=True)
class Params:
    p: int
    q: int
    g: int


def _small_primes(limit: int) -> list:
    sieve = bytearray([1]) * limit
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(limit) if sieve[i]]


_SMALL = _small_primes(2000)
_SMALL_PRODUCT = math.prod(_SMALL)


def is_probable_prime(n: int, rounds: int, rng: random.Random) -> bool:
    """Miller-Rabin (FIPS 186-4 Appendix C.3.1) after trial division."""
    if n < 2:
        return False
    if n <= _SMALL[-1]:
        return n in _SMALL
    if math.gcd(n, _SMALL_PRODUCT) != 1:
        return False
    d, a = n - 1, 0
    while d % 2 == 0:
        d //= 2
        a += 1
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


def _hash_int(data: int, seedlen: int, hash_name: str) -> int:
    return int.from_bytes(hashlib.new(hash_name, data.to_bytes(seedlen // 8, "big")).digest(), "big")


def _p_candidate(seed: int, offset: int, L: int, seedlen: int, n: int, b: int, outlen: int,
                 hash_name: str) -> int:
    w = 0
    for j in range(n + 1):  # steps 11.1 and 11.2
        v = _hash_int((seed + offset + j) % (1 << seedlen), seedlen, hash_name)
        if j == n:
            v %= 1 << b
        w += v << (j * outlen)
    return w + (1 << (L - 1))  # step 11.3, X


def generate_pq(L: int, N: int, seedlen: Optional[int] = None, hash_name: str = "sha256",
                rng: Optional[random.Random] = None, rounds: int = 40,
                allow_unapproved: bool = False) -> Tuple[int, int, int, int]:
    """FIPS 186-4 Appendix A.1.1.2. Returns (p, q, domain_parameter_seed, counter)."""
    if (L, N) not in APPROVED_LN and not allow_unapproved:
        raise ValueError("(L, N) is not an approved pair")
    outlen = hashlib.new(hash_name).digest_size * 8
    seedlen = seedlen or N
    if seedlen < N or outlen < N or seedlen % 8:
        raise ValueError("bad seedlen or hash")
    rng = rng or random.Random(secrets.randbits(64))
    n = -(-L // outlen) - 1  # step 3
    b = L - 1 - n * outlen  # step 4
    while True:
        seed = rng.getrandbits(seedlen) | (1 << (seedlen - 1))  # step 5
        u = _hash_int(seed, seedlen, hash_name) % (1 << (N - 1))  # step 6
        q = (1 << (N - 1)) + u + 1 - (u % 2)  # step 7
        if not is_probable_prime(q, rounds, rng):  # steps 8 and 9
            continue
        offset = 1  # step 10
        for counter in range(4 * L):  # step 11
            x = _p_candidate(seed, offset, L, seedlen, n, b, outlen, hash_name)
            c = x % (2 * q)  # step 11.4
            p = x - (c - 1)  # step 11.5
            if p >= 1 << (L - 1) and is_probable_prime(p, rounds, rng):  # steps 11.6 to 11.8
                return p, q, seed, counter
            offset += n + 1  # step 11.9


def validate_pq(p: int, q: int, seed: int, counter: int, seedlen: int, hash_name: str = "sha256",
                rounds: int = 40, rng: Optional[random.Random] = None) -> bool:
    """FIPS 186-4 Appendix A.1.1.3: recompute q and p from the seed and the counter."""
    rng = rng or random.Random(0)
    L, N = p.bit_length(), q.bit_length()
    outlen = hashlib.new(hash_name).digest_size * 8
    if seedlen < N or counter > 4 * L - 1 or seed.bit_length() > seedlen:
        return False
    u = _hash_int(seed, seedlen, hash_name) % (1 << (N - 1))
    if q != (1 << (N - 1)) + u + 1 - (u % 2) or not is_probable_prime(q, rounds, rng):
        return False
    n = -(-L // outlen) - 1
    b = L - 1 - n * outlen
    offset = 1
    for i in range(counter + 1):
        x = _p_candidate(seed, offset, L, seedlen, n, b, outlen, hash_name)
        cand = x - (x % (2 * q) - 1)
        if i < counter and cand >= 1 << (L - 1) and is_probable_prime(cand, rounds, rng):
            return False  # an earlier counter value would have given a prime
        offset += n + 1
    return cand == p and cand >= 1 << (L - 1) and is_probable_prime(p, rounds, rng)


def generate_g(p: int, q: int) -> int:
    """FIPS 186-4 Appendix A.2.1: g = h^((p-1)/q) mod p for the first h > 1 with g != 1."""
    e = (p - 1) // q
    for h in range(2, p - 1):
        g = pow(h, e, p)
        if g != 1:
            return g
    raise ValueError("no generator")


def keygen(params: Params, rng: Optional[random.Random] = None) -> Tuple[int, int]:
    """Appendix B.1: x uniform in [1, q - 1], y = g^x mod p."""
    x = rng.randrange(1, params.q) if rng else 1 + secrets.randbelow(params.q - 1)
    return x, pow(params.g, x, params.p)


def message_representative(message: bytes, q: int, hash_name: str) -> int:
    """z = the leftmost min(N, outlen) binary digits of Hash(M), Section 4.6."""
    digest = hashlib.new(hash_name, message).digest()
    outlen, n_bits = len(digest) * 8, q.bit_length()
    z = int.from_bytes(digest, "big")
    if outlen > n_bits:
        z >>= outlen - n_bits
    return z


def sign(params: Params, x: int, message: bytes, hash_name: str = "sha256",
         k: Optional[int] = None) -> Tuple[int, int]:
    """FIPS 186-4 Section 4.6. A given k is used as is (for the RFC 6979 vectors);
    otherwise a fresh k is drawn uniformly from [1, q - 1] for each signature."""
    p, q, g = params.p, params.q, params.g
    z = message_representative(message, q, hash_name)  # @line L1
    while True:
        kk = k if k is not None else 1 + secrets.randbelow(q - 1)  # @line L2
        r = pow(g, kk, p) % q  # @line L3
        s = pow(kk, -1, q) * (z + x * r) % q  # @line L4
        if r != 0 and s != 0:  # @line L5
            return r, s  # @line L6
        if k is not None:
            raise ValueError("r = 0 or s = 0 for this k")


def verify(params: Params, y: int, message: bytes, signature: Tuple[int, int],
           hash_name: str = "sha256") -> bool:
    """FIPS 186-4 Section 4.7."""
    p, q, g = params.p, params.q, params.g
    r, s = signature
    if not (0 < r < q and 0 < s < q):  # @line L7
        return False  # @line L7
    w = pow(s, -1, q)  # @line L8
    z = message_representative(message, q, hash_name)  # @line L9
    u1, u2 = z * w % q, r * w % q  # @line L10
    v = pow(g, u1, p) * pow(y, u2, p) % p % q  # @line L11
    return v == r  # @line L12
