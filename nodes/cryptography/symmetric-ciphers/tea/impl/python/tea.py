# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tea/. The authors are listed in prov/1JEH0C.jsonl.

"""The Tiny Encryption Algorithm (TEA) of Wheeler and Needham (1994), for study only.

This code is not constant time as Python runs it, and TEA has related-key
attacks and equivalent keys. It must not protect real data. Use a vetted
cipher from libsodium, OpenSSL or a FIPS 140 validated module.

A block is two 32-bit words (v0, v1) and a key is four 32-bit words
(k0, k1, k2, k3). The byte helpers read words big-endian, as the published
reference values do.
"""

DELTA = 0x9E3779B9
MASK = 0xFFFFFFFF


def tea_encrypt(v: tuple[int, int], k: tuple[int, int, int, int]) -> tuple[int, int]:
    """Encrypt one block with 32 cycles (64 Feistel rounds).

    Precondition: all words are in [0, 2^32). Cost: Theta(1), 32 cycles.
    """
    v0, v1 = v
    k0, k1, k2, k3 = k
    s = 0  # @line L1
    for _ in range(32):  # @line L2
        s = (s + DELTA) & MASK  # @line L3
        v0 = (v0 + ((((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1)) & MASK)) & MASK  # @line L4
        v1 = (v1 + ((((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3)) & MASK)) & MASK  # @line L5
    return v0, v1  # @line L6


def tea_decrypt(v: tuple[int, int], k: tuple[int, int, int, int]) -> tuple[int, int]:
    """Invert tea_encrypt.

    Precondition: all words are in [0, 2^32). Cost: Theta(1), 32 cycles.
    """
    v0, v1 = v
    k0, k1, k2, k3 = k
    s = (DELTA * 32) & MASK  # @line L7
    for _ in range(32):  # @line L8
        v1 = (v1 - ((((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3)) & MASK)) & MASK  # @line L9
        v0 = (v0 - ((((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1)) & MASK)) & MASK  # @line L10
        s = (s - DELTA) & MASK  # @line L11
    return v0, v1  # @line L12


def _words(b: bytes) -> list[int]:
    return [int.from_bytes(b[i:i + 4], "big") for i in range(0, len(b), 4)]


def tea_encrypt_block(block: bytes, key: bytes) -> bytes:
    """Encrypt an 8-byte block with a 16-byte key, words read big-endian."""
    if len(block) != 8 or len(key) != 16:
        raise ValueError("TEA needs an 8-byte block and a 16-byte key")
    v0, v1 = tea_encrypt((_words(block)[0], _words(block)[1]), tuple(_words(key)))  # type: ignore[arg-type]
    return v0.to_bytes(4, "big") + v1.to_bytes(4, "big")


def tea_decrypt_block(block: bytes, key: bytes) -> bytes:
    """Decrypt an 8-byte block with a 16-byte key, words read big-endian."""
    if len(block) != 8 or len(key) != 16:
        raise ValueError("TEA needs an 8-byte block and a 16-byte key")
    v0, v1 = tea_decrypt((_words(block)[0], _words(block)[1]), tuple(_words(key)))  # type: ignore[arg-type]
    return v0.to_bytes(4, "big") + v1.to_bytes(4, "big")


def equivalent_keys(k: tuple[int, int, int, int]) -> list[tuple[int, int, int, int]]:
    """Return the four keys that act as k: flip the top bits of (k0, k1), of (k2, k3), or of both.

    Kelsey, Schneier and Wagner (1996). Cost: Theta(1).
    """
    top = 0x80000000
    k0, k1, k2, k3 = k
    return [
        (k0, k1, k2, k3),
        (k0 ^ top, k1 ^ top, k2, k3),
        (k0, k1, k2 ^ top, k3 ^ top),
        (k0 ^ top, k1 ^ top, k2 ^ top, k3 ^ top),
    ]
