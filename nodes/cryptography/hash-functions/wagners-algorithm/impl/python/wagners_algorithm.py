# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wagners-algorithm/. The authors are listed in prov/ZKP16F.jsonl.
"""Wagner's k-tree algorithm for the k-list XOR problem, k = 2^t.

For study only. The code is not constant time, and it is meant to run only on
toy instances, such as lists of SHA-256 values cut down to 24 to 36 bits.

Input: k lists of n-bit integers. Output: one index into each list such that
the k chosen values XOR to 0. With lists of about 2^(n/(t+1)) values, the
expected time and memory are O(k 2^(n/(t+1))) list operations.
"""

from typing import Iterable

Entry = tuple[int, tuple[int, ...]]  # (xor of the chosen values, the chosen indices)


def merge(a: list[Entry], b: list[Entry], mask: int) -> list[Entry]:
    """Join a and b on the bits in mask; return x XOR y with the indices joined."""
    by_low: dict[int, list[Entry]] = {}
    for x, ix in a:
        by_low.setdefault(x & mask, []).append((x, ix))
    out: list[Entry] = []
    for y, iy in b:
        for x, ix in by_low.get(y & mask, ()):
            out.append((x ^ y, ix + iy))
    return out


def wagner4(l1: list[int], l2: list[int], l3: list[int], l4: list[int], n: int) -> list[tuple[int, int, int, int]]:
    """All index tuples (i1, i2, i3, i4) found by the 4-list tree, with XOR 0 on n bits."""
    ell = -(-n // 3)  # @line L1
    low = (1 << ell) - 1  # @line L1
    full = (1 << n) - 1
    l12 = merge(_entries(l1), _entries(l2), low)  # @line L2
    l34 = merge(_entries(l3), _entries(l4), low)  # @line L3
    sols = []
    for v, ix in merge(l12, l34, full):  # @line L4
        if v == 0:  # @line L5
            sols.append((ix[0], ix[1], ix[2], ix[3]))  # @line L5
    return sols


def k_tree(lists: list[list[int]], n: int) -> list[tuple[int, ...]]:
    """Wagner's tree for k = 2^t lists: merge on n/(t+1) new bits at each of t-1 levels, then on all bits."""
    k = len(lists)
    t = k.bit_length() - 1
    if k < 2 or 1 << t != k:
        raise ValueError("the number of lists must be a power of two, at least 2")
    ell = -(-n // (t + 1))
    level = [_entries(lst) for lst in lists]
    for j in range(1, t):
        mask = (1 << min(n, j * ell)) - 1
        level = [merge(level[i], level[i + 1], mask) for i in range(0, len(level), 2)]
    full = (1 << n) - 1
    return [ix for v, ix in merge(level[0], level[1], full) if v & full == 0]


def _entries(values: Iterable[int]) -> list[Entry]:
    return [(v, (i,)) for i, v in enumerate(values)]
