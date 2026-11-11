# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/drop-the-anchor/. The authors are listed in prov/M2X7MT.jsonl.
"""A simplified anchor scheme, after Braginsky, Kogan and Petrank, on smr_sim.py.

A traversal publishes an anchor only once every K nodes, instead of a
hazard pointer for every node. An anchor guards the node it names and the
K nodes that follow it. When the traversal reaches the K-th node after its
anchor, it publishes that node as the new anchor and checks that the node
is still in the structure; if not, it starts again from the head.

This is a simplified version. On the Michael and Scott queue, each node has
a sequence number, one more than its predecessor, and the queue keeps the
sequence numbers of the head and the tail next to the head and tail
pointers (double-width words). An anchor is a sequence number s, and it
guards the nodes with numbers s to s + K, so a reclaimer never follows
pointers from an anchor. On the Treiber stack, a pop reads only the top
node, so the anchor names that node by its address, as a hazard pointer
does. The paper works on the Harris and Michael linked list and adds
freezing, timestamps and a recovery for the anchor of a stuck thread.
Those parts are not here.

Precondition: on the queue, nodes leave only at the head. Cost: one anchor
write and one check per K nodes of a traversal; a scan reads n anchors. At
most n * R retired nodes are unfreed, even if some processes stop, because
an anchor guards at most K + 1 nodes and R > n (K + 1).
"""

from __future__ import annotations

from typing import Any, Optional

from smr_sim import Gen, Memory, NoReclaim, conserve, queue_values


class Anchors(NoReclaim):
    name = "dta"

    def __init__(self, mem: Memory, n: int, K: int = 2, R: int = 0, validate: bool = True) -> None:
        super().__init__(mem, n)
        self.K, self.validate = K, validate
        self.R = R if R > 0 else 2 * n * (K + 1)
        self.rlist: list = [[] for _ in range(n)]
        mem.cells["anc"] = {t: None for t in range(n)}

    # ------------------------------------------------------------ the stack
    def protect(self, t: int, i: int, a: Any, f: str) -> Gen:
        """Stack: anchor the node read from a.f by its address, and check it again."""
        while True:
            p = yield ("read", a, f)
            yield ("write", "anc", t, ("node", p))
            if not self.validate or (yield ("read", a, f)) == p:
                return p

    def end(self, t: int) -> Gen:
        yield ("write", "anc", t, None)

    # ------------------------------------------------------------ the queue
    def anchor_end(self, t: int, ptr: str, seq: str) -> Gen:
        """Anchor at the head or the tail of the queue. Returns (node, its sequence number)."""
        while True:
            h, s = yield ("read2", "q", ptr, seq)
            yield ("write", "anc", t, ("seq", s))
            if (yield ("read2", "q", ptr, seq)) == (h, s):
                return h, s

    def find(self, t: int, v: Any) -> Gen:
        """Walk the queue from the head and report whether v is in it."""
        while True:
            x, _ = yield from self.anchor_end(t, "head", "hseq")  # @line L1
            hops, found = 0, None
            while found is None:
                if (yield ("read", x, "val")) == v:
                    found = True
                    break
                y = yield ("read", x, "next")  # @line L2
                if y is None:
                    found = False
                    break
                hops += 1  # @line L3
                if hops == self.K:  # @line L4
                    ys = yield ("read", y, "seq")
                    yield ("write", "anc", t, ("seq", ys))  # @line L5
                    if self.validate and (yield ("read", "q", "hseq")) > ys:  # @line L6
                        break
                    hops = 0
                x = y  # @line L7
            if found is not None:
                yield ("write", "anc", t, None)
                return found

    # ------------------------------------------------------------ reclamation
    def retire(self, t: int, a: int, s: Optional[int] = None) -> Gen:
        """Put a (with its sequence number s on the queue) in the private list; scan at R nodes."""
        self.mem.note_retire(a)
        self.rlist[t].append((a, s))
        if len(self.rlist[t]) < self.R:
            return
        anchors = []
        for q in range(self.n):
            an = yield ("read", "anc", q)  # @line L8
            if an is not None:
                anchors.append(an)
        keep = []
        for x, sx in self.rlist[t]:
            if any(self.guards(an, x, sx) for an in anchors):  # @line L9
                keep.append((x, sx))
            else:
                yield ("free", x)  # @line L10
        self.rlist[t] = keep

    def guards(self, an: tuple, x: int, sx: Optional[int]) -> bool:
        if an[0] == "node":
            return an[1] == x
        return sx is not None and an[1] <= sx <= an[1] + self.K


def enq(S: Anchors, t: int, v: Any) -> Gen:
    node = yield ("alloc", {"val": v, "next": None, "seq": 0})
    while True:
        tl, ts = yield from S.anchor_end(t, "tail", "tseq")
        nx = yield ("read", tl, "next")
        if nx is None:
            yield ("write", node, "seq", ts + 1)
            if (yield ("cas", tl, "next", None, node)):
                yield ("dcas", "q", "tail", "tseq", tl, ts, node, ts + 1)
                break
        else:
            yield ("dcas", "q", "tail", "tseq", tl, ts, nx, ts + 1)
    yield ("write", "anc", t, None)


def deq(S: Anchors, t: int) -> Gen:
    while True:
        h, s = yield from S.anchor_end(t, "head", "hseq")
        tl, ts = yield ("read2", "q", "tail", "tseq")
        nx = yield ("read", h, "next")  # nx has number s + 1, which the anchor guards
        if nx is None:
            v = None
            break
        if h == tl:
            yield ("dcas", "q", "tail", "tseq", tl, ts, nx, ts + 1)
            continue
        v = yield ("read", nx, "val")
        if (yield ("dcas", "q", "head", "hseq", h, s, nx, s + 1)):
            yield ("write", "anc", t, None)
            yield from S.retire(t, h, s)
            return v
    yield ("write", "anc", t, None)
    return v


def setup(programs: list, K: int = 2, R: int = 0, initial: int = 2, validate: bool = True):
    """A make() for the explorer: ("enq", v), ("deq",) and ("find", v) on a queue."""

    def make() -> tuple:
        m = Memory()
        n = len(programs)
        S = Anchors(m, n, K, R, validate)
        d = m.new(val=None, next=None, seq=0)
        m.static("q", head=d, hseq=0, tail=d, tseq=0)
        for j in range(initial):
            tl = m.cells["q"]["tail"]
            a = m.new(val=("init", j), next=None, seq=j + 1)
            m.cells[tl]["next"] = a
            m.cells["q"]["tail"], m.cells["q"]["tseq"] = a, j + 1
        pushed = [("init", j) for j in range(initial)] + [op[1] for p in programs for op in p if op[0] == "enq"]

        def prog(t: int, ops: list) -> Gen:
            out = []
            for op in ops:
                if op[0] == "enq":
                    yield from enq(S, t, op[1])
                elif op[0] == "deq":
                    out.append((yield from deq(S, t)))
                else:
                    yield from S.find(t, op[1])
            return out

        def check(mm: Memory, rets: list) -> None:
            conserve(pushed, [v for r in rets for v in r], queue_values(mm))

        return m, [prog(t, p) for t, p in enumerate(programs)], S, check

    return make
