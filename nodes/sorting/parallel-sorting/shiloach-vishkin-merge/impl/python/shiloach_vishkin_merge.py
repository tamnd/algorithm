# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shiloach-vishkin-merge/. The authors are listed in prov/T0XRJS.jsonl.

"""Shiloach-Vishkin merging with p processors, simulated one processor at a time.

Both inputs are cut into blocks of ceil(m/p) and ceil(n/p) items. Each cut
is ranked in the other input by binary search. The cuts are put in output
order by arithmetic, and the pieces between them are merged one by one.
The merge is stable: on equal keys, items of A come first.
"""

import bisect
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def ceil_div(x: int, y: int) -> int:
    return -(-x // y)


def sv_splits(a: list[T], b: list[T], p: int) -> list[tuple[int, int]]:
    """Return the sorted splits (i, j): the first i + j output items are a[:i] and b[:j]."""
    m, n = len(a), len(b)
    sa, sb = max(1, ceil_div(m, p)), max(1, ceil_div(n, p))  # @line L1
    a_cuts = [(t * sa, bisect.bisect_left(b, a[t * sa])) for t in range(1, p) if t * sa < m]  # @line L2
    b_cuts = [(bisect.bisect_right(a, b[t * sb]), t * sb) for t in range(1, p) if t * sb < n]  # @line L3
    order: list[tuple[int, int] | None] = [None] * (len(a_cuts) + len(b_cuts))
    for idx, (i, j) in enumerate(a_cuts):
        order[idx + max(0, ceil_div(j, sb) - 1)] = (i, j)  # @line L4
    for idx, (i, j) in enumerate(b_cuts):
        order[idx + max(0, ceil_div(i, sa) - 1)] = (i, j)
    return [(0, 0)] + order + [(m, n)]  # type: ignore[operator]  # @line L5


def merge_piece(a: list[T], b: list[T], out: list, i: int, i2: int, j: int, j2: int) -> None:
    """Sequential stable merge of a[i:i2] and b[j:j2] into out[i + j : i2 + j2]."""
    k = i + j
    while i < i2 or j < j2:
        if j >= j2 or (i < i2 and not b[j] < a[i]):
            out[k] = a[i]
            i += 1
        else:
            out[k] = b[j]
            j += 1
        k += 1


def shiloach_vishkin_merge(a: list[T], b: list[T], p: int) -> tuple[list[T], list[tuple[int, int]]]:
    """Return the stable merge of the sorted lists a and b, and the splits used."""
    if p < 1:
        raise ValueError("need p >= 1")
    s = sv_splits(a, b, p)
    out: list = [None] * (len(a) + len(b))
    for (i, j), (i2, j2) in zip(s, s[1:]):  # @line L6
        merge_piece(a, b, out, i, i2, j, j2)  # @line L7
    return out, s
