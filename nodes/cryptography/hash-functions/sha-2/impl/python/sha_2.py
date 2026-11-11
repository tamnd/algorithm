# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sha-2/. The authors are listed in prov/CGBNHK.jsonl.
"""SHA-2 (FIPS 180-4): SHA-224, SHA-256, SHA-384, SHA-512, SHA-512/224 and SHA-512/256.

For study only. This code is not constant time and is not for real data.
Use hashlib, OpenSSL or a FIPS 140 validated module instead.

The constants are derived here from the primes, as FIPS 180-4 Sections 4.2.2,
4.2.3 and 5.3 describe, with exact integer roots. The tests compare them with
the digests of the NIST examples. Cost: 64 steps per 64-byte block for the
32-bit functions and 80 steps per 128-byte block for the 64-bit functions.
"""


def primes(k: int) -> list[int]:
    out, n = [], 2
    while len(out) < k:
        if all(n % p for p in out if p * p <= n):
            out.append(n)
        n += 1
    return out


def iroot(x: int, e: int) -> int:
    """floor(x ** (1/e)) for integers, by Newton's method."""
    r = 1 << ((x.bit_length() + e - 1) // e)
    while True:
        s = ((e - 1) * r + x // r ** (e - 1)) // e
        if s >= r:
            break
        r = s
    while r ** e > x:
        r -= 1
    while (r + 1) ** e <= x:
        r += 1
    return r


def frac_root(p: int, e: int, bits: int) -> int:
    """The first `bits` bits of the fractional part of p ** (1/e)."""
    return iroot(p << (e * bits), e) & ((1 << bits) - 1)


P80 = primes(80)
K32 = [frac_root(p, 3, 32) for p in P80[:64]]  # Section 4.2.2
K64 = [frac_root(p, 3, 64) for p in P80]  # Section 4.2.3
IV256 = [frac_root(p, 2, 32) for p in P80[:8]]  # Section 5.3.3
IV512 = [frac_root(p, 2, 64) for p in P80[:8]]  # Section 5.3.5
IV384 = [frac_root(p, 2, 64) for p in P80[8:16]]  # Section 5.3.4
IV224 = [x & 0xFFFFFFFF for x in IV384]  # Section 5.3.2: the second 32 bits

# Word size w, rounds, rotation amounts of Sigma0, Sigma1, sigma0, sigma1 (Section 4.1.2 and 4.1.3).
PARAMS = {
    32: (64, (2, 13, 22), (6, 11, 25), (7, 18, 3), (17, 19, 10)),
    64: (80, (28, 34, 39), (14, 18, 41), (1, 8, 7), (19, 61, 6)),
}


def rotr(x: int, s: int, w: int) -> int:
    return ((x >> s) | (x << (w - s))) & ((1 << w) - 1)


def big_sigma(x: int, r: tuple[int, int, int], w: int) -> int:
    return rotr(x, r[0], w) ^ rotr(x, r[1], w) ^ rotr(x, r[2], w)


def small_sigma(x: int, r: tuple[int, int, int], w: int) -> int:
    return rotr(x, r[0], w) ^ rotr(x, r[1], w) ^ (x >> r[2])


def ch(x: int, y: int, z: int, mask: int) -> int:
    return (x & y) ^ (~x & mask & z)


def maj(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)


def pad(msg: bytes, w: int) -> bytes:
    """Append 0x80, zeros, and the bit length in 2w bits, big-endian, to a multiple of 16w bits."""
    block, lenbytes = 2 * w, w // 4
    n = len(msg)
    zeros = (block - lenbytes - 1 - n) % block
    return msg + b"\x80" + b"\x00" * zeros + (8 * n).to_bytes(lenbytes, "big")


def compress(state: list[int], block: bytes, w: int, trace: list | None = None) -> list[int]:
    """One SHA-256 (w = 32) or SHA-512 (w = 64) compression on a block of 16 words."""
    rounds, s0, s1, ss0, ss1 = PARAMS[w]
    mask = (1 << w) - 1
    k = K32 if w == 32 else K64
    nb = w // 8
    m = [int.from_bytes(block[nb * i:nb * (i + 1)], "big") for i in range(16)]  # @line L5
    for t in range(16, rounds):  # @line L6
        m.append((small_sigma(m[t - 2], ss1, w) + m[t - 7] + small_sigma(m[t - 15], ss0, w) + m[t - 16]) & mask)  # @line L7
    a, b, c, d, e, f, g, h = state  # @line L8
    for t in range(rounds):  # @line L9
        t1 = (h + big_sigma(e, s1, w) + ch(e, f, g, mask) + k[t] + m[t]) & mask  # @line L10
        t2 = (big_sigma(a, s0, w) + maj(a, b, c)) & mask  # @line L11
        a, b, c, d, e, f, g, h = (t1 + t2) & mask, a, b, c, (d + t1) & mask, e, f, g  # @line L12
        if trace is not None:
            trace.append((a, b, c, d, e, f, g, h))
    return [(u + v) & mask for u, v in zip(state, (a, b, c, d, e, f, g, h))]  # @line L13


def iterate(msg: bytes, iv: list[int], w: int) -> list[int]:
    data = pad(msg, w)  # @line L1
    state = list(iv)  # @line L2
    for i in range(0, len(data), 2 * w):  # @line L3
        state = compress(state, data[i:i + 2 * w], w)  # @line L4
    return state


def output(state: list[int], w: int, bits: int) -> bytes:
    """Concatenate the words, big-endian, and keep the leftmost `bits` bits."""
    return b"".join(x.to_bytes(w // 8, "big") for x in state)[: bits // 8]  # @line L14


def sha256(msg: bytes) -> bytes:
    return output(iterate(msg, IV256, 32), 32, 256)


def sha224(msg: bytes) -> bytes:
    return output(iterate(msg, IV224, 32), 32, 224)


def sha512(msg: bytes) -> bytes:
    return output(iterate(msg, IV512, 64), 64, 512)


def sha384(msg: bytes) -> bytes:
    return output(iterate(msg, IV384, 64), 64, 384)


def sha512_t_iv(t: int) -> list[int]:
    """FIPS 180-4, Section 5.3.6: hash the string "SHA-512/t" with the SHA-512 IV XOR a5a5...a5."""
    iv = [x ^ 0xA5A5A5A5A5A5A5A5 for x in IV512]
    return iterate(f"SHA-512/{t}".encode(), iv, 64)


IV512_224 = sha512_t_iv(224)
IV512_256 = sha512_t_iv(256)


def sha512_224(msg: bytes) -> bytes:
    return output(iterate(msg, IV512_224, 64), 64, 224)


def sha512_256(msg: bytes) -> bytes:
    return output(iterate(msg, IV512_256, 64), 64, 256)
