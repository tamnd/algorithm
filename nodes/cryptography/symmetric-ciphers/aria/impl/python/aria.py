# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aria/. The authors are listed in prov/8W4VPR.jsonl.
"""ARIA (RFC 5794): key schedule, encryption and decryption of one block.

For study only. This code is not constant time: the S-boxes are tables
indexed by secret bytes, and Python itself leaks timing. Do not use it to
protect real data. Use a validated library, for example OpenSSL, instead.

The names follow RFC 5794 Section 2. A 128-bit value is a Python int read
big-endian from 16 bytes, so byte x0 is the most significant byte. Cost: 12,
14 or 16 rounds for a key of 16, 24 or 32 bytes. Each round has 16 S-box
lookups and one diffusion layer A; the key schedule adds 3 rounds of the
same functions.
"""

MASK128 = (1 << 128) - 1


def _gf_mul(a: int, b: int) -> int:
    """Multiply in GF(2^8) modulo x^8 + x^4 + x^3 + x + 1 (the AES field)."""
    p = 0
    while b:
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B
        b >>= 1
    return p


def _aes_sbox() -> list[int]:
    """SB1 of ARIA is the AES S-box: inversion in GF(2^8), then the AES affine map."""
    inv = [0] * 256
    for x in range(1, 256):
        for y in range(1, 256):
            if _gf_mul(x, y) == 1:
                inv[x] = y
                break
    box = []
    for x in range(256):
        b = inv[x]
        s = 0x63
        for i in range(5):
            s ^= ((b << i) | (b >> (8 - i))) & 0xFF
        box.append(s)
    return box


SB1 = _aes_sbox()

# RFC 5794 Section 2.4.2, the table SB2, row by row.
SB2 = list(bytes.fromhex("""
    e2 4e 54 fc 94 c2 4a cc 62 0d 6a 46 3c 4d 8b d1
    5e fa 64 cb b4 97 be 2b bc 77 2e 03 d3 19 59 c1
    1d 06 41 6b 55 f0 99 69 ea 9c 18 ae 63 df e7 bb
    00 73 66 fb 96 4c 85 e4 3a 09 45 aa 0f ee 10 eb
    2d 7f f4 29 ac cf ad 91 8d 78 c8 95 f9 2f ce cd
    08 7a 88 38 5c 83 2a 28 47 db b8 c7 93 a4 12 53
    ff 87 0e 31 36 21 58 48 01 8e 37 74 32 ca e9 b1
    b7 ab 0c d7 c4 56 42 26 07 98 60 d9 b6 b9 11 40
    ec 20 8c bd a0 c9 84 04 49 23 f1 4f 50 1f 13 dc
    d8 c0 9e 57 e3 c3 7b 65 3b 02 8f 3e e8 25 92 e5
    15 dd fd 17 a9 bf d4 9a 7e c5 39 67 fe 76 9d 43
    a7 e1 d0 f5 68 f2 1b 34 70 05 a3 8a d5 79 86 a8
    30 c6 51 4b 1e a6 27 f6 35 d2 6e 24 16 82 5f da
    e6 75 a2 ef 2c b2 1c 9f 5d 6f 80 0a 72 44 9b 6c
    90 0b 5b 33 7d 5a 52 f3 61 a1 f7 b0 d6 3f 7c 6d
    ed 14 e0 a5 3d 22 b3 f8 89 de 71 1a af ba b5 81
"""))
SB3 = [0] * 256
SB4 = [0] * 256
for _x in range(256):
    SB3[SB1[_x]] = _x
    SB4[SB2[_x]] = _x

# RFC 5794 Section 2.2, the constants from the fractional part of 1/pi.
C1 = 0x517CC1B727220A94FE13ABE8FA9A6EE0
C2 = 0x6DB14ACC9E21C820FF28B1D5EF5DE2B0
C3 = 0xDB92371D2126E9700324977504E8C90E

# Rows of the diffusion layer A of RFC 5794 Section 2.4.3: y_i is the XOR of these x_j.
A_ROWS = [
    (3, 4, 6, 8, 9, 13, 14),
    (2, 5, 7, 8, 9, 12, 15),
    (1, 4, 6, 10, 11, 12, 15),
    (0, 5, 7, 10, 11, 13, 14),
    (0, 2, 5, 8, 11, 14, 15),
    (1, 3, 4, 9, 10, 14, 15),
    (0, 2, 7, 9, 10, 12, 13),
    (1, 3, 6, 8, 11, 12, 13),
    (0, 1, 4, 7, 10, 13, 15),
    (0, 1, 5, 6, 11, 12, 14),
    (2, 3, 5, 6, 8, 13, 15),
    (2, 3, 4, 7, 9, 12, 14),
    (1, 2, 6, 7, 9, 11, 12),
    (0, 3, 6, 7, 8, 10, 13),
    (0, 3, 4, 5, 9, 11, 14),
    (1, 2, 4, 5, 8, 10, 15),
]


