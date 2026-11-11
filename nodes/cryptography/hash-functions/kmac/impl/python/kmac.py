# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kmac/. The authors are listed in prov/J3VNX8.jsonl.
"""KMAC128 and KMAC256 (NIST SP 800-185, Section 4) on a pure Python Keccak.

hashlib has SHAKE128 and SHAKE256, but not cSHAKE with a function name N and a
customization string S, so this file implements Keccak-f[1600] (FIPS 202,
Section 3), the sponge, cSHAKE and KMAC. Plain SHAKE is checked against hashlib
in the tests.

For study only. The code is not constant time and must not protect real data.
Use a vetted library, for example a FIPS 140 validated module or the KMAC of
OpenSSL 3, instead.
"""

MASK64 = (1 << 64) - 1

# FIPS 202, Section 3.2.5: the round constants of iota.
RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]

# FIPS 202, Section 3.2.2: the rotation offsets of rho, indexed [x][y].
ROT = [
    [0, 36, 3, 41, 18],
    [1, 44, 10, 45, 2],
    [62, 6, 43, 15, 61],
    [28, 55, 25, 21, 56],
    [27, 20, 39, 8, 14],
]


def _rotl(v: int, n: int) -> int:
    n %= 64
    return ((v << n) | (v >> (64 - n))) & MASK64 if n else v


def keccak_f1600(a: list[int]) -> list[int]:
    """The permutation Keccak-f[1600] on 25 lanes; lane (x, y) is a[x + 5 y]."""
    for rnd in range(24):
        c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]  # theta
        d = [c[(x - 1) % 5] ^ _rotl(c[(x + 1) % 5], 1) for x in range(5)]
        a = [a[i] ^ d[i % 5] for i in range(25)]
        b = [0] * 25
        for x in range(5):  # rho and pi
            for y in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = _rotl(a[x + 5 * y], ROT[x][y])
        a = [b[i] ^ (~b[(i % 5 + 1) % 5 + 5 * (i // 5)] & b[(i % 5 + 2) % 5 + 5 * (i // 5)]) for i in range(25)]  # chi
        a[0] ^= RC[rnd]  # iota
    return a


def sponge(data: bytes, rate: int, suffix: int, out_len: int) -> bytes:
    """Keccak[c] with rate `rate` bytes, on data followed by the domain bits in `suffix`.

    `suffix` holds the domain bits and the first bit of pad10*1, as one byte in
    the little-endian bit order of FIPS 202: 0x06 for SHA-3, 0x1F for SHAKE,
    0x04 for cSHAKE.
    """
    p = bytearray(data)
    p.append(suffix)  # @line L4
    while len(p) % rate:
        p.append(0)
    p[-1] |= 0x80  # @line L4
    state = [0] * 25
    for off in range(0, len(p), rate):  # @line L5
        block = p[off : off + rate]
        for i in range(rate // 8):
            state[i] ^= int.from_bytes(block[8 * i : 8 * i + 8], "little")
        state = keccak_f1600(state)  # @line L5
    out = bytearray()
    while True:  # @line L6
        out += b"".join(state[i].to_bytes(8, "little") for i in range(rate // 8))
        if len(out) >= out_len:
            return bytes(out[:out_len])  # @line L7
        state = keccak_f1600(state)  # @line L6


def shake128(data: bytes, out_len: int) -> bytes:
    return sponge(data, 168, 0x1F, out_len)


def shake256(data: bytes, out_len: int) -> bytes:
    return sponge(data, 136, 0x1F, out_len)


def sha3_256(data: bytes) -> bytes:
    return sponge(data, 136, 0x06, 32)


def left_encode(x: int) -> bytes:
    """SP 800-185 Section 2.3.1: the byte count n, then x in n big-endian bytes."""
    n = max(1, (x.bit_length() + 7) // 8)
    return bytes([n]) + x.to_bytes(n, "big")


def right_encode(x: int) -> bytes:
    """SP 800-185 Section 2.3.1: x in n big-endian bytes, then n."""
    n = max(1, (x.bit_length() + 7) // 8)
    return x.to_bytes(n, "big") + bytes([n])


def encode_string(s: bytes) -> bytes:
    """SP 800-185 Section 2.3.2: left_encode of the bit length, then the string."""
    return left_encode(8 * len(s)) + s


def bytepad(x: bytes, w: int) -> bytes:
    """SP 800-185 Section 2.3.3: left_encode(w) || x, padded with zero bytes to a multiple of w."""
    z = left_encode(w) + x
    return z + bytes((-len(z)) % w)


def cshake(x: bytes, out_len: int, n: bytes, s: bytes, rate: int) -> bytes:
    """cSHAKE128 (rate 168) or cSHAKE256 (rate 136), SP 800-185 Section 3.3."""
    if not n and not s:
        return sponge(x, rate, 0x1F, out_len)  # plain SHAKE
    prefix = bytepad(encode_string(n) + encode_string(s), rate)  # @line L2
    return sponge(prefix + x, rate, 0x04, out_len)  # @line L3


def _kmac(key: bytes, x: bytes, out_len: int, s: bytes, rate: int, xof: bool) -> bytes:
    encoded_len = 0 if xof else 8 * out_len
    new_x = bytepad(encode_string(key), rate) + x + right_encode(encoded_len)  # @line L1
    return cshake(new_x, out_len, b"KMAC", s, rate)


def kmac128(key: bytes, x: bytes, out_len: int, s: bytes = b"") -> bytes:
    """KMAC128(K, X, L, S) with L = 8 * out_len bits."""
    return _kmac(key, x, out_len, s, 168, xof=False)


def kmac256(key: bytes, x: bytes, out_len: int, s: bytes = b"") -> bytes:
    """KMAC256(K, X, L, S) with L = 8 * out_len bits."""
    return _kmac(key, x, out_len, s, 136, xof=False)


def kmacxof128(key: bytes, x: bytes, out_len: int, s: bytes = b"") -> bytes:
    """KMACXOF128: the same with right_encode(0), so the output length is not bound in."""
    return _kmac(key, x, out_len, s, 168, xof=True)


def kmacxof256(key: bytes, x: bytes, out_len: int, s: bytes = b"") -> bytes:
    return _kmac(key, x, out_len, s, 136, xof=True)
