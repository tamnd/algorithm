# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bucket-sort/. The authors are listed in prov/HHT9WC.jsonl.

import math
from typing import Callable, Sequence, Union

Key = Union[int, float, str]


def _prefix_code(s: str, width: int, base: int) -> int:
    """A non-decreasing integer code of the first width characters of s (0 marks the end)."""
    code = 0
    for i in range(width):
        code = code * base + (ord(s[i]) + 1 if i < len(s) else 0)
    return code


def bucket_index(a: Sequence[Key], m: int) -> Callable[[Key], int]:
    """Return a non-decreasing map from the keys of a to 0 .. m - 1.

    Floats in [0, 1) use floor(m * x), as on the page. Other numbers are
    mapped linearly from [min, max]. Strings use a code of their first
    four characters, which keeps the lexicographic order (not strictly).
    """
    if all(isinstance(x, float) and 0.0 <= x < 1.0 for x in a):
        return lambda x: min(math.floor(m * x), m - 1)  # type: ignore[operator]
    if all(isinstance(x, str) for x in a):
        base = 2 + max((ord(c) for s in a for c in s), default=0)  # type: ignore[union-attr]
        codes = [_prefix_code(s, 4, base) for s in a]  # type: ignore[arg-type]
        lo, hi = min(codes), max(codes)
        return lambda s: (_prefix_code(s, 4, base) - lo) * m // (hi - lo + 1)  # type: ignore[arg-type]
    if all(isinstance(x, int) for x in a):
        lo, hi = min(a), max(a)  # type: ignore[type-var]
        return lambda x: (x - lo) * m // (hi - lo + 1)  # type: ignore[operator]
    lo_f, hi_f = float(min(a)), float(max(a))  # type: ignore[type-var,arg-type]
    if hi_f == lo_f:
        return lambda x: 0
    return lambda x: min(math.floor((float(x) - lo_f) / (hi_f - lo_f) * m), m - 1)


def _insertion_sort(b: list[Key]) -> None:
    """Stable insertion sort of the list b, in place."""
    for i in range(1, len(b)):
        x = b[i]
        j = i - 1
        while j >= 0 and x < b[j]:  # type: ignore[operator]
            b[j + 1] = b[j]
            j -= 1
        b[j + 1] = x


def bucket_sort(a: list[Key]) -> None:
    """Sort the list a in place, in non-decreasing order. The sort is stable.

    The keys are numbers or strings. The bucket of x is beta(x), a
    non-decreasing map to 0 .. n - 1; for floats in [0, 1) it is
    floor(n * x). The cost is Theta(n) expected time on independent
    uniform keys, Theta(n^2) in the worst case, and Theta(n) extra space.
    """
    n = len(a)
    if n <= 1:
        return
    beta = bucket_index(a, n)
    buckets: list[list[Key]] = [[] for _ in range(n)]  # @line L1
    for i in range(n):  # @line L2
        buckets[beta(a[i])].append(a[i])  # @line L3
    for j in range(n):  # @line L4
        _insertion_sort(buckets[j])  # @line L5
    a[:] = [x for b in buckets for x in b]  # @line L6
