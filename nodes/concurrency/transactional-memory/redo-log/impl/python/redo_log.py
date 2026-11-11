# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/redo-log/. The authors are listed in prov/H76MZA.jsonl.

"""The redo log of a lazy-versioning STM: a private buffer of the new values of one transaction.

The log keeps one entry per written word, in the order of the first write, with
the last value written. A dict maps each word to its entry, so a read after
write finds the buffered value in O(1) expected time. A small Bloom filter (a
bit mask) answers most lookups of words that the transaction never wrote
without a probe of the dict. At commit the STM copies the entries to memory
(write-back); at abort it throws the log away.

Counters: probes counts dict probes and scan steps, so the tests can compare
the indexed log with a log that is searched by a linear scan.
"""

from __future__ import annotations

import hashlib
from typing import Any, Iterator

MISS = object()


class RedoLog:
    def __init__(self, filter_bits: int = 64, hashes: int = 2, indexed: bool = True) -> None:
        self.entries: list[list[Any]] = []  # [word, value], in the order of the first write
        self.index: dict[Any, int] = {}
        self.filter = 0
        self.filter_bits = filter_bits
        self.hashes = hashes
        self.indexed = indexed
        self.probes = 0

    def _bits(self, a: Any) -> Iterator[int]:
        # A fixed hash (not Python's hash, which changes from run to run for strings).
        d = hashlib.blake2b(repr(a).encode(), digest_size=4 * self.hashes).digest()
        for i in range(self.hashes):
            yield int.from_bytes(d[4 * i:4 * i + 4], "little") % self.filter_bits

    def may_contain(self, a: Any) -> bool:
        return all(self.filter >> b & 1 for b in self._bits(a))

    def write(self, a: Any, v: Any) -> None:
        i = self._find(a)
        if i is not None:  # @line L1
            self.entries[i][1] = v
            return
        self.index[a] = len(self.entries)  # @line L2
        self.entries.append([a, v])
        for b in self._bits(a):
            self.filter |= 1 << b

    def _find(self, a: Any) -> int | None:
        if self.indexed:
            self.probes += 1
            return self.index.get(a)
        for i, (b, _) in enumerate(self.entries):
            self.probes += 1
            if b == a:
                return i
        return None

    def lookup(self, a: Any) -> Any:
        """The buffered value of a, or MISS if the transaction did not write a."""
        if not self.may_contain(a):  # @line L3
            return MISS
        i = self._find(a)  # @line L4
        return MISS if i is None else self.entries[i][1]

    def write_back(self, mem: dict) -> int:
        """Copy every entry to memory. Return the number of words written."""
        for a, v in self.entries:  # @line L5
            mem[a] = v
        return len(self.entries)

    def discard(self) -> None:
        self.entries.clear()  # @line L6
        self.index.clear()
        self.filter = 0

    def __len__(self) -> int:
        return len(self.entries)


class AppendOnlyRedoLog:
    """A variant that appends every write. Write-back in log order still gives the last
    value of each word, but the log grows with each write, and a lookup must take the
    last entry for the word."""

    def __init__(self) -> None:
        self.entries: list[tuple[Any, Any]] = []

    def write(self, a: Any, v: Any) -> None:
        self.entries.append((a, v))

    def lookup(self, a: Any) -> Any:
        for b, v in reversed(self.entries):
            if b == a:
                return v
        return MISS

    def write_back(self, mem: dict) -> int:
        for a, v in self.entries:
            mem[a] = v
        return len(self.entries)
