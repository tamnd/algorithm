# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belady-optimal/. The authors are listed in prov/WA9T1Y.jsonl.

"""Belady's MIN: on a miss with a full cache, evict the item whose next use is furthest away."""

import heapq
from typing import Hashable, List, Optional, Sequence, Tuple


def next_uses(seq: Sequence[Hashable]) -> List[int]:
    """next_uses(seq)[t] is the smallest s > t with seq[s] == seq[t], or len(seq) if there is none."""
    n = len(seq)
    nxt = [n] * n
    last = {}  # @line L1
    for t in range(n - 1, -1, -1):  # @line L2
        nxt[t] = last.get(seq[t], n)  # @line L3
        last[seq[t]] = t  # @line L4
    return nxt


def belady_optimal(seq: Sequence[Hashable], k: int) -> List[Tuple[bool, Optional[Hashable]]]:
    """Run MIN with a cache of k items. Return, for each request, (hit, evicted item or None)."""
    if k < 1:
        raise ValueError("k must be at least 1")
    nxt = next_uses(seq)
    # key: item in the cache -> position of its next use. heap: (-next use, push number, item);
    # stale entries are skipped. Ties (next use n) go to the item pushed first, the least recent.
    key, heap, misses = {}, [], 0  # @line L5
    count = 0
    out = []
    for t, x in enumerate(seq):  # @line L6, L7
        evicted = None
        hit = x in key
        if not hit:  # @line L8
            misses += 1  # @line L9
            if len(key) == k:  # @line L10
                while True:  # @line L11
                    neg, _, y = heapq.heappop(heap)
                    if key.get(y) == -neg:
                        break
                del key[y]  # @line L12
                evicted = y
        key[x] = nxt[t]  # @line L13
        heapq.heappush(heap, (-nxt[t], count, x))
        count += 1
        out.append((hit, evicted))
    return out  # @line L14: the misses are the requests with hit == False


def min_misses(seq: Sequence[Hashable], k: int) -> int:
    """The number of misses of MIN with a cache of k items, starting from an empty cache."""
    return sum(1 for hit, _ in belady_optimal(seq, k) if not hit)


def min_variable_size(seq: Sequence[Hashable], size: dict, capacity: int) -> int:
    """Furthest in the future with item sizes: evict furthest items until the new item fits.

    Counts misses (cost 1 each). Every size must be at most the capacity. This rule is not optimal.
    """
    nxt = next_uses(seq)
    key = {}
    used = 0
    misses = 0
    for t, x in enumerate(seq):
        if x not in key:
            misses += 1
            while used + size[x] > capacity:
                y = max(key, key=lambda p: key[p])
                used -= size[y]
                del key[y]
            used += size[x]
        key[x] = nxt[t]
    return misses
