# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-pss/. The authors are listed in prov/CWNPMK.jsonl.
"""RSASSA-PSS of RFC 8017 Section 8.1, with the EMSA-PSS encoding of Section 9.1
and the mask generation function MGF1 of Appendix B.2.1.

The page is about the signature, not the hash, so the hash comes from hashlib.
MGF1 uses the same hash as the message, as RFC 8017 recommends.

For study only. The code is not constant time, the key generator uses a
seeded non-cryptographic random source, and the code must not protect real
data. Use the pyca/cryptography library or a FIPS 140 validated module.
"""

import hashlib
import math
import random
import secrets
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PrivateKey:
    n: int
    e: int
    d: int
    p: int
    q: int


def mgf1(seed: bytes, length: int, hash_name: str) -> bytes:
    """MGF1 of RFC 8017 Appendix B.2.1."""
    out = bytearray()
    counter = 0
    while len(out) < length:
        out += hashlib.new(hash_name, seed + counter.to_bytes(4, "big")).digest()
        counter += 1
    return bytes(out[:length])


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def emsa_pss_encode(message: bytes, em_bits: int, hash_name: str = "sha256",
                    s_len: Optional[int] = None, salt: Optional[bytes] = None) -> bytes:
    """EMSA-PSS-ENCODE of RFC 8017 Section 9.1.1. A given salt is used as is
    (for test vectors); otherwise a fresh salt of s_len bytes is drawn."""
    h_len = hashlib.new(hash_name).digest_size
    if s_len is None:
        s_len = h_len if salt is None else len(salt)
    em_len = (em_bits + 7) // 8
    m_hash = hashlib.new(hash_name, message).digest()  # @line L1
    if em_len < h_len + s_len + 2:  # @line L2
        raise ValueError("encoding error")  # @line L2
    if salt is None:
        salt = secrets.token_bytes(s_len)  # @line L3
    if len(salt) != s_len:
        raise ValueError("salt length mismatch")
    m_prime = b"\x00" * 8 + m_hash + salt  # @line L4
    h = hashlib.new(hash_name, m_prime).digest()  # @line L5
    db = b"\x00" * (em_len - s_len - h_len - 2) + b"\x01" + salt  # @line L6
    masked_db = bytearray(_xor(db, mgf1(h, em_len - h_len - 1, hash_name)))  # @line L7
    masked_db[0] &= 0xFF >> (8 * em_len - em_bits)  # @line L8
    return bytes(masked_db) + h + b"\xbc"  # @line L9


def emsa_pss_verify(message: bytes, em: bytes, em_bits: int, hash_name: str = "sha256",
                    s_len: Optional[int] = None) -> bool:
    """EMSA-PSS-VERIFY of RFC 8017 Section 9.1.2."""
    h_len = hashlib.new(hash_name).digest_size
    if s_len is None:
        s_len = h_len
    em_len = (em_bits + 7) // 8
    if len(em) != em_len:
        return False
    m_hash = hashlib.new(hash_name, message).digest()
    if em_len < h_len + s_len + 2 or em[-1] != 0xBC:  # @line L13
        return False  # @line L13
    masked_db, h = em[: em_len - h_len - 1], em[em_len - h_len - 1: -1]  # @line L14
    top = 8 * em_len - em_bits
    if top and masked_db[0] >> (8 - top):  # @line L14
        return False  # @line L14
    db = bytearray(_xor(masked_db, mgf1(h, em_len - h_len - 1, hash_name)))  # @line L15
    db[0] &= 0xFF >> top  # @line L15
    pad = em_len - h_len - s_len - 2
    if any(db[:pad]) or db[pad] != 0x01:  # @line L16
        return False  # @line L16
    salt = bytes(db[len(db) - s_len:]) if s_len else b""  # @line L17
    h2 = hashlib.new(hash_name, b"\x00" * 8 + m_hash + salt).digest()  # @line L17
    return h == h2  # @line L18


def sign(key: PrivateKey, message: bytes, hash_name: str = "sha256",
         s_len: Optional[int] = None, salt: Optional[bytes] = None) -> bytes:
    """RSASSA-PSS-SIGN of RFC 8017 Section 8.1.1."""
    mod_bits = key.n.bit_length()
    k = (mod_bits + 7) // 8
    em = emsa_pss_encode(message, mod_bits - 1, hash_name, s_len, salt)
    m = int.from_bytes(em, "big")
    s1 = pow(m, key.d % (key.p - 1), key.p)  # @line L10
    s2 = pow(m, key.d % (key.q - 1), key.q)  # @line L10
    s = s2 + key.q * ((pow(key.q, -1, key.p) * (s1 - s2)) % key.p)  # @line L10
    return s.to_bytes(k, "big")  # @line L10


def verify(n: int, e: int, message: bytes, signature: bytes, hash_name: str = "sha256",
           s_len: Optional[int] = None) -> bool:
    """RSASSA-PSS-VERIFY of RFC 8017 Section 8.1.2."""
    mod_bits = n.bit_length()
    k = (mod_bits + 7) // 8
    if len(signature) != k:  # @line L11
        return False  # @line L11
    s = int.from_bytes(signature, "big")
    if s >= n:  # @line L11
        return False  # @line L11
    m = pow(s, e, n)  # @line L12
    em_len = (mod_bits - 1 + 7) // 8
    if m >= 256**em_len:  # @line L12
        return False  # @line L12
    return emsa_pss_verify(message, m.to_bytes(em_len, "big"), mod_bits - 1, hash_name, s_len)


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
