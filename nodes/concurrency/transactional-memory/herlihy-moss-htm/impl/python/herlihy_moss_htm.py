# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/herlihy-moss-htm/. The authors are listed in prov/JTKCNV.jsonl.
"""The transactional memory of Herlihy and Moss (ISCA 1993), as a machine model.

Each processor has a small transactional cache and two flags, TACTIVE and
TSTATUS. The instructions are LT, LTX, ST, COMMIT, ABORT and VALIDATE, and
the non-transactional LOAD and STORE. One call of a method is one atomic
step of the machine (one bus cycle or one local action).

What the model keeps from the paper:
  * a transaction starts implicitly at its first transactional instruction;
  * LT asks for a line in shared mode (T_READ), LTX and ST in exclusive mode
    (T_RFO); an active transaction that holds the line in a conflicting mode
    answers BUSY, and the requester aborts;
  * a tentative write stays in the transactional cache until COMMIT;
  * an overflow of the transactional cache, or an interrupt, aborts;
  * an aborted transaction (an orphan) makes no bus cycles, and its
    transactional instructions return arbitrary values;
  * VALIDATE returns TSTATUS and ends an aborted transaction.

What the model leaves out: the regular cache, the Goodman line states, and
the XCOMMIT entries (they only save write-backs). Committed values live in
`mem`. The paper leaves the mix of LOAD/STORE with transactions open; the
model uses the rule of its footnote 1: a LOAD or STORE acts as a transaction
that always commits and aborts the transactions it conflicts with.

Precondition: every address used is a key of the initial memory; a
processor does not use LOAD or STORE on lines in its own transaction.
Cost: each instruction is O(n + C) in the model, for n processors and a
cache of C entries (the hardware does the snoop and the commit in parallel).
"""

from __future__ import annotations

from typing import Callable, Hashable

SHARED = "S"
EXCLUSIVE = "X"


