# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/total-order-broadcast/. The authors are listed in prov/1XEK7N.jsonl.

"""Total-order broadcast from consensus, and consensus from total-order broadcast.

The two reductions of Chandra and Toueg (1996), run in a seeded asynchronous
simulator with crash failures. Messages are delivered in a random order, with
any delay. A faulty process crashes after a random number of sends, so it can
crash in the middle of a broadcast and reach only some processes.

Consensus is an oracle: instance k decides the first proposal it gets, and it
sends the decision to each process that proposes in instance k. This gives
agreement, validity and termination for the processes that propose.
"""

from __future__ import annotations

import random
from typing import Callable, Hashable, Optional

Msg = Hashable


class Sim:
    """A seeded asynchronous network with reliable channels and crash failures."""

    def __init__(self, n: int, seed: int, faulty: dict[int, int] | None = None) -> None:
        self.n, self.rng = n, random.Random(seed)
        self.sends_left = dict(faulty or {})  # faulty process -> sends before it crashes
        self.crashed: set[int] = set()
        self.inflight: list[tuple[int, int, tuple]] = []  # (src, dst, payload)
        self.handlers: dict[int, Callable[[int, tuple], None]] = {}
        self.decisions: dict[int, frozenset] = {}  # the consensus oracle: instance -> decision

    def send(self, src: int, dst: int, payload: tuple) -> None:
        if src in self.crashed:
            return
        if src in self.sends_left:
            if self.sends_left[src] == 0:
                self.crashed.add(src)  # crash before this send
                return
            self.sends_left[src] -= 1
        self.inflight.append((src, dst, payload))

    def propose(self, p: int, k: int, value: frozenset) -> None:
        """Consensus instance k. The first proposal is decided; the proposer learns it later."""
        if p in self.crashed:
            return
        self.decisions.setdefault(k, value)
        self.inflight.append((-1, p, ("DECIDE", k, self.decisions[k])))

    def step(self) -> bool:
        if not self.inflight:
            return False
        src, dst, payload = self.inflight.pop(self.rng.randrange(len(self.inflight)))
        if dst not in self.crashed:
            self.handlers[dst](src, payload)
        return True


class TOBProcess:
    """Total-order broadcast from reliable broadcast and a sequence of consensus instances."""

    def __init__(self, pid: int, sim: Sim, use_consensus: bool = True) -> None:
        self.pid, self.sim, self.use_consensus = pid, sim, use_consensus
        self.seen: set[Msg] = set()  # messages received by reliable broadcast
        self.pending: set[Msg] = set()
        self.delivered: set[Msg] = set()
        self.sequence: list[Msg] = []
        self.k = 0
        self.waiting = False
        self.on_deliver: Callable[[Msg], None] = lambda m: None
        sim.handlers[pid] = self.receive

    def to_broadcast(self, m: Msg) -> None:
        self.rb_broadcast(m)  # @line L1

    def rb_broadcast(self, m: Msg) -> None:
        """Eager reliable broadcast: send to all, and each process relays on first receipt."""
        for q in range(self.sim.n):
            self.sim.send(self.pid, q, ("RB", m))

    def receive(self, src: int, payload: tuple) -> None:
        if payload[0] == "RB":
            m = payload[1]
            if m in self.seen:
                return
            self.seen.add(m)
            if src != self.pid:
                self.rb_broadcast(m)  # relay before delivery
            if self.pid in self.sim.crashed:
                return
            self.r_deliver(m)
        else:
            _, k, value = payload
            self.on_decide(k, value)

    def r_deliver(self, m: Msg) -> None:
        if not self.use_consensus:  # the broken variant: deliver at once, in arrival order
            self.deliver(m)
            return
        if m not in self.delivered:
            self.pending.add(m)  # @line L2
        self.try_propose()

    def try_propose(self) -> None:
        if self.pending and not self.waiting:  # @line L3
            self.k += 1
            self.waiting = True  # @line L4
            self.sim.propose(self.pid, self.k, frozenset(self.pending))  # @line L5

    def on_decide(self, k: int, value: frozenset) -> None:
        assert k == self.k  # @line L6
        for m in sorted(value - self.delivered, key=repr):  # @line L7
            self.deliver(m)
        self.pending -= value  # @line L8
        self.waiting = False
        self.try_propose()

    def deliver(self, m: Msg) -> None:
        self.delivered.add(m)
        self.sequence.append(m)
        self.on_deliver(m)


