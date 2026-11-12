# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamming-weight/. The authors are listed in prov/N2T38H.jsonl.
"""The Hamming weight of a word, and the weight distribution of a binary linear code.

A binary word of length n is held in a Python integer (bit i is coordinate i).
A binary linear code is given by the k rows of a generator matrix, each an
integer. Words over other alphabets are sequences, with 0 as the zero symbol.
"""

from typing import List, Sequence


def hamming_weight(x: Sequence[int]) -> int:
    """The number of nonzero coordinates of x. Cost: n symbol tests."""
    return sum(1 for v in x if v != 0)


def hamming_weight_bits(x: int) -> int:
    """The number of 1 bits of a non-negative integer, its weight as a binary word."""
    if x < 0:
        raise ValueError("a binary word is a non-negative integer")
    return x.bit_count()


def codewords(rows: Sequence[int]) -> List[int]:
    """All 2^k codewords spanned by the generator rows, in binary reflected Gray code order.

    Consecutive messages in Gray code order differ in one bit, so each new
    codeword is the last one XOR one row. Cost: 2^k XORs of n-bit words.
    Precondition: the rows are linearly independent, or the list has repeats.
    """
    k = len(rows)
    out = [0]
    c = 0
    for i in range(1, 1 << k):
        j = (i & -i).bit_length() - 1  # the bit that changes between gray(i - 1) and gray(i)
        c ^= rows[j]
        out.append(c)
    return out


def weight_distribution(rows: Sequence[int], n: int) -> List[int]:
    """A_0, ..., A_n: the number of codewords of each weight. Cost: 2^k XORs and popcounts."""
    a = [0] * (n + 1)
    for c in codewords(rows):
        if c >> n:
            raise ValueError("a generator row is longer than n")
        a[c.bit_count()] += 1
    return a


def minimum_weight(rows: Sequence[int], n: int) -> int:
    """The least weight of a nonzero codeword; for a linear code this is its minimum distance."""
    a = weight_distribution(rows, n)
    for w in range(1, n + 1):
        if a[w]:
            return w
    raise ValueError("the code has no nonzero codeword")
