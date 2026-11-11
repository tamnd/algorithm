# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zombie-transactions/. The authors are listed in prov/M45GVF.jsonl.

"""Zombie transactions in a small word-based STM, and two ways to stop them,
on the simulated word memory of stmsim.

Shared words: the data words, a global version clock "G", and one versioned
lock ("lock", a) per word holding (version, owner), owner None when free.
Writes go to a redo log; the write locks are taken at commit, which then
takes wv = FAA(G, 1) + 1, validates the read set, writes back and releases
the locks with version wv. Every commit, read-only ones included, validates
its read set, so the committed transactions are always serializable.

mode = "commit"   reads are not checked until commit. A transaction can read
                  a state that never existed and keep running on it: a
                  zombie. It may loop forever or raise a fault before it
                  reaches the commit that would abort it.
mode = "opaque"   each read is checked against the start time rv (as in TL2),
                  so no transaction ever sees an inconsistent state.
mode = "sandbox"  reads are not checked, as in "commit", but the zombie is
                  contained: the program calls tick() at each loop back edge,
                  and every period ticks the STM validates the read set; and
                  the program runs code that may fault inside guard(), which
                  validates before it lets a fault escape. A fault on a valid
                  state is real and is raised; on an invalid one it is an abort.

A transaction body uses tx.stm.tick(tx) and tx.stm.guard(tx, f) with yield from.
Counters: ticks (loop iterations run), max_ticks (the most in one attempt),
validations, faults_hidden (faults turned into aborts) and faults_raised.
"""

from __future__ import annotations

from typing import Any, Callable

from stmsim import Abort, Proc, Tx, nothing

MODES = ("commit", "opaque", "sandbox")


class ZombieSTM:
    def __init__(self, mode: str = "commit", period: int = 4) -> None:
        if mode not in MODES:
            raise ValueError(mode)
        self.mode = mode
        self.period = period
        self.ticks = 0
        self.max_ticks = 0
        self.validations = 0
        self.faults_hidden = 0
        self.faults_raised = 0

    def memory(self, data: dict) -> dict:
        w = dict(data)
        w["G"] = 0
        for a in data:
            w[("lock", a)] = (0, None)
        return w

    def begin(self, tx: Tx) -> Proc:
        tx.rv = yield ("read", "G")
        tx.rset = {}
        tx.wset = {}
        tx.held = {}
        tx.ticks = 0

    def read(self, tx: Tx, a: Any) -> Proc:
        if a in tx.wset:
            return tx.wset[a]
        l1 = yield ("read", ("lock", a))
        v = yield ("read", a)
        l2 = yield ("read", ("lock", a))
        if l1[1] is not None or l1 != l2:
            raise Abort
        if self.mode == "opaque" and l1[0] > tx.rv:
            raise Abort
        tx.rset.setdefault(a, l1[0])
        return v

    def write(self, tx: Tx, a: Any, v: Any) -> Proc:
        tx.wset[a] = v
        yield from nothing()

    def validate(self, tx: Tx) -> Proc:
        self.validations += 1
        for a, ver in tx.rset.items():
            lock = yield ("read", ("lock", a))
            if lock[0] != ver or (lock[1] is not None and lock[1] != tx.tid):
                raise Abort

    def tick(self, tx: Tx) -> Proc:
        """Called by the program at each loop back edge."""
        self.ticks += 1
        tx.ticks += 1
        self.max_ticks = max(self.max_ticks, tx.ticks)
        if self.mode == "sandbox" and tx.ticks % self.period == 0:
            yield from self.validate(tx)
        else:
            yield ("local",)

    def guard(self, tx: Tx, f: Callable[[], Any]) -> Proc:
        """Run f, which may fault. In sandbox mode a fault is first checked."""
        try:
            v = f()
        except Exception:
            if self.mode != "sandbox":
                self.faults_raised += 1
                raise
            try:
                yield from self.validate(tx)
            except Abort:  # the state was inconsistent: the fault belongs to a zombie
                self.faults_hidden += 1
                raise
            self.faults_raised += 1
            raise
        yield ("local",)
        return v

    def commit(self, tx: Tx) -> Proc:
        if not tx.wset:
            yield from self.validate(tx)
            return
        for a in tx.wset:
            lock = yield ("read", ("lock", a))
            if lock[1] is not None or not (yield ("cas", ("lock", a), lock, (lock[0], tx.tid))):
                raise Abort
            tx.held[a] = lock[0]
        wv = (yield ("faa", "G", 1)) + 1
        yield from self.validate(tx)
        for a, v in tx.wset.items():
            yield ("write", a, v)
        for a in tx.held:
            yield ("write", ("lock", a), (wv, None))
        tx.held = {}

    def rollback(self, tx: Tx) -> Proc:
        for a, ver in tx.held.items():
            yield ("write", ("lock", a), (ver, None))
        tx.held = {}
        tx.wset = {}
