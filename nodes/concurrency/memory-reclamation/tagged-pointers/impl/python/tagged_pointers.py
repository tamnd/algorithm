# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tagged-pointers/. The authors are listed in prov/6NM0K3.jsonl.
"""A Treiber stack and a Michael and Scott queue with version tags, on smr_sim.py.

Every shared pointer word is a pair (pointer, tag) in two adjacent words,
read with one double-width load and changed with one double-width CAS.
Each successful CAS writes the new tag (tag + 1) mod 2^w. A CAS that read
(A, x) succeeds only if the word still holds (A, x), so a node A that was
removed, freed and put back in the meantime is caught, as long as the tag
did not wrap around to x. With w = None the tags are not used at all, and
the ABA problem shows.

Nodes are never returned to the system: they go to a type-stable free list
and are reused, so a stale read of a freed node is harmless. In the queue,
the tag of a node's next field lives on across reuse, as in the paper of
Michael and Scott, so that a stale CAS on the next field of a reused node
fails.

Precondition: nodes are reused only as nodes of the same structure. Cost:
one double-width load and one double-width CAS per try. A tag of w bits
fails when a word changes a multiple of 2^w times between the read and the
CAS of one operation.
"""

from __future__ import annotations

from typing import Any, Optional

from smr_sim import Gen, Memory, conserve, queue_values, stack_values


def bump(tag: int, w: Optional[int]) -> int:
    return 0 if w is None else (tag + 1) % (1 << w)


def push(v: Any, w: Optional[int]) -> Gen:
    node = yield ("alloc", {"val": v, "next": None})
    while True:
        top, tag = yield ("read2", "root", "top", "tag")
        yield ("write", node, "next", top)
        if (yield ("dcas", "root", "top", "tag", top, tag, node, bump(tag, w))):
            return


def pop(w: Optional[int]) -> Gen:
    while True:
        top, tag = yield ("read2", "root", "top", "tag")  # @line L1
        if top is None:  # @line L2
            return None
        nxt = yield ("read", top, "next")  # @line L3
        v = yield ("read", top, "val")
        new = bump(tag, w)  # @line L4
        if (yield ("dcas", "root", "top", "tag", top, tag, nxt, new)):  # @line L5
            yield ("free", top)  # @line L6
            return v


def enq(v: Any, w: Optional[int]) -> Gen:
    node = yield ("alloc", {"val": v, "next": None, "ntag": 0})  # a reused node keeps its ntag
    yield ("write", node, "next", None)
    while True:
        tl, tt = yield ("read2", "q", "tail", "ttag")
        nx, nt = yield ("read2", tl, "next", "ntag")
        if (yield ("read2", "q", "tail", "ttag")) != (tl, tt):
            continue
        if nx is None:
            if (yield ("dcas", tl, "next", "ntag", None, nt, node, bump(nt, w))):
                yield ("dcas", "q", "tail", "ttag", tl, tt, node, bump(tt, w))
                return
        else:
            yield ("dcas", "q", "tail", "ttag", tl, tt, nx, bump(tt, w))


def deq(w: Optional[int]) -> Gen:
    while True:
        hd, ht = yield ("read2", "q", "head", "htag")
        tl, tt = yield ("read2", "q", "tail", "ttag")
        nx, _ = yield ("read2", hd, "next", "ntag")
        if (yield ("read2", "q", "head", "htag")) != (hd, ht):
            continue
        if hd == tl:
            if nx is None:
                return None
            yield ("dcas", "q", "tail", "ttag", tl, tt, nx, bump(tt, w))
            continue
        v = yield ("read", nx, "val")
        if (yield ("dcas", "q", "head", "htag", hd, ht, nx, bump(ht, w))):
            yield ("free", hd)
            return v


def setup(programs: list, w: Optional[int], kind: str = "stack", initial: int = 2):
    """A make() for the explorer: a tagged stack or queue on a type-stable pool."""

    def make() -> tuple:
        m = Memory(type_stable=True, stable=("next", "ntag"))
        if kind == "stack":
            m.static("root", top=None, tag=0)
            for j in range(initial):
                m.cells["root"]["top"] = m.new(val=("init", j), next=m.cells["root"]["top"])
        else:
            d = m.new(val=None, next=None, ntag=0)
            m.static("q", head=d, htag=0, tail=d, ttag=0)
            for j in range(initial):
                a = m.new(val=("init", j), next=None, ntag=0)
                m.cells[m.cells["q"]["tail"]]["next"] = a
                m.cells["q"]["tail"] = a
        pushed = [("init", j) for j in range(initial)] + [op[1] for p in programs for op in p if op[0] in ("push", "enq")]

        def prog(ops: list) -> Gen:
            out = []
            for op in ops:
                if op[0] == "push":
                    yield from push(op[1], w)
                elif op[0] == "pop":
                    out.append((yield from pop(w)))
                elif op[0] == "enq":
                    yield from enq(op[1], w)
                else:
                    out.append((yield from deq(w)))
            return out

        def check(mm: Memory, rets: list) -> None:
            left = stack_values(mm) if kind == "stack" else queue_values(mm)
            conserve(pushed, [v for r in rets for v in r], left)

        return m, [prog(p) for p in programs], None, check

    return make
