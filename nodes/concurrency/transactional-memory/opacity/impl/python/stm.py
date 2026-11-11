# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/opacity/. The authors are listed in prov/7CW7RJ.jsonl.
"""Small word-based STM models for the scheduler in sched.py.

Memory is a list of words. Words are grouped in blocks of `block` words;
each block has a version number and an owner (a lock). There is a global
version clock and a global sequence lock for NOrec.

Three STMs are given:
- TL2: lazy versioning (a redo log), commit-time locking, a global version
  clock, and a version check at each read. With validate_reads=False the
  reads are not checked; the commit still validates, so committed
  transactions are serializable, but a live transaction can see an
  inconsistent state (a zombie).
- EagerSTM: eager versioning (in-place writes with an undo log) and
  encounter-time locking.
- NOrec: one global sequence lock and value-based validation.

Accesses outside transactions use nt_read and nt_write. With strong=True,
each of them runs as a transaction of one access (it waits for the lock of
the block and a write gives the block a new version); with strong=False,
they touch the word directly (weak atomicity).

Each method that touches shared memory is a generator: use `yield from`.
Begin is one atomic step that announces the transaction and reads the clock.
A TL2 read checks the lock and version of the block and reads the word in one
step. An aborted transaction that saw a lock held by another process backs
off until some lock changes hands; this keeps the tree of schedules finite.
Precondition: addresses are in range(size). Cost: each read and write is
O(1) steps; a TL2 commit is O(w + r) steps for w written blocks and r read
blocks.
"""

from __future__ import annotations

from typing import Any, Callable, Generator

Gen = Generator[Any, None, Any]


class Abort(Exception):
    """Raised inside a transaction to abort it."""


class History:
    """Events of transactions: (kind, tid, addr, value).

    The kinds are B (begin), R (read), W (write), T (commit requested),
    C (committed) and A (aborted).
    """

    def __init__(self) -> None:
        self.events: list[tuple] = []

    def add(self, kind: str, tid: tuple, addr: int = -1, val: Any = None) -> None:
        self.events.append((kind, tid, addr, val))


class Memory:
    """Shared words with block versions, block owners, a clock and a seqlock."""

    def __init__(self, size: int, init: dict[int, int] | None = None, block: int = 1) -> None:
        self.val = [0] * size
        for a, v in (init or {}).items():
            self.val[a] = v
        self.block = block
        nb = (size + block - 1) // block
        self.ver = [0] * nb
        self.owner: list[Any] = [None] * nb
        self.clock = 0
        self.seq = 0
        self.serial: dict[int, int] = {}

    def blk(self, a: int) -> int:
        return a // self.block

    def words(self, b: int) -> range:
        return range(b * self.block, min((b + 1) * self.block, len(self.val)))


class Tx:
    """The private state of one transaction attempt."""

    def __init__(self, stm: "STM", pid: int, attempt: int) -> None:
        self.stm = stm
        self.pid = pid
        self.tid = (pid, attempt)
        self.rv = 0
        self.snap = 0
        self.rset: dict[int, int] = {}
        self.rlog: list[tuple[int, int]] = []
        self.wbuf: dict[int, int] = {}
        self.wblocks: set[int] = set()
        self.undo: list[tuple[int, int]] = []
        self.locked: list[int] = []

    def read(self, a: int) -> Gen:
        return (yield from self.stm.read(self, a))

    def write(self, a: int, v: int) -> Gen:
        return (yield from self.stm.write(self, a, v))


