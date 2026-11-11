# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/md5/. The authors are listed in prov/E0VM6D.jsonl.
"""MD5 (RFC 1321): the padding, the compression function and the hash.

For study only. MD5 is broken for collisions: a collision takes seconds on a
laptop, and chosen-prefix collisions are practical. This code is not constant
time and is not for real data. Use SHA-256 or SHA-3 from hashlib or OpenSSL
instead.

Words are 32 bits and little-endian. One block is 64 bytes, read as 16 words.
Cost: 64 steps per block, so Theta(n) time for n bytes.
"""

import math

MASK = 0xFFFFFFFF
IV = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)

# T[i] = floor(2^32 * |sin(i + 1)|), with i + 1 in radians (RFC 1321, Section 3.4).
T = [int(abs(math.sin(i + 1)) * 2**32) & MASK for i in range(64)]

SHIFTS = [[7, 12, 17, 22], [5, 9, 14, 20], [4, 11, 16, 23], [6, 10, 15, 21]]


def rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (32 - s))) & MASK


def round_function(r: int, x: int, y: int, z: int) -> int:
    """F, G, H and I of RFC 1321 for rounds r = 0, 1, 2, 3."""
    if r == 0:
        return (x & y) | (~x & z)
    if r == 1:
        return (x & z) | (y & ~z)
    if r == 2:
        return x ^ y ^ z
    return (y ^ (x | (~z & MASK))) & MASK


def word_index(i: int) -> int:
    """The message word used in step i (0 <= i < 64)."""
    r = i // 16
    if r == 0:
        return i
    if r == 1:
        return (5 * i + 1) % 16
    if r == 2:
        return (3 * i + 5) % 16
    return (7 * i) % 16


def pad(msg: bytes) -> bytes:
    """Append 0x80, zeros up to 56 mod 64 bytes, and the bit length as 8 bytes, little-endian."""
    n = len(msg)
    return msg + b"\x80" + b"\x00" * ((55 - n) % 64) + ((8 * n) & ((1 << 64) - 1)).to_bytes(8, "little")


def compress(state: tuple[int, int, int, int], block: bytes) -> tuple[int, int, int, int]:
    """The MD5 compression function on one 64-byte block."""
    x = [int.from_bytes(block[4 * i:4 * i + 4], "little") for i in range(16)]  # @line L5
    a, b, c, d = state  # @line L6
    for i in range(64):  # @line L7
        r = i // 16
        t = (a + round_function(r, b, c, d) + x[word_index(i)] + T[i]) & MASK  # @line L8
        a = (b + rotl(t, SHIFTS[r][i % 4])) & MASK  # @line L9
        a, b, c, d = d, a, b, c  # @line L10
    return tuple((u + v) & MASK for u, v in zip(state, (a, b, c, d)))  # @line L11


def md5(msg: bytes) -> bytes:
    """The 16-byte MD5 digest of msg."""
    data = pad(msg)  # @line L1
    state = IV  # @line L2
    for i in range(0, len(data), 64):  # @line L3
        state = compress(state, data[i:i + 64])  # @line L4
    return b"".join(w.to_bytes(4, "little") for w in state)  # @line L12
