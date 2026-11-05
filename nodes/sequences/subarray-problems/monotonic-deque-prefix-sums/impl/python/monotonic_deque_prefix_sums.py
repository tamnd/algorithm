# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monotonic-deque-prefix-sums/. The authors are listed in prov/HHFZR5.jsonl.

from collections import deque
from typing import Optional, Sequence, Union

Number = Union[int, float]


def shortest_subarray_at_least(a: Sequence[Number], k: Number) -> Optional[tuple[int, int]]:
    """Return (i, j) such that a[i:j] is a shortest non-empty subarray with sum >= k, or None.

    Items may be negative. Among shortest pairs, the one with the smallest end is returned.
    Cost: Theta(n) time and Theta(n) extra space.
    """
    n = len(a)
    p: list[Number] = [0] * (n + 1)  # @line L1
    for t in range(1, n + 1):
        p[t] = p[t - 1] + a[t - 1]
    q: deque[int] = deque()  # @line L2
    best = n + 1
    r: Optional[tuple[int, int]] = None
    for j in range(n + 1):  # @line L3
        while q and p[j] - p[q[0]] >= k:  # @line L4
            i = q.popleft()  # @line L5
            if j - i < best:
                best, r = j - i, (i, j)
        while q and p[q[-1]] >= p[j]:  # @line L6
            q.pop()
        q.append(j)  # @line L7
    return r  # @line L8


def shortest_length_at_least(a: Sequence[Number], k: Number) -> int:
    """Return the length of a shortest subarray with sum >= k, or -1 if there is none."""
    r = shortest_subarray_at_least(a, k)
    return -1 if r is None else r[1] - r[0]


def max_sum_with_length_between(a: Sequence[Number], lo: int, hi: int) -> Optional[Number]:
    """Return the largest sum of a[i:j] with lo <= j - i <= hi, or None if no length fits.

    Precondition: 1 <= lo <= hi (raises ValueError otherwise).
    Cost: Theta(n) time, a sliding window minimum of the prefix sums.
    """
    if lo < 1 or hi < lo:
        raise ValueError("need 1 <= lo <= hi")
    n = len(a)
    p: list[Number] = [0] * (n + 1)
    for t in range(1, n + 1):
        p[t] = p[t - 1] + a[t - 1]
    q: deque[int] = deque()
    best: Optional[Number] = None
    for j in range(lo, n + 1):
        s = j - lo
        while q and p[q[-1]] >= p[s]:
            q.pop()
        q.append(s)
        while q[0] < j - hi:
            q.popleft()
        cand = p[j] - p[q[0]]
        if best is None or cand > best:
            best = cand
    return best
