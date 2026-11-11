# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cmac/. The authors are listed in prov/57R39D.jsonl.
"""CMAC (NIST SP 800-38B, RFC 4493), which is OMAC1 of Iwata and Kurosawa.

For study only. This code is not constant time (the AES in aes.py uses table
lookups, and the doubling branches on a secret bit) and must not protect real
data. Use AES-CMAC from a FIPS 140 validated module instead, or crypto_auth in
libsodium if a block cipher MAC is not required.
"""

from typing import Protocol


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...


# R_b of SP 800-38B, Section 5.3: the low terms of x^128 + x^7 + x^2 + x + 1 and x^64 + x^4 + x^3 + x + 1.
_RB = {16: 0x87, 8: 0x1B}


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def dbl(x: bytes) -> bytes:
    """Multiply by x in GF(2^n), big-endian: shift left by one bit and reduce with R_b."""
    n = len(x)
    v = int.from_bytes(x, "big") << 1
    if v >> (8 * n):
        v ^= (1 << (8 * n)) | _RB[n]
    return v.to_bytes(n, "big")


def subkeys(cipher: BlockCipher) -> tuple[bytes, bytes]:
    """SP 800-38B, Section 6.1: L = E_K(0^n), K1 = dbl(L), K2 = dbl(K1)."""
    ell = cipher.encrypt_block(bytes(cipher.block_size))  # @line L1
    k1 = dbl(ell)  # @line L2
    k2 = dbl(k1)  # @line L3
    return k1, k2


def tags_equal(a: bytes, b: bytes) -> bool:
    """Compare two tags by reading every byte and folding the differences with OR."""
    if len(a) != len(b):
        return False
    d = 0
    for x, y in zip(a, b):
        d |= x ^ y
    return d == 0


def cmac(cipher: BlockCipher, m: bytes, tlen: int | None = None) -> bytes:
    """SP 800-38B, Section 6.2. tlen is the tag length in bytes (default: the full block)."""
    b = cipher.block_size
    tlen = b if tlen is None else tlen
    if not 1 <= tlen <= b:
        raise ValueError("the tag length must be between 1 and the block length")
    k1, k2 = subkeys(cipher)
    nblocks = max(1, -(-len(m) // b))  # @line L4
    last = m[(nblocks - 1) * b :]
    if len(last) == b:  # @line L5
        last = _xor(last, k1)
    else:  # @line L6
        last = _xor(last + b"\x80" + bytes(b - len(last) - 1), k2)
    c = bytes(b)  # @line L7
    for i in range(nblocks - 1):  # @line L8
        c = cipher.encrypt_block(_xor(c, m[i * b : (i + 1) * b]))  # @line L9
    c = cipher.encrypt_block(_xor(c, last))  # @line L10
    return c[:tlen]  # @line L11


def cmac_verify(cipher: BlockCipher, m: bytes, tag: bytes) -> bool:
    """SP 800-38B, Section 6.3: recompute and compare."""
    return tags_equal(cmac(cipher, m, len(tag)), tag)  # @line L12
