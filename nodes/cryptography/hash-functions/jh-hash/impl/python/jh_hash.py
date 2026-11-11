# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jh-hash/. The authors are listed in prov/TGYCB3.jsonl.
"""JH, the final-round version JH42 (specification of 16 January 2011), for study only.

This follows the hardware description of Sections 4 to 6, one 4-bit element at a
time, so it is slow. Bit 0 of a word is its most significant bit. The code hashes
whole bytes only and is not constant time: the s-boxes are table lookups.
"""

from math import isqrt

S0 = (9, 0, 4, 11, 13, 12, 3, 15, 1, 10, 2, 6, 7, 5, 8, 14)  # Section 4.1
S1 = (3, 12, 6, 13, 5, 7, 1, 9, 15, 2, 0, 4, 11, 10, 14, 8)
SBOXES = (S0, S1)
ROUNDS = 42  # 6 (d - 1) with d = 8
SIZES = (224, 256, 384, 512)


def linear(a: int, b: int) -> tuple[int, int]:
    """L of Section 4.2 on two 4-bit words, with A0 the most significant bit of A."""
    a0, a1, a2, a3 = (a >> 3) & 1, (a >> 2) & 1, (a >> 1) & 1, a & 1
    b0, b1, b2, b3 = (b >> 3) & 1, (b >> 2) & 1, (b >> 1) & 1, b & 1
    d0, d1, d2, d3 = b0 ^ a1, b1 ^ a2, b2 ^ a3 ^ a0, b3 ^ a0
    c0, c1, c2, c3 = a0 ^ d1, a1 ^ d2, a2 ^ d3 ^ d0, a3 ^ d0
    return (c0 << 3) | (c1 << 2) | (c2 << 1) | c3, (d0 << 3) | (d1 << 2) | (d2 << 1) | d3


def permute(a: list[int]) -> list[int]:
    """P_d = phi_d o P'_d o pi_d of Section 4.3 on 2^d elements."""
    n = len(a)
    b = list(a)
    for i in range(0, n, 4):  # pi_d: swap the last two of every four
        b[i + 2], b[i + 3] = a[i + 3], a[i + 2]
    c = b[0::2] + b[1::2]  # P'_d: even places to the first half, odd places to the second
    e = list(c)
    for i in range(n // 4, n // 2):  # phi_d: swap pairs in the second half
        e[2 * i], e[2 * i + 1] = c[2 * i + 1], c[2 * i]
    return e


def round_function(a: list[int], const: int) -> list[int]:
    """R_d of Section 4.4. Bit i of const (from the most significant end) picks S0 or S1."""
    n = len(a)
    v = [SBOXES[(const >> (n - 1 - i)) & 1][a[i]] for i in range(n)]  # @line L6
    w = []
    for i in range(0, n, 2):  # @line L7
        w.extend(linear(v[i], v[i + 1]))
    return permute(w)  # @line L8


def _nibbles(x: int, count: int) -> list[int]:
    return [(x >> (4 * (count - 1 - i))) & 15 for i in range(count)]


def _join(q: list[int]) -> int:
    x = 0
    for t in q:
        x = (x << 4) | t
    return x


def round_constants() -> list[int]:
    """Section 4.6: C_0 = floor((sqrt(2) - 1) 2^256), C_r = R_6(C_(r-1), 0)."""
    c = [isqrt(2 << 512) - (1 << 256)]
    for _ in range(1, ROUNDS):
        c.append(_join(round_function(_nibbles(c[-1], 64), 0)))
    return c


CONSTANTS = round_constants()


def _group(a: int) -> list[int]:
    """Section 4.5 step 1: element 2i takes bits i, i + 256, i + 512, i + 768."""
    bit = [(a >> (1023 - j)) & 1 for j in range(1024)]
    q = [0] * 256
    for i in range(128):
        q[2 * i] = (bit[i] << 3) | (bit[i + 256] << 2) | (bit[i + 512] << 1) | bit[i + 768]
        k = i + 128
        q[2 * i + 1] = (bit[k] << 3) | (bit[k + 256] << 2) | (bit[k + 512] << 1) | bit[k + 768]
    return q


def _degroup(q: list[int]) -> int:
    bit = [0] * 1024
    for i in range(128):
        for k, t in ((i, q[2 * i]), (i + 128, q[2 * i + 1])):
            bit[k], bit[k + 256], bit[k + 512], bit[k + 768] = (
                (t >> 3) & 1, (t >> 2) & 1, (t >> 1) & 1, t & 1)
    x = 0
    for b in bit:
        x = (x << 1) | b
    return x


def e8(a: int) -> int:
    """The bijection E_8 on a 1024-bit integer (bit 0 is the most significant)."""
    q = _group(a)
    for r in range(ROUNDS):
        q = round_function(q, CONSTANTS[r])
    return _degroup(q)


def compress(h: int, m: int) -> int:
    """F_8 of Section 5.1: h has 1024 bits, m has 512 bits."""
    a = h ^ (m << 512)  # @line L5
    return e8(a) ^ m  # @line L9


def pad(msg: bytes) -> bytes:
    """Section 6.1 for whole bytes: 0x80, zero bytes, then the 128-bit bit length."""
    zeros = 64 + (-len(msg)) % 64 - 17
    return msg + b"\x80" + bytes(zeros) + (8 * len(msg)).to_bytes(16, "big")


def jh(msg: bytes, n: int = 256) -> bytes:
    """JH-n for n in 224, 256, 384 and 512."""
    if n not in SIZES:
        raise ValueError("n must be 224, 256, 384 or 512")
    h = compress(n << 1008, 0)  # @line L1
    padded = pad(msg)  # @line L2
    for k in range(0, len(padded), 64):
        h = compress(h, int.from_bytes(padded[k:k + 64], "big"))  # @line L3
    return h.to_bytes(128, "big")[128 - n // 8:]  # @line L4


def jh256(msg: bytes) -> bytes:
    return jh(msg, 256)


def jh512(msg: bytes) -> bytes:
    return jh(msg, 512)
