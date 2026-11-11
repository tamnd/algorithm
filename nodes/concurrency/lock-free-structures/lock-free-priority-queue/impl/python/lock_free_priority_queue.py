# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-free-priority-queue/. The authors are listed in prov/F7GS7Y.jsonl.

"""The skip list priority queue of Linden and Jonsson (OPODIS 2013).

The queue is a skip list sorted by key. delete_min removes the first node
that is still in the queue, so the deleted nodes always form a prefix of the
bottom level. A node is deleted by setting the mark bit of the bottom level
pointer of its *predecessor*, with one fetch-and-or: if the old pointer was
not marked, the node it points to is now deleted, and this delete_min owns
it. An insert links its node at level 0 with a CAS that expects an unmarked
pointer, so it can never link a node behind a deleted node's successor
pointer that has been marked: the mark and the link race on the same word.

Deleted nodes are not unlinked one by one. When a delete_min has walked past
more than `bound` deleted nodes, it moves the head's level 0 pointer past the
prefix with one CAS (keeping a node that is still being inserted at the upper
levels), and then moves the head's upper pointers past deleted nodes.

Upper level pointers carry no mark; they are hints for insert. A node is
"deleted, and not the last deleted node" when its own level 0 pointer is
marked; the last deleted node is the one whose incoming pointer is marked.

With flag_in_node=True, a node is deleted by setting a flag in the node
itself (a CAS on node.dl), as in queues that put the deletion mark in the
deleted node. Then an insert can link a new node right behind a deleted
node, inside the prefix, and the CAS that cuts the prefix loses it.

Levels are given per key (no random numbers), so runs can be replayed. Keys
never change, so the code reads them with Memory.peek. Duplicate keys are
allowed: a new key goes in front of equal keys.
"""

from __future__ import annotations

from typing import Iterable

from explorer import NULL, Memory, Proc

INF = float("inf")
EMPTY = "EMPTY"


def default_level(k: int, maxl: int) -> int:
    """A deterministic stand-in for a random level: the number of trailing 1 bits of k."""
    t = 0
    while k & 1 and t < maxl - 1:
        k >>= 1
        t += 1
    return t


