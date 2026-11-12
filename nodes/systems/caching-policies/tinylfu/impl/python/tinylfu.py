# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tinylfu/. The authors are listed in prov/F0NQ2Y.jsonl.

import hashlib
import random
from collections import OrderedDict
from collections.abc import Hashable, Iterable


class FrequencyFilter:
    """The TinyLFU frequency filter of Einziger, Friedman and Manes (2017).

    A count-min sketch with conservative update and counters capped at
    W / c, a doorkeeper Bloom filter in front of it, and the reset that
    halves every counter after W additions. Hashing is blake2b with salts
    drawn from a seeded random.Random, so runs are reproducible.
    """

    def __init__(self, c: int, sample_factor: int = 10, depth: int = 4,
                 width: int | None = None, door_bits: int | None = None,
                 door_hashes: int = 3, seed: int = 0) -> None:
        rng = random.Random(seed)
        self.window = sample_factor * c  # W, the sample size
        self.cap = max(1, self.window // c)  # a counter never passes W / c
        self.width = width or max(16, 4 * c)
        self.rows = [[0] * self.width for _ in range(depth)]
        self.salts = [rng.getrandbits(64).to_bytes(8, "big") for _ in range(depth)]
        self.door_bits = door_bits or max(64, 4 * self.window)
        self.door_salts = [rng.getrandbits(64).to_bytes(8, "big") for _ in range(door_hashes)]
        self.door = bytearray(self.door_bits)
        self.additions = 0
        self.resets = 0

    @staticmethod
    def _h(salt: bytes, x: Hashable, m: int) -> int:
        d = hashlib.blake2b(repr(x).encode(), digest_size=8, salt=salt).digest()
        return int.from_bytes(d, "big") % m

    def _cells(self, x: Hashable) -> list[int]:
        return [self._h(s, x, self.width) for s in self.salts]

    def in_door(self, x: Hashable) -> bool:
        return all(self.door[self._h(s, x, self.door_bits)] for s in self.door_salts)

    def sketch(self, x: Hashable) -> int:
        return min(row[j] for row, j in zip(self.rows, self._cells(x)))

    def add(self, x: Hashable) -> None:
        """RECORD: count one access to x."""
        if not self.in_door(x):  # @line L10
            for s in self.door_salts:
                self.door[self._h(s, x, self.door_bits)] = 1
        else:  # @line L11
            cells = self._cells(x)
            low = min(row[j] for row, j in zip(self.rows, cells))
            if low < self.cap:  # conservative update: raise only the minimal counters
                for row, j in zip(self.rows, cells):
                    if row[j] == low:
                        row[j] += 1
        self.additions += 1  # @line L12
        if self.additions == self.window:  # @line L13
            self.reset()

    def reset(self) -> None:
        for row in self.rows:  # @line L14
            for j in range(self.width):
                row[j] //= 2
        self.door = bytearray(self.door_bits)
        self.additions //= 2
        self.resets += 1

    def estimate(self, x: Hashable) -> int:
        return self.sketch(x) + (1 if self.in_door(x) else 0)  # @line L15


class TinyLFU:
    """An LRU cache of c objects behind the TinyLFU admission filter."""

    def __init__(self, c: int, seed: int = 0, **filter_args) -> None:
        if c < 1:
            raise ValueError("the cache size must be at least 1")
        self.c = c
        self.filter = FrequencyFilter(c, seed=seed, **filter_args)
        self.cache: OrderedDict[Hashable, None] = OrderedDict()  # LRU end first
        self.last: tuple[Hashable, bool] | None = None  # (victim, admitted) of the last full miss

    def __contains__(self, x: Hashable) -> bool:
        return x in self.cache

    def __len__(self) -> int:
        return len(self.cache)

    def access(self, x: Hashable) -> bool:
        """Serve one request. Return True on a hit."""
        self.last = None
        self.filter.add(x)  # @line L1
        if x in self.cache:  # @line L2
            self.cache.move_to_end(x)  # @line L3
            return True
        if len(self.cache) < self.c:  # @line L4
            self.cache[x] = None  # @line L5
            return False
        v = next(iter(self.cache))  # @line L6
        admit = self.filter.estimate(x) > self.filter.estimate(v)  # @line L7
        if admit:
            del self.cache[v]  # @line L8
            self.cache[x] = None
        self.last = (v, admit)
        return False  # @line L9


def tinylfu_hits(trace: Iterable[Hashable], c: int, seed: int = 0, **filter_args) -> list[bool]:
    """Run TinyLFU over LRU with c objects. Return one hit flag per request."""
    cache = TinyLFU(c, seed, **filter_args)
    return [cache.access(x) for x in trace]