class SequencerTOB:
    """A total-order broadcast service used as a black box: one global sequence, sent to each process in order."""

    def __init__(self, sim: Sim) -> None:
        self.sim, self.log = sim, []
        self.next: dict[int, int] = {}
        self.buffer: dict[int, dict[int, Msg]] = {}
        self.sequence: dict[int, list[Msg]] = {}
        self.on_deliver: dict[int, Callable[[Msg], None]] = {}
        for p in range(sim.n):
            self.next[p], self.buffer[p], self.sequence[p] = 0, {}, []
            sim.handlers[p] = self._make_handler(p)

    def to_broadcast(self, p: int, m: Msg) -> None:
        if p in self.sim.crashed:
            return
        self.log.append(m)
        for q in range(self.sim.n):
            self.sim.inflight.append((-1, q, ("SEQ", len(self.log) - 1, m)))

    def _make_handler(self, p: int) -> Callable[[int, tuple], None]:
        def handle(src: int, payload: tuple) -> None:
            _, i, m = payload
            self.buffer[p][i] = m
            while self.next[p] in self.buffer[p]:
                m = self.buffer[p].pop(self.next[p])
                self.next[p] += 1
                self.sequence[p].append(m)
                self.on_deliver.get(p, lambda m: None)(m)
        return handle


class ConsensusFromTOB:
    """Consensus from total-order broadcast: decide the value of the first message delivered."""

    def __init__(self, pid: int, broadcast: Callable[[Msg], None]) -> None:
        self.pid, self.broadcast = pid, broadcast
        self.decision: Optional[object] = None

    def propose(self, v: object) -> None:
        self.broadcast((self.pid, v))  # @line L9

    def on_deliver(self, m: Msg) -> None:
        if self.decision is None:  # @line L10
            self.decision = m[1]


def run_tob(n: int, seed: int, faulty: dict[int, int], per_process: int = 3,
            use_consensus: bool = True) -> tuple[Sim, list[TOBProcess], dict[int, list[Msg]]]:
    """Each process to-broadcasts per_process messages at random times. Run until no message is in flight."""
    sim = Sim(n, seed, faulty)
    procs = [TOBProcess(p, sim, use_consensus) for p in range(n)]
    todo = [(p, f"m{p}.{i}") for p in range(n) for i in range(per_process)]
    sim.rng.shuffle(todo)
    broadcast: dict[int, list[Msg]] = {p: [] for p in range(n)}
    while todo or sim.inflight:
        if todo and (not sim.inflight or sim.rng.random() < 0.15):
            p, m = todo.pop()
            if p not in sim.crashed:
                broadcast[p].append(m)
                procs[p].to_broadcast(m)
        else:
            sim.step()
    return sim, procs, broadcast


def check_tob(n: int, sim: Sim, sequences: dict[int, list[Msg]], broadcast: dict[int, list[Msg]]) -> list[str]:
    """Return the violated properties: validity, agreement, integrity and total order (uniform form)."""
    bad = []
    correct = [p for p in range(n) if p not in sim.crashed]
    every = {m for ms in broadcast.values() for m in ms}
    for p in range(n):
        s = sequences[p]
        if len(set(s)) != len(s) or not set(s) <= every:
            bad.append(f"integrity at {p}")
    for p in correct:
        for m in broadcast[p]:
            if m not in sequences[p]:
                bad.append(f"validity: {p} never delivers its {m}")
    for p in range(n):
        for q in correct:
            if not set(sequences[p]) <= set(sequences[q]):
                bad.append(f"agreement: {q} misses a message that {p} delivered")
    for p in range(n):
        for q in range(p + 1, n):
            a, b = sequences[p], sequences[q]
            common = set(a) & set(b)
            if [m for m in a if m in common] != [m for m in b if m in common]:
                bad.append(f"total order: {p} and {q}")
    return bad
