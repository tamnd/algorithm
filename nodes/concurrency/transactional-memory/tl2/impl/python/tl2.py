# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tl2/. The authors are listed in prov/V7T1AZ.jsonl.

"""TL2 (Dice, Shalev and Shavit, DISC 2006) on the simulated word memory of stmsim.

Shared words: the data words, the global version clock "gv", and one
versioned write lock ("lock", s) per stripe s. A lock word holds
(version, owner); owner is None when the lock is free. stripe(a) maps an
address to its stripe (the identity by default; a coarser map gives lock
striping and false conflicts).

Each transaction keeps rv (the clock at begin), a read set and a redo log
(the write set). Reads are post-validated against rv. Commit locks the write
set, takes wv from the clock, validates the read set unless wv = rv + 1,
writes back and releases each lock with version wv.

Cost: a read takes 3 shared steps, a write 0, and a commit with w lock words
and r reads takes about 2w + 1 + r + |W| + w steps; no step waits.

Two switches make the broken variants of the tests: post_validate=False
reads a word with no check, and write_locks=False commits with no locks.
"""

from __future__ import annotations

from typing import Any, Callable

from stmsim import Abort, Proc, Tx, nothing


class TL2:
    def __init__(self, stripe: Callable[[Any], Any] | None = None, post_validate: bool = True,
                 write_locks: bool = True) -> None:
        self.stripe = stripe or (lambda a: a)
        self.post_validate = post_validate
        self.write_locks = write_locks
        self.skipped = 0
        self.validated = 0

    def memory(self, data: dict) -> dict:
        """The initial words for the data words in data."""
        w = dict(data)
        w["gv"] = 0
        for a in data:
            w[("lock", self.stripe(a))] = (0, None)
        return w

    def begin(self, tx: Tx) -> Proc:
        tx.rv = yield ("read", "gv")  # @line L1
        tx.rset = {}  # @line L2
        tx.wset = {}
        tx.held = {}

    def read(self, tx: Tx, a: Any) -> Proc:
        if a in tx.wset:  # @line L3
            return tx.wset[a]
        lock = ("lock", self.stripe(a))
        if not self.post_validate:
            v = yield ("read", a)
            tx.rset[a] = True
            return v
        l1 = yield ("read", lock)  # @line L4
        v = yield ("read", a)  # @line L5
        l2 = yield ("read", lock)  # @line L6
        if l1[1] is not None or l1 != l2 or l1[0] > tx.rv:  # @line L7
            raise Abort
        tx.rset[a] = True  # @line L8
        return v

    def write(self, tx: Tx, a: Any, v: Any) -> Proc:
        tx.wset[a] = v  # @line L9
        yield from nothing()

    def commit(self, tx: Tx) -> Proc:
        if not tx.wset:  # @line L10
            return
        if self.write_locks:
            for s in dict.fromkeys(self.stripe(a) for a in tx.wset):  # @line L11
                l = yield ("read", ("lock", s))
                if l[1] is not None:
                    raise Abort
                if not (yield ("cas", ("lock", s), l, (l[0], tx.tid))):
                    raise Abort
                tx.held[s] = l[0]
        tx.wv = (yield ("faa", "gv", 1)) + 1  # @line L12
        if tx.wv != tx.rv + 1:  # @line L13
            self.validated += 1
            for a in tx.rset:  # @line L14
                s = self.stripe(a)
                if s in tx.held:
                    if tx.held[s] > tx.rv:
                        raise Abort
                    continue
                l = yield ("read", ("lock", s))
                if l[1] is not None or l[0] > tx.rv:
                    raise Abort
        else:
            self.skipped += 1
        for a, v in tx.wset.items():  # @line L15
            yield ("write", a, v)
        stripes = tx.held if self.write_locks else dict.fromkeys(self.stripe(a) for a in tx.wset)
        for s in stripes:  # @line L16
            yield ("write", ("lock", s), (tx.wv, None))
        tx.held = {}  # @line L17

    def rollback(self, tx: Tx) -> Proc:
        for s, ver in tx.held.items():  # @line L18
            yield ("write", ("lock", s), (ver, None))
        tx.held = {}
        tx.wset = {}
