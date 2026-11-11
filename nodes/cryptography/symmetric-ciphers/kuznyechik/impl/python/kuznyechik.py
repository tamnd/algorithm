# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kuznyechik/. The authors are listed in prov/0Z0TM1.jsonl.
"""Kuznyechik, the 128-bit block cipher of GOST R 34.12-2015 (RFC 7801).

For study only. This code is not constant time: the S-box is a table indexed
by secret bytes, and Python itself leaks timing. Do not use it to protect real
data. Use a validated library that implements GOST R 34.12-2015 instead.

A block is 16 bytes b[0..15]. RFC 7801 writes a block as a_15||...||a_0, so
b[0] is a_15 and b[15] is a_0. Cost: 9 rounds of X, S and L plus a last key
XOR. L is 16 steps of R, and each R step does 16 multiplications in GF(2^8).
The key schedule does 32 rounds of the same LSX map.
"""

# RFC 7801 Section 4.1, the array Pi' = (Pi'(0), ..., Pi'(255)).
PI = [
    252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250,
    218, 35, 197, 4, 77, 233, 119, 240, 219, 147, 46,
    153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 249,
    24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66,
    139, 1, 142, 79, 5, 132, 2, 174, 227, 106, 143,
    160, 6, 11, 237, 152, 127, 212, 211, 31, 235, 52,
    44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253,
    58, 206, 204, 181, 112, 14, 86, 8, 12, 118, 18,
    191, 114, 19, 71, 156, 183, 93, 135, 21, 161, 150,
    41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158,
    178, 177, 50, 117, 25, 61, 255, 53, 138, 126, 109,
    84, 198, 128, 195, 189, 13, 87, 223, 245, 36, 169,
    62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185,
    3, 224, 15, 236, 222, 122, 148, 176, 188, 220, 232,
    40, 80, 78, 51, 10, 74, 167, 151, 96, 115, 30,
    0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65,
    173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165,
    125, 105, 213, 149, 59, 7, 88, 179, 64, 134, 172,
    29, 247, 48, 55, 107, 228, 136, 217, 231, 137, 225,
    27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144,
    202, 216, 133, 97, 32, 113, 103, 164, 45, 43, 9,
    91, 203, 155, 37, 208, 190, 229, 108, 82, 89, 166,
    116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57,
    75, 99, 182,
]
PI_INV = [0] * 256
for _x in range(256):
    PI_INV[PI[_x]] = _x

# RFC 7801 Section 4.2: the coefficients of l for a_15, a_14, ..., a_0.
L_COEF = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]


def gf_mul(a: int, b: int) -> int:
    """Multiply in Q = GF(2)[x]/p(x), p(x) = x^8 + x^7 + x^6 + x + 1."""
    p = 0
    while b:
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x1C3
        b >>= 1
    return p


def l_func(b: list[int]) -> int:
    v = 0
    for c, x in zip(L_COEF, b):
        v ^= gf_mul(c, x)  # @line L9
    return v


def r_step(b: list[int]) -> list[int]:
    """R(a_15||...||a_0) = l(a_15, ..., a_0)||a_15||...||a_1."""
    return [l_func(b)] + b[:15]


def r_inv(b: list[int]) -> list[int]:
    """R^-1(a_15||...||a_0) = a_14||...||a_0||l(a_14, ..., a_0, a_15)."""
    rest = b[1:]
    return rest + [l_func(rest + [b[0]])]


def l_layer(b: list[int]) -> list[int]:
    for _ in range(16):  # @line L6
        b = r_step(b)  # @line L7
    return b  # @line L8


def l_inv(b: list[int]) -> list[int]:
    for _ in range(16):
        b = r_inv(b)
    return b


def s_layer(b: list[int]) -> list[int]:
    return [PI[x] for x in b]


def s_inv(b: list[int]) -> list[int]:
    return [PI_INV[x] for x in b]


def xor(a: list[int], b: list[int]) -> list[int]:
    return [x ^ y for x, y in zip(a, b)]


def lsx(k: list[int], a: list[int]) -> list[int]:
    return l_layer(s_layer(xor(k, a)))


def round_constants() -> list[list[int]]:
    """C_i = L(Vec_128(i)) for i = 1, ..., 32."""
    return [l_layer(list(i.to_bytes(16, "big"))) for i in range(1, 33)]


C = round_constants()


def key_schedule(key: bytes) -> list[list[int]]:
    """Return the round keys K_1, ..., K_10 of RFC 7801 Section 4.4."""
    if len(key) != 32:
        raise ValueError("the key must have 32 bytes")
    a1, a0 = list(key[:16]), list(key[16:])  # @line L10
    keys = [a1, a0]
    for i in range(4):  # @line L11
        for j in range(8):  # @line L12
            a1, a0 = xor(lsx(C[8 * i + j], a1), a0), a1  # @line L13
        keys += [a1, a0]  # @line L14
    return keys  # @line L15


def encrypt_block(key: bytes, block: bytes) -> bytes:
    if len(block) != 16:
        raise ValueError("the block must have 16 bytes")
    ks = key_schedule(key)
    a = list(block)
    for i in range(9):  # @line L1
        a = xor(ks[i], a)  # @line L2
        a = s_layer(a)  # @line L3
        a = l_layer(a)  # @line L4
    return bytes(xor(ks[9], a))  # @line L5


def decrypt_block(key: bytes, block: bytes) -> bytes:
    if len(block) != 16:
        raise ValueError("the block must have 16 bytes")
    ks = key_schedule(key)
    a = xor(ks[9], list(block))
    for i in range(8, -1, -1):
        a = xor(ks[i], s_inv(l_inv(a)))
    return bytes(a)
