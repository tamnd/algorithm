# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sha-3/. The authors are listed in prov/J553RH.jsonl.
"""SHA3-224, SHA3-256, SHA3-384 and SHA3-512 (FIPS 202, Section 6.1).

For study only. This code is not constant time and is not for real data. Use
hashlib, OpenSSL or a FIPS 140 validated module instead.

SHA3-d(M) = KECCAK[2d](M || 01, d): the sponge on Keccak-f[1600] with capacity
c = 2d bits and rate r = 1600 - 2d bits. On bytes, the suffix 01 and the first
bit of pad10*1 form the byte 0x06, and the last padding bit is 0x80.
Cost: one call of Keccak-f (24 rounds) per r/8 bytes of input.
"""

MASK = (1 << 64) - 1

RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
# Rotation offsets r[x + 5y] (FIPS 202, Table 2).
RHO = [0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14]


def rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (64 - s))) & MASK if s else x


def keccak_f(a: list[int]) -> list[int]:
    """Keccak-f[1600] = Keccak-p[1600, 24]: theta, rho, pi, chi and iota, 24 times."""
    for rc in RC:
        c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
        d = [c[(x - 1) % 5] ^ rotl(c[(x + 1) % 5], 1) for x in range(5)]
        a = [a[i] ^ d[i % 5] for i in range(25)]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = rotl(a[x + 5 * y], RHO[x + 5 * y])
        a = [b[i] ^ (~b[(i % 5 + 1) % 5 + i - i % 5] & b[(i % 5 + 2) % 5 + i - i % 5] & MASK) for i in range(25)]
        a[0] ^= rc
    return a


def sha3(msg: bytes, d: int) -> bytes:
    """SHA3-d for d in (224, 256, 384, 512)."""
    rate = 200 - 2 * d // 8  # @line L1
    data = bytearray(msg) + b"\x06"  # @line L2
    data += b"\x00" * ((-len(data)) % rate)  # @line L3
    data[-1] |= 0x80  # @line L4
    a = [0] * 25  # @line L5
    for off in range(0, len(data), rate):  # @line L6
        for i in range(rate // 8):  # @line L7
            a[i] ^= int.from_bytes(data[off + 8 * i:off + 8 * i + 8], "little")
        a = keccak_f(a)  # @line L8
    out = b"".join(x.to_bytes(8, "little") for x in a)  # @line L9
    return out[: d // 8]  # @line L10


def sha3_224(msg: bytes) -> bytes:
    return sha3(msg, 224)


def sha3_256(msg: bytes) -> bytes:
    return sha3(msg, 256)


def sha3_384(msg: bytes) -> bytes:
    return sha3(msg, 384)


def sha3_512(msg: bytes) -> bytes:
    return sha3(msg, 512)
