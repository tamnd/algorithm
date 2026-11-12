# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/w-tinylfu/. The authors are listed in prov/MSGGRD.jsonl.

import hashlib
import random
from collections import OrderedDict
from collections.abc import Hashable, Iterable


class FrequencyFilter:
    """The TinyLFU filter: a count-min sketch with conservative update and
    counters capped at W / c, a doorkeeper Bloom filter, and a reset that
    halves every counter and clears the doorkeeper after W additions."""

    def __init__(self, c: int, sample_factor: int = 10, depth: int = 4, seed: int = 0) -> None:
        rng = random.Random(seed)
        self.window = sample_factor * c
        self.cap = max(1, self.window // c)
        self.width = max(16, 4 * c)
        self.rows = [[0] * self.width for _ in range(depth)]
        self.salts = [rng.getrandbits(64).to_bytes(8, "big") for _ in range(depth)]
        self.door_bits = max(64, 4 * self.window)
        self.door_salts = [rng.getrandbits(64).to_bytes(8, "big") for _ in range(3)]
        self.door = bytearray(self.door_bits)
        self.additions = 0

    @staticmethod
    def _h(salt: bytes, x: Hashable, m: int) -> int:
        d = hashlib.blake2b(repr(x).encode(), digest_size=8, salt=salt).digest()
        return int.from_bytes(d, "big") % m

    def _in_door(self, x: Hashable) -> bool:
        return all(self.door[self._h(s, x, self.door_bits)] for s in self.door_salts)

    def add(self, x: Hashable) -> None:
        if not self._in_door(x):
            for s in self.door_salts:
                self.door[self._h(s, x, self.door_bits)] = 1
        else:
            cells = [self._h(s, x, self.width) for s in self.salts]
            low = min(row[j] for row, j in zip(self.rows, cells))
            if low < self.cap:
                for row, j in zip(self.rows, cells):
                    if row[j] == low:
                        row[j] += 1
        self.additions += 1
        if self.additions == self.window:
            for row in self.rows:
                for j in range(self.width):
                    row[j] //= 2
            self.door = bytearray(self.door_bits)
            self.additions //= 2

    def estimate(self, x: Hashable) -> int:
        cells = [self._h(s, x, self.width) for s in self.salts]
        low = min(row[j] for row, j in zip(self.rows, cells))
        return low + (1 if self._in_door(x) else 0)


class WTinyLFU:
    """W-TinyLFU of Einziger, Friedman and Manes (2017), with a fixed window.

    An LRU window of `window` objects (1 percent of c by default, at least 1)
    takes every new object. The main cache of c - window objects is an SLRU
    with a protected segment of 80 percent and a probation segment that uses
    the rest. A window victim enters the main cache only if TinyLFU estimates
    it more frequent than the main victim, the LRU object of probation.
    """

    def __init__(self, c: int, window: int | None = None, seed: int = 0) -> None:
        if c < 2:
            raise ValueError("the cache size must be at least 2")
        self.c = c
        self.window_cap = window if window is not None else max(1, c // 100)
        if not 1 <= self.window_cap < c:
            raise ValueError("need 1 <= window < c")
        self.main_cap = c - self.window_cap
        self.protected_cap = self.main_cap * 4 // 5
        self.filter = FrequencyFilter(c, seed=seed)
        self.window: OrderedDict[Hashable, None] = OrderedDict()  # LRU end first
        self.probation: OrderedDict[Hashable, None] = OrderedDict()
        self.protected: OrderedDict[Hashable, None] = OrderedDict()
        self.evicted: Hashable | None = None
        self.duel: tuple[Hashable, Hashable, bool] | None = None  # (candidate, victim, admitted)

    def __contains__(self, x: Hashable) -> bool:
        return x in self.window or x in self.probation or x in self.protected

    def __len__(self) -> int:
        return len(self.window) + len(self.probation) + len(self.protected)

    def access(self, x: Hashable) -> bool:
        """Serve one request. Return True on a hit."""
        self.evicted, self.duel = None, None
        self.filter.add(x)  # @line L1
        if x in self.window:  # @line L2
            self.window.move_to_end(x)
            return True
        if x in self.protected:  # @line L3
            self.protected.move_to_end(x)
            return True
        if x in self.probation:  # @line L4
            del self.probation[x]
            self.protected[x] = None  # @line L5
            if len(self.protected) > self.protected_cap:  # @line L6
                y, _ = self.protected.popitem(last=False)
                self.probation[y] = None
            return True  # @line L7
        self.window[x] = None  # @line L8
        if len(self.window) > self.window_cap:  # @line L9
            w, _ = self.window.popitem(last=False)  # @line L10
            if len(self.probation) + len(self.protected) < self.main_cap:  # @line L11
                self.probation[w] = None
            else:
                v = next(iter(self.probation))  # @line L12
                admit = self.filter.estimate(w) > self.filter.estimate(v)  # @line L13
                self.duel = (w, v, admit)
                if admit:
                    del self.probation[v]
                    self.probation[w] = None
                    self.evicted = v
                else:  # @line L14
                    self.evicted = w
        return False  # @line L15


def w_tinylfu_hits(trace: Iterable[Hashable], c: int, window: int | None = None, seed: int = 0) -> list[bool]:
    """Run W-TinyLFU with c objects. Return one hit flag per request."""
    cache = WTinyLFU(c, window, seed)
    return [cache.access(x) for x in trace]
