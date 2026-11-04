# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernighan-popcount/. The authors are listed in prov/TVK2SZ.jsonl.


def kernighan_popcount(x: int) -> int:
    """Return the number of 1-bits of the non-negative integer x.

    Each iteration clears the lowest 1-bit with x & (x - 1), so the loop runs
    exactly popcount(x) times. A negative x has infinitely many 1-bits in
    Python's two's complement view, so it is rejected; mask it to w bits first.
    Cost: popcount(x) iterations, each O(1) word operations for x < 2**w.
    """
    if x < 0:
        raise ValueError("x must be non-negative; mask it to a word size first")
    c = 0  # @line L1
    while x != 0:  # @line L2
        x &= x - 1  # @line L3
        c += 1  # @line L4
    return c  # @line L5
