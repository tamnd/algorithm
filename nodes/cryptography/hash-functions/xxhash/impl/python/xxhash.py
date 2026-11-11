# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xxhash/. The authors are listed in prov/SK12VS.jsonl.
"""XXH32 and XXH64 as in the xxHash specification (Yann Collet, xxhash_spec.md, version 0.2.0).

xxh32(data, seed) returns a 32-bit integer and xxh64(data, seed) a 64-bit integer.
The canonical byte form of a result is big-endian.

xxHash is not a cryptographic hash. It gives no protection against collisions or
preimages chosen by an attacker, even with a secret seed. This code is for study
only and is not constant time. Use the xxhash C library or the xxhash Python
package for speed, and a cryptographic hash such as BLAKE2 or SHA-256 for security.
XXH3 and XXH128 are not implemented here.
"""

M32, M64 = (1 << 32) - 1, (1 << 64) - 1

P32_1, P32_2, P32_3, P32_4, P32_5 = 0x9E3779B1, 0x85EBCA77, 0xC2B2AE3D, 0x27D4EB2F, 0x165667B1
P64_1, P64_2, P64_3 = 0x9E3779B185EBCA87, 0xC2B2AE3D27D4EB4F, 0x165667B19E3779F9
P64_4, P64_5 = 0x85EBCA77C2B2AE63, 0x27D4EB2F165667C5


def _rotl(x: int, r: int, w: int, mask: int) -> int:
    return ((x << r) | (x >> (w - r))) & mask


def _le(data: bytes, i: int, n: int) -> int:
    return int.from_bytes(data[i:i + n], "little")


def xxh32(data: bytes, seed: int = 0) -> int:
    n, i = len(data), 0
    seed &= M32
    # @line L1
    if n >= 16:
        acc = [(seed + P32_1 + P32_2) & M32, (seed + P32_2) & M32, seed, (seed - P32_1) & M32]
        # @line L2
        while i + 16 <= n:
            for k in range(4):
                lane = _le(data, i + 4 * k, 4)
                acc[k] = (_rotl((acc[k] + lane * P32_2) & M32, 13, 32, M32) * P32_1) & M32
            i += 16
        # @line L3
        h = (_rotl(acc[0], 1, 32, M32) + _rotl(acc[1], 7, 32, M32)
             + _rotl(acc[2], 12, 32, M32) + _rotl(acc[3], 18, 32, M32)) & M32
    else:
        h = (seed + P32_5) & M32
    # @line L4
    h = (h + n) & M32
    # @line L5
    while i + 4 <= n:
        h = (h + _le(data, i, 4) * P32_3) & M32
        h = (_rotl(h, 17, 32, M32) * P32_4) & M32
        i += 4
    while i < n:
        h = (h + data[i] * P32_5) & M32
        h = (_rotl(h, 11, 32, M32) * P32_1) & M32
        i += 1
    # @line L6
    h ^= h >> 15
    h = (h * P32_2) & M32
    h ^= h >> 13
    h = (h * P32_3) & M32
    h ^= h >> 16
    return h


def _round64(acc: int, lane: int) -> int:
    acc = (acc + lane * P64_2) & M64
    return (_rotl(acc, 31, 64, M64) * P64_1) & M64


def _merge64(h: int, acc: int) -> int:
    h ^= _round64(0, acc)
    return (h * P64_1 + P64_4) & M64


def xxh64(data: bytes, seed: int = 0) -> int:
    n, i = len(data), 0
    seed &= M64
    # @line L1
    if n >= 32:
        acc = [(seed + P64_1 + P64_2) & M64, (seed + P64_2) & M64, seed, (seed - P64_1) & M64]
        # @line L2
        while i + 32 <= n:
            for k in range(4):
                acc[k] = _round64(acc[k], _le(data, i + 8 * k, 8))
            i += 32
        # @line L3
        h = (_rotl(acc[0], 1, 64, M64) + _rotl(acc[1], 7, 64, M64)
             + _rotl(acc[2], 12, 64, M64) + _rotl(acc[3], 18, 64, M64)) & M64
        for a in acc:
            h = _merge64(h, a)
    else:
        h = (seed + P64_5) & M64
    # @line L4
    h = (h + n) & M64
    # @line L5
    while i + 8 <= n:
        h ^= _round64(0, _le(data, i, 8))
        h = (_rotl(h, 27, 64, M64) * P64_1 + P64_4) & M64
        i += 8
    if i + 4 <= n:
        h ^= (_le(data, i, 4) * P64_1) & M64
        h = (_rotl(h, 23, 64, M64) * P64_2 + P64_3) & M64
        i += 4
    while i < n:
        h ^= (data[i] * P64_5) & M64
        h = (_rotl(h, 11, 64, M64) * P64_1) & M64
        i += 1
    # @line L6
    h ^= h >> 33
    h = (h * P64_2) & M64
    h ^= h >> 29
    h = (h * P64_3) & M64
    h ^= h >> 32
    return h


def canonical32(h: int) -> bytes:
    """Step 7: the canonical form is big-endian."""
    # @line L7
    return h.to_bytes(4, "big")


def canonical64(h: int) -> bytes:
    return h.to_bytes(8, "big")
