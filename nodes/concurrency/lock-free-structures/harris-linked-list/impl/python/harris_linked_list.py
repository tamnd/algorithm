# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harris-linked-list/. The authors are listed in prov/CQ32KC.jsonl.

"""The Harris lock-free sorted linked list (DISC 2001), a set of integer keys.

Each node has an immutable key and a field next that holds a marked pointer
(ptr, mark). A node is logically deleted when the mark bit of its own next
field is set. The search finds two adjacent unmarked nodes left and right
with left.key < key <= right.key, and unlinks every marked node between them
with one CAS. Delete marks the node first and then tries to unlink it.

Flag that models a known bug, for the tests:

- mark=False: the naive list, in which delete unlinks the node with one CAS
  on the predecessor and never marks it. An insert just after the deleted
  node, or a delete of its successor, can then be lost.

Nodes are never freed (the paper assumes a garbage collector). Keys never
change after a node is made, so the code reads them with Memory.peek, not as
steps. Each method is a generator that yields one shared memory step at a
time (see explorer.py).
"""

from __future__ import annotations

from typing import Iterable

from explorer import NULL, Memory, Proc

INF = float("inf")


class HarrisList:
    def __init__(self, mem: Memory, keys: Iterable[int] = (), marked: Iterable[int] = (), mark: bool = True) -> None:
        """Build the list with the given keys. Keys in `marked` start as
        logically deleted (marked but still linked), for tests of the search."""
        self.mem, self.marking = mem, mark
        marked = set(marked)
        self.tail = mem.new(key=INF, next=(NULL, False))
        nxt = self.tail
        for k in sorted(set(keys), reverse=True):
            nxt = mem.new(key=k, next=(nxt, k in marked))
        self.head = mem.new(key=-INF, next=(nxt, False))

    def key(self, node: int) -> float:
        return self.mem.peek((node, "key"))

    def search(self, key: int) -> Proc:
        """Return (left, right): adjacent, both unmarked when checked, with
        left.key < key <= right.key. Unlink the marked nodes between them."""
        while True:
            t = self.head
            t_next = yield ("read", (t, "next"))  # @line L1
            left, left_next = t, t_next
            while True:  # @line L2
                if not t_next[1]:
                    left, left_next = t, t_next  # @line L3
                t = t_next[0]
                if t == self.tail:
                    break
                t_next = yield ("read", (t, "next"))  # @line L4
                if not (t_next[1] or self.key(t) < key):  # @line L5
                    break
            right = t
            if left_next[0] == right:  # @line L6
                if right != self.tail and (yield ("read", (right, "next")))[1]:
                    continue  # @line L7
                return left, right
            if (yield ("cas", (left, "next"), left_next, (right, False))):  # @line L8
                if right != self.tail and (yield ("read", (right, "next")))[1]:
                    continue  # @line L9
                return left, right

    def insert(self, key: int) -> Proc:
        new = None
        while True:
            left, right = yield from self.search(key)  # @line L10
            if self.key(right) == key:  # @line L11
                return False
            if new is None:
                new = yield ("alloc", (("key", key), ("next", (right, False))))  # @line L12
            else:
                yield ("write", (new, "next"), (right, False))
            if (yield ("cas", (left, "next"), (right, False), (new, False))):  # @line L13
                return True

    def delete(self, key: int) -> Proc:
        while True:
            left, right = yield from self.search(key)  # @line L14
            if self.key(right) != key:  # @line L15
                return False
            right_next = yield ("read", (right, "next"))  # @line L16
            if right_next[1]:
                continue
            if not self.marking:
                # The naive list: unlink with no mark.
                if (yield ("cas", (left, "next"), (right, False), (right_next[0], False))):
                    return True
                continue
            if (yield ("cas", (right, "next"), right_next, (right_next[0], True))):  # @line L17
                break
        if not (yield ("cas", (left, "next"), (right, False), (right_next[0], False))):  # @line L18
            yield from self.search(key)
        return True  # @line L19

    def find(self, key: int) -> Proc:
        left, right = yield from self.search(key)  # @line L20
        return self.key(right) == key  # @line L21

    # Not steps: for the tests, read the list when no process runs.
    def reachable(self) -> list[tuple[int, bool]]:
        out, n = [], self.mem.peek((self.head, "next"))[0]
        while n != self.tail:
            nxt = self.mem.peek((n, "next"))
            out.append((self.key(n), nxt[1]))
            n = nxt[0]
        return out
