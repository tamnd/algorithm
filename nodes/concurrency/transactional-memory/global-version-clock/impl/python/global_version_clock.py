# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/global-version-clock/. The authors are listed in prov/VVC9F1.jsonl.

"""A TL2-style STM with four ways to run the global version clock, on the
simulated word memory of stmsim.

Shared words: the data words, the clock "G", and one versioned lock
("lock", a) per word holding (version, owner), owner None when free.

clock = "gv1"  wv = FAA(G, 1) + 1 at each update commit (the DISC 2006 paper)
clock = "gv4"  one CAS(G, g, g + 1); if it fails, use the value that the
               winner installed (two writers may share a wv)
clock = "gv5"  no write to G at commit: wv = G + 1. A reader that meets a
               version newer than its rv aborts and first raises G to that
               version (one CAS), so that its retry can read the word
clock = "gv6"  gv4 for one commit in every n6 commits, gv5 for the others

The names GV4, GV5 and GV6 come from the release notes of the TL2 code.
A commit may skip the validation of its read set only when its wv was made
by its own increment, wv = rv + 1, and every commit moves the clock (gv1, or
gv4 when the CAS won). Under gv6 no commit skips: a gv5 commit between rv
and the CAS leaves no trace in the clock. unsafe_skip=True makes the broken
variant of the tests: skip whenever wv = rv + 1.

Counters: clock_writes (successful FAA or CAS on G at commit), cas_failures,
bumps (CAS on G by an aborting reader), skipped and validated.
"""

from __future__ import annotations

from typing import Any

from stmsim import Abort, Proc, Tx, nothing

CLOCKS = ("gv1", "gv4", "gv5", "gv6")


class ClockSTM:
    def __init__(self, clock: str = "gv1", n6: int = 4, unsafe_skip: bool = False) -> None:
        if clock not in CLOCKS:
            raise ValueError(clock)
        self.clock = clock
        self.n6 = n6
        self.unsafe_skip = unsafe_skip
        self.commits = 0
        self.clock_writes = 0
        self.cas_failures = 0
        self.bumps = 0
        self.skipped = 0
        self.validated = 0

    def memory(self, data: dict) -> dict:
        w = dict(data)
        w["G"] = 0
        for a in data:
            w[("lock", a)] = (0, None)
        return w

    def begin(self, tx: Tx) -> Proc:
        tx.rv = yield ("read", "G")  # @line L1
        tx.rset = []
        tx.wset = {}
        tx.held = {}

    def read(self, tx: Tx, a: Any) -> Proc:
        if a in tx.wset:
            return tx.wset[a]
        l1 = yield ("read", ("lock", a))  # @line L2
        v = yield ("read", a)
        l2 = yield ("read", ("lock", a))
        if l1[1] is not None or l1 != l2:
            raise Abort
        if l1[0] > tx.rv:  # @line L3
            if self.clock in ("gv5", "gv6"):  # @line L4
                g = yield ("read", "G")
                if g < l1[0] and (yield ("cas", "G", g, l1[0])):
                    self.bumps += 1
            raise Abort
        tx.rset.append(a)
        return v

    def write(self, tx: Tx, a: Any, v: Any) -> Proc:
        tx.wset[a] = v
        yield from nothing()

    def _mode(self) -> str:
        if self.clock != "gv6":
            return self.clock
        self.commits += 1
        return "gv4" if self.commits % self.n6 == 0 else "gv5"

    def commit(self, tx: Tx) -> Proc:
        if not tx.wset:
            return
        for a in tx.wset:  # @line L5
            lock = yield ("read", ("lock", a))
            if lock[1] is not None or not (yield ("cas", ("lock", a), lock, (lock[0], tx.tid))):
                raise Abort
            tx.held[a] = lock[0]
        mode = self._mode()
        own = False
        if mode == "gv1":  # @line L6
            tx.wv = (yield ("faa", "G", 1)) + 1
            self.clock_writes += 1
            own = True
        elif mode == "gv4":  # @line L7
            g = yield ("read", "G")
            if (yield ("cas", "G", g, g + 1)):
                tx.wv = g + 1
                self.clock_writes += 1
                own = self.clock == "gv4"  # under gv6, a gv5 commit may hide behind rv + 1
            else:
                self.cas_failures += 1
                tx.wv = yield ("read", "G")  # the value some winner installed
        else:  # @line L8
            tx.wv = (yield ("read", "G")) + 1
        if tx.wv == tx.rv + 1 and (own or self.unsafe_skip):  # @line L9
            self.skipped += 1
        else:
            self.validated += 1
            for a in tx.rset:  # @line L10
                if a in tx.held:
                    if tx.held[a] > tx.rv:
                        raise Abort
                    continue
                lock = yield ("read", ("lock", a))
                if lock[1] is not None or lock[0] > tx.rv:
                    raise Abort
        for a, v in tx.wset.items():  # @line L11
            yield ("write", a, v)
        for a in tx.held:
            yield ("write", ("lock", a), (tx.wv, None))
        tx.held = {}

    def rollback(self, tx: Tx) -> Proc:
        for a, ver in tx.held.items():
            yield ("write", ("lock", a), (ver, None))
        tx.held = {}
        tx.wset = {}
