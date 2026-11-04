# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/concurrent-hash-table/. The authors are listed in prov/HQKVBH.jsonl.

import threading
import time
from collections.abc import Generator, Hashable
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
R = TypeVar("R")

MISSING = object()  # the result of get or remove when the key is absent
SPIN = "spin"  # what a step generator yields while it waits for a lock

Steps = Generator[str | None, None, R]


def acquire(lock: threading.Lock) -> Generator[str | None, None, None]:
    """Take the lock, one try per step; yield SPIN while another holder has it."""
    while not lock.acquire(blocking=False):
        yield SPIN


def run(steps: "Steps[R]") -> R:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


class ConcurrentHashTable(Generic[K, V]):
    """A chained hash table with lock striping, as in the StripedHashSet of Herlihy and Shavit.

    There are L locks. The bucket array has a capacity that is always a
    multiple of L, so bucket b is guarded by lock b mod L, and a key k with
    hash h is guarded by lock h mod L whatever the capacity is. put, get and
    remove hold one lock and take O(1 + chain length) steps; resize takes
    all L locks in index order and doubles the capacity. The table is
    linearizable and deadlock-free.

    The *_steps methods are generators that yield after each step on shared
    memory, for tests that choose the interleaving; the plain methods run the
    same steps and are safe to call from threads.
    """

    def __init__(self, stripes: int = 4, capacity: int = 4, max_load: float = 2.0) -> None:
        if stripes < 1 or capacity < stripes or capacity % stripes:
            raise ValueError("capacity must be a positive multiple of stripes")
        self.locks = [threading.Lock() for _ in range(stripes)]
        self.buckets: list[list[tuple[K, V]]] = [[] for _ in range(capacity)]
        self.counts = [0] * stripes  # counts[i]: pairs in the stripe of lock i
        self.max_load = max_load
        self.resizes = 0

    def _stripe(self, k: K) -> int:
        return hash(k) % len(self.locks)

    def put_steps(self, k: K, v: V) -> "Steps[object]":
        """Map k to v; return the old value, or MISSING if k was absent."""
        i = self._stripe(k)
        yield from acquire(self.locks[i])  # @line L1
        table = self.buckets  # @line L2
        b = table[hash(k) % len(table)]
        yield None
        old: object = MISSING
        for j, (key, val) in enumerate(b):  # @line L3
            if key == k:
                old = val
                b[j] = (k, v)  # @line L4
                break
        else:
            b.append((k, v))  # @line L5
            self.counts[i] += 1
        yield None
        cap = len(table)
        self.locks[i].release()  # @line L6
        if sum(self.counts) > self.max_load * cap:  # @line L7
            yield from self.resize_steps(cap)  # @line L8
        return old  # @line L9

    def get_steps(self, k: K) -> "Steps[object]":
        """Return the value of k, or MISSING."""
        i = self._stripe(k)
        yield from acquire(self.locks[i])  # @line L10
        table = self.buckets
        b = table[hash(k) % len(table)]
        yield None
        res: object = MISSING
        for key, val in b:  # @line L11
            if key == k:
                res = val
                break
        self.locks[i].release()  # @line L12
        return res

    def remove_steps(self, k: K) -> "Steps[object]":
        """Delete k; return its old value, or MISSING if it was absent."""
        i = self._stripe(k)
        yield from acquire(self.locks[i])
        table = self.buckets
        b = table[hash(k) % len(table)]
        yield None
        res: object = MISSING
        for j, (key, val) in enumerate(b):
            if key == k:
                res = val
                del b[j]
                self.counts[i] -= 1
                break
        yield None
        self.locks[i].release()
        return res

    def resize_steps(self, old_cap: int) -> "Steps[None]":
        """Double the capacity, unless another thread resized since the caller saw old_cap."""
        for lock in self.locks:  # @line L13
            yield from acquire(lock)
        try:
            if len(self.buckets) == old_cap:  # @line L14
                new: list[list[tuple[K, V]]] = [[] for _ in range(2 * old_cap)]
                for b in self.buckets:  # @line L15
                    for k, v in b:
                        new[hash(k) % len(new)].append((k, v))
                self.buckets = new  # @line L16
                self.resizes += 1
            yield None
        finally:
            for lock in self.locks:  # @line L17
                lock.release()

    def put(self, k: K, v: V) -> object:
        return run(self.put_steps(k, v))

    def get(self, k: K) -> object:
        return run(self.get_steps(k))

    def remove(self, k: K) -> object:
        return run(self.remove_steps(k))

    def to_dict(self) -> dict[K, V]:
        """The contents, read at a quiet moment."""
        return {k: v for b in self.buckets for k, v in b}

    def check_invariant(self) -> None:
        """At a quiet moment: each pair is in its bucket, keys are unique, counts are right."""
        cap, n = len(self.buckets), len(self.locks)
        assert cap % n == 0
        counts = [0] * n
        seen = set()
        for idx, b in enumerate(self.buckets):
            for k, _ in b:
                assert hash(k) % cap == idx and k not in seen
                assert idx % n == hash(k) % n  # the bucket and the key share a stripe
                seen.add(k)
                counts[hash(k) % n] += 1
        assert counts == self.counts
        assert not any(lock.locked() for lock in self.locks)
