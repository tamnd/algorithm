# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/version-vectors/. The authors are listed in prov/MTVENE.jsonl.

"""Version vectors (Parker et al. 1983).

n replicas hold copies of one object. Replica i increments entry i when it
updates its copy. Two replicas that synchronize compare their vectors: if
one dominates, the other copy is old and is replaced; if the vectors are
incomparable, the copies were updated concurrently and there is a conflict.
Each operation costs O(n) time, and each copy carries n integers.
"""

import random

EQUAL, BEFORE, AFTER, CONCURRENT = "equal", "before", "after", "concurrent"


class VersionVector:
    """The version vector of one copy among n replicas."""

    def __init__(self, n: int) -> None:
        self.v = [0] * n  # @line L1

    def update(self, i: int) -> None:
        """Replica i changes the copy. O(1)."""
        self.v[i] += 1  # @line L2

    def merge(self, other: "VersionVector") -> None:
        """Entrywise maximum, used when two concurrent copies are reconciled. O(n)."""
        for k in range(len(self.v)):  # @line L3
            self.v[k] = max(self.v[k], other.v[k])  # @line L4

    def compare(self, other: "VersionVector") -> str:
        """EQUAL, BEFORE (other dominates), AFTER (self dominates) or CONCURRENT. O(n)."""
        if self.v == other.v:  # @line L5
            return EQUAL
        if all(a <= b for a, b in zip(self.v, other.v)):  # @line L6
            return BEFORE
        if all(a >= b for a, b in zip(self.v, other.v)):  # @line L7
            return AFTER
        return CONCURRENT  # @line L8

    def copy(self) -> "VersionVector":
        out = VersionVector(len(self.v))
        out.v = self.v[:]
        return out


class Replica:
    """A replica: a version vector and the data, here the set of update ids applied."""

    def __init__(self, n: int, i: int) -> None:
        self.i = i
        self.vv = VersionVector(n)
        self.data: frozenset = frozenset()

    def write(self, update_id: object) -> None:
        """A local update: change the data and increment the own entry."""
        self.data = self.data | {update_id}
        self.vv.update(self.i)


def sync(a: Replica, b: Replica) -> str:
    """Two-way synchronization of replicas a and b. Return the comparison result."""
    c = a.vv.compare(b.vv)  # @line L9
    if c == BEFORE:  # @line L10
        a.vv, a.data = b.vv.copy(), b.data
    elif c == AFTER:  # @line L11
        b.vv, b.data = a.vv.copy(), a.data
    elif c == CONCURRENT:  # @line L12
        # A conflict. Here it is resolved by union; an application may do otherwise.
        a.vv.merge(b.vv)
        a.data = a.data | b.data
        b.vv, b.data = a.vv.copy(), a.data
    return c


def random_ops(n: int, steps: int, rng: random.Random) -> list[tuple]:
    """A seeded random schedule of ("write", i) and ("sync", i, j) operations."""
    ops: list[tuple] = []
    for _ in range(steps):
        if n > 1 and rng.random() < 0.5:
            i, j = rng.sample(range(n), 2)
            ops.append(("sync", i, j))
        else:
            ops.append(("write", rng.randrange(n)))
    return ops
