# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmac/. The authors are listed in prov/02765M.jsonl.
"""HMAC (RFC 2104, FIPS 198-1) on top of a hashlib hash.

This page is about HMAC, not about the hash, so the hash H comes from hashlib
and only the HMAC layer is written here: the key handling, the two pads, the
nesting, truncation and the tag check.

For study only. The code is not constant time (Python bytes and ints are not),
and it must not protect real data. Use the hmac module of the Python standard
library, libsodium, or a FIPS 140 validated module instead.

This file has the same name as the standard module hmac. The tests load it by
its path, so that both modules can be used side by side.
"""

import hashlib

IPAD = 0x36
OPAD = 0x5C


def _new(hash_name: str, data: bytes = b"") -> "hashlib._Hash":
    return hashlib.new(hash_name, data)


def block_size(hash_name: str) -> int:
    """B, the input block size of H in bytes (64 for SHA-256, 128 for SHA-512)."""
    return _new(hash_name).block_size


def normalize_key(key: bytes, hash_name: str) -> bytes:
    """K' of RFC 2104: hash a key longer than B, then pad with zero bytes to B bytes."""
    b = block_size(hash_name)
    if len(key) > b:  # @line L1
        key = _new(hash_name, key).digest()  # @line L1
    return key + bytes(b - len(key))  # @line L2


def hmac_digest(key: bytes, msg: bytes, hash_name: str = "sha256") -> bytes:
    """HMAC(K, m) = H((K' xor opad) || H((K' xor ipad) || m))."""
    k0 = normalize_key(key, hash_name)
    inner = _new(hash_name, bytes(x ^ IPAD for x in k0) + msg).digest()  # @line L3
    return _new(hash_name, bytes(x ^ OPAD for x in k0) + inner).digest()  # @line L4


def hmac_truncated(key: bytes, msg: bytes, t: int, hash_name: str = "sha256") -> bytes:
    """The leftmost t bytes of the tag (RFC 2104 Section 5, HMAC-H-t)."""
    full = hmac_digest(key, msg, hash_name)
    if not 1 <= t <= len(full):
        raise ValueError("t must be between 1 and the hash length")
    return full[:t]


def tags_equal(a: bytes, b: bytes) -> bool:
    """Compare two tags without an early exit at the first different byte.

    This removes the main timing leak of a byte-by-byte compare, but Python
    gives no real constant time guarantee. Use hmac.compare_digest in real code.
    """
    if len(a) != len(b):
        return False
    d = 0
    for x, y in zip(a, b):  # @line L6
        d |= x ^ y  # @line L6
    return d == 0  # @line L7


def hmac_verify(key: bytes, msg: bytes, tag: bytes, hash_name: str = "sha256") -> bool:
    """Accept tag if it equals the full tag or a truncation of it of the same length."""
    full = hmac_digest(key, msg, hash_name)
    if not 1 <= len(tag) <= len(full):
        return False
    return tags_equal(full[: len(tag)], tag)  # @line L5
