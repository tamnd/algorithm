# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-q-replacement/. The authors are listed in prov/VWYKNJ.jsonl.

from collections import OrderedDict
from typing import Hashable, List, Optional, Sequence, Tuple

Page = Hashable


class TwoQ:
    """The full 2Q buffer rule of Johnson and Shasha (1994).

    a1in: a FIFO queue of resident pages seen once recently.
    a1out: a FIFO queue of page identifiers only (no data) evicted from a1in.
    am: an LRU queue of resident pages seen again while in a1out.
    In each OrderedDict the head is the last entry and the tail is the first entry.
    c is the number of page slots, kin the threshold of a1in, kout the size of a1out.
    """

    def __init__(self, c: int, kin: int, kout: int) -> None:
        if c < 1 or kin < 0 or kout < 0 or kin >= c:
            raise ValueError("need c >= 1, kout >= 0 and 0 <= kin < c")
        self.c, self.kin, self.kout = c, kin, kout
        self.a1in: "OrderedDict[Page, None]" = OrderedDict()
        self.a1out: "OrderedDict[Page, None]" = OrderedDict()
        self.am: "OrderedDict[Page, None]" = OrderedDict()

    def resident(self) -> List[Page]:
        return list(self.a1in) + list(self.am)

    def reclaim(self) -> Optional[Page]:
        """Free one slot. Returns the page that is paged out, or None if a slot was free."""
        if len(self.a1in) + len(self.am) < self.c:  # @line L8
            return None
        if len(self.a1in) > self.kin:  # @line L9
            y, _ = self.a1in.popitem(last=False)
            self.a1out[y] = None
            if len(self.a1out) > self.kout:
                self.a1out.popitem(last=False)
            return y
        y, _ = self.am.popitem(last=False)  # @line L10
        return y

    def access(self, x: Page) -> Tuple[bool, Optional[Page]]:
        """Serve one access. Returns (hit, the page that was paged out or None)."""
        if x in self.am:  # @line L3
            self.am.move_to_end(x)
            return True, None
        if x in self.a1in:  # @line L4
            return True, None
        if x in self.a1out:  # @line L5
            del self.a1out[x]
            out = self.reclaim()
            self.am[x] = None
            return False, out
        out = self.reclaim()  # @line L6
        self.a1in[x] = None
        return False, out


def two_q_replacement(requests: Sequence[Page], c: int, kin: int, kout: int) -> Tuple[int, List[Tuple[Page, bool, Optional[Page]]]]:
    """Run 2Q on a request sequence. Returns (misses, log of (page, hit, paged out)).

    Each access takes O(1) expected time with hash-linked queues.
    """
    cache = TwoQ(c, kin, kout)
    misses = 0  # @line L1
    log = []
    for x in requests:  # @line L2
        hit, out = cache.access(x)
        misses += 0 if hit else 1
        log.append((x, hit, out))
    return misses, log  # @line L7
