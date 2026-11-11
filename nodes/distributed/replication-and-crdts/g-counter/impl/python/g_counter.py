# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/g-counter/. The authors are listed in prov/MQEY7J.jsonl.

"""The grow-only counter, a state-based CRDT (Shapiro et al. 2011, Section 4.1).

Replica i of n keeps a vector P of n naturals. P[j] is the number of
increments made at replica j that replica i knows about. increment adds 1 to
its own entry, value is the sum, and merge is the pointwise max. The state
must be durable: a replica that restarts from zeros under its old id can
lose increments.

The module also has two counters that are not CRDTs, used in the tests and on
the page: a single integer merged with max, and a single integer merged with +.
"""


class GCounter:
    """One replica of a grow-only counter."""

    def __init__(self, n: int, i: int) -> None:
        if not 0 <= i < n:
            raise ValueError("replica id out of range")
        self.p = [0] * n  # @line L1
        self.me = i  # @line L2

    def increment(self) -> None:
        self.p[self.me] += 1  # @line L3

    def value(self) -> int:
        return sum(self.p)  # @line L4

    def merge(self, other: "GCounter | list[int]") -> None:
        """Join a received state (another replica or a copy of its vector) into this one."""
        q = other.p if isinstance(other, GCounter) else other
        if len(q) != len(self.p):
            raise ValueError("states of different sizes")
        for j in range(len(self.p)):  # @line L5
            self.p[j] = max(self.p[j], q[j])  # @line L6

    def compare(self, other: "GCounter | list[int]") -> bool:
        """True when this state is below the other one in the semilattice order."""
        q = other.p if isinstance(other, GCounter) else other
        return all(a <= b for a, b in zip(self.p, q))  # @line L7

    def state(self) -> list[int]:
        """A copy of the vector, which is what a replica sends."""
        return list(self.p)

    def check_invariant(self, increments_known: list[int]) -> None:
        """P[j] must equal the number of increments of j that this replica knows."""
        assert self.p == increments_known, (self.p, increments_known)


class OpGCounter:
    """The op-based form: an increment is broadcast as the message "+1".

    It converges only when every message is delivered exactly once.
    """

    def __init__(self) -> None:
        self.v = 0

    def increment(self) -> str:
        self.v += 1
        return "+1"

    def deliver(self, msg: str) -> None:
        if msg != "+1":
            raise ValueError("unknown message")
        self.v += 1

    def value(self) -> int:
        return self.v


class MaxIntCounter:
    """Not a CRDT: one integer, merged with max. It loses concurrent increments."""

    def __init__(self) -> None:
        self.v = 0

    def increment(self) -> None:
        self.v += 1

    def merge(self, other: int) -> None:
        self.v = max(self.v, other)

    def value(self) -> int:
        return self.v


class SumMergeCounter:
    """Not a CRDT: one integer per replica, merged by adding. Duplicates count twice."""

    def __init__(self) -> None:
        self.v = 0

    def increment(self) -> None:
        self.v += 1

    def merge(self, other: int) -> None:
        self.v += other

    def value(self) -> int:
        return self.v
