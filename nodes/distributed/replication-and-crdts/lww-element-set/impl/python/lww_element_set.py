# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lww-element-set/. The authors are listed in prov/3D6HMS.jsonl.

"""The last-writer-wins element set, a state-based CRDT (Shapiro et al. 2011, RR-7506 Section 3.3.3).

For each element the replica keeps the largest add timestamp and the largest
remove timestamp it has seen. An element is in the set when its add timestamp
is larger than its remove timestamp. On equal timestamps the bias decides:
"add" keeps the element, "remove" drops it. Merge takes the maximum of each
timestamp, which is the join of a product of max-semilattices.
Timestamps come from the caller, so the set reflects whatever clock the
replicas use. Each operation takes O(1) expected time and merge takes O(m)
expected time for a received state with m entries.
"""

from collections.abc import Hashable

Stamps = dict[Hashable, int]
State = tuple[tuple[tuple[Hashable, int], ...], tuple[tuple[Hashable, int], ...]]


class LWWElementSet:
    """One replica of an LWW-Element-Set with a fixed bias."""

    def __init__(self, bias: str = "add") -> None:
        if bias not in ("add", "remove"):
            raise ValueError("bias is 'add' or 'remove'")
        self.bias = bias
        self.add_ts: Stamps = {}  # @line L1
        self.rem_ts: Stamps = {}

    def add(self, e: Hashable, ts: int) -> None:
        if ts > self.add_ts.get(e, -1):  # @line L2
            self.add_ts[e] = ts

    def remove(self, e: Hashable, ts: int) -> None:
        if ts > self.rem_ts.get(e, -1):  # @line L3
            self.rem_ts[e] = ts

    def lookup(self, e: Hashable) -> bool:
        if e not in self.add_ts:  # @line L4
            return False
        a = self.add_ts[e]
        r = self.rem_ts.get(e, -1)
        if a != r:  # @line L5
            return a > r
        return self.bias == "add"  # @line L6

    def merge(self, other: "LWWElementSet | State") -> None:
        if isinstance(other, LWWElementSet):
            oa, orr = other.add_ts.items(), other.rem_ts.items()
        else:
            oa, orr = other
        for e, t in oa:  # @line L7
            self.add(e, t)
        for e, t in orr:  # @line L8
            self.remove(e, t)

    def state(self) -> State:
        return (tuple(sorted(self.add_ts.items(), key=repr)), tuple(sorted(self.rem_ts.items(), key=repr)))

    def elements(self) -> frozenset:
        return frozenset(e for e in self.add_ts if self.lookup(e))

    def check_invariant(self) -> None:
        for d in (self.add_ts, self.rem_ts):
            for t in d.values():
                assert isinstance(t, int) and t >= 0
