# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baeza-yates-intersection/. The authors are listed in prov/SRAJ81.jsonl.

from typing import Any, Sequence


def _lower_bound(b: Sequence[Any], x: Any, lo: int, hi: int) -> int:
    """Least p in [lo, hi] with p == hi or b[p] >= x, for sorted b. At most ceil(log2(hi - lo + 1)) tests."""
    while lo < hi:
        q = (lo + hi) // 2
        if b[q] < x:
            lo = q + 1
        else:
            hi = q
    return lo


def _by(a: Sequence[Any], alo: int, ahi: int, b: Sequence[Any], blo: int, bhi: int, out: list[Any]) -> None:
    if ahi - alo > bhi - blo:  # @line L1
        a, alo, ahi, b, blo, bhi = b, blo, bhi, a, alo, ahi
    if alo == ahi:  # @line L2
        return
    mid = alo + (ahi - alo) // 2  # @line L3
    x = a[mid]
    p = _lower_bound(b, x, blo, bhi)  # @line L4
    _by(a, alo, mid, b, blo, p, out)  # @line L5
    if p < bhi and b[p] == x:  # @line L6
        out.append(x)
        p += 1
    _by(a, mid + 1, ahi, b, p, bhi, out)  # @line L7


def baeza_yates(a: Sequence[Any], b: Sequence[Any]) -> list[Any]:
    """Return the ids in both a and b, in increasing order (Baeza-Yates double binary search).

    Precondition: a and b are strictly increasing. With m = min(len(a), len(b)) >= 1 and
    n = max(len(a), len(b)), it makes at most 2 m log2(2 + n/m) + 6 m tests (< and ==).
    Extra space O(log m) for the recursion, besides the output.
    """
    out: list[Any] = []
    _by(a, 0, len(a), b, 0, len(b), out)
    return out


def baeza_yates_all(lists: Sequence[Sequence[Any]]) -> list[Any]:
    """Intersect k >= 1 strictly increasing lists two at a time, shortest first."""
    order = sorted(lists, key=len)
    r = list(order[0])
    for t in range(1, len(order)):
        if not r:
            break
        r = baeza_yates(r, order[t])
    return r
