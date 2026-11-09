# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gray-to-binary-conversion/. The authors are listed in prov/09XZRF.jsonl.


def from_gray(a: int) -> int:
    """Return the rank b of the reflected Gray code a, so that b ^ (b >> 1) == a."""
    if a < 0:
        raise ValueError("a must be non-negative")
    b = 0  # @line L1
    while a != 0:  # @line L2
        b ^= a  # @line L3
        a >>= 1  # @line L4
    return b  # @line L5


def from_gray_fast(a: int, w: int | None = None) -> int:
    """Return the rank of a by shifts of 1, 2, 4, ...; a must be below 2**w.

    When w is None, the bit length of a is used.
    """
    if a < 0:
        raise ValueError("a must be non-negative")
    if w is None:
        w = max(1, a.bit_length())
    if a >> w:
        raise ValueError("a does not fit in w bits")
    s = 1  # @line L6
    while s < w:  # @line L7
        a ^= a >> s  # @line L8
        s <<= 1  # @line L9
    return a  # @line L10


def from_gray_bits(a: list[int]) -> list[int]:
    """Array form: a[0] is the lowest bit; b_j = a_j XOR b_(j+1), from the top down."""
    n = len(a)
    b = [0] * n
    run = 0
    for j in range(n - 1, -1, -1):
        run ^= a[j]
        b[j] = run
    return b
