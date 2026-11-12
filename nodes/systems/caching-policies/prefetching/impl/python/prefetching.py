# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prefetching/. The authors are listed in prov/P6H46Y.jsonl.

"""Prefetching, in two models.

1. Hardware style, with no timing: an LRU cache of blocks and a prefetcher that loads
   blocks before they are asked for. The prefetchers are the sequential ones of Smith
   (always, on miss, tagged) and the stride prefetcher of Chen and Baer, with its
   reference prediction table.
2. The model of Cao, Felten, Karlin and Li (SIGMETRICS 1995): a known sequence, one
   reference per time unit, a cache of k blocks, and fetches of F time units, one at a
   time. It has their aggressive and conservative strategies, demand fetching with MIN,
   and an exact optimum by search over all schedules, for small inputs.
"""

from collections import OrderedDict, deque
from typing import Hashable, Iterable, Optional, Sequence


# ---------------------------------------------------------------- hardware style


class PrefetchCache:
    """An LRU cache of `capacity` blocks that counts demand misses and prefetches.

    A prefetched block goes in at the most recent end and carries a tag bit until its
    first demand use, which is what tagged prefetching needs.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.blocks: OrderedDict = OrderedDict()  # block -> True if prefetched and not used yet
        self.misses = self.hits = self.prefetches = self.useful = 0

    def demand(self, b: int) -> tuple[bool, bool]:
        """Access block b. Return (hit, first use of a prefetched block)."""
        if b in self.blocks:
            first = self.blocks[b]
            if first:
                self.useful += 1
            self.blocks[b] = False
            self.blocks.move_to_end(b)
            self.hits += 1
            return True, first
        self.misses += 1
        self._insert(b, False)
        return False, False

    def prefetch(self, b: int) -> None:
        if b in self.blocks:
            return
        self.prefetches += 1
        self._insert(b, True)

    def _insert(self, b: int, tag: bool) -> None:
        self.blocks[b] = tag
        if len(self.blocks) > self.capacity:
            self.blocks.popitem(last=False)


def sequential(blocks: Iterable[int], capacity: int, mode: str = "tagged") -> PrefetchCache:
    """One-block-lookahead prefetching of block i + 1 after a reference to block i.

    mode "none": no prefetching; "always": after every reference; "miss": after a miss;
    "tagged": after a miss and after the first use of a prefetched block.
    """
    if mode not in ("none", "always", "miss", "tagged"):
        raise ValueError("unknown mode")
    cache = PrefetchCache(capacity)
    for b in blocks:
        hit, first = cache.demand(b)
        if mode == "always" or (mode == "miss" and not hit) or (mode == "tagged" and (not hit or first)):
            cache.prefetch(b + 1)
    return cache


INITIAL, TRANSIENT, STEADY, NO_PRED = "initial", "transient", "steady", "no-pred"


class ReferencePredictionTable:
    """The basic stride prefetcher of Chen and Baer.

    One entry per load instruction (pc): the previous address, the stride, and a state.
    A hit is "correct" when address = previous + stride. Correct moves the state toward
    steady; incorrect moves it toward no-pred and, except from steady, learns the new
    stride. A prefetch of address + stride is issued unless the new state is no-pred.
    """

    MOVE = {
        (INITIAL, True): STEADY, (INITIAL, False): TRANSIENT,
        (TRANSIENT, True): STEADY, (TRANSIENT, False): NO_PRED,
        (STEADY, True): STEADY, (STEADY, False): INITIAL,
        (NO_PRED, True): TRANSIENT, (NO_PRED, False): NO_PRED,
    }

    def __init__(self, entries: int = 64) -> None:
        self.entries = entries
        self.table: OrderedDict = OrderedDict()  # pc -> [prev, stride, state], LRU order

    def access(self, pc: Hashable, address: int) -> Optional[int]:
        """Record a load; return the address to prefetch, or None."""
        e = self.table.get(pc)
        if e is None:
            self.table[pc] = [address, 0, INITIAL]
            if len(self.table) > self.entries:
                self.table.popitem(last=False)
            return None
        self.table.move_to_end(pc)
        prev, stride, state = e
        correct = address - prev == stride
        if not correct and state != STEADY:
            stride = address - prev
        state = self.MOVE[(state, correct)]
        e[0], e[1], e[2] = address, stride, state
        if state == NO_PRED or stride == 0:
            return None
        return address + stride


def stride_prefetch(loads: Iterable[tuple[Hashable, int]], capacity: int, entries: int = 64) -> PrefetchCache:
    """Run (pc, block) loads through an LRU cache with a reference prediction table."""
    cache = PrefetchCache(capacity)
    rpt = ReferencePredictionTable(entries)
    for pc, b in loads:
        cache.demand(b)
        target = rpt.access(pc, b)
        if target is not None:
            cache.prefetch(target)
    return cache


# ---------------------------------------------------------------- Cao, Felten, Karlin, Li


def _next_use(refs: Sequence[Hashable], i: int, b: Hashable) -> float:
    for j in range(i, len(refs)):
        if refs[j] == b:
            return j
    return float("inf")


def run_schedule(refs: Sequence[Hashable], k: int, F: int, start: Iterable[Hashable], choose) -> tuple[int, int]:
    """Simulate the model. Return (elapsed time, number of fetches).

    At the start of each time unit, a fetch that is due completes. Then, if no fetch is in
    progress, choose(i, cache, t) may return (block, victim) to start a fetch; victim is
    None when the cache has a free slot. The victim leaves at once, and the block arrives
    F units later. Then the reference refs[i] is served if its block is in the cache, or
    the time unit is a stall.
    """
    cache, inflight, t, i, fetches = set(start), None, 0, 0, 0
    if len(cache) > k:
        raise ValueError("the start set is larger than the cache")
    while i < len(refs):
        if inflight is not None and inflight[1] == t:
            cache.add(inflight[0])
            inflight = None
        if inflight is None:
            move = choose(i, frozenset(cache), t)
            if move is not None:
                block, victim = move
                if victim is None:
                    if len(cache) >= k:
                        raise ValueError("no free slot")
                else:
                    cache.remove(victim)
                inflight = (block, t + F)
                fetches += 1
        if refs[i] in cache:
            i += 1
        t += 1
    return t, fetches


def aggressive(refs: Sequence[Hashable], k: int, F: int, start: Iterable[Hashable] = ()) -> tuple[int, int]:
    """Fetch the next missing block as soon as the disk is free, replacing the block used
    furthest in the future, but only if that block is not needed before the missing one."""

    def choose(i, cache, t):
        j = next((j for j in range(i, len(refs)) if refs[j] not in cache), None)
        if j is None:
            return None  # rule 1: the next missing block; there is none
        if len(cache) < k:
            return refs[j], None
        victim = max(sorted(cache, key=repr), key=lambda b: _next_use(refs, i, b))  # rule 2
        if _next_use(refs, i, victim) <= j:
            return None  # rule 3: do no harm
        return refs[j], victim

    return run_schedule(refs, k, F, start, choose)


def min_fetches(refs: Sequence[Hashable], k: int, start: Iterable[Hashable] = ()) -> list[tuple[int, Hashable, Optional[Hashable]]]:
    """The demand fetches of Belady's MIN: (index of the miss, block, victim or None)."""
    cache, out = set(start), []
    for i, b in enumerate(refs):
        if b in cache:
            continue
        victim = None
        if len(cache) >= k:
            victim = max(sorted(cache, key=repr), key=lambda x: _next_use(refs, i, x))
            cache.remove(victim)
        cache.add(b)
        out.append((i, b, victim))
    return out


