# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quiescent-state-based-reclamation/. The authors are listed in prov/RNB9XT.jsonl.
"""Quiescent-state-based reclamation (QSBR) on the simulator in smr_sim.py.

The static block "qsbr" holds a global counter G and, for each process, the
value of G that the process saw at its last quiescent state. A process
announces a quiescent state only at a point where it holds no references,
here at the end of each operation. G moves from e to e + 1 only when every
process has announced e. A retired node is tagged with G, read after the
unlink, and is freed once its owner sees G >= tag + 2.

Precondition: a process holds no reference to a shared node across a call
of quiescent(). Cost: reads cost nothing extra; a quiescent state is two
steps; an attempt to advance reads n words. A process that never reaches a
quiescent state stops all reclamation.

The parameter lag is 2 in the real scheme; lag = 1 frees one period too
early and is kept for the tests.
"""

from __future__ import annotations

from smr_sim import Gen, Memory, NoReclaim


class QSBR(NoReclaim):
    name = "qsbr"

    def __init__(self, mem: Memory, n: int, R: int = 1, lag: int = 2) -> None:
        super().__init__(mem, n)
        self.R, self.lag = R, lag
        self.limbo: list = [[] for _ in range(n)]
        mem.cells["qsbr"] = {"G": 0, **{t: 0 for t in range(n)}}

    def quiescent(self, t: int) -> Gen:
        """Announce that this process holds no references now."""
        e = yield ("read", "qsbr", "G")  # @line L1
        yield ("write", "qsbr", t, e)  # @line L2

    def end(self, t: int) -> Gen:
        yield from self.quiescent(t)

    def retire(self, t: int, a: int) -> Gen:
        """Tag a with G read after the unlink; try to advance G and free old nodes."""
        self.mem.note_retire(a)
        r = yield ("read", "qsbr", "G")  # @line L3
        self.limbo[t].append((a, r))
        if len(self.limbo[t]) >= self.R:
            g = yield from self.try_advance(t)
            keep = []
            for a2, r2 in self.limbo[t]:
                if g >= r2 + self.lag:  # @line L7
                    yield ("free", a2)  # @line L8
                else:
                    keep.append((a2, r2))
            self.limbo[t] = keep

    def try_advance(self, t: int) -> Gen:
        """Move G from e to e + 1 if every process announced e. Returns the counter seen."""
        e = yield ("read", "qsbr", "G")  # @line L4
        for q in range(self.n):
            if (yield ("read", "qsbr", q)) != e:  # @line L5
                return e
        if (yield ("cas", "qsbr", "G", e, e + 1)):  # @line L6
            return e + 1
        return (yield ("read", "qsbr", "G"))
