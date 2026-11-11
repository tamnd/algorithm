# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/enumerative-coding/. The authors are listed in prov/HHYSRG.jsonl.

"""Enumerative coding of binary sequences (Lynch, Davisson, Cover).

A binary sequence of length n with k ones is coded as k, in ceil(lg(n + 1))
bits, followed by its rank among the C(n, k) sequences of length n and weight
k in lexicographic order (0 before 1), in ceil(lg C(n, k)) bits.

The rank is Cover's formula: the sum, over the positions i (1-based) that hold
a 1, of C(n - i, j), where j is the number of ones at positions i to n.
`cover_rank` and `cover_unrank` give the general form for any set given by a
counting function; `rank_multiset` and `unrank_multiset` apply it to the
sequences of a fixed type over a larger alphabet.
"""

from collections import Counter
from math import comb, factorial
from typing import Callable, Sequence


def rank(bits: Sequence[int]) -> tuple[int, int]:
    """Return (k, r): the weight and the lexicographic rank among sequences of that weight."""
    n = len(bits)
    k = sum(bits)  # @line L1
    j, r = k, 0
    for i in range(1, n + 1):  # @line L2
        b = bits[i - 1]
        if b not in (0, 1):
            raise ValueError("bits must be 0 or 1")
        if b == 1:  # @line L3
            r += comb(n - i, j)  # @line L4
            j -= 1  # @line L5
    return k, r  # @line L6


def unrank(n: int, k: int, r: int) -> list[int]:
    """The sequence of length n and weight k with rank r."""
    if not 0 <= k <= n or not 0 <= r < comb(n, k):
        raise ValueError("no such sequence")
    j = k  # @line L7
    out = []
    for i in range(1, n + 1):  # @line L8
        c = comb(n - i, j)  # @line L9
        if r >= c:
            out.append(1)  # @line L10
            r -= c
            j -= 1
        else:
            out.append(0)  # @line L11
    return out  # @line L12


def _width(m: int) -> int:
    """ceil(lg m) for m >= 1: the bits needed for a number in [0, m)."""
    return (m - 1).bit_length()


def code_length(n: int, k: int) -> int:
    """The length of the two-part code: ceil(lg(n + 1)) + ceil(lg C(n, k))."""
    return _width(n + 1) + _width(comb(n, k))


def encode(bits: Sequence[int]) -> list[int]:
    """The two-part code as a list of bits: k, then the rank."""
    n = len(bits)
    k, r = rank(bits)
    wk, wr = _width(n + 1), _width(comb(n, k))  # @line L13
    return [(k >> (wk - 1 - t)) & 1 for t in range(wk)] + [(r >> (wr - 1 - t)) & 1 for t in range(wr)]


def decode(code: Sequence[int], n: int) -> list[int]:
    """Read k and the rank from the code and unrank."""
    wk = _width(n + 1)
    k = int("".join(map(str, code[:wk])) or "0", 2)  # @line L14
    wr = _width(comb(n, k))
    if len(code) != wk + wr:
        raise ValueError("wrong code length")
    r = int("".join(map(str, code[wk:])) or "0", 2)
    return unrank(n, k, r)


def cover_rank(x: Sequence[int], alphabet: int, count: Callable[[tuple], int]) -> int:
    """Cover's rank of x in a set S of sequences of length len(x).

    count(prefix) is the number of sequences in S that start with prefix.
    The rank is the sum over i of count(x_1 .. x_{i-1} c) over the symbols c < x_i.
    """
    r = 0
    for i, s in enumerate(x):
        prefix = tuple(x[:i])
        r += sum(count(prefix + (c,)) for c in range(s))
    return r


def cover_unrank(n: int, r: int, alphabet: int, count: Callable[[tuple], int]) -> list[int]:
    prefix: tuple = ()
    for _ in range(n):
        for c in range(alphabet):
            m = count(prefix + (c,))
            if r < m:
                prefix += (c,)
                break
            r -= m
        else:
            raise ValueError("rank out of range")
    return list(prefix)


def multinomial(counts: Sequence[int]) -> int:
    """(sum counts)! / prod(count!)."""
    m = factorial(sum(counts))
    for c in counts:
        m //= factorial(c)
    return m


def type_counter(n: int, counts: Sequence[int]) -> Callable[[tuple], int]:
    """The counting function of the type class with the given symbol counts."""
    def count(prefix: tuple) -> int:
        left = list(counts)
        for s in prefix:
            left[s] -= 1
            if left[s] < 0:
                return 0
        return multinomial(left)
    return count


def rank_multiset(seq: Sequence[int], alphabet: int) -> tuple[list[int], int]:
    """The type (symbol counts) of seq and its lexicographic rank in its type class."""
    cnt = Counter(seq)
    counts = [cnt.get(c, 0) for c in range(alphabet)]
    return counts, cover_rank(seq, alphabet, type_counter(len(seq), counts))


def unrank_multiset(counts: Sequence[int], r: int) -> list[int]:
    return cover_unrank(sum(counts), r, len(counts), type_counter(sum(counts), counts))
