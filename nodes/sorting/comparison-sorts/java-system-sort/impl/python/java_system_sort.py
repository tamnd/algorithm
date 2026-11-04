# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/java-system-sort/. The authors are listed in prov/YQKT8T.jsonl.

"""A model of the two sorts of the Java standard library.

Arrays of primitive values (here: int and float) go to a dual-pivot
quicksort with an insertion sort for short ranges and a heapsort when the
recursion is too deep. Other arrays go to a stable merge of natural runs in
the style of Timsort. The constants are those of the JDK 7 and 8 sources
where the model has the same step.
"""

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

INSERTION_SORT_THRESHOLD = 47
MIN_MERGE = 32


def java_system_sort(a: list[T]) -> None:
    """Sort a in place, in non-decreasing order.

    Primitive values use the unstable dual-pivot quicksort, other items use
    the stable run-merging sort. Cost: O(n log n) comparisons in the worst
    case on both paths, and O(n) on a sorted array of objects.
    """
    n = len(a)
    if all(type(x) in (int, float) for x in a):  # @line L1
        _sort_primitive(a, 0, n - 1, 2 * n.bit_length() + 2)
    else:
        _sort_objects(a)  # @line L2


# The path for primitive values.


def _sort_primitive(a: list[T], lo: int, hi: int, depth: int) -> None:
    if hi - lo < INSERTION_SORT_THRESHOLD:  # @line L3
        _insertion_sort(a, lo, hi)
        return
    if depth == 0:  # @line L4
        _heapsort(a, lo, hi)
        return
    p, q = _choose_pivots(a, lo, hi)  # @line L5
    lt, gt = lo + 1, hi - 1  # @line L6: three-way partition around p <= q
    k = lt
    while k <= gt:
        if a[k] < p:
            a[k], a[lt] = a[lt], a[k]
            lt += 1
        elif q < a[k]:
            while q < a[gt] and k < gt:
                gt -= 1
            a[k], a[gt] = a[gt], a[k]
            gt -= 1
            if a[k] < p:
                a[k], a[lt] = a[lt], a[k]
                lt += 1
        k += 1
    lt -= 1  # @line L7: the pivots go to their places
    gt += 1
    a[lo], a[lt] = a[lt], a[lo]
    a[hi], a[gt] = a[gt], a[hi]
    _sort_primitive(a, lo, lt - 1, depth - 1)  # @line L8
    _sort_primitive(a, gt + 1, hi, depth - 1)
    if p < q:  # @line L9
        _sort_primitive(a, lt + 1, gt - 1, depth - 1)


def _choose_pivots(a: list[T], lo: int, hi: int) -> tuple[T, T]:
    """Sort five sample items, and move the second and fourth to a[lo] and a[hi]."""
    seventh = (hi - lo + 1) // 7
    e3 = (lo + hi) // 2
    idx = [e3 - 2 * seventh, e3 - seventh, e3, e3 + seventh, e3 + 2 * seventh]
    for s in range(1, 5):
        x, t = a[idx[s]], s
        while t > 0 and x < a[idx[t - 1]]:
            a[idx[t]] = a[idx[t - 1]]
            t -= 1
        a[idx[t]] = x
    a[lo], a[idx[1]] = a[idx[1]], a[lo]
    a[hi], a[idx[3]] = a[idx[3]], a[hi]
    return a[lo], a[hi]


def _insertion_sort(a: list[T], lo: int, hi: int) -> None:
    for i in range(lo + 1, hi + 1):
        x, j = a[i], i
        while j > lo and x < a[j - 1]:
            a[j] = a[j - 1]
            j -= 1
        a[j] = x


def _heapsort(a: list[T], lo: int, hi: int) -> None:
    m = hi - lo + 1
    for s in range(m // 2 - 1, -1, -1):
        _sift_down(a, lo, s, m)
    for end in range(m - 1, 0, -1):
        a[lo], a[lo + end] = a[lo + end], a[lo]
        _sift_down(a, lo, 0, end)


def _sift_down(a: list[T], lo: int, s: int, m: int) -> None:
    while 2 * s + 1 < m:
        c = 2 * s + 1
        if c + 1 < m and a[lo + c] < a[lo + c + 1]:
            c += 1
        if not a[lo + s] < a[lo + c]:
            return
        a[lo + s], a[lo + c] = a[lo + c], a[lo + s]
        s = c


# The path for objects: a stable merge of natural runs.


def _sort_objects(a: list[T]) -> None:
    n = len(a)
    min_run = _min_run_length(n)
    runs: list[list[int]] = []  # [start, length], from left to right
    i = 0
    while i < n:
        run = _count_run_and_make_ascending(a, i, n)  # @line L10
        if run < min_run:
            end = min(i + min_run, n)
            _binary_insertion_sort(a, i, end, i + run)
            run = end - i
        runs.append([i, run])  # @line L11
        _merge_collapse(a, runs)
        i += run
    while len(runs) > 1:  # @line L12
        k = len(runs) - 2
        if k > 0 and runs[k - 1][1] < runs[k + 1][1]:
            k -= 1
        _merge_at(a, runs, k)


def _min_run_length(n: int) -> int:
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


def _count_run_and_make_ascending(a: list[T], lo: int, n: int) -> int:
    """Return the length of the run at lo; reverse it first if it strictly descends."""
    hi = lo + 1
    if hi == n:
        return 1
    if a[hi] < a[lo]:
        while hi < n and a[hi] < a[hi - 1]:
            hi += 1
        a[lo:hi] = a[lo:hi][::-1]
    else:
        while hi < n and not a[hi] < a[hi - 1]:
            hi += 1
    return hi - lo


def _binary_insertion_sort(a: list[T], lo: int, hi: int, start: int) -> None:
    """Sort a[lo:hi], of which a[lo:start] is already sorted; equal items keep their order."""
    for i in range(start, hi):
        x = a[i]
        left, right = lo, i
        while left < right:
            mid = (left + right) // 2
            if x < a[mid]:
                right = mid
            else:
                left = mid + 1
        a[left + 1 : i + 1] = a[left:i]
        a[left] = x


def _merge_collapse(a: list[T], runs: list[list[int]]) -> None:
    """Merge runs on the top of the stack until the run lengths satisfy the invariants."""
    while len(runs) > 1:
        k = len(runs) - 2
        length = [r[1] for r in runs]
        if (k > 0 and length[k - 1] <= length[k] + length[k + 1]) or (
            k > 1 and length[k - 2] <= length[k - 1] + length[k]
        ):
            if length[k - 1] < length[k + 1]:
                k -= 1
        elif length[k] > length[k + 1]:
            break
        _merge_at(a, runs, k)


def _merge_at(a: list[T], runs: list[list[int]], k: int) -> None:
    """Merge the adjacent runs k and k + 1, stably, with a copy of the left run."""
    lo, n1 = runs[k]
    mid, n2 = runs[k + 1]
    left = a[lo:mid]
    i, j, out = 0, mid, lo
    while i < n1 and j < mid + n2:
        if a[j] < left[i]:
            a[out] = a[j]
            j += 1
        else:
            a[out] = left[i]
            i += 1
        out += 1
    a[out : out + n1 - i] = left[i:]
    runs[k] = [lo, n1 + n2]
    del runs[k + 1]
