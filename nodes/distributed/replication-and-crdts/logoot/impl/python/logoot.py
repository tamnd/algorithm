# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logoot/. The authors are listed in prov/AHQMT3.jsonl.

"""Logoot (Weiss, Urso and Molli 2009), a sequence CRDT with dense identifiers.

Each element has a position: a list of triples (digit, site, clock) with
digits in [0, base). Positions are compared as lists, so they form a dense
total order: between any two positions there is room for a new one, at the
price of a longer list. The document is the set of (position, value) pairs
sorted by position. A delete removes the pair, so there are no tombstones.

alloc walks down the levels of p and q. At the first level with a free digit
between them it picks one with the boundary strategy: at most `boundary`
above the digit of p. At a level with no room it copies the triple of p (or
of q, when p has run out and the digit of q is 0) and goes one level deeper.
The new triple carries the site and clock of the replica, which makes the
position unique. Delivery must be causal, so a delete comes after its insert.
"""

import bisect
import random
from typing import Any

Triple = tuple[int, int, int]  # (digit, site, clock)
Pos = tuple[Triple, ...]


def alloc(p: Pos, q: Pos | None, base: int, boundary: int, site: int, clock: int, rng: random.Random) -> Pos:
    """A new position strictly between p and q. q None means the end of the document."""
    out: list[Triple] = []
    bound = q is not None  # the new prefix still equals the prefix of q
    i = 0
    while True:
        pd = p[i][0] if i < len(p) else 0  # @line L1
        qd = q[i][0] if bound else base  # @line L2
        if qd - pd - 1 >= 1:  # @line L3
            step = min(boundary, qd - pd - 1)  # @line L4
            out.append((pd + rng.randint(1, step), site, clock))  # @line L5
            return tuple(out)
        if i < len(p):  # @line L6
            out.append(p[i])
            bound = bound and p[i] == q[i]
        elif qd == 0:  # @line L7
            out.append(q[i])
        else:
            out.append((0, site, clock))  # @line L8
            bound = False
        i += 1  # @line L9


class Logoot:
    """One Logoot replica with site id site."""

    def __init__(self, site: int, base: int = 2**10, boundary: int = 10, seed: int = 0) -> None:
        self.site, self.base, self.boundary = site, base, boundary
        self.clock = 0
        self.rng = random.Random(seed * 7919 + site)
        self.pos: list[Pos] = []
        self.val: dict[Pos, Any] = {}

    def local_insert(self, i: int, value: Any) -> tuple:
        p = self.pos[i - 1] if i > 0 else ()
        q = self.pos[i] if i < len(self.pos) else None
        self.clock += 1
        x = alloc(p, q, self.base, self.boundary, self.site, self.clock, self.rng)
        op = ("ins", x, value)
        self.apply(op)
        return op

    def local_delete(self, i: int) -> tuple:
        op = ("del", self.pos[i])
        self.apply(op)
        return op

    def apply(self, op: tuple) -> None:
        if op[0] == "ins":
            _, x, value = op
            if x not in self.val:
                bisect.insort(self.pos, x)
                self.val[x] = value
        else:
            x = op[1]
            if x in self.val:
                del self.val[x]
                self.pos.pop(bisect.bisect_left(self.pos, x))

    def value(self) -> list[Any]:
        return [self.val[x] for x in self.pos]

    def order(self) -> list[Pos]:
        return list(self.pos)

    def check_invariant(self) -> None:
        assert all(a < b for a, b in zip(self.pos, self.pos[1:]))
        assert len(self.pos) == len(self.val)
        for x in self.pos:
            assert x[-1][0] >= 1, "a position never ends with digit 0"
            assert all(0 <= t[0] < self.base for t in x)
