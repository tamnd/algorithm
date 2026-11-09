# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-to-gray-conversion/. The authors are listed in prov/JSK194.jsonl.


def to_gray(b: int) -> int:
    """Return the reflected Gray code of rank b, that is b XOR (b >> 1)."""
    if b < 0:
        raise ValueError("b must be non-negative")
    return b ^ (b >> 1)  # @line L1


def to_gray_bits(bits: list[int]) -> list[int]:
    """Convert the bits of b (bits[0] is the lowest bit) to the bits of its Gray code."""
    n = len(bits)
    ext = list(bits) + [0]  # @line L2: b_n = 0
    a = [0] * n
    for j in range(n):  # @line L3
        a[j] = ext[j] ^ ext[j + 1]  # @line L4
    return a  # @line L5
