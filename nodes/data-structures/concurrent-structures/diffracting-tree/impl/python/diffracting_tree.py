# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffracting-tree/. The authors are listed in prov/8G5PTB.jsonl.

import random
import threading
import time
from collections.abc import Generator
from typing import TypeVar

R = TypeVar("R")

SPIN = "spin"  # what a step generator yields while it waits for a partner
TIMEOUT = object()  # the result of an exchange that found no partner
EMPTY, WAITING, BUSY = "EMPTY", "WAITING", "BUSY"

Steps = Generator[str | None, None, R]


def run(steps: "Steps[R]") -> R:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


class Atomic:
    """A word with atomic get, set and compare-and-swap, simulated with a lock."""

    def __init__(self, value: object) -> None:
        self._value = value
        self._lock = threading.Lock()

    def get(self) -> object:
        with self._lock:
            return self._value

    def set(self, value: object) -> None:
        with self._lock:
            self._value = value

    def cas(self, expect: object, new: object) -> bool:
        with self._lock:
            if self._value == expect:
                self._value = new
                return True
            return False

    def fetch_and_add(self, k: int) -> int:
        with self._lock:
            old = self._value
            self._value = old + k  # type: ignore[operator]
            return old  # type: ignore[return-value]


def exchange_steps(slot: Atomic, me: int, patience: int) -> "Steps[object]":
    """The lock-free exchanger of Herlihy and Shavit: the partner's id, or TIMEOUT.

    The slot holds a pair (item, state). Each access is one step.
    """
    for _ in range(patience):  # @line L12
        item, state = slot.get()  # type: ignore[misc] # @line L13
        yield None
        if state == EMPTY:
            ok = slot.cas((item, EMPTY), (me, WAITING))  # @line L14
            yield None
            if not ok:
                continue
            for _ in range(patience):  # @line L15
                item, state = slot.get()  # type: ignore[misc]
                yield SPIN
                if state == BUSY:
                    slot.set((None, EMPTY))
                    yield None
                    return item
            ok = slot.cas((me, WAITING), (None, EMPTY))  # @line L16
            yield None
            if ok:
                return TIMEOUT
            item, _ = slot.get()  # type: ignore[misc] # @line L17
            slot.set((None, EMPTY))
            yield None
            return item
        if state == WAITING:
            ok = slot.cas((item, WAITING), (me, BUSY))  # @line L18
            yield None
            if ok:
                return item
        else:
            yield SPIN  # BUSY: another pair is finishing
    return TIMEOUT  # @line L19


class Balancer:
    """A toggle bit with a prism of exchangers in front of it."""

    def __init__(self, prism_size: int) -> None:
        self.toggle = Atomic(0)
        self.prism = [Atomic((None, EMPTY)) for _ in range(prism_size)]
        self.toggled = [0, 0]  # tokens that left through the toggle, per side
        self.diffracted = 0  # pairs that left through the prism
        self.stats = threading.Lock()  # guards the two statistics above


class DiffractingTree:
    """A diffracting tree counter of Shavit and Zemach, in the form of Herlihy and Shavit.

    width = 2^k output wires; a binary tree of width - 1 balancers sends each
    token to one wire, and wire i hands out i, i + width, i + 2 width, ...
    Two tokens that meet in the prism of a balancer leave on different sides
    without touching its toggle. The counter is quiescently consistent and
    lock-free, not linearizable. Callers pass distinct ids.
    """

    def __init__(self, width: int, prism_size: int = 2, patience: int = 3, seed: int = 0) -> None:
        if width < 2 or width & (width - 1):
            raise ValueError("width must be a power of two, at least 2")
        self.width = width
        self.patience = patience
        self.balancers: list[Balancer] = []
        depth = 0
        while len(self.balancers) < width - 1:
            size = max(1, prism_size >> depth)
            self.balancers.extend(Balancer(size) for _ in range(1 << depth))
            depth += 1
        self.count = [Atomic(0) for _ in range(width)]
        self.rng = random.Random(seed)
        self.rng_lock = threading.Lock()

    def _balance(self, b: Balancer, me: int) -> "Steps[int]":
        with self.rng_lock:
            i = self.rng.randrange(len(b.prism))  # @line L7
        partner = yield from exchange_steps(b.prism[i], me, self.patience)  # @line L8
        if partner is not TIMEOUT:  # @line L9
            d = 0 if me < partner else 1  # type: ignore[operator]
            if d == 0:
                with b.stats:
                    b.diffracted += 1
            return d
        while True:  # @line L10
            t = b.toggle.get()
            yield None
            ok = b.toggle.cas(t, 1 - t)  # type: ignore[operator]
            yield None
            if ok:
                with b.stats:
                    b.toggled[t] += 1  # type: ignore[index]
                return t  # @line L11

    def get_and_increment_steps(self, me: int) -> "Steps[int]":
        j, wire, bit = 0, 0, 1  # @line L1
        while j < self.width - 1:  # @line L2
            d = yield from self._balance(self.balancers[j], me)  # @line L3
            wire, bit, j = wire + d * bit, 2 * bit, 2 * j + 1 + d  # @line L4
        k = self.count[wire].fetch_and_add(1)  # @line L5
        yield None
        return wire + self.width * k  # type: ignore[operator] # @line L6

    def get_and_increment(self, me: int) -> int:
        return run(self.get_and_increment_steps(me))

    def wire_counts(self) -> list[int]:
        return [c.get() for c in self.count]  # type: ignore[misc]

    def check_step_property(self) -> None:
        """At a quiet moment: wire counts fall by at most 1 from left to right, and so do balancers."""
        y = self.wire_counts()
        assert all(0 <= y[i] - y[j] <= 1 for i in range(len(y)) for j in range(i + 1, len(y)))
        for b in self.balancers:
            assert b.toggled[0] - b.toggled[1] == b.toggle.get()
            assert all(s.get() == (None, EMPTY) for s in b.prism)
