# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shards/. The authors are listed in prov/8186QR.jsonl.

"""SHARDS (Waldspurger, Park, Garthwaite and Ahmad, FAST 2015): an approximate LRU miss
ratio curve from the requests of a hash-chosen sample of the items.

An item L is sampled when T_L = hash(L) mod P is below the threshold T, so the sampling
rate is R = T / P. Reuse distances are computed exactly among the sampled items and then
scaled by 1 / R. Fixed-rate SHARDS keeps T. Fixed-size SHARDS keeps at most s_max items:
when one more would enter, it drops the items with the largest T_L and lowers T to that
value, and it rescales the histogram so that old counts match the new rate.
"""

import hashlib
import heapq
from typing import Hashable, Iterable, Sequence

P = 1 << 24


def item_hash(key: Hashable, salt: int = 0) -> int:
    """A fixed hash of the item, the same in each run, reduced mod P."""
    data = repr(key).encode()
    digest = hashlib.blake2b(data, digest_size=8, salt=salt.to_bytes(8, "little")).digest()
    return int.from_bytes(digest, "little") % P


class LiveMarks:
    """Marks at the times of the last use of live items, in a Fenwick tree with compaction.

    distance(key) counts the live items used after the last use of key; the space stays
    O(number of live items) because the times are renumbered when the array fills up.
    """

    def __init__(self) -> None:
        self.size = 16
        self.tree = [0] * (self.size + 1)
        self.next = 1
        self.last: dict = {}
        self.count = 0

    def _add(self, i: int, delta: int) -> None:
        while i <= self.size:
            self.tree[i] += delta
            i += i & -i

    def _prefix(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

    def _compact(self) -> None:
        order = sorted(self.last, key=self.last.get)
        self.size = 2 * len(order) + 16
        self.tree = [0] * (self.size + 1)
        for i, key in enumerate(order, start=1):
            self.last[key] = i
            self._add(i, 1)
        self.next = len(order) + 1

    def access(self, key: Hashable) -> int | None:
        """Record a use of key; return the number of distinct live items used since its last use."""
        if self.next > self.size:
            self._compact()
        p = self.last.get(key)
        d = None
        if p is not None:
            d = self.count - self._prefix(p)
            self._add(p, -1)
            self.count -= 1
        self.last[key] = self.next
        self._add(self.next, 1)
        self.count += 1
        self.next += 1
        return d

    def remove(self, key: Hashable) -> None:
        p = self.last.pop(key)
        self._add(p, -1)
        self.count -= 1


class Shards:
    """SHARDS with a fixed rate (s_max=None) or a fixed size s_max.

    The histogram maps a bucket b (scaled distances in [b * width, (b + 1) * width)) to a count.
    """

    def __init__(self, rate: float = 0.01, s_max: int | None = None, width: int = 1, salt: int = 0, adjust: bool = False) -> None:
        if not 0 < rate <= 1:
            raise ValueError("rate must be in (0, 1]")
        self.T = round(rate * P)
        self.s_max = s_max
        self.width = width
        self.salt = salt
        self.adjust = adjust
        self.marks = LiveMarks()
        self.hist: dict[int, float] = {}
        self.t_bucket: dict[int, int] = {}  # the threshold at the last update of each bucket
        self.cold = 0.0
        self.t_cold = self.T
        self.total_requests = 0
        self.sampled = 0.0
        self.t_sampled = self.T
        self._heap: list[tuple[int, Hashable]] = []  # (-T_L, L) for the items in the sample set

    def _rescale(self, value: float, t_old: int) -> float:
        return value * self.T / t_old if t_old != self.T else value

    def _count(self, bucket: int | None) -> None:
        self.sampled = self._rescale(self.sampled, self.t_sampled) + 1
        self.t_sampled = self.T
        if bucket is None:
            self.cold = self._rescale(self.cold, self.t_cold) + 1
            self.t_cold = self.T
            return
        old = self.hist.get(bucket, 0.0)
        self.hist[bucket] = self._rescale(old, self.t_bucket.get(bucket, self.T)) + 1
        self.t_bucket[bucket] = self.T

    def access(self, key: Hashable) -> None:
        self.total_requests += 1
        t_l = item_hash(key, self.salt)
        if t_l >= self.T:  # @line L1
            return
        new = key not in self.marks.last
        d = self.marks.access(key)  # @line L2
        if new and self.s_max is not None:
            heapq.heappush(self._heap, (-t_l, key))
            if len(self._heap) > self.s_max:  # @line L3
                t_max = -self._heap[0][0]
                while self._heap and -self._heap[0][0] == t_max:  # @line L4
                    _, out = heapq.heappop(self._heap)
                    self.marks.remove(out)
                self.T = t_max  # @line L5
                if t_l >= self.T:  # the new item itself left the sample
                    return
        if d is None:
            self._count(None)  # @line L6
        else:
            scaled = d * P / self.T  # @line L7
            self._count(int(scaled // self.width))  # @line L8

    def feed(self, trace: Iterable[Hashable]) -> "Shards":
        for key in trace:
            self.access(key)
        return self

    def curve(self, sizes: Sequence[int]) -> list[float]:
        """The estimated miss ratio of LRU at each size c: the share of scaled distances >= c."""
        hist = {b: self._rescale(v, self.t_bucket[b]) for b, v in self.hist.items()}
        total = self._rescale(self.sampled, self.t_sampled)
        if self.adjust and self.s_max is None:
            # SHARDS_adj: correct the sample count to its expected value N * R in the first bucket
            expected = self.total_requests * self.T / P
            hist[0] = hist.get(0, 0.0) + expected - total
            total = expected
        if total <= 0:
            return [1.0 for _ in sizes]
        out = []
        for c in sizes:
            # a request hits a cache of size c when its scaled distance is below c
            hits = sum(v for b, v in hist.items() if (b + 1) * self.width <= c)
            out.append(min(1.0, max(0.0, 1 - hits / total)))  # @line L9
        return out


def shards_curve(trace: Iterable[Hashable], sizes: Sequence[int], **options) -> list[float]:
    return Shards(**options).feed(trace).curve(sizes)
