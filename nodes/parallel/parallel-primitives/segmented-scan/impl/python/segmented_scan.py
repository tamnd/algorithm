# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segmented-scan/. The authors are listed in prov/KQTVZW.jsonl.

"""Segmented scan as one unsegmented scan over (flag, value) pairs.

flags[i] is True when a segment starts at position i. Position 0 always
starts a segment. The unsegmented scan is a work-efficient tree scan
(up-sweep and down-sweep) that counts its combines and rounds.
"""

from typing import Callable, TypeVar

T = TypeVar("T")
Pair = tuple[bool, T]


def seg_op(op: Callable[[T, T], T]) -> Callable[[Pair, Pair], Pair]:
    """The segmented operator: (f, x) ⊕s (g, y) = (f or g, y if g else x ⊕ y)."""

    def combine(p: Pair, q: Pair) -> Pair:
        return (p[0] or q[0], q[1] if q[0] else op(p[1], q[1]))

    return combine


class Stats:
    def __init__(self) -> None:
        self.work = 0
        self.rounds = 0


def tree_scan(op: Callable[[T, T], T], e: T, a: list[T], st: Stats) -> list[T]:
    """Exclusive scan by up-sweep and down-sweep, padded to a power of two."""
    n = len(a)
    if n == 0:
        return []
    m = 1 << (n - 1).bit_length()
    x = list(a) + [e] * (m - n)
    h = 1
    while h < m:
        st.rounds += 1
        for i in range(0, m, 2 * h):
            x[i + 2 * h - 1] = op(x[i + h - 1], x[i + 2 * h - 1])
            st.work += 1
        h *= 2
    x[m - 1] = e
    h = m // 2
    while h >= 1:
        st.rounds += 1
        for i in range(0, m, 2 * h):
            left, right = i + h - 1, i + 2 * h - 1
            t = x[left]
            x[left] = x[right]
            x[right] = op(x[right], t)
            st.work += 1
        h //= 2
    return x[:n]


def segmented_scan(
    op: Callable[[T, T], T], e: T, flags: list[bool], a: list[T], st: Stats | None = None
) -> tuple[list[T], list[T]]:
    """Return (inclusive, exclusive) segmented scans of a."""
    st = st if st is not None else Stats()
    n = len(a)
    s = seg_op(op)
    p = [(flags[i] or i == 0, a[i]) for i in range(n)]  # @line L1
    q = tree_scan(s, (False, e), p, st)  # @line L2
    inclusive: list[T] = []
    exclusive: list[T] = []
    if n > 0:
        st.rounds += 1
    for i in range(n):  # @line L3
        inclusive.append(s(q[i], p[i])[1])  # @line L4
        st.work += 1
        exclusive.append(e if p[i][0] else q[i][1])  # @line L5
    return inclusive, exclusive  # @line L6


def exclusive_without_care(op: Callable[[T, T], T], e: T, flags: list[bool], a: list[T]) -> list[T]:
    """A wrong exclusive version that takes the value of the pair scan as is.

    At a segment start it returns the sum of the end of the previous
    segment instead of the identity.
    """
    s = seg_op(op)
    p = [(flags[i] or i == 0, a[i]) for i in range(len(a))]
    return [v for _, v in tree_scan(s, (False, e), p, Stats())]


def flags_from_lengths(lengths: list[int]) -> list[bool]:
    """Segment flags from segment lengths: a scatter of True to the starts."""
    n = sum(lengths)
    flags = [False] * n
    start = 0
    for length in lengths:  # the starts are an exclusive +-scan of the lengths
        if length > 0:
            flags[start] = True
        start += length
    return flags
