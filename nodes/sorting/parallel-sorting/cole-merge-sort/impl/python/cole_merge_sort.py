# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cole-merge-sort/. The authors are listed in prov/342B4P.jsonl.

"""Cole's pipelined merge sort, simulated one stage at a time.

The tree has n = 2^k leaves, padded with items larger than all keys.
Node u is stored at index u of a heap layout, with children 2u and 2u + 1.
Every stage first forms SUP(v) for all live nodes from UP(v), and then
forms NEWUP(u) as the merge of SUP(2u) and SUP(2u + 1). Each item of
SUP(x) finds its rank in SUP(y) with at most three comparisons, by the
3-cover property. The ranks that Cole keeps up to date in O(1) time per
stage (line L9) are computed here by a sequential merge.
"""

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class Item:
    """A key with its input index. Padding items are larger than all keys."""

    __slots__ = ("pad", "key", "index")

    def __init__(self, pad: bool, key: object, index: int) -> None:
        self.pad, self.key, self.index = pad, key, index

    def __lt__(self, other: "Item") -> bool:
        if self.pad != other.pad:
            return other.pad
        if not self.pad:
            if self.key < other.key:  # type: ignore[operator]
                return True
            if other.key < self.key:  # type: ignore[operator]
                return False
        return self.index < other.index


def rank_in(src: list[Item], dst: list[Item]) -> list[int]:
    """For each item of the sorted list src, the number of items of dst less than it."""
    out, j = [], 0
    for e in src:
        while j < len(dst) and dst[j] < e:
            j += 1
        out.append(j)
    return out


def cover_rank(e: Item, r: int, up: list[Item], up_in_y: list[int], sup_y: list[Item], stats: dict) -> int:
    """Rank of e in sup_y, from the rank r of e in up and the ranks of up in sup_y."""
    lo = up_in_y[r - 1] if r > 0 else 0  # @line L6
    hi = up_in_y[r] if r < len(up) else len(sup_y)
    stats["max_candidates"] = max(stats["max_candidates"], hi - lo)
    j = lo
    while j < hi and sup_y[j] < e:  # @line L7
        j += 1
    return j


def cole_merge_sort(a: list[T], stats: dict | None = None) -> list[T]:
    """Return a stably sorted copy of a."""
    if stats is None:
        stats = {}
    stats.update(max_candidates=0, stages=0, max_live=0)
    n = len(a)
    if n <= 1:
        return list(a)
    k = (n - 1).bit_length()
    size = 1 << k
    up: dict[int, list[Item]] = {}
    full_at: dict[int, int] = {}
    for i in range(size):  # @line L1
        up[size + i] = [Item(i >= n, a[i] if i < n else None, i)]
        full_at[size + i] = 0
    for t in range(1, 3 * k + 1):  # @line L2
        stats["stages"] = t
        sup: dict[int, list[Item]] = {}
        for v, items in up.items():  # @line L3
            if v not in full_at:
                step = 4  # @line L4
            else:
                age = t - full_at[v]
                if age > 3:
                    continue
                step = {1: 4, 2: 2, 3: 1}[age]  # @line L5
            sup[v] = items[step - 1 :: step]
        live = sum(len(s) for s in sup.values())
        new_up: dict[int, list[Item]] = {}
        for u in range(1, size):
            x, y = 2 * u, 2 * u + 1
            sx, sy = sup.get(x, []), sup.get(y, [])
            if u in full_at or not (sx or sy):
                continue
            cur = up.get(u, [])
            # Ranks that Cole maintains in O(1) time per stage.  # @line L9
            x_in_up, y_in_up = rank_in(sx, cur), rank_in(sy, cur)
            up_in_x, up_in_y = rank_in(cur, sx), rank_in(cur, sy)
            merged: list[Item | None] = [None] * (len(sx) + len(sy))
            for i, e in enumerate(sx):
                merged[i + cover_rank(e, x_in_up[i], cur, up_in_y, sy, stats)] = e  # @line L8
            for j, e in enumerate(sy):
                merged[j + cover_rank(e, y_in_up[j], cur, up_in_x, sx, stats)] = e
            new_up[u] = merged  # type: ignore[assignment]
        for u, items in new_up.items():  # @line L10
            up[u] = items
            live += len(items)
            height = k - (u.bit_length() - 1)
            if len(items) == 1 << height:
                full_at[u] = t
        stats["max_live"] = max(stats["max_live"], live)
    return [it.key for it in up[1] if not it.pad]  # @line L11
