# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sha-1/. The authors are listed in prov/THSRT9.jsonl.
"""SHA-1 (FIPS 180-4, Section 6.1): the padding, the compression function and the hash.

For study only. SHA-1 is broken for collisions (SHAttered, 2017, and a
chosen-prefix collision, 2020), and NIST retires it by 2030. This code is not
constant time and is not for real data. Use SHA-256 or SHA-3 from hashlib or a
FIPS 140 validated module instead.

Words are 32 bits and big-endian. One block is 64 bytes, read as 16 words.
Cost: 80 steps per block, so Theta(n) time for n bytes.
"""

MASK = 0xFFFFFFFF
IV = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)  # FIPS 180-4, Section 5.3.1
K = (0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6)  # FIPS 180-4, Section 4.2.1


def rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (32 - s))) & MASK


def f(t: int, x: int, y: int, z: int) -> int:
    """Ch, Parity, Maj and Parity for steps 0-19, 20-39, 40-59 and 60-79 (FIPS 180-4, Section 4.1.1)."""
    if t < 20:
        return (x & y) ^ (~x & z)
    if t < 40 or t >= 60:
        return x ^ y ^ z
    return (x & y) ^ (x & z) ^ (y & z)


def pad(msg: bytes) -> bytes:
    """Append 0x80, zeros up to 56 mod 64 bytes, and the bit length as 8 bytes, big-endian."""
    n = len(msg)
    return msg + b"\x80" + b"\x00" * ((55 - n) % 64) + (8 * n).to_bytes(8, "big")


def schedule(block: bytes) -> list[int]:
    """The 80 words W_t: 16 from the block, then W_t = ROTL1(W_t-3 ^ W_t-8 ^ W_t-14 ^ W_t-16)."""
    w = [int.from_bytes(block[4 * i:4 * i + 4], "big") for i in range(16)]
    for t in range(16, 80):
        w.append(rotl(w[t - 3] ^ w[t - 8] ^ w[t - 14] ^ w[t - 16], 1))
    return w


def compress(state: tuple[int, ...], block: bytes, trace: list | None = None) -> tuple[int, ...]:
    """The SHA-1 compression function. If trace is a list, the registers after each step are appended."""
    w = schedule(block)  # @line L5
    a, b, c, d, e = state  # @line L6
    for t in range(80):  # @line L7
        tmp = (rotl(a, 5) + f(t, b, c, d) + e + K[t // 20] + w[t]) & MASK  # @line L8
        a, b, c, d, e = tmp, a, rotl(b, 30), c, d  # @line L9
        if trace is not None:
            trace.append((a, b, c, d, e))
    return tuple((u + v) & MASK for u, v in zip(state, (a, b, c, d, e)))  # @line L10


def sha1(msg: bytes) -> bytes:
    """The 20-byte SHA-1 digest of msg."""
    data = pad(msg)  # @line L1
    state = IV  # @line L2
    for i in range(0, len(data), 64):  # @line L3
        state = compress(state, data[i:i + 64])  # @line L4
    return b"".join(x.to_bytes(4, "big") for x in state)  # @line L11
