# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-phase-commit/. The authors are listed in prov/DSVH0K.jsonl.

"""Three-phase commit (Skeen 1981) with the termination protocol, in lock-step synchronous rounds.

Process 0 is the coordinator and processes 1..n are the participants. The
states are q (initial), w (wait: voted yes), p (pre-commit), c (commit) and
a (abort). A message sent in round r arrives in round r + 1. A process that
crashes in round r sends only the first k of its messages of that round, and
then stops for good. The failure detector is perfect: in round r + 1 every
live process knows that it crashed.

A partition can be switched on from some round. Then each side sees the other
side as crashed, which is what a timeout-based failure detector reports. The
protocol is not safe in that case, and the tests show a run.
"""

from __future__ import annotations

from typing import Optional

Q, W, P, C, A = "q", "w", "p", "c", "a"


class ThreePC:
    def __init__(self, votes: dict[int, bool], crashes: Optional[dict[int, tuple[int, int]]] = None,
                 partition: Optional[tuple[int, list[set[int]]]] = None) -> None:
        self.n = len(votes)
        self.N = self.n + 1
        self.votes = votes
        self.crash_plan = crashes or {}  # process -> (round, number of messages it sends in that round)
        self.partition = partition  # (first round, groups)
        self.state = {i: Q for i in range(self.N)}
        self.crashed: set[int] = set()
        self.inbox: dict[int, list[tuple[int, str, object]]] = {i: [] for i in range(self.N)}
        self.leader = {i: 0 for i in range(self.N)}
        self.timer: dict[int, Optional[tuple[str, int]]] = {i: None for i in range(self.N)}
        self.timer[0] = ("start", 0)
        self.yes: dict[int, set[int]] = {i: set() for i in range(self.N)}
        self.states: dict[int, dict[int, str]] = {i: {} for i in range(self.N)}
        self.round = 0
        self.trace: list[dict[int, str]] = []

    def group(self, i: int, r: int) -> set[int]:
        if self.partition and r >= self.partition[0]:
            return next(g for g in self.partition[1] if i in g)
        return set(range(self.N))

    def view(self, i: int, r: int) -> set[int]:
        """The processes that i believes to be up in round r."""
        return {j for j in self.group(i, r) if j not in self.crashed}

    def to_all(self, i: int, kind: str, val: object = None) -> list[tuple[int, str, object]]:
        return [(j, kind, val) for j in range(self.N) if j != i]

    def act(self, i: int, r: int) -> list[tuple[int, str, object]]:
        out: list[tuple[int, str, object]] = []
        for src, kind, val in self.inbox[i]:
            if kind == "VOTE-REQ":
                if self.votes[i]:
                    self.state[i] = W  # @line L2
                    out.append((src, "YES", None))
                else:
                    self.state[i] = A
                    out.append((src, "NO", None))
            elif kind == "YES":
                self.yes[i].add(src)
            elif kind == "PRE-COMMIT":
                self.state[i] = P  # @line L4
                out.append((src, "ACK", None))
            elif kind == "COMMIT":
                self.state[i] = C  # @line L6
            elif kind == "ABORT":
                self.state[i] = A
            elif kind == "STATE-REQ":
                out.append((src, "STATE", self.state[i]))
            elif kind == "STATE":
                self.states[i][src] = str(val)
        v = self.view(i, r)
        if self.leader[i] not in v:
            self.leader[i] = min(v)  # @line L7
            if self.leader[i] == i:
                self.timer[i] = ("terminate", r)
        t = self.timer[i]
        if t is None or t[1] != r:
            return out
        self.timer[i] = None
        action = t[0]
        if action == "start":
            self.state[i] = W
            out += self.to_all(i, "VOTE-REQ")  # @line L1
            self.timer[i] = ("votes", r + 2)
        elif action == "votes":
            if len(self.yes[i]) == self.n:
                self.state[i] = P  # @line L3
                out += self.to_all(i, "PRE-COMMIT")
                self.timer[i] = ("commit", r + 2)
            else:
                self.state[i] = A
                out += self.to_all(i, "ABORT")
        elif action == "commit":
            self.state[i] = C  # @line L5
            out += self.to_all(i, "COMMIT")
        elif action == "terminate":
            if self.state[i] in (C, A):
                out += self.to_all(i, "COMMIT" if self.state[i] == C else "ABORT")
            else:
                self.states[i] = {}
                out += self.to_all(i, "STATE-REQ")  # @line L8
                self.timer[i] = ("decide", r + 2)
        elif action == "decide":
            seen = set(self.states[i].values()) | {self.state[i]}
            if A in seen:
                self.state[i] = A  # @line L9
                out += self.to_all(i, "ABORT")
            elif C in seen:
                self.state[i] = C  # @line L10
                out += self.to_all(i, "COMMIT")
            elif P not in seen:
                self.state[i] = A  # @line L11
                out += self.to_all(i, "ABORT")
            else:
                self.state[i] = P  # @line L12
                out += self.to_all(i, "PRE-COMMIT")
                self.timer[i] = ("commit", r + 2)
        return out

    def step(self) -> None:
        r = self.round
        alive = [i for i in range(self.N) if i not in self.crashed]
        outs = {i: self.act(i, r) for i in alive}
        new_inbox: dict[int, list[tuple[int, str, object]]] = {i: [] for i in range(self.N)}
        for i, msgs in outs.items():
            if i in self.crash_plan and self.crash_plan[i][0] == r:
                msgs = msgs[: self.crash_plan[i][1]]
                self.crashed.add(i)
            for dst, kind, val in msgs:
                if dst in self.group(i, r):
                    new_inbox[dst].append((i, kind, val))
        self.inbox = new_inbox
        self.trace.append(dict(self.state))
        self.round += 1

    def run(self, rounds: int = 40) -> None:
        for _ in range(rounds):
            self.step()

    def decisions(self) -> set[str]:
        return {s for s in self.state.values() if s in (C, A)}

    def safe(self) -> bool:
        return len(self.decisions()) <= 1 and (C not in self.decisions() or all(self.votes.values()))

    def live_undecided(self) -> list[int]:
        return [i for i in range(self.N) if i not in self.crashed and self.state[i] not in (C, A)]
