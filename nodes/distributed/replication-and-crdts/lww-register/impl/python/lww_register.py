# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lww-register/. The authors are listed in prov/TFCFZR.jsonl.

"""The last-writer-wins register, a state-based CRDT (Shapiro et al. 2011, RR-7506 Specification 8).

The state is one value with a stamp (c, r): a counter c and the id r of the
replica that wrote it. Stamps are compared as pairs, so two different writes
never tie. A write takes a counter one larger than any counter the replica
has seen, which makes stamps respect causality. Merge keeps the pair with the
larger stamp. Every operation takes O(1) time.
"""

from typing import Any

Stamp = tuple[int, int]
State = tuple[Stamp, Any]


class LWWRegister:
    """One replica of an LWW-Register with replica id rid."""

    def __init__(self, rid: int, initial: Any = None) -> None:
        self.rid = rid
        self.stamp: Stamp = (0, -1)  # @line L1
        self.value: Any = initial

    def read(self) -> Any:
        return self.value  # @line L2

    def write(self, v: Any) -> None:
        c = self.stamp[0] + 1  # @line L3
        self.stamp = (c, self.rid)  # @line L4
        self.value = v

    def merge(self, other: "LWWRegister | State") -> None:
        st, v = (other.stamp, other.value) if isinstance(other, LWWRegister) else other
        if st > self.stamp:  # @line L5
            self.stamp, self.value = st, v  # @line L6

    def compare(self, other: "LWWRegister | State") -> bool:
        st = other.stamp if isinstance(other, LWWRegister) else other[0]
        return self.stamp <= st  # @line L7

    def state(self) -> State:
        return (self.stamp, self.value)

    def check_invariant(self) -> None:
        c, r = self.stamp
        assert c >= 0 and (c == 0) == (r == -1)


def join(x: State, y: State) -> State:
    """The pure join on states: the pair with the larger stamp."""
    return x if x[0] >= y[0] else y
