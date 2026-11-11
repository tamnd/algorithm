# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-signature/. The authors are listed in prov/PEKVQA.jsonl.
"""RSA signatures: RSASSA-PKCS1-v1_5 of RFC 8017 Section 8.2, with the
EMSA-PKCS1-v1_5 encoding of Section 9.2, signing with the Chinese remainder
theorem (RSASP1, Section 5.2.1), and textbook RSA for comparison.

The page is about the RSA signature, not about the hash, so the hash comes
from hashlib.

For study only. The code is not constant time (Python integers are not), the
key generator uses a seeded, non-cryptographic random source, and the code
must not protect real data. Use the pyca/cryptography library or a FIPS 140
validated module instead.
"""

import hashlib
import math
import random
from dataclasses import dataclass
from typing import Callable, Optional

# The DER encoding of DigestInfo up to the hash value, RFC 8017 Section 9.2, Note 1.
DIGEST_INFO_PREFIX = {
    "sha1": bytes.fromhex("3021300906052b0e03021a05000414"),
    "sha224": bytes.fromhex("302d300d06096086480165030402040500041c"),
    "sha256": bytes.fromhex("3031300d060960864801650304020105000420"),
    "sha384": bytes.fromhex("3041300d060960864801650304020205000430"),
    "sha512": bytes.fromhex("3051300d060960864801650304020305000440"),
}


@dataclass(frozen=True)
class PrivateKey:
    """An RSA private key in the CRT form of RFC 8017 Section 3.2."""

    n: int
    e: int
    d: int
    p: int
    q: int
    dp: int
    dq: int
    qinv: int


def i2osp(x: int, length: int) -> bytes:
    """I2OSP of RFC 8017 Section 4.1: the big-endian string of `length` bytes."""
    if x < 0 or x >= 256**length:
        raise ValueError("integer too large")
    return x.to_bytes(length, "big")


def os2ip(data: bytes) -> int:
    """OS2IP of RFC 8017 Section 4.2."""
    return int.from_bytes(data, "big")


def byte_length(n: int) -> int:
    """k, the length of the modulus in bytes."""
    return (n.bit_length() + 7) // 8


def emsa_pkcs1_v15_encode(message: bytes, em_len: int, hash_name: str = "sha256") -> bytes:
    """EMSA-PKCS1-v1_5-ENCODE of RFC 8017 Section 9.2."""
    h = hashlib.new(hash_name, message).digest()  # @line L2
    t = DIGEST_INFO_PREFIX[hash_name] + h  # @line L3
    if em_len < len(t) + 11:  # @line L4
        raise ValueError("intended encoded message length too short")  # @line L4
    return b"\x00\x01" + b"\xff" * (em_len - len(t) - 3) + b"\x00" + t  # @line L5


def rsasp1_crt(key: PrivateKey, m: int, fault: Optional[Callable[[int], int]] = None) -> int:
    """RSASP1 with the CRT (RFC 8017 Section 5.2.1, case b), Garner's recombination.

    `fault`, if given, is applied to s1. It simulates a hardware fault for the
    test of the fault attack, and is never used in normal signing.
    """
    if not 0 <= m < key.n:
        raise ValueError("message representative out of range")
    s1 = pow(m, key.dp, key.p)  # @line L7
    s2 = pow(m, key.dq, key.q)  # @line L7
    if fault is not None:
        s1 = fault(s1)
    h = (key.qinv * (s1 - s2)) % key.p  # @line L8
    return s2 + key.q * h  # @line L9


def sign(key: PrivateKey, message: bytes, hash_name: str = "sha256") -> bytes:
    """RSASSA-PKCS1-V1_5-SIGN of RFC 8017 Section 8.2.1."""
    k = byte_length(key.n)  # @line L1
    em = emsa_pkcs1_v15_encode(message, k, hash_name)
    m = os2ip(em)  # @line L6
    s = rsasp1_crt(key, m)
    return i2osp(s, k)  # @line L10


def verify(n: int, e: int, message: bytes, signature: bytes, hash_name: str = "sha256") -> bool:
    """RSASSA-PKCS1-V1_5-VERIFY of RFC 8017 Section 8.2.2.

    It re-encodes the message and compares whole encodings. It never parses
    the decoded block, which is what made the e = 3 forgery possible.
    """
    k = byte_length(n)
    if len(signature) != k:  # @line L11
        return False  # @line L11
    s = os2ip(signature)  # @line L12
    if s >= n:  # @line L12
        return False  # @line L12
    m = pow(s, e, n)  # @line L13
    em = i2osp(m, k)  # @line L14
    try:
        em2 = emsa_pkcs1_v15_encode(message, k, hash_name)  # @line L15
    except ValueError:
        return False
    return em == em2  # @line L16


def sign_checked(key: PrivateKey, message: bytes, hash_name: str = "sha256",
                 fault: Optional[Callable[[int], int]] = None) -> bytes:
    """Sign, then verify with the public key before release: the standard
    countermeasure to the CRT fault attack."""
    k = byte_length(key.n)
    m = os2ip(emsa_pkcs1_v15_encode(message, k, hash_name))
    s = rsasp1_crt(key, m, fault)
    if pow(s, key.e, key.n) != m:
        raise RuntimeError("signature check failed; output withheld")
    return i2osp(s, k)


def textbook_sign(key: PrivateKey, m: int) -> int:
    """Textbook RSA: s = m^d mod N, with no hash and no padding. Insecure."""
    return pow(m, key.d, key.n)


def textbook_verify(n: int, e: int, m: int, s: int) -> bool:
    return 0 <= s < n and pow(s, e, n) == m % n


def _is_probable_prime(n: int, rng: random.Random, rounds: int = 40) -> bool:
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
        a = rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _random_prime(bits: int, e: int, rng: random.Random) -> int:
    while True:
        c = rng.getrandbits(bits) | (3 << (bits - 2)) | 1
        if math.gcd(c - 1, e) == 1 and _is_probable_prime(c, rng):
            return c


def generate_key(bits: int = 1024, e: int = 65537, seed: int = 0) -> PrivateKey:
    """A key with an exact `bits`-bit modulus, from a seeded random source.

    Toy key generation for tests: it does not follow FIPS 186-5 Appendix A.1.
    """
    rng = random.Random(seed)
    while True:
        p = _random_prime(bits // 2, e, rng)
        q = _random_prime(bits - bits // 2, e, rng)
        n = p * q
        if p != q and n.bit_length() == bits:
            break
    if p < q:
        p, q = q, p
    lam = (p - 1) * (q - 1) // math.gcd(p - 1, q - 1)
    d = pow(e, -1, lam)
    return PrivateKey(n, e, d, p, q, d % (p - 1), d % (q - 1), pow(q, -1, p))
