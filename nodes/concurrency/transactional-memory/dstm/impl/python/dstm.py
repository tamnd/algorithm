# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dstm/. The authors are listed in prov/4KD1YP.jsonl.

"""DSTM (Herlihy, Luchangco, Moir and Scherer, PODC 2003) on the simulated word memory of stmsim.

Each data word of stmsim is one transactional object (a TMObject). Its shared
word ("start", o) holds a locator, an immutable tuple

    (lid, owner, old, new)    with old and new versions (vid, value)

where owner is the tid of the transaction that installed the locator (None
for the initial locator). The current committed version of o is new if the
owner committed and old if it aborted or is still active. A real DSTM keeps
the new version as a private copy reachable from the locator; here the value
of the copy sits inside the locator, and a second write to an owned object
replaces the locator by one with the same lid and a new value.

Each transaction attempt (p, s) has a status word ("status", p, s), which
starts as ACTIVE. Commit is one CAS of the own status from ACTIVE to
COMMITTED; an enemy aborts the owner by a CAS from ACTIVE to ABORTED.

Reads are invisible: a transaction keeps a read table of (object, vid) and
validates the whole table at each open and at commit (O(r) steps per open).
release(tx, o) removes o from the read table (early release).

With strict=False, VALIDATE checks only that each read version is still the
current committed version. Then two transactions can each validate before the
other commits its status, and both commit: write skew (see the tests). With
strict=True (the default), VALIDATE also fails when another active
transaction has an object of the read table open for writing.

The contention manager decides what to do when an open finds an active
owner. "aggressive" aborts the owner at once. "polite" backs off for 2^k
local steps, up to `rounds` times, and then aborts the owner.
"""

from __future__ import annotations

from typing import Any

from stmsim import Abort, Proc, Tx, nothing

ACTIVE, COMMITTED, ABORTED = "ACTIVE", "COMMITTED", "ABORTED"


class DSTM:
    def __init__(self, nprocs: int = 3, cm: str = "polite", rounds: int = 3, max_attempts: int = 40,
                 validate_reads: bool = True, strict: bool = True) -> None:
        self.nprocs = nprocs
        self.cm = cm
        self.rounds = rounds
        self.max_attempts = max_attempts
        self.validate_reads = validate_reads
        self.strict = strict
        self.checks = 0  # read table entries checked by VALIDATE
        self.kills = 0

    def memory(self, data: dict) -> dict:
        w = {}
        for o, v in data.items():
            init = (("init", o), v)
            w[("start", o)] = (("init", o), None, init, init)
        for p in range(self.nprocs):
            for s in range(self.max_attempts):
                w[("status", p, s)] = ACTIVE
        return w

    def begin(self, tx: Tx) -> Proc:
        if tx.tid[1] >= self.max_attempts:
            raise RuntimeError("too many attempts for the preallocated status words")
        tx.rset = {}  # @line L1
        tx.owned = {}  # o -> the locator this transaction installed
        yield from nothing()

    def status(self, owner: tuple) -> Proc:
        return (yield ("read", ("status", owner[0], owner[1])))

    def current(self, tx: Tx, o: Any) -> Proc:
        """Return (locator, current committed version) of o, after the CM has
        dealt with an active owner."""
        k = 0
        while True:
            loc = yield ("read", ("start", o))  # @line L2
            owner = loc[1]
            if owner is None:
                return loc, loc[3]
            st = yield from self.status(owner)
            if st == ACTIVE:  # @line L3
                if self.cm == "polite" and k < self.rounds:
                    for _ in range(2 ** k):
                        yield ("local",)
                    k += 1
                    continue
                if (yield ("cas", ("status", owner[0], owner[1]), ACTIVE, ABORTED)):
                    self.kills += 1
                continue
            if st == COMMITTED:  # @line L4
                if (yield ("read", ("start", o))) != loc:  # read the data of the new version
                    continue
                return loc, loc[3]
            return loc, loc[2]

    def validate(self, tx: Tx) -> Proc:
        if (yield ("read", ("status",) + tx.tid)) != ACTIVE:  # @line L10
            return False
        for o, vid in tx.rset.items():  # @line L11
            self.checks += 1
            loc = yield ("read", ("start", o))
            st = COMMITTED if loc[1] is None else (yield from self.status(loc[1]))
            if st == ACTIVE and self.strict:
                return False  # another live transaction has o open for writing
            if (loc[3][0] if st == COMMITTED else loc[2][0]) != vid:
                return False
        return True

    def read(self, tx: Tx, a: Any) -> Proc:
        if a in tx.owned:
            return tx.owned[a][3][1]
        _, ver = yield from self.current(tx, a)
        tx.rset[a] = ver[0]  # @line L5
        if self.validate_reads and not (yield from self.validate(tx)):
            raise Abort
        return ver[1]

    def write(self, tx: Tx, a: Any, v: Any) -> Proc:
        if a in tx.owned:  # @line L6
            lid, me, old, _ = loc = tx.owned[a]
            new = (lid, me, old, (lid, v))
            if not (yield ("cas", ("start", a), loc, new)):
                raise Abort
            tx.owned[a] = new
            return
        lid = tx.tid + (a,)
        while True:
            loc, cur = yield from self.current(tx, a)
            new = (lid, tx.tid, cur, (lid, v))  # @line L7
            if (yield ("cas", ("start", a), loc, new)):  # @line L8
                break
        tx.owned[a] = new
        if a in tx.rset and tx.rset.pop(a) != cur[0]:  # @line L9
            raise Abort
        if not (yield from self.validate(tx)):
            raise Abort

    def release(self, tx: Tx, a: Any) -> Proc:
        tx.rset.pop(a, None)  # @line L15
        yield from nothing()

    def commit(self, tx: Tx) -> Proc:
        if not (yield from self.validate(tx)):  # @line L12
            raise Abort
        if not (yield ("cas", ("status",) + tx.tid, ACTIVE, COMMITTED)):  # @line L13
            raise Abort

    def rollback(self, tx: Tx) -> Proc:
        yield ("write", ("status",) + tx.tid, ABORTED)  # @line L14
