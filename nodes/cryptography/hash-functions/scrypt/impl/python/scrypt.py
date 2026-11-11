# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scrypt/. The authors are listed in prov/1CM1NZ.jsonl.
"""scrypt as in RFC 7914: PBKDF2-HMAC-SHA256, ROMix, BlockMix and Salsa20/8.

The module has its own Salsa20/8 core, BlockMix, ROMix, HMAC-SHA256 and
PBKDF2 with one iteration. SHA-256 itself comes from hashlib. It also has a
ROMix that stores only every k-th block, to show the time-memory trade-off.

For study only. The code is not constant time and must not protect real data.
It is also about a thousand times slower than C, so real parameters
(N = 2^17, r = 8) take minutes. Use hashlib.scrypt, libsodium
(crypto_pwhash_scryptsalsa208sha256) or the scrypt package instead, or better
Argon2id.
"""

import hashlib
import struct

_M = 0xFFFFFFFF

# The quarter-round positions of Salsa20: four columns, then four rows.
_COLUMNS = [(0, 4, 8, 12), (5, 9, 13, 1), (10, 14, 2, 6), (15, 3, 7, 11)]
_ROWS = [(0, 1, 2, 3), (5, 6, 7, 4), (10, 11, 8, 9), (15, 12, 13, 14)]


def salsa20_8(b: bytes) -> bytes:
    """The Salsa20/8 core of RFC 7914, Section 3: 64 bytes to 64 bytes."""
    inp = struct.unpack("<16I", b)
    x = list(inp)
    for _ in range(4):  # 8 rounds = 4 double rounds
        for group in (_COLUMNS, _ROWS):
            for y0, y1, y2, y3 in group:
                t = (x[y0] + x[y3]) & _M
                x[y1] ^= ((t << 7) | (t >> 25)) & _M
                t = (x[y1] + x[y0]) & _M
                x[y2] ^= ((t << 9) | (t >> 23)) & _M
                t = (x[y2] + x[y1]) & _M
                x[y3] ^= ((t << 13) | (t >> 19)) & _M
                t = (x[y3] + x[y2]) & _M
                x[y0] ^= ((t << 18) | (t >> 14)) & _M
    return struct.pack("<16I", *((x[i] + inp[i]) & _M for i in range(16)))


def _xor(a: bytes, b: bytes) -> bytes:
    return (int.from_bytes(a, "little") ^ int.from_bytes(b, "little")).to_bytes(len(a), "little")


def block_mix(b: bytes, r: int) -> bytes:
    """scryptBlockMix of RFC 7914, Section 4, on 2r blocks of 64 bytes."""
    blocks = [b[64 * i : 64 * i + 64] for i in range(2 * r)]
    x = blocks[2 * r - 1]  # @line L7
    y = []
    for i in range(2 * r):
        x = salsa20_8(_xor(x, blocks[i]))  # @line L7
        y.append(x)  # @line L7
    return b"".join(y[0::2]) + b"".join(y[1::2])  # @line L8


def integerify(x: bytes, n: int) -> int:
    """The last 64-byte block read as a little endian integer, mod N (N a power of 2)."""
    return int.from_bytes(x[-64:-56], "little") % n


def ro_mix(b: bytes, n: int, r: int) -> bytes:
    """scryptROMix of RFC 7914, Section 5. Stores N blocks of 128 r bytes."""
    x = b  # @line L4
    v = []
    for _ in range(n):
        v.append(x)  # @line L4
        x = block_mix(x, r)  # @line L4
    for _ in range(n):
        j = integerify(x, n)  # @line L5
        x = block_mix(_xor(x, v[j]), r)  # @line L5
    return x  # @line L6


def ro_mix_low_memory(b: bytes, n: int, r: int, k: int) -> tuple[bytes, int]:
    """ROMix storing only V[0], V[k], V[2k], ...; returns (output, BlockMix calls)."""
    calls = 0
    x = b
    v = {}
    for i in range(n):
        if i % k == 0:
            v[i] = x
        x = block_mix(x, r)
        calls += 1
    for _ in range(n):
        j = integerify(x, n)
        c = j - j % k
        vj = v[c]
        for _ in range(j - c):  # recompute V[j] from the checkpoint below it
            vj = block_mix(vj, r)
            calls += 1
        x = block_mix(_xor(x, vj), r)
        calls += 1
    return x, calls


def _hmac_sha256(key: bytes, msg: bytes) -> bytes:
    if len(key) > 64:
        key = hashlib.sha256(key).digest()
    key = key.ljust(64, b"\x00")
    inner = hashlib.sha256(bytes(c ^ 0x36 for c in key) + msg).digest()
    return hashlib.sha256(bytes(c ^ 0x5C for c in key) + inner).digest()


def pbkdf2_sha256_1(password: bytes, salt: bytes, dk_len: int) -> bytes:
    """PBKDF2-HMAC-SHA256 with one iteration (RFC 8018, Section 5.2, c = 1)."""
    out = b""
    i = 1
    while len(out) < dk_len:
        out += _hmac_sha256(password, salt + struct.pack(">I", i))
        i += 1
    return out[:dk_len]


def scrypt(password: bytes, salt: bytes, n: int, r: int, p: int, dk_len: int) -> bytes:
    """scrypt(P, S, N, r, p, dkLen) of RFC 7914, Section 6."""
    if n < 2 or n & (n - 1) or r < 1 or p < 1 or dk_len < 1:
        raise ValueError("N must be a power of 2 above 1, and r, p, dkLen must be positive")
    mf = 128 * r
    b = pbkdf2_sha256_1(password, salt, p * mf)  # @line L1
    mixed = [ro_mix(b[i * mf : (i + 1) * mf], n, r) for i in range(p)]  # @line L2
    return pbkdf2_sha256_1(password, b"".join(mixed), dk_len)  # @line L3
