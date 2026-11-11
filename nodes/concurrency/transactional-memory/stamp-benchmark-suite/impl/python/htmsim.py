# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stamp-benchmark-suite/. The authors are listed in prov/A9KZDJ.jsonl.
"""A small model of a best-effort hardware transactional memory.

Each processor can run one transaction at a time. Reads go into a read set
and writes into a write buffer; both are bounded, as a cache is. Conflicts
are found eagerly, as a coherence protocol finds them: a request for a line
aborts every other transaction that holds the line in a conflicting way
(the requester wins). Ordinary loads and stores count as requests too
(strong isolation). An aborted transaction learns about the abort at its
next instruction, which raises `Abort` with a status word; its effects are
gone at once, so it never acts on values from after the conflict.

The status word follows the layout of the RTM abort status of Intel TSX:
bit 0 explicit abort, bit 1 retry may succeed, bit 2 conflict, bit 3
capacity, bits 31:24 the code given to an explicit abort. An abort for
another reason (an interrupt here) sets none of these bits.

Precondition: every address is a key of the initial memory; a processor
does not start a transaction inside a transaction.
Cost: each instruction is O(n + r + w) in the model, for n processors and
read and write sets of sizes r and w.
"""

from __future__ import annotations

from typing import Hashable

EXPLICIT = 1 << 0
RETRY = 1 << 1
CONFLICT = 1 << 2
CAPACITY = 1 << 3


def explicit_code(status: int) -> int:
    """The 8-bit code of an explicit abort (valid only if EXPLICIT is set)."""
    return (status >> 24) & 0xFF


class Abort(Exception):
    """Raised in the aborted processor at its next instruction."""

    def __init__(self, status: int) -> None:
        super().__init__(status)
        self.status = status


class HTM:
    """n processors over a shared memory, with bounded transactional sets."""

    def __init__(self, n: int, memory: dict, read_cap: int = 8, write_cap: int = 4) -> None:
        self.mem = dict(memory)
        self.read_cap = read_cap
        self.write_cap = write_cap
        self.active = [False] * n
        self.doomed: list[int | None] = [None] * n
        self.rset: list[set] = [set() for _ in range(n)]
        self.wbuf: list[dict] = [{} for _ in range(n)]
        self.first_reads: list[dict] = [{} for _ in range(n)]
        self.history: list[tuple] = []     # committed transactions and plain accesses
        self.stats = {"commit": 0, "conflict": 0, "capacity": 0, "explicit": 0, "other": 0}

    # -- internal -------------------------------------------------------------
    def _kill(self, q: int, status: int) -> None:
        """Abort the transaction of q now; q sees it at its next instruction."""
        if self.active[q] and self.doomed[q] is None:
            self.doomed[q] = status
            self.rset[q].clear()
            self.wbuf[q].clear()
            self.first_reads[q].clear()
            if status & CONFLICT:
                self.stats["conflict"] += 1
            elif status & CAPACITY:
                self.stats["capacity"] += 1
            elif status & EXPLICIT:
                self.stats["explicit"] += 1
            else:
                self.stats["other"] += 1

    def _check(self, p: int) -> None:
        status = self.doomed[p]
        if status is not None:
            self.active[p] = False
            self.doomed[p] = None
            raise Abort(status)

    def _request(self, p: int, a: Hashable, exclusive: bool) -> None:
        """A coherence request by p for line a: abort conflicting holders."""
        for q in range(len(self.active)):
            if q == p or not self.active[q]:
                continue
            if a in self.wbuf[q] or (exclusive and a in self.rset[q]):
                self._kill(q, CONFLICT | RETRY)

    # -- instructions -----------------------------------------------------------
    def in_tx(self, p: int) -> bool:
        return self.active[p]

    def begin(self, p: int) -> None:
        """Start a transaction (XBEGIN)."""
        if self.active[p]:
            raise ValueError("nested transactions are not modelled")
        self.active[p] = True
        self.doomed[p] = None

    def load(self, p: int, a: Hashable) -> int:
        """Read a; inside a transaction, a joins the read set."""
        if not self.active[p]:
            self._request(p, a, exclusive=False)
            value = self.mem[a]
            self.history.append((p, {a: value}, {}))
            return value
        self._check(p)
        if a in self.wbuf[p]:
            return self.wbuf[p][a]
        self._request(p, a, exclusive=False)
        if a not in self.rset[p] and len(self.rset[p]) >= self.read_cap:
            self._kill(p, CAPACITY)
            self._check(p)
        self.rset[p].add(a)
        value = self.mem[a]
        self.first_reads[p].setdefault(a, value)
        return value

    def store(self, p: int, a: Hashable, v: int) -> None:
        """Write a; inside a transaction the value is buffered until commit."""
        if not self.active[p]:
            self._request(p, a, exclusive=True)
            self.mem[a] = v
            self.history.append((p, {}, {a: v}))
            return
        self._check(p)
        self._request(p, a, exclusive=True)
        if a not in self.wbuf[p] and len(self.wbuf[p]) >= self.write_cap:
            self._kill(p, CAPACITY)
            self._check(p)
        self.wbuf[p][a] = v

    def cas(self, p: int, a: Hashable, old: int, new: int) -> bool:
        """Ordinary compare-and-swap; it asks for the line exclusively."""
        if self.active[p]:
            raise ValueError("cas is modelled only outside transactions")
        self._request(p, a, exclusive=True)
        seen = self.mem[a]
        if seen != old:
            self.history.append((p, {a: seen}, {}))
            return False
        self.mem[a] = new
        self.history.append((p, {a: seen}, {a: new}))
        return True

    def commit(self, p: int) -> None:
        """End the transaction (XEND); its writes appear at once."""
        self._check(p)
        writes = dict(self.wbuf[p])
        self.mem.update(writes)
        self.history.append((p, dict(self.first_reads[p]), writes))
        self.active[p] = False
        self.rset[p].clear()
        self.wbuf[p].clear()
        self.first_reads[p].clear()
        self.stats["commit"] += 1

    def abort(self, p: int, code: int) -> None:
        """Explicit abort (XABORT code); raises in the caller."""
        self._check(p)
        self._kill(p, EXPLICIT | ((code & 0xFF) << 24))
        self._check(p)

    def interrupt(self, p: int) -> None:
        """An interrupt or a context switch aborts the transaction of p."""
        self._kill(p, 0)


def serial_replay_ok(initial: dict, history: list[tuple], final: dict) -> bool:
    """Run the recorded transactions one by one in commit order; check that
    each sees the values it read and that the end state is `final`."""
    mem = dict(initial)
    for _p, reads, writes in history:
        for a, v in reads.items():
            if mem[a] != v:
                return False
        mem.update(writes)
    return mem == final
