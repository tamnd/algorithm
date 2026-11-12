# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc/. The authors are listed in prov/Z520JB.jsonl.

from collections import OrderedDict
from collections.abc import Hashable, Iterable
from fractions import Fraction


class ARC:
    """Adaptive Replacement Cache of Megiddo and Modha (FAST 2003), for c pages.

    T1 and T2 hold the cached pages, B1 and B2 hold only keys (ghosts).
    Each list is an OrderedDict with the LRU page first and the MRU page last.
    The target p for the size of T1 is kept as an exact Fraction.
    """

    def __init__(self, c: int) -> None:
        if c < 1:
            raise ValueError("the cache size c must be at least 1")
        self.c = c
        self.p = Fraction(0)
        self.t1: OrderedDict[Hashable, None] = OrderedDict()
        self.t2: OrderedDict[Hashable, None] = OrderedDict()
        self.b1: OrderedDict[Hashable, None] = OrderedDict()
        self.b2: OrderedDict[Hashable, None] = OrderedDict()
        self.evicted: Hashable | None = None

    def __contains__(self, x: Hashable) -> bool:
        return x in self.t1 or x in self.t2

    def __len__(self) -> int:
        return len(self.t1) + len(self.t2)

    def access(self, x: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        c = self.c
        if x in self.t1 or x in self.t2:  # @line L1
            if x in self.t1:  # @line L2
                del self.t1[x]
            else:
                del self.t2[x]
            self.t2[x] = None
            return True  # @line L3
        if x in self.b1:  # @line L4
            d = max(Fraction(len(self.b2), len(self.b1)), Fraction(1))
            self.p = min(Fraction(c), self.p + d)  # @line L5
            self._replace(x)  # @line L6
            del self.b1[x]  # @line L7
            self.t2[x] = None
            return False  # @line L8
        if x in self.b2:  # @line L9
            d = max(Fraction(len(self.b1), len(self.b2)), Fraction(1))
            self.p = max(Fraction(0), self.p - d)  # @line L10
            self._replace(x)  # @line L11
            del self.b2[x]  # @line L12
            self.t2[x] = None
            return False  # @line L13
        if len(self.t1) + len(self.b1) == c:  # @line L14
            if len(self.t1) < c:  # @line L15
                self.b1.popitem(last=False)  # @line L16
                self._replace(x)  # @line L17
            else:  # @line L18
                self.evicted, _ = self.t1.popitem(last=False)  # @line L19
        else:  # @line L20
            total = len(self.t1) + len(self.t2) + len(self.b1) + len(self.b2)
            if total >= c:  # @line L21
                if total == 2 * c:  # @line L22
                    self.b2.popitem(last=False)  # @line L23
                self._replace(x)  # @line L24
        self.t1[x] = None  # @line L25
        return False  # @line L26

    def _replace(self, x: Hashable) -> None:
        n1 = len(self.t1)
        if n1 >= 1 and (n1 > self.p or (x in self.b2 and n1 == self.p)):  # @line L27
            y, _ = self.t1.popitem(last=False)  # @line L28
            self.b1[y] = None
        else:  # @line L29
            y, _ = self.t2.popitem(last=False)  # @line L30
            self.b2[y] = None
        self.evicted = y


def arc_hits(trace: Iterable[Hashable], c: int) -> list[bool]:
    """Run ARC with c pages on the trace. Return one hit flag per request."""
    cache = ARC(c)
    return [cache.access(x) for x in trace]
