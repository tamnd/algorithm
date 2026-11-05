# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merge-path/. The authors are listed in prov/8R73CV.jsonl.

"""Merge path: split a stable merge into p pieces of equal output length.

The p pieces are independent; the code merges them one after the other,
which gives the same output as merging them at the same time.
"""

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def co_rank(k: int, a: list[T], b: list[T]) -> tuple[int, int]:
    """Return (i, j) with i + j = k such that the first k items of the
    stable merge of a and b (a first on ties) are a[:i] and b[:j]."""
    m, n = len(a), len(b)
    lo, hi = max(0, k - n), min(k, m)  # @line L1
    while lo < hi:  # @line L2
        i = (lo + hi) // 2  # @line L3
        if b[k - i - 1] < a[i]:  # @line L4
            hi = i
        else:
            lo = i + 1
    return lo, k - lo  # @line L5


def sequential_merge(a: list[T], b: list[T]) -> list[T]:
    """The stable two-finger merge, a first on ties."""
    out: list[T] = []
    i = j = 0
    while i < len(a) and j < len(b):
        if b[j] < a[i]:
            out.append(b[j])
            j += 1
        else:
            out.append(a[i])
            i += 1
    return out + a[i:] + b[j:]


def merge_path(a: list[T], b: list[T], p: int) -> list[T]:
    """Merge sorted a and b stably with p independent pieces."""
    if p < 1:
        raise ValueError("need p >= 1")
    total = len(a) + len(b)
    out: list[T] = []
    for t in range(p):  # @line L6
        i0, j0 = co_rank(t * total // p, a, b)  # @line L7
        i1, j1 = co_rank((t + 1) * total // p, a, b)
        out.extend(sequential_merge(a[i0:i1], b[j0:j1]))  # @line L8
    return out
