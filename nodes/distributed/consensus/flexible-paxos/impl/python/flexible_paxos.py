# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flexible-paxos/. The authors are listed in prov/4PEKRH.jsonl.

"""Flexible Paxos: Paxos with separate quorums for phase 1 and phase 2.

A quorum system is given by two predicates on sets of acceptors. Safety needs
only that every phase 1 quorum meets every phase 2 quorum. The simulator is a
seeded discrete event simulator with loss, duplication, reordering, crashes
and dueling proposers.
"""

import random
from dataclasses import dataclass, field
from itertools import combinations
from typing import Callable

Ballot = tuple[int, int]
Pred = Callable[[frozenset], bool]


def by_size(q: int) -> Pred:
    return lambda s: len(s) >= q


def grid(rows: int, cols: int) -> tuple[Pred, Pred]:
    """Acceptor r * cols + c sits at row r, column c. A phase 1 quorum holds a
    full column and a phase 2 quorum holds a full row."""
    def has_col(s: frozenset) -> bool:
        return any(all(r * cols + c in s for r in range(rows)) for c in range(cols))

    def has_row(s: frozenset) -> bool:
        return any(all(r * cols + c in s for c in range(cols)) for r in range(rows))
    return has_col, has_row


def minimal_sets(n: int, pred: Pred) -> list[frozenset]:
    out = []
    for k in range(n + 1):
        for c in combinations(range(n), k):
            s = frozenset(c)
            if pred(s) and not any(m <= s for m in out):
                out.append(s)
    return out


def intersect(n: int, p1: Pred, p2: Pred) -> bool:
    """True if every phase 1 quorum meets every phase 2 quorum (brute force)."""
    a, b = minimal_sets(n, p1), minimal_sets(n, p2)
    return all(x & y for x in a for y in b)


class Proposer:
    def __init__(self, pid: int, value: object, q1: Pred) -> None:
        self.pid, self.value, self.q1 = pid, value, q1
        self.round_seen = 0
        self.ballot: Ballot | None = None
        self.phase = 0
        self.promises: dict[int, tuple[Ballot | None, object]] = {}

    def start(self, net: "Net") -> None:
        self.round_seen += 1
        self.ballot = (self.round_seen, self.pid)
        self.phase, self.promises = 1, {}
        net.to_acceptors(("P", self.pid), ("PREPARE", self.ballot))  # @line L1

    def on_promise(self, net: "Net", a: int, b: Ballot, vb: Ballot | None, vv: object) -> None:
        if b != self.ballot or self.phase != 1:
            return
        self.promises[a] = (vb, vv)  # @line L2
        if self.q1(frozenset(self.promises)):  # @line L3
            voted = [(x, y) for x, y in self.promises.values() if x is not None]
            v = max(voted, key=lambda t: t[0])[1] if voted else self.value  # @line L4
            self.phase = 2
            net.to_acceptors(("P", self.pid), ("ACCEPT", b, v))  # @line L5

    def on_nack(self, b: Ballot) -> None:
        self.round_seen = max(self.round_seen, b[0])


class Acceptor:
    def __init__(self, aid: int) -> None:
        self.aid = aid
        self.promised: Ballot | None = None
        self.vb: Ballot | None = None
        self.vv: object = None

    def on_prepare(self, net: "Net", b: Ballot) -> None:
        if self.promised is None or b > self.promised:  # @line L6
            self.promised = b
            net.send(("A", self.aid), ("P", b[1]), ("PROMISE", self.aid, b, self.vb, self.vv))
        else:
            net.send(("A", self.aid), ("P", b[1]), ("NACK", self.promised))

    def on_accept(self, net: "Net", b: Ballot, v: object) -> None:
        if self.promised is None or b >= self.promised:  # @line L7
            self.promised, self.vb, self.vv = b, b, v
            net.sim.votes.setdefault(b, {})[self.aid] = v
            for j in range(net.sim.n_learners):
                net.send(("A", self.aid), ("L", j), ("ACCEPTED", self.aid, b, v))
        else:
            net.send(("A", self.aid), ("P", b[1]), ("NACK", self.promised))


class Learner:
    def __init__(self, q2: Pred) -> None:
        self.q2 = q2
        self.votes: dict[Ballot, set[int]] = {}
        self.learned: object = None

    def on_accepted(self, a: int, b: Ballot, v: object) -> None:
        self.votes.setdefault(b, set()).add(a)
        if self.q2(frozenset(self.votes[b])):  # @line L8
            self.learned = v


