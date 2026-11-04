# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-sort/. The authors are listed in prov/0XYD20.jsonl.

from math import isqrt
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

RUN = 16
SMALL_MERGE = 64


def _reverse(a: list[T], i: int, j: int) -> None:
    j -= 1
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1


def _rotate(a: list[T], i: int, m: int, j: int) -> None:
    """Turn a[i:m] + a[m:j] into a[m:j] + a[i:m]."""
    if i < m < j:
        _reverse(a, i, m)
        _reverse(a, m, j)
        _reverse(a, i, j)


def _swap_blocks(a: list[T], i: int, j: int, size: int) -> None:
    for d in range(size):
        a[i + d], a[j + d] = a[j + d], a[i + d]


def _insertion_sort(a: list[T], lo: int, hi: int) -> None:
    for i in range(lo + 1, hi):
        x = a[i]
        j = i
        while j > lo and x < a[j - 1]:
            a[j] = a[j - 1]
            j -= 1
        a[j] = x


def _lower_bound(a: list[T], lo: int, hi: int, x: T) -> int:
    while lo < hi:
        m = (lo + hi) // 2
        if a[m] < x:
            lo = m + 1
        else:
            hi = m
    return lo


def _upper_bound(a: list[T], lo: int, hi: int, x: T) -> int:
    while lo < hi:
        m = (lo + hi) // 2
        if x < a[m]:
            hi = m
        else:
            lo = m + 1
    return lo


def _rotation_merge(a: list[T], lo: int, mid: int, hi: int) -> None:
    """Stable merge of a[lo:mid] and a[mid:hi] by binary search and rotation."""
    if lo == mid or mid == hi:
        return
    if hi - lo == 2:
        if a[mid] < a[lo]:
            a[lo], a[mid] = a[mid], a[lo]
        return
    if mid - lo >= hi - mid:
        cut1 = lo + (mid - lo) // 2
        cut2 = _lower_bound(a, mid, hi, a[cut1])
    else:
        cut2 = mid + (hi - mid) // 2
        cut1 = _upper_bound(a, lo, mid, a[cut2])
    _rotate(a, cut1, mid, cut2)
    new_mid = cut1 + (cut2 - mid)
    _rotation_merge(a, lo, cut1, new_mid)
    _rotation_merge(a, new_mid, cut2, hi)


def _extract(a: list[T], lo: int, mid: int, k: int) -> int:
    """Move the first copies of the smallest distinct values of the sorted
    run a[lo:mid], up to k of them, to a[lo:lo+found]. Return found."""
    b0, found = lo, 1
    i = lo + 1
    while i < mid and found < k:
        if a[b0 + found - 1] < a[i]:
            _rotate(a, b0, b0 + found, i)
            b0 = i - found
            found += 1
        i += 1
    _rotate(a, lo, b0, b0 + found)
    return found


def _redistribute(a: list[T], lo: int, k: int, hi: int) -> None:
    """a[lo:lo+k] is a sorted set of distinct items and a[lo+k:hi] is sorted.
    Put each buffer item before the first item that is not smaller."""
    b0 = lo
    while k > 0:
        p = _lower_bound(a, b0 + k, hi, a[b0])
        _rotate(a, b0, b0 + k, p)
        b0 = p - k + 1
        k -= 1


def _buffered_merge(a: list[T], buf: int, f_end: int, g_end: int, s: int, f_is_a: bool) -> tuple[int, bool]:
    """Merge F = a[buf+s:f_end] with G = a[f_end:g_end], len(G) <= s, writing
    into a[buf:], with the buffer a[buf:buf+s] moving right. Return the start
    of the moved buffer; the rest of F or G follows it up to g_end. The flag
    tells whether the rest comes from the A run."""
    out, i, j = buf, buf + s, f_end
    while i < f_end and j < g_end:
        take_f = not a[j] < a[i] if f_is_a else a[i] < a[j]
        if take_f:
            a[out], a[i] = a[i], a[out]
            i += 1
        else:
            a[out], a[j] = a[j], a[out]
            j += 1
        out += 1
    if i == f_end:
        return out, not f_is_a
    rest = f_end - i
    for x in range(f_end - 1, i - 1, -1):
        a[x], a[x + (g_end - f_end)] = a[x + (g_end - f_end)], a[x]
    return g_end - rest - s, f_is_a


