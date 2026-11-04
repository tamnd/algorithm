# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timsort/. The authors are listed in prov/PM6BZ3.jsonl.

from typing import Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

MIN_MERGE = 64
MIN_GALLOP = 7


def min_run(n: int) -> int:
    """Return the least run length: n itself if n < 64, else a value in [32, 64]."""
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


def count_run(a: list[T], lo: int, hi: int) -> int:
    """Return the length of the run that starts at lo. A strictly decreasing run is reversed."""
    if lo + 1 == hi:
        return 1
    i = lo + 1
    if a[i] < a[lo]:
        while i + 1 < hi and a[i + 1] < a[i]:
            i += 1
        a[lo : i + 1] = a[lo : i + 1][::-1]
    else:
        while i + 1 < hi and not a[i + 1] < a[i]:
            i += 1
    return i + 1 - lo


def binary_insertion_sort(a: list[T], lo: int, hi: int, start: int) -> None:
    """Sort a[lo:hi], given that a[lo:start] is sorted. Each item goes after its equals."""
    for i in range(start, hi):
        pivot = a[i]
        left, right = lo, i
        while left < right:
            mid = (left + right) // 2
            if pivot < a[mid]:
                right = mid
            else:
                left = mid + 1
        a[left + 1 : i + 1] = a[left:i]
        a[left] = pivot


def gallop_left(key: T, a: list[T], lo: int, n: int, hint: int) -> int:
    """Return k in [0, n] with a[lo + k - 1] < key <= a[lo + k], searching from lo + hint."""
    last, ofs = 0, 1
    if a[lo + hint] < key:
        maxofs = n - hint
        while ofs < maxofs and a[lo + hint + ofs] < key:
            last, ofs = ofs, 2 * ofs + 1
        ofs = min(ofs, maxofs)
        last, ofs = last + hint, ofs + hint
    else:
        maxofs = hint + 1
        while ofs < maxofs and not a[lo + hint - ofs] < key:
            last, ofs = ofs, 2 * ofs + 1
        ofs = min(ofs, maxofs)
        last, ofs = hint - ofs, hint - last
    last += 1  # now a[lo + last - 1] < key <= a[lo + ofs]
    while last < ofs:
        m = last + (ofs - last) // 2
        if a[lo + m] < key:
            last = m + 1
        else:
            ofs = m
    return ofs


def gallop_right(key: T, a: list[T], lo: int, n: int, hint: int) -> int:
    """Return k in [0, n] with a[lo + k - 1] <= key < a[lo + k], searching from lo + hint."""
    last, ofs = 0, 1
    if key < a[lo + hint]:
        maxofs = hint + 1
        while ofs < maxofs and key < a[lo + hint - ofs]:
            last, ofs = ofs, 2 * ofs + 1
        ofs = min(ofs, maxofs)
        last, ofs = hint - ofs, hint - last
    else:
        maxofs = n - hint
        while ofs < maxofs and not key < a[lo + hint + ofs]:
            last, ofs = ofs, 2 * ofs + 1
        ofs = min(ofs, maxofs)
        last, ofs = last + hint, ofs + hint
    last += 1  # now a[lo + last - 1] <= key < a[lo + ofs]
    while last < ofs:
        m = last + (ofs - last) // 2
        if key < a[lo + m]:
            ofs = m
        else:
            last = m + 1
    return ofs


