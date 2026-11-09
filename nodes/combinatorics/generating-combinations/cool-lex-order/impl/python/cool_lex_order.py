# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cool-lex-order/. The authors are listed in prov/T6JKA4.jsonl.

from collections.abc import Iterator
from math import comb


def cool_lex(n: int, k: int) -> Iterator[tuple[int, ...]]:
    """Yield the n-bit strings with k ones, b_1 ... b_n, in cool-lex order."""
    if k < 0 or k > n:
        return
    if k == 0:
        yield (0,) * n
        return
    b = [0] * (n + 1)  # b[0] is not used
    for i in range(1, k + 1):  # @line L1
        b[i] = 1
    x = k  # @line L2
    y = k
    yield tuple(b[1:])  # @line L3
    while x < n:  # @line L4
        b[x] = 0  # @line L5
        b[y] = 1
        x += 1
        y += 1
        if b[x] == 0:  # @line L6
            b[x] = 1  # @line L7
            b[1] = 0
            if y > 2:  # @line L8
                x = 2
            y = 1  # @line L9
        yield tuple(b[1:])  # @line L10


def cool_lex_sets(n: int, k: int) -> Iterator[tuple[int, ...]]:
    """Yield the k-subsets of {1, ..., n} as increasing tuples, in cool-lex order."""
    for b in cool_lex(n, k):
        yield tuple(i + 1 for i, v in enumerate(b) if v)


def rotate_successor(b: tuple[int, ...]) -> tuple[int, ...]:
    """The cool-lex successor by its definition: rotate the shortest prefix that ends
    in 010 or 011, or the whole string if there is none, one place to the right."""
    n = len(b)
    length = n
    for i in range(2, n):
        if b[i - 2] == 0 and b[i - 1] == 1:
            length = i + 1
            break
    if length == 0:
        return b
    return (b[length - 1],) + b[: length - 1] + b[length:]


def cool_lex_rank(c: tuple[int, ...]) -> int:
    """Rank of the k-subset c_1 < ... < c_k of {1, ..., n} in cool-lex order (Ruskey and Williams)."""
    k = len(c)
    r = next((i for i in range(1, k + 1) if c[i - 1] > i), None)
    if r is None:
        return 0
    return comb(c[r - 1], r) - 1 + sum(comb(c[j - 1] - 1, j) - 1 for j in range(r + 1, k + 1))
