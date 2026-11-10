# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-paxos/. The authors are listed in prov/5TRQGX.jsonl.

"""Multi-Paxos in a deterministic discrete event simulator.

A leader runs phase 1 once for all slots, fills the gaps that it finds with
no-ops, and then runs only phase 2 for each new command. The network can lose,
duplicate and reorder messages, and a seeded scheduler fixes each run.

The module also has a small model of a leader lease with drifting clocks.
"""

import random
from dataclasses import dataclass, field

Ballot = tuple[int, int]
NOOP = "no-op"


def majority(n: int) -> int:
    return n // 2 + 1


class Leader:
    def __init__(self, pid: int, n: int) -> None:
        self.pid, self.n = pid, n
        self.round_seen = 0
        self.ballot: Ballot | None = None
        self.active = False
        self.promises: dict[int, dict[int, tuple[Ballot, object]]] = {}
        self.next_slot = 0
        self.pending: list[object] = []  # commands waiting for an active leader

    def start(self, net: "Net") -> None:
        self.round_seen += 1
        self.ballot = (self.round_seen, self.pid)  # @line L1
        self.active, self.promises = False, {}
        net.broadcast(("L", self.pid), ("PREPARE", self.ballot))  # @line L2

    def on_promise(self, net: "Net", a: int, b: Ballot, votes: dict) -> None:
        if b != self.ballot or self.active:
            return
        self.promises[a] = votes
        if len(self.promises) < majority(self.n):  # @line L3
            return
        best: dict[int, tuple[Ballot, object]] = {}
        for vs in self.promises.values():
            for s, (vb, vv) in vs.items():
                if s not in best or vb > best[s][0]:
                    best[s] = (vb, vv)  # @line L4
        top = max(best) + 1 if best else 0
        self.active = True
        for s in range(top):
            v = best[s][1] if s in best else NOOP
            net.broadcast(("L", self.pid), ("ACCEPT", b, s, v))  # @line L5
        self.next_slot = top  # @line L6
        for c in self.pending:
            self.propose(net, c)
        self.pending = []

    def propose(self, net: "Net", c: object) -> None:
        if not self.active:
            self.pending.append(c)
            return
        s = self.next_slot  # @line L7
        self.next_slot += 1
        net.broadcast(("L", self.pid), ("ACCEPT", self.ballot, s, c))  # @line L8

    def on_nack(self, b: Ballot) -> None:
        self.round_seen = max(self.round_seen, b[0])
        if self.ballot is not None and b > self.ballot:
            self.active = False  # a larger ballot exists: this leader is deposed


class Acceptor:
    def __init__(self, aid: int) -> None:
        self.aid = aid
        self.promised: Ballot | None = None
        self.accepted: dict[int, tuple[Ballot, object]] = {}

    def on_prepare(self, net: "Net", b: Ballot) -> None:
        if self.promised is None or b > self.promised:  # @line L9
            self.promised = b
            net.send(("A", self.aid), ("L", b[1]), ("PROMISE", self.aid, b, dict(self.accepted)))  # @line L10
        else:
            net.send(("A", self.aid), ("L", b[1]), ("NACK", self.promised))

    def on_accept(self, net: "Net", b: Ballot, s: int, v: object) -> None:
        if self.promised is None or b >= self.promised:  # @line L11
            self.promised = b
            self.accepted[s] = (b, v)
            net.record_vote(self.aid, b, s, v)
            net.to_learners(("A", self.aid), ("ACCEPTED", self.aid, b, s, v))  # @line L12
        else:
            net.send(("A", self.aid), ("L", b[1]), ("NACK", self.promised))


class Learner:
    def __init__(self, n: int) -> None:
        self.n = n
        self.votes: dict[tuple[Ballot, int], set[int]] = {}
        self.learned: dict[int, object] = {}
        self.applied: list[object] = []

    def on_accepted(self, a: int, b: Ballot, s: int, v: object) -> None:
        self.votes.setdefault((b, s), set()).add(a)
        if len(self.votes[(b, s)]) >= majority(self.n) and s not in self.learned:  # @line L13
            self.learned[s] = v
            while len(self.applied) in self.learned:  # @line L14
                self.applied.append(self.learned[len(self.applied)])


