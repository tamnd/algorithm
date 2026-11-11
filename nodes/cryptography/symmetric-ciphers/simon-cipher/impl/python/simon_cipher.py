# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simon-cipher/. The authors are listed in prov/D973ES.jsonl.

"""The SIMON family of block ciphers (Beaulieu et al., ePrint 2013/404), for study only.

This code is not constant time as Python runs it and must not protect real
data. Use a vetted cipher from libsodium, OpenSSL or a FIPS 140 validated module.

Words are n-bit integers. A block is the pair (x, y), written x first, and a
key is the list of m words written k[m-1], ..., k[0], as in the paper.
"""

# The five constant sequences z0 .. z4, bit j from the left is z[j].
Z = [
    "11111010001001010110000111001101111101000100101011000011100110",
    "10001110111110010011000010110101000111011111001001100001011010",
    "10101111011100000011010010011000101000010001111110010110110011",
    "11011011101011000110010111100000010010001010011100110100001111",
    "11010001111001101011011000100000010111000011001010010011101111",
]

# (block size 2n, key size mn) -> (n, m, rounds T, sequence j)
PARAMS = {
    (32, 64): (16, 4, 32, 0),
    (48, 72): (24, 3, 36, 0),
    (48, 96): (24, 4, 36, 1),
    (64, 96): (32, 3, 42, 2),
    (64, 128): (32, 4, 44, 3),
    (96, 96): (48, 2, 52, 2),
    (96, 144): (48, 3, 54, 3),
    (128, 128): (64, 2, 68, 2),
    (128, 192): (64, 3, 69, 3),
    (128, 256): (64, 4, 72, 4),
}


def _rotl(x: int, r: int, n: int) -> int:
    return ((x << r) | (x >> (n - r))) & ((1 << n) - 1)


def _rotr(x: int, r: int, n: int) -> int:
    return ((x >> r) | (x << (n - r))) & ((1 << n) - 1)


def _f(x: int, n: int) -> int:
    return (_rotl(x, 1, n) & _rotl(x, 8, n)) ^ _rotl(x, 2, n)


def simon_key_schedule(key_words: list[int], block_bits: int, key_bits: int) -> list[int]:
    """Return the T round keys k[0..T-1].

    key_words is [k[m-1], ..., k[0]]. Cost: Theta(T) word operations.
    """
    n, m, rounds, j = PARAMS[(block_bits, key_bits)]
    if len(key_words) != m:
        raise ValueError("wrong number of key words")
    mask = (1 << n) - 1
    c = mask ^ 3  # 2^n - 4
    k = list(reversed(key_words))
    for i in range(m, rounds):
        tmp = _rotr(k[i - 1], 3, n)
        if m == 4:
            tmp ^= k[i - 3]
        tmp ^= _rotr(tmp, 1, n)
        k.append(c ^ int(Z[j][(i - m) % 62]) ^ k[i - m] ^ tmp)
    return k


def simon_encrypt(block: tuple[int, int], key_words: list[int], block_bits: int, key_bits: int) -> tuple[int, int]:
    """Encrypt the block (x, y).

    Precondition: (block_bits, key_bits) is in PARAMS and words fit in n bits.
    Cost: Theta(T) word operations.
    """
    n = PARAMS[(block_bits, key_bits)][0]
    k = simon_key_schedule(key_words, block_bits, key_bits)  # @line L1
    x, y = block
    for ki in k:  # @line L2
        x, y = y ^ _f(x, n) ^ ki, x  # @line L3
    return x, y  # @line L4


def simon_decrypt(block: tuple[int, int], key_words: list[int], block_bits: int, key_bits: int) -> tuple[int, int]:
    """Invert simon_encrypt. Same preconditions and cost."""
    n = PARAMS[(block_bits, key_bits)][0]
    k = simon_key_schedule(key_words, block_bits, key_bits)  # @line L5
    x, y = block
    for ki in reversed(k):  # @line L6
        x, y = y, x ^ _f(y, n) ^ ki  # @line L7
    return x, y  # @line L8
