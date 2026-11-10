# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-paxos/. The authors are listed in prov/YZ2GMJ.jsonl.

"""Fast Paxos in a deterministic discrete event simulator.

Rounds are integers. Round i has coordinator (i // 2) mod k. Even rounds are
fast and odd rounds are classic, so a coordinator owns a fast round 2m and the
classic round 2m + 1 that it uses for coordinated recovery after a collision.
A classic quorum is any set of at least qc acceptors and a fast quorum any set
of at least qf acceptors.
"""

import random
from dataclasses import dataclass, field
from itertools import combinations

ANY = "<any>"


def requirement_holds(n: int, qc: int, qf: int) -> bool:
    """The Quorum Requirement of Fast Paxos, by brute force over all quorums.

    (a) Any two quorums intersect. (b) Any quorum and any two fast quorums
    have a common acceptor. Quorums of each kind are the sets of the given
    size; larger sets only make intersections larger.
    """
    acc = range(n)
    classic = [set(c) for c in combinations(acc, qc)]
    fast = [set(c) for c in combinations(acc, qf)]
    every = classic + fast
    for q1 in every:
        for q2 in every:
            if not q1 & q2:
                return False
    for q in every:
        for r1 in fast:
            for r2 in fast:
                if not q & r1 & r2:
                    return False
    return True


def counting_condition(n: int, qc: int, qf: int) -> bool:
    """The same requirement as a counting rule, for qc <= qf."""
    return 2 * qc > n and qc + 2 * qf > 2 * n


def smallest_fast_quorum(n: int) -> int:
    """The smallest qf allowed when classic quorums are majorities."""
    qc = n // 2 + 1
    return next(qf for qf in range(qc, n + 1) if counting_condition(n, qc, qf))


def is_fast(i: int) -> bool:
    return i % 2 == 0


class Acceptor:
    def __init__(self, aid: int) -> None:
        self.aid = aid
        self.rnd = -1
        self.vrnd = -1  # -1 means "has not voted"
        self.vval: object = None
        self.any_round = -1  # the fast round in which it may vote for any proposal
        self.proposals: list[object] = []

    def on_1a(self, net: "Net", i: int) -> None:
        if i > self.rnd:  # @line L9
            self.rnd = i
            net.send(("A", self.aid), ("C", coord_of(i, net.k)), ("1b", i, self.aid, self.vrnd, self.vval))

    def on_2a(self, net: "Net", i: int, v: object) -> None:
        if i >= self.rnd and self.vrnd != i:  # @line L10
            if v == ANY:
                self.rnd, self.any_round = i, i
                if self.proposals:
                    self.vote(net, i, self.proposals[0])
            else:
                self.vote(net, i, v)

    def on_proposal(self, net: "Net", v: object) -> None:
        self.proposals.append(v)
        if self.any_round >= 0 and self.any_round == self.rnd and self.vrnd != self.rnd:  # @line L11
            self.vote(net, self.rnd, v)

    def vote(self, net: "Net", i: int, v: object) -> None:
        self.rnd, self.vrnd, self.vval = i, i, v  # @line L12
        net.record_vote(self.aid, i, v)
        net.to_learners_and_coord(("A", self.aid), ("2b", i, self.aid, v))


