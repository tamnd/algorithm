# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-q/. The authors are listed in prov/RTRVA7.jsonl.

from collections import OrderedDict
from collections.abc import Hashable, Iterable


class TwoQ:
    """Full 2Q of Johnson and Shasha (1994) on a buffer of k pages.

    A1in is a FIFO queue of resident pages seen once, Am an LRU queue of
    resident pages seen again, and A1out a FIFO queue of at most kout page
    identifiers paged out of A1in, with no data. Each OrderedDict keeps its
    oldest entry first, so the tail of a queue in the paper is the first key.
    """

    def __init__(self, k: int, kin: int, kout: int) -> None:
        if k < 1:
            raise ValueError("the buffer size k must be at least 1")
        if not 0 <= kin < k or kout < 0:
            raise ValueError("need 0 <= kin < k and kout >= 0")
        self.k, self.kin, self.kout = k, kin, kout
        self.a1in: OrderedDict[Hashable, None] = OrderedDict()
        self.a1out: OrderedDict[Hashable, None] = OrderedDict()
        self.am: OrderedDict[Hashable, None] = OrderedDict()
        self.evicted: Hashable | None = None

    def __contains__(self, p: Hashable) -> bool:
        return p in self.am or p in self.a1in

    def __len__(self) -> int:
        return len(self.am) + len(self.a1in)

    def contents(self) -> set[Hashable]:
        return set(self.am) | set(self.a1in)

    def _reclaim(self) -> None:
        if len(self.a1in) + len(self.am) < self.k:  # @line L10
            return
        if len(self.a1in) > self.kin:  # @line L11
            y, _ = self.a1in.popitem(last=False)  # @line L12
            if self.kout > 0:
                self.a1out[y] = None  # @line L13
                if len(self.a1out) > self.kout:
                    self.a1out.popitem(last=False)  # @line L14
        else:
            y, _ = self.am.popitem(last=False)  # @line L15
        self.evicted = y

    def access(self, p: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        if p in self.am:  # @line L1
            self.am.move_to_end(p)  # @line L2
            return True
        if p in self.a1in:  # @line L3
            return True  # @line L4
        if p in self.a1out:  # @line L5
            del self.a1out[p]
            self._reclaim()  # @line L6
            self.am[p] = None  # @line L7
            return False
        self._reclaim()  # @line L8
        self.a1in[p] = None  # @line L9
        return False


class SimplifiedTwoQ:
    """Simplified 2Q: a FIFO queue A1 and an LRU queue Am, both resident.

    A hit in A1 moves the page to Am at once. A miss puts the page in A1, and
    frees a slot from A1 if A1 holds more than threshold pages, else from Am.
    """

    def __init__(self, k: int, threshold: int) -> None:
        if k < 1 or not 0 <= threshold < k:
            raise ValueError("need k >= 1 and 0 <= threshold < k")
        self.k, self.threshold = k, threshold
        self.a1: OrderedDict[Hashable, None] = OrderedDict()
        self.am: OrderedDict[Hashable, None] = OrderedDict()
        self.evicted: Hashable | None = None

    def __contains__(self, p: Hashable) -> bool:
        return p in self.am or p in self.a1

    def __len__(self) -> int:
        return len(self.am) + len(self.a1)

    def access(self, p: Hashable) -> bool:
        self.evicted = None
        if p in self.am:
            self.am.move_to_end(p)
            return True
        if p in self.a1:
            del self.a1[p]
            self.am[p] = None
            return True
        if len(self.a1) + len(self.am) == self.k:
            if len(self.a1) > self.threshold:
                self.evicted, _ = self.a1.popitem(last=False)
            else:
                self.evicted, _ = self.am.popitem(last=False)
        self.a1[p] = None
        return False


def two_q_hits(trace: Iterable[Hashable], k: int, kin: int, kout: int) -> list[bool]:
    """Run full 2Q with a buffer of k pages on the trace. Return one hit flag per request."""
    cache = TwoQ(k, kin, kout)
    return [cache.access(p) for p in trace]
