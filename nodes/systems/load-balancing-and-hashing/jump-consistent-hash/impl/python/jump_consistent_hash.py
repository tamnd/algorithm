# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jump-consistent-hash/. The authors are listed in prov/F8JS2K.jsonl.

"""Jump consistent hash of Lamping and Veach (2014), as in the paper.

The C code of the paper works on an unsigned 64-bit key and does the
division in double precision. Python integers do not wrap, so each update of
the key is masked to 64 bits; Python floats are IEEE doubles, so the
division gives the same value as the C code.
"""

MASK64 = (1 << 64) - 1
MULT = 2862933555777941757


def jump_consistent_hash(key: int, num_buckets: int) -> int:
    """Return the bucket in 0 .. num_buckets - 1 of a 64-bit key."""
    if num_buckets < 1:
        raise ValueError("num_buckets must be at least 1")
    key &= MASK64
    b, j = -1, 0  # @line L1
    while j < num_buckets:  # @line L2
        b = j  # @line L3
        key = (key * MULT + 1) & MASK64  # @line L4
        j = int((b + 1) * (float(1 << 31) / float((key >> 33) + 1)))  # @line L5
    return b  # @line L6


def jump_trace(key: int, num_buckets: int) -> list[int]:
    """The values of j that the loop computes, for the worked example."""
    key &= MASK64
    b, j = -1, 0
    out = []
    while j < num_buckets:
        b = j
        key = (key * MULT + 1) & MASK64
        j = int((b + 1) * (float(1 << 31) / float((key >> 33) + 1)))
        out.append(j)
    return out


def iterations(key: int, num_buckets: int) -> int:
    """The number of times the loop body runs."""
    return len(jump_trace(key, num_buckets))
