# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/norec/. The authors are listed in prov/4NBAVM.jsonl.

"""NOrec (Dalessandro, Spear and Scott, PPoPP 2010) on the simulated word memory of stmsim.

The only metadata is one global sequence lock "seqlock". It is even when no
writer is in its write-back, and odd while one writer writes back. A
transaction keeps a snapshot of the sequence lock, a read log of
(address, value) pairs and a redo log. Validation is value based: it checks
that each logged address still holds the logged value, at a moment when the
sequence lock is even and does not change. A writer commits by a CAS of the
sequence lock from its snapshot to snapshot + 1, writes back, and stores
snapshot + 2. So commits are serialized, and there are no ownership records.

Cost: a read takes 2 shared steps when no writer committed since the
snapshot; each validation takes r + 2 steps for r logged reads.
"""

from __future__ import annotations

from typing import Any

from stmsim import Abort, Proc, Tx, nothing


class NOrec:
    """check_reads=False drops the check of the sequence lock after each read
    (L4 to L6). That broken variant validates only at commit, so it is not opaque."""

    def __init__(self, check_reads: bool = True) -> None:
        self.check_reads = check_reads
        self.validations = 0

    def memory(self, data: dict) -> dict:
        w = dict(data)
        w["seqlock"] = 0
        return w

    def begin(self, tx: Tx) -> Proc:
        tx.snapshot = yield ("await", "seqlock", "even", None)  # @line L1
        tx.reads = []
        tx.writes = {}

    def read(self, tx: Tx, a: Any) -> Proc:
        if a in tx.writes:  # @line L2
            return tx.writes[a]
        v = yield ("read", a)  # @line L3
        while self.check_reads and tx.snapshot != (yield ("read", "seqlock")):  # @line L4
            tx.snapshot = yield from self.validate(tx)  # @line L5
            v = yield ("read", a)  # @line L6
        tx.reads.append((a, v))  # @line L7
        return v

    def write(self, tx: Tx, a: Any, v: Any) -> Proc:
        tx.writes[a] = v  # @line L8
        yield from nothing()

    def validate(self, tx: Tx) -> Proc:
        self.validations += 1
        while True:  # @line L9
            t = yield ("await", "seqlock", "even", None)  # @line L10
            for a, v in tx.reads:  # @line L11
                if (yield ("read", a)) != v:
                    raise Abort
            if (yield ("read", "seqlock")) == t:  # @line L12
                return t

    def commit(self, tx: Tx) -> Proc:
        if not tx.writes:  # @line L13
            return
        while not (yield ("cas", "seqlock", tx.snapshot, tx.snapshot + 1)):  # @line L14
            tx.snapshot = yield from self.validate(tx)
        for a, v in tx.writes.items():  # @line L15
            yield ("write", a, v)
        yield ("write", "seqlock", tx.snapshot + 2)  # @line L16

    def rollback(self, tx: Tx) -> Proc:
        tx.writes = {}
        yield from nothing()
