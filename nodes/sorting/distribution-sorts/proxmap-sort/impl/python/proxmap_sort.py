# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proxmap-sort/. The authors are listed in prov/QTZM0Z.jsonl.
from typing import Callable, Union

Key = Union[int, float, str]


def _common_prefix(s: str, t: str) -> int:
    p = 0
    while p < len(s) and p < len(t) and s[p] == t[p]:
        p += 1
    return p


def map_key(a: list[Key], lo: Key, hi: Key, m: int) -> Callable[[Key], int]:
    """Return a non-decreasing map from the keys of a onto 0 .. m - 1, with K(lo) = 0 and K(hi) = m - 1.

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


def proxmap_sort(a: list[Key], m: int | None = None, key_map: Callable[[Key], int] | None = None) -> None:
    """Sort the list a in place, in non-decreasing order. The sort is stable.

    Precondition: the keys are all numbers or all strings; key_map, if given,
    is non-decreasing with values in 0 .. m - 1. By default m = n and the map
    is linear from the minimum to the maximum. The cost is Theta(n) expected
    time for keys spread evenly, Theta(n^2) in the worst case, and
    Theta(n + m) extra space.
    """
    n = len(a)
    if n <= 1:
        return
    if m is None:
        m = n
    if m < 1:
        raise ValueError("m must be at least 1")
    if key_map is None:
        lo, hi = min(a), max(a)
        if not lo < hi:  # type: ignore[operator]
            return
        key_map = map_key(a, lo, hi, m) if m >= 2 else (lambda x: 0)
    M = key_map
    h = [0] * m  # @line L1
    for x in a:
        h[M(x)] += 1
    p = [0] * m  # @line L2
    s = 0
    for k in range(m):
        p[k] = s
        s += h[k]
    f = [0] * m  # @line L3
    b: list[Key] = [None] * n  # type: ignore[list-item]
    for i in range(n):  # @line L4
        x = a[i]  # @line L5
        k = M(x)
        j = p[k] + f[k]
        f[k] += 1
        while j > p[k] and b[j - 1] > x:  # @line L6
            b[j] = b[j - 1]
            j -= 1
        b[j] = x  # @line L7
    a[:] = b  # @line L8
    return  # @line L9
