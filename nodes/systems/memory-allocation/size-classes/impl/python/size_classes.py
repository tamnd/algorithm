# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/size-classes/. The authors are listed in prov/3FJ7YX.jsonl.

"""Size classes: a fixed list of block sizes to which requests are rounded up.

Two families are given. Power-of-two classes 1, 2, 4, 8, ... as in the binary
buddy system. Geometric classes with g classes per doubling (g a power of
two): every size 1 .. 2g, then from each power of two 2^e >= 2g, the sizes
2^e + j * 2^e / g for j = 1 .. g. Two consecutive geometric classes differ by
a factor of at most 1 + 1/g, so a request wastes less than 1/(g + 1) of its
block.
"""

from bisect import bisect_left


def pow2_classes(top: int) -> list[int]:
    """The powers of two up to the first one that is at least top."""
    out = [1]
    while out[-1] < top:
        out.append(out[-1] * 2)
    return out


def geometric_classes(g: int, top: int) -> list[int]:
    """Geometric classes with g classes per doubling, up to the first class >= top."""
    if g < 1 or g & (g - 1):
        raise ValueError("g must be a power of two")
    out = list(range(1, 2 * g + 1))
    base = 2 * g
    while out[-1] < top:
        step = base // g
        out.extend(base + j * step for j in range(1, g + 1))
        base *= 2
    return out


def round_up(classes: list[int], n: int) -> int:
    """The least class that is at least n (binary search)."""
    i = bisect_left(classes, n)
    if i == len(classes):
        raise ValueError("n is larger than the largest class")
    return classes[i]


def geometric_index(g: int, n: int) -> int:
    """Index of the class of n in geometric_classes(g, ...), in O(1) word operations."""
    if n <= 2 * g:
        return n - 1
    e = (n - 1).bit_length() - 1  # 2^e < n <= 2^(e+1)
    shift = e - (g.bit_length() - 1)  # the step is 2^shift = 2^e / g
    j = (n - (1 << e) + (1 << shift) - 1) >> shift  # ceil((n - 2^e) / step), 1 .. g
    lg2g = g.bit_length()  # lg(2g)
    return 2 * g - 1 + (e - lg2g) * g + j


def worst_waste(classes: list[int]) -> float:
    """The largest (class - n) / class over all n from 1 to the last class."""
    worst = 0.0
    prev = 0
    for c in classes:
        if c - prev > 1:
            worst = max(worst, (c - prev - 1) / c)  # the request n = prev + 1
        prev = c
    return worst