class STM:
    """Common driver: run a body as a transaction and retry it on abort."""

    def __init__(self, mem: Memory, hist: History | None = None, strong: bool = False) -> None:
        self.mem = mem
        self.hist = hist if hist is not None else History()
        self.strong = strong

    def atomic(self, pid: int, body: Callable[[Tx], Gen], max_attempts: int = 1_000) -> Gen:
        """Run body(tx) as a transaction until it commits; return its value."""
        for attempt in range(1, max_attempts + 1):
            tx = Tx(self, pid, attempt)
            yield from self.begin(tx)
            try:
                r = yield from body(tx)
                self.hist.add("T", tx.tid)
                yield from self.commit(tx)
            except Abort:
                yield
                yield from self.rollback(tx)
                self.hist.add("A", tx.tid)
                self.mem.serial[pid] += 1
                held = tuple(self.mem.owner)
                if any(o is not None and o != pid for o in held):
                    # back off: retry only after some lock changes hands
                    yield lambda: tuple(self.mem.owner) != held
                continue
            self.hist.add("C", tx.tid)
            self.mem.serial[pid] += 1
            return r
        raise RuntimeError("too many attempts")

    def begin(self, tx: Tx) -> Gen:
        m = self.mem
        m.serial[tx.pid] = m.serial.get(tx.pid, 0) + 1
        tx.rv = m.clock
        self.hist.add("B", tx.tid)
        yield

    def rollback(self, tx: Tx) -> Gen:
        for b in tx.locked:
            self.mem.owner[b] = None
            yield
        tx.locked = []

    # accesses outside transactions

    def nt_read(self, a: int) -> Gen:
        m = self.mem
        b = m.blk(a)
        if self.strong:
            yield lambda: m.owner[b] is None
        v = m.val[a]
        yield
        return v

    def nt_write(self, a: int, v: int) -> Gen:
        m = self.mem
        b = m.blk(a)
        if self.strong:
            yield lambda: m.owner[b] is None
            m.clock += 1
            m.ver[b] = m.clock
        m.val[a] = v
        yield

    def fence(self, pid: int) -> Gen:
        """Quiescence fence: wait until each transaction that is active now has ended."""
        m = self.mem
        for p in sorted(m.serial):
            if p == pid:
                continue
            s = m.serial[p]
            yield
            if s % 2 == 1:
                yield (lambda p=p, s=s: m.serial[p] != s)

    def read(self, tx: Tx, a: int) -> Gen:
        raise NotImplementedError

    def write(self, tx: Tx, a: int, v: int) -> Gen:
        raise NotImplementedError

    def commit(self, tx: Tx) -> Gen:
        raise NotImplementedError


class TL2(STM):
    """TL2-like STM: redo log, commit-time locks, global version clock."""

    def __init__(self, mem: Memory, hist: History | None = None, strong: bool = False,
                 validate_reads: bool = True) -> None:
        super().__init__(mem, hist, strong)
        self.validate_reads = validate_reads

    def _check(self, tx: Tx, b: int) -> None:
        m = self.mem
        if self.validate_reads and (m.owner[b] is not None or m.ver[b] > tx.rv):
            raise Abort

    def read(self, tx: Tx, a: int) -> Gen:
        if a in tx.wbuf:
            return tx.wbuf[a]
        m = self.mem
        b = m.blk(a)
        self._check(tx, b)
        v = m.val[a]
        tx.rset.setdefault(b, m.ver[b])
        self.hist.add("R", tx.tid, a, v)
        yield
        return v

    def write(self, tx: Tx, a: int, v: int) -> Gen:
        m = self.mem
        b = m.blk(a)
        if m.block > 1 and b not in tx.wblocks:
            self._check(tx, b)
            for w in m.words(b):
                tx.wbuf.setdefault(w, m.val[w])
            tx.rset.setdefault(b, m.ver[b])
            yield
        tx.wblocks.add(b)
        tx.wbuf[a] = v
        self.hist.add("W", tx.tid, a, v)

    def commit(self, tx: Tx) -> Gen:
        m = self.mem
        if not tx.wbuf:
            if self.validate_reads:
                return
            for b, seen in tx.rset.items():
                if m.owner[b] is not None or m.ver[b] != seen:
                    raise Abort
                yield
            return
        blocks = sorted(tx.wblocks)
        for b in blocks:
            if m.owner[b] is not None:
                raise Abort
            m.owner[b] = tx.pid
            tx.locked.append(b)
            yield
        m.clock += 1
        wv = m.clock
        yield
        if wv != tx.rv + 1 or not self.validate_reads:
            for b, seen in tx.rset.items():
                o = m.owner[b]
                if o is not None and o != tx.pid:
                    raise Abort
                stale = m.ver[b] > tx.rv if self.validate_reads else m.ver[b] != seen
                if stale:
                    raise Abort
                yield
        for b in blocks:
            for w in m.words(b):
                if w in tx.wbuf:
                    m.val[w] = tx.wbuf[w]
            m.ver[b] = wv
            m.owner[b] = None
            tx.locked.remove(b)
            yield


