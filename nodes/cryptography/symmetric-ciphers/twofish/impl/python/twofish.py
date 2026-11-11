# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/twofish/. The authors are listed in prov/HJZJTY.jsonl.
"""Twofish (Schneier, Kelsey, Whiting, Wagner, Hall and Ferguson 1998).

For study only. This code is not constant time: the q permutations are
tables indexed by secret bytes, and Python itself leaks timing. Do not use it
to protect real data. Use AES or ChaCha20 from a validated library (for
example the Python package "cryptography") instead.

The names follow the Twofish paper, Section 4: the q permutations q0 and q1
built from 4-bit tables, the MDS matrix over GF(2^8) mod x^8+x^6+x^5+x^3+1,
the RS matrix over GF(2^8) mod x^8+x^6+x^3+x^2+1, the function h, the
pseudo-Hadamard transform (PHT) and the key schedule with vectors Me, Mo and
S. Words are read little-endian. Keys of 16, 24 or 32 bytes. Cost: 16 rounds,
each with two calls of g (12 q lookups and one MDS product per call with a
128-bit key).
"""

MASK32 = 0xFFFFFFFF
RHO = 0x01010101

# Section 4.3.5: the 4-bit tables t0..t3 for q0 and for q1.
Q0_T = [
    [0x8, 0x1, 0x7, 0xD, 0x6, 0xF, 0x3, 0x2, 0x0, 0xB, 0x5, 0x9, 0xE, 0xC, 0xA, 0x4],
    [0xE, 0xC, 0xB, 0x8, 0x1, 0x2, 0x3, 0x5, 0xF, 0x4, 0xA, 0x6, 0x7, 0x0, 0x9, 0xD],
    [0xB, 0xA, 0x5, 0xE, 0x6, 0xD, 0x9, 0x0, 0xC, 0x8, 0xF, 0x3, 0x2, 0x4, 0x7, 0x1],
    [0xD, 0x7, 0xF, 0x4, 0x1, 0x2, 0x6, 0xE, 0x9, 0xB, 0x3, 0x0, 0x8, 0x5, 0xC, 0xA],
]
Q1_T = [
    [0x2, 0x8, 0xB, 0xD, 0xF, 0x7, 0x6, 0xE, 0x3, 0x1, 0x9, 0x4, 0x0, 0xA, 0xC, 0x5],
    [0x1, 0xE, 0x2, 0xB, 0x4, 0xC, 0x3, 0x7, 0x6, 0xD, 0xA, 0x5, 0xF, 0x9, 0x0, 0x8],
    [0x4, 0xC, 0x7, 0x5, 0x1, 0x6, 0x9, 0xA, 0x0, 0xE, 0xD, 0x8, 0x2, 0xB, 0x3, 0xF],
    [0xB, 0x9, 0x5, 0x1, 0xC, 0x3, 0xD, 0xE, 0x6, 0x4, 0x7, 0xF, 0x2, 0x0, 0x8, 0xA],
]

MDS = [
    [0x01, 0xEF, 0x5B, 0x5B],
    [0x5B, 0xEF, 0xEF, 0x01],
    [0xEF, 0x5B, 0x01, 0xEF],
    [0xEF, 0x01, 0xEF, 0x5B],
]
RS = [
    [0x01, 0xA4, 0x55, 0x87, 0x5A, 0x58, 0xDB, 0x9E],
    [0xA4, 0x56, 0x82, 0xF3, 0x1E, 0xC6, 0x68, 0xE5],
    [0x02, 0xA1, 0xFC, 0xC1, 0x47, 0xAE, 0x3D, 0x19],
    [0xA4, 0x55, 0x87, 0x5A, 0x58, 0xDB, 0x9E, 0x03],
]


def _ror4(x: int, n: int) -> int:
    return ((x >> n) | (x << (4 - n))) & 0xF


def _q(t: list[list[int]], x: int) -> int:
    a0, b0 = x >> 4, x & 0xF
    a1 = a0 ^ b0
    b1 = a0 ^ _ror4(b0, 1) ^ ((8 * a0) & 0xF)
    a2, b2 = t[0][a1], t[1][b1]
    a3 = a2 ^ b2
    b3 = a2 ^ _ror4(b2, 1) ^ ((8 * a2) & 0xF)
    a4, b4 = t[2][a3], t[3][b3]
    return 16 * b4 + a4


Q0 = [_q(Q0_T, x) for x in range(256)]
Q1 = [_q(Q1_T, x) for x in range(256)]