def coord_of(i: int, k: int) -> int:
    return (i // 2) % k


def pick(reports: dict[int, tuple[int, object]], qc: int, qf: int, n: int, i: int,
         proposals: list[object]) -> object | None:
    """Lines L3 to L7: the value that round i may use, given the reports
    (acceptor -> (vrnd, vval)) of a classic quorum Q."""
    k = max(vr for vr, _ in reports.values())  # @line L3
    if k < 0:
        if is_fast(i):
            return ANY  # @line L4
        return proposals[0] if proposals else None
    vals = {vv for vr, vv in reports.values() if vr == k}
    if len(vals) == 1:
        return next(iter(vals))  # @line L5
    q = set(reports)
    for w in sorted(vals, key=str):
        # O4(w): some k-quorum R has every acceptor of R and Q voting w in round k.
        need = qf if is_fast(k) else qc
        for r in combinations(range(n), need):
            inter = q & set(r)
            if all(reports[a] == (k, w) for a in inter):
                return w  # @line L6
    return proposals[0] if proposals else None  # @line L7


class Coordinator:
    def __init__(self, cid: int, n: int, k: int, qc: int, qf: int) -> None:
        self.cid, self.n, self.k, self.qc, self.qf = cid, n, k, qc, qf
        self.crnd = -1
        self.ones: dict[int, dict[int, tuple[int, object]]] = {}
        self.twos: dict[int, dict[int, object]] = {}
        self.sent_2a: set[int] = set()
        self.proposals: list[object] = []
        self.recover = True

    def start(self, net: "Net", seen: int) -> None:
        m = max(seen, self.crnd) // 2 + 1
        while m % self.k != self.cid:
            m += 1
        self.crnd = 2 * m  # a fast round of this coordinator
        net.to_acceptors(("C", self.cid), ("1a", self.crnd))  # @line L1

    def on_1b(self, net: "Net", i: int, a: int, vr: int, vv: object) -> None:
        if i != self.crnd or i in self.sent_2a:
            return
        self.ones.setdefault(i, {})[a] = (vr, vv)
        if len(self.ones[i]) >= self.qc:  # @line L2
            v = pick(self.ones[i], self.qc, self.qf, self.n, i, self.proposals)
            if v is not None:
                self.sent_2a.add(i)
                net.to_acceptors(("C", self.cid), ("2a", i, v))  # @line L8

    def on_2b(self, net: "Net", i: int, a: int, v: object) -> None:
        """Coordinated recovery: the 2b messages of fast round i serve as the
        1b messages of the classic round i + 1."""
        if not self.recover or i != self.crnd or not is_fast(i):
            return
        self.twos.setdefault(i, {})[a] = v
        got = self.twos[i]
        if len(got) >= self.qc and len(set(got.values())) > 1 and i + 1 not in self.sent_2a:
            reports = {b: (i, w) for b, w in got.items()}
            v2 = pick(reports, self.qc, self.qf, self.n, i + 1, self.proposals)
            self.crnd = i + 1
            self.sent_2a.add(i + 1)
            net.to_acceptors(("C", self.cid), ("2a", i + 1, v2))


class Net:
    def __init__(self, sim: "FastPaxos") -> None:
        self.sim = sim
        self.k = sim.k
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

    def to_learners_and_coord(self, src: tuple, msg: tuple) -> None:
        self.send(src, ("C", coord_of(msg[1], self.k)), msg)
        for j in range(self.sim.n_learners):
            self.send(src, ("L", j), msg)

    def record_vote(self, a: int, i: int, v: object) -> None:
        self.sim.votes.setdefault(i, {})[a] = v


class Learner:
    def __init__(self, sim: "FastPaxos") -> None:
        self.sim = sim
        self.votes: dict[int, dict[int, object]] = {}
        self.learned: object = None

    def on_2b(self, i: int, a: int, v: object) -> None:
        self.votes.setdefault(i, {})[a] = v
        need = self.sim.qf if is_fast(i) else self.sim.qc
        if sum(1 for w in self.votes[i].values() if w == v) >= need:  # @line L13
            self.learned = v


@dataclass
class Result:
    chosen: set = field(default_factory=set)
    learned: list = field(default_factory=list)


class FastPaxos:
    def __init__(self, n: int, qc: int, qf: int, values: list, seed: int, k: int = 2,
                 n_learners: int = 2, drop: float = 0.0, dup: float = 0.0,
                 crash_prob: float = 0.0, max_acceptor_crashes: int = 0,
                 timeout_prob: float = 0.03, stable_after: int | None = None,
                 max_steps: int = 3000) -> None:
        self.n, self.qc, self.qf, self.k = n, qc, qf, k
        self.values = values
        self.rng = random.Random(seed)
        self.drop, self.dup, self.crash_prob = drop, dup, crash_prob
        self.max_acceptor_crashes = max_acceptor_crashes
        self.timeout_prob, self.stable_after, self.max_steps = timeout_prob, stable_after, max_steps
        self.n_learners = n_learners
        self.crashed: set[tuple] = set()
        self.votes: dict[int, dict[int, object]] = {}
        self.acceptors = [Acceptor(a) for a in range(n)]
        self.coords = [Coordinator(c, n, k, qc, qf) for c in range(k)]
        self.learners = [Learner(self) for _ in range(n_learners)]
        self.net = Net(self)

    def propose_all(self) -> None:
        for p, v in enumerate(self.values):
            for a in range(self.n):
                self.net.send(("P", p), ("A", a), ("prop", v))
            for c in range(self.k):
                self.net.send(("P", p), ("C", c), ("prop", v))

    def deliver(self, dst: tuple, msg: tuple) -> None:
        if dst in self.crashed:
            return
        kind = msg[0]
        if dst[0] == "A":
            a = self.acceptors[dst[1]]
            if kind == "1a":
                a.on_1a(self.net, msg[1])
            elif kind == "2a":
                a.on_2a(self.net, msg[1], msg[2])
            else:
                a.on_proposal(self.net, msg[1])
        elif dst[0] == "C":
            c = self.coords[dst[1]]
            if kind == "1b":
                c.on_1b(self.net, *msg[1:])
            elif kind == "2b":
                c.on_2b(self.net, *msg[1:])
            elif msg[1] not in c.proposals:
                c.proposals.append(msg[1])
        else:
            self.learners[dst[1]].on_2b(*msg[1:])

    def max_round(self) -> int:
        return max([a.rnd for a in self.acceptors] + [c.crnd for c in self.coords])

    def run(self) -> Result:
        self.propose_all()
        for c in self.coords:
            c.start(self.net, self.max_round())
        for step in range(self.max_steps):
            stable = self.stable_after is not None and step >= self.stable_after
            if stable:
                self.drop = self.dup = 0.0
                if not self.net.queue:
                    if all(l.learned is not None for l in self.learners):
                        break
                    self.propose_all()  # clients retry
                    self.coords[0].start(self.net, self.max_round())
            else:
                if self.rng.random() < self.timeout_prob:
                    c = self.coords[self.rng.randrange(self.k)]
                    if ("C", c.cid) not in self.crashed:
                        c.start(self.net, self.max_round())
                if self.rng.random() < self.crash_prob:
                    self.crash_one()
            if self.net.queue:
                dst, msg = self.net.queue.pop(self.rng.randrange(len(self.net.queue)))
                self.deliver(dst, msg)
        return self.result()

    def crash_one(self) -> None:
        down = sum(1 for c in self.crashed if c[0] == "A")
        cands = [("C", c) for c in range(1, self.k)]
        if down < self.max_acceptor_crashes:
            cands += [("A", a) for a in range(self.n)]
        if cands:
            self.crashed.add(cands[self.rng.randrange(len(cands))])

    def result(self) -> Result:
        r = Result(learned=[l.learned for l in self.learners if l.learned is not None])
        for i, by_acc in self.votes.items():
            need = self.qf if is_fast(i) else self.qc
            for v in set(by_acc.values()):
                if sum(1 for w in by_acc.values() if w == v) >= need:
                    r.chosen.add(v)
        return r


def safe(r: Result, values: list) -> bool:
    return len(r.chosen) <= 1 and r.chosen <= set(values) and all(v in r.chosen for v in r.learned)


def drain_rounds(sim: FastPaxos, until) -> int:
    """Deliver in synchronous rounds (one round is one message delay) and
    return the number of rounds until the predicate holds."""
    rounds = 0
    while not until():
        batch, sim.net.queue = sim.net.queue, []
        for dst, msg in batch:
            sim.deliver(dst, msg)
        rounds += 1
    return rounds
