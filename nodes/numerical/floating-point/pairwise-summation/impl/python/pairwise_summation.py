# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pairwise-summation/. The authors are listed in prov/QGCJX6.jsonl.

"""Pairwise (cascade) summation of binary64 floats.

The terms are split into two halves, each half is summed the same way, and
the two partial sums are added. Every term then passes through at most
ceil(log2 n) additions, so the error bound grows like log2 n instead of n.
"""

from collections.abc import Sequence


def recursive_sum(xs: Sequence[float]) -> float:
    """Plain left-to-right summation, one rounding per term. Cost: n - 1 additions.

    Python's built-in sum() uses compensated summation for floats since
    Python 3.12, so it is not used here as the naive reference.
    """
    s = 0.0
    for x in xs:
        s += x
    return s


def pairwise_sum(xs: Sequence[float], block: int = 1) -> float:
    """Pairwise sum of xs; slices of at most `block` terms are summed left to right.

    With block = 1 the tree is a full binary split down to single terms.
    The recursion depth is ceil(log2(n / block)) + 1, so no deep recursion
    occurs. Cost: n - 1 additions and O(log n) stack frames.
    """
    if block < 1:
        raise ValueError("block must be at least 1")
    n = len(xs)
    if n == 0:
        return 0.0
    return _sum(xs, 0, n, block)


def _sum(xs: Sequence[float], lo: int, hi: int, block: int) -> float:
    n = hi - lo  # @line L1
    if n <= block:  # @line L2
        s = xs[lo]  # @line L3
        for i in range(lo + 1, hi):  # @line L4
            s += xs[i]
        return s  # @line L5
    mid = lo + n // 2  # @line L6
    s1 = _sum(xs, lo, mid, block)  # @line L7
    s2 = _sum(xs, mid, hi, block)  # @line L8
    return s1 + s2  # @line L9


def pairwise_sum_iterative(xs: Sequence[float]) -> float:
    """Bottom-up pairwise sum: add neighbours level by level.

    Each level adds x[0]+x[1], x[2]+x[3], ...; an odd last term is carried
    up unchanged. The tree has depth ceil(log2 n), the same bound as the
    recursive split, though the tree shape can differ when n is not a power
    of two. Cost: n - 1 additions and n/2 extra floats.
    """
    level = list(xs)
    if not level:
        return 0.0
    while len(level) > 1:
        nxt = [level[i] + level[i + 1] for i in range(0, len(level) - 1, 2)]
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return level[0]


def depth(n: int, block: int = 1) -> int:
    """The largest number of additions any term goes through in pairwise_sum.

    It is the h in the error bound |error| <= gamma_h * sum |x_i|.
    """
    if n <= 1:
        return 0
    if n <= block:
        return n - 1
    return 1 + depth(n - n // 2, block)
