# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triple-des/. The authors are listed in prov/1FR1YR.jsonl.
"""TDEA (Triple DES) in the EDE form of NIST SP 800-67, with the DES code it needs.

For study only. This code is not constant time, and NIST disallows TDEA for
encryption after 2023 (SP 800-131A Rev. 2). Do not use it to protect real data.
Use AES from a FIPS 140 validated module, or a library such as libsodium.

Blocks and keys are 64-bit integers, with bit 1 of the standard as the most
significant bit. Cost: 3 DES calls, so 48 Feistel rounds, for each block.
"""

IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
FP = [0] * 64
for _i, _p in enumerate(IP):
    FP[_p - 1] = _i + 1
E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
_S = """
14 4 13 1 2 15 11 8 3 10 6 12 5 9 0 7 0 15 7 4 14 2 13 1 10 6 12 11 9 5 3 8 4 1 14 8 13 6 2 11 15 12 9 7 3 10 5 0 15 12 8 2 4 9 1 7 5 11 3 14 10 0 6 13
15 1 8 14 6 11 3 4 9 7 2 13 12 0 5 10 3 13 4 7 15 2 8 14 12 0 1 10 6 9 11 5 0 14 7 11 10 4 13 1 5 8 12 6 9 3 2 15 13 8 10 1 3 15 4 2 11 6 7 12 0 5 14 9
10 0 9 14 6 3 15 5 1 13 12 7 11 4 2 8 13 7 0 9 3 4 6 10 2 8 5 14 12 11 15 1 13 6 4 9 8 15 3 0 11 1 2 12 5 10 14 7 1 10 13 0 6 9 8 7 4 15 14 3 11 5 2 12
7 13 14 3 0 6 9 10 1 2 8 5 11 12 4 15 13 8 11 5 6 15 0 3 4 7 2 12 1 10 14 9 10 6 9 0 12 11 7 13 15 1 3 14 5 2 8 4 3 15 0 6 10 1 13 8 9 4 5 11 12 7 2 14
2 12 4 1 7 10 11 6 8 5 3 15 13 0 14 9 14 11 2 12 4 7 13 1 5 0 15 10 3 9 8 6 4 2 1 11 10 13 7 8 15 9 12 5 6 3 0 14 11 8 12 7 1 14 2 13 6 15 0 9 10 4 5 3
12 1 10 15 9 2 6 8 0 13 3 4 14 7 5 11 10 15 4 2 7 12 9 5 6 1 13 14 0 11 3 8 9 14 15 5 2 8 12 3 7 0 4 10 1 13 11 6 4 3 2 12 9 5 15 10 11 14 1 7 6 0 8 13
4 11 2 14 15 0 8 13 3 12 9 7 5 10 6 1 13 0 11 7 4 9 1 10 14 3 5 12 2 15 8 6 1 4 11 13 12 3 7 14 10 15 6 8 0 5 9 2 6 11 13 8 1 4 10 7 9 5 0 15 14 2 3 12
13 2 8 4 6 15 11 1 10 9 3 14 5 0 12 7 1 15 13 8 10 3 7 4 12 5 6 11 0 14 9 2 7 11 4 1 9 12 14 2 0 6 10 13 15 3 5 8 2 1 14 7 4 10 8 13 15 12 9 0 3 5 6 11
"""
SBOXES = [[int(v) for v in line.split()] for line in _S.strip().splitlines()]
M28 = (1 << 28) - 1
M32 = (1 << 32) - 1


def _permute(x: int, table: list[int], width: int) -> int:
    out = 0
    for p in table:
        out = (out << 1) | ((x >> (width - p)) & 1)
    return out


def _round_keys(key: int) -> list[int]:
    cd = _permute(key, PC1, 64)
    c, d = cd >> 28, cd & M28
    keys = []
    for s in SHIFTS:
        c = ((c << s) | (c >> (28 - s))) & M28
        d = ((d << s) | (d >> (28 - s))) & M28
        keys.append(_permute((c << 28) | d, PC2, 56))
    return keys


def _f(r: int, k: int) -> int:
    b = _permute(r, E, 32) ^ k
    out = 0
    for i in range(8):
        six = (b >> (42 - 6 * i)) & 0x3F
        out = (out << 4) | SBOXES[i][16 * (((six >> 4) & 2) | (six & 1)) + ((six >> 1) & 0xF)]
    return _permute(out, P, 32)


def _des(block: int, keys: list[int]) -> int:
    x = _permute(block, IP, 64)
    left, right = x >> 32, x & M32
    for k in keys:
        left, right = right, left ^ _f(right, k)
    return _permute((right << 32) | left, FP, 64)


def des_encrypt(key: int, block: int) -> int:
    """The forward DEA transformation F_K of SP 800-67."""
    return _des(block, _round_keys(key))


def des_decrypt(key: int, block: int) -> int:
    """The inverse DEA transformation I_K of SP 800-67."""
    return _des(block, _round_keys(key)[::-1])


def tdea_encrypt(k1: int, k2: int, k3: int, block: int) -> int:
    """O = F_K3(I_K2(F_K1(I))), SP 800-67 Rev. 2 Section 3.1."""
    a = des_encrypt(k1, block)  # @line L1
    b = des_decrypt(k2, a)  # @line L2
    return des_encrypt(k3, b)  # @line L3


def tdea_decrypt(k1: int, k2: int, k3: int, block: int) -> int:
    """O = I_K1(F_K2(I_K3(I))), SP 800-67 Rev. 2 Section 3.1."""
    a = des_decrypt(k3, block)  # @line L4
    b = des_encrypt(k2, a)  # @line L5
    return des_decrypt(k1, b)  # @line L6
