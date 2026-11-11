# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rga/. The authors are listed in prov/WZ1GQT.jsonl.

"""The Replicated Growable Array (Roh, Jeon, Kim and Lee 2011), an op-based sequence CRDT.

Every element has a unique timestamp. Roh et al. use an S4Vector
(ssn, sum, sid, seq): a session number, the sum of the site's vector clock,
the site id and the site's own operation count. Two S4Vectors are ordered by
(ssn, sum, sid). With causal delivery, sum grows along causality, so the order
respects happens-before like a Lamport timestamp does.

The list keeps every element ever inserted. A deleted element stays as a
tombstone. To insert after a reference element, a replica starts right after
the reference and skips every element with a larger timestamp, then inserts.
Operations must arrive in causal order, and each at most once.
"""

from typing import Any, NamedTuple


class S4(NamedTuple):
    ssn: int
    sum: int
    sid: int
    seq: int

    def key(self) -> tuple[int, int, int]:
        return (self.ssn, self.sum, self.sid)


class Node:
    __slots__ = ("ts", "value", "dead")

    def __init__(self, ts: S4 | None, value: Any) -> None:
        self.ts, self.value, self.dead = ts, value, False


Op = tuple  # ("ins", ref, ts, value) or ("del", ts)


class RGA:
    """One RGA replica with site id sid among n sites."""

    def __init__(self, n: int, sid: int, ssn: int = 0) -> None:
        self.sid, self.ssn = sid, ssn
        self.vc = [0] * n
        self.nodes: list[Node] = [Node(None, None)]  # @line L1
        self.index: dict[S4, Node] = {}

    def _pos(self, ts: S4 | None) -> int:
        if ts is None:
            return 0
        return self.nodes.index(self.index[ts])

    def _visible(self) -> list[Node]:
        return [x for x in self.nodes[1:] if not x.dead]

    def _stamp(self) -> S4:
        self.vc[self.sid] += 1
        return S4(self.ssn, sum(self.vc), self.sid, self.vc[self.sid])

    def local_insert(self, i: int, value: Any) -> Op:
        """Insert value so that it becomes visible element i. Returns the op to broadcast."""
        vis = self._visible()
        ref = vis[i - 1].ts if i > 0 else None
        op = ("ins", ref, self._stamp(), value)
        self._integrate(op)
        return op

    def local_delete(self, i: int) -> Op:
        op = ("del", self._visible()[i].ts)
        self._integrate(op)
        return op

    def apply(self, op: Op) -> None:
        """Apply a remote op. The caller delivers ops in causal order."""
        ts = op[2] if op[0] == "ins" else None
        if ts is not None:
            self.vc[ts.sid] = max(self.vc[ts.sid], ts.seq)
        self._integrate(op)

    def _integrate(self, op: Op) -> None:
        if op[0] == "del":
            self.index[op[1]].dead = True  # @line L8
            return
        _, ref, ts, value = op
        p = self._pos(ref) + 1  # @line L2
        while p < len(self.nodes) and self.nodes[p].ts.key() > ts.key():  # @line L3
            p += 1  # @line L4
        node = Node(ts, value)  # @line L5
        self.nodes.insert(p, node)  # @line L6
        self.index[ts] = node  # @line L7

    def value(self) -> list[Any]:
        return [x.value for x in self._visible()]

    def order(self) -> list[S4]:
        """All timestamps in list order, tombstones included."""
        return [x.ts for x in self.nodes[1:]]

    def check_invariant(self) -> None:
        keys = [x.ts.key() for x in self.nodes[1:]]
        assert len(set(keys)) == len(keys)
        assert len(self.index) == len(keys)
