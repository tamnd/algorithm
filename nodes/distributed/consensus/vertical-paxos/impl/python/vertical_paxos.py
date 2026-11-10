# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertical-paxos/. The authors are listed in prov/53MYYW.jsonl.
"""Vertical Paxos I and II for one consensus instance, in a seeded simulator.

Each ballot has its own configuration: a set of acceptors with read quorums
and write quorums. An external master, assumed reliable, starts ballots,
picks configurations and tracks complete (VP I) or activated (VP II) ballots.
"""

import random
from typing import Optional

ALL_SAFE = None  # the special value AllSafe, and also the vote None


class Config:
    """kind "pb": any one acceptor is a read quorum, all of them the write
    quorum. kind "maj": majorities for both. kind "bad": any one acceptor for
    both, which breaks the rule that read and write quorums meet."""

    def __init__(self, members: frozenset, kind: str) -> None:
        self.members, self.kind = frozenset(members), kind

    def is_read_quorum(self, s: set) -> bool:
        s = set(s) & self.members
        if self.kind in ("pb", "bad"):
            return len(s) >= 1
        return 2 * len(s) > len(self.members)

    def is_write_quorum(self, s: set) -> bool:
        s = set(s) & self.members
        if self.kind == "pb":
            return s == self.members
        if self.kind == "bad":
            return len(s) >= 1
        return 2 * len(s) > len(self.members)


class Acceptor:
    def __init__(self, sim: "VerticalPaxos", a: int) -> None:
        self.sim, self.a = sim, a
        self.max_ballot = 0
        self.vote: dict = {}

    def on_1a(self, b: int, c: int) -> None:
        if b >= self.max_ballot:
            self.max_ballot = b  # @line L11
            self.sim.send(("L", b), ("1b", self.a, b, c, self.vote.get(c)))

    def on_2a(self, b: int, v: object) -> None:
        if b >= self.max_ballot and b not in self.vote:
            self.max_ballot = b
            self.vote[b] = v  # @line L12
            self.sim.send(("L", b), ("2b", self.a, b, v))
            self.sim.votes.setdefault(b, {})[self.a] = v


class Leader:
    def __init__(self, sim: "VerticalPaxos", b: int, low: int, value: object) -> None:
        self.sim, self.b = sim, b
        self.low = low  # completeBal (VP I) or prevBal (VP II)
        self.value = value  # the client value used if all values are safe
        self.safe = ALL_SAFE  # @line L4
        self.c = b - 1 if sim.variant == 1 else low
        self.none_from: set = set()
        self.acks: set = set()
        self.state = "phase1"
        self.alive = True
        self.queried: set = set()

    def ask(self) -> None:
        if self.sim.variant == 1 and self.c < self.low:
            self.end_phase1()
            return
        self.queried.add(self.c)
        for a in self.sim.config[self.c].members:  # @line L5
            self.sim.send(("A", a), ("1a", self.b, self.c))

    def on_1b(self, a: int, b: int, c: int, v: object) -> None:
        if self.state != "phase1" or b != self.b or c != self.c:
            return
        if v is not None:
            self.safe = v  # @line L6
            self.end_phase1()
            return
        self.none_from.add(a)
        if self.sim.config[c].is_read_quorum(self.none_from):
            self.none_from = set()  # @line L7
            if self.sim.variant == 2:
                self.end_phase1()
            else:
                self.c -= 1
                self.ask()

    def end_phase1(self) -> None:
        if self.safe is not ALL_SAFE:
            self.state = "phase2"  # @line L8
            self.send_2a(self.safe)
        else:
            self.complete()

    def on_2b(self, a: int, b: int, v: object) -> None:
        if self.state != "phase2" or b != self.b:
            return
        self.acks.add(a)
        if self.sim.config[b].is_write_quorum(self.acks):
            self.complete()

    def complete(self) -> None:
        self.state = "complete"  # @line L9
        self.sim.master_complete(self.b, self.low)
        if self.sim.variant == 1:
            self.after_complete()

    def on_activated(self) -> None:
        self.after_complete()

    def after_complete(self) -> None:
        self.state = "done"
        if self.safe is ALL_SAFE:
            self.send_2a(self.value)  # @line L10

    def send_2a(self, v: object) -> None:
        for a in self.sim.config[self.b].members:
            self.sim.send(("A", a), ("2a", self.b, v))


