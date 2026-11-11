# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hazard-pointers/. The authors are listed in prov/319C81.jsonl.
"""Michael's hazard pointers on the simulator in smr_sim.py.

Each process has K hazard pointer slots in the static block "hp". A reader
publishes a pointer in a slot and then reads the source again to check that
the pointer is still there (the validation). A retired node goes to a
private list; when the list reaches R nodes, the process reads all n*K
slots and frees every listed node that no slot names.

Precondition: a process dereferences only nodes that it has protected and
validated. Cost: protect is 3 steps per try; a scan reads n*K slots and
frees at least R - n*K nodes, so with R = 2*n*K the cost per retired node
is O(1) amortized. At most n*R retired nodes are unfreed at any time, even
if some processes stop.
"""

from __future__ import annotations

from typing import Any

from smr_sim import Gen, Memory, NoReclaim


class HazardPointers(NoReclaim):
    name = "hp"
    K = 2

    def __init__(self, mem: Memory, n: int, R: int = 0, validate: bool = True) -> None:
        super().__init__(mem, n)
        self.R = R if R > 0 else 2 * n * self.K
        self.validate = validate
        self.rlist: list = [[] for _ in range(n)]
        mem.cells["hp"] = {(t, i): None for t in range(n) for i in range(self.K)}

    def protect(self, t: int, i: int, a: Any, f: str) -> Gen:
        """Read a.f, publish it in slot i, and re-read a.f until it did not change."""
        while True:
            p = yield ("read", a, f)  # @line L1
            yield ("write", "hp", (t, i), p)  # @line L2
            if not self.validate:
                return p
            if (yield ("read", a, f)) == p:  # @line L3
                return p  # @line L4

    def retire(self, t: int, a: int) -> Gen:
        """Put a in the private list, and scan when the list holds R nodes."""
        self.mem.note_retire(a)
        self.rlist[t].append(a)  # @line L5
        if len(self.rlist[t]) >= self.R:  # @line L6
            yield from self.scan(t)

    def scan(self, t: int) -> Gen:
        """Read every slot, then free the listed nodes that no slot names."""
        plist = set()
        for q in range(self.n):  # @line L7
            for i in range(self.K):
                h = yield ("read", "hp", (q, i))
                if h is not None:
                    plist.add(h)
        keep = []
        for a in self.rlist[t]:  # @line L8
            if a in plist:
                keep.append(a)
            else:
                yield ("free", a)  # @line L9
        self.rlist[t] = keep

    def end(self, t: int) -> Gen:
        """Clear the own slots after the operation."""
        for i in range(self.K):
            yield ("write", "hp", (t, i), None)  # @line L10
