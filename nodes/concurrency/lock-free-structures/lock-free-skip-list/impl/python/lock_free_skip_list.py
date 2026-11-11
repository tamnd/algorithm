# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-free-skip-list/. The authors are listed in prov/BMT1MG.jsonl.

"""The lock-free skip list of Herlihy and Shavit (The Art of Multiprocessor
Programming, the LockFreeSkipList class), after Fraser (2004).

Each level is a lock-free list with the mark bit in the next word. A node
with top level t has the words (node, l0) .. (node, lt), each holding a marked
pointer (successor, mark). The bottom level holds the set: a key is present
if its node is linked at level 0 and (node, l0) is not marked. The upper
levels are shortcuts.

add links the node at level 0 first (its linearization point) and then at
the higher levels, one by one. remove marks the levels from the top down and
then marks level 0; the process whose CAS marks level 0 wins, and its mark is
the linearization point. find unlinks every marked node it meets, at every
level. contains never writes: it skips marked nodes.

Before each try to link the new node at an upper level, add sets the node's
own next at that level to the successor it found, and it stops if the node is
marked there (the node is being removed). The book's code sets that field
only once, when the node is made.

With decide_at_top=True, remove also returns True when its own CAS marked
the top level, even if another process then marked level 0. That is a bug:
two removes of one key can both return True.

Levels are given per key (no random numbers), so that runs can be replayed.
Keys never change, so the code reads them with Memory.peek.
"""

from __future__ import annotations

from typing import Iterable

from explorer import NULL, Memory, Proc

INF = float("inf")


def default_level(k: int, maxl: int) -> int:
    """A deterministic stand-in for a random level: the number of trailing 1 bits of k."""
    t = 0
    while k & 1 and t < maxl - 1:
        k >>= 1
        t += 1
    return t


class LockFreeSkipList:
    def __init__(self, mem: Memory, keys: Iterable[int] = (), maxl: int = 3,
                 levels: dict[int, int] | None = None, decide_at_top: bool = False) -> None:
        self.mem, self.maxl, self.bad = mem, maxl, decide_at_top
        self.levels = levels or {}
        self.tail = mem.new(key=INF, top=maxl - 1, **{f"l{i}": (NULL, False) for i in range(maxl)})
        nodes = []
        for k in sorted(set(keys)):
            nodes.append((k, self.level(k)))
        nxt = [self.tail] * maxl
        for k, t in reversed(nodes):
            n = mem.new(key=k, top=t, **{f"l{i}": (nxt[i], False) for i in range(t + 1)})
            for i in range(t + 1):
                nxt[i] = n
        self.head = mem.new(key=-INF, top=maxl - 1, **{f"l{i}": (nxt[i], False) for i in range(maxl)})

    def level(self, k: int) -> int:
        return self.levels.get(k, default_level(k, self.maxl))

    def key(self, n: int) -> float:
        return self.mem.peek((n, "key"))

    def top(self, n: int) -> int:
        return self.mem.peek((n, "top"))

    @staticmethod
    def w(n: int, i: int) -> tuple:
        return (n, f"l{i}")

    def find(self, k: int) -> Proc:
        """Return (found, preds, succs). Unlinks marked nodes on the way."""
        w = self.w
        while True:  # retry
            preds, succs = [NULL] * self.maxl, [NULL] * self.maxl
            pred = self.head  # @line L1
            ok = True
            for i in range(self.maxl - 1, -1, -1):  # @line L2
                curr = (yield ("read", w(pred, i)))[0]  # @line L3
                while True:
                    succ, m = yield ("read", w(curr, i))  # @line L4
                    while m:  # @line L5
                        if not (yield ("cas", w(pred, i), (curr, False), (succ, False))):  # @line L6
                            ok = False
                            break
                        curr = succ  # @line L7
                        succ, m = yield ("read", w(curr, i))
                    if not ok:
                        break
                    if self.key(curr) < k:  # @line L8
                        pred, curr = curr, succ
                    else:
                        break
                if not ok:
                    break
                preds[i], succs[i] = pred, curr  # @line L9
            if ok:
                return self.key(succs[0]) == k, preds, succs  # @line L10

    def add(self, k: int) -> Proc:
        w = self.w
        t = self.level(k)
        while True:
            found, preds, succs = yield from self.find(k)  # @line L11
            if found:  # @line L12
                return False
            node = yield ("alloc", (("key", k), ("top", t)) + tuple((f"l{i}", (succs[i], False)) for i in range(t + 1)))  # @line L13
            if not (yield ("cas", w(preds[0], 0), (succs[0], False), (node, False))):  # @line L14
                continue
            break
        for i in range(1, t + 1):  # @line L15
            while True:
                cur = yield ("read", w(node, i))  # @line L16
                if cur[1]:
                    return True  # node is being removed: stop building it
                if cur[0] != succs[i] and not (yield ("cas", w(node, i), cur, (succs[i], False))):
                    continue
                if (yield ("cas", w(preds[i], i), (succs[i], False), (node, False))):  # @line L17
                    break
                found, preds, succs = yield from self.find(k)  # @line L18
                if not found or succs[0] != node:
                    return True  # node already removed at level 0
        return True  # @line L19

    def remove(self, k: int) -> Proc:
        w = self.w
        found, preds, succs = yield from self.find(k)  # @line L20
        if not found:  # @line L21
            return False
        node = succs[0]
        marked_top = False
        for i in range(self.top(node), 0, -1):  # @line L22
            succ, m = yield ("read", w(node, i))
            while not m:  # @line L23
                if (yield ("cas", w(node, i), (succ, False), (succ, True))) and i == self.top(node):
                    marked_top = True
                succ, m = yield ("read", w(node, i))
        succ, m = yield ("read", w(node, 0))  # @line L24
        while True:
            won = yield ("cas", w(node, 0), (succ, False), (succ, True))  # @line L25
            if won:
                yield from self.find(k)  # @line L26
                return True
            succ, m = yield ("read", w(node, 0))
            if m:  # @line L27
                return self.bad and marked_top

    def contains(self, k: int) -> Proc:
        w = self.w
        pred = self.head  # @line L28
        curr = NULL
        for i in range(self.maxl - 1, -1, -1):
            curr = (yield ("read", w(pred, i)))[0]
            while True:
                succ, m = yield ("read", w(curr, i))  # @line L29
                while m:  # skip a marked node, never unlink it
                    curr = succ
                    succ, m = yield ("read", w(curr, i))
                if self.key(curr) < k:
                    pred, curr = curr, succ
                else:
                    break
        return self.key(curr) == k  # @line L30

    # Not steps: for the tests, read the structure when no process runs.
    def level_keys(self, i: int, unmarked: bool = True) -> list[float]:
        out, n = [], self.mem.peek(self.w(self.head, i))[0]
        while n != self.tail:
            nxt, m = self.mem.peek(self.w(n, i))
            if not (unmarked and m):
                out.append(self.key(n))
            n = nxt
        return out

    def keys(self) -> list[float]:
        out, n = [], self.mem.peek(self.w(self.head, 0))[0]
        while n != self.tail:
            nxt, m = self.mem.peek(self.w(n, 0))
            if not m:
                out.append(self.key(n))
            n = nxt
        return out
