# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-blocking-bst/. The authors are listed in prov/H9D744.jsonl.

"""The non-blocking binary search tree of Ellen, Fatourou, Ruppert and van Breugel (PODC 2010).

The tree is leaf oriented: the keys of the set are in the leaves, and the
internal nodes only route the searches. Each internal node has full two
children. A search for k goes left at an internal node with key > k and right
otherwise.

Each internal node has a field update, a pair (state, info). The state is
CLEAN, IFLAG, DFLAG or MARK, and info points to an Info record that
describes the operation that set it. An insert flags the parent of the leaf
(IFLAG), swings the child pointer to a new internal node with two leaves, and
unflags the parent. A delete flags the grandparent (DFLAG), marks the parent
(MARK, for ever), swings the grandparent's child pointer to the sibling of
the leaf, and unflags the grandparent. A process that finds a flag or a mark
in its way first helps the operation in the Info record to finish.

The two sentinel keys INF1 < INF2 are larger than every key of the set, so a
real leaf always has a parent and a grandparent.

Flag that models a known bug, for the tests:

- mark_parent=False: delete does not mark the parent. Then an insert can
  still flag the parent and put a new leaf under it, after the delete has
  read the sibling, and the delete then cuts the parent and the new leaf out
  of the tree.

Nodes and Info records are never freed (the paper assumes a garbage
collector). Keys and the fields of an Info record never change after they
are made, so the code reads them with Memory.peek, not as steps. Each method
is a generator that yields one shared memory step at a time (see
explorer.py).
"""

from __future__ import annotations

from typing import Any, Iterable

from explorer import NULL, Memory, Proc

CLEAN, IFLAG, DFLAG, MARK = "CLEAN", "IFLAG", "DFLAG", "MARK"
INF1, INF2 = 10**9, 10**9 + 1


