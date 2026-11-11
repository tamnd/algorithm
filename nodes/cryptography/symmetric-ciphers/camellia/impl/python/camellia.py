# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/camellia/. The authors are listed in prov/JV176X.jsonl.
"""Camellia (RFC 3713): key schedule, encryption and decryption of one block.

For study only. This code is not constant time: the S-boxes are tables
indexed by secret bytes, and Python itself leaks timing. Do not use it to
protect real data. Use a validated library, for example OpenSSL, instead.

The names follow RFC 3713 Section 2. A block and a key are bytes, read as
big-endian integers. Cost: 18 rounds of the F-function for a 128-bit key and
24 rounds for a 192-bit or 256-bit key, with 2 or 3 FL and FLINV layers, plus
4 or 6 F-function calls in the key schedule.
"""

MASK32 = 0xFFFFFFFF
MASK64 = 0xFFFFFFFFFFFFFFFF
MASK128 = (1 << 128) - 1

# RFC 3713 Section 2.4.4, SBOX1, in decimal, row by row.
SBOX1 = [
    112, 130, 44, 236, 179, 39, 192, 229, 228, 133, 87, 53, 234, 12, 174, 65,
    35, 239, 107, 147, 69, 25, 165, 33, 237, 14, 79, 78, 29, 101, 146, 189,
    134, 184, 175, 143, 124, 235, 31, 206, 62, 48, 220, 95, 94, 197, 11, 26,
    166, 225, 57, 202, 213, 71, 93, 61, 217, 1, 90, 214, 81, 86, 108, 77,
    139, 13, 154, 102, 251, 204, 176, 45, 116, 18, 43, 32, 240, 177, 132, 153,
    223, 76, 203, 194, 52, 126, 118, 5, 109, 183, 169, 49, 209, 23, 4, 215,
    20, 88, 58, 97, 222, 27, 17, 28, 50, 15, 156, 22, 83, 24, 242, 34,
    254, 68, 207, 178, 195, 181, 122, 145, 36, 8, 232, 168, 96, 252, 105, 80,
    170, 208, 160, 125, 161, 137, 98, 151, 84, 91, 30, 149, 224, 255, 100, 210,
    16, 196, 0, 72, 163, 247, 117, 219, 138, 3, 230, 218, 9, 63, 221, 148,
    135, 92, 131, 2, 205, 74, 144, 51, 115, 103, 246, 243, 157, 127, 191, 226,
    82, 155, 216, 38, 200, 55, 198, 59, 129, 150, 111, 75, 19, 190, 99, 46,
    233, 121, 167, 140, 159, 110, 188, 142, 41, 245, 249, 182, 47, 253, 180, 89,
    120, 152, 6, 106, 231, 70, 113, 186, 212, 37, 171, 66, 136, 162, 141, 250,
    114, 7, 185, 85, 248, 238, 172, 10, 54, 73, 42, 104, 60, 56, 241, 164,
    64, 40, 211, 123, 187, 201, 67, 193, 21, 227, 173, 244, 119, 199, 128, 158,
]


def rotl8(x: int, s: int) -> int:
    return ((x << s) | (x >> (8 - s))) & 0xFF


def rotl32(x: int, s: int) -> int:
    return ((x << s) | (x >> (32 - s))) & MASK32


def rotl128(x: int, s: int) -> int:
    s %= 128
    return ((x << s) | (x >> (128 - s))) & MASK128 if s else x


SBOX2 = [rotl8(SBOX1[x], 1) for x in range(256)]
SBOX3 = [rotl8(SBOX1[x], 7) for x in range(256)]
SBOX4 = [SBOX1[rotl8(x, 1)] for x in range(256)]

SIGMA = [
    0xA09E667F3BCC908B,
    0xB67AE8584CAA73B2,
    0xC6EF372FE94F82BE,
    0x54FF53A5F1D36F1C,
    0x10E527FADE682D1D,
    0xB05688C2B3E6C1FD,
]


def f_function(f_in: int, ke: int) -> int:
    """The F-function: key XOR, eight S-boxes (S-function), then the P-function."""
    x = f_in ^ ke  # @line L9
    t = [(x >> (56 - 8 * i)) & 0xFF for i in range(8)]
    t1 = SBOX1[t[0]]  # @line L10
    t2 = SBOX2[t[1]]
    t3 = SBOX3[t[2]]
    t4 = SBOX4[t[3]]
    t5 = SBOX2[t[4]]
    t6 = SBOX3[t[5]]
    t7 = SBOX4[t[6]]
    t8 = SBOX1[t[7]]
    y1 = t1 ^ t3 ^ t4 ^ t6 ^ t7 ^ t8  # @line L11
    y2 = t1 ^ t2 ^ t4 ^ t5 ^ t7 ^ t8
    y3 = t1 ^ t2 ^ t3 ^ t5 ^ t6 ^ t8
    y4 = t2 ^ t3 ^ t4 ^ t5 ^ t6 ^ t7
    y5 = t1 ^ t2 ^ t6 ^ t7 ^ t8
    y6 = t2 ^ t3 ^ t5 ^ t7 ^ t8
    y7 = t3 ^ t4 ^ t5 ^ t6 ^ t8
    y8 = t1 ^ t4 ^ t5 ^ t6 ^ t7
    out = 0
    for y in (y1, y2, y3, y4, y5, y6, y7, y8):
        out = (out << 8) | y
    return out


