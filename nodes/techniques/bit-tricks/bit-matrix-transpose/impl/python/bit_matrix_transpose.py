# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-matrix-transpose/. The authors are listed in prov/SYYJVH.jsonl.


def transpose(a: list[int]) -> list[int]:
    """Transpose an n x n bit matrix stored one row to a word, in place.

    Bit c of a[r] is the entry in row r and column c. n = len(a) must be a
    power of 2 and every a[r] must be below 2**n. Returns a, which now holds
    the transpose. Cost: lg n rounds of n/2 masked swaps.
    """
    n = len(a)
    if n == 0 or n & (n - 1):
        raise ValueError("n must be a power of 2")
    if any(not 0 <= v < (1 << n) for v in a):
        raise ValueError("each row must fit in n bits")
    j = n // 2
    m = (1 << j) - 1  # @line L1
    while j >= 1:  # @line L2
        for k in range(n):  # @line L3
            if k & j:
                continue
            t = ((a[k] >> j) ^ a[k + j]) & m  # @line L4
            a[k + j] ^= t  # @line L5
            a[k] ^= t << j  # @line L6
        j //= 2
        m ^= m << j  # @line L7
    return a  # @line L8


def transpose8x8(x: int) -> int:
    """Transpose an 8 x 8 bit matrix in one 64-bit word, entry (r, c) at bit 8r + c."""
    for s, m in ((7, 0x00AA00AA00AA00AA), (14, 0x0000CCCC0000CCCC), (28, 0x00000000F0F0F0F0)):
        t = (x ^ (x >> s)) & m
        x = x ^ t ^ (t << s)
    return x
