# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combining-tree/. The authors are listed in prov/9G1178.jsonl.

import threading
import time
from collections.abc import Generator
from typing import TypeVar

R = TypeVar("R")

SPIN = "spin"  # what a step generator yields while it waits

Steps = Generator[str | None, None, R]

IDLE, FIRST, SECOND, RESULT, ROOT = "IDLE", "FIRST", "SECOND", "RESULT", "ROOT"


def run(steps: "Steps[R]") -> R:
    """Run a step generator to its end in the calling thread and return its result."""
    while True:
        try:
            if next(steps) == SPIN:
                time.sleep(0)
        except StopIteration as stop:
            return stop.value


class Node:
    """A node of the tree. Its fields are read and written only under mon."""

    def __init__(self, parent: "Node | None") -> None:
        self.parent = parent
        self.status = ROOT if parent is None else IDLE
        self.locked = False
        self.first = 0
        self.second = 0
        self.result = 0
        self.mon = threading.Lock()

    def enter(self, ready) -> Generator[str | None, None, None]:
        """Take the monitor once ready() holds; yield SPIN after each failed check."""
        while True:
            while not self.mon.acquire(blocking=False):
                yield SPIN
            if ready():
                return
            self.mon.release()
            yield SPIN

    def leave(self) -> Generator[str | None, None, None]:
        self.mon.release()
        yield None


class CombiningTree:
    """The software combining tree counter of Herlihy and Shavit.

    A complete binary tree with width - 1 nodes for width threads; threads
    2i and 2i + 1 start at leaf i. The first thread to reach a node goes on
    up, carrying the increments of the second one, so at the root one step
    adds a whole batch. get_and_increment is linearizable: a batch takes
    effect at its step at the root. The tree is blocking: a thread may wait
    for its partner at a node. The thread ids of concurrent callers must be
    distinct and below width.
    """

    def __init__(self, width: int) -> None:
        if width < 2 or width & (width - 1):
            raise ValueError("width must be a power of two, at least 2")
        self.width = width
        self.nodes = [Node(None)]
        for i in range(1, width - 1):
            self.nodes.append(Node(self.nodes[(i - 1) // 2]))
        self.leaves = self.nodes[len(self.nodes) - width // 2 :]

    def _precombine(self, n: Node) -> "Steps[bool]":
        yield from n.enter(lambda: not n.locked)  # @line L9
        if n.status == IDLE:  # @line L10
            n.status = FIRST
            go_up = True
        elif n.status == FIRST:  # @line L11
            n.locked = True
            n.status = SECOND
            go_up = False
        else:
            go_up = False  # @line L12
        yield from n.leave()
        return go_up

    def _combine(self, n: Node, c: int) -> "Steps[int]":
        yield from n.enter(lambda: not n.locked)  # @line L13
        n.locked = True  # @line L14
        n.first = c
        out = c if n.status == FIRST else c + n.second  # @line L15
        yield from n.leave()
        return out

    def _op(self, n: Node, c: int) -> "Steps[int]":
        yield from n.enter(lambda: True)
        if n.status == ROOT:  # @line L16
            prior = n.result
            n.result = prior + c
            yield from n.leave()
            return prior
        n.second = c  # @line L17
        n.locked = False
        yield from n.leave()
        yield from n.enter(lambda: n.status == RESULT)  # @line L18
        n.locked = False  # @line L19
        n.status = IDLE
        prior = n.result
        yield from n.leave()
        return prior

    def _distribute(self, n: Node, prior: int) -> "Steps[None]":
        yield from n.enter(lambda: True)
        if n.status == FIRST:  # @line L20
            n.status = IDLE
            n.locked = False
        else:
            n.result = prior + n.first  # @line L21
            n.status = RESULT
        yield from n.leave()

    def get_and_increment_steps(self, tid: int) -> "Steps[int]":
        leaf = self.leaves[tid // 2]  # @line L1
        node = leaf
        while (yield from self._precombine(node)):  # @line L2
            assert node.parent is not None
            node = node.parent
        stop = node  # @line L3
        node, combined, stack = leaf, 1, []
        while node is not stop:  # @line L4
            combined = yield from self._combine(node, combined)  # @line L5
            stack.append(node)
            assert node.parent is not None
            node = node.parent
        prior = yield from self._op(stop, combined)  # @line L6
        while stack:  # @line L7
            yield from self._distribute(stack.pop(), prior)
        return prior  # @line L8

    def get_and_increment(self, tid: int) -> int:
        return run(self.get_and_increment_steps(tid))

    def value(self) -> int:
        """The count, read at a quiet moment."""
        return self.nodes[0].result

    def check_invariant(self) -> None:
        """At a quiet moment: every node but the root is IDLE and unlocked."""
        assert self.nodes[0].status == ROOT
        for n in self.nodes[1:]:
            assert n.status == IDLE and not n.locked and not n.mon.locked()
