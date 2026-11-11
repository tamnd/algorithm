# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hazard-eras/. The authors are listed in prov/D8CRRV.jsonl.
"""Hazard eras (Ramalhete and Correia) on the simulator in smr_sim.py.

A global era clock counts retirements. Each node records the era of its
allocation (birth) and of its retirement. A reader publishes the current
era in a slot instead of the pointer itself; it re-publishes only when the
clock has moved since its last read. A retired node is freed when no
published era e has birth <= e <= retire.

Precondition: a process dereferences only nodes it got from protect().
Cost: protect is 2 steps when the era did not change. A scan reads n*K
slots. A stopped process blocks only nodes that were alive in the eras it
published, so with a retire list threshold R the garbage is at most
n * R + n * K * L, where L is the largest number of nodes whose life
interval [birth, retire] contains one era.
"""

from __future__ import annotations

from typing import Any

from smr_sim import Gen, Memory, NoReclaim


class HazardEras(NoReclaim):
    name = "he"
    K = 2

    def __init__(self, mem: Memory, n: int, R: int = 0) -> None:
        super().__init__(mem, n)
        self.R = R if R > 0 else 2 * n * self.K
        self.rlist: list = [[] for _ in range(n)]
        self.local = [[None] * self.K for _ in range(n)]
        mem.cells["he"] = {"clock": 1, **{(t, i): None for t in range(n) for i in range(self.K)}}

    def setup(self) -> None:
        """Nodes of the initial state are born in era 1."""
        for a, c in self.mem.cells.items():
            if isinstance(a, int):
                c["birth"] = 1

    def alloc(self, t: int, fields: dict) -> Gen:
        e = yield ("read", "he", "clock")
        return (yield ("alloc", {**fields, "birth": e}))

    def protect(self, t: int, i: int, a: Any, f: str) -> Gen:
        """Read a.f; publish the clock in slot i until the clock is stable around the read."""
        prev = self.local[t][i]
        while True:
            p = yield ("read", a, f)  # @line L1
            e = yield ("read", "he", "clock")  # @line L2
            if e == prev:  # @line L3
                return p
            yield ("write", "he", (t, i), e)  # @line L4
            self.local[t][i] = prev = e

    def retire(self, t: int, a: int) -> Gen:
        """Stamp the retire era, move the clock on, and scan when the list is long."""
        self.mem.note_retire(a)
        e = yield ("read", "he", "clock")  # @line L5
        self.rlist[t].append((a, self.mem.cells[a]["birth"], e))
        yield ("cas", "he", "clock", e, e + 1)  # @line L6
        if len(self.rlist[t]) >= self.R:
            yield from self.scan(t)

    def scan(self, t: int) -> Gen:
        eras = []
        for q in range(self.n):
            for i in range(self.K):
                h = yield ("read", "he", (q, i))  # @line L7
                if h is not None:
                    eras.append(h)
        keep = []
        for a, b, r in self.rlist[t]:
            if any(b <= h <= r for h in eras):  # @line L8
                keep.append((a, b, r))
            else:
                yield ("free", a)  # @line L9
        self.rlist[t] = keep

    def end(self, t: int) -> Gen:
        for i in range(self.K):
            yield ("write", "he", (t, i), None)  # @line L10
            self.local[t][i] = None
