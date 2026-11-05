# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distinct-count-two-pointers/. The authors are listed in prov/9MW95T.jsonl.

from collections.abc import Hashable, Sequence


def longest_at_most_k_distinct(a: Sequence[Hashable], k: int) -> tuple[int, int]:
    """Return (length, start) of a longest subarray a[start:start+length] with at most k distinct values.

    Precondition: the items are hashable and k >= 0 (raises ValueError if k < 0).
    For the empty answer the start is 0.
    Cost: O(n) expected time over the hash table, O(min(n, k)) extra space.
    """
    if k < 0:
        raise ValueError("k must be non-negative")
    cnt: dict[Hashable, int] = {}  # @line L1
    d = 0
    i = 0
    best = 0
    start = 0
    for j in range(len(a)):  # @line L2
        x = a[j]
        if x not in cnt:  # @line L3
            cnt[x] = 0
            d += 1
        cnt[x] += 1  # @line L4
        while d > k:  # @line L5
            y = a[i]  # @line L6
            cnt[y] -= 1
            if cnt[y] == 0:
                del cnt[y]
                d -= 1
            i += 1  # @line L7
        if j + 1 - i > best:  # @line L8
            best = j + 1 - i
            start = i
    return best, start  # @line L9


def count_at_most_k_distinct(a: Sequence[Hashable], k: int) -> int:
    """Return the number of non-empty subarrays with at most k distinct values.

    Precondition: hashable items. Returns 0 for k <= 0.
    Cost: O(n) expected time, O(min(n, k)) extra space.
    """
    if k <= 0:
        return 0
    cnt: dict[Hashable, int] = {}
    i = 0
    total = 0
    for j, x in enumerate(a):
        cnt[x] = cnt.get(x, 0) + 1
        while len(cnt) > k:
            y = a[i]
            cnt[y] -= 1
            if cnt[y] == 0:
                del cnt[y]
            i += 1
        total += j + 1 - i
    return total


def count_exactly_k_distinct(a: Sequence[Hashable], k: int) -> int:
    """Return the number of non-empty subarrays with exactly k distinct values.

    Precondition: hashable items. Returns 0 for k <= 0.
    Cost: two passes, O(n) expected time.
    """
    if k <= 0:
        return 0
    return count_at_most_k_distinct(a, k) - count_at_most_k_distinct(a, k - 1)