class EagerSTM(STM):
    """Eager versioning: encounter-time locks, in-place writes, an undo log."""

    def read(self, tx: Tx, a: int) -> Gen:
        m = self.mem
        b = m.blk(a)
        o = m.owner[b]
        if o is not None and o != tx.pid:
            raise Abort
        if o != tx.pid and m.ver[b] > tx.rv:
            raise Abort
        v = m.val[a]
        tx.rset.setdefault(b, m.ver[b])
        self.hist.add("R", tx.tid, a, v)
        yield
        return v

    def write(self, tx: Tx, a: int, v: int) -> Gen:
        m = self.mem
        b = m.blk(a)
        if m.owner[b] != tx.pid:
            if m.owner[b] is not None or m.ver[b] > tx.rv:
                raise Abort
            m.owner[b] = tx.pid
            tx.locked.append(b)
            yield
        tx.undo.append((a, m.val[a]))
        m.val[a] = v
        tx.wbuf[a] = v
        self.hist.add("W", tx.tid, a, v)
        yield

    def commit(self, tx: Tx) -> Gen:
        m = self.mem
        if not tx.locked:
            return
        m.clock += 1
        wv = m.clock
        yield
        for b, seen in tx.rset.items():
            o = m.owner[b]
            if (o is not None and o != tx.pid) or m.ver[b] != seen:
                raise Abort
            yield
        for b in list(tx.locked):
            m.ver[b] = wv
            m.owner[b] = None
            tx.locked.remove(b)
            yield

    def rollback(self, tx: Tx) -> Gen:
        m = self.mem
        for a, old in reversed(tx.undo):
            m.val[a] = old
            yield
        tx.undo = []
        yield from super().rollback(tx)


class NOrec(STM):
    """NOrec: a global sequence lock, a redo log and value-based validation."""

    def begin(self, tx: Tx) -> Gen:
        m = self.mem
        yield lambda: m.seq % 2 == 0
        m.serial[tx.pid] = m.serial.get(tx.pid, 0) + 1
        tx.snap = m.seq
        self.hist.add("B", tx.tid)
        yield

    def _validate(self, tx: Tx) -> Gen:
        m = self.mem
        while True:
            yield lambda: m.seq % 2 == 0
            s = m.seq
            yield
            for a, v in tx.rlog:
                if m.val[a] != v:
                    raise Abort
                yield
            if m.seq == s:
                yield
                return s

    def read(self, tx: Tx, a: int) -> Gen:
        if a in tx.wbuf:
            return tx.wbuf[a]
        m = self.mem
        v = m.val[a]
        yield
        while True:
            s = m.seq
            yield
            if s == tx.snap:
                break
            tx.snap = yield from self._validate(tx)
            v = m.val[a]
            yield
        tx.rlog.append((a, v))
        self.hist.add("R", tx.tid, a, v)
        return v

    def write(self, tx: Tx, a: int, v: int) -> Gen:
        tx.wbuf[a] = v
        self.hist.add("W", tx.tid, a, v)
        if False:
            yield

    def commit(self, tx: Tx) -> Gen:
        m = self.mem
        if not tx.wbuf:
            return
        while m.seq != tx.snap:
            yield
            tx.snap = yield from self._validate(tx)
        m.seq = tx.snap + 1
        yield
        for a in sorted(tx.wbuf):
            m.val[a] = tx.wbuf[a]
            yield
        m.seq = tx.snap + 2
        yield
