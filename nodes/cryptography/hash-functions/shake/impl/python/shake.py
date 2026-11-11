# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shake/. The authors are listed in prov/WR6HQ2.jsonl.
"""SHAKE128 and SHAKE256 (FIPS 202, Section 6.2).

For study only. This code is not constant time and is not for real data. Use
hashlib.shake_128 and hashlib.shake_256, OpenSSL or a FIPS 140 validated module
instead.

SHAKE128(M, d) = KECCAK[256](M || 1111, d) and SHAKE256(M, d) = KECCAK[512](M || 1111, d).
On bytes, the suffix 1111 and the first padding bit form the byte 0x1F. The rate
is 168 bytes for SHAKE128 and 136 bytes for SHAKE256. Cost: one Keccak-f call
per rate bytes of input and per rate bytes of output.
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
RHO = [0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14]


def rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (64 - s))) & MASK if s else x


def keccak_f(a: list[int]) -> list[int]:
    """Keccak-f[1600]: 24 rounds of theta, rho, pi, chi and iota."""
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


class Shake:
    """A SHAKE instance: absorb the whole message, then read any number of bytes, in any pieces."""

    def __init__(self, security: int, msg: bytes) -> None:
        self.rate = 200 - security // 4  # @line L1
        data = bytearray(msg) + b"\x1f"  # @line L2
        data += b"\x00" * ((-len(data)) % self.rate)  # @line L3
        data[-1] |= 0x80  # @line L4
        a = [0] * 25
        for off in range(0, len(data), self.rate):  # @line L5
            for i in range(self.rate // 8):
                a[i] ^= int.from_bytes(data[off + 8 * i:off + 8 * i + 8], "little")
            a = keccak_f(a)  # @line L6
        self.state = a
        self.buf = b"".join(x.to_bytes(8, "little") for x in a)[: self.rate]

    def read(self, n: int) -> bytes:
        """The next n bytes of output."""
        out = b""
        while len(out) < n:  # @line L7
            if not self.buf:
                self.state = keccak_f(self.state)  # @line L8
                self.buf = b"".join(x.to_bytes(8, "little") for x in self.state)[: self.rate]
            take = min(n - len(out), len(self.buf))  # @line L9
            out += self.buf[:take]
            self.buf = self.buf[take:]
        return out  # @line L10


def shake128(msg: bytes, n: int) -> bytes:
    """The first n bytes of SHAKE128(msg)."""
    return Shake(128, msg).read(n)


def shake256(msg: bytes, n: int) -> bytes:
    """The first n bytes of SHAKE256(msg)."""
    return Shake(256, msg).read(n)
