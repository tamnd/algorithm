# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyaline/. The authors are listed in prov/XC1TS5.jsonl.
"""Hyaline-1 and Hyaline-1S (Nikolaev and Ravindran) on the simulator in smr_sim.py.

Each process has its own slot with a head word (HRef, HPtr). enter() sets
the head to (1, None). A retiring process collects n + 1 nodes in a batch.
Then it puts one node of the batch into the list of every slot whose HRef
is not 0, with a CAS on the head, and adds the number of inserts to the
reference counter NRef of the batch. leave() swaps the head to (0, None)
and walks the list it took: for each batch node it subtracts 1 from NRef
of that batch. The batch is freed by whoever brings NRef to 0.

Hyaline-1S adds eras for robustness. A global era grows every F
allocations of a process, each node records its birth era, and each slot
publishes the era of its last pointer read in Access. A batch is not put
into a slot whose Access era is older than the smallest birth era in the
batch.

This is the one-slot-per-thread version (Hyaline-1 and -1S of the paper),
not the general Hyaline with shared slots and double-width CAS.

Precondition: references are held only between enter() and leave().
Cost: enter is 1 step, leave is 1 step plus 3 steps per batch in the list;
retire costs O(n) steps per batch of n + 1 nodes, so O(1) per node.
Hyaline-1 is not robust: a stopped process keeps every later batch. With
Hyaline-1S a stopped process keeps only the batches that have a node born
at or before its Access era.
"""

from __future__ import annotations

from typing import Any

from smr_sim import Gen, Memory, NoReclaim


class Hyaline(NoReclaim):
    name = "hyaline"

    def __init__(self, mem: Memory, n: int, robust: bool = False, F: int = 2) -> None:
        super().__init__(mem, n)
        self.robust, self.F = robust, F
        self.batch: list = [[] for _ in range(n)]
        self.count = [0] * n
        self.access = [0] * n
        mem.cells["hy"] = {"era": 1, **{("H", t): (0, None) for t in range(n)}, **{("A", t): 0 for t in range(n)}}

    def setup(self) -> None:
        """Nodes of the initial state are born in era 1."""
        for a, c in self.mem.cells.items():
            if isinstance(a, int):
                c["birth"] = 1

    def alloc(self, t: int, fields: dict) -> Gen:
        e = 1
        if self.robust:
            self.count[t] += 1
            if self.count[t] % self.F == 0:
                yield ("faa", "hy", "era", 1)
            e = yield ("read", "hy", "era")
        return (yield ("alloc", {**fields, "birth": e}))

    def begin(self, t: int) -> Gen:
        yield ("write", "hy", ("H", t), (1, None))  # @line L1

    def protect(self, t: int, i: int, a: Any, f: str) -> Gen:
        """deref of the paper: in Hyaline-1S, publish the era until it is stable around the read."""
        if not self.robust:
            return (yield ("read", a, f))
        while True:
            p = yield ("read", a, f)  # @line L2
            e = yield ("read", "hy", "era")
            if e == self.access[t]:  # @line L3
                return p
            yield ("write", "hy", ("A", t), e)  # @line L4
            self.access[t] = e

    def read(self, t: int, a: Any, f: str) -> Gen:
        if f == "next":
            return (yield from self.protect(t, 0, a, f))
        return (yield ("read", a, f))

    def end(self, t: int) -> Gen:
        _, p = yield ("swap", "hy", ("H", t), (0, None))  # @line L5
        while p is not None:  # @line L6
            nxt = yield ("read", p, "blink")
            ref = yield ("read", p, "bref")
            if (yield ("faa", ref, "nref", -1)) == 1:  # @line L7
                yield from self.free_batch(ref)
            p = nxt

    def free_batch(self, ref: int) -> Gen:
        nodes = yield ("read", ref, "nodes")
        for a in nodes:
            yield ("free", a)

    def retire(self, t: int, a: int) -> Gen:
        self.mem.note_retire(a)
        b = self.batch[t]
        b.append(a)
        if len(b) < self.n + 1:
            return
        self.batch[t] = []
        ref = b[0]
        yield ("write", ref, "nodes", tuple(b))
        yield ("write", ref, "nref", 0)
        minb = min(self.mem.cells[x]["birth"] for x in b)
        inserts = 0
        for q in range(self.n):  # @line L8
            node = b[q + 1]
            yield ("write", node, "bref", ref)
            while True:
                h = yield ("read", "hy", ("H", q))
                if h[0] == 0:  # @line L9
                    break
                if self.robust and (yield ("read", "hy", ("A", q))) < minb:  # @line L10
                    break
                yield ("write", node, "blink", h[1])
                if (yield ("cas", "hy", ("H", q), h, (h[0], node))):  # @line L11
                    inserts += 1
                    break
        if (yield ("faa", ref, "nref", inserts)) == -inserts:  # @line L12
            yield from self.free_batch(ref)