class TimSort(Generic[T]):
    def __init__(self, a: list[T]) -> None:
        self.a = a
        self.min_gallop = MIN_GALLOP
        self.runs: list[tuple[int, int]] = []  # (base, length), from the bottom of the stack
        self.merges: list[tuple[int, int]] = []  # the lengths of each merge, for tests

    def merge_at(self, i: int) -> None:
        """Merge the runs i and i + 1 of the stack."""
        a = self.a
        base_a, len_a = self.runs[i]
        base_b, len_b = self.runs[i + 1]
        self.merges.append((len_a, len_b))
        self.runs[i] = (base_a, len_a + len_b)
        del self.runs[i + 1]
        # Items of A that are at most B[0] are already in place.
        k = gallop_right(a[base_b], a, base_a, len_a, 0)
        base_a += k
        len_a -= k
        if len_a == 0:
            return
        # Items of B that are at least the last item of A are already in place.
        len_b = gallop_left(a[base_a + len_a - 1], a, base_b, len_b, len_b - 1)
        if len_b == 0:
            return
        if len_a <= len_b:
            self.merge_lo(base_a, len_a, base_b, len_b)
        else:
            self.merge_hi(base_a, len_a, base_b, len_b)

    def merge_lo(self, base_a: int, len_a: int, base_b: int, len_b: int) -> None:
        """Merge from the left, with A copied to a buffer. On a tie the item of A goes first."""
        a = self.a
        tmp = a[base_a : base_a + len_a]
        i, j, dest = 0, base_b, base_a
        end_b = base_b + len_b
        while i < len_a and j < end_b:
            count_a = count_b = 0
            while i < len_a and j < end_b:  # one item at a time
                if a[j] < tmp[i]:
                    a[dest] = a[j]
                    j += 1
                    count_b += 1
                    count_a = 0
                    if count_b >= self.min_gallop:
                        break
                else:
                    a[dest] = tmp[i]
                    i += 1
                    count_a += 1
                    count_b = 0
                    if count_a >= self.min_gallop:
                        break
                dest += 1
            else:
                break
            dest += 1
            self.min_gallop += 1
            while i < len_a and j < end_b:  # galloping mode
                self.min_gallop -= self.min_gallop > 1
                k = gallop_right(a[j], tmp, i, len_a - i, 0)
                a[dest : dest + k] = tmp[i : i + k]
                dest += k
                i += k
                if i == len_a:
                    break
                a[dest] = a[j]
                dest += 1
                j += 1
                if j == end_b:
                    break
                k2 = gallop_left(tmp[i], a, j, end_b - j, 0)
                a[dest : dest + k2] = a[j : j + k2]
                dest += k2
                j += k2
                if j == end_b:
                    break
                a[dest] = tmp[i]
                dest += 1
                i += 1
                if i == len_a:
                    break
                if k < MIN_GALLOP and k2 < MIN_GALLOP:
                    self.min_gallop += 1
                    break
        a[dest : dest + len_a - i] = tmp[i:]

    def merge_hi(self, base_a: int, len_a: int, base_b: int, len_b: int) -> None:
        """Merge from the right, with B copied to a buffer. On a tie the item of B goes last."""
        a = self.a
        tmp = a[base_b : base_b + len_b]
        i, j = base_a + len_a - 1, len_b - 1  # the last items of A and of the buffer
        dest = base_b + len_b - 1
        while i >= base_a and j >= 0:
            count_a = count_b = 0
            while i >= base_a and j >= 0:  # one item at a time
                if tmp[j] < a[i]:
                    a[dest] = a[i]
                    i -= 1
                    count_a += 1
                    count_b = 0
                    if count_a >= self.min_gallop:
                        break
                else:
                    a[dest] = tmp[j]
                    j -= 1
                    count_b += 1
                    count_a = 0
                    if count_b >= self.min_gallop:
                        break
                dest -= 1
            else:
                break
            dest -= 1
            self.min_gallop += 1
            while i >= base_a and j >= 0:  # galloping mode
                self.min_gallop -= self.min_gallop > 1
                rem_a = i - base_a + 1
                k = rem_a - gallop_right(tmp[j], a, base_a, rem_a, rem_a - 1)
                a[dest - k + 1 : dest + 1] = a[i - k + 1 : i + 1]
                dest -= k
                i -= k
                if i < base_a:
                    break
                a[dest] = tmp[j]
                dest -= 1
                j -= 1
                if j < 0:
                    break
                k2 = j + 1 - gallop_left(a[i], tmp, 0, j + 1, j)
                a[dest - k2 + 1 : dest + 1] = tmp[j - k2 + 1 : j + 1]
                dest -= k2
                j -= k2
                if j < 0:
                    break
                a[dest] = a[i]
                dest -= 1
                i -= 1
                if i < base_a:
                    break
                if k < MIN_GALLOP and k2 < MIN_GALLOP:
                    self.min_gallop += 1
                    break
        a[base_a : base_a + j + 1] = tmp[: j + 1]

    def merge_collapse(self) -> None:
        """Restore the invariants on the run lengths, with the check of de Gouw et al. (2015)."""
        r = self.runs
        while len(r) > 1:
            n = len(r) - 2
            if (n > 0 and r[n - 1][1] <= r[n][1] + r[n + 1][1]) or (
                n > 1 and r[n - 2][1] <= r[n - 1][1] + r[n][1]
            ):
                if r[n - 1][1] < r[n + 1][1]:
                    n -= 1
                self.merge_at(n)
            elif r[n][1] <= r[n + 1][1]:
                self.merge_at(n)
            else:
                break

    def merge_force_collapse(self) -> None:
        r = self.runs
        while len(r) > 1:
            n = len(r) - 2
            if n > 0 and r[n - 1][1] < r[n + 1][1]:
                n -= 1
            self.merge_at(n)


def timsort(a: list[T]) -> list[tuple[int, int]]:
    """Sort the list a in place, stably. Return the lengths of the runs that were merged, in order."""
    n = len(a)
    ts = TimSort(a)
    if n < 2:
        return ts.merges
    minrun = min_run(n)  # @line L1
    lo = 0  # @line L2
    while lo < n:  # @line L3
        run = count_run(a, lo, n)  # @line L4
        if run < minrun:  # @line L5
            force = min(minrun, n - lo)
            binary_insertion_sort(a, lo, lo + force, lo + run)
            run = force
        ts.runs.append((lo, run))  # @line L6
        lo += run
        ts.merge_collapse()  # @line L7
    ts.merge_force_collapse()  # @line L8
    return ts.merges
