# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prefix-sum-hash-counting/. The authors are listed in prov/ASHEE3.jsonl.

def count_subarrays_with_sum(a: list[int], k: int) -> int:
    """Return the number of non-empty subarrays of a whose sum is exactly k.

    Items may be negative. Precondition: integer items, so that sums compare exactly.
    Cost: O(n) expected time with Python's dict, O(n) extra space.
    """
    counts: dict[int, int] = {0: 1}  # @line L1
    p = 0
    count = 0
    for x in a:  # @line L2
        p += x  # @line L3
        count += counts.get(p - k, 0)  # @line L4
        counts[p] = counts.get(p, 0) + 1  # @line L5
    return count  # @line L6


def longest_subarray_with_sum(a: list[int], k: int) -> tuple[int, int]:
    """Return (length, start) of a longest subarray with sum k, or (0, -1) if there is none.

    Among the longest ones, the one with the earliest end is returned.
    Cost: O(n) expected time, O(n) extra space.
    """
    first: dict[int, int] = {0: 0}
    p = 0
    best, start = 0, -1
    for j, x in enumerate(a):
        p += x
        i = first.get(p - k)
        if i is not None and j + 1 - i > best:
            best, start = j + 1 - i, i
        if p not in first:
            first[p] = j + 1
    return best, start


def count_subarrays_divisible(a: list[int], k: int) -> int:
    """Return the number of non-empty subarrays of a whose sum is a multiple of k > 0.

    Cost: O(n + k) time, O(k) extra space.
    """
    if k <= 0:
        raise ValueError("k must be positive")
    counts = [0] * k
    counts[0] = 1
    p = 0
    total = 0
    for x in a:
        p = (p + x) % k
        total += counts[p]
        counts[p] += 1
    return total
