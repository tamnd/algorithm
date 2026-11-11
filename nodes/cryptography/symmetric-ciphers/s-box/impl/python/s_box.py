# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/s-box/. The authors are listed in prov/FXRB76.jsonl.
"""Measures of an S-box: the DDT, the LAT, the differential uniformity and the nonlinearity.

For study only. An S-box lookup indexed by a secret is not constant time. Do
not use this code to protect real data; use a FIPS 140 validated module or a
library such as libsodium.

An S-box with m input bits and m output bits is a list s of length 2^m.
Cost: the DDT takes Theta(4^m) steps, the LAT takes Theta(8^m) steps here
(Theta(m 4^m) with a fast Walsh-Hadamard transform).
"""

# The 4-bit S-box of Heys, "A tutorial on linear and differential cryptanalysis" (Cryptologia 2002), Table 1.
HEYS_SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]


def gf_mul(a: int, b: int) -> int:
    """Multiply two bytes in GF(2^8) modulo x^8 + x^4 + x^3 + x + 1."""
    p = 0
    while b:
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B
        b >>= 1
    return p


def gf_inv(a: int) -> int:
    """The inverse in GF(2^8) as a^254, with 0 mapped to 0."""
    r, e, x = 1, 254, a
    while e:
        if e & 1:
            r = gf_mul(r, x)
        x = gf_mul(x, x)
        e >>= 1
    return r if a else 0


def aes_affine(b: int) -> int:
    """b'_i = b_i + b_(i+4) + b_(i+5) + b_(i+6) + b_(i+7) + c_i over GF(2), with c = 0x63."""
    out = 0
    for i in range(8):
        bit = (b >> i) ^ (b >> ((i + 4) % 8)) ^ (b >> ((i + 5) % 8)) ^ (b >> ((i + 6) % 8)) ^ (b >> ((i + 7) % 8)) ^ (0x63 >> i)
        out |= (bit & 1) << i
    return out


def aes_sbox() -> list[int]:
    """The AES S-box: the inverse in GF(2^8), then the affine map."""
    return [aes_affine(gf_inv(b)) for b in range(256)]


def parity(x: int) -> int:
    return bin(x).count("1") & 1


def ddt(s: list[int]) -> list[list[int]]:
    """D[a][b] = #{x : s(x XOR a) XOR s(x) = b}."""
    n = len(s)
    t = [[0] * n for _ in range(n)]
    for a in range(n):
        row = t[a]
        for x in range(n):
            row[s[x ^ a] ^ s[x]] += 1
    return t


def differential_uniformity(s: list[int]) -> int:
    """The largest DDT entry with a nonzero input difference."""
    return max(max(row) for row in ddt(s)[1:])


def lat(s: list[int]) -> list[list[int]]:
    """L[a][b] = #{x : a.x = b.s(x)} - 2^m / 2, the bias times 2^m (Heys's convention)."""
    n = len(s)
    t = [[0] * n for _ in range(n)]
    for b in range(n):
        ys = [parity(b & s[x]) for x in range(n)]
        for a in range(n):
            agree = sum(1 for x in range(n) if parity(a & x) == ys[x])
            t[a][b] = agree - n // 2
    return t


def walsh(s: list[int], b: int) -> list[int]:
    """The Walsh spectrum W(a) = sum over x of (-1)^(a.x XOR b.s(x)), by a fast transform."""
    w = [1 - 2 * parity(b & y) for y in s]
    h = 1
    while h < len(w):
        for i in range(0, len(w), 2 * h):
            for j in range(i, i + h):
                u, v = w[j], w[j + h]
                w[j], w[j + h] = u + v, u - v
        h *= 2
    return w


def nonlinearity(s: list[int]) -> int:
    """min over b != 0 and all affine functions of the Hamming distance: 2^(m-1) - max |W| / 2."""
    n = len(s)
    best = max(max(abs(v) for v in walsh(s, b)) for b in range(1, n))
    return n // 2 - best // 2


def sac_matrix(s: list[int], m: int) -> list[list[float]]:
    """P[i][j] = Pr over x that output bit j flips when input bit i flips (Webster and Tavares)."""
    n = len(s)
    return [[sum((s[x] ^ s[x ^ (1 << i)]) >> j & 1 for x in range(n)) / n for j in range(m)] for i in range(m)]
