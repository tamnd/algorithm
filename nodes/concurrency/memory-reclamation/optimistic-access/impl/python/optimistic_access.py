# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimistic-access/. The authors are listed in prov/HH6AVD.jsonl.
"""A simplified optimistic access scheme (after Cohen and Petrank) on smr_sim.py.

Reads are optimistic: a process may read a node that was freed, and then
checks its own warning bit before it uses the value. If the bit is set, it
clears the bit and restarts the operation. Before a CAS, a process puts
hazard pointers on the nodes the CAS uses and checks the warning bit again.
A reclaiming process first sets the warning bit of every process, then
reads all hazard pointers, and frees the retired nodes that no hazard
pointer names.

This is a simplified version: the paper keeps three shared pools of nodes
and a phase number, and recycles in phases that any process can help. Here
each process recycles only its own retired nodes. The memory is a
type-stable pool, as the scheme requires: a read of a freed node returns
stale data, and only writes to freed nodes are errors.

Precondition: the data structure is in the normalized form, so that every
operation can restart from the root at any read. Cost: one extra read of
the warning bit per read; K hazard pointer writes per CAS; a recycle writes
n warning bits and reads n K hazard pointers.
"""

from __future__ import annotations

from typing import Any

from smr_sim import Gen, Memory, NoReclaim, Restart


class OptimisticAccess(NoReclaim):
    name = "oa"
    K = 2

    def __init__(self, mem: Memory, n: int, R: int = 0, check: bool = True) -> None:
        super().__init__(mem, n)
        self.R = R if R > 0 else 2 * n * self.K
        self.check = check
        self.rlist: list = [[] for _ in range(n)]
        mem.cells["oa"] = {**{("W", t): False for t in range(n)}, **{(t, i): None for t in range(n) for i in range(self.K)}}

    def read(self, t: int, a: Any, f: str) -> Gen:
        v = yield ("read", a, f)  # @line L1
        if self.check and (yield ("read", "oa", ("W", t))):  # @line L2
            yield ("write", "oa", ("W", t), False)
            raise Restart()  # @line L3
        return v

    def protect(self, t: int, i: int, a: Any, f: str) -> Gen:
        return (yield from self.read(t, a, f))

    def before_write(self, t: int, ptrs: list) -> Gen:
        for i, p in enumerate(ptrs[: self.K]):
            yield ("write", "oa", (t, i), p)  # @line L4
        if self.check and (yield ("read", "oa", ("W", t))):  # @line L5
            yield ("write", "oa", ("W", t), False)
            raise Restart()

    def end(self, t: int) -> Gen:
        for i in range(self.K):
            yield ("write", "oa", (t, i), None)

    def retire(self, t: int, a: int) -> Gen:
        self.mem.note_retire(a)
        self.rlist[t].append(a)
        if len(self.rlist[t]) < self.R:
            return
        for q in range(self.n):
            yield ("write", "oa", ("W", q), True)  # @line L6
        held = set()
        for q in range(self.n):
            for i in range(self.K):
                h = yield ("read", "oa", (q, i))  # @line L7
                if h is not None:
                    held.add(h)
        keep = []
        for x in self.rlist[t]:
            if x in held:
                keep.append(x)
            else:
                yield ("free", x)  # @line L8
        self.rlist[t] = keep
