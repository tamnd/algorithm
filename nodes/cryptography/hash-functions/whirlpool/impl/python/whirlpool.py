# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whirlpool/. The authors are listed in prov/C0V92H.jsonl.
"""Whirlpool (final version, ISO/IEC 10118-3): the cipher W and the Miyaguchi-Preneel iteration.

For study only. This code is not constant time (it indexes a table by secret
bytes) and is not for real data. Whirlpool is not in hashlib; use SHA-512 or
SHA3-512 from hashlib or OpenSSL instead.

The state is an 8 x 8 matrix of bytes, stored as a list of 64 bytes in row
order: entry (i, j) is s[8 * i + j], filled from the block byte by byte. The
S-box is built from the 4-bit mini-boxes E, E^-1 and R of the specification.
Cost: 10 rounds for the cipher and 10 for its key schedule, per 64-byte block.
"""

E = [0x1, 0xB, 0x9, 0xC, 0xD, 0x6, 0xF, 0x3, 0xE, 0x8, 0x7, 0x4, 0xA, 0x2, 0x5, 0x0]
R = [0x7, 0xC, 0xB, 0xD, 0xE, 0x4, 0x9, 0xF, 0x6, 0x3, 0x8, 0xA, 0x2, 0x5, 0x1, 0x0]
E_INV = [E.index(v) for v in range(16)]
ROUNDS = 10
C = [0x01, 0x01, 0x04, 0x01, 0x08, 0x05, 0x02, 0x09]  # first row of the circulant matrix of theta


def sbox_entry(u: int) -> int:
    """S(u): E on the high nibble, E^-1 on the low nibble, R on their XOR, then E and E^-1 again."""
    a, b = E[u >> 4], E_INV[u & 15]
    r = R[a ^ b]
    return (E[a ^ r] << 4) | E_INV[b ^ r]


S = [sbox_entry(u) for u in range(256)]


def gmul(a: int, b: int) -> int:
    """Multiply in GF(2^8) modulo x^8 + x^4 + x^3 + x^2 + 1 (0x11D)."""
    p = 0
    while b:
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11D
        b >>= 1
    return p


MUL = [[gmul(c, x) for x in range(256)] for c in range(10)]


def gamma(s: list[int]) -> list[int]:
    return [S[x] for x in s]


def pi(s: list[int]) -> list[int]:
    """Column j moves down by j places: b[i][j] = a[(i - j) mod 8][j]."""
    return [s[8 * ((i - j) % 8) + j] for i in range(8) for j in range(8)]


def theta(s: list[int]) -> list[int]:
    """Each row times the circulant matrix cir(01, 01, 04, 01, 08, 05, 02, 09)."""
    out = []
    for i in range(8):
        row = s[8 * i:8 * i + 8]
        for j in range(8):
            v = 0
            for k in range(8):
                v ^= MUL[C[(j - k) % 8]][row[k]]
            out.append(v)
    return out


def rho(s: list[int], k: list[int]) -> list[int]:
    """One round: gamma, pi, theta, then XOR with the round key (sigma)."""
    t = theta(pi(gamma(s)))
    return [x ^ y for x, y in zip(t, k)]


def round_constant(r: int) -> list[int]:
    """c^r: row 0 is S[8(r - 1) + j] for j = 0..7, the other rows are 0."""
    return [S[8 * (r - 1) + j] for j in range(8)] + [0] * 56


def w_cipher(key: list[int], block: list[int]) -> list[int]:
    """The block cipher W[key](block), with the key schedule K^r = rho[c^r](K^(r-1))."""
    k = list(key)  # @line L7
    s = [x ^ y for x, y in zip(block, k)]  # @line L8
    for r in range(1, ROUNDS + 1):  # @line L9
        k = rho(k, round_constant(r))  # @line L10
        s = rho(s, k)  # @line L11
    return s  # @line L12


def pad(msg: bytes) -> bytes:
    """A 1 bit, zeros until the length is 256 mod 512 bits, then the bit length in 256 bits, big-endian."""
    n = len(msg)
    return msg + b"\x80" + b"\x00" * ((31 - n) % 64) + (8 * n).to_bytes(32, "big")


def compress(h: list[int], block: bytes) -> list[int]:
    """Miyaguchi-Preneel: H' = W[H](m) XOR H XOR m."""
    m = list(block)  # @line L5
    return [x ^ y ^ z for x, y, z in zip(w_cipher(h, m), h, m)]  # @line L6


def whirlpool(msg: bytes) -> bytes:
    """The 64-byte Whirlpool digest of msg."""
    data = pad(msg)  # @line L1
    h = [0] * 64  # @line L2
    for i in range(0, len(data), 64):  # @line L3
        h = compress(h, data[i:i + 64])  # @line L4
    return bytes(h)  # @line L13
