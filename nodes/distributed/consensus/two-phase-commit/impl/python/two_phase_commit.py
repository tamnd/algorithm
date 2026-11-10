# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-phase-commit/. The authors are listed in prov/S2MVM5.jsonl.

"""Two-phase commit (Gray 1978; Lampson and Sturgis 1976) with logging, recovery and cooperative termination.

Process 0 is the coordinator and processes 1..n are the participants. Each
process has a log on stable storage that survives a crash; all other state is
lost. The network is asynchronous: the tests pick which message to deliver,
and when a process crashes, recovers or times out. A seeded random scheduler
drives the random runs.

The log records are "prepared", "commit", "abort" and "end". A participant
forces "prepared" before it votes yes, and the coordinator forces its decision
before it sends it. These two rules make recovery safe.
"""

from __future__ import annotations

import random
from typing import Optional

COMMIT, ABORT = "commit", "abort"
INIT, UNCERTAIN = "init", "uncertain"


class TwoPC:
    def __init__(self, votes: dict[int, bool], seed: int = 0, naive_termination: bool = False) -> None:
        self.n = len(votes)
        self.votes = votes  # participant -> its vote (True means yes)
        self.rng = random.Random(seed)
        self.naive = naive_termination  # the unsafe rule: give up and abort when all others are uncertain
        self.log: dict[int, list[str]] = {i: [] for i in range(self.n + 1)}
        self.alive = {i: True for i in range(self.n + 1)}
        self.inflight: list[tuple[int, int, str]] = []  # (src, dst, kind)
        self.decision: dict[int, str] = {}  # process -> the decision it applied
        self.reset(0)
        for p in range(1, self.n + 1):
            self.reset(p)

    # ---- volatile state
    def reset(self, i: int) -> None:
        if i == 0:
            self.yes: set[int] = set()
            self.acks: set[int] = set()
            self.waiting = False
        else:
            setattr(self, f"_state{i}", INIT)
            setattr(self, f"_unc{i}", set())

    def state(self, p: int) -> str:
        if p in self.decision:
            return self.decision[p]
        return getattr(self, f"_state{p}")

    def send(self, src: int, dst: int, kind: str) -> None:
        if self.alive[src]:
            self.inflight.append((src, dst, kind))

    def broadcast(self, src: int, kind: str) -> None:
        for p in range(1, self.n + 1):
            self.send(src, p, kind)

    # ---- the coordinator
    def start(self) -> None:
        self.waiting = True
        self.broadcast(0, "PREPARE")  # @line L1

    def decide(self, i: int, d: str) -> None:
        """Force the decision to the log, then apply it. The coordinator then sends it to all."""
        if i in self.decision:
            return
        self.log[i].append(d)  # forced write
        self.decision[i] = d
        if i == 0:
            self.waiting = False
            self.broadcast(0, d.upper())  # @line L4

    def coordinator_vote(self, src: int, kind: str) -> None:
        if 0 in self.decision:
            self.send(0, src, self.decision[0].upper())  # a late vote gets the decision
            return
        if kind == "NO":
            self.decide(0, ABORT)  # @line L3
            return
        self.yes.add(src)
        if len(self.yes) == self.n:
            self.decide(0, COMMIT)  # @line L2

    # ---- the participants
    def on_prepare(self, p: int) -> None:
        if p in self.decision:  # it aborted on its own before PREPARE came
            self.send(p, 0, "NO")
            return
        if self.votes[p]:
            self.log[p].append("prepared")  # @line L5
            setattr(self, f"_state{p}", UNCERTAIN)
            self.send(p, 0, "YES")
        else:
            self.decide(p, ABORT)  # @line L6
            self.send(p, 0, "NO")

    def on_decision(self, p: int, d: str) -> None:
        self.decide(p, d)  # @line L7
        self.send(p, 0, "ACK")

    def on_request(self, q: int, src: int) -> None:
        """A process asks q for the decision (the cooperative termination protocol)."""
        if q in self.decision:
            self.send(q, src, self.decision[q].upper())  # @line L10
        elif q == 0 or self.state(q) == INIT:
            self.decide(q, ABORT)  # @line L11
            if q != 0:
                self.send(q, src, "ABORT")
        elif self.state(q) == UNCERTAIN:
            self.send(q, src, "UNCERTAIN")  # @line L12

    def timeout(self, i: int) -> None:
        if not self.alive[i] or i in self.decision:
            return
        if i == 0:
            if self.waiting:
                self.decide(0, ABORT)  # @line L3
            return
        if self.state(i) == INIT:
            self.decide(i, ABORT)  # @line L8
        else:
            for q in range(self.n + 1):  # @line L9
                if q != i:
                    self.send(i, q, "DREQ")
            others = {q for q in range(1, self.n + 1) if q != i and self.alive[q]}
            if self.naive and getattr(self, f"_unc{i}") >= others:
                # unsafe: every live participant is uncertain, but a dead process may have committed
                self.decide(i, ABORT)

    # ---- crashes and recovery
    def crash(self, i: int) -> None:
        self.alive[i] = False
        self.inflight = [m for m in self.inflight if m[0] != i]  # unsent output is lost
        self.reset(i)

    def recover(self, i: int) -> None:
        if self.alive[i]:
            return
        self.alive[i] = True
        log = self.log[i]
        if COMMIT in log or ABORT in log:  # @line L13
            d = COMMIT if COMMIT in log else ABORT
            if i == 0:
                self.broadcast(0, d.upper())
        elif i == 0:
            self.decide(0, ABORT)  # no decision was logged, so no one can have committed
        elif "prepared" in log:
            setattr(self, f"_state{i}", UNCERTAIN)  # @line L14
            self.timeout(i)
        else:
            self.decide(i, ABORT)  # it never voted yes

    # ---- the network
    def deliver(self, k: int) -> None:
        src, dst, kind = self.inflight.pop(k)
        if not self.alive[dst]:
            return
        if dst == 0:
            if kind in ("YES", "NO"):
                self.coordinator_vote(src, kind)
            elif kind == "ACK":
                self.acks.add(src)
                if len(self.acks) == self.n and "end" not in self.log[0]:
                    self.log[0].append("end")
            elif kind == "DREQ":
                self.on_request(0, src)
        elif kind == "PREPARE":
            self.on_prepare(dst)
        elif kind in ("COMMIT", "ABORT"):
            self.on_decision(dst, kind.lower())
        elif kind == "DREQ":
            self.on_request(dst, src)
        elif kind == "UNCERTAIN":
            getattr(self, f"_unc{dst}").add(src)

    def deliver_all(self, limit: int = 100000) -> None:
        for _ in range(limit):
            if not self.inflight:
                return
            self.deliver(0)

    def random_run(self, steps: int, crash_p: float = 0.05) -> None:
        """Random delivery, crashes, recoveries and timeouts; then all recover and the network drains."""
        self.start()
        rng = self.rng
        for _ in range(steps):
            r = rng.random()
            i = rng.randrange(self.n + 1)
            if r < 0.7 and self.inflight:
                self.deliver(rng.randrange(len(self.inflight)))
            elif r < 0.7 + crash_p:
                self.crash(i)
            elif r < 0.85:
                self.recover(i)
            else:
                self.timeout(i)
        for i in range(self.n + 1):
            self.recover(i)
        for _ in range(4):
            for i in range(self.n + 1):
                self.timeout(i)
            self.deliver_all()

    def check(self) -> Optional[str]:
        """Return a violated property, or None."""
        ds = set(self.decision.values())
        if len(ds) > 1:
            return "agreement"
        if COMMIT in ds and not all(self.votes.values()):
            return "validity"
        return None
