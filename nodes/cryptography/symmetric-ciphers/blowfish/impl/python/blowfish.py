# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blowfish/. The authors are listed in prov/YRNRA5.jsonl.
"""Blowfish (Schneier 1993): key setup, encryption and decryption.

For study only. This code is not constant time: the S-boxes are tables
indexed by secret bytes, and Python itself leaks timing. Do not use it to
protect real data, and do not use a 64-bit block cipher for new designs. Use
AES or ChaCha20 from a validated library instead.

Blowfish fills its P-array (18 words) and its four S-boxes (4 x 256 words)
with the hexadecimal digits of the fractional part of pi, in order. This
module computes those 8336 hex digits with Machin's formula instead of
storing them. A block is two big-endian 32-bit words. Cost: 16 rounds, each
with 4 S-box lookups and 3 additions or XORs; the key setup runs the cipher
521 times to replace the 1042 words of P and S.
"""

MASK32 = 0xFFFFFFFF


def _arctan_inv(x: int, scale: int) -> int:
    """arctan(1/x) * scale, by the alternating series, in exact integers."""
    total = term = scale // x
    x2 = x * x
    n = 1
    sign = -1
    while term:
        term //= x2
        total += sign * (term // (2 * n + 1))
        sign = -sign
        n += 1
    return total


def pi_hex_words(count: int) -> list[int]:
    """The first count 32-bit words of the fractional part of pi."""
    bits = 32 * count + 64
    scale = 1 << bits
    pi = 16 * _arctan_inv(5, scale) - 4 * _arctan_inv(239, scale)
    frac = (pi - 3 * scale) >> 64  # drop guard bits; keep 32 * count bits
    return [(frac >> (32 * (count - 1 - i))) & MASK32 for i in range(count)]


_PI = pi_hex_words(18 + 4 * 256)
P_INIT = _PI[:18]
S_INIT = [_PI[18 + 256 * k:18 + 256 * (k + 1)] for k in range(4)]


class Blowfish:
    def __init__(self, key: bytes) -> None:
        # Schneier's paper allows 32 to 448 bits (4 to 56 bytes). The setup
        # works for 1 to 72 bytes, and Eric Young's test set uses 1 to 24.
        if not 1 <= len(key) <= 72:
            raise ValueError("the key must have 1 to 72 bytes")
        self.p = list(P_INIT)  # @line L11
        self.s = [list(box) for box in S_INIT]
        # Step 1: XOR P with the key, cycled, 32 bits at a time.
        j = 0
        for i in range(18):  # @line L12
            d = 0
            for _ in range(4):
                d = (d << 8) | key[j]
                j = (j + 1) % len(key)
            self.p[i] ^= d  # @line L13
        # Step 2: replace P and S with outputs of the cipher itself.
        left = right = 0  # @line L14
        for i in range(0, 18, 2):  # @line L15
            left, right = self._encrypt(left, right)  # @line L16
            self.p[i], self.p[i + 1] = left, right  # @line L17
        for box in self.s:
            for i in range(0, 256, 2):
                left, right = self._encrypt(left, right)
                box[i], box[i + 1] = left, right

    def _f(self, x: int) -> int:
        s0, s1, s2, s3 = self.s
        h = (s0[x >> 24] + s1[(x >> 16) & 0xFF]) & MASK32
        return ((h ^ s2[(x >> 8) & 0xFF]) + s3[x & 0xFF]) & MASK32  # @line L10

    def _encrypt(self, left: int, right: int) -> tuple[int, int]:
        for i in range(16):  # @line L2
            left ^= self.p[i]  # @line L3
            right ^= self._f(left)  # @line L4
            left, right = right, left  # @line L5
        left, right = right, left  # @line L6
        right ^= self.p[16]  # @line L7
        left ^= self.p[17]  # @line L8
        return left, right  # @line L9

    def _decrypt(self, left: int, right: int) -> tuple[int, int]:
        for i in range(17, 1, -1):
            left ^= self.p[i]
            right ^= self._f(left)
            left, right = right, left
        left, right = right, left
        right ^= self.p[1]
        left ^= self.p[0]
        return left, right

    def encrypt_block(self, block: bytes) -> bytes:
        if len(block) != 8:
            raise ValueError("the block must have 8 bytes")
        left, right = self._encrypt(int.from_bytes(block[:4], "big"), int.from_bytes(block[4:], "big"))  # @line L1
        return left.to_bytes(4, "big") + right.to_bytes(4, "big")

    def decrypt_block(self, block: bytes) -> bytes:
        if len(block) != 8:
            raise ValueError("the block must have 8 bytes")
        left, right = self._decrypt(int.from_bytes(block[:4], "big"), int.from_bytes(block[4:], "big"))
        return left.to_bytes(4, "big") + right.to_bytes(4, "big")
