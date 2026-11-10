# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paxos/. The authors are listed in prov/7W88GQ.jsonl.

"""Single-decree Paxos in a deterministic discrete event simulator.

The model is asynchronous message passing with crash failures. The network
can lose, duplicate and reorder messages. A seeded scheduler picks the next
message to deliver, so a run is fixed by its seed. Proposers, acceptors and
learners are separate processes, each with a handler per message type.

A ballot is a pair (round, proposer id), compared as a tuple, so two
proposers never use the same ballot.
"""

import random
from dataclasses import dataclass, field

Ballot = tuple[int, int]


def majority(n: int) -> int:
    """The size of a majority quorum of n acceptors."""
    return n // 2 + 1


class Proposer:
    def __init__(self, pid: int, value: object, n: int, follow_rule: bool = True) -> None:
        self.pid = pid
        self.value = value
        self.n = n
        self.follow_rule = follow_rule  # False gives the broken variant of the tests
        self.round_seen = 0
        self.ballot: Ballot | None = None
        self.phase = 0
        self.promises: dict[int, tuple[Ballot | None, object]] = {}

    def start(self, net: "Network") -> None:
        self.round_seen += 1
        self.ballot = (self.round_seen, self.pid)  # @line L2
        self.promises = {}
        self.phase = 1
        net.broadcast(("P", self.pid), "acceptors", ("PREPARE", self.ballot))  # @line L3

    def on_promise(self, net: "Network", acc: int, b: Ballot, vb: Ballot | None, vv: object) -> None:
        if b != self.ballot or self.phase != 1:  # @line L4
            return
        self.promises[acc] = (vb, vv)  # @line L5
        if len(self.promises) >= majority(self.n):  # @line L6
            voted = [(vb2, vv2) for vb2, vv2 in self.promises.values() if vb2 is not None]
            if voted and self.follow_rule:
                v = max(voted, key=lambda t: t[0])[1]  # @line L7
            else:
                v = self.value  # @line L8
            self.phase = 2
            net.broadcast(("P", self.pid), "acceptors", ("ACCEPT", b, v))  # @line L9

    def on_nack(self, promised: Ballot) -> None:
        self.round_seen = max(self.round_seen, promised[0])


class Acceptor:
    def __init__(self, aid: int) -> None:
        self.aid = aid
        self.promised: Ballot | None = None  # kept in stable storage
        self.vb: Ballot | None = None
        self.vv: object = None

    def on_prepare(self, net: "Network", src: tuple, b: Ballot) -> None:
        if self.promised is None or b > self.promised:  # @line L10
            self.promised = b  # @line L11
            net.send(("A", self.aid), src, ("PROMISE", self.aid, b, self.vb, self.vv))
        else:
            net.send(("A", self.aid), src, ("NACK", self.promised))  # @line L12

    def on_accept(self, net: "Network", src: tuple, b: Ballot, v: object) -> None:
        if self.promised is None or b >= self.promised:  # @line L13
            self.promised, self.vb, self.vv = b, b, v  # @line L14
            net.record_vote(self.aid, b, v)
            net.broadcast(("A", self.aid), "learners", ("ACCEPTED", self.aid, b, v))
        else:
            net.send(("A", self.aid), src, ("NACK", self.promised))  # @line L15


class Learner:
    def __init__(self, lid: int, n: int) -> None:
        self.lid = lid
        self.n = n
        self.votes: dict[Ballot, set[int]] = {}
        self.value_at: dict[Ballot, object] = {}
        self.learned: object = None

    def on_accepted(self, acc: int, b: Ballot, v: object) -> None:
        self.votes.setdefault(b, set()).add(acc)  # @line L16
        self.value_at[b] = v
        if len(self.votes[b]) >= majority(self.n) and self.learned is None:
            self.learned = v  # @line L17


@dataclass
class Result:
    chosen: set = field(default_factory=set)
    learned: dict = field(default_factory=dict)
    proposed: set = field(default_factory=set)
    values_per_ballot_ok: bool = True
    steps: int = 0
    messages: int = 0


class Network:
    """The message queue, the scheduler and the fault injector."""

    def __init__(self, sim: "Paxos") -> None:
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

    def broadcast(self, src: tuple, group: str, msg: tuple) -> None:
        s = self.sim
        role, count = ("A", s.n) if group == "acceptors" else ("L", s.n_learners)
        for i in range(count):
            # A crash in the middle of a broadcast: only some messages go out.
            if s.rng.random() < s.crash_mid and s.may_crash(src):
                s.crashed.add(src)
                return
            self.send(src, (role, i), msg)

    def record_vote(self, aid: int, b: Ballot, v: object) -> None:
        s = self.sim
        s.votes.setdefault(b, {})[aid] = v