def demand_min(refs: Sequence[Hashable], k: int, F: int, start: Iterable[Hashable] = ()) -> tuple[int, int]:
    """No prefetching: fetch on a miss, with MIN replacement, while the cursor stalls."""
    plan = deque(min_fetches(refs, k, start))

    def choose(i, cache, t):
        if plan and plan[0][0] == i:
            _, b, v = plan.popleft()
            return b, v
        return None

    return run_schedule(refs, k, F, start, choose)


def conservative(refs: Sequence[Hashable], k: int, F: int, start: Iterable[Hashable] = ()) -> tuple[int, int]:
    """The fetches and replacements of MIN, each started as early as the disk and the
    do-no-harm rule allow: the victim must have no reference left before the miss."""
    plan = deque(min_fetches(refs, k, start))

    def choose(i, cache, t):
        if not plan:
            return None
        j, b, v = plan[0]
        if v is not None and (v not in cache or _next_use(refs, i, v) < j):
            return None
        plan.popleft()
        return b, v

    return run_schedule(refs, k, F, start, choose)


def optimal(refs: Sequence[Hashable], k: int, F: int, start: Iterable[Hashable] = (), rules: bool = False) -> int:
    """The least elapsed time over all schedules, by breadth-first search over time.

    The state is (cursor, cache, fetch in progress). Fetching a block that is never used
    again cannot help, so only blocks with a later use are fetched. With rules=True the
    search keeps only fetches that obey rules 1 to 3 of Cao et al.; it still decides when.
    """
    n = len(refs)
    layer = {(0, frozenset(start), None)}
    t = 0
    while True:
        nxt = set()
        for i, cache, inflight in layer:
            if inflight is not None and inflight[1] == 0:
                cache, inflight = cache | {inflight[0]}, None
            options = [(cache, inflight)]
            if inflight is None:
                future = set(refs[i:])
                if rules:
                    j = next((j for j in range(i, n) if refs[j] not in cache), None)
                    wanted = [] if j is None else [refs[j]]
                else:
                    wanted = sorted(future - cache, key=repr)
                for b in wanted:
                    if len(cache) < k:
                        options.append((cache, (b, F)))
                        continue
                    victims = sorted(cache, key=repr)
                    if rules:
                        v = max(victims, key=lambda x: _next_use(refs, i, x))
                        victims = [v] if _next_use(refs, i, v) > j else []
                    for v in victims:
                        options.append((cache - {v}, (b, F)))
            for c, fl in options:
                i2 = i + 1 if refs[i] in c else i
                if i2 == n:
                    return t + 1
                nxt.add((i2, c, None if fl is None else (fl[0], fl[1] - 1)))
        layer = nxt
        t += 1


def lru_fetches(refs: Sequence[Hashable], k: int, start: Iterable[Hashable] = ()) -> int:
    cache: OrderedDict = OrderedDict((b, True) for b in start)
    misses = 0
    for b in refs:
        if b in cache:
            cache.move_to_end(b)
        else:
            misses += 1
            cache[b] = True
            if len(cache) > k:
                cache.popitem(last=False)
    return misses
