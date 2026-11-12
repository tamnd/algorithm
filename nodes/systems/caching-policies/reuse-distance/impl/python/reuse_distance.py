# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reuse-distance/. The authors are listed in prov/30G9RA.jsonl.

"""Reuse distance (distinct items between two uses) and reuse time (all requests between two uses)."""

from typing import Hashable, List, Optional, Sequence


def reuse_times(seq: Sequence[Hashable]) -> List[Optional[int]]:
    """t - p for a request at t whose previous use is at p, or None for a first use."""
    last = {}
    out: List[Optional[int]] = []
    for t, x in enumerate(seq):
        out.append(t - last[x] if x in last else None)
        last[x] = t
    return out


def reuse_distances_naive(seq: Sequence[Hashable]) -> List[Optional[int]]:
    """The number of distinct items other than seq[t] requested strictly between the two uses."""
    last = {}
    out: List[Optional[int]] = []
    for t, x in enumerate(seq):
        out.append(len(set(seq[last[x] + 1:t])) if x in last else None)
        last[x] = t
    return out


def reuse_distances(seq: Sequence[Hashable]) -> List[Optional[int]]:
    """The same values in O(n log n) time.

    A Fenwick tree over positions has a 1 at the latest use of each item. The reuse distance of a
    request at t with previous use p is the number of 1s in positions p + 1 .. t - 1.
    """
    n = len(seq)
    tree = [0] * (n + 1)

    def add(i: int, v: int) -> None:
        i += 1
        while i <= n:
            tree[i] += v
            i += i & -i

    def prefix(i: int) -> int:  # sum of positions 0 .. i - 1
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    last = {}
    out: List[Optional[int]] = []
    for t, x in enumerate(seq):
        if x in last:
            p = last[x]
            out.append(prefix(t) - prefix(p + 1))
            add(p, -1)
        else:
            out.append(None)
        add(t, 1)
        last[x] = t
    return out


def lru_hits_from_distances(distances: Sequence[Optional[int]], k: int) -> int:
    """An LRU cache of size k hits exactly the requests with reuse distance less than k."""
    return sum(1 for d in distances if d is not None and d < k)
