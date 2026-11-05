# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/murmurhash/. The authors are listed in prov/HXY9Z7.jsonl.

# Constants of MurmurHash3_x86_32, from MurmurHash3.cpp in SMHasher.
C1, C2 = 0xCC9E2D51, 0x1B873593
N = 0xE6546B64
F1, F2 = 0x85EBCA6B, 0xC2B2AE35
MASK = 0xFFFFFFFF


def rotl32(x: int, r: int) -> int:
    return ((x << r) | (x >> (32 - r))) & MASK


def mix(k: int) -> int:
    """The block mix, which does not depend on the seed: rotl(k * c1, 15) * c2 mod 2^32."""
    k = rotl32((k * C1) & MASK, 15)  # @line L12
    return (k * C2) & MASK  # @line L13


def fmix32(h: int) -> int:
    """The finalizer: XOR-shifts and multiplications that make every output bit depend on every bit of h."""
    h ^= h >> 16  # @line L14
    h = (h * F1) & MASK  # @line L15
    h ^= h >> 13  # @line L16
    h = (h * F2) & MASK  # @line L17
    return h ^ (h >> 16)  # @line L18


def murmur3_32(data: bytes | str, seed: int = 0) -> int:
    """MurmurHash3_x86_32 of a byte string (str is encoded as UTF-8) with a 32-bit seed."""
    b = data.encode("utf-8") if isinstance(data, str) else bytes(data)
    n = len(b)
    h = seed & MASK  # @line L1
    for j in range(n // 4):  # @line L2
        k = int.from_bytes(b[4 * j : 4 * j + 4], "little")  # @line L3
        h ^= mix(k)  # @line L4
        h = (rotl32(h, 13) * 5 + N) & MASK  # @line L5
    t = 4 * (n // 4)  # @line L6
    k = int.from_bytes(b[t:], "little")  # @line L7
    if n > t:  # @line L8
        h ^= mix(k)  # @line L9
    h ^= n & MASK  # @line L10
    return fmix32(h)  # @line L11