class LindenJonssonPQ:
    def __init__(self, mem: Memory, keys: Iterable[int] = (), maxl: int = 3,
                 levels: dict[int, int] | None = None, bound: int = 1,
                 flag_in_node: bool = False) -> None:
        self.mem, self.maxl, self.bound, self.bug = mem, maxl, bound, flag_in_node
        self.levels = levels or {}
        up = {f"l{i}": NULL for i in range(1, maxl)}
        self.tail = mem.new(key=INF, top=maxl - 1, inserting=False, dl=False, l0=(NULL, False), **up)
        nxt = [self.tail] * maxl
        for k in sorted(keys, reverse=True):
            t = self.level(k)
            n = mem.new(key=k, top=t, inserting=False, dl=False, l0=(nxt[0], False),
                        **{f"l{i}": nxt[i] for i in range(1, t + 1)})
            for i in range(t + 1):
                nxt[i] = n
        self.head = mem.new(key=-INF, top=maxl - 1, inserting=False, dl=False, l0=(nxt[0], False),
                            **{f"l{i}": nxt[i] for i in range(1, maxl)})

    def level(self, k: int) -> int:
        return self.levels.get(k, default_level(k, self.maxl))

    def key(self, n: int) -> float:
        return self.mem.peek((n, "key"))

    def _next(self, n: int, i: int) -> Proc:
        """Read the level i pointer of n as (pointer, mark)."""
        v = yield ("read", (n, f"l{i}"))
        return v if i == 0 else (v, False)

    def _deleted(self, n: int) -> Proc:
        """Is n deleted and not the last deleted node? (With the bug: is n deleted?)"""
        if self.bug:
            return (yield ("read", (n, "dl")))
        return (yield ("read", (n, "l0")))[1]

    def locate_preds(self, k: int) -> Proc:
        """Return (last deleted node seen, preds, succs). Skips the deleted prefix."""
        preds, succs = [NULL] * self.maxl, [NULL] * self.maxl
        dele = NULL
        pred = self.head  # @line L1
        for i in range(self.maxl - 1, -1, -1):  # @line L2
            cur, d = yield from self._next(pred, i)  # @line L3
            while True:
                if self.key(cur) < k or (yield from self._deleted(cur)) or (i == 0 and d):  # @line L4
                    if i == 0 and d:
                        dele = cur  # @line L5
                    pred = cur  # @line L6
                    cur, d = yield from self._next(pred, i)
                else:
                    break
            preds[i], succs[i] = pred, cur  # @line L7
        return dele, preds, succs  # @line L8

    def insert(self, k: int) -> Proc:
        t = self.level(k)
        node = yield ("alloc", (("key", k), ("top", t), ("inserting", True), ("dl", False), ("l0", (NULL, False)))
                      + tuple((f"l{i}", NULL) for i in range(1, t + 1)))  # @line L9
        while True:
            dele, preds, succs = yield from self.locate_preds(k)  # @line L10
            yield ("write", (node, "l0"), (succs[0], False))  # @line L11
            if (yield ("cas", (preds[0], "l0"), (succs[0], False), (node, False))):  # @line L12
                break
        i = 1
        while i <= t:  # @line L13
            yield ("write", (node, f"l{i}"), succs[i])  # @line L14
            if (yield from self._deleted(node)) or (yield from self._deleted(succs[i])) or dele == succs[i]:  # @line L15
                break
            if (yield ("cas", (preds[i], f"l{i}"), succs[i], node)):  # @line L16
                i += 1
            else:
                dele, preds, succs = yield from self.locate_preds(k)  # @line L17
                if succs[0] != node:
                    break
        yield ("write", (node, "inserting"), False)  # @line L18
        return True

    def delete_min(self) -> Proc:
        x, offset, newhead = self.head, 0, NULL
        obshead = yield ("read", (self.head, "l0"))  # @line L19
        while True:
            nxt = yield ("read", (x, "l0"))  # @line L20
            if nxt[0] == self.tail:  # @line L21
                return EMPTY
            if newhead == NULL and (yield ("read", (x, "inserting"))):  # @line L22
                newhead = x
            offset += 1
            if self.bug:
                y = nxt[0]
                won = yield ("cas", (y, "dl"), False, True)
                x = y
                if won:
                    break
                continue
            old = yield ("mark", (x, "l0"))  # @line L23
            x = old[0]  # @line L24
            if not old[1]:
                break
        v = self.key(x)  # @line L25
        if newhead == NULL:
            newhead = x
        if offset <= self.bound:  # @line L26
            return v
        new = (newhead, not self.bug)
        if (yield ("cas", (self.head, "l0"), obshead, new)):  # @line L27
            yield from self.restructure()  # @line L28
        return v  # @line L29

    def restructure(self) -> Proc:
        pred = self.head
        for i in range(self.maxl - 1, 0, -1):  # @line L30
            while True:
                h = yield ("read", (self.head, f"l{i}"))  # @line L31
                if not (yield from self._deleted(h)):  # @line L32
                    break
                cur = yield ("read", (pred, f"l{i}"))  # @line L33
                while (yield from self._deleted(cur)):  # @line L34
                    pred = cur
                    cur = yield ("read", (pred, f"l{i}"))
                if (yield ("cas", (self.head, f"l{i}"), h, cur)):  # @line L35
                    break

    # Not steps: for the tests, read the structure when no process runs.
    def live_keys(self) -> list[float]:
        """The keys of the nodes that are still in the queue, in list order."""
        out, n, d = [], self.mem.peek((self.head, "l0")), None
        ptr, d = n
        while ptr != self.tail:
            dead = self.mem.peek((ptr, "dl")) if self.bug else d
            if not dead:
                out.append(self.key(ptr))
            ptr, d = self.mem.peek((ptr, "l0"))
        return out

    def prefix_length(self) -> int:
        """The number of deleted nodes still reachable at level 0."""
        n, c = self.mem.peek((self.head, "l0")), 0
        while n[1]:
            c += 1
            n = self.mem.peek((n[0], "l0"))
        return c

    def level_keys(self, i: int) -> list[float]:
        out, n = [], self.mem.peek((self.head, f"l{i}"))
        n = n[0] if i == 0 else n
        while n != self.tail:
            out.append(self.key(n))
            v = self.mem.peek((n, f"l{i}"))
            n = v[0] if i == 0 else v
        return out
