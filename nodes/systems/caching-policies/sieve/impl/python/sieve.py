# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sieve/. The authors are listed in prov/JP6T1M.jsonl.

from collections.abc import Hashable, Iterable


class Sieve:
    """SIEVE of Zhang, Yang, Yue, Vigfusson and Rashmi (NSDI 2024), Algorithm 1.

    One FIFO queue, kept as a doubly linked list in two dicts. The head is the
    newest object and the tail the oldest. `prev[x]` is the next newer object
    (toward the head) and `nxt[x]` the next older one (toward the tail), as in
    the paper. The hand moves from the tail toward the head.
    """

    def __init__(self, c: int) -> None:
        if c < 1:
            raise ValueError("the cache size must be at least 1")
        self.c = c
        self.visited: dict[Hashable, bool] = {}
        self.prev: dict[Hashable, Hashable | None] = {}
        self.nxt: dict[Hashable, Hashable | None] = {}
        self.head: Hashable | None = None
        self.tail: Hashable | None = None
        self.hand: Hashable | None = None
        self.evicted: Hashable | None = None

    def __contains__(self, x: Hashable) -> bool:
        return x in self.visited

    def __len__(self) -> int:
        return len(self.visited)

    def order(self) -> list[Hashable]:
        """The queue from the tail (oldest) to the head (newest)."""
        out, x = [], self.tail
        while x is not None:
            out.append(x)
            x = self.prev[x]
        return out

    def access(self, x: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        if x in self.visited:  # @line L1
            self.visited[x] = True  # @line L2
            return True
        return self._miss(x)  # @line L3

    def _miss(self, x: Hashable) -> bool:
        if len(self) == self.c:  # @line L4
            o = self.hand  # @line L5
            if o is None:  # @line L6
                o = self.tail  # @line L7
            while self.visited[o]:  # @line L8
                self.visited[o] = False  # @line L9
                o = self.prev[o]  # @line L10
                if o is None:  # @line L11
                    o = self.tail  # @line L12
            self.hand = self.prev[o]  # @line L13
            self._unlink(o)  # @line L14
            self.evicted = o
        self._push_head(x)  # @line L15
        self.visited[x] = False  # @line L16
        return False

    def _push_head(self, x: Hashable) -> None:
        self.prev[x] = None
        self.nxt[x] = self.head
        if self.head is not None:
            self.prev[self.head] = x
        self.head = x
        if self.tail is None:
            self.tail = x

    def _unlink(self, o: Hashable) -> None:
        p, n = self.prev.pop(o), self.nxt.pop(o)
        del self.visited[o]
        if p is None:
            self.head = n
        else:
            self.nxt[p] = n
        if n is None:
            self.tail = p
        else:
            self.prev[n] = p


def sieve_hits(trace: Iterable[Hashable], c: int) -> list[bool]:
    """Run SIEVE with c objects on the trace. Return one hit flag per request."""
    cache = Sieve(c)
    return [cache.access(x) for x in trace]
