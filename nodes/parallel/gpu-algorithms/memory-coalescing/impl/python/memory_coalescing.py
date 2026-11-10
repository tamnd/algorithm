# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/memory-coalescing/.
"""Count the 32-byte sectors that one warp access touches.

The model follows the CUDA Programming Guide v13.5, Section 2.3.4.1: global memory is read and
written in 32-byte transactions (sectors), and one warp instruction needs one transaction for
each distinct sector that its 32 lanes touch. Addresses are byte addresses.
"""

from fractions import Fraction

WARP_SIZE = 32
SECTOR = 32
LINE = 128


def sectors(byte_addrs, word=4):
    """The set of sectors touched by lanes that each access `word` bytes at the given addresses."""
    out = set()
    for a in byte_addrs:
        for b in range(a, a + word):
            out.add(b // SECTOR)
    return out


def lines(byte_addrs, word=4):
    return {s * SECTOR // LINE for s in sectors(byte_addrs, word)}


def warp_addresses(lane_to_index, base=0, word=4, active=range(WARP_SIZE)):
    """Byte addresses of a warp where lane l reads element lane_to_index(l) of an array of words."""
    return [base + word * lane_to_index(l) for l in active]


def transactions(lane_to_index, base=0, word=4, active=range(WARP_SIZE)):
    return len(sectors(warp_addresses(lane_to_index, base, word, active), word))


def efficiency(lane_to_index, base=0, word=4, active=range(WARP_SIZE)):
    """Useful bytes over bytes moved."""
    used = word * len(set(lane_to_index(l) for l in active))
    return Fraction(used, SECTOR * transactions(lane_to_index, base, word, active))


def strided_formula(stride, word=4):
    """Sectors for lane l reading element stride * l, aligned base, word divides 32."""
    return min(WARP_SIZE, (WARP_SIZE - 1) * word * stride // SECTOR + 1)


def expected_random(num_sectors):
    """Expected distinct sectors when 32 lanes pick sectors uniformly and independently."""
    n = Fraction(num_sectors)
    return n * (1 - (1 - 1 / n) ** WARP_SIZE)


def kernel_transactions(n, index_of, word=4, block=128):
    """Total sectors of a 1D kernel in which global thread i reads element index_of(i), i < n."""
    total = 0
    for w in range(-(-n // WARP_SIZE)):
        lanes = [w * WARP_SIZE + l for l in range(WARP_SIZE) if w * WARP_SIZE + l < n]
        total += len(sectors([word * index_of(i) for i in lanes], word))
    return total


def aos_field(stride_words):
    """Lane l reads field 0 of struct l, when each struct has stride_words 4-byte words."""
    return lambda l: stride_words * l
