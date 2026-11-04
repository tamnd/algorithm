# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fine-grained-concurrent-heap/. The authors are listed in prov/5B1WV2.jsonl.

import threading
import time
from collections.abc import Generator
from typing import Any, TypeVar

R = TypeVar("R")

SPIN = "spin"  # what a step generator yields while it waits
EMPTY_HEAP = "EMPTY"  # what delete-min returns on an empty heap

EMPTY = -1  # tag of an unused slot
AVAILABLE = 0  # tag of an item that is in its place
# any other tag is the id of the thread whose insert is still moving the item up

Steps = Generator[str | None, None, R]


def run(steps: "Steps[R]") -> R:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


def bit_reversed(n: int) -> int:
    """The slot of the n-th item: keep the top bit of n and reverse the bits below it."""
    top = n.bit_length() - 1
    low = n - (1 << top)
    rev = int(format(low, f"0{top}b")[::-1], 2) if top else 0
    return (1 << top) | rev


class Slot:
    __slots__ = ("lock", "tag", "pri")

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.tag = EMPTY
        self.pri: Any = None


class ConcurrentHeap:
    """The concurrent heap of Hunt, Michael, Parthasarathy and Scott (1996).

    An array heap with a lock per slot and one lock for the size. Insert
    puts its item at the bottom, in bit-reversed order, and moves it up
    while holding only a parent and a child lock at a time. Delete-min takes
    the bottom item, puts it at the root and moves it down, again with two
    locks at a time. Locks are always taken from the root downward, so
    inserts and deletes can run in parallel without deadlock. Every lock
    attempt and every field change is one step of a generator.
    """

    def __init__(self, levels: int = 10) -> None:
        self.capacity = (1 << levels) - 1
        self.slots = [Slot() for _ in range(self.capacity + 2)]  # 1-based, with spare room
        self.size_lock = threading.Lock()
        self.size = 0

    def _lock_steps(self, lock: threading.Lock) -> "Steps[None]":
        while not lock.acquire(blocking=False):
            yield SPIN
        yield None

    def _swap(self, i: int, j: int) -> None:
        a, b = self.slots[i], self.slots[j]
        a.tag, b.tag = b.tag, a.tag
        a.pri, b.pri = b.pri, a.pri

    def insert_steps(self, pri: Any, me: int) -> "Steps[None]":
        """Insert pri; me is the caller's thread id, a number of at least 1."""
        assert me > AVAILABLE
        yield from self._lock_steps(self.size_lock)  # @line L1
        if self.size == self.capacity:
            self.size_lock.release()
            raise OverflowError("heap is full")
        self.size += 1
        i = bit_reversed(self.size)
        yield from self._lock_steps(self.slots[i].lock)  # @line L2
        self.size_lock.release()
        yield None
        s = self.slots[i]  # @line L3
        s.pri, s.tag = pri, me
        yield None
        s.lock.release()
        yield None
        while i > 1:  # @line L4
            parent = i // 2
            yield from self._lock_steps(self.slots[parent].lock)  # @line L5
            yield from self._lock_steps(self.slots[i].lock)
            old = i
            p, c = self.slots[parent], self.slots[i]
            if p.tag == AVAILABLE and c.tag == me:  # @line L6
                if c.pri < p.pri:
                    self._swap(i, parent)  # @line L7
                    i = parent
                else:
                    c.tag = AVAILABLE  # @line L8
                    i = 0
            elif c.tag != me:  # @line L9
                i = parent  # a delete-min moved the item up, or took it; follow it to the root
            yield None
            self.slots[old].lock.release()  # @line L10
            self.slots[parent].lock.release()
            yield None
            if i == old:  # @line L11
                yield SPIN  # the parent holds another insert's item; wait for it to move
        if i == 1:  # @line L12
            yield from self._lock_steps(self.slots[1].lock)
            if self.slots[1].tag == me:
                self.slots[1].tag = AVAILABLE
                yield None
            self.slots[1].lock.release()
        return None

    def delete_min_steps(self) -> "Steps[Any]":
        yield from self._lock_steps(self.size_lock)  # @line L13
        if self.size == 0:
            self.size_lock.release()
            return EMPTY_HEAP
        bottom = bit_reversed(self.size)
        self.size -= 1
        yield from self._lock_steps(self.slots[bottom].lock)  # @line L14
        self.size_lock.release()
        yield None
        b = self.slots[bottom]  # @line L15
        pri = b.pri
        b.tag, b.pri = EMPTY, None
        yield None
        b.lock.release()
        yield None
        if bottom == 1:
            return pri
        yield from self._lock_steps(self.slots[1].lock)  # @line L16
        root = self.slots[1]
        if root.tag == EMPTY:
            root.lock.release()
            return pri
        pri, root.pri = root.pri, pri  # @line L17
        root.tag = AVAILABLE
        yield None
        i = 1
        while 2 * i <= self.capacity:  # @line L18
            left, right = 2 * i, 2 * i + 1
            yield from self._lock_steps(self.slots[left].lock)
            yield from self._lock_steps(self.slots[right].lock)
            ls, rs = self.slots[left], self.slots[right]
            if ls.tag == EMPTY:  # @line L19
                ls.lock.release()
                rs.lock.release()
                yield None
                break
            if rs.tag == EMPTY or ls.pri < rs.pri:
                rs.lock.release()
                child = left
            else:
                ls.lock.release()
                child = right
            yield None
            if self.slots[child].pri < self.slots[i].pri:  # @line L20
                self._swap(child, i)
                yield None
                self.slots[i].lock.release()
                i = child
            else:
                self.slots[child].lock.release()
                yield None
                break
        self.slots[i].lock.release()  # @line L21
        return pri

    def insert(self, pri: Any, me: int = 1) -> None:
        run(self.insert_steps(pri, me))

    def delete_min(self) -> Any:
        return run(self.delete_min_steps())

    # ---- checks, for a quiescent heap ----

    def items(self) -> list[Any]:
        return sorted(self.slots[bit_reversed(n)].pri for n in range(1, self.size + 1))

    def check_invariant(self) -> None:
        assert not self.size_lock.locked()
        used = {bit_reversed(n) for n in range(1, self.size + 1)}
        for i in range(1, self.capacity + 1):
            s = self.slots[i]
            assert not s.lock.locked()
            assert (s.tag == AVAILABLE) == (i in used) and (s.tag == EMPTY) == (i not in used)
            if i > 1 and i in used:
                assert self.slots[i // 2].pri <= s.pri
