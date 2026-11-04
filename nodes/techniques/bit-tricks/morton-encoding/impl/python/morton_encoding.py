# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morton-encoding/. The authors are listed in prov/JEHNP6.jsonl.

MASK64 = (1 << 64) - 1
MASK32 = (1 << 32) - 1


def spread(x: int) -> int:
    """Move bit i of a 32-bit x to bit 2i of a 64-bit word.

    Higher bits of x are ignored. Cost: 5 stages of 3 word operations.
    """
    x &= MASK32
    x = (x | (x << 16)) & 0x0000FFFF0000FFFF  # @line L1
    x = (x | (x << 8)) & 0x00FF00FF00FF00FF  # @line L2
    x = (x | (x << 4)) & 0x0F0F0F0F0F0F0F0F  # @line L3
    x = (x | (x << 2)) & 0x3333333333333333  # @line L4
    x = (x | (x << 1)) & 0x5555555555555555  # @line L5
    return x  # @line L6


def morton_encode(x: int, y: int) -> int:
    """Return the 64-bit Morton code of (x, y): x in the even bits, y in the odd bits."""
    return spread(x) | ((spread(y) << 1) & MASK64)  # @line L7


def compact(z: int) -> int:
    """Inverse of spread: move bit 2i of a 64-bit z to bit i; odd bits are ignored."""
    z &= 0x5555555555555555
    z = (z ^ (z >> 1)) & 0x3333333333333333
    z = (z ^ (z >> 2)) & 0x0F0F0F0F0F0F0F0F
    z = (z ^ (z >> 4)) & 0x00FF00FF00FF00FF
    z = (z ^ (z >> 8)) & 0x0000FFFF0000FFFF
    z = (z ^ (z >> 16)) & 0x00000000FFFFFFFF
    return z


def morton_decode(z: int) -> tuple[int, int]:
    """Return (x, y) with morton_encode(x, y) == z, for 0 <= z < 2**64."""
    z &= MASK64
    return compact(z), compact(z >> 1)


def spread3(x: int) -> int:
    """Move bit i of a 10-bit x to bit 3i of a 32-bit word."""
    x &= 0x3FF
    x = (x | (x << 16)) & 0x030000FF
    x = (x | (x << 8)) & 0x0300F00F
    x = (x | (x << 4)) & 0x030C30C3
    x = (x | (x << 2)) & 0x09249249
    return x


def morton_encode3(x: int, y: int, z: int) -> int:
    """Return the 30-bit Morton code of three 10-bit coordinates."""
    return spread3(x) | (spread3(y) << 1) | (spread3(z) << 2)
