# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mv-register/. The authors are listed in prov/ZMJZQC.jsonl.

"""The multi-value register, a state-based CRDT (Shapiro et al. 2011, RR-7506 Specification 10).

The state is a set of pairs (x, V), where V is a version vector over n
replicas. A write by replica i takes the entrywise maximum of all vectors in
the state, adds one to entry i, and replaces the state with the single new
pair. Merge takes the union and keeps only the pairs whose vector is not
strictly dominated by another vector in the union. A read returns every value
in the state, so concurrent writes show up as siblings. With s pairs a write
takes O(s n) time and a merge of states with s and t pairs takes O((s + t)^2 n).
"""

from typing import Any

Vec = tuple[int, ...]
State = frozenset[tuple[Any, Vec]]


def leq(v: Vec, w: Vec) -> bool:
    return all(a <= b for a, b in zip(v, w))


def maximal(pairs: set[tuple[Any, Vec]]) -> set[tuple[Any, Vec]]:
    """Keep each pair whose vector no other vector in the set strictly dominates."""
    out = set()
    for x, v in pairs:  # @line L8
        if not any(leq(v, w) and v != w for _, w in pairs):  # @line L9
            out.add((x, v))
    return out


class MVRegister:
    """One replica of an MV-Register among n replicas, with id i."""

    def __init__(self, n: int, i: int) -> None:
        self.n, self.me = n, i
        self.s: set[tuple[Any, Vec]] = set()  # @line L1

    def read(self) -> frozenset[Any]:
        return frozenset(x for x, _ in self.s)  # @line L2

    def write(self, x: Any) -> None:
        v = [0] * self.n  # @line L3
        for _, w in self.s:  # @line L4
            v = [max(a, b) for a, b in zip(v, w)]
        v[self.me] += 1  # @line L5
        self.s = {(x, tuple(v))}  # @line L6

    def merge(self, other: "MVRegister | State") -> None:
        b = other.s if isinstance(other, MVRegister) else other
        self.s = maximal(self.s | set(b))  # @line L7

    def compare(self, other: "MVRegister | State") -> bool:
        """State order: every own vector is below some vector of the other state."""
        b = other.s if isinstance(other, MVRegister) else other
        return all(any(leq(v, w) for _, w in b) for _, v in self.s)

    def state(self) -> State:
        return frozenset(self.s)

    def check_invariant(self) -> None:
        """No vector in the state dominates another, and equal vectors carry one value."""
        vecs = [v for _, v in self.s]
        assert len(set(vecs)) == len(vecs)
        assert maximal(self.s) == self.s


def join(x: State, y: State) -> State:
    return frozenset(maximal(set(x) | set(y)))
