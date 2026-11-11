# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/byzantine-resilience-bound/. The authors are listed in prov/NNA88Z.jsonl.

"""The hexagon (scenario) argument of Fischer, Lynch and Merritt (1986) for
consensus with n = 3 processes A, B, C and t = 1 Byzantine fault, oral messages.

Six copies A0 B0 C0 A1 B1 C1 sit on a ring. Each copy runs the code of its
process, and each of its two neighbours on the ring is a copy of one of the
other two processes, so each copy sees the messages it expects. Copies with
index 0 have input 0 and copies with index 1 have input 1. For two adjacent
copies, a real run with those two processes correct and the third one faulty
gives them the same views as in the ring: the faulty process sends to each
correct process what its adjacent copy sends in the ring. Code cannot prove
the impossibility; it shows the construction on concrete protocols.
"""

from typing import Callable, Hashable

PROCS = "ABC"
RING = ["A0", "B0", "C0", "A1", "B1", "C1"]


class Protocol:
    """A deterministic synchronous protocol for 3 processes."""

    rounds = 1

    def __init__(self, me: str, x: int) -> None:
        self.me, self.x = me, x
        self.got: dict[tuple[int, str], Hashable] = {}

    def send(self, r: int) -> dict[str, Hashable]:
        raise NotImplementedError

    def receive(self, r: int, src: str, msg: Hashable) -> None:
        self.got[(r, src)] = msg

    def decide(self) -> int:
        raise NotImplementedError

    def others(self) -> list[str]:
        return [p for p in PROCS if p != self.me]


class Majority(Protocol):
    """Exchange inputs once and decide the majority of the three values."""

    def send(self, r):
        return {q: self.x for q in self.others()}

    def decide(self):
        vals = [self.x] + [self.got.get((1, q), 0) for q in self.others()]
        return int(sum(vals) >= 2)


class Echo(Protocol):
    """Exchange inputs, then echo what the other process said; distrust a
    value if the echo does not match it (use 0), then take the majority."""

    rounds = 2

    def send(self, r):
        if r == 1:
            return {q: self.x for q in self.others()}
        a, b = self.others()
        return {a: self.got.get((1, b), 0), b: self.got.get((1, a), 0)}

    def decide(self):
        a, b = self.others()
        va = self.got.get((1, a), 0) if self.got.get((1, a)) == self.got.get((2, b)) else 0
        vb = self.got.get((1, b), 0) if self.got.get((1, b)) == self.got.get((2, a)) else 0
        return int(self.x + va + vb >= 2)


class FloodMin(Protocol):
    """FloodSet for two rounds, decide the minimum (correct for one crash)."""

    rounds = 2

    def __init__(self, me, x):
        super().__init__(me, x)
        self.w = {x}

    def send(self, r):
        return {q: frozenset(self.w) for q in self.others()}

    def receive(self, r, src, msg):
        super().receive(r, src, msg)
        self.w |= set(msg)

    def decide(self):
        return min(self.w)


class Own(Protocol):
    """Decide the own input: valid but never agrees on mixed inputs."""

    def send(self, r):
        return {}

    def decide(self):
        return self.x


PROTOCOLS: dict[str, Callable[[str, int], Protocol]] = {
    "majority": Majority, "echo": Echo, "flood-min": FloodMin, "own": Own,
}


def neighbour(copy: str, proc: str) -> str:
    """The ring neighbour of copy that is a copy of proc."""
    i = RING.index(copy)
    for j in (i - 1, i + 1):
        if RING[j % 6][0] == proc:
            return RING[j % 6]
    raise AssertionError


def hexagon(proto) -> tuple[dict, dict]:
    nodes = {c: proto(c[0], int(c[1])) for c in RING}
    views: dict[str, list] = {c: [] for c in RING}
    for r in range(1, proto.rounds + 1):
        batch = []
        for c, node in nodes.items():
            for q, msg in node.send(r).items():
                batch.append((neighbour(c, q), r, c[0], msg))
        for dst, r_, src, msg in batch:
            views[dst].append((r_, src, msg))
            nodes[dst].receive(r_, src, msg)
    return views, {c: nodes[c].decide() for c in RING}


def scenario(proto, pair: tuple[str, str]) -> dict:
    """A real run: the two named copies are the correct processes with their
    inputs; the third process is faulty and replays the ring."""
    hviews, _ = hexagon(proto)
    copy_of = {c[0]: c for c in pair}
    nodes = {p: proto(p, int(c[1])) for p, c in copy_of.items()}
    views: dict[str, list] = {p: [] for p in nodes}
    for r in range(1, proto.rounds + 1):
        batch = []
        for p, node in nodes.items():
            for q, msg in node.send(r).items():
                if q in nodes:
                    batch.append((q, r, p, msg))
        for p in nodes:
            batch += [(p, rr, src, msg) for rr, src, msg in hviews[copy_of[p]] if rr == r and src not in nodes]
        for dst, rr, src, msg in batch:
            views[dst].append((rr, src, msg))
            nodes[dst].receive(rr, src, msg)
    dec = {p: nodes[p].decide() for p in nodes}
    inputs = {nodes[p].x for p in nodes}
    agreement = len(set(dec.values())) == 1
    validity = len(inputs) != 1 or set(dec.values()) <= inputs
    same = all(sorted(views[p], key=repr) == sorted(hviews[copy_of[p]], key=repr) for p in nodes)
    return {"decisions": dec, "views_match": same, "agreement": agreement, "validity": validity}


PAIRS = [("B0", "C0"), ("A1", "B1"), ("C0", "A1")]


def three_runs(proto) -> list[dict]:
    return [scenario(proto, pr) for pr in PAIRS]
