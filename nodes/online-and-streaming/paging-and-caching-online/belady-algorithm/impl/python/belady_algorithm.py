# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belady-algorithm/. The authors are listed in prov/6CTF08.jsonl.

import heapq
from collections.abc import Hashable, Sequence


def next_requests(sigma: Sequence[Hashable]) -> list[int]:
    """Return nxt with nxt[t] the next position s > t with sigma[s] == sigma[t].

    Positions are 0-based, and len(sigma) stands for "never again".
    Cost: O(n) expected time and O(n) space, with n = len(sigma).
    """
    n = len(sigma)
    nxt = [n] * n
    last: dict[Hashable, int] = {}
    for t in range(n - 1, -1, -1):  # @line L1
        nxt[t] = last.get(sigma[t], n)
        last[sigma[t]] = t
    return nxt


def belady(sigma: Sequence[Hashable], k: int) -> tuple[int, list[Hashable | None]]:
    """Serve sigma with a cache of k pages that starts empty, by the rule MIN.

    Precondition: k >= 1 and the pages are hashable.
    Returns (faults, evicted), where evicted[t] is the page evicted at request t,
    or None if request t evicts nothing. Among pages that are never requested
    again, the page whose last request is oldest is evicted.
    Cost: O(n log n) time and O(n) space, with n = len(sigma).
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    n = len(sigma)
    nxt = next_requests(sigma)
    cache: set[Hashable] = set()  # @line L2
    key: dict[Hashable, int] = {}
    heap: list[tuple[int, int, Hashable]] = []  # entries (-next request, push time, page)
    faults = 0
    evicted: list[Hashable | None] = [None] * n
    for t in range(n):  # @line L3
        p = sigma[t]  # @line L4
        if p not in cache:  # @line L5
            faults += 1  # @line L6
            if len(cache) == k:  # @line L7
                while True:  # @line L8
                    neg_u, _, q = heapq.heappop(heap)
                    if q in cache and key[q] == -neg_u:
                        break
                cache.remove(q)  # @line L9
                evicted[t] = q
            cache.add(p)  # @line L10
        key[p] = nxt[t]  # @line L11
        heapq.heappush(heap, (-nxt[t], t, p))
    return faults, evicted  # @line L12
