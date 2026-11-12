# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lirs/. The authors are listed in prov/ESWX79.jsonl.

from collections import OrderedDict
from collections.abc import Hashable, Iterable


class LIRS:
    """LIRS of Jiang and Zhang (SIGMETRICS 2002) for a cache of c blocks.

    S is the LIRS stack and Q the stack of resident HIR blocks. Both are
    OrderedDicts with the bottom first and the top last. A block is resident
    if and only if it is LIR or it is in Q. Stack S has no size limit here,
    as in the paper's main description.
    """

    def __init__(self, c: int, lhirs: int | None = None) -> None:
        if lhirs is None:
            lhirs = max(1, c // 100)  # the paper uses 1% of the cache
        if lhirs < 1 or c - lhirs < 1:
            raise ValueError("need at least one LIR block and one HIR block")
        self.c = c
        self.lhirs = lhirs
        self.llirs = c - lhirs
        self.s: OrderedDict[Hashable, None] = OrderedDict()
        self.q: OrderedDict[Hashable, None] = OrderedDict()
        self.lir: set[Hashable] = set()
        self.evicted: Hashable | None = None

    def __contains__(self, x: Hashable) -> bool:
        return x in self.lir or x in self.q

    def __len__(self) -> int:
        return len(self.lir) + len(self.q)

    def access(self, x: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        if x in self.lir:  # @line L1
            self._top(x)  # @line L2
            self._prune()  # @line L3
            return True  # @line L4
        if x in self.q:  # @line L5
            if x in self.s:  # @line L6
                self._top(x)  # @line L7
                self.lir.add(x)
                del self.q[x]
                self._demote()  # @line L8
            else:  # @line L9
                self._top(x)  # @line L10
                self.q.move_to_end(x)
            return True  # @line L11
        if len(self.lir) < self.llirs:  # @line L12
            self._top(x)  # @line L13
            self.lir.add(x)
            return False
        if len(self) == self.c:  # @line L14
            self.evicted, _ = self.q.popitem(last=False)  # @line L15
        if x in self.s:  # @line L16
            self._top(x)  # @line L17
            self.lir.add(x)
            self._demote()  # @line L18
        else:  # @line L19
            self._top(x)  # @line L20
            self.q[x] = None
        return False  # @line L21

    def _top(self, x: Hashable) -> None:
        self.s[x] = None
        self.s.move_to_end(x)

    def _demote(self) -> None:
        y, _ = self.s.popitem(last=False)  # @line L22
        self.lir.remove(y)
        self.q[y] = None
        self._prune()  # @line L23

    def _prune(self) -> None:
        while self.s and next(iter(self.s)) not in self.lir:  # @line L24
            self.s.popitem(last=False)


def lirs_hits(trace: Iterable[Hashable], c: int, lhirs: int | None = None) -> list[bool]:
    """Run LIRS with c blocks on the trace. Return one hit flag per request."""
    cache = LIRS(c, lhirs)
    return [cache.access(x) for x in trace]
