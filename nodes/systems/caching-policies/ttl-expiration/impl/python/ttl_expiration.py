# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ttl-expiration/. The authors are listed in prov/WFW1C7.jsonl.

"""A TTL cache with a simulated clock: lazy expiry on access and an active sweep.

An entry set at time t with time-to-live T is live while now < t + T. With an
absolute TTL a hit does not change the expiry time; with a sliding TTL each hit
moves it to now + T. get() removes an expired entry when it sees one (lazy
expiry). sweep(now) removes every expired entry, in order of expiry time, with a
min-heap of (expiry, sequence number, key). An entry that was overwritten or
extended leaves an old heap item behind; the sweep skips such items by their
sequence number, and the heap is rebuilt when old items are more than half.
"""

import heapq
import math


class TTLCache:
    def __init__(self, sliding=False):
        self.sliding = sliding
        self.data = {}  # key -> [value, expiry, ttl, seq]
        self.heap = []  # (expiry, seq, key)
        self.seq = 0
        self.lazy_expired = 0
        self.swept = 0

    def _push(self, key, entry):
        self.seq += 1
        entry[3] = self.seq
        heapq.heappush(self.heap, (entry[1], self.seq, key))
        if len(self.heap) > 2 * len(self.data) + 16:
            self.heap = [(e[1], e[3], k) for k, e in self.data.items()]
            heapq.heapify(self.heap)

    def set(self, key, value, now, ttl):
        if ttl <= 0:
            self.data.pop(key, None)
            return
        entry = [value, now + ttl, ttl, 0]
        self.data[key] = entry
        self._push(key, entry)

    def delete(self, key):
        return self.data.pop(key, None) is not None

    def get(self, key, now, default=None):
        """Return the value, or default on a miss. An expired entry is removed here."""
        entry = self.data.get(key)
        if entry is None:
            return default
        if now >= entry[1]:
            del self.data[key]  # lazy expiry
            self.lazy_expired += 1
            return default
        if self.sliding:
            entry[1] = now + entry[2]
            self._push(key, entry)
        return entry[0]

    def contains(self, key, now):
        entry = self.data.get(key)
        return entry is not None and now < entry[1]

    def sweep(self, now):
        """Active expiry: remove every entry with expiry <= now. Return how many."""
        removed = 0
        while self.heap and self.heap[0][0] <= now:
            expiry, seq, key = heapq.heappop(self.heap)
            entry = self.data.get(key)
            if entry is not None and entry[3] == seq:
                del self.data[key]
                removed += 1
        self.swept += removed
        return removed

    def stored(self):
        """Number of stored entries, expired or not (memory in use)."""
        return len(self.data)


def simulate_hit_ratio(lam, ttl, n, rng, sliding=False):
    """One item with Poisson requests of rate lam. On a miss, cache it for ttl.

    Return the fraction of hits among n requests. Uses TTLCache itself."""
    cache = TTLCache(sliding=sliding)
    now, hits = 0.0, 0
    for _ in range(n):
        now += rng.expovariate(lam)
        if cache.get("x", now) is not None:
            hits += 1
        else:
            cache.set("x", 1, now, ttl)
    return hits / n


def hit_probability(lam, ttl, sliding=False):
    """Long-run hit probability under Poisson arrivals.

    Absolute TTL started at a miss: lam T / (1 + lam T). Sliding TTL: 1 - exp(-lam T)."""
    x = lam * ttl
    return -math.expm1(-x) if sliding else x / (1 + x)