class Paxos:
    """One run of single-decree Paxos, fixed by its seed.

    inputs[i] is the value of proposer i. The schedule is "random", "fifo",
    "lifo" or "slow" (the messages of process slow_target go last).
    max_acceptor_crashes bounds the crashed acceptors; proposer 0 never
    crashes when keep_leader is true. After stable_after steps the run has no
    loss and no duplication, and only proposer 0 times out, which models the
    distinguished leader of the liveness argument.
    """

    def __init__(self, n: int, inputs: list, seed: int, n_learners: int = 2,
                 drop: float = 0.0, dup: float = 0.0, schedule: str = "random",
                 slow_target: tuple | None = None, crash_prob: float = 0.0,
                 crash_mid: float = 0.0, max_acceptor_crashes: int | None = None,
                 timeout_prob: float = 0.05, stable_after: int | None = None,
                 keep_leader: bool = True, follow_rule: bool = True,
                 max_steps: int = 3000) -> None:
        self.n = n
        self.n_learners = n_learners
        self.rng = random.Random(seed)
        self.drop, self.dup = drop, dup
        self.schedule, self.slow_target = schedule, slow_target
        self.crash_prob, self.crash_mid = crash_prob, crash_mid
        self.max_acceptor_crashes = (n - 1) // 2 if max_acceptor_crashes is None else max_acceptor_crashes
        self.timeout_prob, self.stable_after = timeout_prob, stable_after
        self.keep_leader = keep_leader
        self.max_steps = max_steps
        self.crashed: set[tuple] = set()
        self.votes: dict[Ballot, dict[int, object]] = {}
        self.proposers = [Proposer(i, x, n, follow_rule) for i, x in enumerate(inputs)]
        self.acceptors = [Acceptor(i) for i in range(n)]
        self.learners = [Learner(i, n) for i in range(n_learners)]
        self.net = Network(self)

    def may_crash(self, who: tuple) -> bool:
        if who in self.crashed:
            return False
        if who[0] == "P":
            return not (self.keep_leader and who[1] == 0)
        if who[0] == "A":
            down = sum(1 for c in self.crashed if c[0] == "A")
            return down < self.max_acceptor_crashes
        return False

    def stable(self, step: int) -> bool:
        return self.stable_after is not None and step >= self.stable_after

    def pick(self) -> tuple[tuple, tuple]:
        q = self.net.queue
        if self.schedule == "fifo":
            return q.pop(0)
        if self.schedule == "lifo":
            return q.pop()
        if self.schedule == "slow" and self.slow_target is not None:
            fast = [i for i, (d, m) in enumerate(q) if d != self.slow_target and m[1] != self.slow_target[1]]
            if fast:
                return q.pop(fast[self.rng.randrange(len(fast))])
        return q.pop(self.rng.randrange(len(q)))

    def deliver(self, dst: tuple, msg: tuple) -> None:
        if dst in self.crashed:
            return
        kind = msg[0]
        if dst[0] == "A":
            a = self.acceptors[dst[1]]
            src = ("P", msg[1][1])  # the proposer id is part of the ballot
            if kind == "PREPARE":
                a.on_prepare(self.net, src, msg[1])
            elif kind == "ACCEPT":
                a.on_accept(self.net, src, msg[1], msg[2])
        elif dst[0] == "P":
            p = self.proposers[dst[1]]
            if kind == "PROMISE":
                p.on_promise(self.net, msg[1], msg[2], msg[3], msg[4])
            elif kind == "NACK":
                p.on_nack(msg[1])
        elif dst[0] == "L" and kind == "ACCEPTED":
            self.learners[dst[1]].on_accepted(msg[1], msg[2], msg[3])

    def all_learned(self) -> bool:
        return all(l.learned is not None for l in self.learners)

    def run(self) -> Result:
        for p in self.proposers:
            p.start(self.net)  # @line L1
        step = 0
        while step < self.max_steps:
            step += 1
            stable = self.stable(step)
            if stable:
                self.drop = self.dup = 0.0
            # Seeded crashes of proposers and acceptors.
            if not stable and self.rng.random() < self.crash_prob:
                cands = [("P", i) for i in range(len(self.proposers))] + [("A", i) for i in range(self.n)]
                who = cands[self.rng.randrange(len(cands))]
                if self.may_crash(who):
                    self.crashed.add(who)
            # Timeouts: a proposer gives up its ballot and starts a higher one.
            if stable:
                leader = self.proposers[0]
                if not self.net.queue and not self.all_learned() and ("P", 0) not in self.crashed:
                    leader.start(self.net)
            elif self.rng.random() < self.timeout_prob:
                p = self.proposers[self.rng.randrange(len(self.proposers))]
                if ("P", p.pid) not in self.crashed:
                    p.start(self.net)
            if self.net.queue:
                dst, msg = self.pick()
                self.deliver(dst, msg)
            elif stable and self.all_learned():
                break
        return self.result(step)

    def result(self, steps: int) -> Result:
        r = Result(steps=steps, messages=self.net.sent)
        r.proposed = {p.value for p in self.proposers}
        maj = majority(self.n)
        for b, by_acc in self.votes.items():
            vals = set(by_acc.values())
            if len(vals) > 1:
                r.values_per_ballot_ok = False
            for v in vals:
                if sum(1 for x in by_acc.values() if x == v) >= maj:
                    r.chosen.add(v)
        r.learned = {l.lid: l.learned for l in self.learners if l.learned is not None}
        return r


def run_paxos(n: int, inputs: list, seed: int, **kw) -> Result:
    """Run one seeded execution and return what was chosen and learned."""
    return Paxos(n, inputs, seed, **kw).run()


def safe(r: Result) -> bool:
    """Agreement and validity: at most one value is chosen, it was proposed,
    and every learner learned that value."""
    if not r.values_per_ballot_ok or len(r.chosen) > 1:
        return False
    if not r.chosen <= r.proposed:
        return False
    return all(v in r.chosen for v in r.learned.values())