class Machine:
    """n processors with transactional caches of `capacity` entries each."""

    def __init__(self, n: int, memory: dict, capacity: int,
                 orphan_value: Callable[[int, Hashable], int] | None = None) -> None:
        self.mem = dict(memory)
        self.capacity = capacity
        self.tactive = [False] * n
        self.tstatus = [True] * n
        self.tcache: list[dict] = [{} for _ in range(n)]   # addr -> [mode, value]
        self.orphan_value = orphan_value or (lambda p, a: 0)
        # Instrumentation for tests, not part of the hardware.
        self.first_reads: list[dict] = [{} for _ in range(n)]
        self.history: list[tuple] = []                       # committed, in order
        self.abort_cause: list[str | None] = [None] * n

    # -- helpers ----------------------------------------------------------
    def _others_hold(self, p: int, a: Hashable, modes: str) -> bool:
        """True if an active transaction other than p holds a in a mode in modes."""
        for q, cache in enumerate(self.tcache):
            if q != p and self.tstatus[q] and a in cache and cache[a][0] in modes:
                return True
        return False

    def abort_self(self, p: int, cause: str) -> None:
        """The hardware aborts the transaction of p (BUSY, overflow, interrupt)."""
        if not self.tactive[p] or not self.tstatus[p]:
            return
        self.tcache[p].clear()  # @line L24
        self.tstatus[p] = False  # @line L24
        self.first_reads[p].clear()
        self.abort_cause[p] = cause

    def interrupt(self, p: int) -> None:
        """An interrupt or a context switch on processor p."""
        self.abort_self(p, "interrupt")

    def _end(self, p: int) -> None:
        self.tcache[p].clear()
        self.first_reads[p].clear()
        self.tstatus[p] = True
        self.tactive[p] = False

    # -- transactional instructions -------------------------------------
    def lt(self, p: int, a: Hashable) -> int:
        """Load-transactional: read a into the read set."""
        if not self.tstatus[p]:  # @line L1
            return self.orphan_value(p, a)  # @line L1
        self.tactive[p] = True  # @line L2
        cache = self.tcache[p]
        if a in cache:  # @line L3
            return cache[a][1]  # @line L3
        if self._others_hold(p, a, EXCLUSIVE):  # @line L4
            self.abort_self(p, "busy")  # @line L5
            return self.orphan_value(p, a)  # @line L5
        if len(cache) >= self.capacity:  # @line L6
            self.abort_self(p, "overflow")  # @line L6
            return self.orphan_value(p, a)  # @line L6
        value = self.mem[a]  # @line L7
        cache[a] = [SHARED, value]  # @line L7
        self.first_reads[p][a] = value
        return value  # @line L7

    def _exclusive(self, p: int, a: Hashable) -> list | None:
        """Shared part of LTX and ST: get a in exclusive mode, or abort."""
        if not self.tstatus[p]:  # @line L8
            return None  # @line L8
        self.tactive[p] = True  # @line L9
        cache = self.tcache[p]
        if a in cache and cache[a][0] == EXCLUSIVE:  # @line L10
            return cache[a]  # @line L10
        if self._others_hold(p, a, SHARED + EXCLUSIVE):  # @line L11
            self.abort_self(p, "busy")  # @line L12
            return None  # @line L12
        if a not in cache and len(cache) >= self.capacity:  # @line L13
            self.abort_self(p, "overflow")  # @line L13
            return None  # @line L13
        if a in cache:  # @line L14
            cache[a][0] = EXCLUSIVE  # @line L14
        else:
            cache[a] = [EXCLUSIVE, self.mem[a]]  # @line L14
        return cache[a]

    def ltx(self, p: int, a: Hashable) -> int:
        """Load-transactional-exclusive: read a into the write set."""
        first = a not in self.tcache[p]
        entry = self._exclusive(p, a)
        if entry is None:
            return self.orphan_value(p, a)  # @line L8
        if first:
            self.first_reads[p][a] = entry[1]
        return entry[1]  # @line L15

    def st(self, p: int, a: Hashable, v: int) -> None:
        """Store-transactional: tentatively write v to a."""
        entry = self._exclusive(p, a)
        if entry is not None:
            entry[1] = v  # @line L14

    def commit(self, p: int) -> bool:
        """Try to make the tentative writes permanent; return the status."""
        ok = self.tstatus[p]  # @line L16
        if ok:  # @line L17
            writes = {a: e[1] for a, e in self.tcache[p].items() if e[0] == EXCLUSIVE}
            self.mem.update(writes)  # @line L17
            self.history.append((p, dict(self.first_reads[p]), writes))
        self._end(p)  # @line L18
        return ok  # @line L19

    def abort(self, p: int) -> None:
        """Discard the tentative writes and end the transaction."""
        self._end(p)  # @line L20

    def validate(self, p: int) -> bool:
        """Return TSTATUS; if it is false, end the aborted transaction."""
        ok = self.tstatus[p]  # @line L21
        if not ok:  # @line L22
            self._end(p)  # @line L22
        return ok  # @line L23

    # -- non-transactional instructions (footnote 1 rule) ----------------
    def store(self, p: int, a: Hashable, v: int) -> None:
        """Ordinary store: aborts every transaction that holds a."""
        for q in range(len(self.tcache)):
            if q != p and a in self.tcache[q]:  # @line L25
                self.abort_self(q, "store")  # @line L25
        self.mem[a] = v  # @line L26
        self.history.append((p, {}, {a: v}))

    def load(self, p: int, a: Hashable) -> int:
        """Ordinary load: aborts every transaction that holds a exclusively."""
        for q in range(len(self.tcache)):
            if q != p and a in self.tcache[q] and self.tcache[q][a][0] == EXCLUSIVE:  # @line L27
                self.abort_self(q, "load")  # @line L27
        value = self.mem[a]  # @line L28
        self.history.append((p, {a: value}, {}))
        return value  # @line L28


def serial_replay_ok(initial: dict, history: list[tuple], final: dict) -> bool:
    """Check that running the committed transactions one by one, in commit
    order, gives each transaction the values it read and ends in `final`."""
    mem = dict(initial)
    for _p, reads, writes in history:
        for a, v in reads.items():
            if mem[a] != v:
                return False
        mem.update(writes)
    return mem == final
