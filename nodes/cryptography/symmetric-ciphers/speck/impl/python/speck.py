# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/speck/. The authors are listed in prov/7HAM9F.jsonl.

"""The SPECK family of block ciphers (Beaulieu et al., ePrint 2013/404), for study only.

This code is not constant time as Python runs it and must not protect real
data. Use a vetted cipher from libsodium, OpenSSL or a FIPS 140 validated module.

Words are n-bit integers. A block is the pair (x, y), written x first, and a
key is the list of m words written l[m-2], ..., l[0], k[0], as in the paper.
"""

# (block size 2n, key size mn) -> (n, m, rounds T)
PARAMS = {
    (32, 64): (16, 4, 22),
    (48, 72): (24, 3, 22),
    (48, 96): (24, 4, 23),
    (64, 96): (32, 3, 26),
    (64, 128): (32, 4, 27),
    (96, 96): (48, 2, 28),
    (96, 144): (48, 3, 29),
    (128, 128): (64, 2, 32),
    (128, 192): (64, 3, 33),
    (128, 256): (64, 4, 34),
}


def _rotl(x: int, r: int, n: int) -> int:
    return ((x << r) | (x >> (n - r))) & ((1 << n) - 1)


def _rotr(x: int, r: int, n: int) -> int:
    return ((x >> r) | (x << (n - r))) & ((1 << n) - 1)


def _shifts(n: int) -> tuple[int, int]:
    return (7, 2) if n == 16 else (8, 3)


def speck_key_schedule(key_words: list[int], block_bits: int, key_bits: int) -> list[int]:
    """Return the T round keys k[0..T-1]. The schedule reuses the round function with i as the key.

    key_words is [l[m-2], ..., l[0], k[0]]. Cost: Theta(T) word operations.
    """
    n, m, rounds = PARAMS[(block_bits, key_bits)]
    if len(key_words) != m:
        raise ValueError("wrong number of key words")
    alpha, beta = _shifts(n)
    mask = (1 << n) - 1
    words = list(reversed(key_words))
    k = [words[0]]
    ell = words[1:]
    for i in range(rounds - 1):
        ell.append(((k[i] + _rotr(ell[i], alpha, n)) & mask) ^ i)
        k.append(_rotl(k[i], beta, n) ^ ell[i + m - 1])
    return k


def speck_encrypt(block: tuple[int, int], key_words: list[int], block_bits: int, key_bits: int) -> tuple[int, int]:
    """Encrypt the block (x, y).

    Precondition: (block_bits, key_bits) is in PARAMS and words fit in n bits.
    Cost: Theta(T) word operations.
    """
    n = PARAMS[(block_bits, key_bits)][0]
    alpha, beta = _shifts(n)
    mask = (1 << n) - 1
    k = speck_key_schedule(key_words, block_bits, key_bits)  # @line L1
    x, y = block
    for ki in k:  # @line L2
        x = ((_rotr(x, alpha, n) + y) & mask) ^ ki  # @line L3
        y = _rotl(y, beta, n) ^ x  # @line L4
    return x, y  # @line L5


def speck_decrypt(block: tuple[int, int], key_words: list[int], block_bits: int, key_bits: int) -> tuple[int, int]:
    """Invert speck_encrypt. Same preconditions and cost."""
    n = PARAMS[(block_bits, key_bits)][0]
    alpha, beta = _shifts(n)
    mask = (1 << n) - 1
    k = speck_key_schedule(key_words, block_bits, key_bits)  # @line L6
    x, y = block
    for ki in reversed(k):  # @line L7
        y = _rotr(x ^ y, beta, n)  # @line L8
        x = _rotl(((x ^ ki) - y) & mask, alpha, n)  # @line L9
    return x, y  # @line L10
