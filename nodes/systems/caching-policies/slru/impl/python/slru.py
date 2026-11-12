# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slru/. The authors are listed in prov/1K8PDH.jsonl.

from collections import OrderedDict
from collections.abc import Hashable, Iterable


class SLRU:
    """Segmented LRU (Karedla, Love and Wherry 1994) on a cache of k pages.

    The probationary segment and the protected segment are LRU lists, kept as
    OrderedDicts with the LRU end first. The protected segment holds at most
    p pages, with 0 <= p < k. A miss enters the MRU end of the probationary
    segment, a hit moves the page to the MRU end of the protected segment, and
    the LRU page of a full protected segment drops back to the MRU end of the
    probationary segment. Victims come from the LRU end of the probationary
    segment.
    """

    def __init__(self, k: int, p: int) -> None:
        if k < 1 or not 0 <= p < k:
            raise ValueError("need k >= 1 and 0 <= p < k")
        self.k, self.p = k, p
        self.prob: OrderedDict[Hashable, None] = OrderedDict()
        self.prot: OrderedDict[Hashable, None] = OrderedDict()
        self.evicted: Hashable | None = None

    def __contains__(self, x: Hashable) -> bool:
        return x in self.prob or x in self.prot

    def __len__(self) -> int:
        return len(self.prob) + len(self.prot)

    def contents(self) -> set[Hashable]:
        return set(self.prob) | set(self.prot)

    def access(self, x: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        if x in self.prot:  # @line L1
            self.prot.move_to_end(x)  # @line L2
            return True
        if x in self.prob:  # @line L3
            del self.prob[x]  # @line L4
            self.prot[x] = None
            if len(self.prot) > self.p:  # @line L5
                y, _ = self.prot.popitem(last=False)  # @line L6
                self.prob[y] = None
            return True  # @line L7
        if len(self.prob) + len(self.prot) == self.k:  # @line L8
            self.evicted, _ = self.prob.popitem(last=False)  # @line L9
        self.prob[x] = None  # @line L10
        return False  # @line L11


def slru_hits(trace: Iterable[Hashable], k: int, p: int) -> list[bool]:
    """Run SLRU with k pages and a protected segment of at most p pages."""
    cache = SLRU(k, p)
    return [cache.access(x) for x in trace]