class Net:
    def __init__(self, sim: "FlexiblePaxos") -> None:
        self.sim = sim
        self.queue: list[tuple[tuple, tuple]] = []

    def send(self, src: tuple, dst: tuple, msg: tuple) -> None:
        s = self.sim
        if src in s.crashed or s.rng.random() < s.drop:
            return
        self.queue.append((dst, msg))
        if s.rng.random() < s.dup:
            self.queue.append((dst, msg))

    def to_acceptors(self, src: tuple, msg: tuple) -> None:
        for a in range(self.sim.n):
            self.send(src, ("A", a), msg)


@dataclass
class Result:
    chosen: set = field(default_factory=set)
    learned: list = field(default_factory=list)


class FlexiblePaxos:
    def __init__(self, n: int, q1: Pred, q2: Pred, inputs: list, seed: int,
                 n_learners: int = 2, drop: float = 0.0, dup: float = 0.0,
                 crash_prob: float = 0.0, max_acceptor_crashes: int = 0,
                 timeout_prob: float = 0.05, stable_after: int | None = None,
                 max_steps: int = 2000) -> None:
        self.n, self.q1, self.q2 = n, q1, q2
        self.rng = random.Random(seed)
        self.drop, self.dup, self.crash_prob = drop, dup, crash_prob
        self.max_acceptor_crashes = max_acceptor_crashes
        self.timeout_prob, self.stable_after, self.max_steps = timeout_prob, stable_after, max_steps
        self.n_learners = n_learners
        self.crashed: set[tuple] = set()
        self.votes: dict[Ballot, dict[int, object]] = {}
        self.inputs = inputs
        self.proposers = [Proposer(i, x, q1) for i, x in enumerate(inputs)]
        self.acceptors = [Acceptor(a) for a in range(n)]
        self.learners = [Learner(q2) for _ in range(n_learners)]
        self.net = Net(self)

    def deliver(self, dst: tuple, msg: tuple) -> None:
        if dst in self.crashed:
            return
        if dst[0] == "A":
            a = self.acceptors[dst[1]]
            if msg[0] == "PREPARE":
                a.on_prepare(self.net, msg[1])
            else:
                a.on_accept(self.net, msg[1], msg[2])
        elif dst[0] == "P":
            p = self.proposers[dst[1]]
            if msg[0] == "PROMISE":
                p.on_promise(self.net, *msg[1:])
            else:
                p.on_nack(msg[1])
        else:
            self.learners[dst[1]].on_accepted(*msg[1:])

    def run(self) -> Result:
        for p in self.proposers:
            p.start(self.net)
        for step in range(self.max_steps):
            stable = self.stable_after is not None and step >= self.stable_after
            if stable:
                self.drop = self.dup = 0.0
                if not self.net.queue:
                    if all(l.learned is not None for l in self.learners):
                        break
                    self.proposers[0].start(self.net)
            else:
                if self.rng.random() < self.timeout_prob:
                    p = self.proposers[self.rng.randrange(len(self.proposers))]
                    if ("P", p.pid) not in self.crashed:
                        p.start(self.net)
                if self.rng.random() < self.crash_prob:
                    down = sum(1 for c in self.crashed if c[0] == "A")
                    cands = [("P", i) for i in range(1, len(self.proposers))]
                    if down < self.max_acceptor_crashes:
                        cands += [("A", a) for a in range(self.n)]
                    if cands:
                        self.crashed.add(cands[self.rng.randrange(len(cands))])
            if self.net.queue:
                dst, msg = self.net.queue.pop(self.rng.randrange(len(self.net.queue)))
                self.deliver(dst, msg)
        return self.result()

    def result(self) -> Result:
        r = Result(learned=[l.learned for l in self.learners if l.learned is not None])
        for b, by_acc in self.votes.items():
            for v in set(by_acc.values()):
                if self.q2(frozenset(a for a, w in by_acc.items() if w == v)):
                    r.chosen.add(v)
        return r


def safe(r: Result, inputs: list) -> bool:
    return len(r.chosen) <= 1 and r.chosen <= set(inputs) and all(v in r.chosen for v in r.learned)
