# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-stacks-queue/. The authors are listed in prov/69X9SB.jsonl.

from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class TwoStacksQueue(Generic[T]):
    """A FIFO window with an aggregate query over a monoid (op, identity).

    The front stack holds pairs (v_i, v_i op ... op v_f), oldest item on top.
    The back stack holds the newer values, and back_agg is their aggregate.
    insert and query use exactly one call of op. evict uses no call of op,
    except when the front stack is empty: then it moves the back stack and
    makes one call per moved item. op must be associative; it need not be
    commutative or invertible.
    """

    def __init__(self, op: Callable[[T, T], T], identity: T) -> None:
        self.op = op
        self.e = identity
        self.front: list[tuple[T, T]] = []
        self.back: list[T] = []
        self.back_agg: T = identity

    def __len__(self) -> int:
        return len(self.front) + len(self.back)

    def insert(self, v: T) -> None:
        """Add v as the newest item of the window."""
        self.back.append(v)  # @line L1
        self.back_agg = self.op(self.back_agg, v)  # @line L2

    def evict(self) -> T:
        """Remove and return the oldest item. Precondition: not empty."""
        if len(self) == 0:
            raise IndexError("evict from an empty window")
        if not self.front:  # @line L3
            a = self.e  # @line L4
            while self.back:  # @line L5
                v = self.back.pop()  # @line L6
                a = self.op(v, a)  # @line L7
                self.front.append((v, a))  # @line L8
            self.back_agg = self.e  # @line L9
        return self.front.pop()[0]  # @line L10

    def query(self) -> T:
        """Return v_1 op v_2 op ... op v_n, oldest first, or the identity."""
        fa = self.front[-1][1] if self.front else self.e  # @line L11
        return self.op(fa, self.back_agg)  # @line L12

    def items(self) -> list[T]:
        """The window from the oldest to the newest item."""
        return [v for v, _ in reversed(self.front)] + list(self.back)

    def check_invariant(self) -> None:
        """Check the stored aggregates against a direct fold."""
        a = self.e
        for v, stored in self.front:
            a = self.op(v, a)
            assert stored == a
        b = self.e
        for v in self.back:
            b = self.op(b, v)
        assert self.back_agg == b
