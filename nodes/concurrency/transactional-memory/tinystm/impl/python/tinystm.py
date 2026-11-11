# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tinystm/. The authors are listed in prov/PKTMQN.jsonl.

"""TinySTM (Felber, Fetzer and Riegel, PPoPP 2008) on the simulated word memory of stmsim.

Shared words: the data words, the global clock "clock", and one versioned
lock ("lock", s) per stripe s, holding (version, owner); owner is None when
the lock is free. Locks are taken at the first write (encounter-time
locking). Reads are invisible and keep (stripe, version) pairs. When a read
finds a version newer than the snapshot bound ub, the transaction tries to
extend its snapshot (the lazy snapshot algorithm of Riegel, Felber and
Fetzer 2006): it reads the clock, validates its read set, and moves ub.

Two update modes:
    write_back=True   writes go to a redo log and reach memory at commit
    write_back=False  write-through: writes go to memory at once, and an undo
                      log restores the old values on abort; the locks are then
                      released with a new version taken from the clock

Switches for the tests: extend=False aborts where the extension would help
(the TL2 rule); restore_version_on_abort=True is the bug of releasing the
locks of a write-through abort with their old versions.

The tuning parameters of the real TinySTM (the number of locks, the shift of
the address hash, hierarchical locking) are not modelled; stripe(a) only
chooses the lock of a word.
"""

from __future__ import annotations

from typing import Any, Callable

from stmsim import Abort, Proc, Tx, nothing


class TinySTM:
    def __init__(self, write_back: bool = True, extend: bool = True,
                 stripe: Callable[[Any], Any] | None = None, restore_version_on_abort: bool = False) -> None:
        self.write_back = write_back
        self.extend_on = extend
        self.stripe = stripe or (lambda a: a)
        self.restore_version_on_abort = restore_version_on_abort
        self.extensions = 0

    def memory(self, data: dict) -> dict:
        w = dict(data)
        w["clock"] = 0
        for a in data:
            w[("lock", self.stripe(a))] = (0, None)
        return w

    def begin(self, tx: Tx) -> Proc:
        tx.ub = yield ("read", "clock")  # @line L1
        tx.rset = {}
        tx.wset = {}
        tx.undo = []
        tx.held = {}

    def read(self, tx: Tx, a: Any) -> Proc:
        s = self.stripe(a)
        if s in tx.held:  # @line L2
            if self.write_back and a in tx.wset:
                return tx.wset[a]
            return (yield ("read", a))
        while True:
            l1 = yield ("read", ("lock", s))  # @line L3
            v = yield ("read", a)
            l2 = yield ("read", ("lock", s))
            if l1[1] is not None or l1 != l2:  # @line L4
                raise Abort
            if l1[0] > tx.ub:  # @line L5
                if not (yield from self.extend(tx)):  # @line L6
                    raise Abort
                continue  # @line L7
            tx.rset[s] = l1[0]  # @line L8
            return v

    def write(self, tx: Tx, a: Any, v: Any) -> Proc:
        s = self.stripe(a)
        if s not in tx.held:
            l = yield ("read", ("lock", s))  # @line L9
            if l[1] is not None:
                raise Abort
            if not (yield ("cas", ("lock", s), l, (l[0], tx.tid))):  # @line L10
                raise Abort
            tx.held[s] = l[0]
            if l[0] > tx.ub and not (yield from self.extend(tx)):
                raise Abort
        if self.write_back:  # @line L11
            tx.wset[a] = v
        else:
            old = yield ("read", a)
            tx.undo.append((a, old))
            yield ("write", a, v)
            tx.wset[a] = v

    def validate(self, tx: Tx) -> Proc:
        for s, ver in tx.rset.items():  # @line L13
            if s in tx.held:
                if tx.held[s] != ver:
                    return False
                continue
            l = yield ("read", ("lock", s))
            if l != (ver, None):
                return False
        return True

    def extend(self, tx: Tx) -> Proc:
        if not self.extend_on:
            return False
        now = yield ("read", "clock")  # @line L12
        if not (yield from self.validate(tx)):
            return False
        tx.ub = now  # @line L14
        self.extensions += 1
        return True

    def commit(self, tx: Tx) -> Proc:
        if not tx.held:  # @line L15
            return
        wv = (yield ("faa", "clock", 1)) + 1  # @line L16
        if tx.ub != wv - 1 and not (yield from self.validate(tx)):  # @line L17
            raise Abort
        if self.write_back:
            for a, v in tx.wset.items():  # @line L18
                yield ("write", a, v)
        for s in tx.held:  # @line L19
            yield ("write", ("lock", s), (wv, None))
        tx.held = {}

    def rollback(self, tx: Tx) -> Proc:
        for a, old in reversed(tx.undo):  # @line L20
            yield ("write", a, old)
        if self.write_back or self.restore_version_on_abort or not tx.held:
            versions = dict(tx.held)
        else:
            nv = (yield ("faa", "clock", 1)) + 1
            versions = {s: nv for s in tx.held}
        for s, ver in versions.items():
            yield ("write", ("lock", s), (ver, None))
        tx.held = {}
        tx.wset = {}
        tx.undo = []
        yield from nothing()
