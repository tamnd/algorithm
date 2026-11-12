# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-reference-counting/. The authors are listed in prov/BYX9WD.jsonl.

"""Weighted reference counting (Bevan 1987, Watson and Watson 1987).

Each reference carries a weight, and each object keeps a total weight. The
invariant is: the total weight of x equals the sum of the weights of all
references to x plus the weights in the decrement messages for x that are
not yet delivered. COPY splits a weight and sends no message. DELETE sends
one message. A reference of weight 1 is copied through an indirection cell.
"""

from collections import deque


class Ref:
    __slots__ = ("target", "w")

    def __init__(self, target: int, w: int) -> None:
        self.target = target
        self.w = w


class WRCHeap:
    def __init__(self, max_weight: int = 1 << 16) -> None:
        assert max_weight >= 2 and max_weight & (max_weight - 1) == 0
        self.W = max_weight
        self.fields: dict[int, list[Ref | None]] = {}
        self.tw: dict[int, int] = {}
        self.indirect: set[int] = set()  # ids of indirection cells
        self.freed: set[int] = set()
        self.queue: deque[tuple[int, int]] = deque()  # DEC messages in flight
        self.messages = 0
        self.next_id = 1

    def _alloc(self, n: int) -> int:
        x = self.next_id
        self.next_id += 1
        self.fields[x] = [None] * n
        self.tw[x] = self.W
        return x

    def new(self, n: int) -> Ref:
        x = self._alloc(n)  # @line L1
        self.tw[x] = self.W  # @line L2
        return Ref(x, self.W)  # @line L3

    def copy(self, r: Ref) -> Ref:
        """Return a second reference to the same object. No message is sent."""
        if r.w == 1:  # @line L4
            c = self._alloc(1)  # @line L5
            self.indirect.add(c)
            self.fields[c][0] = Ref(r.target, 1)  # @line L6
            r.target, r.w = c, self.W  # @line L7
        h = r.w // 2  # @line L8
        r.w -= h  # @line L9
        return Ref(r.target, h)  # @line L10

    def delete(self, r: Ref) -> None:
        """Drop a reference: send its weight back to the owner of its target."""
        self.queue.append((r.target, r.w))  # @line L11
        self.messages += 1
        r.w = 0

    def deliver(self, k: int = 0) -> None:
        """Deliver the k-th message in flight; messages may arrive in any order."""
        x, w = self.queue[k]
        del self.queue[k]
        self.tw[x] -= w  # @line L12
        if self.tw[x] == 0:  # @line L13
            for s in self.fields[x]:  # @line L14
                if s is not None:
                    self.delete(s)
            del self.fields[x]  # @line L15
            del self.tw[x]
            self.indirect.discard(x)
            self.freed.add(x)

    def deliver_all(self) -> None:
        while self.queue:
            self.deliver()

    def store(self, p: int, i: int, r: Ref) -> None:
        """Move reference r into field i of object p; the old field is deleted."""
        old = self.fields[p][i]
        self.fields[p][i] = r
        if old is not None:
            self.delete(old)

    def deref(self, r: Ref) -> int:
        """The object that r denotes, after the chain of indirection cells."""
        x = r.target
        while x in self.indirect:
            x = self.fields[x][0].target  # type: ignore[union-attr]
        return x
