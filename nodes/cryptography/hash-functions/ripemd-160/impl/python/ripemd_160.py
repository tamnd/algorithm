# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ripemd-160/. The authors are listed in prov/QEE7BH.jsonl.
"""RIPEMD-160 (Dobbertin, Bosselaers and Preneel, 1996) and Bitcoin HASH160.

For study only. This code is not constant time and is not for real data. Use
hashlib.new("ripemd160") where OpenSSL provides it, or a vetted library.

Words are 32 bits and little-endian, as in MD4. Each 64-byte block goes
through two parallel lines of 5 rounds of 16 steps, and the two results are
added to the chaining value with a rotation of the words. The constants follow
the specification by Bosselaers (rmd160.txt) and the 1996 paper.
Cost: 160 steps per block.
"""

MASK = 0xFFFFFFFF
IV = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)

# K_j = floor(2^30 sqrt(p)) and K'_j = floor(2^30 cbrt(p)) for p = 2, 3, 5, 7, with 0 at the ends.
K_LEFT = (0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E)
K_RIGHT = (0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000)

R_LEFT = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
    3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
    1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
    4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13,
]
R_RIGHT = [
    5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
    6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
    15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
    8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
    12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11,
]
S_LEFT = [
    11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
    7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
    11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
    11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
    9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6,
]
S_RIGHT = [
    8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
    9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
    9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
    15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
    8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11,
]


def rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (32 - s))) & MASK


def f(j: int, x: int, y: int, z: int) -> int:
    """The five Boolean functions, for steps j = 0..79."""
    r = j // 16
    if r == 0:
        return x ^ y ^ z
    if r == 1:
        return (x & y) | (~x & z)
    if r == 2:
        return (x | (~y & MASK)) ^ z
    if r == 3:
        return (x & z) | (y & ~z)
    return x ^ (y | (~z & MASK))


def pad(msg: bytes) -> bytes:
    """The MD4 padding: 0x80, zeros to 56 mod 64 bytes, then the bit length in 8 bytes, little-endian."""
    n = len(msg)
    return msg + b"\x80" + b"\x00" * ((55 - n) % 64) + ((8 * n) & ((1 << 64) - 1)).to_bytes(8, "little")


def line(state: tuple[int, ...], x: list[int], left: bool) -> tuple[int, ...]:
    """One line of 80 steps. The right line uses f(79 - j) and its own tables."""
    a, b, c, d, e = state
    for j in range(80):  # @line L7
        if left:
            t = rotl((a + f(j, b, c, d) + x[R_LEFT[j]] + K_LEFT[j // 16]) & MASK, S_LEFT[j])  # @line L8
        else:
            t = rotl((a + f(79 - j, b, c, d) + x[R_RIGHT[j]] + K_RIGHT[j // 16]) & MASK, S_RIGHT[j])  # @line L9
        t = (t + e) & MASK
        a, e, d, c, b = e, d, rotl(c, 10), b, t  # @line L10
    return a, b, c, d, e


def compress(h: tuple[int, ...], block: bytes) -> tuple[int, ...]:
    """The RIPEMD-160 compression function on one 64-byte block."""
    x = [int.from_bytes(block[4 * i:4 * i + 4], "little") for i in range(16)]  # @line L5
    al, bl, cl, dl, el = line(h, x, True)  # @line L6
    ar, br, cr, dr, er = line(h, x, False)
    h0, h1, h2, h3, h4 = h
    return (  # @line L11
        (h1 + cl + dr) & MASK,
        (h2 + dl + er) & MASK,
        (h3 + el + ar) & MASK,
        (h4 + al + br) & MASK,
        (h0 + bl + cr) & MASK,
    )


def ripemd160(msg: bytes) -> bytes:
    """The 20-byte RIPEMD-160 digest of msg."""
    data = pad(msg)  # @line L1
    h = IV  # @line L2
    for i in range(0, len(data), 64):  # @line L3
        h = compress(h, data[i:i + 64])  # @line L4
    return b"".join(w.to_bytes(4, "little") for w in h)  # @line L12


def hash160(data: bytes, sha256) -> bytes:
    """Bitcoin HASH160: RIPEMD-160 of SHA-256. The SHA-256 function is passed in by the caller."""
    return ripemd160(sha256(data))
