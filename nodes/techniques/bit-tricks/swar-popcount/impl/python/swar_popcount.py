# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swar-popcount/. The authors are listed in prov/W1VS75.jsonl.


def _repeat(pattern: int, period: int, w: int) -> int:
    """Return the w-bit word that repeats the period-bit pattern."""
    m = 0
    for i in range(0, w, period):
        m |= pattern << i
    return m


def swar_popcount(x: int, w: int = 64) -> int:
    """Return the number of 1-bits of the unsigned w-bit word x.

    Precondition: w is 8, 16, 32, 64 or 128 and 0 <= x < 2**w. All arithmetic
    is reduced modulo 2**w, as with an unsigned C type. Cost: 12 word
    operations, with no branch that depends on x.
    """
    if w not in (8, 16, 32, 64, 128):
        raise ValueError("w must be 8, 16, 32, 64 or 128")
    if not 0 <= x < (1 << w):
        raise ValueError("x must be an unsigned w-bit word")
    mask = (1 << w) - 1
    m1 = _repeat(0b01, 2, w)
    m2 = _repeat(0b0011, 4, w)
    m4 = _repeat(0b00001111, 8, w)
    h = _repeat(0b00000001, 8, w)
    x = (x - ((x >> 1) & m1)) & mask  # @line L1
    x = ((x & m2) + ((x >> 2) & m2)) & mask  # @line L2
    x = (x + (x >> 4)) & m4  # @line L3
    return ((x * h) & mask) >> (w - 8)  # @line L4
