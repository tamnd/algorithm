# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neutralization-based-reclamation/. The authors are listed in prov/A696BX.jsonl.
"""Neutralization-based reclamation, NBR (Singh, Brown and Mashtizadeh), on smr_sim.py.

An operation attempt has a read phase and a write phase. At the start of
the read phase a process clears its reservations and becomes restartable.
In the read phase a signal makes it restart from the root, so it drops
every reference it holds. Before the write phase it publishes reservations
for the nodes it will use, and only then stops being restartable. A
process whose retire list reaches R sends a signal to every other process,
then reads all reservations and frees every listed node that no
reservation names.

The simulator handles a signal before the next shared step of its target,
which is Assumption 4 of the paper: a signalled thread runs its handler
before it dereferences any record.

Precondition: the read phase only reads shared nodes (and its own new
node) and can restart at any step; the write phase uses only reserved
nodes. Cost: no extra step per read; a write per reservation; a
reclamation sends n - 1 signals and reads n * K slots. At most n * R
retired nodes are unfreed, even if some processes stop.
"""

from __future__ import annotations

from smr_sim import Gen, Memory, NoReclaim


class NBR(NoReclaim):
    name = "nbr"
    K = 2

    def __init__(self, mem: Memory, n: int, R: int = 0) -> None:
        super().__init__(mem, n)
        self.R = R if R > 0 else 2 * n * self.K
        self.rlist: list = [[] for _ in range(n)]
        self.phase = [False] * n
        self.mine: list = [[None] * self.K for _ in range(n)]
        mem.cells["sig"] = {t: False for t in range(n)}
        mem.cells["res"] = {(t, i): None for t in range(n) for i in range(self.K)}

    def restartable(self, t: int) -> bool:
        return self.phase[t]

    def attempt(self, t: int) -> Gen:
        """Begin the read phase: drop the old reservations, then become restartable."""
        for i in range(self.K):
            if self.mine[t][i] is not None:
                yield ("write", "res", (t, i), None)  # @line L1
                self.mine[t][i] = None
        self.phase[t] = True  # @line L2

    def before_write(self, t: int, ptrs: list) -> Gen:
        """End the read phase: reserve the nodes the write phase uses, then stop being restartable."""
        for i, p in enumerate(ptrs[: self.K]):
            yield ("write", "res", (t, i), p)  # @line L3
            self.mine[t][i] = p
        self.phase[t] = False  # @line L4

    def end(self, t: int) -> Gen:
        self.phase[t] = False
        return
        yield

    def retire(self, t: int, a: int) -> Gen:
        self.mem.note_retire(a)
        self.rlist[t].append(a)  # @line L5
        if len(self.rlist[t]) < self.R:
            return
        for q in range(self.n):
            if q != t:
                yield ("signal", q)  # @line L6
        held = set()
        for q in range(self.n):
            for i in range(self.K):
                r = yield ("read", "res", (q, i))  # @line L7
                if r is not None:
                    held.add(r)
        keep = []
        for a2 in self.rlist[t]:
            if a2 in held:
                keep.append(a2)
            else:
                yield ("free", a2)  # @line L8
        self.rlist[t] = keep
