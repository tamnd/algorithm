# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spreadsort/. The authors are listed in prov/ER6NF4.jsonl.
import struct
from typing import Callable, Union

Key = Union[int, float, str]


def _float_bits(x: float) -> int:
    """An integer with the same order as the float x (IEEE 754 bit trick)."""
    u = struct.unpack(">Q", struct.pack(">d", x))[0]
    return u ^ 0xFFFFFFFFFFFFFFFF if u >> 63 else u | (1 << 63)


def integer_key(a: list[Key]) -> tuple[Callable[[Key], int], bool]:
    """Return an order-preserving map from the keys of a to non-negative integers.

    The second value says whether the map is one-to-one. Integers map to
    themselves, floats to their ordered bit patterns, and strings to the
    number with the digits ord(c) + 1, padded with 0 to the longest length.
    """
    if all(isinstance(x, int) for x in a):
        return (lambda x: x), True  # type: ignore[return-value]
    if all(isinstance(x, str) for x in a):
        width = max(len(s) for s in a)  # type: ignore[arg-type]
        base = 2 + max((ord(c) for s in a for c in s), default=0)  # type: ignore[union-attr]

        def code(s: str) -> int:
            v = 0
            for c in s:
                v = v * base + ord(c) + 1
            return v * base ** (width - len(s))

        return code, True  # type: ignore[return-value]
    exact = all(isinstance(x, float) for x in a)
    return (lambda x: _float_bits(float(x))), exact  # type: ignore[arg-type]


def _insertion_sort(p: list[tuple[int, Key]], lo: int, hi: int) -> None:
    """Stable insertion sort of p[lo:hi] by the original keys."""
    for i in range(lo + 1, hi):
        item = p[i]
        j = i - 1
        while j >= lo and item[1] < p[j][1]:  # type: ignore[operator]
            p[j + 1] = p[j]
            j -= 1
        p[j + 1] = item


def spreadsort(a: list[Key], max_splits: int = 11, small: int = 16, log_bin: int = 2) -> None:
    """Sort the list a in place, in non-decreasing order. The sort is not stable.

    Precondition: the keys are all numbers or all strings. Each step spreads
    a range of at least `small` keys into at most 2**max_splits bins by the top
    bits of (key - min); small ranges use insertion sort. The cost is O(n K / b)
    for K-bit keys and at least b >= 1 bits per step, and O(n) on random keys
    for a fixed key length; the extra space is O(2**max_splits) per open range.
    """
    if len(a) <= 1:
        return
    f, injective = integer_key(a)
    p = [(f(x), x) for x in a]
    stack = [(0, len(p))]  # @line L1
    while stack:  # @line L2
        lo, hi = stack.pop()  # @line L3
        if hi - lo < small:  # @line L4
            _insertion_sort(p, lo, hi)
            continue
        mn = min(p[i][0] for i in range(lo, hi))  # @line L5
        mx = max(p[i][0] for i in range(lo, hi))
        if mn == mx:  # @line L6
            if not injective:
                _insertion_sort(p, lo, hi)
            continue
        r = (mx - mn).bit_length()  # @line L7
        b = max(1, min(max_splits, (hi - lo).bit_length() - 1 - log_bin, r))  # @line L8
        shift = r - b  # @line L9
        nb = 1 << b
        count = [0] * nb  # @line L10
        for i in range(lo, hi):
            count[(p[i][0] - mn) >> shift] += 1
        start = [0] * (nb + 1)
        pos = lo
        for j in range(nb):
            start[j] = pos
            pos += count[j]
        start[nb] = hi
        nxt = start[:nb]
        for j in range(nb):  # @line L11
            end = start[j + 1]
            while nxt[j] < end:
                k = (p[nxt[j]][0] - mn) >> shift
                if k == j:
                    nxt[j] += 1
                else:
                    t = nxt[k]
                    p[nxt[j]], p[t] = p[t], p[nxt[j]]
                    nxt[k] = t + 1
        if shift == 0 and injective:  # @line L12
            continue
        for j in range(nb):  # @line L13
            if start[j + 1] - start[j] >= 2:
                stack.append((start[j], start[j + 1]))
    a[:] = [x for _, x in p]  # @line L14
