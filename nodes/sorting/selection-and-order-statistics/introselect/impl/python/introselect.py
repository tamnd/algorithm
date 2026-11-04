# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/introselect/. The authors are listed in prov/AQN873.jsonl.

from typing import Protocol, Sequence, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def median3(x: T, y: T, z: T) -> T:
    """Return the median of three items, with at most three comparisons."""
    if y < x:
        x, y = y, x
    if z < y:
        y = z
        if y < x:
            y = x
    return y


def partition3(b: list[T], lo: int, hi: int, x: T) -> tuple[int, int]:
    """Rearrange b[lo .. hi - 1] into items < x, items equal to x, items > x.

    Returns (p, q) with b[lo .. p - 1] < x, b[p .. q - 1] equal to x, and
    b[q .. hi - 1] > x. This is the Dutch national flag partition.
    """
    p, i, q = lo, lo, hi
    while i < q:
        if b[i] < x:
            b[p], b[i] = b[i], b[p]
            p += 1
            i += 1
        elif x < b[i]:
            q -= 1
            b[i], b[q] = b[q], b[i]
        else:
            i += 1
    return p, q


def mom_select(s: list[T], k: int) -> T:
    """Return the item of rank k (1-based) of s by median of medians, in O(n) time."""
    while True:
        n = len(s)
        if n <= 5:
            return sorted(s)[k - 1]
        medians = [sorted(s[i:i + 5])[(min(5, n - i) - 1) // 2] for i in range(0, n, 5)]
        x = mom_select(medians, (len(medians) + 1) // 2)
        less = [y for y in s if y < x]
        greater = [y for y in s if x < y]
        equal = n - len(less) - len(greater)
        if k <= len(less):
            s = less
        elif k <= len(less) + equal:
            return x
        else:
            s, k = greater, k - len(less) - equal


def introselect(a: Sequence[T], k: int, limit: int = 2) -> T:
    """Return the item of rank k (1-based) of a, in O(n) time in the worst case.

    Runs quickselect with a median-of-three pivot and three-way partition.
    After limit partitions in a row that keep more than 3/4 of the range, it finishes
    the current range with median of medians. The input is not changed.
    """
    n = len(a)
    if not 1 <= k <= n:
        raise ValueError("k must be between 1 and len(a)")
    b = list(a)
    lo, hi, t, bad = 0, n, k - 1, 0  # @line L1
    while hi - lo > 1:  # @line L2
        if bad >= limit:  # @line L3
            return mom_select(b[lo:hi], t - lo + 1)  # @line L3
        x = median3(b[lo], b[(lo + hi - 1) // 2], b[hi - 1])  # @line L4
        p, q = partition3(b, lo, hi, x)  # @line L5
        if p <= t < q:  # @line L6
            return x  # @line L6
        old = hi - lo  # @line L7
        if t < p:  # @line L8
            hi = p  # @line L8
        else:
            lo = q  # @line L8
        if 4 * (hi - lo) > 3 * old:  # @line L9
            bad += 1  # @line L9
        else:
            bad = 0  # @line L9
    return b[lo]  # @line L10