def _to_bytes(x: int) -> list[int]:
    return list(x.to_bytes(16, "big"))


def _from_bytes(b: list[int]) -> int:
    return int.from_bytes(bytes(b), "big")


def diffusion(x: int) -> int:
    """The layer A. It is an involution: A(A(x)) = x."""
    b = _to_bytes(x)
    out = []
    for row in A_ROWS:
        v = 0
        for j in row:
            v ^= b[j]  # @line L9
        out.append(v)
    return _from_bytes(out)


def sl1(x: int) -> int:
    b = _to_bytes(x)
    boxes = (SB1, SB2, SB3, SB4)
    return _from_bytes([boxes[i % 4][b[i]] for i in range(16)])  # @line L7


def sl2(x: int) -> int:
    b = _to_bytes(x)
    boxes = (SB3, SB4, SB1, SB2)
    return _from_bytes([boxes[i % 4][b[i]] for i in range(16)])  # @line L8


def fo(d: int, rk: int) -> int:
    return diffusion(sl1(d ^ rk))  # @line L5


def fe(d: int, rk: int) -> int:
    return diffusion(sl2(d ^ rk))  # @line L6


def rotr128(x: int, s: int) -> int:
    return ((x >> s) | (x << (128 - s))) & MASK128


def rotl128(x: int, s: int) -> int:
    return ((x << s) | (x >> (128 - s))) & MASK128


def encryption_round_keys(key: bytes) -> list[int]:
    """Return ek1, ..., ek(n+1) of RFC 5794 Section 2.2."""
    n = len(key)
    if n not in (16, 24, 32):
        raise ValueError("the key must have 16, 24 or 32 bytes")
    k = int.from_bytes(key + bytes(32 - n), "big")
    kl, kr = k >> 128, k & MASK128  # @line L10
    ck = {16: (C1, C2, C3), 24: (C2, C3, C1), 32: (C3, C1, C2)}[n]  # @line L11
    w0 = kl
    w1 = fo(w0, ck[0]) ^ kr  # @line L12
    w2 = fe(w1, ck[1]) ^ w0  # @line L13
    w3 = fo(w2, ck[2]) ^ w1
    rounds = {16: 12, 24: 14, 32: 16}[n]
    ek = []
    for rot in (lambda v: rotr128(v, 19), lambda v: rotr128(v, 31),
                lambda v: rotl128(v, 61), lambda v: rotl128(v, 31)):
        ek += [w0 ^ rot(w1), w1 ^ rot(w2), w2 ^ rot(w3), rot(w0) ^ w3]  # @line L14
    ek.append(w0 ^ rotl128(w1, 19))  # @line L15
    return ek[: rounds + 1]


def decryption_round_keys(key: bytes) -> list[int]:
    ek = encryption_round_keys(key)
    n = len(ek) - 1
    return [ek[n]] + [diffusion(ek[i]) for i in range(n - 1, 0, -1)] + [ek[0]]


def _crypt(x: int, rk: list[int]) -> int:
    n = len(rk) - 1
    for r in range(n - 1):  # @line L1
        if r % 2 == 0:  # rounds 1, 3, 5, ... in the 1-based count of RFC 5794
            x = fo(x, rk[r])  # @line L2
        else:
            x = fe(x, rk[r])  # @line L3
    return sl2(x ^ rk[n - 1]) ^ rk[n]  # @line L4


def encrypt_block(key: bytes, block: bytes) -> bytes:
    if len(block) != 16:
        raise ValueError("the block must have 16 bytes")
    return _crypt(int.from_bytes(block, "big"), encryption_round_keys(key)).to_bytes(16, "big")


def decrypt_block(key: bytes, block: bytes) -> bytes:
    """Decrypt with the same rounds and the decryption round keys dk."""
    if len(block) != 16:
        raise ValueError("the block must have 16 bytes")
    return _crypt(int.from_bytes(block, "big"), decryption_round_keys(key)).to_bytes(16, "big")
