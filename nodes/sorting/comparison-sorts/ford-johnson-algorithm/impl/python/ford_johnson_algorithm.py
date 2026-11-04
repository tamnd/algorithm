# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ford-johnson-algorithm/. The authors are listed in prov/311MZG.jsonl.

from typing import Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class _Pair(Generic[T]):
    """A winner a with the loser b of its first comparison; ordered by a."""

    __slots__ = ("a", "b")

    def __init__(self, a: T, b: T) -> None:
        self.a, self.b = a, b

    def __lt__(self, other: "_Pair[T]") -> bool:
        return self.a < other.a


def _group_ends(m: int) -> list[int]:
    """t_1 = 1, t_2 = 3, t_3 = 5, t_4 = 11, ...: t_k = (2^(k+1) + (-1)^k) / 3, up to m."""
    ends = [1]
    k = 2
    while ends[-1] < m:
        ends.append(min(m, (2 ** (k + 1) + (-1) ** k) // 3))
        k += 1
    return ends


def _merge_insertion(x: list[T]) -> list[T]:
    n = len(x)
    if n <= 1:  # @line L1
        return list(x)
    pairs: list[_Pair[T]] = []
    for i in range(1, n, 2):  # @line L2
        if x[i] < x[i - 1]:  # @line L3
            pairs.append(_Pair(x[i - 1], x[i]))
        else:
            pairs.append(_Pair(x[i], x[i - 1]))
    extra = x[-1] if n % 2 == 1 else None  # @line L4: the item with no partner
    pairs = _merge_insertion(pairs)  # @line L5
    m = len(pairs)
    a = [p.a for p in pairs]
    b = [p.b for p in pairs] + ([extra] if extra is not None else [])
    s: list[T] = [b[0]] + a  # @line L6
    ends = _group_ends(len(b))
    for k in range(1, len(ends)):  # @line L7
        for j in range(ends[k], ends[k - 1], -1):  # @line L8: b_j for j = t_k down to t_(k-1) + 1
            item = b[j - 1]
            if j <= m:  # @line L9
                partner = a[j - 1]
                u = next(i for i, v in enumerate(s) if v is partner)
            else:
                u = len(s)
            lo, hi = 0, u  # @line L10: binary search in s[0 .. u - 1]
            while lo < hi:
                mid = (lo + hi) // 2
                if item < s[mid]:
                    hi = mid
                else:
                    lo = mid + 1
            s.insert(lo, item)
    return s  # @line L11


def ford_johnson_algorithm(a: list[T]) -> None:
    """Sort a in place, in non-decreasing order, by merge insertion.

    Pair the items, sort the winners recursively, then insert the losers into
    the chain of winners by binary search, in the order b3 b2, b5 b4, b11 ... b6,
    b21 ... b12, ..., so that each binary search is over at most 2^k - 1 items.
    Worst case: F(n) = sum_{k=1..n} ceil(lg(3k/4)) comparisons, which equals
    ceil(lg n!) for n <= 11. Not stable.
    """
    a[:] = _merge_insertion(a)
