# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/md4/. The authors are listed in prov/HK9M2T.jsonl.
"""MD4 (RFC 1320): the padding, the compression function and the hash.

For study only. MD4 is broken: collisions take less work than one hash
evaluation of a long message. This code is not constant time and is not for
real data. Use SHA-256 or SHA-3 from hashlib or OpenSSL instead.

Words are 32 bits and little-endian. One block is 64 bytes, read as 16 words.
Cost: 48 steps per block, so Theta(n) time for n bytes and Theta(1) extra space
beyond the padded copy of the message.
"""

MASK = 0xFFFFFFFF
IV = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)

# The order of the message words in rounds 2 and 3 (RFC 1320, Section 3.4).
ORDER2 = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
ORDER3 = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
SHIFTS = [[3, 7, 11, 19], [3, 5, 9, 13], [3, 9, 11, 15]]
K2 = 0x5A827999  # floor(2^30 * sqrt(2))
K3 = 0x6ED9EBA1  # floor(2^30 * sqrt(3))


def rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (32 - s))) & MASK


def f(x: int, y: int, z: int) -> int:
    """Round 1: if x then y else z."""
    return (x & y) | (~x & z)


def g(x: int, y: int, z: int) -> int:
    """Round 2: majority of x, y and z."""
    return (x & y) | (x & z) | (y & z)


def h(x: int, y: int, z: int) -> int:
    """Round 3: parity."""
    return x ^ y ^ z


def pad(msg: bytes) -> bytes:
    """Append 0x80, zeros up to 56 mod 64 bytes, and the bit length as 8 bytes, little-endian."""
    n = len(msg)
    zeros = (55 - n) % 64
    return msg + b"\x80" + b"\x00" * zeros + ((8 * n) & ((1 << 64) - 1)).to_bytes(8, "little")


def compress(state: tuple[int, int, int, int], block: bytes) -> tuple[int, int, int, int]:
    """The MD4 compression function on one 64-byte block."""
    x = [int.from_bytes(block[4 * i:4 * i + 4], "little") for i in range(16)]  # @line L5
    a, b, c, d = state  # @line L6
    for i in range(16):  # @line L7
        k = i
        a = rotl((a + f(b, c, d) + x[k]) & MASK, SHIFTS[0][i % 4])
        a, b, c, d = d, a, b, c
    for i in range(16):  # @line L8
        k = ORDER2[i]
        a = rotl((a + g(b, c, d) + x[k] + K2) & MASK, SHIFTS[1][i % 4])
        a, b, c, d = d, a, b, c
    for i in range(16):  # @line L9
        k = ORDER3[i]
        a = rotl((a + h(b, c, d) + x[k] + K3) & MASK, SHIFTS[2][i % 4])
        a, b, c, d = d, a, b, c
    return tuple((u + v) & MASK for u, v in zip(state, (a, b, c, d)))  # @line L10


def md4(msg: bytes) -> bytes:
    """The 16-byte MD4 digest of msg."""
    data = pad(msg)  # @line L1
    state = IV  # @line L2
    for i in range(0, len(data), 64):  # @line L3
        state = compress(state, data[i:i + 64])  # @line L4
    return b"".join(w.to_bytes(4, "little") for w in state)  # @line L11