class Net:
    def __init__(self, sim: "MultiPaxos") -> None:
        self.sim = sim
        self.queue: list[tuple[tuple, tuple]] = []
        self.sent = 0

    def send(self, src: tuple, dst: tuple, msg: tuple) -> None:
        s = self.sim
        if src in s.crashed:
            return
        self.sent += 1
        if s.rng.random() < s.drop:
            return
        self.queue.append((dst, msg))
        if s.rng.random() < s.dup:
            self.queue.append((dst, msg))

    def broadcast(self, src: tuple, msg: tuple) -> None:
        for i in range(self.sim.n):
            self.send(src, ("A", i), msg)

    def to_learners(self, src: tuple, msg: tuple) -> None:
        for i in range(len(self.sim.learners)):
            self.send(src, ("X", i), msg)

    def record_vote(self, a: int, b: Ballot, s: int, v: object) -> None:
        self.sim.votes.setdefault((b, s), {})[a] = v


@dataclass
class Result:
    learned: list[dict[int, object]] = field(default_factory=list)
    applied: list[list[object]] = field(default_factory=list)
    chosen: dict[int, set] = field(default_factory=dict)
    submitted: set = field(default_factory=set)


class MultiPaxos:
    """A seeded run with leaders 0..k-1, n acceptors and l learners.

    Commands arrive at random leaders. Leaders time out and start new ballots,
    leaders and a minority of acceptors crash. After stable_after steps there
    is no loss, and only leader 0 acts; it then gets every later command.
    """

    def __init__(self, n: int, k: int, seed: int, n_learners: int = 2, drop: float = 0.0,
                 dup: float = 0.0, crash_prob: float = 0.0, timeout_prob: float = 0.02,
                 n_commands: int = 6, stable_after: int | None = None, max_steps: int = 4000) -> None:
        self.n = n
        self.rng = random.Random(seed)
        self.drop, self.dup, self.crash_prob = drop, dup, crash_prob
        self.timeout_prob, self.stable_after, self.max_steps = timeout_prob, stable_after, max_steps
        self.leaders = [Leader(i, n) for i in range(k)]
        self.acceptors = [Acceptor(i) for i in range(n)]
        self.learners = [Learner(n) for _ in range(n_learners)]
        self.crashed: set[tuple] = set()
        self.votes: dict[tuple[Ballot, int], dict[int, object]] = {}
        self.net = Net(self)
        self.to_submit = [f"c{i}" for i in range(n_commands)]
        self.late = [f"d{i}" for i in range(n_commands)]  # sent to leader 0 once stable
        self.late_all = list(self.late)

    def deliver(self, dst: tuple, msg: tuple) -> None:
        if dst in self.crashed:
            return
        kind = msg[0]
        if dst[0] == "A":
            a = self.acceptors[dst[1]]
            if kind == "PREPARE":
                a.on_prepare(self.net, msg[1])
            else:
                a.on_accept(self.net, msg[1], msg[2], msg[3])
        elif dst[0] == "L":
            ld = self.leaders[dst[1]]
            if kind == "PROMISE":
                ld.on_promise(self.net, msg[1], msg[2], msg[3])
            else:
                ld.on_nack(msg[1])
        else:
            self.learners[dst[1]].on_accepted(*msg[1:])

    def run(self) -> Result:
        for ld in self.leaders:
            ld.start(self.net)
        for step in range(self.max_steps):
            stable = self.stable_after is not None and step >= self.stable_after
            if stable:
                self.drop = self.dup = 0.0
                ld = self.leaders[0]
                if self.late:
                    ld.propose(self.net, self.late.pop())
                if not self.net.queue and not self.done():
                    ld.start(self.net)
                    self.retry()
            else:
                if self.to_submit and self.rng.random() < 0.05:
                    ld = self.leaders[self.rng.randrange(len(self.leaders))]
                    if ("L", ld.pid) not in self.crashed:
                        ld.propose(self.net, self.to_submit.pop())
                if self.rng.random() < self.timeout_prob:
                    ld = self.leaders[self.rng.randrange(len(self.leaders))]
                    if ("L", ld.pid) not in self.crashed:
                        ld.start(self.net)
                if self.rng.random() < self.crash_prob:
                    self.crash_one()
            if self.net.queue:
                dst, msg = self.net.queue.pop(self.rng.randrange(len(self.net.queue)))
                self.deliver(dst, msg)
            elif stable and self.done():
                break
        return self.result()

    def crash_one(self) -> None:
        down = sum(1 for c in self.crashed if c[0] == "A")
        cands = [("L", i) for i in range(1, len(self.leaders))]
        if down < (self.n - 1) // 2:
            cands += [("A", i) for i in range(self.n)]
        who = cands[self.rng.randrange(len(cands))]
        self.crashed.add(who)

    def done(self) -> bool:
        """All commands sent once the run is stable are applied everywhere."""
        if self.late:
            return False
        return all(set(self.late_all) <= set(l.applied) for l in self.learners)

    def retry(self) -> None:
        """A client retries each late command that learner 0 has not applied."""
        ld = self.leaders[0]
        for c in self.late_all:
            if c not in self.learners[0].applied and c not in ld.pending:
                ld.pending.append(c)

    def result(self) -> Result:
        r = Result()
        r.learned = [dict(l.learned) for l in self.learners]
        r.applied = [list(l.applied) for l in self.learners]
        maj = majority(self.n)
        for (b, s), by_acc in self.votes.items():
            for v in set(by_acc.values()):
                if sum(1 for x in by_acc.values() if x == v) >= maj:
                    r.chosen.setdefault(s, set()).add(v)
        return r


