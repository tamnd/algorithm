# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flashsort/. The authors are listed in prov/GEP1AZ.jsonl.
from typing import Callable, Union

Key = Union[int, float, str]


def _common_prefix(s: str, t: str) -> int:
    p = 0
    while p < len(s) and p < len(t) and s[p] == t[p]:
        p += 1
    return p


def class_map(a: list[Key], lo: Key, hi: Key, m: int) -> Callable[[Key], int]:
    """Return a non-decreasing map K from the keys of a onto 0 .. m - 1, with K(lo) = 0 and K(hi) = m - 1.

    Integers use exact arithmetic, floats use (x - lo) / (hi - lo) with a
    clamp, and strings use a code of four characters after the common
    prefix of lo and hi. Precondition: lo < hi are the extremes of a.
    """
    if isinstance(lo, str):
        p = _common_prefix(lo, hi)  # type: ignore[arg-type]
        base = 2 + max(ord(c) for s in a for c in s[p:p + 4])  # type: ignore[union-attr]

        def code(s: str) -> int:
            v = 0
            for t in range(p, p + 4):
                v = v * base + (ord(s[t]) + 1 if t < len(s) else 0)
            return v

        clo, chi = code(lo), code(hi)  # type: ignore[arg-type]
        return lambda s: (m - 1) * (code(s) - clo) // (chi - clo)  # type: ignore[arg-type]
    if isinstance(lo, int) and isinstance(hi, int) and all(isinstance(x, int) for x in a):
        span = hi - lo
        return lambda x: (m - 1) * (x - lo) // span  # type: ignore[operator]
    flo, fhi = float(lo) / 2, float(hi) / 2  # halves avoid overflow of hi - lo
    fspan = fhi - flo
    return lambda x: min(m - 1, max(0, int((float(x) / 2 - flo) / fspan * (m - 1))))


def _insertion_sort(a: list[Key]) -> None:
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and x < a[j]:  # type: ignore[operator]
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


def flashsort(a: list[Key], m: int | None = None) -> None:
    """Sort the list a in place, in non-decreasing order. The sort is not stable.

    Precondition: the keys are all numbers or all strings; m >= 2 classes,
    by default max(2, ceil(n / 10)). The cost is Theta(n + m) expected time
    on keys uniform on their range, Theta(n^2) in the worst case, and
    Theta(m) extra space.
    """
    n = len(a)
    if n <= 1:  # @line L1
        return
    lo, hi = min(a), max(a)  # @line L2
    if not lo < hi:  # type: ignore[operator]
        return
    if m is None:
        m = max(2, -(-n // 10))
    if m < 2:
        raise ValueError("m must be at least 2")
    K = class_map(a, lo, hi, m)  # @line L3
    count = [0] * m  # @line L4
    for x in a:
        count[K(x)] += 1
    top = [0] * m  # @line L5
    s = 0
    for k in range(m):
        s += count[k]
        top[k] = s
    i = 0  # @line L6
    while i < n:  # @line L7
        if i >= top[K(a[i])]:  # @line L8
            i += 1
            continue
        x = a[i]  # @line L9
        while True:  # @line L10
            k = K(x)
            top[k] -= 1
            p = top[k]
            x, a[p] = a[p], x
            if p == i:
                break
    _insertion_sort(a)  # @line L11
    return  # @line L12
