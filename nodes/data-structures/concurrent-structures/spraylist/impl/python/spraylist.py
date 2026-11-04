# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spraylist/. The authors are listed in prov/GA0P2G.jsonl.

import math
import random
import threading
import time
from collections.abc import Generator
from typing import Any, TypeVar

R = TypeVar("R")

SPIN = "spin"  # what a step generator yields while it retries
EMPTY = "EMPTY"  # what delete-min returns when the queue is empty

Steps = Generator[str | None, None, R]

MAX_LEVEL = 16


def run(steps: "Steps[R]") -> R:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


class MarkableRef:
    """A reference with a mark bit, read and compare-and-swapped as one word (a lock simulates the hardware)."""

    def __init__(self, ref: Any = None, mark: bool = False) -> None:
        self._ref, self._mark = ref, mark
        self._lock = threading.Lock()

    def get(self) -> "tuple[Any, bool]":
        with self._lock:
            return self._ref, self._mark

    def ref(self) -> Any:
        with self._lock:
            return self._ref

    def cas(self, ref: Any, new_ref: Any, mark: bool, new_mark: bool) -> bool:
        with self._lock:
            if self._ref is ref and self._mark == mark:
                self._ref, self._mark = new_ref, new_mark
                return True
            return False


class Flag:
    """A boolean word with compare-and-swap."""

    def __init__(self) -> None:
        self._value = False
        self._lock = threading.Lock()

    def get(self) -> bool:
        with self._lock:
            return self._value

    def cas(self, old: bool, new: bool) -> bool:
        with self._lock:
            if self._value == old:
                self._value = new
                return True
            return False


class Counter:
    """A word with atomic read and fetch-and-add."""

    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.Lock()

    def get(self) -> int:
        with self._lock:
            return self._value

    def fetch_and_add(self, k: int) -> int:
        with self._lock:
            self._value += k
            return self._value - k


class Node:
    def __init__(self, key: Any, top: int) -> None:
        self.key = key  # (item, unique number); None for the head
        self.top = top
        self.next = [MarkableRef() for _ in range(top + 1)]
        self.claimed = Flag()  # logical deletion by delete-min


def before(node: "Node | None", key: Any) -> bool:
    """True if node holds a key smaller than key (the end of a level is +infinity)."""
    return node is not None and node.key < key


