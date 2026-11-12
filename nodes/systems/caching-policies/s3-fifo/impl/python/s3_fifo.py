# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/s3-fifo/. The authors are listed in prov/5D8W5S.jsonl.

from collections import OrderedDict
from collections.abc import Hashable, Iterable
from fractions import Fraction


class S3FIFO:
    """S3-FIFO of Yang, Zhang, Qiu, Yue and Rashmi (SOSP 2023), Algorithm 1.

    The cache holds c objects of size 1. S, M and G are FIFO queues kept as
    OrderedDicts with the tail (oldest) first and the head (newest) last.
    S gets the fraction `small` of the cache (10 percent in the paper), M
    the rest, and G holds as many keys as M can hold objects, rounded up.
    `move_at` is the frequency an object needs at the tail of S to move to
    M; Algorithm 1 tests freq > 1, so the default is 2.
    """

    def __init__(self, c: int, small: Fraction = Fraction(1, 10), move_at: int = 2) -> None:
        if c < 1 or not 0 < small < 1:
            raise ValueError("need c >= 1 and 0 < small < 1")
        self.c = c
        self.small = Fraction(small)
        self.move_at = move_at
        main = (1 - self.small) * c
        self.g_cap = max(1, -(-main.numerator // main.denominator))
        self.s: OrderedDict[Hashable, None] = OrderedDict()
        self.m: OrderedDict[Hashable, None] = OrderedDict()
        self.g: OrderedDict[Hashable, None] = OrderedDict()
        self.freq: dict[Hashable, int] = {}
        self.evicted: list[Hashable] = []

    def __contains__(self, x: Hashable) -> bool:
        return x in self.freq

    def __len__(self) -> int:
        return len(self.s) + len(self.m)

    def access(self, x: Hashable) -> bool:
        """Serve one request (read in Algorithm 1). Return True on a hit."""
        self.evicted = []
        if x in self.freq:  # @line L1
            self.freq[x] = min(self.freq[x] + 1, 3)  # @line L2
            return True
        self._insert(x)  # @line L3
        self.freq[x] = 0  # @line L4
        return False

    def _insert(self, x: Hashable) -> None:
        while len(self) >= self.c:  # @line L5
            self._evict()  # @line L6
        if x in self.g:  # @line L7
            del self.g[x]
            self.m[x] = None  # @line L8
        else:  # @line L9
            self.s[x] = None  # @line L10

    def _evict(self) -> None:
        if len(self.s) >= self.small * self.c:  # @line L11
            self._evict_s()  # @line L12
        else:  # @line L13
            self._evict_m()  # @line L14

    def _m_full(self) -> bool:
        # Read as "M holds more than its share" after the move.
        return len(self.m) > (1 - self.small) * self.c

    def _evict_s(self) -> None:
        while self.s:  # @line L15
            t = next(iter(self.s))  # @line L16
            del self.s[t]
            if self.freq[t] >= self.move_at:  # @line L17
                self.freq[t] = 0  # the access bits are cleared on the move
                self.m[t] = None  # @line L18
                if self._m_full():  # @line L19
                    self._evict_m()  # @line L20
            else:  # @line L21
                del self.freq[t]
                self.evicted.append(t)
                self.g[t] = None  # @line L22
                if len(self.g) > self.g_cap:
                    self.g.popitem(last=False)
                return  # @line L23

    def _evict_m(self) -> None:
        while self.m:  # @line L24
            t = next(iter(self.m))  # @line L25
            if self.freq[t] > 0:  # @line L26
                self.m.move_to_end(t)  # @line L27
                self.freq[t] -= 1
            else:  # @line L28
                del self.m[t]
                del self.freq[t]
                self.evicted.append(t)
                return  # @line L29


def s3_fifo_hits(trace: Iterable[Hashable], c: int, small: Fraction = Fraction(1, 10), move_at: int = 2) -> list[bool]:
    """Run S3-FIFO with c objects on the trace. Return one hit flag per request."""
    cache = S3FIFO(c, small, move_at)
    return [cache.access(x) for x in trace]
