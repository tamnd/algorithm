# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lcrq/. The authors are listed in prov/83B4J8.jsonl.

import threading
import time
from collections.abc import Generator
from typing import Any, TypeVar

R_ = TypeVar("R_")

SPIN = "spin"
EMPTY = "EMPTY"
CLOSED = "CLOSED"
OK = "OK"
BOTTOM = None  # an empty cell

Steps = Generator[str | None, None, R_]


def run(steps: "Steps[R_]") -> R_:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


class Word:
    """A shared word with atomic read, compare-and-swap and fetch-and-add, simulated with a lock.

    A cell of the ring is one such word holding (safe, idx, val): its compare-and-swap
    stands for the double-width CAS2 of the paper.
    """

    __slots__ = ("_v", "_lock")

    def __init__(self, v: Any) -> None:
        self._v = v
        self._lock = threading.Lock()

    def read(self) -> Any:
        with self._lock:
            return self._v

    def cas(self, expect: Any, new: Any) -> bool:
        with self._lock:
            if self._v == expect if isinstance(expect, tuple) else self._v is expect:
                self._v = new
                return True
            return False

    def fetch_add(self, x: int) -> Any:
        """For an int word, add x; for a tail word (closed, t), add x to t. Return the old value."""
        with self._lock:
            old = self._v
            self._v = (old[0], old[1] + x) if isinstance(old, tuple) else old + x
            return old

    def close(self) -> None:
        """Set the closed bit of a tail word (test-and-set)."""
        with self._lock:
            self._v = (True, self._v[1])


class CRQ:
    """The concurrent ring queue of Morrison and Afek: a ring of R cells, two fetch-and-add counters."""

    def __init__(self, r: int, first: Any = BOTTOM) -> None:
        self.r = r
        self.head = Word(0)
        self.tail = Word((False, 0))
        self.next = Word(None)
        self.ring = [Word((1, i, BOTTOM)) for i in range(r)]
        if first is not BOTTOM:  # a new ring that already holds one item, at index 0
            self.ring[0] = Word((1, 0, first))
            self.tail = Word((False, 1))

    def enqueue_steps(self, x: Any, patience: int) -> "Steps[str]":
        tries = 0
        while True:
            closed, t = self.tail.fetch_add(1)  # @line L1
            yield None
            if closed:  # @line L2
                return CLOSED
            cell = self.ring[t % self.r]
            s, idx, val = cell.read()  # @line L3
            yield None
            if val is BOTTOM and idx <= t:  # @line L4
                ok = s == 1
                if not ok:
                    ok = self.head.read() <= t
                    yield None
                if ok:
                    done = cell.cas((s, idx, BOTTOM), (1, t, x))  # @line L5
                    yield None
                    if done:
                        return OK
            tries += 1
            h = self.head.read()  # @line L6
            yield None
            if t - h >= self.r or tries >= patience:
                self.tail.close()
                yield None
                return CLOSED

    def dequeue_steps(self) -> "Steps[Any]":
        while True:
            h = self.head.fetch_add(1)  # @line L7
            yield None
            cell = self.ring[h % self.r]
            while True:
                s, idx, val = cell.read()  # @line L8
                yield None
                if idx > h:  # @line L9
                    break
                if val is not BOTTOM:
                    if idx == h:
                        done = cell.cas((s, h, val), (s, h + self.r, BOTTOM))  # @line L10
                        yield None
                        if done:
                            return val
                    else:
                        done = cell.cas((s, idx, val), (0, idx, val))  # @line L11
                        yield None
                        if done:
                            break
                else:
                    done = cell.cas((s, idx, BOTTOM), (s, h + self.r, BOTTOM))  # @line L12
                    yield None
                    if done:
                        break
            _, t = self.tail.read()  # @line L13
            yield None
            if t <= h + 1:  # @line L14
                yield from self._fix_state_steps()
                return EMPTY

    def _fix_state_steps(self) -> "Steps[None]":
        while True:
            tw = self.tail.read()  # @line L15
            yield None
            h = self.head.read()
            yield None
            if self.tail.read() != tw:
                yield None
                continue
            closed, t = tw
            if closed or h <= t:
                return None
            done = self.tail.cas(tw, (False, h))
            yield None
            if done:
                return None


class LCRQ:
    """A linked list of CRQs. Enqueuers move to a new ring when the last one is closed."""

    def __init__(self, r: int = 1 << 10, patience: int = 10) -> None:
        self.r, self.patience = r, patience
        first = CRQ(r)
        self.head = Word(first)
        self.tail = Word(first)

    def enqueue_steps(self, x: Any) -> "Steps[None]":
        while True:
            crq = self.tail.read()  # @line L16
            yield None
            nxt = crq.next.read()
            yield None
            if nxt is not None:
                self.tail.cas(crq, nxt)
                yield None
                continue
            if (yield from crq.enqueue_steps(x, self.patience)) == OK:  # @line L17
                return None
            new = CRQ(self.r, first=x)  # @line L18
            done = crq.next.cas(None, new)
            yield None
            if done:
                self.tail.cas(crq, new)
                yield None
                return None

    def dequeue_steps(self) -> "Steps[Any]":
        while True:
            crq = self.head.read()  # @line L19
            yield None
            v = yield from crq.dequeue_steps()
            if v != EMPTY:
                return v
            nxt = crq.next.read()  # @line L20
            yield None
            if nxt is None:
                return EMPTY
            v = yield from crq.dequeue_steps()  # @line L21
            if v != EMPTY:
                return v
            self.head.cas(crq, nxt)  # @line L22
            yield None

    def enqueue(self, x: Any) -> None:
        run(self.enqueue_steps(x))

    def dequeue(self) -> Any:
        return run(self.dequeue_steps())

    def rings(self) -> int:
        """The number of CRQs from the head to the end of the list."""
        n, c = 0, self.head.read()
        while c is not None:
            n, c = n + 1, c.next.read()
        return n
