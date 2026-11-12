# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-around/. The authors are listed in prov/ECHMAV.jsonl.

"""A write-around cache: no-write-allocate, and every write goes to the store.

The cache holds at most k lines of `block` words each and replaces lines in LRU
order. Only a read miss brings a line into the cache. A write always goes to the
store. If the written line is in the cache, the cache either drops it
("invalidate") or updates it in place ("update"; this is write-through with
no-write-allocate).
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


class WriteAroundCache:
    def __init__(self, k, block=1, on_write_hit="invalidate", store=None):
        if k < 1 or block < 1:
            raise ValueError("k and block must be positive")
        if on_write_hit not in ("invalidate", "update"):
            raise ValueError("on_write_hit is 'invalidate' or 'update'")
        self.k = k
        self.block = block
        self.on_write_hit = on_write_hit
        self.store = store if store is not None else {}
        self.lines = OrderedDict()  # line -> list of words, least recent first
        self.stats = Stats()

    def _split(self, addr):
        return addr // self.block, addr % self.block

    def _store_line(self, line):
        if line not in self.store:
            self.store[line] = [0] * self.block
        return self.store[line]

    def read(self, addr):
        line, off = self._split(addr)
        if line in self.lines:
            self.stats.read_hits += 1
            self.lines.move_to_end(line)
        else:
            self.stats.read_misses += 1
            self.stats.line_reads += 1
            if len(self.lines) == self.k:
                self.lines.popitem(last=False)  # clean line: no store write
            self.lines[line] = list(self._store_line(line))
        return self.lines[line][off]

    def write(self, addr, value):
        line, off = self._split(addr)
        if line in self.lines:
            self.stats.write_hits += 1
            if self.on_write_hit == "invalidate":
                del self.lines[line]
            else:
                self.lines[line][off] = value
                self.lines.move_to_end(line)
        else:
            self.stats.write_misses += 1  # no-write-allocate: the cache does not change
        self._store_line(line)[off] = value
        self.stats.store_writes += 1
        self.stats.words_written += 1

    def consistent(self):
        """True when every cached line equals the store line."""
        return all(self.store.get(x) == d for x, d in self.lines.items())


def run(trace, k, block=1, on_write_hit="invalidate", store=None):
    """Run a trace of ("R", addr) and ("W", addr, value) requests. Return the cache."""
    c = WriteAroundCache(k, block, on_write_hit, store)
    for req in trace:
        if req[0] == "R":
            c.read(req[1])
        else:
            c.write(req[1], req[2])
    return c
