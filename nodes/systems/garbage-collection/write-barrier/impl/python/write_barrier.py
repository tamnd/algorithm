# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-barrier/. The authors are listed in prov/YR5TKX.jsonl.

"""A write barrier and five of its uses, on one small heap model.

Every pointer store o.f[i] <- v goes through write(). The barrier has a part
that runs before the store (it sees the overwritten value u) and a part that
runs after it (it sees the new value v). The kinds are:

  "generational"  record (o, i) in a remembered set if o is old and v young
  "card"          mark the card of the slot dirty, with no test
  "incremental"   during marking, shade v if it is white (Dijkstra et al.)
  "snapshot"      during marking, shade u if it is white (Yuasa)
  "refcount"      increment the count of v, then decrement the count of u
  "none"          no barrier, to show what goes wrong

The heap also has an incremental tri-color marker that runs in steps between
mutator operations, so that the two marking barriers can be tested.
"""

from typing import Optional

WHITE, GRAY, BLACK = 0, 1, 2
KINDS = ("generational", "card", "incremental", "snapshot", "refcount", "none")


class Heap:
    def __init__(self, kind: str, card_shift: int = 2) -> None:
        if kind not in KINDS:
            raise ValueError("unknown barrier kind")
        self.kind = kind
        self.fields: dict[int, list[Optional[int]]] = {}
        self.roots: list[Optional[int]] = []
        self.next_id = 0
        # generational and card state
        self.old: set[int] = set()
        self.remset: set[tuple[int, int]] = set()
        self.card_shift = card_shift
        self.dirty: set[int] = set()
        # reference counts (heap references only)
        self.rc: dict[int, int] = {}
        # marking state
        self.marking = False
        self.color: dict[int, int] = {}
        self.gray: list[int] = []
        self.freed: set[int] = set()

    # ---- the barrier ---------------------------------------------------
    def address(self, o: int, i: int) -> int:
        return 16 * o + 1 + i  # each object owns 16 words of a flat address space

    def write(self, o: int, i: int, v: Optional[int]) -> None:
        """The store o.f[i] <- v with the barrier of this heap's kind."""
        u = self.fields[o][i]  # @line L1
        self.before(o, i, u, v)  # @line L2
        self.fields[o][i] = v  # @line L3
        self.after(o, i, u, v)  # @line L4

    def before(self, o: int, i: int, u: Optional[int], v: Optional[int]) -> None:
        if self.kind == "snapshot" and self.marking and u is not None:  # @line L8
            self.shade(u)
        if self.kind == "refcount" and v is not None:  # @line L9
            self.rc[v] += 1

    def after(self, o: int, i: int, u: Optional[int], v: Optional[int]) -> None:
        if self.kind == "generational":  # @line L5
            if o in self.old and v is not None and v not in self.old:
                self.remset.add((o, i))
        elif self.kind == "card":  # @line L6
            self.dirty.add(self.address(o, i) >> self.card_shift)
        elif self.kind == "incremental":  # @line L7
            if self.marking and v is not None:
                self.shade(v)
        elif self.kind == "refcount" and u is not None:  # @line L10
            self.rc[u] -= 1
            if self.rc[u] == 0 and not self.rooted(u):
                self.release(u)

    # ---- the mutator ---------------------------------------------------
    def alloc(self, nfields: int, old: bool = False) -> int:
        o = self.next_id
        self.next_id += 1
        self.fields[o] = [None] * nfields
        self.rc[o] = 0
        self.color[o] = BLACK if self.marking else WHITE  # allocate black during marking
        if old:
            self.old.add(o)
        self.roots.append(o)
        return o

    def rooted(self, o: int) -> bool:
        return o in self.roots

    def release(self, o: int) -> None:
        """Reference counting: free o and decrement its children (explicit stack)."""
        stack = [o]
        while stack:
            x = stack.pop()
            if x not in self.fields:
                continue
            for t in self.fields.pop(x):
                if t is not None and t in self.rc:
                    self.rc[t] -= 1
                    if self.rc[t] == 0 and not self.rooted(t):
                        stack.append(t)
            del self.rc[x]
            self.freed.add(x)

    # ---- an incremental tri-color marker -------------------------------
    def shade(self, o: int) -> None:
        if self.color.get(o) == WHITE:
            self.color[o] = GRAY
            self.gray.append(o)

    def start_marking(self) -> None:
        self.marking = True
        for o in self.fields:
            self.color[o] = WHITE
        for r in self.roots:
            if r is not None:
                self.shade(r)

    def mark_step(self) -> None:
        if self.gray:
            o = self.gray.pop()
            for t in self.fields[o]:
                if t is not None:
                    self.shade(t)
            self.color[o] = BLACK

    def finish_marking(self) -> set[int]:
        """Finish the mark, sweep the white objects and return them.

        Incremental update (and no barrier) rescans the roots here, because
        root updates have no barrier. A snapshot barrier does not need it:
        the roots were shaded at the start."""
        if self.kind != "snapshot":
            for r in self.roots:
                if r is not None:
                    self.shade(r)
        while self.gray:
            self.mark_step()
        dead = {o for o in self.fields if self.color[o] == WHITE}
        for o in dead:
            del self.fields[o]
        self.freed |= dead
        self.marking = False
        return dead
