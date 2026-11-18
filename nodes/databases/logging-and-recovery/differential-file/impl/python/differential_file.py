# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-file/. The authors are listed in prov/PBST4C.jsonl.

"""A differential file in the style of Severance and Lohman (1976).

The main file M is read-only between reorganizations. Every insert, change
and delete goes to the differential file D, newest entry per key, with a
delete marker for a delete. A Bloom filter F over the keys in D lets a lookup
of an unchanged key go to M without a read of D. A reorganization merges D
into a new generation of M and dumps it to the archive.

The counters count the simulated file reads, so a test can compare the reads
with the false positive rate of the filter.
"""

import hashlib

DELETED = object()  # the delete marker in D


class DifferentialFile:
    def __init__(self, main: dict, m: int = 256, k: int = 3):
        self.main = dict(sorted(main.items()))  # read-only generation of the main file
        self.diff: dict = {}  # key -> value or DELETED
        self.m, self.k = m, k
        self.bits = 0  # the filter F as an integer of m bits
        self.archive = [dict(self.main)]  # dumps of each generation of M
        self.main_reads = self.diff_reads = self.false_positives = 0

    def _positions(self, key) -> list[int]:
        h = hashlib.blake2b(repr(key).encode(), digest_size=16).digest()
        h1, h2 = int.from_bytes(h[:8], "big"), int.from_bytes(h[8:], "big") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def maybe_changed(self, key) -> bool:
        return all(self.bits >> p & 1 for p in self._positions(key))

    def lookup(self, key):
        """The value of key, or None if the key is absent."""
        if self.maybe_changed(key):  # @line L1
            self.diff_reads += 1
            if key in self.diff:  # @line L2
                v = self.diff[key]  # @line L2
                return None if v is DELETED else v  # @line L2
            self.false_positives += 1
        self.main_reads += 1
        return self.main.get(key)  # @line L3

    def put(self, key, value) -> None:
        """Insert or change a record."""
        self.diff[key] = value  # @line L4
        for p in self._positions(key):
            self.bits |= 1 << p  # @line L5

    def delete(self, key) -> None:
        self.diff[key] = DELETED  # @line L4
        for p in self._positions(key):
            self.bits |= 1 << p  # @line L5

    def scan(self) -> list:
        """All records in key order: the merge of M and D."""
        out = dict(self.main)
        for key, v in self.diff.items():
            if v is DELETED:
                out.pop(key, None)
            else:
                out[key] = v
        return sorted(out.items())

    def reorganize(self) -> None:
        new_main = dict(self.scan())  # @line L6
        self.archive.append(dict(new_main))  # @line L7
        self.main = new_main  # @line L7
        self.diff, self.bits = {}, 0  # @line L8

    def restore_main(self) -> None:
        """Recover from the loss of M: copy the dump of the current generation."""
        self.main = dict(self.archive[-1])