class EFRBTree:
    def __init__(self, mem: Memory, keys: Iterable[int] = (), mark_parent: bool = True) -> None:
        self.mem, self.mark_parent = mem, mark_parent
        l1 = mem.new(key=INF1, leaf=True)
        l2 = mem.new(key=INF2, leaf=True)
        self.root = mem.new(key=INF2, leaf=False, left=l1, right=l2, update=(CLEAN, NULL))
        for k in keys:
            self.solo(self.insert(k))

    def solo(self, g: Proc) -> Any:
        """Run one operation alone, before the run starts (not steps of the run)."""
        try:
            op = g.send(None)
            while True:
                op = g.send(self.mem.apply(op))
        except StopIteration as e:
            return e.value

    def key(self, n: int) -> int:
        return self.mem.peek((n, "key"))

    def is_leaf(self, n: int) -> bool:
        return self.mem.peek((n, "leaf"))

    def field(self, op: int, f: str) -> Any:
        return self.mem.peek((op, f))

    def search(self, k: int) -> Proc:
        gp = p = NULL
        l = self.root  # @line L1
        pupdate = gpupdate = (CLEAN, NULL)
        while not self.is_leaf(l):  # @line L2
            gp, p, gpupdate = p, l, pupdate  # @line L3
            pupdate = yield ("read", (p, "update"))  # @line L4
            if k < self.key(l):  # @line L5
                l = yield ("read", (p, "left"))
            else:
                l = yield ("read", (p, "right"))  # @line L6
        return gp, p, l, pupdate, gpupdate  # @line L7

    def find(self, k: int) -> Proc:
        _, _, l, _, _ = yield from self.search(k)  # @line L8
        return self.key(l) == k

    def insert(self, k: int) -> Proc:
        while True:
            _, p, l, pupdate, _ = yield from self.search(k)  # @line L9
            lk = self.key(l)
            if lk == k:  # @line L10
                return False
            if pupdate[0] != CLEAN:  # @line L11
                yield from self.help(pupdate)
                continue
            newleaf = yield ("alloc", (("key", k), ("leaf", True)))  # @line L12
            sibling = yield ("alloc", (("key", lk), ("leaf", True)))
            left, right = (newleaf, sibling) if k < lk else (sibling, newleaf)
            newint = yield ("alloc", (("key", max(k, lk)), ("leaf", False), ("left", left),
                                      ("right", right), ("update", (CLEAN, NULL))))  # @line L13
            op = yield ("alloc", (("kind", "I"), ("p", p), ("l", l), ("new", newint)))  # @line L14
            result = yield ("cmpxchg", (p, "update"), pupdate, (IFLAG, op))  # @line L15
            if result == pupdate:  # @line L16
                yield from self.help_insert(op)
                return True
            yield from self.help(result)  # @line L17

    def help_insert(self, op: int) -> Proc:
        p, l, new = self.field(op, "p"), self.field(op, "l"), self.field(op, "new")
        yield from self.cas_child(p, l, new)  # @line L18
        yield ("cas", (p, "update"), (IFLAG, op), (CLEAN, op))  # @line L19

    def delete(self, k: int) -> Proc:
        while True:
            gp, p, l, pupdate, gpupdate = yield from self.search(k)  # @line L20
            if self.key(l) != k:  # @line L21
                return False
            if gpupdate[0] != CLEAN:  # @line L22
                yield from self.help(gpupdate)
            elif pupdate[0] != CLEAN:  # @line L23
                yield from self.help(pupdate)
            else:
                op = yield ("alloc", (("kind", "D"), ("gp", gp), ("p", p), ("l", l), ("pupdate", pupdate)))  # @line L24
                result = yield ("cmpxchg", (gp, "update"), gpupdate, (DFLAG, op))  # @line L25
                if result == gpupdate:  # @line L26
                    if (yield from self.help_delete(op)):  # @line L27
                        return True
                else:
                    yield from self.help(result)  # @line L28

    def help_delete(self, op: int) -> Proc:
        gp, p, pupdate = self.field(op, "gp"), self.field(op, "p"), self.field(op, "pupdate")
        if not self.mark_parent:
            yield from self.help_marked(op)
            return True
        result = yield ("cmpxchg", (p, "update"), pupdate, (MARK, op))  # @line L29
        if result == pupdate or result == (MARK, op):  # @line L30
            yield from self.help_marked(op)
            return True
        yield from self.help(result)  # @line L31
        yield ("cas", (gp, "update"), (DFLAG, op), (CLEAN, op))  # @line L32
        return False  # @line L33

    def help_marked(self, op: int) -> Proc:
        gp, p, l = self.field(op, "gp"), self.field(op, "p"), self.field(op, "l")
        r = yield ("read", (p, "right"))  # @line L34
        other = (yield ("read", (p, "left"))) if r == l else r
        yield from self.cas_child(gp, p, other)  # @line L35
        yield ("cas", (gp, "update"), (DFLAG, op), (CLEAN, op))  # @line L36

    def help(self, u: tuple) -> Proc:
        state, op = u
        if state == IFLAG:  # @line L37
            yield from self.help_insert(op)
        elif state == MARK:  # @line L38
            yield from self.help_marked(op)
        elif state == DFLAG:  # @line L39
            yield from self.help_delete(op)

    def cas_child(self, parent: int, old: int, new: int) -> Proc:
        if self.key(new) < self.key(parent):  # @line L40
            yield ("cas", (parent, "left"), old, new)
        else:
            yield ("cas", (parent, "right"), old, new)  # @line L41

    # Not steps: for the tests, read the tree when no process runs.
    def leaves(self) -> list[int]:
        """The keys of the real leaves, in order from left to right."""
        out: list[int] = []

        def walk(n: int) -> None:
            if self.is_leaf(n):
                if self.key(n) < INF1:
                    out.append(self.key(n))
                return
            walk(self.mem.peek((n, "left")))
            walk(self.mem.peek((n, "right")))

        walk(self.root)
        return out

    def check_shape(self) -> str | None:
        """Every key in the left subtree of a node is less than its key, and every key on the right is at least it."""

        def walk(n: int, lo: float, hi: float) -> str | None:
            k = self.key(n)
            if not lo <= k < hi and not (k == hi == INF2):
                return f"key {k} out of range [{lo}, {hi})"
            if self.is_leaf(n):
                return None
            return walk(self.mem.peek((n, "left")), lo, k) or walk(self.mem.peek((n, "right")), k, hi)

        return walk(self.root, -float("inf"), INF2)

    def internal_depth(self, k: int) -> int:
        """The number of internal nodes on the search path for k."""
        n, d = self.root, 0
        while not self.is_leaf(n):
            d += 1
            n = self.mem.peek((n, "left" if k < self.key(n) else "right"))
        return d
