# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/idea/. The authors are listed in prov/M2H1VD.jsonl.
"""IDEA (Lai and Massey 1991): key schedule, encryption and decryption.

For study only. This code is not constant time, and Python itself leaks
timing. Do not use it to protect real data, and do not use a 64-bit block
cipher for new designs. Use AES or ChaCha20 from a validated library instead.

The notation follows Menezes, van Oorschot and Vanstone, Handbook of Applied
Cryptography, Algorithms 7.101 and 7.102 and Note 7.103. A block is four
16-bit words (big-endian), the key is eight 16-bit words. Cost: 8 rounds, each
with 4 multiplications modulo 2^16 + 1, 4 additions modulo 2^16 and 6 XORs,
then an output transformation with 2 multiplications and 2 additions.
"""

MOD = 0x10001  # 2^16 + 1, a prime
MASK16 = 0xFFFF


def mul(a: int, b: int) -> int:
    """Multiplication modulo 2^16 + 1, where the word 0 stands for 2^16."""
    a = a or 0x10000
    b = b or 0x10000
    return (a * b % MOD) & MASK16  # the result 2^16 becomes the word 0  # @line L9


def mul_inv(a: int) -> int:
    """The inverse for mul; 0 (that is 2^16 = -1) and 1 are their own inverses."""
    a = a or 0x10000
    return pow(a, MOD - 2, MOD) & MASK16


def encryption_subkeys(key: bytes) -> list[int]:
    """The 52 subkeys: cut the key into 16-bit words, rotate it left by 25 bits, repeat."""
    if len(key) != 16:
        raise ValueError("the key must have 16 bytes")
    k = int.from_bytes(key, "big")
    out = []
    while len(out) < 52:  # @line L10
        out += [(k >> (112 - 16 * i)) & MASK16 for i in range(8)]  # @line L11
        k = ((k << 25) | (k >> 103)) & ((1 << 128) - 1)  # @line L12
    return out[:52]  # @line L13


def decryption_subkeys(ek: list[int]) -> list[int]:
    """HAC Table 7.11: invert and negate the subkeys, in reverse round order."""
    dk = []
    for r in range(9):  # decryption round r + 1 uses encryption round 9 - r
        j = 6 * (8 - r)
        k1, k4 = mul_inv(ek[j]), mul_inv(ek[j + 3])
        if r in (0, 8):
            k2, k3 = -ek[j + 1] & MASK16, -ek[j + 2] & MASK16
        else:
            k2, k3 = -ek[j + 2] & MASK16, -ek[j + 1] & MASK16
        dk += [k1, k2, k3, k4]
        if r < 8:
            dk += [ek[j - 2], ek[j - 1]]  # K5 and K6 of encryption round 8 - r
    return dk


def crypt_words(x: list[int], sk: list[int], rounds: int = 8) -> list[int]:
    """Algorithm 7.101 with the given 52 subkeys (encryption or decryption)."""
    x1, x2, x3, x4 = x
    for r in range(rounds):  # @line L1
        k = sk[6 * r:6 * r + 6]  # @line L2
        x1 = mul(x1, k[0])  # @line L3
        x2 = (x2 + k[1]) & MASK16
        x3 = (x3 + k[2]) & MASK16
        x4 = mul(x4, k[3])
        t0 = mul(k[4], x1 ^ x3)  # @line L4
        t1 = mul(k[5], (t0 + (x2 ^ x4)) & MASK16)  # @line L5
        t2 = (t0 + t1) & MASK16  # @line L6
        x1 ^= t1  # @line L7
        x4 ^= t2
        x2, x3 = x3 ^ t1, x2 ^ t2
    k = sk[48:52]
    return [mul(x1, k[0]), (x3 + k[1]) & MASK16, (x2 + k[2]) & MASK16, mul(x4, k[3])]  # @line L8


def _words(block: bytes) -> list[int]:
    if len(block) != 8:
        raise ValueError("the block must have 8 bytes")
    return [int.from_bytes(block[2 * i:2 * i + 2], "big") for i in range(4)]


def _bytes(words: list[int]) -> bytes:
    return b"".join(w.to_bytes(2, "big") for w in words)


def encrypt_block(key: bytes, block: bytes) -> bytes:
    return _bytes(crypt_words(_words(block), encryption_subkeys(key)))


def decrypt_block(key: bytes, block: bytes) -> bytes:
    return _bytes(crypt_words(_words(block), decryption_subkeys(encryption_subkeys(key))))
