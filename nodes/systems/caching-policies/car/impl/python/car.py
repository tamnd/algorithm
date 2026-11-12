# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/car/. The authors are listed in prov/BEKWFB.jsonl.

from collections import OrderedDict, deque
from collections.abc import Hashable, Iterable
from fractions import Fraction


class CAR:
    """CLOCK with Adaptive Replacement of Bansal and Modha (FAST 2004), for c pages.

    T1 and T2 are clocks, kept as deques: the head (left end) is the page under
    the hand, and the tail (right end) is the page just behind the hand.
    B1 and B2 are LRU lists of keys only (OrderedDict, LRU first).
    """

    def __init__(self, c: int) -> None:
        if c < 1:
            raise ValueError("the cache size c must be at least 1")
        self.c = c
        self.p = Fraction(0)
        self.t1: deque[Hashable] = deque()
        self.t2: deque[Hashable] = deque()
        self.where: dict[Hashable, int] = {}  # 1 or 2 for a cached page
        self.ref: dict[Hashable, bool] = {}
        self.b1: OrderedDict[Hashable, None] = OrderedDict()
        self.b2: OrderedDict[Hashable, None] = OrderedDict()
        self.evicted: Hashable | None = None

    def __contains__(self, x: Hashable) -> bool:
        return x in self.where

    def __len__(self) -> int:
        return len(self.where)

    def access(self, x: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        c = self.c
        if x in self.where:  # @line L1
            self.ref[x] = True  # @line L2
            return True
        if len(self.t1) + len(self.t2) == c:  # @line L3
            self._replace()  # @line L4
            ghost = x in self.b1 or x in self.b2
            if not ghost and len(self.t1) + len(self.b1) == c:  # @line L5
                self.b1.popitem(last=False)  # @line L6
            elif not ghost and len(self.t1) + len(self.t2) + len(self.b1) + len(self.b2) == 2 * c:  # @line L7
                self.b2.popitem(last=False)  # @line L8
        if x not in self.b1 and x not in self.b2:  # @line L9
            self._put(x, self.t1, 1)  # @line L10
        elif x in self.b1:  # @line L11
            d = max(Fraction(1), Fraction(len(self.b2), len(self.b1)))
            self.p = min(self.p + d, Fraction(c))  # @line L12
            del self.b1[x]  # @line L13
            self._put(x, self.t2, 2)
        else:  # @line L14
            d = max(Fraction(1), Fraction(len(self.b1), len(self.b2)))
            self.p = max(self.p - d, Fraction(0))  # @line L15
            del self.b2[x]  # @line L16
            self._put(x, self.t2, 2)
        return False

    def _put(self, x: Hashable, clock: deque, k: int) -> None:
        clock.append(x)
        self.where[x] = k
        self.ref[x] = False

    def _replace(self) -> None:
        while True:  # @line L17
            if len(self.t1) >= max(1, self.p):  # @line L18
                y = self.t1.popleft()
                if not self.ref[y]:  # @line L19
                    self._drop(y)
                    self.b1[y] = None  # @line L20
                    return
                self.ref[y] = False  # @line L21
                self.t2.append(y)
                self.where[y] = 2
            else:  # @line L22
                y = self.t2.popleft()
                if not self.ref[y]:  # @line L23
                    self._drop(y)
                    self.b2[y] = None  # @line L24
                    return
                self.ref[y] = False  # @line L25
                self.t2.append(y)

    def _drop(self, y: Hashable) -> None:
        del self.where[y]
        del self.ref[y]
        self.evicted = y


def car_hits(trace: Iterable[Hashable], c: int) -> list[bool]:
    """Run CAR with c pages on the trace. Return one hit flag per request."""
    cache = CAR(c)
    return [cache.access(x) for x in trace]
