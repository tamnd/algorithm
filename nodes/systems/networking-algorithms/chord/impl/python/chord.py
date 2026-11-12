# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chord/. The authors are listed in prov/W8KBGE.jsonl.

"""Chord: a ring of m-bit identifiers with successor lists and fingers.

This is a sequential simulation. Each call such as stabilize(n) is one
atomic step of node n, and a node may read the state of a live node
directly (this models a remote call that gets an answer). The ring
maintenance follows the corrected protocol of Pamela Zave (2017):

* each node keeps prdc and a successor list succ of length r;
* join(n, via) asks a live member for the predecessor of n and copies its
  successor list;
* stabilize(n) repairs the head of succ, adopts a closer successor if the
  successor knows one, and then notifies the successor, which may adopt n
  as its predecessor (rectify).

Lookups use the finger table: finger[i] = successor(n + 2**i).
"""

from typing import Optional


def between(a: int, b: int, c: int) -> bool:
    """True if b lies strictly inside the clockwise arc from a to c.

    If a == c the arc is the whole ring without a.
    """
    if a < c:
        return a < b < c
    return a < b or b < c


class Node:
    __slots__ = ("ident", "prdc", "succ", "finger", "alive")

    def __init__(self, ident: int, m: int):
        self.ident = ident
        self.prdc: Optional[int] = None
        self.succ: list[int] = []
        self.finger: list[Optional[int]] = [None] * m
        self.alive = True


class Ring:
    def __init__(self, m: int, r: int):
        self.m, self.r = m, r
        self.size = 1 << m
        self.nodes: dict[int, Node] = {}

    # -- set-up -------------------------------------------------------------

    def live_ids(self) -> list[int]:
        return sorted(i for i, v in self.nodes.items() if v.alive)

    def create(self, ids) -> None:
        """Start with at least r + 1 nodes in the ideal state (Zave)."""
        ids = sorted(set(ids))
        if len(ids) < self.r + 1:
            raise ValueError("Zave's protocol needs at least r + 1 initial nodes")
        for i in ids:
            self.nodes[i] = Node(i, self.m)
        k = len(ids)
        for j, i in enumerate(ids):
            v = self.nodes[i]
            v.prdc = ids[j - 1]
            v.succ = [ids[(j + t) % k] for t in range(1, self.r + 1)]
        self.fix_all_fingers()

    def alive(self, i: Optional[int]) -> bool:
        return i is not None and i in self.nodes and self.nodes[i].alive

    # -- the protocol -------------------------------------------------------

    def join(self, ident: int, via: int) -> None:
        if ident in self.nodes:
            raise ValueError("identifier in use")
        p = self.find_predecessor(via, ident)[0]  # @line L11
        v = Node(ident, self.m)
        v.succ = list(self.nodes[p].succ)  # @line L12
        v.prdc = p
        v.finger = [v.succ[0]] * self.m
        self.nodes[ident] = v

    def fail(self, ident: int) -> None:
        self.nodes[ident].alive = False

    def stabilize(self, ident: int) -> None:
        v = self.nodes[ident]
        while not self.alive(v.succ[0]):  # @line L13: the head failed, drop it
            v.succ = v.succ[1:]
            if not v.succ:
                raise RuntimeError("operating assumption broken: no live successor")
        head = self.nodes[v.succ[0]]
        v.succ = [head.ident] + head.succ[: self.r - 1]  # @line L14
        new = head.prdc  # @line L15
        if self.alive(new) and between(ident, new, head.ident):  # @line L16
            w = self.nodes[new]  # a node that joined between v and its successor
            v.succ = [new] + w.succ[: self.r - 1]
        self.rectify(v.succ[0], ident)  # @line L17

    def rectify(self, ident: int, candidate: int) -> None:
        """The successor ident was notified by candidate."""
        v = self.nodes[ident]
        if not self.alive(v.prdc) or between(v.prdc, candidate, ident):  # @line L18
            v.prdc = candidate

    def fix_finger(self, ident: int, i: int) -> None:
        v = self.nodes[ident]
        v.finger[i] = self.find_successor(ident, (ident + (1 << i)) % self.size)[0]  # @line L19

    def fix_all_fingers(self) -> None:
        live = self.live_ids()
        for ident in live:
            for i in range(self.m):
                self.nodes[ident].finger[i] = successor_of(live, (ident + (1 << i)) % self.size)

    # -- lookup ---------------------------------------------------------------

    def closest_preceding(self, ident: int, key: int) -> int:
        """The live node known to ident that is closest before key."""
        v = self.nodes[ident]
        best = ident  # @line L7
        for c in reversed(v.finger + v.succ):  # @line L8
            if self.alive(c) and between(best, c, key):  # @line L9
                best = c
        return best  # @line L10

    def first_live(self, ident: int) -> int:
        return next(c for c in self.nodes[ident].succ if self.alive(c))

    def find_predecessor(self, start: int, key: int) -> tuple[int, int]:
        """A live node n with key in (n, s], s the first live successor of n.

        Returns n and the number of forwarding hops. The first live
        successor s is always a candidate of closest_preceding, so each hop
        moves strictly closer to key.
        """
        n, hops = start, 0  # @line L1
        s = self.first_live(n)  # @line L2
        while not (between(n, key, s) or key == s):  # @line L3
            n, hops = self.closest_preceding(n, key), hops + 1  # @line L4
            s = self.first_live(n)  # @line L5
        return n, hops

    def find_successor(self, start: int, key: int) -> tuple[int, int]:
        """The node responsible for key, and the forwarding hops."""
        n, hops = self.find_predecessor(start, key)
        return self.first_live(n), hops  # @line L6

    # -- checks -----------------------------------------------------------------

    def is_ideal(self) -> bool:
        """Zave's ideal state: every live node points at the next live nodes."""
        live = self.live_ids()
        k = len(live)
        for j, i in enumerate(live):
            v = self.nodes[i]
            want = [live[(j + t) % k] for t in range(1, min(self.r, k - 1) + 1)]
            if v.succ[: len(want)] != want or v.prdc != live[j - 1]:
                return False
        return True

    def has_live_successor(self) -> bool:
        return all(any(self.alive(c) for c in self.nodes[i].succ) for i in self.live_ids())


def successor_of(sorted_ids: list[int], key: int) -> int:
    """The first identifier at or after key, clockwise."""
    import bisect

    j = bisect.bisect_left(sorted_ids, key)
    return sorted_ids[j % len(sorted_ids)]


def stabilize_round(ring: Ring, rng) -> None:
    order = ring.live_ids()
    rng.shuffle(order)
    for i in order:
        ring.stabilize(i)


def rounds_to_ideal(ring: Ring, rng, limit: int = 1000) -> int:
    """Run stabilize rounds until the ring is ideal; return the number of rounds."""
    for k in range(limit + 1):
        if ring.is_ideal():
            return k
        stabilize_round(ring, rng)
    raise RuntimeError("no convergence")
