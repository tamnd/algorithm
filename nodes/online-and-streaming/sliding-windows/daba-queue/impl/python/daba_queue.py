# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/daba-queue/. The authors are listed in prov/JMSPSC.jsonl.

from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class DabaQueue(Generic[T]):
    """DABA, the De-Amortized Banker's Aggregator (Tangwongsan, Hirzel and Schneider).

    A FIFO window over a monoid (op, identity). The items have absolute
    positions F <= L <= R <= A <= B <= E; position i holds val[i] and agg[i].
    Every operation makes O(1) calls of op in the worst case: at most 1 for
    query, 4 for insert and 3 for evict. op must be associative; it need not
    be commutative or invertible.
    """

    def __init__(self, op: Callable[[T, T], T], identity: T) -> None:
        self.op = op
        self.e = identity
        self.val: dict[int, T] = {}
        self.agg: dict[int, T] = {}
        self.F = self.L = self.R = self.A = self.B = self.E = 0

    def __len__(self) -> int:
        return self.E - self.F

    # The aggregate of each sublist, or the identity if it is empty.
    def _pi_f(self) -> T:
        return self.e if self.F == self.B else self.agg[self.F]

    def _pi_b(self) -> T:
        return self.e if self.B == self.E else self.agg[self.E - 1]

    def _pi_l(self) -> T:
        return self.e if self.L == self.R else self.agg[self.L]

    def _pi_r(self) -> T:
        return self.e if self.R == self.A else self.agg[self.A - 1]

    def _pi_a(self) -> T:
        return self.e if self.A == self.B else self.agg[self.A]

    def query(self) -> T:
        """Return v_0 op ... op v_(n-1), oldest first, or the identity."""
        return self.op(self._pi_f(), self._pi_b())  # @line L1

    def insert(self, v: T) -> None:
        """Add v as the newest item."""
        self.val[self.E] = v  # @line L2
        self.agg[self.E] = self.op(self._pi_b(), v)
        self.E += 1
        self._fixup()  # @line L3

    def evict(self) -> T:
        """Remove and return the oldest item. Precondition: not empty."""
        if self.F == self.E:
            raise IndexError("evict from an empty window")
        v = self.val.pop(self.F)  # @line L4
        del self.agg[self.F]
        self.F += 1
        self._fixup()  # @line L5
        return v

    def _fixup(self) -> None:
        if self.F == self.B:  # @line L6
            self.B = self.A = self.R = self.L = self.E  # @line L7
            return
        if self.L == self.B:  # @line L8
            self.L, self.A, self.B = self.F, self.E, self.E  # @line L9
        if self.L == self.R:  # @line L10
            self.A += 1  # @line L11
            self.R += 1
            self.L += 1
        else:
            pa = self._pi_a()
            self.agg[self.L] = self.op(self.op(self._pi_l(), self._pi_r()), pa)  # @line L12
            self.L += 1  # @line L13
            self.agg[self.A - 1] = self.op(self.val[self.A - 1], pa)  # @line L14
            self.A -= 1  # @line L15

    def items(self) -> list[T]:
        return [self.val[i] for i in range(self.F, self.E)]

    def check_invariant(self) -> None:
        """Check the order, size and values invariants by direct folds."""
        F, L, R, A, B, E = self.F, self.L, self.R, self.A, self.B, self.E
        assert F <= L <= R <= A <= B <= E
        assert (B == F and E == B) or (L - F == E - B + 1 and R - L == A - R)
        op, v = self.op, self.val

        def fold(lo: int, hi: int) -> T:
            a = self.e
            for i in range(lo, hi):
                a = op(a, v[i])
            return a

        for i in range(F, L):
            assert self.agg[i] == fold(i, B)
        for i in range(L, R):
            assert self.agg[i] == fold(i, R)
        for i in range(R, A):
            assert self.agg[i] == fold(R, i + 1)
        for i in range(A, B):
            assert self.agg[i] == fold(i, B)
        for i in range(B, E):
            assert self.agg[i] == fold(B, i + 1)
