# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/permutation-rank-unrank/. The authors are listed in prov/NW945N.jsonl.

from typing import Sequence


def _full_tree(n: int) -> list[int]:
    """Fenwick tree (1-based) in which every value 1..n is present once."""
    return [0] + [i & -i for i in range(1, n + 1)]


def _prefix(tree: list[int], i: int) -> int:
    """Number of present values among 1..i."""
    s = 0
    while i > 0:  # @line L16
        s += tree[i]
        i -= i & -i
    return s  # @line L17


def _add(tree: list[int], n: int, i: int, d: int) -> None:
    """Add d to the count of value i."""
    while i <= n:  # @line L18
        tree[i] += d
        i += i & -i


def _select(tree: list[int], n: int, k: int) -> int:
    """Return the k-th smallest present value, for 1 <= k <= number present."""
    pos = 0  # @line L13
    step = 1 << (n.bit_length() - 1) if n > 0 else 0
    while step > 0:  # @line L14
        if pos + step <= n and tree[pos + step] < k:
            pos += step
            k -= tree[pos]
        step >>= 1
    return pos + 1  # @line L15


def rank(a: Sequence[int]) -> int:
    """Return the lexicographic rank (from 0) of a permutation a of 1..n.

    Time O(n log n) arithmetic operations; the rank is an exact Python int.
    """
    n = len(a)
    if sorted(a) != list(range(1, n + 1)):
        raise ValueError("a must be a permutation of 1..n")
    tree = _full_tree(n)  # @line L1
    r = 0
    for i in range(1, n + 1):  # @line L2
        c = _prefix(tree, a[i - 1] - 1)  # @line L3
        _add(tree, n, a[i - 1], -1)  # @line L4
        r = r * (n - i + 1) + c  # @line L5
    return r  # @line L6


def unrank(r: int, n: int) -> list[int]:
    """Return the permutation of 1..n with lexicographic rank r, for 0 <= r < n!."""
    if n < 0 or r < 0:
        raise ValueError("need n >= 0 and r >= 0")
    d = [0] * (n + 1)
    for i in range(n, 0, -1):  # @line L7
        d[i] = r % (n - i + 1)
        r //= n - i + 1
    if r != 0:
        raise ValueError("r must be less than n!")
    tree = _full_tree(n)  # @line L8
    a = [0] * n
    for i in range(1, n + 1):  # @line L9
        a[i - 1] = _select(tree, n, d[i] + 1)  # @line L10
        _add(tree, n, a[i - 1], -1)  # @line L11
    return a  # @line L12


def lehmer_code(a: Sequence[int]) -> list[int]:
    """Return c with c[i] = number of j > i with a[j] < a[i], in O(n log n) time."""
    n = len(a)
    tree = _full_tree(n)
    out = []
    for x in a:
        out.append(_prefix(tree, x - 1))
        _add(tree, n, x, -1)
    return out