def _shift_past_buffer(a: list[T], buf: int, s: int, f_end: int) -> int:
    """[buffer][F] becomes [F][buffer]; return the new buffer start."""
    for x in range(buf + s, f_end):
        a[x - s], a[x] = a[x], a[x - s]
    return f_end - s


def _block_merge(a: list[T], lo: int, mid: int, hi: int) -> None:
    m = mid - lo
    if m < SMALL_MERGE:  # @line L5
        _rotation_merge(a, lo, mid, hi)
        return
    s = isqrt(m - 1) + 1  # @line L6
    k = 3 * s
    found = _extract(a, lo, mid, k)  # @line L7
    if found < k:  # @line L8
        _rotation_merge(a, lo + found, mid, hi)
        _redistribute(a, lo, found, hi)
        return
    tags, buf = lo, lo + 2 * s  # @line L9
    a_start = lo + k  # @line L10
    r = (mid - a_start) % s
    first = a_start + r
    p = (mid - first) // s
    q = (hi - mid) // s
    w_start = mid + q * s
    t = p + q
    mid_tag = a[tags + p] if q > 0 else None
    for x in range(t):  # @line L11
        best = x
        for y in range(x + 1, t):
            hy, hb = a[first + y * s], a[first + best * s]
            if hy < hb or (not hb < hy and a[tags + y] < a[tags + best]):
                best = y
        if best != x:
            _swap_blocks(a, first + x * s, first + best * s, s)
            a[tags + x], a[tags + best] = a[tags + best], a[tags + x]

    def is_a(x: int) -> bool:
        return mid_tag is None or a[tags + x] < mid_tag

    c = 0  # @line L12
    if w_start < hi:
        while c < t and is_a(t - 1 - c) and a[w_start] < a[first + (t - 1 - c) * s]:
            c += 1
        _rotate(a, first + (t - c) * s, w_start, hi)
    shift = hi - w_start
    count = t + (1 if shift > 0 else 0)
    f_end, f_is_a = first, True  # @line L13
    for x in range(count):
        if x < t - c:
            start, size, z_is_a = first + x * s, s, is_a(x)
        elif shift > 0 and x == t - c:
            start, size, z_is_a = first + x * s, shift, False
        else:
            y = x - (1 if shift > 0 else 0)
            start, size, z_is_a = first + y * s + shift, s, True
        if z_is_a == f_is_a:  # @line L14
            buf = _shift_past_buffer(a, buf, s, f_end)
            f_is_a = z_is_a
        else:  # @line L15
            buf, f_is_a = _buffered_merge(a, buf, f_end, start + size, s, f_is_a)
        f_end = start + size
    buf = _shift_past_buffer(a, buf, s, f_end)  # @line L16
    _rotate(a, lo + 2 * s, buf, hi)
    _insertion_sort(a, lo, lo + k)  # @line L17
    _redistribute(a, lo, k, hi)


def block_sort(a: list[T]) -> None:
    """Sort a in place, stably, in non-decreasing order, with O(1) extra words.

    Bottom-up merge sort. Each merge of two runs takes about 3√m distinct
    items of the left run as an internal buffer: one part tags the blocks of
    about √m items, the other is swap space for the local merges. The blocks
    are put in order of their first items, merged locally through the swap
    space, and the buffer is sorted and put back. If the left run has too few
    distinct values, the merge falls back to rotations.
    Cost: O(n log n) time when the buffers are found, O(n log² n) otherwise.
    """
    n = len(a)
    for lo in range(0, n, RUN):  # @line L1
        _insertion_sort(a, lo, min(lo + RUN, n))
    w = RUN
    while w < n:  # @line L2
        for lo in range(0, n - w, 2 * w):  # @line L3
            mid, hi = lo + w, min(lo + 2 * w, n)
            if a[mid] < a[mid - 1]:  # @line L4
                _block_merge(a, lo, mid, hi)
        w *= 2
