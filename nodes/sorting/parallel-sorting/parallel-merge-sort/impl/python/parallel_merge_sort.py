# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-merge-sort/. The authors are listed in prov/J1JZCG.jsonl.

"""Parallel merge sort in the work-span model.

The code runs the spawned calls one after the other, which is a legal
schedule of the parallel program. Each function also returns the work
and the span of the computation in a unit-cost model: one unit for each
call, each probe of a binary search and each copied item.
"""

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def lower_bound(y: list[T], lo: int, hi: int, key: T) -> tuple[int, int]:
    """First index r in [lo, hi] with not y[r] < key, and the number of probes."""
    probes = 0
    while lo < hi:
        probes += 1
        mid = (lo + hi) // 2
        if y[mid] < key:
            lo = mid + 1
        else:
            hi = mid
    return lo, probes


def upper_bound(x: list[T], lo: int, hi: int, key: T) -> tuple[int, int]:
    """First index r in [lo, hi] with key < x[r], and the number of probes."""
    probes = 0
    while lo < hi:
        probes += 1
        mid = (lo + hi) // 2
        if key < x[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo, probes


def p_merge(x: list[T], a1: int, a2: int, y: list[T], b1: int, b2: int, z: list[T], c: int) -> tuple[int, int]:
    """Merge sorted x[a1:a2] and y[b1:b2] into z[c:], stably (x first on ties).

    Return (work, span)."""
    na, nb = a2 - a1, b2 - b1  # @line L8
    if na + nb == 0:  # @line L9
        return 1, 1
    if na >= nb:  # @line L10
        q = a1 + na // 2  # @line L11
        r, probes = lower_bound(y, b1, b2, x[q])  # @line L12
        t = c + (q - a1) + (r - b1)  # @line L13
        z[t] = x[q]  # @line L14
        w1, s1 = p_merge(x, a1, q, y, b1, r, z, c)  # @line L15
        w2, s2 = p_merge(x, q + 1, a2, y, r, b2, z, t + 1)  # @line L16
        # sync: the two calls above are done here  # @line L17
    else:  # @line L18
        q = b1 + nb // 2  # @line L19
        r, probes = upper_bound(x, a1, a2, y[q])  # @line L20
        t = c + (r - a1) + (q - b1)  # @line L21
        z[t] = y[q]  # @line L22
        w1, s1 = p_merge(x, a1, r, y, b1, q, z, c)  # @line L23
        w2, s2 = p_merge(x, r, a2, y, q + 1, b2, z, t + 1)  # @line L24
        # sync: the two calls above are done here  # @line L25
    return 1 + probes + w1 + w2, 1 + probes + max(s1, s2)


def p_merge_sort(a: list[T], lo: int = 0, hi: int | None = None, buf: list[T] | None = None) -> tuple[int, int]:
    """Sort a[lo:hi] in place, stably. Return (work, span)."""
    if hi is None:
        hi = len(a)
    if buf is None:
        buf = list(a)
    if hi - lo <= 1:  # @line L1
        return 1, 1
    mid = lo + (hi - lo) // 2  # @line L2
    w1, s1 = p_merge_sort(a, lo, mid, buf)  # @line L3
    w2, s2 = p_merge_sort(a, mid, hi, buf)  # @line L4
    # sync: both halves are sorted here  # @line L5
    buf[lo:hi] = a[lo:hi]  # @line L6: a parallel loop, span about lg(hi - lo)
    copy_span = (hi - lo).bit_length()
    w3, s3 = p_merge(buf, lo, mid, buf, mid, hi, a, lo)  # @line L7
    return 1 + w1 + w2 + (hi - lo) + w3, 1 + max(s1, s2) + copy_span + s3
