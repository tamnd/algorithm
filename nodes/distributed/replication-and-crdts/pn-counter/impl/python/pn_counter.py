# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pn-counter/. The authors are listed in prov/KN5BQ5.jsonl.

"""The PN-counter, a state-based CRDT (Shapiro et al. 2011, RR-7506 Specification 7).

Replica i of n keeps two vectors of n naturals: P counts increments and N
counts decrements, one entry per replica. The value is sum(P) - sum(N), and
merge is the pointwise max of both vectors. Each operation is Theta(n) time
except increment and decrement, which are Theta(1).

The module also has BrokenSignedCounter, a single vector where a decrement
subtracts from the own entry. It is not a CRDT, and the tests show it.
"""


class PNCounter:
    """One replica of a PN-counter."""

    def __init__(self, n: int, i: int) -> None:
        if not 0 <= i < n:
            raise ValueError("replica id out of range")
        self.p = [0] * n  # @line L1
        self.n = [0] * n  # @line L2
        self.me = i  # @line L3

    def increment(self) -> None:
        self.p[self.me] += 1  # @line L4

    def decrement(self) -> None:
        self.n[self.me] += 1  # @line L5

    def value(self) -> int:
        return sum(self.p) - sum(self.n)  # @line L6

    def merge(self, other: "PNCounter | tuple[list[int], list[int]]") -> None:
        """Join a received state (a replica or a pair of vectors) into this one."""
        qp, qn = (other.p, other.n) if isinstance(other, PNCounter) else other
        if len(qp) != len(self.p) or len(qn) != len(self.n):
            raise ValueError("states of different sizes")
        for j in range(len(self.p)):  # @line L7
            self.p[j] = max(self.p[j], qp[j])  # @line L8
            self.n[j] = max(self.n[j], qn[j])  # @line L9

    def compare(self, other: "PNCounter | tuple[list[int], list[int]]") -> bool:
        """True when this state is at or below the other one in the product order."""
        qp, qn = (other.p, other.n) if isinstance(other, PNCounter) else other
        return all(a <= b for a, b in zip(self.p, qp)) and all(  # @line L10
            a <= b for a, b in zip(self.n, qn)
        )

    def state(self) -> tuple[list[int], list[int]]:
        """A copy of the two vectors, which is what a replica sends."""
        return (list(self.p), list(self.n))

    def check_invariant(self, incs: list[int], decs: list[int]) -> None:
        """P[j] and N[j] must equal the increments and decrements of j that are known here."""
        assert self.p == incs and self.n == decs, (self.p, self.n, incs, decs)


def join(a: tuple[list[int], list[int]], b: tuple[list[int], list[int]]) -> tuple[list[int], list[int]]:
    """The join of two states as a pure function, for the semilattice tests."""
    return ([max(x, y) for x, y in zip(a[0], b[0])], [max(x, y) for x, y in zip(a[1], b[1])])


class BrokenSignedCounter:
    """A single vector where decrement subtracts 1 from the own entry, merged by max.

    Decrement moves the state down in the pointwise order, so a merge with an
    older copy undoes it. This is not a CRDT.
    """

    def __init__(self, n: int, i: int) -> None:
        self.v = [0] * n
        self.me = i

    def increment(self) -> None:
        self.v[self.me] += 1

    def decrement(self) -> None:
        self.v[self.me] -= 1

    def value(self) -> int:
        return sum(self.v)

    def merge(self, q: list[int]) -> None:
        self.v = [max(a, b) for a, b in zip(self.v, q)]

    def state(self) -> list[int]:
        return list(self.v)
