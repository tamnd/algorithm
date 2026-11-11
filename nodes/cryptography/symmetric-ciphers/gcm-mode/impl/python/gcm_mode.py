# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gcm-mode/. The authors are listed in prov/74AABT.jsonl.
"""Galois/Counter Mode (GCM), NIST SP 800-38D and McGrew and Viega's specification.

For study only. This code is not constant time: AES uses table lookups and the
field multiplication branches on secret bits. Do not use it to protect real
data; use AES-GCM from a FIPS 140 validated module, or the AEAD functions of
libsodium.

Bit order. A block is a 128-bit string X_0 X_1 ... X_127, stored big-endian in a
Python int, so X_0 is the most significant bit. GCM reads X_i as the coefficient
of x^i: the leftmost bit is the constant term. So "multiply by x" is a shift to
the right, and the reduction constant R = 11100001 || 0^120 is x^128 reduced
modulo x^128 + x^7 + x^2 + x + 1, that is 1 + x + x^2 + x^7, written in this order.
"""

from typing import Protocol

R = 0xE1 << 120
ONE = 1 << 127  # the polynomial 1: only the leftmost bit is set
MASK = (1 << 128) - 1


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...


class InvalidTag(ValueError):
    """The tag did not verify. No plaintext is returned."""


def gf_mult(x: int, y: int) -> int:
    """X . Y in GF(2^128), Algorithm 1 of SP 800-38D (and of the GCM specification, Section 2.5)."""
    z, v = 0, y  # @line L1
    for i in range(128):  # @line L2
        if (x >> (127 - i)) & 1:  # @line L3
            z ^= v
        v = (v >> 1) ^ R if v & 1 else v >> 1  # @line L4
    return z  # @line L5


def gf_pow(x: int, e: int) -> int:
    result = ONE
    while e:
        if e & 1:
            result = gf_mult(result, x)
        x = gf_mult(x, x)
        e >>= 1
    return result


def gf_inverse(x: int) -> int:
    """x^(2^128 - 2), the inverse of a nonzero element."""
    if x == 0:
        raise ZeroDivisionError("0 has no inverse")
    return gf_pow(x, (1 << 128) - 2)


def gf_sqrt(x: int) -> int:
    """x^(2^127). Squaring is a bijection of GF(2^128), and this is its inverse."""
    return gf_pow(x, 1 << 127)


def ghash(h: int, data: bytes) -> int:
    """GHASH_H(X_1 ... X_m) for a whole number of 16-byte blocks."""
    if len(data) % 16:
        raise ValueError("GHASH takes whole blocks")
    y = 0  # @line L6
    for j in range(0, len(data), 16):  # @line L7
        y = gf_mult(y ^ int.from_bytes(data[j : j + 16], "big"), h)
    return y  # @line L8


def _pad(x: bytes) -> bytes:
    return x + bytes(-len(x) % 16)


def inc32(block: bytes) -> bytes:
    """Add 1 modulo 2^32 to the rightmost 32 bits; the leftmost 96 bits stay."""
    low = (int.from_bytes(block[12:], "big") + 1) & 0xFFFFFFFF
    return block[:12] + low.to_bytes(4, "big")


def gctr(cipher: BlockCipher, icb: bytes, x: bytes) -> bytes:
    """CTR mode with inc32, SP 800-38D Algorithm 3. The last block may be partial."""
    out, cb = bytearray(), icb
    for j in range(0, len(x), 16):
        out += bytes(a ^ b for a, b in zip(x[j : j + 16], cipher.encrypt_block(cb)))
        cb = inc32(cb)
    return bytes(out)


def _j0(cipher: BlockCipher, h: int, iv: bytes) -> bytes:
    if len(iv) == 12:  # @line L10
        return iv + b"\x00\x00\x00\x01"
    if not iv:
        raise ValueError("the IV must not be empty")
    block = _pad(iv) + bytes(8) + (8 * len(iv)).to_bytes(8, "big")
    return ghash(h, block).to_bytes(16, "big")  # @line L11


def _s(h: int, a: bytes, c: bytes) -> int:
    lengths = (8 * len(a)).to_bytes(8, "big") + (8 * len(c)).to_bytes(8, "big")
    return ghash(h, _pad(a) + _pad(c) + lengths)


def hash_subkey(cipher: BlockCipher) -> int:
    return int.from_bytes(cipher.encrypt_block(bytes(16)), "big")


def gcm_encrypt(cipher: BlockCipher, iv: bytes, a: bytes, p: bytes, tag_len: int = 16) -> tuple[bytes, bytes]:
    """Return (C, T). Precondition: the IV is never used twice under the key."""
    if cipher.block_size != 16 or not 4 <= tag_len <= 16:
        raise ValueError("GCM needs a 128-bit block cipher and a tag of 4 to 16 bytes")
    h = hash_subkey(cipher)  # @line L9
    j0 = _j0(cipher, h, iv)
    c = gctr(cipher, inc32(j0), p)  # @line L12
    s = _s(h, a, c)  # @line L13
    t = gctr(cipher, j0, s.to_bytes(16, "big"))[:tag_len]  # @line L14
    return c, t  # @line L15


def tags_equal(a: bytes, b: bytes) -> bool:
    if len(a) != len(b):
        return False
    d = 0
    for x, y in zip(a, b):
        d |= x ^ y
    return d == 0


def gcm_decrypt(cipher: BlockCipher, iv: bytes, a: bytes, c: bytes, t: bytes) -> bytes:
    """Return P, or raise InvalidTag. The tag is checked before any plaintext is made."""
    if not 4 <= len(t) <= 16:
        raise ValueError("bad tag length")
    h = hash_subkey(cipher)  # @line L16
    j0 = _j0(cipher, h, iv)
    expected = gctr(cipher, j0, _s(h, a, c).to_bytes(16, "big"))[: len(t)]
    if not tags_equal(expected, t):  # @line L17
        raise InvalidTag("tag mismatch")
    return gctr(cipher, inc32(j0), c)  # @line L18
