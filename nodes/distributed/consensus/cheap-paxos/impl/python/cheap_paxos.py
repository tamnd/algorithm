# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cheap-paxos/. The authors are listed in prov/DJBX02.jsonl.

"""Cheap Paxos in a deterministic discrete event simulator.

There are f + 1 main processors and f auxiliary processors. Each slot of the
log is one Paxos instance whose quorums come from the configuration of that
slot: the set of all mains, or a majority of all processors that holds at
least one main. The configuration of slot s + 1 is the configuration of slot
s, changed by the command chosen in slot s (the window alpha is 1). While all
mains are up, the auxiliary processors get no messages at all.
"""

import random
from dataclasses import dataclass

Ballot = tuple[int, int]


@dataclass(frozen=True)
class Config:
    mains: frozenset
    aux: frozenset

    @property
    def members(self) -> frozenset:
        return self.mains | self.aux

    def is_quorum(self, s: frozenset) -> bool:
        if self.mains <= s:
            return True
        g = self.members
        return len(s & g) * 2 > len(g) and bool(s & self.mains)

    def apply(self, cmd: object) -> "Config":
        """A command ("remove", p) removes main p. Auxiliaries are dropped while
        the mains are fewer than half of the processors, so that the set of
        mains still meets every majority."""
        if not (isinstance(cmd, tuple) and cmd[0] == "remove" and cmd[1] in self.mains):
            return self
        if len(self.mains) == 1:  # the last main is never removed
            return self
        mains, aux = self.mains - {cmd[1]}, set(self.aux)
        while aux and len(mains) * 2 < len(mains) + len(aux):
            aux.remove(max(aux))
        return Config(frozenset(mains), frozenset(aux))


def initial_config(f: int) -> Config:
    return Config(frozenset(range(f + 1)), frozenset(range(f + 1, 2 * f + 1)))


def config_at(c0: Config, decided: dict, s: int) -> Config | None:
    """The configuration of slot s, if the slots before s are known."""
    c = c0
    for t in range(s):
        if t not in decided:
            return None
        c = c.apply(decided[t])
    return c


