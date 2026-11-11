# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transaction-validation/. The authors are listed in prov/HDPVHM.jsonl.

"""Four read validation policies in one small word-based STM, on the simulated
memory of stmsim.

Shared words: the data words, one versioned lock ("lock", a) per word holding
(version, owner) with owner None when free, a global version clock "gv" and a
global commit counter "cc". Writes go to a redo log and the write locks are
taken at commit (commit-time locking).

mode = "incremental"  after each read, check every earlier entry of the read
                      set; at commit, check all r entries (r(r+1)/2 checks)
mode = "counter"      after each read, read the global commit counter; scan the
                      whole read set (the new entry too) only when the counter
                      has moved since the last scan (the commit counter
                      heuristic of Spear et al., 2006). Writers increment the
                      counter while they hold their locks, before write-back.
mode = "clock"        TL2 style: each read checks its version against the
                      start time rv, and the commit checks the r entries once
mode = "commit"       no check after a read; check the r entries at commit
                      only. Serializable, but not opaque: a transaction can
                      run on an inconsistent state (a zombie).

check_new=False makes the broken counter variant of the tests: when the
counter has moved, it scans only the earlier entries, not the new one.

self.checks counts the read-set entries examined by validation scans (one
shared read each). The per-read test of the clock mode is part of the read
and is not counted.
"""

from __future__ import annotations

from typing import Any

from stmsim import Abort, Proc, Tx, nothing

MODES = ("incremental", "counter", "clock", "commit")


class ValidatingSTM:
    def __init__(self, mode: str = "incremental", check_new: bool = True) -> None:
        if mode not in MODES:
            raise ValueError(mode)
        self.mode = mode
        self.check_new = check_new
        self.checks = 0
        self.scans = 0

    def memory(self, data: dict) -> dict:
        w = dict(data)
        w["gv"] = 0
        w["cc"] = 0
        for a in data:
            w[("lock", a)] = (0, None)
        return w

    def begin(self, tx: Tx) -> Proc:
        tx.rset = []
        tx.wset = {}
        tx.held = {}
        if self.mode == "clock":
            tx.rv = yield ("read", "gv")
        elif self.mode == "counter":
            tx.last = yield ("read", "cc")

    def _ok(self, tx: Tx, lock: tuple, ver: int) -> bool:
        if lock[1] is not None and lock[1] != tx.tid:
            return False
        if self.mode == "clock":
            return lock[0] <= tx.rv
        return lock[0] == ver

    def validate(self, tx: Tx, entries: list) -> Proc:
        self.scans += 1
        for b, ver in entries:  # @line L8
            self.checks += 1
            lock = yield ("read", ("lock", b))
            if not self._ok(tx, lock, ver):
                raise Abort

    def read(self, tx: Tx, a: Any) -> Proc:
        if a in tx.wset:  # @line L1
            return tx.wset[a]
        l1 = yield ("read", ("lock", a))  # @line L2
        v = yield ("read", a)
        l2 = yield ("read", ("lock", a))
        if l1[1] is not None or l1 != l2:  # @line L3
            raise Abort
        if self.mode == "clock" and l1[0] > tx.rv:  # @line L4
            raise Abort
        earlier = list(tx.rset)
        tx.rset.append((a, l1[0]))  # @line L5
        if self.mode == "incremental":  # @line L6
            yield from self.validate(tx, earlier)
        elif self.mode == "counter":  # @line L7
            c = yield ("read", "cc")
            if c != tx.last:
                yield from self.validate(tx, tx.rset if self.check_new else earlier)
                tx.last = c
        return v

    def write(self, tx: Tx, a: Any, v: Any) -> Proc:
        tx.wset[a] = v
        yield from nothing()

    def commit(self, tx: Tx) -> Proc:
        if not tx.wset:
            if self.mode == "commit":
                yield from self.validate(tx, tx.rset)
            return
        for a in tx.wset:  # @line L9
            lock = yield ("read", ("lock", a))
            if lock[1] is not None or not (yield ("cas", ("lock", a), lock, (lock[0], tx.tid))):
                raise Abort
            tx.held[a] = lock[0]
        if self.mode == "clock":  # @line L10
            wv = (yield ("faa", "gv", 1)) + 1
        else:
            if self.mode == "counter":
                yield ("faa", "cc", 1)
            wv = None
        yield from self.validate(tx, tx.rset)  # @line L11
        for a, v in tx.wset.items():  # @line L12
            yield ("write", a, v)
        for a, old in tx.held.items():
            yield ("write", ("lock", a), (wv if wv is not None else old + 1, None))
        tx.held = {}

    def rollback(self, tx: Tx) -> Proc:
        for a, old in tx.held.items():
            yield ("write", ("lock", a), (old, None))
        tx.held = {}
        tx.wset = {}
