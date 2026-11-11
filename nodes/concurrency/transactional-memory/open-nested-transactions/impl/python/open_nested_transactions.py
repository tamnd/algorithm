# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/open-nested-transactions/. The authors are listed in prov/R3QGVQ.jsonl.
"""Open nesting with compensation and abstract locks on a TL2 model.

An open nested transaction runs inside a parent transaction but commits on
its own, at once: its writes become visible to every process, and they are
not in the read or write set of the parent. If the parent later aborts (or
is cancelled), each open child that committed is undone by a compensating
transaction, run as its own top-level transaction, in reverse order. To keep
other transactions from seeing or changing the abstract state that an open
child touched before the parent ends, the parent holds an abstract lock on
the key until it commits or finishes compensating.

The shared object is a set of small integer keys: word SIZE holds the number
of keys, and word k (k >= 1) is 1 if key k is in the set. The module gives
the set operations as transaction bodies and three compensations for an
insert: the correct one (remove the key if this insert added it), a physical
undo (restore the old words, which loses concurrent updates of SIZE), and an
unconditional remove (wrong when the insert found the key already there).

Precondition: keys are in range(1, size - 1); the last word is free for
closed work of the parent. Cost: each set operation is O(1) steps; a parent
that aborts runs one compensating transaction per committed open child.
"""

from __future__ import annotations

from typing import Any, Callable

from stm import TL2, Abort, Gen, Tx

SIZE = 0
Body = Callable[[Tx], Gen]


class Cancel(Exception):
    """Raised by a parent body to abort it for good (no retry)."""


class OpenNestingTL2(TL2):
    """TL2 with open nested children, compensation and abstract locks."""

    def __init__(self, *args: Any, use_locks: bool = True, coarse: bool = False,
                 **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.use_locks = use_locks
        self.coarse = coarse
        self.alocks: dict[Any, int] = {}

    def run_op(self, pid: int, body: Body) -> Gen:
        """Run body as a top-level transaction with no parent.

        With coarse=True the whole transaction is one step, as if the set
        were a linearizable object; this keeps the tree of schedules small.
        """
        if not self.coarse:
            return (yield from self.atomic(pid, body))
        gen = self.atomic(pid, body)
        try:
            while True:
                guard = next(gen)
                if guard is not None and not guard():
                    raise RuntimeError("a one-step transaction had to wait")
        except StopIteration as stop:
            value = stop.value
        yield
        return value

    def atomic_top(self, pid: int, body: Body, max_attempts: int = 1_000) -> Gen:
        """Run a top-level transaction whose body may open nested children.

        Return the value of the body, or None if the body raised Cancel.
        """
        m = self.mem
        for attempt in range(1, max_attempts + 1):
            tx = Tx(self, pid, attempt)
            tx.on_abort = []      # type: ignore[attr-defined]
            tx.held = []          # type: ignore[attr-defined]
            yield from self.begin(tx)
            try:
                r = yield from body(tx)
                self.hist.add("T", tx.tid)
                yield from self.commit(tx)
            except (Abort, Cancel) as exc:
                yield
                yield from self.rollback(tx)
                self.hist.add("A", tx.tid)
                m.serial[pid] += 1
                for comp in reversed(tx.on_abort):     # type: ignore[attr-defined]
                    yield from self.run_op(pid, comp)
                self._release(tx)
                if isinstance(exc, Cancel):
                    return None
                held = tuple(m.owner)
                if any(o is not None and o != pid for o in held):
                    yield lambda: tuple(m.owner) != held
                continue
            self.hist.add("C", tx.tid)
            m.serial[pid] += 1
            self._release(tx)
            return r
        raise RuntimeError("too many attempts")

    def _release(self, tx: Tx) -> None:
        for key in tx.held:                            # type: ignore[attr-defined]
            if self.alocks.get(key) == tx.pid:
                del self.alocks[key]
        tx.held = []                                   # type: ignore[attr-defined]

    def open_atomic(self, tx: Tx, key: Any, body: Body,
                    compensate: Callable[[Any], Body | None] | None) -> Gen:
        """Run body as an open nested child of tx and log its compensation."""
        pid = tx.pid
        if self.use_locks and key is not None and self.alocks.get(key) != pid:
            yield lambda: key not in self.alocks       # wait for the abstract lock
            self.alocks[key] = pid
            tx.held.append(key)                        # type: ignore[attr-defined]
        r = yield from self.run_op(pid, body)          # commits on its own
        if compensate is not None:
            comp = compensate(r)
            if comp is not None:
                tx.on_abort.append(comp)               # type: ignore[attr-defined]
        return r


# set operations as transaction bodies

def insert(k: int) -> Body:
    """Add key k; return (added, old size)."""

    def body(tx: Tx) -> Gen:
        present = yield from tx.read(k)
        if present:
            return (False, None)
        s = yield from tx.read(SIZE)
        yield from tx.write(k, 1)
        yield from tx.write(SIZE, s + 1)
        return (True, s)

    return body


def remove(k: int) -> Body:
    """Remove key k; return True if it was there."""

    def body(tx: Tx) -> Gen:
        present = yield from tx.read(k)
        if not present:
            return False
        s = yield from tx.read(SIZE)
        yield from tx.write(k, 0)
        yield from tx.write(SIZE, s - 1)
        return True

    return body


def contains(k: int) -> Body:
    def body(tx: Tx) -> Gen:
        return (yield from tx.read(k)) == 1

    return body


# compensations for insert(k): each maps the result of the insert to a body

def compensate_insert(k: int) -> Callable[[Any], Body | None]:
    """Correct: the inverse of an insert that added k is remove(k)."""
    return lambda r: remove(k) if r[0] else None


def physical_undo(k: int) -> Callable[[Any], Body | None]:
    """Wrong: restore the words the insert wrote to their old values."""

    def comp(r: Any) -> Body | None:
        added, old = r
        if not added:
            return None

        def body(tx: Tx) -> Gen:
            yield from tx.write(k, 0)
            yield from tx.write(SIZE, old)

        return body

    return comp


def unconditional_remove(k: int) -> Callable[[Any], Body | None]:
    """Wrong: remove k even if this insert did not add it."""
    return lambda r: remove(k)


def parent(stm: OpenNestingTL2, pid: int, k: int,
           comp: Callable[[Any], Body | None], cancel: bool, work: int) -> Gen:
    """A parent that inserts k in an open child, reads word `work`, then commits or cancels."""

    def body(tx: Tx) -> Gen:
        r = yield from stm.open_atomic(tx, k, insert(k), comp)
        yield from tx.read(work)
        if cancel:
            raise Cancel
        return r

    return (yield from stm.atomic_top(pid, body))
