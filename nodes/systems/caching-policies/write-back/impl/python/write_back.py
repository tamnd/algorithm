# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-back/. The authors are listed in prov/67S2DT.jsonl.

"""A write-back cache with a dirty bit per line, in front of a slower store.

The cache holds at most k lines of `block` words each and replaces lines in LRU
order. A write hit changes only the cached line and sets its dirty bit. A dirty
line goes to the store, as one write of the whole line, when it is evicted or
flushed. On a write miss the cache fetches the line and keeps it
(write-allocate, the usual pair) or writes the word to the store only
(no-write-allocate).
"""

from collections import OrderedDict


class Stats:
    FIELDS = ("read_hits", "read_misses", "write_hits", "write_misses",
              "line_reads", "store_writes", "words_written")

    def __init__(self):
        for f in self.FIELDS:
            setattr(self, f, 0)

    def as_dict(self):
        return {f: getattr(self, f) for f in self.FIELDS}


class WriteBackCache:
    def __init__(self, k, block=1, write_allocate=True, store=None):
        if k < 1 or block < 1:
            raise ValueError("k and block must be positive")
        self.k = k
        self.block = block
        self.write_allocate = write_allocate
        self.store = store if store is not None else {}
        self.lines = OrderedDict()  # line -> list of words, least recent first
        self.dirty = set()
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

    def _write_line(self, line):
        """Copy a dirty line to the store and clear its dirty bit."""
        self.store[line] = list(self.lines[line])
        self.stats.store_writes += 1
        self.stats.words_written += self.block
        self.dirty.discard(line)

    def _insert(self, line, data):
        if len(self.lines) == self.k:
            victim = next(iter(self.lines))
            if victim in self.dirty:
                self._write_line(victim)
            del self.lines[victim]
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
            self.dirty.add(line)
        elif self.write_allocate:
            self.stats.write_misses += 1
            data = self._fetch(line)
            data[off] = value
            self._insert(line, data)
            self.dirty.add(line)
        else:
            self.stats.write_misses += 1
            self._store_line(line)[off] = value
            self.stats.store_writes += 1
            self.stats.words_written += 1

    def flush(self):
        """Write every dirty line to the store, in LRU order."""
        for line in [x for x in self.lines if x in self.dirty]:
            self._write_line(line)

    def clean_lines_agree(self):
        """The dirty-bit invariant: each clean cached line equals its store line."""
        return all(self.store.get(x) == d for x, d in self.lines.items() if x not in self.dirty)

    def crash(self):
        """Lose the cache. Return {line: words} for the updates that the store never got."""
        lost = {x: list(d) for x, d in self.lines.items()
                if x in self.dirty and self.store.get(x) != d}
        self.lines.clear()
        self.dirty.clear()
        return lost


def run(trace, k, block=1, write_allocate=True, store=None, flush=True):
    """Run a trace of ("R", addr) and ("W", addr, value) requests. Return the cache."""
    c = WriteBackCache(k, block, write_allocate, store)
    for req in trace:
        if req[0] == "R":
            c.read(req[1])
        else:
            c.write(req[1], req[2])
    if flush:
        c.flush()
    return c
