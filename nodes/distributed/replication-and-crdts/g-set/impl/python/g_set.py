# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/g-set/. The authors are listed in prov/PZZKRZ.jsonl.

"""The grow-only set, a state-based CRDT (Shapiro et al. 2011, RR-7506 Specification 11).

The state is a finite set A. add puts an element in A, lookup tests membership,
and merge is set union. With a hash set, add and lookup take O(1) expected
time, and merge takes O(|B|) expected time for a received state B.
"""

from collections.abc import Hashable, Iterable


class GSet:
    """One replica of a grow-only set."""

    def __init__(self) -> None:
        self.a: set[Hashable] = set()  # @line L1

    def add(self, e: Hashable) -> None:
        self.a.add(e)  # @line L2

    def lookup(self, e: Hashable) -> bool:
        return e in self.a  # @line L3

    def merge(self, other: "GSet | Iterable[Hashable]") -> None:
        """Join a received state into this one."""
        b = other.a if isinstance(other, GSet) else other
        self.a |= set(b)  # @line L4

    def compare(self, other: "GSet | Iterable[Hashable]") -> bool:
        """True when this state is a subset of the other one."""
        b = other.a if isinstance(other, GSet) else set(other)
        return self.a <= b  # @line L5

    def state(self) -> frozenset[Hashable]:
        """An immutable copy of A, which is what a replica sends."""
        return frozenset(self.a)

    def elements(self) -> frozenset[Hashable]:
        return frozenset(self.a)

    def check_invariant(self, added_in_history: set[Hashable]) -> None:
        """A must equal the set of elements added in the causal history."""
        assert self.a == added_in_history, (self.a, added_in_history)
