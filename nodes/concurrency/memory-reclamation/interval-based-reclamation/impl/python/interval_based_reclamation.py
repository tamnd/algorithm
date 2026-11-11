# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-based-reclamation/. The authors are listed in prov/8KPT1J.jsonl.
"""2GEIBR, interval-based reclamation with two global epochs (Wen et al.), on smr_sim.py.

A global epoch E grows by one every F allocations of a process. Each node
records its birth epoch, and gets a retire epoch when it is retired. Each
process reserves an interval [lower, upper] of epochs: at the start of an
operation both ends are set to E, and every pointer read raises upper to
the current E. A retired node is freed when no reserved interval meets its
lifetime [birth, retire].

This is the 2GEIBR variant of the paper only; the tagged and pointer-based
variants (TagIBR, POIBR) are not implemented.

Precondition: a process dereferences only nodes it got from protect()
inside an operation. Cost: a pointer read is 2 steps when E did not move.
A stopped process blocks only nodes born at or before its upper end.
"""

from __future__ import annotations

from typing import Any

from smr_sim import Gen, Memory, NoReclaim


class IntervalBased(NoReclaim):
    name = "ibr"

    def __init__(self, mem: Memory, n: int, R: int = 0, F: int = 2) -> None:
        super().__init__(mem, n)
        self.R = R if R > 0 else 2 * n
        self.F = F
        self.count = [0] * n
        self.upper = [None] * n
        self.lower = [None] * n
        self.rlist: list = [[] for _ in range(n)]
        mem.cells["ibr"] = {"E": 1, **{t: None for t in range(n)}}

    def setup(self) -> None:
        """Nodes of the initial state are born in epoch 1."""
        for a, c in self.mem.cells.items():
            if isinstance(a, int):
                c["birth"] = 1

    def alloc(self, t: int, fields: dict) -> Gen:
        """Every F-th allocation of a process moves E; the node is born in the epoch read after that."""
        self.count[t] += 1
        if self.count[t] % self.F == 0:
            yield ("faa", "ibr", "E", 1)
        e = yield ("read", "ibr", "E")
        return (yield ("alloc", {**fields, "birth": e}))

    def begin(self, t: int) -> Gen:
        e = yield ("read", "ibr", "E")  # @line L1
        yield ("write", "ibr", t, (e, e))  # @line L2
        self.lower[t] = self.upper[t] = e

    def protect(self, t: int, i: int, a: Any, f: str) -> Gen:
        """Read a.f, and raise the upper end until E is stable around the read."""
        while True:
            p = yield ("read", a, f)  # @line L3
            e = yield ("read", "ibr", "E")  # @line L4
            if e == self.upper[t]:  # @line L5
                return p
            yield ("write", "ibr", t, (self.lower[t], e))  # @line L6
            self.upper[t] = e

    def read(self, t: int, a: Any, f: str) -> Gen:
        if f == "next":
            return (yield from self.protect(t, 0, a, f))
        return (yield ("read", a, f))

    def end(self, t: int) -> Gen:
        yield ("write", "ibr", t, None)  # @line L7
        self.lower[t] = self.upper[t] = None

    def retire(self, t: int, a: int) -> Gen:
        self.mem.note_retire(a)
        e = yield ("read", "ibr", "E")  # @line L8
        self.rlist[t].append((a, self.mem.cells[a]["birth"], e))
        if len(self.rlist[t]) >= self.R:
            res = []
            for q in range(self.n):
                v = yield ("read", "ibr", q)  # @line L9
                if v is not None:
                    res.append(v)
            keep = []
            for a2, b, r in self.rlist[t]:
                if any(b <= u and r >= lo for lo, u in res):  # @line L10
                    keep.append((a2, b, r))
                else:
                    yield ("free", a2)  # @line L11
            self.rlist[t] = keep