class Process:
    """A processor: an acceptor, and a leader too if it is a main."""

    def __init__(self, pid: int, sim: "CheapPaxos") -> None:
        self.pid, self.sim = pid, sim
        self.promised: Ballot | None = None
        self.accepted: dict[int, tuple[Ballot, object]] = {}
        self.decided: dict[int, object] = {}
        self.forgot_below = 0
        # Leader state.
        self.leading = False
        self.round_seen = 0
        self.ballot: Ballot | None = None
        self.slot = 0
        self.promises: dict[int, tuple[dict, dict]] = {}
        self.acks: set[int] = set()
        self.value: object = None
        self.mine: object = None
        self.use_aux = False
        self.pending_remove: list[int] = []

    # Acceptor part.
    def on_prepare(self, b: Ballot, s0: int) -> None:
        if s0 < self.forgot_below:  # this auxiliary no longer knows these slots
            self.sim.send(self.pid, b[1], ("NACK", self.promised or b))
            return
        if self.promised is None or b >= self.promised:  # @line L10
            self.promised = b
            votes = {s: x for s, x in self.accepted.items() if s >= s0}
            dec = {s: v for s, v in self.decided.items() if s >= s0}
            self.sim.send(self.pid, b[1], ("PROMISE", b, self.pid, votes, dec))
        else:
            self.sim.send(self.pid, b[1], ("NACK", self.promised))

    def on_accept(self, b: Ballot, s: int, v: object) -> None:
        if s < self.forgot_below:
            return
        if self.promised is None or b >= self.promised:  # @line L11
            self.promised = b
            self.accepted[s] = (b, v)
            self.sim.record_vote(self.pid, s, b, v)
            self.sim.send(self.pid, b[1], ("ACCEPTED", b, s, self.pid))
        else:
            self.sim.send(self.pid, b[1], ("NACK", self.promised))

    def on_decide(self, s: int, v: object) -> None:
        if s >= self.forgot_below:
            self.decided[s] = v  # @line L12

    def on_forget(self, s: int) -> None:
        self.forgot_below = max(self.forgot_below, s)  # @line L13
        self.accepted = {t: x for t, x in self.accepted.items() if t >= s}
        self.decided = {t: v for t, v in self.decided.items() if t >= s}

    # Leader part.
    def first_open(self) -> int:
        s = 0
        while s in self.decided:
            s += 1
        return s

    def config(self, s: int) -> Config | None:
        return config_at(self.sim.c0, self.decided, s)

    def targets(self, c: Config) -> frozenset:
        return c.members if self.use_aux else c.mains

    def start(self) -> None:
        self.round_seen += 1
        self.ballot = (self.round_seen, self.pid)  # @line L1
        self.leading, self.promises, self.acks = True, {}, set()
        if self.mine is not None:
            self.sim.pool.insert(0, self.mine)
        self.mine, self.value = None, None
        self.slot = self.first_open()
        self.prepare()

    def prepare(self) -> None:
        c = self.config(self.slot)
        for q in self.targets(c):
            self.sim.send(self.pid, q, ("PREPARE", self.ballot, self.slot))

    def on_promise(self, b: Ballot, a: int, votes: dict, dec: dict) -> None:
        if not self.leading or b != self.ballot:
            return
        self.promises[a] = (votes, dec)  # @line L2
        self.try_propose()

    def try_propose(self) -> None:
        if self.value is not None:
            return
        c = self.config(self.slot)
        if c is None or not c.is_quorum(frozenset(self.promises)):  # @line L3
            return
        s = self.slot
        reported = [d[s] for _, d in self.promises.values() if s in d]
        votes = [vs[s] for vs, _ in self.promises.values() if s in vs]
        if reported:
            v = reported[0]
        elif votes:
            v = max(votes, key=lambda t: t[0])[1]  # @line L4
        elif self.pending_remove:
            v = ("remove", self.pending_remove[0])
        elif self.sim.pool:
            v = self.mine = self.sim.pool.pop(0)
        else:
            return
        self.value, self.acks = v, set()
        for q in self.targets(c):
            self.sim.send(self.pid, q, ("ACCEPT", self.ballot, s, v))  # @line L5

    def on_accepted(self, b: Ballot, s: int, a: int) -> None:
        if not self.leading or b != self.ballot or s != self.slot or self.value is None:
            return
        self.acks.add(a)
        c = self.config(s)
        if not c.is_quorum(frozenset(self.acks)):  # @line L6
            return
        v = self.value
        self.decided[s] = v
        for q in c.mains:
            self.sim.send(self.pid, q, ("DECIDE", s, v))
        if isinstance(v, tuple) and v[0] == "remove" and v[1] in self.pending_remove:
            self.pending_remove.remove(v[1])
        if self.mine is not None and self.mine != v:
            self.sim.pool.insert(0, self.mine)
        self.mine, self.value = None, None
        self.slot = s + 1
        c2 = self.config(self.slot)  # @line L8
        if c2 != c:
            # Bring the new mains up to date, then let the auxiliaries forget.
            for q in c2.mains:
                for t in range(self.slot):
                    self.sim.send(self.pid, q, ("DECIDE", t, self.decided[t]))
            self.sim.forget_after_decides.append((self.slot, frozenset(c.aux), self.pid))  # @line L9
        if not self.pending_remove:
            self.use_aux = False  # all failed mains are removed: the auxiliaries rest again
        if c2.is_quorum(frozenset(self.promises)):
            self.try_propose()
        else:
            self.promises = {}
            self.prepare()

    def on_nack(self, b: Ballot) -> None:
        self.round_seen = max(self.round_seen, b[0])
        if self.ballot is not None and b > self.ballot and self.leading:
            self.leading = False
            if self.mine is not None:
                self.sim.pool.insert(0, self.mine)
            self.mine, self.value = None, None

    def timeout(self) -> None:
        """Nothing is in flight and the leader is stuck: include the
        auxiliaries and resend the current phase."""
        self.use_aux = True
        c = self.config(self.slot)
        heard = self.promises if self.value is None else self.acks
        for m in sorted(c.mains):
            if m != self.pid and m not in heard and m not in self.pending_remove:
                self.pending_remove.append(m)  # @line L7
        if self.value is None:
            for q in c.members:
                self.sim.send(self.pid, q, ("PREPARE", self.ballot, self.slot))
        else:
            for q in c.members:
                self.sim.send(self.pid, q, ("ACCEPT", self.ballot, self.slot, self.value))


