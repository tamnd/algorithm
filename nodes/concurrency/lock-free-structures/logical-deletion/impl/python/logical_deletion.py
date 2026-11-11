# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logical-deletion/. The authors are listed in prov/5CC8PY.jsonl.

"""Logical deletion: mark a node as deleted, then unlink it.

Two sorted-list sets of integer keys show the technique.

MarkedList is a lock-free list in the style of Michael (2002) and of the
LockFreeList of Herlihy and Shavit. The mark bit lives in the node's own next
field, as a pair (ptr, mark), so one CAS checks the pointer and the mark
together. delete marks the node (the logical deletion, its linearization
point) and then tries once to unlink it; find unlinks every marked node it
meets. contains only reads, and is wait-free.

With mark_in_word=False the mark is a separate field of the node, and insert
reads it before its CAS on next. That is the bug that the shared word
prevents: a delete can mark and unlink the predecessor between the read and
the CAS, and the insert is lost.

LazyList is the lazy list of Heller, Herlihy, Luchangco, Moir, Scherer and
Shavit (2005). It uses the same mark, as a separate field, but changes nodes
only under locks (spin locks here), and contains takes no lock.

Nodes are never freed. Keys never change, so the code reads them with
Memory.peek, not as steps. Each method is a generator that yields one shared
memory step at a time (see explorer.py).
"""

from __future__ import annotations

from typing import Iterable

from explorer import NULL, Memory, Proc

INF = float("inf")


class MarkedList:
    def __init__(self, mem: Memory, keys: Iterable[int] = (), mark_in_word: bool = True) -> None:
        self.mem, self.in_word = mem, mark_in_word
        self.tail = mem.new(key=INF, next=(NULL, False), marked=False)
        nxt = self.tail
        for k in sorted(set(keys), reverse=True):
            nxt = mem.new(key=k, next=(nxt, False), marked=False)
        self.head = mem.new(key=-INF, next=(nxt, False), marked=False)

    def key(self, node: int) -> float:
        return self.mem.peek((node, "key"))

    def _load(self, node: int) -> Proc:
        """Return (successor, mark) of node."""
        if self.in_word:
            return (yield ("read", (node, "next")))
        m = yield ("read", (node, "marked"))
        nxt = yield ("read", (node, "next"))
        return (nxt[0], m)

    def find(self, k: int) -> Proc:
        while True:
            pred = self.head  # @line L13
            curr = (yield ("read", (pred, "next")))[0]
            while True:  # @line L14
                succ, m = yield from self._load(curr)  # @line L15
                if m:  # @line L16
                    if not (yield ("cas", (pred, "next"), (curr, False), (succ, False))):  # @line L17
                        break
                    curr = succ  # @line L18
                elif self.key(curr) >= k:  # @line L19
                    return pred, curr
                else:
                    pred, curr = curr, succ  # @line L20

    def delete(self, k: int) -> Proc:
        while True:  # @line L1
            pred, curr = yield from self.find(k)  # @line L2
            if self.key(curr) != k:  # @line L3
                return False
            succ, m = yield from self._load(curr)  # @line L4
            if m:
                continue
            if self.in_word:
                ok = yield ("cas", (curr, "next"), (succ, False), (succ, True))  # @line L5
            else:
                ok = yield ("cas", (curr, "marked"), False, True)
            if ok:
                break
        yield ("cas", (pred, "next"), (curr, False), (succ, False))  # @line L6
        return True  # @line L7

    def insert(self, k: int) -> Proc:
        node = None
        while True:  # @line L8
            pred, curr = yield from self.find(k)  # @line L9
            if self.key(curr) == k:  # @line L10
                return False
            if node is None:
                node = yield ("alloc", (("key", k), ("next", (curr, False)), ("marked", False)))  # @line L11
            else:
                yield ("write", (node, "next"), (curr, False))
            if not self.in_word and (yield ("read", (pred, "marked"))):
                continue  # the check that does not help: pred can be marked right after it
            if (yield ("cas", (pred, "next"), (curr, False), (node, False))):  # @line L12
                return True

    def contains(self, k: int) -> Proc:
        curr = self.head  # @line L21
        while self.key(curr) < k:
            curr = (yield ("read", (curr, "next")))[0]
        _, m = yield from self._load(curr)  # @line L22
        return self.key(curr) == k and not m

    # Not steps: for the tests, read the list when no process runs.
    def reachable(self) -> list[int]:
        out, n = [], self.mem.peek((self.head, "next"))[0]
        while n != self.tail:
            out.append(self.key(n))
            n = self.mem.peek((n, "next"))[0]
        return out


class LazyList:
    """The lazy list: optimistic traversal with no locks, then lock pred and
    curr, validate, and change. delete sets curr.marked before it unlinks."""

    def __init__(self, mem: Memory, keys: Iterable[int] = ()) -> None:
        self.mem = mem
        self.tail = mem.new(key=INF, next=NULL, marked=False, lock=False)
        nxt = self.tail
        for k in sorted(set(keys), reverse=True):
            nxt = mem.new(key=k, next=nxt, marked=False, lock=False)
        self.head = mem.new(key=-INF, next=nxt, marked=False, lock=False)

    def key(self, node: int) -> float:
        return self.mem.peek((node, "key"))

    def _lock(self, node: int) -> Proc:
        while not (yield ("cas", (node, "lock"), False, True)):
            pass

    def _unlock(self, node: int) -> Proc:
        yield ("write", (node, "lock"), False)

    def _locate(self, k: int) -> Proc:
        """Walk with no locks, lock pred and curr, and validate. Return them locked."""
        while True:
            pred = self.head
            curr = yield ("read", (pred, "next"))
            while self.key(curr) < k:
                pred, curr = curr, (yield ("read", (curr, "next")))
            yield from self._lock(pred)
            yield from self._lock(curr)
            pm = yield ("read", (pred, "marked"))
            cm = yield ("read", (curr, "marked"))
            pn = yield ("read", (pred, "next"))
            if not pm and not cm and pn == curr:
                return pred, curr
            yield from self._unlock(curr)
            yield from self._unlock(pred)

    def insert(self, k: int) -> Proc:
        pred, curr = yield from self._locate(k)
        ok = self.key(curr) != k
        if ok:
            node = yield ("alloc", (("key", k), ("next", curr), ("marked", False), ("lock", False)))
            yield ("write", (pred, "next"), node)
        yield from self._unlock(curr)
        yield from self._unlock(pred)
        return ok

    def delete(self, k: int) -> Proc:
        pred, curr = yield from self._locate(k)
        ok = self.key(curr) == k
        if ok:
            yield ("write", (curr, "marked"), True)  # logical deletion
            succ = yield ("read", (curr, "next"))
            yield ("write", (pred, "next"), succ)  # physical deletion
        yield from self._unlock(curr)
        yield from self._unlock(pred)
        return ok

    def contains(self, k: int) -> Proc:
        curr = self.head
        while self.key(curr) < k:
            curr = yield ("read", (curr, "next"))
        m = yield ("read", (curr, "marked"))
        return self.key(curr) == k and not m

    def reachable(self) -> list[int]:
        out, n = [], self.mem.peek((self.head, "next"))
        while n != self.tail:
            out.append(self.key(n))
            n = self.mem.peek((n, "next"))
        return out