def gf_mul(a: int, b: int, poly: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        if a & 0x100:
            a ^= poly
        b >>= 1
    return r


def rol(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & MASK32


def ror(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK32


def _bytes_le(x: int) -> list[int]:
    return [(x >> (8 * i)) & 0xFF for i in range(4)]


def _word_le(b: list[int]) -> int:
    return b[0] | (b[1] << 8) | (b[2] << 16) | (b[3] << 24)


def h(x: int, lst: list[int]) -> int:
    """Section 4.3.2: the function h with the list L = (L0, ..., L(k-1))."""
    y = _bytes_le(x)
    k = len(lst)
    l_b = [_bytes_le(w) for w in lst]
    if k == 4:  # @line L11
        y = [Q1[y[0]] ^ l_b[3][0], Q0[y[1]] ^ l_b[3][1], Q0[y[2]] ^ l_b[3][2], Q1[y[3]] ^ l_b[3][3]]
    if k >= 3:
        y = [Q1[y[0]] ^ l_b[2][0], Q1[y[1]] ^ l_b[2][1], Q0[y[2]] ^ l_b[2][2], Q0[y[3]] ^ l_b[2][3]]
    y = [
        Q1[Q0[Q0[y[0]] ^ l_b[1][0]] ^ l_b[0][0]],
        Q0[Q0[Q1[y[1]] ^ l_b[1][1]] ^ l_b[0][1]],
        Q1[Q1[Q0[y[2]] ^ l_b[1][2]] ^ l_b[0][2]],
        Q0[Q1[Q1[y[3]] ^ l_b[1][3]] ^ l_b[0][3]],
    ]
    z = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            z[i] ^= gf_mul(MDS[i][j], y[j], 0x169)
    return _word_le(z)  # @line L12


def key_schedule(key: bytes) -> tuple[list[int], list[int]]:
    """Return the 40 subkeys K0..K39 and the S-box key vector S."""
    if len(key) not in (16, 24, 32):
        raise ValueError("the key must have 16, 24 or 32 bytes")
    k = len(key) // 8
    m = [_word_le(list(key[4 * i:4 * i + 4])) for i in range(2 * k)]
    me, mo = m[0::2], m[1::2]  # @line L13
    s = []
    for i in range(k):
        v = [0, 0, 0, 0]
        for r in range(4):
            for c in range(8):
                v[r] ^= gf_mul(RS[r][c], key[8 * i + c], 0x14D)
        s.append(_word_le(v))
    s.reverse()  # S = (S(k-1), ..., S0)  # @line L14
    sub = []
    for i in range(20):  # @line L15
        a = h(2 * i * RHO & MASK32, me)  # @line L16
        b = rol(h((2 * i + 1) * RHO & MASK32, mo), 8)  # @line L17
        sub.append((a + b) & MASK32)  # the PHT  # @line L18
        sub.append(rol((a + 2 * b) & MASK32, 9))  # @line L19
    return sub, s


class Twofish:
    def __init__(self, key: bytes) -> None:
        self.k, self.s = key_schedule(key)

    def _g(self, x: int) -> int:
        return h(x, self.s)

    def _f(self, r0: int, r1: int, rnd: int) -> tuple[int, int]:
        t0 = self._g(r0)  # @line L6
        t1 = self._g(rol(r1, 8))  # @line L7
        f0 = (t0 + t1 + self.k[2 * rnd + 8]) & MASK32  # @line L8
        f1 = (t0 + 2 * t1 + self.k[2 * rnd + 9]) & MASK32  # @line L9
        return f0, f1  # @line L10

    def encrypt_block(self, block: bytes) -> bytes:
        if len(block) != 16:
            raise ValueError("the block must have 16 bytes")
        r = [_word_le(list(block[4 * i:4 * i + 4])) ^ self.k[i] for i in range(4)]  # @line L1
        for rnd in range(16):  # @line L2
            f0, f1 = self._f(r[0], r[1], rnd)  # @line L3
            r = [ror(r[2] ^ f0, 1), rol(r[3], 1) ^ f1, r[0], r[1]]  # @line L4
        c = [r[(i + 2) % 4] ^ self.k[i + 4] for i in range(4)]  # @line L5
        return b"".join(bytes(_bytes_le(w)) for w in c)

    def decrypt_block(self, block: bytes) -> bytes:
        if len(block) != 16:
            raise ValueError("the block must have 16 bytes")
        c = [_word_le(list(block[4 * i:4 * i + 4])) ^ self.k[i + 4] for i in range(4)]
        r = [c[2], c[3], c[0], c[1]]
        for rnd in range(15, -1, -1):
            # r is the state after round rnd; undo it.
            f0, f1 = self._f(r[2], r[3], rnd)
            r = [r[2], r[3], rol(r[0], 1) ^ f0, ror(r[1] ^ f1, 1)]
        return b"".join(bytes(_bytes_le(w ^ self.k[i])) for i, w in enumerate(r))