def fl(fl_in: int, ke: int) -> int:
    x1, x2 = fl_in >> 32, fl_in & MASK32  # @line L12
    k1, k2 = ke >> 32, ke & MASK32
    x2 ^= rotl32(x1 & k1, 1)  # @line L13
    x1 ^= x2 | k2  # @line L14
    return (x1 << 32) | x2  # @line L15


def fl_inv(fl_in: int, ke: int) -> int:
    y1, y2 = fl_in >> 32, fl_in & MASK32
    k1, k2 = ke >> 32, ke & MASK32
    y1 ^= y2 | k2
    y2 ^= rotl32(y1 & k1, 1)
    return (y1 << 32) | y2


def _halves(x: int, rot: int) -> tuple[int, int]:
    r = rotl128(x, rot)
    return r >> 64, r & MASK64


def key_schedule(key: bytes) -> dict:
    """Return the subkeys kw (4), k (18 or 24) and ke (4 or 6) of RFC 3713 Section 2.2."""
    n = len(key)
    if n not in (16, 24, 32):
        raise ValueError("the key must have 16, 24 or 32 bytes")
    k = int.from_bytes(key, "big")
    if n == 16:
        kl, kr = k, 0  # @line L16
    elif n == 24:
        kl = k >> 64
        low = k & MASK64
        kr = (low << 64) | (~low & MASK64)
    else:
        kl, kr = k >> 128, k & MASK128
    d1, d2 = (kl ^ kr) >> 64, (kl ^ kr) & MASK64
    d2 ^= f_function(d1, SIGMA[0])  # @line L17
    d1 ^= f_function(d2, SIGMA[1])
    d1 ^= kl >> 64  # @line L18
    d2 ^= kl & MASK64
    d2 ^= f_function(d1, SIGMA[2])
    d1 ^= f_function(d2, SIGMA[3])
    ka = (d1 << 64) | d2  # @line L19
    d1, d2 = (ka ^ kr) >> 64, (ka ^ kr) & MASK64
    d2 ^= f_function(d1, SIGMA[4])
    d1 ^= f_function(d2, SIGMA[5])
    kb = (d1 << 64) | d2  # @line L20
    if n == 16:
        # (source, rotation) pairs; each gives two 64-bit halves.
        kw = [*_halves(kl, 0), *_halves(ka, 111)]  # @line L21
        ks = []
        for src, rot in ((ka, 0), (kl, 15), (ka, 15), (kl, 45)):
            ks += _halves(src, rot)
        ks.append(_halves(ka, 45)[0])
        ks.append(_halves(kl, 60)[1])
        ks += _halves(ka, 60)
        for src, rot in ((kl, 94), (ka, 94), (kl, 111)):
            ks += _halves(src, rot)
        ke = [*_halves(ka, 30), *_halves(kl, 77)]
    else:
        kw = [*_halves(kl, 0), *_halves(kb, 111)]
        ks = []
        for src, rot in ((kb, 0), (kr, 15), (ka, 15), (kb, 30), (kl, 45), (ka, 45),
                         (kr, 60), (kb, 60), (kl, 77), (kr, 94), (ka, 94), (kl, 111)):
            ks += _halves(src, rot)
        ke = [*_halves(kr, 30), *_halves(kl, 60), *_halves(ka, 77)]
    return {"kw": kw, "k": ks, "ke": ke}


def _crypt(block: int, kw: list[int], ks: list[int], ke: list[int]) -> int:
    d1, d2 = block >> 64, block & MASK64  # @line L1
    d1 ^= kw[0]  # @line L2
    d2 ^= kw[1]
    for r in range(0, len(ks), 2):  # @line L3
        if r > 0 and r % 6 == 0:  # @line L4
            j = r // 3 - 2
            d1 = fl(d1, ke[j])  # @line L5
            d2 = fl_inv(d2, ke[j + 1])
        d2 ^= f_function(d1, ks[r])  # @line L6
        d1 ^= f_function(d2, ks[r + 1])  # @line L7
    d2 ^= kw[2]  # @line L8
    d1 ^= kw[3]
    return (d2 << 64) | d1


def encrypt_block(key: bytes, block: bytes) -> bytes:
    if len(block) != 16:
        raise ValueError("the block must have 16 bytes")
    s = key_schedule(key)
    c = _crypt(int.from_bytes(block, "big"), s["kw"], s["k"], s["ke"])
    return c.to_bytes(16, "big")


def decrypt_block(key: bytes, block: bytes) -> bytes:
    """Decrypt with the same network and the subkeys in reverse order (RFC 3713 Section 2.3.3)."""
    if len(block) != 16:
        raise ValueError("the block must have 16 bytes")
    s = key_schedule(key)
    kw = [s["kw"][2], s["kw"][3], s["kw"][0], s["kw"][1]]
    m = _crypt(int.from_bytes(block, "big"), kw, s["k"][::-1], s["ke"][::-1])
    return m.to_bytes(16, "big")
