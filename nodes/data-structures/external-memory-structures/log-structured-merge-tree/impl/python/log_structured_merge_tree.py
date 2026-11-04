# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/log-structured-merge-tree/. The authors are listed in prov/T0A3TV.jsonl.

from bisect import bisect_left, bisect_right
from math import ceil
from typing import Any, Generic, Iterator, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)
V = TypeVar("V")

TOMB: Any = object()  # the value stored for a deleted key


class Run(Generic[K, V]):
    """A sorted run on disk: distinct keys in increasing order, with values
    or tombstones, cut into blocks of B entries. The first key of each block
    (the fence keys) is kept in memory."""

    def __init__(self, keys: list[K], vals: list[Any], block_size: int) -> None:
        self.keys = keys
        self.vals = vals
        self.fences = keys[::block_size]

    def __len__(self) -> int:
        return len(self.keys)


class LSMTree(Generic[K, V]):
    """A leveled log-structured merge tree.

    Updates go into a memtable of at most C0 entries in memory. When it is
    full, it is written out and merged into level 1. Level i holds one sorted
    run of at most C0 * T**i entries; a level that overflows is merged into
    the next one. A newer entry hides an older one on the same key, and a
    delete writes a tombstone, dropped when it reaches the last level.
    `ios` counts block reads and writes.
    """

    def __init__(self, block_size: int = 4, memtable_size: int = 4, ratio: int = 2) -> None:
        if block_size < 1 or memtable_size < 1 or ratio < 2:
            raise ValueError("need block_size >= 1, memtable_size >= 1, ratio >= 2")
        self.B = block_size
        self.C0 = memtable_size
        self.T = ratio
        self.mem: dict[K, Any] = {}
        self.levels: list[Run[K, V]] = []  # levels[0] is level 1
        self.ios = 0

    def capacity(self, i: int) -> int:
        """The capacity of level i + 1."""
        return self.C0 * self.T ** (i + 1)

    # updates -------------------------------------------------------------

    def put(self, k: K, v: V) -> None:
        """Insert k with value v, or replace its value."""
        self._update(k, v)

    def delete(self, k: K) -> None:
        """Delete k by writing a tombstone."""
        self._update(k, TOMB)

    def _update(self, k: K, v: Any) -> None:
        self.mem[k] = v  # @line L1
        if len(self.mem) >= self.C0:  # @line L2
            self._flush()

    def _flush(self) -> None:
        keys = sorted(self.mem)  # @line L3
        run: Run[K, V] = Run(keys, [self.mem[k] for k in keys], self.B)
        self.mem = {}
        i = 0
        while True:  # @line L4
            if i == len(self.levels):
                self.levels.append(Run([], [], self.B))
            last = all(len(r) == 0 for r in self.levels[i + 1 :])
            run = self._merge(run, self.levels[i], drop_tombs=last)  # @line L5
            if len(run) <= self.capacity(i):  # @line L6
                self.levels[i] = run
                return
            self.levels[i] = Run([], [], self.B)  # @line L7
            i += 1

    def _merge(self, new: Run[K, V], old: Run[K, V], drop_tombs: bool) -> Run[K, V]:
        """Merge two runs; on equal keys the entry of `new` wins."""
        self.ios += ceil(len(old) / self.B)  # `new` was just written or is in memory
        keys: list[K] = []
        vals: list[Any] = []
        a = b = 0
        while a < len(new) or b < len(old):
            if b == len(old) or (a < len(new) and new.keys[a] < old.keys[b]):
                k, v = new.keys[a], new.vals[a]
                a += 1
            elif a == len(new) or old.keys[b] < new.keys[a]:
                k, v = old.keys[b], old.vals[b]
                b += 1
            else:
                k, v = new.keys[a], new.vals[a]
                a += 1
                b += 1
            if drop_tombs and v is TOMB:
                continue
            keys.append(k)
            vals.append(v)
        self.ios += ceil(len(keys) / self.B)
        return Run(keys, vals, self.B)

    # queries -------------------------------------------------------------

    def get(self, k: K, default: Optional[V] = None) -> Optional[V]:
        """Return the value of k, or default if k is absent."""
        if k in self.mem:  # @line L8
            v = self.mem[k]
            return default if v is TOMB else v
        for run in self.levels:  # @line L9
            if not run.keys or k < run.keys[0]:
                continue
            blk = bisect_right(run.fences, k) - 1  # the fence keys are in memory
            self.ios += 1
            lo = blk * self.B
            hi = min(lo + self.B, len(run))
            j = bisect_left(run.keys, k, lo, hi)
            if j < hi and not (k < run.keys[j]):  # @line L10
                v = run.vals[j]
                return default if v is TOMB else v
        return default  # @line L11

    def range(self, lo: K, hi: K) -> list[tuple[K, V]]:
        """All live pairs with lo <= key <= hi, in key order."""
        seen: dict[K, Any] = {}
        for run in reversed(self.levels):  # oldest first, newer ones overwrite
            a = bisect_left(run.keys, lo)
            b = bisect_right(run.keys, hi)
            self.ios += ceil((b - a) / self.B) + (1 if a < b else 0)
            for j in range(a, b):
                seen[run.keys[j]] = run.vals[j]
        for k, v in self.mem.items():
            if not (k < lo) and not (hi < k):
                seen[k] = v
        return [(k, seen[k]) for k in sorted(seen) if seen[k] is not TOMB]

    def items(self) -> list[tuple[K, V]]:
        out: dict[K, Any] = {}
        for run in reversed(self.levels):
            out.update(zip(run.keys, run.vals))
        out.update(self.mem)
        return [(k, out[k]) for k in sorted(out) if out[k] is not TOMB]

    def __iter__(self) -> Iterator[K]:
        return iter([k for k, _ in self.items()])

    def __len__(self) -> int:
        return len(self.items())

    # checking -----------------------------------------------------------

    def check_invariant(self) -> None:
        """Raise AssertionError if a property of the tree fails."""
        assert len(self.mem) < self.C0
        for i, run in enumerate(self.levels):
            assert len(run.keys) == len(run.vals) <= self.capacity(i)
            assert all(a < b for a, b in zip(run.keys, run.keys[1:]))
            assert run.fences == run.keys[:: self.B]
        nonempty = [i for i, r in enumerate(self.levels) if len(r)]
        if nonempty:
            assert all(v is not TOMB for v in self.levels[nonempty[-1]].vals)
