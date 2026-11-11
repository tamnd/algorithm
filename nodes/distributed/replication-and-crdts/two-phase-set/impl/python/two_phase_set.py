# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-phase-set/. The authors are listed in prov/0YDBGZ.jsonl.

"""The two-phase set (2P-Set), a state-based CRDT (Shapiro et al. 2011, RR-7506 Specification 12).

The state is a pair of grow-only sets: A holds every element ever added and R
(the tombstone set) every element ever removed. An element is in the set when
it is in A and not in R. Remove has a precondition at the source: the element
must be in the set there. Once removed, an element can never come back.
With hash sets, add, remove and lookup take O(1) expected time, and merge
takes O(|A'| + |R'|) expected time for a received state (A', R').
"""

from collections.abc import Hashable

State = tuple[frozenset, frozenset]


class TwoPhaseSet:
    """One replica of a 2P-Set."""

    def __init__(self) -> None:
        self.a: set[Hashable] = set()  # @line L1
        self.r: set[Hashable] = set()

    def lookup(self, e: Hashable) -> bool:
        return e in self.a and e not in self.r  # @line L2

    def add(self, e: Hashable) -> None:
        """Add e. If e was removed before, the add has no visible effect."""
        self.a.add(e)  # @line L3

    def remove(self, e: Hashable) -> None:
        """Remove e. Precondition: lookup(e) is true at this replica."""
        if not self.lookup(e):  # @line L4
            raise ValueError("remove needs the element in the set at the source")
        self.r.add(e)  # @line L5

    def merge(self, other: "TwoPhaseSet | State") -> None:
        """Join a received state into this one."""
        oa, orr = (other.a, other.r) if isinstance(other, TwoPhaseSet) else other
        self.a |= set(oa)  # @line L6
        self.r |= set(orr)  # @line L7

    def compare(self, other: "TwoPhaseSet | State") -> bool:
        """True when A and R are both subsets of the other state's sets."""
        oa, orr = (other.a, other.r) if isinstance(other, TwoPhaseSet) else other
        return self.a <= set(oa) and self.r <= set(orr)  # @line L8

    def state(self) -> State:
        return (frozenset(self.a), frozenset(self.r))

    def elements(self) -> frozenset:
        return frozenset(self.a - self.r)

    def check_invariant(self) -> None:
        """Every tombstone names an element that was added: R is a subset of A."""
        assert self.r <= self.a, (self.a, self.r)
