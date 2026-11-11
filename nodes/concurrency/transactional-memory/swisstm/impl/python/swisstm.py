# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swisstm/. The authors are listed in prov/DS6V72.jsonl.

"""SwissTM (Dragojevic, Guerraoui and Kapalka, PLDI 2009) on the simulated word memory of stmsim.

Each word a has two lock words:
    ("wlock", a)  the owner tid of a pending write, or None. Taken at the first
                  write (eager write-write conflict detection).
    ("rlock", a)  the version of a (an int), or LOCKED while the owner writes
                  back at commit. Readers look only at this word, so a reader
                  and a writer of the same word do not conflict until the
                  writer commits (lazy read-write conflict detection).
Other shared words: the commit clock "clock", the greedy counter "greedy",
and per process p a status word ("status", p) = (serial, state, cm_ts), where
state is "active", "committing" or "aborted" and cm_ts is the greedy
timestamp of the attempt, or INF while it is timid.

The contention manager has two phases. A transaction is timid until it has
done `greedy_after` writes: on a write-write conflict with an active owner it
aborts itself. Then it takes a timestamp from the greedy counter and stores it
in its status word with a CAS. A greedy transaction that meets an active
owner with a larger timestamp (a younger owner, or a timid one) aborts the
owner with a CAS on its status word and waits until the owner releases the
lock; meeting an older owner, it aborts itself. The kill CAS expects the exact
status word that the CM read, so it fails if the owner became greedy in the
meantime, and the CM then looks again.

Simplifications: one lock pair per word (no hashing into a lock table), no
back-off after an abort, and a waiter for a committing owner simply waits.
"""

from __future__ import annotations

from typing import Any

from stmsim import INF, Abort, Proc, Tx, nothing

LOCKED = "LOCKED"


class SwissTM:
    def __init__(self, nprocs: int = 3, greedy_after: int = 10) -> None:
        self.nprocs = nprocs
        self.greedy_after = greedy_after
        self.extensions = 0
        self.kills = 0

    def memory(self, data: dict) -> dict:
        w = dict(data)
        w["clock"] = 0
        w["greedy"] = 0
        for a in data:
            w[("wlock", a)] = None
            w[("rlock", a)] = 0
        for p in range(self.nprocs):
            w[("status", p)] = (-1, "idle", INF)
        return w

    def begin(self, tx: Tx) -> Proc:
        p, serial = tx.tid
        tx.cm_ts = INF
        yield ("write", ("status", p), (serial, "active", INF))  # @line L1
        tx.valid_ts = yield ("read", "clock")
        tx.rset = {}
        tx.wset = {}
        tx.saved = {}

    def alive(self, tx: Tx) -> Proc:
        st = yield ("read", ("status", tx.tid[0]))
        if st[1] != "active":
            raise Abort

    def read(self, tx: Tx, a: Any) -> Proc:
        yield from self.alive(tx)  # @line L2
        if a in tx.wset:  # @line L3
            return tx.wset[a]
        while True:
            v1 = yield ("await", ("rlock", a), "ne", LOCKED)  # @line L4
            v = yield ("read", a)
            v2 = yield ("read", ("rlock", a))
            if v1 == v2:  # @line L5
                break
        tx.rset[a] = v1  # @line L6
        if v1 > tx.valid_ts and not (yield from self.extend(tx)):  # @line L7
            raise Abort
        return v  # @line L8

    def write(self, tx: Tx, a: Any, v: Any) -> Proc:
        p, serial = tx.tid
        yield from self.alive(tx)  # @line L9
        if a in tx.wset:  # @line L10
            tx.wset[a] = v
            return
        while True:
            o = yield ("read", ("wlock", a))  # @line L11
            if o is None:
                if (yield ("cas", ("wlock", a), None, tx.tid)):
                    break
                continue
            st = yield ("read", ("status", o[0]))  # @line L12
            if st[0] != o[1]:
                continue  # the owner attempt is over; the lock is free again
            if st[1] == "active":
                if tx.cm_ts >= st[2]:
                    raise Abort  # timid, or younger than the owner: abort self
                if not (yield ("cas", ("status", o[0]), st, (st[0], "aborted", st[2]))):
                    continue  # the owner changed its status: look again
                self.kills += 1
            yield ("await", ("wlock", a), "ne", o)
        tx.wset[a] = v  # @line L13
        if len(tx.wset) == self.greedy_after:
            ts = (yield ("faa", "greedy", 1)) + 1
            if not (yield ("cas", ("status", p), (serial, "active", INF), (serial, "active", ts))):
                raise Abort  # killed before the switch
            tx.cm_ts = ts

    def validate(self, tx: Tx) -> Proc:
        for a, ver in tx.rset.items():
            if a in tx.saved:
                if tx.saved[a] != ver:
                    return False
                continue
            if (yield ("read", ("rlock", a))) != ver:
                return False
        return True

    def extend(self, tx: Tx) -> Proc:
        now = yield ("read", "clock")  # @line L14
        if not (yield from self.validate(tx)):
            return False
        tx.valid_ts = now
        self.extensions += 1
        return True

    def commit(self, tx: Tx) -> Proc:
        if not tx.wset:  # @line L15
            return
        p, serial = tx.tid
        if not (yield ("cas", ("status", p), (serial, "active", tx.cm_ts), (serial, "committing", tx.cm_ts))):  # @line L16
            raise Abort
        for a in tx.wset:  # @line L17
            tx.saved[a] = yield ("read", ("rlock", a))
            yield ("write", ("rlock", a), LOCKED)
        ts = (yield ("faa", "clock", 1)) + 1  # @line L18
        if ts > tx.valid_ts + 1 and not (yield from self.validate(tx)):  # @line L19
            raise Abort
        for a, v in tx.wset.items():  # @line L20
            yield ("write", a, v)
        for a in tx.wset:  # @line L21
            yield ("write", ("rlock", a), ts)
            yield ("write", ("wlock", a), None)
        tx.saved = {}
        tx.wset = {}

    def rollback(self, tx: Tx) -> Proc:
        for a, ver in tx.saved.items():  # @line L22
            yield ("write", ("rlock", a), ver)
        for a in tx.wset:
            yield ("write", ("wlock", a), None)
        yield ("write", ("status", tx.tid[0]), (tx.tid[1], "aborted", tx.cm_ts))
        tx.saved = {}
        tx.wset = {}
        yield from nothing()
