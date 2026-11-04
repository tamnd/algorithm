# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combining-funnel/. The authors are listed in prov/3D757V.jsonl.

import random
import threading
import time
from collections.abc import Callable, Generator
from typing import TypeVar

R = TypeVar("R")

SPIN = "spin"  # what a step generator yields while it waits
SELF = "self"  # a location word: the owner is busy combining and cannot be captured
CAPTURED = "captured"  # a location word: another thread took over this operation
NONE = None  # no result yet

Steps = Generator[str | None, None, R]


def run(steps: "Steps[R]") -> R:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


class Word:
    """One shared word with atomic read, write, swap and compare-and-swap, simulated with a lock."""

    __slots__ = ("_v", "_lock")

    def __init__(self, v: object = None) -> None:
        self._v = v
        self._lock = threading.Lock()

    def read(self) -> object:
        with self._lock:
            return self._v

    def write(self, v: object) -> None:
        with self._lock:
            self._v = v

    def swap(self, v: object) -> object:
        with self._lock:
            old, self._v = self._v, v
            return old

    def cas(self, expect: object, new: object) -> bool:
        with self._lock:
            if self._v == expect:
                self._v = new
                return True
            return False

    def fetch_add(self, x: int) -> int:
        with self._lock:
            old = self._v
            self._v = old + x  # type: ignore[operator]
            return old  # type: ignore[return-value]


class Record:
    """The per-thread record of the current operation."""

    __slots__ = ("loc", "sum", "kids", "result")

    def __init__(self) -> None:
        self.loc = Word(None)  # a layer number, SELF, CAPTURED, or None when idle
        self.sum = 0  # this operation's amount plus those of the operations it captured
        self.kids: list[tuple[int, int]] = []  # (captured thread, offset of its range)
        self.result = Word(NONE)


class CombiningFunnel:
    """A fetch-and-add counter behind a combining funnel (Shavit and Zemach).

    Each thread passes through D layers. On a layer it swaps its id into a
    random cell and gets the previous occupant. If that thread is on the same
    layer, it tries to capture it: it adds the captured sum to its own and
    remembers the offset. A thread that leaves the last layer uncaptured
    applies the whole sum to the counter with one fetch-and-add and hands each
    captured thread its part of the range. Every access to a shared word is
    one step of a generator.
    """

    def __init__(self, widths: list[int], threads: int, seed: int = 0,
                 choose: Callable[[int, int, int], int] | None = None, wait: int = 1) -> None:
        self.widths = list(widths)
        self.layers = [[Word(None) for _ in range(w)] for w in widths]
        self.recs = [Record() for _ in range(threads)]
        self.counter = Word(0)
        self.wait = wait
        rng = random.Random(seed)
        lock = threading.Lock()

        def default(me: int, d: int, w: int) -> int:
            with lock:
                return rng.randrange(w)

        self.choose = choose or default  # choose(me, layer, width) picks a cell

    def fetch_and_add_steps(self, me: int, x: int) -> "Steps[int]":
        r = self.recs[me]
        r.sum, r.kids = x, []  # @line L1
        r.result.write(NONE)
        r.loc.write(0)
        yield None
        captured = False
        for d, w in enumerate(self.widths):  # @line L2
            q = self.layers[d][self.choose(me, d, w)].swap(me)  # @line L3
            yield None
            if q is not None and q != me:  # @line L4
                if not r.loc.cas(d, SELF):  # @line L5
                    captured = True
                    break
                yield None
                if self.recs[q].loc.cas(d, CAPTURED):  # @line L6
                    yield None
                    r.kids.append((q, r.sum))
                    r.sum += self.recs[q].sum  # frozen: q can no longer capture
                yield None
                r.loc.write(d)  # @line L7
                yield None
            for _ in range(self.wait):  # @line L8
                yield None  # stay on the layer for a while, so that others can collide
            if not r.loc.cas(d, d + 1):  # @line L9
                captured = True
                break
            yield None
        if not captured:
            v = self.counter.fetch_add(r.sum)  # @line L10
            yield None
        else:
            while (v := r.result.read()) is NONE:  # @line L11
                yield SPIN
            yield None
        for q, base in r.kids:  # @line L12
            self.recs[q].result.write(v + base)
            yield None
        r.loc.write(None)
        return v  # @line L13

    def fetch_and_add(self, me: int, x: int) -> int:
        return run(self.fetch_and_add_steps(me, x))

    def value(self) -> int:
        return self.counter.read()  # type: ignore[return-value]
