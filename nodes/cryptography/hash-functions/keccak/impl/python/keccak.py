# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/keccak/. The authors are listed in prov/MDJVBV.jsonl.
"""Keccak-f[1600] and the Keccak[c] sponge with the original padding.

For study only. This code is not constant time and is not for real data. Use
hashlib (sha3_256, shake_128), OpenSSL or the XKCP library instead.

The state is a list of 25 lanes of 64 bits; lane (x, y) is A[x + 5 * y], and
byte i of the 200-byte state is byte i % 8 of lane i // 8, little-endian. The
round constants and the rotation offsets are derived here from their
definitions, not copied. Cost: 24 rounds per call of the permutation, each with
about 25 * 5 lane operations.
"""

MASK = (1 << 64) - 1
ROUNDS = 24


def rotl(x: int, s: int) -> int:
    s %= 64
    return ((x << s) | (x >> (64 - s))) & MASK


def rc_bit(t: int) -> int:
    """Bit rc(t) of the LFSR with polynomial x^8 + x^6 + x^5 + x^4 + 1 (FIPS 202, Algorithm 5)."""
    if t % 255 == 0:
        return 1
    r = 1
    for _ in range(t % 255):
        r <<= 1
        if r & 0x100:
            r ^= 0x171
    return r & 1


def round_constants() -> list[int]:
    """RC[i] has bit 2^j - 1 equal to rc(j + 7i) for j = 0..6 (FIPS 202, Algorithm 6)."""
    out = []
    for i in range(ROUNDS):
        rc = 0
        for j in range(7):
            rc |= rc_bit(j + 7 * i) << ((1 << j) - 1)
        out.append(rc)
    return out


def rho_offsets() -> list[int]:
    """r[x + 5y]: start at (1, 0), add (t + 1)(t + 2) / 2 for t = 0..23, step (x, y) -> (y, 2x + 3y)."""
    r = [0] * 25
    x, y = 1, 0
    for t in range(24):
        r[x + 5 * y] = ((t + 1) * (t + 2) // 2) % 64
        x, y = y, (2 * x + 3 * y) % 5
    return r


RC = round_constants()
RHO = rho_offsets()


def theta(a: list[int]) -> list[int]:
    c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
    d = [c[(x - 1) % 5] ^ rotl(c[(x + 1) % 5], 1) for x in range(5)]
    return [a[i] ^ d[i % 5] for i in range(25)]


def rho(a: list[int]) -> list[int]:
    return [rotl(a[i], RHO[i]) for i in range(25)]


def pi(a: list[int]) -> list[int]:
    """A'[x, y] = A[(x + 3y) mod 5, x]."""
    return [a[((x + 3 * y) % 5) + 5 * x] for y in range(5) for x in range(5)]


def chi(a: list[int]) -> list[int]:
    return [a[i] ^ (~a[(i % 5 + 1) % 5 + 5 * (i // 5)] & a[(i % 5 + 2) % 5 + 5 * (i // 5)] & MASK)
            for i in range(25)]


def iota(a: list[int], i: int) -> list[int]:
    return [a[0] ^ RC[i]] + a[1:]


def keccak_f(a: list[int], trace: list | None = None) -> list[int]:
    """Keccak-f[1600]: 24 rounds of theta, rho, pi, chi and iota."""
    for i in range(ROUNDS):  # @line L1
        a = theta(a)  # @line L2
        if trace is not None:
            trace.append(("theta", i, a))
        a = rho(a)  # @line L3
        a = pi(a)  # @line L4
        a = chi(a)  # @line L5
        a = iota(a, i)  # @line L6
        if trace is not None:
            trace.append(("iota", i, a))
    return a  # @line L7


def to_bytes(a: list[int]) -> bytes:
    return b"".join(x.to_bytes(8, "little") for x in a)


def from_bytes(b: bytes) -> list[int]:
    return [int.from_bytes(b[8 * i:8 * i + 8], "little") for i in range(25)]


def sponge(rate: int, msg: bytes, suffix: int, out_len: int) -> bytes:
    """Keccak[c] with rate = 200 - c/8 bytes. suffix holds the domain bits and the first padding bit:
    0x01 for the original Keccak, 0x06 for SHA-3 and 0x1F for SHAKE."""
    data = bytearray(msg) + bytes([suffix])  # @line L8
    data += b"\x00" * ((-len(data)) % rate)  # @line L9
    data[-1] |= 0x80  # @line L10
    a = [0] * 25  # @line L11
    for off in range(0, len(data), rate):  # @line L12
        block = data[off:off + rate] + b"\x00" * (200 - rate)
        a = keccak_f([u ^ v for u, v in zip(a, from_bytes(block))])  # @line L13
    out = b""
    while True:  # @line L14
        out += to_bytes(a)[:rate]  # @line L15
        if len(out) >= out_len:
            return out[:out_len]  # @line L16
        a = keccak_f(a)  # @line L17


def keccak256(msg: bytes) -> bytes:
    """Keccak-256 as submitted to the SHA-3 competition and used by Ethereum: c = 512, suffix 0x01."""
    return sponge(136, msg, 0x01, 32)


def sha3_256(msg: bytes) -> bytes:
    """SHA3-256 of FIPS 202 for comparison: the same sponge with the suffix 01, so the byte 0x06."""
    return sponge(136, msg, 0x06, 32)
