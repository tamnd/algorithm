# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pass-the-buck/. The authors are listed in prov/HJDC4M.jsonl.
"""Pass the buck (Herlihy, Luchangco, Martin and Moir) on the simulator in smr_sim.py.

Each process owns K guards. A guard g has a post word POST[g] and a handoff
word HNDOFF[g], which holds a pair (value, version). PostGuard is one
write to POST[g]; the client then reads the source again, as with hazard
pointers. Liberate(S) takes a set of retired values and returns the subset
that no guard traps. For each guard: if the guard posts a value v of the
set, Liberate tries to put v into the handoff word of the guard with a CAS
that bumps the version; on success it removes v from the set and adds the
value it took out of the handoff word, if any. After three failed CAS
tries it moves on. A value left in a handoff word is not lost: the next
Liberate that sees the guard posting a different value takes it out again.

This follows Figure 9 of the TOCS 2005 paper, except that the guards are
assigned to processes once (K per process) instead of with HireGuard and
FireGuard.

Precondition: a value is given to Liberate only after it is unreachable,
and the client reads the source again after each PostGuard.
Cost: Liberate is wait free, with at most 3 CAS tries per guard, so O(G)
steps for G = n K guards, plus O(1) per value with a hash set.
"""

from __future__ import annotations

from typing import Any

from smr_sim import Gen, Memory, NoReclaim


class PassTheBuck(NoReclaim):
    name = "ptb"
    K = 2

    def __init__(self, mem: Memory, n: int, R: int = 0) -> None:
        super().__init__(mem, n)
        self.G = n * self.K
        self.R = R if R > 0 else 2 * self.G
        self.vs: list = [set() for _ in range(n)]
        mem.cells["ptb"] = {**{("P", g): None for g in range(self.G)}, **{("H", g): (None, 0) for g in range(self.G)}}

    def protect(self, t: int, i: int, a: Any, f: str) -> Gen:
        """Read a.f, post it in guard i of t, and read a.f again until it is unchanged."""
        g = t * self.K + i
        while True:
            p = yield ("read", a, f)
            yield ("write", "ptb", ("P", g), p)  # @line L1
            if (yield ("read", a, f)) == p:
                return p

    def end(self, t: int) -> Gen:
        for i in range(self.K):
            yield ("write", "ptb", ("P", t * self.K + i), None)

    def retire(self, t: int, a: int) -> Gen:
        self.mem.note_retire(a)
        self.vs[t].add(a)
        if len(self.vs[t]) >= self.R:
            free = yield from self.liberate(self.vs[t])
            for x in sorted(free):
                yield ("free", x)
            self.vs[t] = set()

    def liberate(self, vs: set) -> Gen:
        """Return the values of vs that no guard traps; trapped values are handed off."""
        for g in range(self.G):  # @line L2
            attempts = 0
            h = yield ("read", "ptb", ("H", g))  # @line L3
            v = yield ("read", "ptb", ("P", g))  # @line L4
            if v is not None and v in vs:  # @line L5
                while True:
                    if (yield ("cas", "ptb", ("H", g), h, (v, h[1] + 1))):  # @line L6
                        vs.discard(v)
                        if h[0] is not None:
                            vs.add(h[0])  # @line L7
                        break
                    attempts += 1
                    if attempts == 3:
                        break
                    h = yield ("read", "ptb", ("H", g))
                    if attempts == 2 and h[0] is not None:
                        break
                    if v != (yield ("read", "ptb", ("P", g))):  # @line L8
                        break
            elif h[0] is not None and h[0] != v:  # @line L9
                if (yield ("cas", "ptb", ("H", g), h, (None, h[1] + 1))):  # @line L10
                    vs.add(h[0])
        return vs  # @line L11
