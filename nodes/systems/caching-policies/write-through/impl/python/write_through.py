# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-through/. The authors are listed in prov/J9Z92K.jsonl.

"""A write-through cache in front of a slower store.

The cache holds at most k lines of `block` words each and replaces lines in LRU
order. Every write goes to the store at once. On a write miss the cache either
fetches the line and keeps it (write-allocate) or leaves the cache unchanged
(no-write-allocate). The store is a dict from a line number to a list of words.
"""

from collections import OrderedDict


class Stats:
    """Counters of one run. A store write is one write operation on the store."""

    FIELDS = ("read_hits", "read_misses", "write_hits", "write_misses",
              "line_reads", "store_writes", "words_written")

    def __init__(self):
        for f in self.FIELDS:
            setattr(self, f, 0)

    def as_dict(self):
        return {f: getattr(self, f) for f in self.FIELDS}


class WriteThroughCache:
    def __init__(self, k, block=1, write_allocate=False, store=None):
        if k < 1 or block < 1:
            raise ValueError("k and block must be positive")
        self.k = k
        self.block = block
        self.write_allocate = write_allocate
        self.store = store if store is not None else {}
        self.lines = OrderedDict()  # line -> list of words, least recent first
        self.stats = Stats()

    def _split(self, addr):
        return addr // self.block, addr % self.block

    def _store_line(self, line):
        if line not in self.store:
            self.store[line] = [0] * self.block
        return self.store[line]

    def _fetch(self, line):
        self.stats.line_reads += 1
        return list(self._store_line(line))

    def _insert(self, line, data):
        if len(self.lines) == self.k:
            self.lines.popitem(last=False)  # every line is clean: drop it, no store write
        self.lines[line] = data

    def read(self, addr):
        line, off = self._split(addr)
        if line in self.lines:
            self.stats.read_hits += 1
            self.lines.move_to_end(line)
        else:
            self.stats.read_misses += 1
            self._insert(line, self._fetch(line))
        return self.lines[line][off]

    def write(self, addr, value):
        line, off = self._split(addr)
        if line in self.lines:
            self.stats.write_hits += 1
            self.lines[line][off] = value
            self.lines.move_to_end(line)
        else:
            self.stats.write_misses += 1
            if self.write_allocate:
                data = self._fetch(line)
                data[off] = value
                self._insert(line, data)
        # the write-through step: the store gets the word now
        self._store_line(line)[off] = value
        self.stats.store_writes += 1
        self.stats.words_written += 1

    def consistent(self):
        """True when every cached line equals the store line (always, for write-through)."""
        return all(self.store.get(x) == d for x, d in self.lines.items())


def run(trace, k, block=1, write_allocate=False, store=None):
    """Run a trace of ("R", addr) and ("W", addr, value) requests. Return the cache."""
    c = WriteThroughCache(k, block, write_allocate, store)
    for req in trace:
        if req[0] == "R":
            c.read(req[1])
        else:
            c.write(req[1], req[2])
    return c