class VerticalPaxos:
    def __init__(self, variant: int, seed: int, n_procs: int = 5, kinds: tuple = ("pb", "maj"),
                 dup: float = 0.0, crashes: int = 0, crash_prob: float = 0.0,
                 leader_fail: float = 0.0, new_ballot_prob: float = 0.0,
                 max_steps: int = 5000, after: int = 0) -> None:
        assert variant in (1, 2)
        self.after = after
        self.variant = variant
        self.rng = random.Random(seed)
        self.n_procs = n_procs
        self.kinds = kinds
        self.dup = dup
        self.crashes_left, self.crash_prob = crashes, crash_prob
        self.leader_fail = leader_fail
        self.new_ballot_prob = new_ballot_prob
        self.max_steps = max_steps
        self.acceptors = [Acceptor(self, a) for a in range(n_procs)]
        self.crashed: set = set()
        self.net: list = []
        self.votes: dict = {}
        self.config: dict = {0: self.pick_config()}
        self.leaders: dict = {}
        # Master state.
        self.complete_bal = 0
        self.cur_bal = 0
        self.activated = {0}
        self.next_ballot = 1

    def pick_config(self) -> Config:
        kind = self.rng.choice(self.kinds)
        live = [p for p in range(self.n_procs) if p not in self.crashed]
        size = 3 if kind == "maj" else self.rng.choice((2, 3))
        size = min(size, len(live))
        return Config(frozenset(self.rng.sample(live, size)), kind)

    def new_ballot(self) -> int:
        b = self.next_ballot  # @line L1
        self.next_ballot += 1
        self.config[b] = self.pick_config()
        low = self.complete_bal if self.variant == 1 else self.cur_bal
        ld = Leader(self, b, low, f"v{b}")
        self.leaders[b] = ld
        ld.ask()
        return b

    def master_complete(self, b: int, prev: int) -> None:
        if self.variant == 1:
            self.complete_bal = max(self.complete_bal, b)  # @line L2
        elif prev == self.cur_bal:
            self.cur_bal = b  # @line L3
            self.activated.add(b)
            self.send(("L", b), ("activated",))

    def send(self, dst: tuple, msg: tuple) -> None:
        self.net.append((dst, msg))
        if self.rng.random() < self.dup:
            self.net.append((dst, msg))

    def deliver(self, dst: tuple, msg: tuple) -> None:
        if dst[0] == "A":
            if dst[1] in self.crashed:
                return
            acc = self.acceptors[dst[1]]
            if msg[0] == "1a":
                acc.on_1a(msg[1], msg[2])
            else:
                acc.on_2a(msg[1], msg[2])
            return
        ld = self.leaders[dst[1]]
        if not ld.alive:
            return
        if msg[0] == "1b":
            ld.on_1b(*msg[1:])
        elif msg[0] == "2b":
            ld.on_2b(*msg[1:])
        else:
            ld.on_activated()

    def chosen_in(self, b: int) -> set:
        """@line L13 the values chosen in ballot b: voted by a write quorum."""
        if self.variant == 2 and b not in self.activated:
            return set()
        return self.raw_chosen_in(b)

    def raw_chosen_in(self, b: int) -> set:
        out = set()
        for v in set(self.votes.get(b, {}).values()):
            voters = {a for a, w in self.votes[b].items() if w == v}
            if self.config[b].is_write_quorum(voters):
                out.add(v)
        return out

    def chosen(self) -> set:
        return set().union(*(self.chosen_in(b) for b in self.votes)) if self.votes else set()

    def raw_chosen(self) -> set:
        return set().union(*(self.raw_chosen_in(b) for b in self.votes)) if self.votes else set()

    def run(self) -> "VerticalPaxos":
        self.new_ballot()
        for _ in range(self.max_steps):
            if self.crashes_left and self.rng.random() < self.crash_prob:
                p = self.rng.randrange(self.n_procs)
                if p not in self.crashed:
                    self.crashed.add(p)
                    self.crashes_left -= 1
            if self.leader_fail and self.rng.random() < self.leader_fail:
                live = [ld for ld in self.leaders.values() if ld.alive and ld.state != "done"]
                if live:
                    self.rng.choice(live).alive = False
            if self.new_ballot_prob and self.rng.random() < self.new_ballot_prob:
                self.new_ballot()
            if self.net:
                i = self.rng.randrange(len(self.net))
                self.net[i], self.net[-1] = self.net[-1], self.net[i]
                self.deliver(*self.net.pop())
                continue
            if self.chosen():
                if self.after <= 0:
                    break
                self.after -= 1  # more ballots after the choice, to test safety
            self.new_ballot()  # the master reacts to a stalled ballot
        return self
