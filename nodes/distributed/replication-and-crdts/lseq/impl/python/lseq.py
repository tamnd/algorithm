# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lseq/. The authors are listed in prov/DDRN05.jsonl.

"""LSEQ (Nedelec, Molli, Mostefaoui and Desmontils 2013), a sequence CRDT with dense identifiers.

Positions are lists of triples (digit, site, clock), as in Logoot, but the
base depends on the depth: with initial base 2^4, depth d has 2^(4 + d)
digits, so the base doubles at each new level (an exponential tree). The
first time a replica allocates at a depth it picks, with probability 1/2,
boundary+ (a digit at most `boundary` above the digit of p) or boundary-
(a digit at most `boundary` below the digit of q), and keeps that choice for
that depth. A delete removes the pair, so there are no tombstones.
Delivery must be causal, so a delete comes after its insert.
"""

import bisect
import random
from typing import Any

Triple = tuple[int, int, int]  # (digit, site, clock)
Pos = tuple[Triple, ...]


def base_at(i: int, b0: int = 4) -> int:
    """The number of digits at level i (0 based), that is at depth i + 1."""
    return 2 ** (b0 + i + 1)


class LSeq:
    """One LSEQ replica with site id site."""

    def __init__(self, site: int, boundary: int = 10, seed: int = 0) -> None:
        self.site, self.boundary = site, boundary
        self.clock = 0
        self.rng = random.Random(seed * 7919 + site)
        self.strategy: dict[int, bool] = {}  # depth -> True for boundary+, False for boundary-
        self.pos: list[Pos] = []
        self.val: dict[Pos, Any] = {}

    def alloc(self, p: Pos, q: Pos | None) -> Pos:
        """A new position strictly between p and q. q None means the end of the document."""
        out: list[Triple] = []
        bound = q is not None
        i = 0
        while True:
            pd = p[i][0] if i < len(p) else 0  # @line L1
            qd = q[i][0] if bound else base_at(i)  # @line L2
            if qd - pd - 1 >= 1:  # @line L3
                step = min(self.boundary, qd - pd - 1)  # @line L4
                if i not in self.strategy:  # @line L5
                    self.strategy[i] = self.rng.random() < 0.5
                if self.strategy[i]:  # @line L6
                    d = pd + self.rng.randint(1, step)
                else:
                    d = qd - self.rng.randint(1, step)  # @line L7
                out.append((d, self.site, self.clock))
                return tuple(out)
            if i < len(p):  # @line L8
                out.append(p[i])
                bound = bound and p[i] == q[i]
            elif qd == 0:
                out.append(q[i])
            else:
                out.append((0, self.site, self.clock))
                bound = False
            i += 1  # @line L9

    def local_insert(self, i: int, value: Any) -> tuple:
        p = self.pos[i - 1] if i > 0 else ()
        q = self.pos[i] if i < len(self.pos) else None
        self.clock += 1
        op = ("ins", self.alloc(p, q), value)
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
            assert all(0 <= t[0] < base_at(i) for i, t in enumerate(x))


def bits(x: Pos, b0: int = 4) -> int:
    """Bits of the digit path only (site and clock not counted)."""
    return sum(b0 + i + 1 for i in range(len(x)))
