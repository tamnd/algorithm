# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inclusion-property/. The authors are listed in prov/4SP6AS.jsonl.

"""Check the inclusion property: the cache of size k is a subset of the cache of size k + 1 at every time."""

from collections import OrderedDict
from typing import Callable, FrozenSet, Hashable, List, Optional, Sequence, Tuple

Contents = List[FrozenSet[Hashable]]


def lru_contents(seq: Sequence[Hashable], k: int) -> Contents:
    """The contents of an LRU cache of size k after each request."""
    cache: "OrderedDict[Hashable, bool]" = OrderedDict()
    out = []
    for x in seq:
        if x in cache:
            cache.move_to_end(x)
        else:
            if len(cache) == k:
                cache.popitem(last=False)
            cache[x] = True
        out.append(frozenset(cache))
    return out


def fifo_contents(seq: Sequence[Hashable], k: int) -> Contents:
    """The contents of a FIFO cache of size k after each request."""
    queue: List[Hashable] = []
    out = []
    for x in seq:
        if x not in queue:
            if len(queue) == k:
                queue.pop(0)
            queue.append(x)
        out.append(frozenset(queue))
    return out


def min_contents(seq: Sequence[Hashable], k: int) -> Contents:
    """The contents of Belady's MIN with a cache of size k after each request.

    The victim has the latest next use. Among items with no next use, the victim is the one
    used least recently. This tie rule does not depend on k.
    """
    n = len(seq)
    nxt, seen = [n] * n, {}
    for t in range(n - 1, -1, -1):
        nxt[t] = seen.get(seq[t], n)
        seen[seq[t]] = t
    nextuse, lastuse = {}, {}
    out = []
    for t, x in enumerate(seq):
        if x not in nextuse and len(nextuse) == k:
            victim = max(nextuse, key=lambda p: (nextuse[p], -lastuse[p]))
            del nextuse[victim]
        nextuse[x] = nxt[t]
        lastuse[x] = t
        out.append(frozenset(nextuse))
    return out


def first_violation(policy: Callable[[Sequence[Hashable], int], Contents], seq: Sequence[Hashable],
                    kmax: int) -> Optional[Tuple[int, int]]:
    """Return (k, t) for the first time t where contents(k) is not a subset of contents(k + 1), or None."""
    runs = [policy(seq, k) for k in range(1, kmax + 2)]
    for t in range(len(seq)):
        for k in range(1, kmax + 1):
            if not runs[k - 1][t] <= runs[k][t]:
                return k, t
    return None


def misses(policy: Callable[[Sequence[Hashable], int], Contents], seq: Sequence[Hashable], k: int) -> int:
    """The number of misses, read off the contents: request t misses if seq[t] was not cached after t - 1."""
    contents = policy(seq, k)
    count = 0
    before: FrozenSet[Hashable] = frozenset()
    for x, after in zip(seq, contents):
        if x not in before:
            count += 1
        before = after
    return count
