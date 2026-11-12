# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-size-caching/. The authors are listed in prov/3V56B1.jsonl.

"""Caching with variable sizes and costs: an exact offline optimum by search, and two greedy rules.

The cache holds items of total size at most `capacity`. A request for an item that
is not in the cache is a miss and costs cost[x]. In the forced model the item must
then be in the cache; in the optional model the cache may also serve it without
loading it (bypass). The functions are for small instances: the optimum takes time
exponential in the number of distinct items.
"""

from itertools import combinations
from typing import Hashable, Mapping, Sequence

Item = Hashable


def fault_costs(items: Sequence[Item]) -> dict[Item, int]:
    """The fault model: each miss costs 1."""
    return {x: 1 for x in items}


def bit_costs(size: Mapping[Item, int]) -> dict[Item, int]:
    """The bit model: a miss costs the size of the item."""
    return dict(size)


def _check(trace: Sequence[Item], size: Mapping[Item, int], capacity: int) -> None:
    for x in trace:
        if size[x] <= 0 or size[x] > capacity:
            raise ValueError(f"item {x!r} has size {size[x]}, which is not in 1..{capacity}")


def optimal_cost(
    trace: Sequence[Item],
    size: Mapping[Item, int],
    cost: Mapping[Item, int],
    capacity: int,
    optional: bool = False,
) -> int:
    """The least total miss cost of an offline policy, by search over all cache states.

    After each request we keep, for each reachable cache content, the least cost to
    reach it. On a miss the policy may evict any subset of the cache that makes room.
    Evicting only at a miss loses nothing, so the search is exact.
    """
    _check(trace, size, capacity)
    best: dict[frozenset, int] = {frozenset(): 0}
    for x in trace:
        nxt: dict[frozenset, int] = {}

        def relax(state: frozenset, value: int) -> None:
            if value < nxt.get(state, value + 1):
                nxt[state] = value

        for state, value in best.items():
            if x in state:
                relax(state, value)
                continue
            if optional:
                relax(state, value + cost[x])
            used = sum(size[y] for y in state)
            members = sorted(state, key=repr)
            for r in range(len(members) + 1):
                for out in combinations(members, r):
                    freed = sum(size[y] for y in out)
                    if used - freed + size[x] <= capacity:
                        relax((state - frozenset(out)) | {x}, value + cost[x])
        best = nxt
    return min(best.values())


def _next_use(trace: Sequence[Item], t: int, y: Item) -> int:
    for u in range(t + 1, len(trace)):
        if trace[u] == y:
            return u
    return len(trace)


def belady_rule_cost(
    trace: Sequence[Item], size: Mapping[Item, int], cost: Mapping[Item, int], capacity: int
) -> int:
    """Belady's rule used as it is: evict the item with the furthest next use until the new item fits."""
    _check(trace, size, capacity)
    cache: set = set()
    total = 0
    for t, x in enumerate(trace):
        if x in cache:
            continue
        total += cost[x]
        while sum(size[y] for y in cache) + size[x] > capacity:
            victim = max(sorted(cache, key=repr), key=lambda y: _next_use(trace, t, y))
            cache.remove(victim)
        cache.add(x)
    return total


def belady_rule_trace(
    trace: Sequence[Item], size: Mapping[Item, int], capacity: int
) -> list[tuple[Item, bool, list[Item], list[Item]]]:
    """The steps of Belady's rule: (request, hit, evicted items, cache after), for the page table."""
    cache: list = []
    rows = []
    for t, x in enumerate(trace):
        if x in cache:
            rows.append((x, True, [], sorted(cache, key=repr)))
            continue
        out = []
        while sum(size[y] for y in cache) + size[x] > capacity:
            victim = max(sorted(cache, key=repr), key=lambda y: _next_use(trace, t, y))
            cache.remove(victim)
            out.append(victim)
        cache.append(x)
        rows.append((x, False, out, sorted(cache, key=repr)))
    return rows
