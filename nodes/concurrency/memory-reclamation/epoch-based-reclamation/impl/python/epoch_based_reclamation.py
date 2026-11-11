# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epoch-based-reclamation/. The authors are listed in prov/E1V1VX.jsonl.
"""Epoch-based reclamation (Fraser's scheme) on the simulator in smr_sim.py.

The static block "ebr" holds the global epoch G and one announcement per
process: None outside an operation, or the epoch that the process saw when
it started. A retired node is tagged with G, read after the unlink. The
epoch moves from e to e + 1 only when every active process has announced
e, and a node with tag r is freed once its owner sees G >= r + 2.

Precondition: a process holds references to nodes only inside
begin()..end(). Cost: begin and end are O(1) steps; an attempt to advance
reads n announcements. If a process stops inside an operation, the epoch
stops and the garbage grows without bound.

The parameter lag is 2 in the real scheme; lag = 1 is the classic bug of
freeing one epoch too early, kept for the tests.
"""

from __future__ import annotations

from smr_sim import Gen, Memory, NoReclaim


class EpochBased(NoReclaim):
    name = "ebr"

    def __init__(self, mem: Memory, n: int, R: int = 1, lag: int = 2) -> None:
        super().__init__(mem, n)
        self.R, self.lag = R, lag
        self.limbo: list = [[] for _ in range(n)]
        mem.cells["ebr"] = {"G": 0, **{t: None for t in range(n)}}

    def begin(self, t: int) -> Gen:
        """Announce the global epoch, and check that it did not move meanwhile."""
        while True:
            e = yield ("read", "ebr", "G")  # @line L1
            yield ("write", "ebr", t, e)  # @line L2
            if (yield ("read", "ebr", "G")) == e:  # @line L3
                return

    def end(self, t: int) -> Gen:
        yield ("write", "ebr", t, None)  # @line L4

    def retire(self, t: int, a: int) -> Gen:
        """Tag a with the epoch read after the unlink; try to advance and free."""
        self.mem.note_retire(a)
        r = yield ("read", "ebr", "G")  # @line L5
        self.limbo[t].append((a, r))
        if len(self.limbo[t]) >= self.R:
            g = yield from self.try_advance(t)
            keep = []
            for a2, r2 in self.limbo[t]:
                if g >= r2 + self.lag:  # @line L9
                    yield ("free", a2)  # @line L10
                else:
                    keep.append((a2, r2))
            self.limbo[t] = keep

    def try_advance(self, t: int) -> Gen:
        """Move G from e to e + 1 if every active process announced e. Returns the epoch seen."""
        e = yield ("read", "ebr", "G")  # @line L6
        for q in range(self.n):
            v = yield ("read", "ebr", q)  # @line L7
            if v is not None and v != e:
                return e
        if (yield ("cas", "ebr", "G", e, e + 1)):  # @line L8
            return e + 1
        return (yield ("read", "ebr", "G"))
