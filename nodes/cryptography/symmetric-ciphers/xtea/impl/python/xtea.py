# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xtea/. The authors are listed in prov/07Z3SA.jsonl.

"""XTEA, the extended TEA of Needham and Wheeler (1997), for study only.

This code is not constant time as Python runs it, and XTEA has a 64-bit
block. It must not protect real data. Use a vetted cipher from libsodium,
OpenSSL or a FIPS 140 validated module.

A block is two 32-bit words (v0, v1) and a key is four 32-bit words. The byte
helpers read words big-endian, as the published reference values do. One
cycle is two Feistel rounds; the standard cipher uses 32 cycles (64 rounds).
"""

DELTA = 0x9E3779B9
MASK = 0xFFFFFFFF


def xtea_encrypt(v: tuple[int, int], k: tuple[int, int, int, int], cycles: int = 32) -> tuple[int, int]:
    """Encrypt one block.

    Precondition: all words are in [0, 2^32) and cycles >= 0.
    Cost: Theta(cycles) word operations.
    """
    v0, v1 = v
    s = 0  # @line L1
    for _ in range(cycles):  # @line L2
        v0 = (v0 + (((((v1 << 4) ^ (v1 >> 5)) + v1) ^ (s + k[s & 3])) & MASK)) & MASK  # @line L3
        s = (s + DELTA) & MASK  # @line L4
        v1 = (v1 + (((((v0 << 4) ^ (v0 >> 5)) + v0) ^ (s + k[(s >> 11) & 3])) & MASK)) & MASK  # @line L5
    return v0, v1  # @line L6


def xtea_decrypt(v: tuple[int, int], k: tuple[int, int, int, int], cycles: int = 32) -> tuple[int, int]:
    """Invert xtea_encrypt with the same number of cycles.

    Precondition: all words are in [0, 2^32) and cycles >= 0.
    Cost: Theta(cycles) word operations.
    """
    v0, v1 = v
    s = (DELTA * cycles) & MASK  # @line L7
    for _ in range(cycles):  # @line L8
        v1 = (v1 - (((((v0 << 4) ^ (v0 >> 5)) + v0) ^ (s + k[(s >> 11) & 3])) & MASK)) & MASK  # @line L9
        s = (s - DELTA) & MASK  # @line L10
        v0 = (v0 - (((((v1 << 4) ^ (v1 >> 5)) + v1) ^ (s + k[s & 3])) & MASK)) & MASK  # @line L11
    return v0, v1  # @line L12


def _words(b: bytes) -> list[int]:
    return [int.from_bytes(b[i:i + 4], "big") for i in range(0, len(b), 4)]


def xtea_encrypt_block(block: bytes, key: bytes, cycles: int = 32) -> bytes:
    """Encrypt an 8-byte block with a 16-byte key, words read big-endian."""
    if len(block) != 8 or len(key) != 16:
        raise ValueError("XTEA needs an 8-byte block and a 16-byte key")
    w, kw = _words(block), _words(key)
    v0, v1 = xtea_encrypt((w[0], w[1]), (kw[0], kw[1], kw[2], kw[3]), cycles)
    return v0.to_bytes(4, "big") + v1.to_bytes(4, "big")


def xtea_decrypt_block(block: bytes, key: bytes, cycles: int = 32) -> bytes:
    """Decrypt an 8-byte block with a 16-byte key, words read big-endian."""
    if len(block) != 8 or len(key) != 16:
        raise ValueError("XTEA needs an 8-byte block and a 16-byte key")
    w, kw = _words(block), _words(key)
    v0, v1 = xtea_decrypt((w[0], w[1]), (kw[0], kw[1], kw[2], kw[3]), cycles)
    return v0.to_bytes(4, "big") + v1.to_bytes(4, "big")
