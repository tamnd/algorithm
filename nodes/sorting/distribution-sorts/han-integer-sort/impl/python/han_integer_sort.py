# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/han-integer-sort/. The authors are listed in prov/0V80XQ.jsonl.
from bisect import bisect_left
from math import isqrt


def _insertion_sort(a: list[int]) -> list[int]:
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return a


def han_integer_sort(a: list[int], base: int = 8) -> list[int]:
    """Return the integers of a in non-decreasing order.

    Precondition: a holds integers (any sign) and base >= 2. This is a model of
    the structure of Han's algorithm: a recursion on about sqrt(n) splitters,
    as in an exponential search tree, with a deterministic sample. Han passes
    the keys down each level in O(1) amortized time per key with packed words,
    which gives O(n log log n) time in total. Here each key is placed by binary
    search, so one level costs O(n log n), and the sample is not balanced on
    every input. The extra space is O(n).
    """
    if base < 2:
        raise ValueError("base must be at least 2")
    return _sort(list(a), base)


def _sort(a: list[int], base: int) -> list[int]:
    n = len(a)
    if n <= base:  # @line L1
        return _insertion_sort(a)
    k = isqrt(n - 1) + 1  # @line L2
    sample = a[::k]  # @line L3
    p = _sort(sample, base)  # @line L4
    splitters = [x for i, x in enumerate(p) if i == 0 or x != p[i - 1]]
    s = len(splitters)
    parts: list[list[int]] = [[] for _ in range(s + 1)]
    equal = [0] * s
    for x in a:  # @line L5
        j = bisect_left(splitters, x)
        if j < s and splitters[j] == x:  # @line L6
            equal[j] += 1
        else:
            parts[j].append(x)
    out: list[int] = []
    for j in range(s + 1):  # @line L7
        out.extend(_sort(parts[j], base))
        if j < s:
            out.extend([splitters[j]] * equal[j])
    return out  # @line L8
