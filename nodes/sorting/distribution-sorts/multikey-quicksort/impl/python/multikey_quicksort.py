# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multikey-quicksort/. The authors are listed in prov/36KMJW.jsonl.
import random


def _c(s: str, d: int) -> int:
    """The character code of s at index d, or -1 when s has ended."""
    return ord(s[d]) if d < len(s) else -1


def multikey_quicksort(a: list[str], seed: int | None = None) -> list[str]:
    """Sort the list a of strings in lexicographic order, in place, and return it.

    Precondition: the items are str. The sort is not stable.
    The expected cost is O(n log n + D) character reads, where D is the total
    length of the distinguishing prefixes; the extra space is the task stack.
    """
    rng = random.Random(seed)
    stack = [(0, len(a), 0)]  # @line L1
    while stack:  # @line L2
        lo, hi, d = stack.pop()  # @line L3
        if hi - lo <= 1:  # @line L4
            continue
        v = _c(a[rng.randrange(lo, hi)], d)  # @line L5
        lt, i, gt = lo, lo, hi - 1  # @line L6
        while i <= gt:
            x = _c(a[i], d)
            if x < v:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif x > v:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        gt += 1
        stack.append((gt, hi, d))  # @line L7
        if v != -1:  # @line L8
            stack.append((lt, gt, d + 1))
        stack.append((lo, lt, d))  # @line L9
    return a  # @line L10
