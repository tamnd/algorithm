# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hkdf/. The authors are listed in prov/DCNWKP.jsonl.
"""HKDF, the HMAC-based extract-and-expand key derivation function (RFC 5869).

HKDF-Extract turns input keying material of any length into a pseudorandom
key PRK = HMAC(salt, IKM). HKDF-Expand stretches PRK into L bytes of output
keying material, bound to a context string info. The HMAC here is the one of
the Python standard library.

For study only. The code is not constant time. Do not use it to protect
real data. Use the HKDF of the Python package cryptography, of OpenSSL, or
of a FIPS 140 validated module instead. HKDF is not a password hash: for
passwords use PBKDF2, scrypt or Argon2.

Cost: Extract is one HMAC call; Expand is ceil(L / HashLen) HMAC calls.
"""

import hashlib
import hmac
import math


def hkdf_extract(salt: bytes, ikm: bytes, hash_name: str = "sha256") -> bytes:
    """PRK = HMAC-Hash(salt, IKM). An empty salt means HashLen zero bytes."""
    hash_len = hashlib.new(hash_name).digest_size
    if not salt:  # @line L1
        salt = bytes(hash_len)
    return hmac.new(salt, ikm, hash_name).digest()  # @line L2


def hkdf_expand(prk: bytes, info: bytes, length: int, hash_name: str = "sha256") -> bytes:
    """OKM = the first L bytes of T(1) | T(2) | ..., T(i) = HMAC(PRK, T(i-1) | info | i)."""
    hash_len = hashlib.new(hash_name).digest_size
    n = math.ceil(length / hash_len)  # @line L3
    if n > 255:  # @line L4
        raise ValueError("L is larger than 255 * HashLen")
    okm, t = b"", b""  # @line L5
    for i in range(1, n + 1):  # @line L6
        t = hmac.new(prk, t + info + bytes([i]), hash_name).digest()  # @line L7
        okm += t
    return okm[:length]  # @line L8


def hkdf(salt: bytes, ikm: bytes, info: bytes, length: int, hash_name: str = "sha256") -> bytes:
    """HKDF(salt, IKM, info, L) = HKDF-Expand(HKDF-Extract(salt, IKM), info, L)."""
    return hkdf_expand(hkdf_extract(salt, ikm, hash_name), info, length, hash_name)


def hkdf_expand_label(secret: bytes, label: bytes, context: bytes, length: int, hash_name: str = "sha256") -> bytes:
    """HKDF-Expand-Label of TLS 1.3 (RFC 8446 Section 7.1).

    The info is the HkdfLabel structure: a 2-byte length, then the label
    "tls13 " + label and the context, each with a 1-byte length prefix.
    """
    full = b"tls13 " + label
    info = length.to_bytes(2, "big") + bytes([len(full)]) + full + bytes([len(context)]) + context
    return hkdf_expand(secret, info, length, hash_name)


def derive_secret(secret: bytes, label: bytes, transcript_hash: bytes, hash_name: str = "sha256") -> bytes:
    """Derive-Secret of TLS 1.3: HKDF-Expand-Label(secret, label, hash, HashLen)."""
    hash_len = hashlib.new(hash_name).digest_size
    return hkdf_expand_label(secret, label, transcript_hash, hash_len, hash_name)
