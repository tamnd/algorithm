# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/serpent/. The authors are listed in prov/9ATZRG.jsonl.
"""Serpent (Anderson, Biham and Knudsen 1998), in the bitslice form.

For study only. This code is not constant time, and Python itself leaks
timing. Do not use it to protect real data. Use AES or ChaCha20 from a
validated library (for example the Python package "cryptography") instead.

The names follow "Serpent: A Proposal for the Advanced Encryption Standard",
Sections 3 and 4 and Appendix A.5. The bitslice form needs no initial or final
permutation: the block is four 32-bit words X0..X3, and S-box j acts on the
4-bit column made of bit j of X0 (lowest), X1, X2 and X3 (highest).

Bit order. The paper treats every value as a little-endian number: word 0 is
the least significant word, bit 0 is the least significant bit. This module
reads a byte string the way the NESSIE test vectors do: byte 0 is the least
significant byte, so the 16 bytes b0..b15 give X0 = b0 + 2^8 b1 + ... and so
on. The same rule holds for the key, and a short key gets a "1" bit just
above its most significant bit, then zeros up to 256 bits.
Cost: 32 rounds, each with 32 parallel 4-bit S-boxes and a linear transform.
"""

MASK32 = 0xFFFFFFFF
PHI = 0x9E3779B9

# Appendix A.5.
SBOX = [
    [3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12],
    [15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4],
    [8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2],
    [0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14],
    [1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13],
    [15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1],
    [7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0],
    [1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6],
]
SBOX_INV = [[box.index(v) for v in range(16)] for box in SBOX]


def rol(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & MASK32


def ror(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK32


def apply_sbox(box: list[int], x: list[int]) -> list[int]:
    """Apply a 4-bit S-box to each of the 32 bit columns of four words."""
    out = [0, 0, 0, 0]
    for j in range(32):
        v = sum(((x[i] >> j) & 1) << i for i in range(4))
        s = box[v]
        for i in range(4):
            out[i] |= ((s >> i) & 1) << j
    return out


def lt(x: list[int]) -> list[int]:
    """Section 3: the linear transformation."""
    x0, x1, x2, x3 = x
    x0 = rol(x0, 13)  # @line L9
    x2 = rol(x2, 3)
    x1 ^= x0 ^ x2  # @line L10
    x3 ^= x2 ^ ((x0 << 3) & MASK32)
    x1 = rol(x1, 1)  # @line L11
    x3 = rol(x3, 7)
    x0 ^= x1 ^ x3  # @line L12
    x2 ^= x3 ^ ((x1 << 7) & MASK32)
    x0 = rol(x0, 5)  # @line L13
    x2 = rol(x2, 22)
    return [x0, x1, x2, x3]  # @line L14


def lt_inv(x: list[int]) -> list[int]:
    x0, x1, x2, x3 = x
    x2 = ror(x2, 22)
    x0 = ror(x0, 5)
    x2 ^= x3 ^ ((x1 << 7) & MASK32)
    x0 ^= x1 ^ x3
    x3 = ror(x3, 7)
    x1 = ror(x1, 1)
    x3 ^= x2 ^ ((x0 << 3) & MASK32)
    x1 ^= x0 ^ x2
    x2 = ror(x2, 3)
    x0 = ror(x0, 13)
    return [x0, x1, x2, x3]


def round_keys(key: bytes) -> list[list[int]]:
    """Section 4: pad the key, build the 132 prekeys, pass them through S-boxes."""
    if not 1 <= len(key) <= 32:
        raise ValueError("the key must have 1 to 32 bytes")
    k = int.from_bytes(key, "little")
    if len(key) < 32:
        k |= 1 << (8 * len(key))  # @line L15
    w = [(k >> (32 * i)) & MASK32 for i in range(8)]  # w(-8) .. w(-1)  # @line L16
    for i in range(132):
        w.append(rol(w[i] ^ w[i + 3] ^ w[i + 5] ^ w[i + 7] ^ PHI ^ i, 11))  # @line L17
    pre = w[8:]
    return [apply_sbox(SBOX[(3 - i) % 8], pre[4 * i:4 * i + 4]) for i in range(33)]  # @line L18


def _words(block: bytes) -> list[int]:
    if len(block) != 16:
        raise ValueError("the block must have 16 bytes")
    return [int.from_bytes(block[4 * i:4 * i + 4], "little") for i in range(4)]


def _bytes(x: list[int]) -> bytes:
    return b"".join(w.to_bytes(4, "little") for w in x)


def encrypt_block(key: bytes, block: bytes) -> bytes:
    kr = round_keys(key)  # @line L1
    x = _words(block)  # @line L2
    for i in range(32):  # @line L3
        x = [a ^ b for a, b in zip(x, kr[i])]  # @line L4
        x = apply_sbox(SBOX[i % 8], x)  # @line L5
        if i < 31:
            x = lt(x)  # @line L6
        else:
            x = [a ^ b for a, b in zip(x, kr[32])]  # @line L7
    return _bytes(x)  # @line L8


def decrypt_block(key: bytes, block: bytes) -> bytes:
    kr = round_keys(key)
    x = _words(block)
    for i in range(31, -1, -1):
        x = [a ^ b for a, b in zip(x, kr[32])] if i == 31 else lt_inv(x)
        x = apply_sbox(SBOX_INV[i % 8], x)
        x = [a ^ b for a, b in zip(x, kr[i])]
    return _bytes(x)
