# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bin-packing-inapproximability/. The authors are listed in prov/9SGJ55.jsonl.
"""The gap reduction from partition to bin packing, and its padded form.

For small instances only: the exact solver searches all packings.
"""

from itertools import combinations


def has_partition(a: list[int]) -> bool:
    """Decide partition by trying every subset."""
    total = sum(a)
    if total % 2:
        return False
    return any(sum(s) == total // 2 for r in range(len(a) + 1) for s in combinations(a, r))


def partition_to_bin_packing(a: list[int], k: int = 2) -> tuple[int, list[int]]:
    """Map a partition instance to (capacity, sizes).

    The answer is yes exactly when OPT <= k. For k > 2 the list gets k - 2 items that fill a bin each.
    An instance that is clearly a no-instance (odd total or an item above half) maps to a fixed list with OPT = k + 1.
    """
    total = sum(a)
    if total % 2 or 2 * max(a) > total:
        return 1, [1] * (k + 1)
    b = total // 2
    return b, list(a) + [b] * (k - 2)


def opt_bins(capacity: int, sizes: list[int]) -> int:
    """The least number of bins, by depth-first search over packings with the items in decreasing order."""
    items = sorted(sizes, reverse=True)
    best = len(items)
    loads: list[int] = []

    def place(i: int) -> None:
        nonlocal best
        if len(loads) >= best:
            return
        if i == len(items):
            best = len(loads)
            return
        seen = set()
        for j in range(len(loads)):
            if loads[j] + items[i] <= capacity and loads[j] not in seen:
                seen.add(loads[j])
                loads[j] += items[i]
                place(i + 1)
                loads[j] -= items[i]
        loads.append(items[i])
        place(i + 1)
        loads.pop()

    place(0)
    return best


def first_fit_decreasing(capacity: int, sizes: list[int]) -> int:
    """The number of bins that first fit decreasing uses."""
    loads: list[int] = []
    for s in sorted(sizes, reverse=True):
        for j, load in enumerate(loads):
            if load + s <= capacity:
                loads[j] += s
                break
        else:
            loads.append(s)
    return len(loads)