def slots_agree(r: Result) -> bool:
    """At most one value is chosen per slot, and learners agree with it."""
    if any(len(vs) > 1 for vs in r.chosen.values()):
        return False
    for learned in r.learned:
        for s, v in learned.items():
            if r.chosen.get(s) != {v}:
                return False
    logs = sorted(r.applied, key=len)
    return all(logs[i] == logs[-1][: len(logs[i])] for i in range(len(logs)))


def steady_state_delays(n: int, n_learners: int) -> int:
    """Message delays from a command at the leader until all learners learn it.

    The run is synchronous: each round delivers every message in flight, so
    one round is one message delay. Phase 1 is done before the command comes.
    """
    sim = MultiPaxos(n, 1, seed=0, n_learners=n_learners)
    ld = sim.leaders[0]
    ld.start(sim.net)
    while sim.net.queue:
        batch, sim.net.queue = sim.net.queue, []
        for dst, msg in batch:
            sim.deliver(dst, msg)
    assert ld.active
    ld.propose(sim.net, "cmd")
    rounds = 0
    while not all(0 in l.learned for l in sim.learners):
        batch, sim.net.queue = sim.net.queue, []
        for dst, msg in batch:
            sim.deliver(dst, msg)
        rounds += 1
    return rounds


def lease_overlap(rho: float, true_rho: float, lease: float, seed: int, trials: int = 200) -> bool:
    """Return True if some trial lets an old leader read locally after a new
    leader has finished phase 1.

    Each acceptor promises not to join a new ballot for `lease` units of its
    own clock, counted from when it receives the request. The leader starts
    its own timer when it sends the request, and uses the lease for
    lease * (1 - rho) / (1 + rho) units of its own clock. The true clock rates
    lie in [1 - true_rho, 1 + true_rho]; the bound is safe when true_rho <= rho.
    """
    rng = random.Random(seed)
    n = 5
    q = majority(n)
    use = lease * (1 - rho) / (1 + rho)
    for _ in range(trials):
        rates = [rng.uniform(1 - true_rho, 1 + true_rho) for _ in range(n + 1)]
        if rng.random() < 0.5:  # push the rates to the edges of the range
            rates = [1 - true_rho if rng.random() < 0.5 else 1 + true_rho for _ in range(n + 1)]
        delays = [rng.uniform(0.0, 0.2 * lease) for _ in range(n)]
        granted = rng.sample(range(n), q)
        # Real time at which each acceptor may promise a new leader.
        free = [delays[i] + lease / rates[i] if i in granted else 0.0 for i in range(n)]
        new_leader_ready = sorted(free)[q - 1]  # the earliest majority of free acceptors
        old_leader_end = use / rates[n]
        if old_leader_end > new_leader_ready:
            return True
    return False
