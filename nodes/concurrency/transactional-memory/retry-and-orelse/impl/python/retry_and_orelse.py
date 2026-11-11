# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/retry-and-orelse/. The authors are listed in prov/E1CEZX.jsonl.
"""retry and orElse (Harris, Marlow, Peyton Jones and Herlihy, 2005) on a TL2 model.

`retry` aborts the current transaction and blocks the process until some
block in the read set of the transaction has a new version; then the
transaction runs again from the start. `or_else(tx, first, second)` runs
`first`; if it calls retry, its writes are discarded (its reads stay in the
read set) and `second` runs in the same transaction. If `second` also calls
retry, the whole transaction retries and waits on the union of the reads of
both branches.

TL2 takes no locks before commit, so a retry needs no rollback of memory;
the redo log is simply dropped.

Precondition: bodies are generators that use tx.read and tx.write.
Cost: a retry adds one step plus the wait; or_else copies the redo log,
O(w) for w buffered writes.
"""

from __future__ import annotations

from typing import Any, Callable

from stm import TL2, Abort, Gen, Tx


class Retry(Exception):
    """Raised by `retry` inside a transaction."""


def retry() -> None:
    """Abort the transaction and wait until something it read changes."""
    raise Retry


def or_else(tx: Tx, first: Callable[[Tx], Gen], second: Callable[[Tx], Gen]) -> Gen:
    """Run first; if it retries, undo its writes and run second."""
    saved_wbuf = dict(tx.wbuf)
    saved_wblocks = set(tx.wblocks)
    try:
        return (yield from first(tx))
    except Retry:
        tx.wbuf = saved_wbuf
        tx.wblocks = saved_wblocks
        return (yield from second(tx))


class BlockingTL2(TL2):
    """TL2 whose atomic blocks support retry.

    `log` records ("begin", tid, versions) at the start of each attempt and
    ("retry", tid, versions) when an attempt retries, so tests can check
    when a blocked transaction woke up. At a retry, the version of a block
    in the read set is the version that the attempt read.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.log: list[tuple] = []

    def begin(self, tx: Tx) -> Gen:
        self.log.append(("begin", tx.tid, tuple(self.mem.ver)))
        yield from super().begin(tx)

    def atomic(self, pid: int, body: Callable[[Tx], Gen], max_attempts: int = 1_000) -> Gen:
        m = self.mem
        for attempt in range(1, max_attempts + 1):
            tx = Tx(self, pid, attempt)
            yield from self.begin(tx)
            try:
                r = yield from body(tx)
                self.hist.add("T", tx.tid)
                yield from self.commit(tx)
            except Retry:
                self.hist.add("A", tx.tid)
                m.serial[pid] += 1
                watch = dict(tx.rset)
                seen = [watch.get(b, v) for b, v in enumerate(m.ver)]
                self.log.append(("retry", tx.tid, tuple(seen)))
                # block until a block that the attempt read has a new version
                yield lambda: any(m.ver[b] != v for b, v in watch.items())
                continue
            except Abort:
                yield
                yield from self.rollback(tx)
                self.hist.add("A", tx.tid)
                m.serial[pid] += 1
                held = tuple(m.owner)
                if any(o is not None and o != pid for o in held):
                    yield lambda: tuple(m.owner) != held
                continue
            self.hist.add("C", tx.tid)
            m.serial[pid] += 1
            return r
        raise RuntimeError("too many attempts")


def take(addr: int, tag: Any = None) -> Callable[[Tx], Gen]:
    """A body that takes one item from the counter at addr, or retries if it is 0."""

    def body(tx: Tx) -> Gen:
        v = yield from tx.read(addr)
        if v == 0:
            retry()
        yield from tx.write(addr, v - 1)
        return addr if tag is None else tag

    return body


def put(addr: int, cap: int) -> Callable[[Tx], Gen]:
    """A body that adds one item to the counter at addr, or retries if it holds cap."""

    def body(tx: Tx) -> Gen:
        v = yield from tx.read(addr)
        if v >= cap:
            retry()
        yield from tx.write(addr, v + 1)

    return body