class CheapPaxos:
    def __init__(self, f: int, seed: int, n_commands: int = 6, dup: float = 0.0,
                 drop: float = 0.0, crashes: int = 0, crash_prob: float = 0.0,
                 duel_prob: float = 0.0, max_steps: int = 20000) -> None:
        self.f = f
        self.c0 = initial_config(f)
        self.rng = random.Random(seed)
        self.dup, self.drop = dup, drop
        self.crashes_left, self.crash_prob, self.duel_prob = crashes, crash_prob, duel_prob
        self.max_steps = max_steps
        self.procs = [Process(p, self) for p in range(2 * f + 1)]
        self.crashed: set[int] = set()
        self.queue: list[tuple[int, tuple]] = []
        self.pool: list[object] = [f"c{i}" for i in range(n_commands)]
        self.commands = list(self.pool)
        self.votes: dict[int, dict[Ballot, dict[int, object]]] = {}
        self.forget_after_decides: list[tuple[int, frozenset]] = []
        self.aux_messages = 0

    def send(self, src: int, dst: int, msg: tuple) -> None:
        if src in self.crashed or self.rng.random() < self.drop:
            return
        if dst in self.c0.aux:
            self.aux_messages += 1
        self.queue.append((dst, msg))
        if self.rng.random() < self.dup:
            self.queue.append((dst, msg))

    def record_vote(self, a: int, s: int, b: Ballot, v: object) -> None:
        self.votes.setdefault(s, {}).setdefault(b, {})[a] = v

    def deliver(self, dst: int, msg: tuple) -> None:
        if dst in self.crashed:
            return
        p, kind = self.procs[dst], msg[0]
        if kind == "PREPARE":
            p.on_prepare(msg[1], msg[2])
        elif kind == "ACCEPT":
            p.on_accept(msg[1], msg[2], msg[3])
        elif kind == "DECIDE":
            p.on_decide(msg[1], msg[2])
        elif kind == "FORGET":
            p.on_forget(msg[1])
        elif kind == "PROMISE":
            p.on_promise(*msg[1:])
        elif kind == "ACCEPTED":
            p.on_accepted(*msg[1:])
        else:
            p.on_nack(msg[1])

    def leaders(self) -> list[Process]:
        return [p for p in self.procs if p.leading and p.pid not in self.crashed]

    def done(self) -> bool:
        chosen = self.chosen_log()
        return set(self.commands) <= set(chosen)

    def run(self) -> "CheapPaxos":
        self.procs[0].start()
        for _ in range(self.max_steps):
            if self.crashes_left and self.rng.random() < self.crash_prob:
                live = [p for p in range(len(self.procs)) if p not in self.crashed]
                self.crashed.add(self.rng.choice(live))
                self.crashes_left -= 1
            if self.duel_prob and self.rng.random() < self.duel_prob:
                cand = [p for p in self.c0.mains if p not in self.crashed]
                if cand:
                    self.procs[self.rng.choice(cand)].start()
            if self.queue:
                dst, msg = self.queue.pop(self.rng.randrange(len(self.queue)))
                self.deliver(dst, msg)
                continue
            # Nothing in flight.
            for s, aux, src in self.forget_after_decides:
                for q in aux:
                    self.send(src, q, ("FORGET", s))
            self.forget_after_decides = []
            for p in self.procs:  # a client retries a command held by a crashed leader
                if p.pid in self.crashed and p.mine is not None:
                    self.pool.append(p.mine)
                    p.mine = None
            if self.queue:
                continue
            leads = self.leaders()
            if leads:
                ld = max(leads, key=lambda p: p.ballot)
                ld.try_propose()
                if self.queue:
                    continue
                if self.done() and not ld.pending_remove:
                    break
                ld.timeout()
            else:
                live = self.live_mains()
                if not live:
                    break
                self.procs[min(live)].start()
        return self

    def live_mains(self) -> list[int]:
        out = []
        for p in self.procs:
            if p.pid in self.crashed:
                continue
            c = p.config(p.first_open())
            if c is not None and p.pid in c.mains:
                out.append(p.pid)
        return out

    def chosen_log(self) -> list[object]:
        """The chosen value of each slot, in order; raises if a slot has two."""
        log: list[object] = []
        c = self.c0
        s = 0
        while s in self.votes:
            vals = set()
            for b, by in self.votes[s].items():
                for v in set(by.values()):
                    if c.is_quorum(frozenset(a for a, w in by.items() if w == v)):
                        vals.add(v)
            if len(vals) > 1:
                raise AssertionError(f"slot {s} has two chosen values {vals}")
            if not vals:
                break
            v = vals.pop()
            log.append(v)
            c = c.apply(v)
            s += 1
        return log

    def consistent(self) -> bool:
        log = self.chosen_log()
        for p in self.procs:
            for s, v in p.decided.items():
                if s >= len(log) or log[s] != v:
                    return False
        return True