class SprayList:
    """The SprayList of Alistarh, Kopinsky, Li and Shavit on a lock-free skip list.

    Insert is the lock-free skip list insert. Delete-min makes a random walk,
    the spray, from the head: at each of a few levels it moves forward a
    random number of nodes, then goes down. It claims the first unclaimed
    node at or after the landing node with a compare-and-swap, and then
    unlinks it. If the spray finds nothing, a scan from the head looks for
    an unclaimed node, and returns EMPTY only when no insert was in
    progress during the scan. Every access to a shared word is one step.
    """

    def __init__(self, threads: int = 4, seed: int | None = None, jump: int | None = None) -> None:
        self.rng = random.Random(seed)
        lg = max(1, math.ceil(math.log2(max(2, threads))))
        self.height = min(MAX_LEVEL, lg)  # starting level of a spray
        self.jump = jump if jump is not None else lg**3  # largest jump at a level
        self.descent = max(1, math.ceil(math.log2(lg))) if lg > 1 else 1  # levels per descent
        self.head = Node(None, MAX_LEVEL)
        self.started = Counter()  # inserts that have begun
        self.linked = Counter()  # inserts that are linked on level 0
        self._serial = Counter()

    def _random_top(self) -> int:
        top = 0
        while top < MAX_LEVEL and self.rng.random() < 0.5:
            top += 1
        return top

    # ---- the lock-free skip list (Herlihy and Shavit) ----

    def _find_steps(self, key: Any, preds: list, succs: list) -> "Steps[None]":
        """Fill preds and succs for key at every level, unlinking marked nodes on the way."""
        while True:
            retry = False
            pred = self.head
            for level in range(MAX_LEVEL, -1, -1):
                curr = pred.next[level].ref()
                yield None
                while curr is not None:
                    succ, marked = curr.next[level].get()
                    yield None
                    while marked:  # curr is being removed: unlink it at this level
                        if not pred.next[level].cas(curr, succ, False, False):
                            retry = True
                            break
                        yield None
                        curr = succ
                        if curr is None:
                            break
                        succ, marked = curr.next[level].get()
                        yield None
                    if retry or curr is None or not before(curr, key):
                        break
                    pred, curr = curr, succ
                if retry:
                    break
                preds[level], succs[level] = pred, curr
            if not retry:
                return None
            yield SPIN

    def insert_steps(self, item: Any) -> "Steps[None]":
        self.started.fetch_and_add(1)  # @line L13
        yield None
        key = (item, self._serial.fetch_and_add(1))
        node = Node(key, self._random_top())
        preds: list = [None] * (MAX_LEVEL + 1)
        succs: list = [None] * (MAX_LEVEL + 1)
        while True:  # @line L14
            yield from self._find_steps(key, preds, succs)
            for level in range(node.top + 1):
                node.next[level] = MarkableRef(succs[level])
            if preds[0].next[0].cas(succs[0], node, False, False):
                break
            yield SPIN
        yield None
        self.linked.fetch_and_add(1)  # @line L15
        yield None
        for level in range(1, node.top + 1):  # @line L16
            while True:
                cur, marked = node.next[level].get()
                yield None
                if marked:
                    return None  # the node is being removed; stop building it
                if cur is not succs[level]:
                    if not node.next[level].cas(cur, succs[level], False, False):
                        return None
                    yield None
                if preds[level].next[level].cas(succs[level], node, False, False):
                    yield None
                    break
                yield SPIN
                yield from self._find_steps(key, preds, succs)
        return None

    def _remove_steps(self, node: Node) -> "Steps[None]":
        for level in range(node.top, -1, -1):  # @line L17
            while True:
                succ, marked = node.next[level].get()
                yield None
                if marked or node.next[level].cas(succ, succ, False, True):
                    yield None
                    break
        preds: list = [None] * (MAX_LEVEL + 1)
        succs: list = [None] * (MAX_LEVEL + 1)
        yield from self._find_steps(node.key, preds, succs)  # @line L18

    # ---- delete-min ----

    def _claim_from_steps(self, x: "Node | None") -> "Steps[Node | None]":
        """Walk level 0 from x and claim the first unclaimed node."""
        while x is not None:
            if not x.claimed.get():
                yield None
                if x.claimed.cas(False, True):
                    yield None
                    return x
            yield None
            x = x.next[0].ref()
            yield None
        return None

    def delete_min_steps(self) -> "Steps[Any]":
        while True:
            x = self.head  # @line L1
            h = self.height
            while True:  # @line L2
                j = self.rng.randint(0, self.jump)  # @line L3
                for _ in range(j):  # @line L4
                    nxt = x.next[h].ref()
                    yield None
                    if nxt is None:
                        break
                    x = nxt
                if h == 0:
                    break
                h = max(0, h - self.descent)  # @line L5
            if x is self.head:
                x = self.head.next[0].ref()
                yield None
            got = yield from self._claim_from_steps(x)  # @line L6
            if got is not None:
                yield from self._remove_steps(got)  # @line L7
                return got.key[0]
            linked = self.linked.get()  # @line L8
            yield None
            started = self.started.get()
            yield None
            first = self.head.next[0].ref()  # @line L9
            yield None
            got = yield from self._claim_from_steps(first)  # @line L10
            if got is not None:
                yield from self._remove_steps(got)
                return got.key[0]
            if linked == started and self.started.get() == started:  # @line L11
                return EMPTY
            yield SPIN  # @line L12

    def insert(self, item: Any) -> None:
        run(self.insert_steps(item))

    def delete_min(self) -> Any:
        return run(self.delete_min_steps())

    # ---- checks, for a quiescent list ----

    def items(self) -> list[Any]:
        out = []
        x = self.head.next[0].ref()
        while x is not None:
            if not x.claimed.get():
                out.append(x.key[0])
            x = x.next[0].ref()
        return out

    def check_invariant(self) -> None:
        """Every level is sorted, every node of a level is on level 0, and no
        claimed node is still linked (in a quiescent list)."""
        bottom = []
        x = self.head.next[0].ref()
        while x is not None:
            ref, marked = x.next[0].get()
            assert not marked and not x.claimed.get()
            bottom.append(x)
            x = ref
        keys = [n.key for n in bottom]
        assert keys == sorted(keys)
        on = set(map(id, bottom))
        for level in range(1, MAX_LEVEL + 1):
            prev = None
            x = self.head.next[level].ref()
            while x is not None:
                ref, marked = x.next[level].get()
                # a node whose removal raced with the linking of this level may stay
                # here, marked, until the next find passes it
                assert (id(x) in on and not marked) or (marked and x.claimed.get())
                assert x.top >= level and (prev is None or prev.key < x.key)
                prev, x = x, ref
        assert self.linked.get() == self.started.get()
