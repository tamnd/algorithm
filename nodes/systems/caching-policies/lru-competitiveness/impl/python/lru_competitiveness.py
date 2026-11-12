# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lru-competitiveness/. The authors are listed in prov/JZN82D.jsonl.

"""Pieces of the Sleator-Tarjan bound: LRU, FIFO, brute-force OPT_h, and the phase partition."""

from collections import OrderedDict
from typing import Hashable, List, Sequence


def lru_faults(seq: Sequence[Hashable], k: int) -> int:
    cache: "OrderedDict[Hashable, bool]" = OrderedDict()
    faults = 0
    for x in seq:
        if x in cache:
            cache.move_to_end(x)
        else:
            faults += 1
            if len(cache) == k:
                cache.popitem(last=False)
            cache[x] = True
    return faults


def fifo_faults(seq: Sequence[Hashable], k: int) -> int:
    queue: List[Hashable] = []
    faults = 0
    for x in seq:
        if x not in queue:
            faults += 1
            if len(queue) == k:
                queue.pop(0)
            queue.append(x)
    return faults


def opt_faults(seq: Sequence[Hashable], h: int) -> int:
    """Least faults of any demand-paging algorithm with h frames from an empty cache.

    Exhaustive search over every eviction choice (dynamic programming over cache contents),
    with no use of Belady's rule.
    """
    states = {frozenset(): 0}
    for x in seq:
        new = {}
        for c, f in states.items():
            if x in c:
                nxt = [(c, f)]
            elif len(c) < h:
                nxt = [(c | {x}, f + 1)]
            else:
                nxt = [((c - {y}) | {x}, f + 1) for y in c]
            for s, v in nxt:
                if v < new.get(s, v + 1):
                    new[s] = v
        states = new
    return min(states.values())


def phases(seq: Sequence[Hashable], k: int) -> List[int]:
    """Start positions of the k-phases: a new phase starts at the request that would make
    the current phase hold k + 1 distinct pages."""
    starts: List[int] = []
    seen: set = set()
    for t, x in enumerate(seq):
        if not starts or (x not in seen and len(seen) == k):
            starts.append(t)
            seen = set()
        seen.add(x)
    return starts
