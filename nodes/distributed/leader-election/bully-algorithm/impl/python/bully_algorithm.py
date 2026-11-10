# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bully-algorithm/. The authors are listed in prov/HSXH10.jsonl.

"""The bully algorithm (Garcia-Molina 1982) in a synchronous system with crashes.

Processes have identifiers 1..N. Time goes in integer steps. A message sent at
step t is delivered at step t + 1, unless the receiver is down at that step.
The failure detector is perfect: when a process polls, it learns whether its
coordinator is up. This is the synchrony that the algorithm needs.

Timeouts: T_OK = 2 steps (a round trip), T_COORD = 3 steps after an OK.
Only ELECTION, OK and COORDINATOR messages are counted.
"""

import random

T_OK = 2
T_COORD = 3


class Proc:
    def __init__(self, uid: int) -> None:
        self.uid = uid
        self.coord: int | None = None
        self.electing = False
        self.ok_deadline: int | None = None
        self.coord_deadline: int | None = None


class Bully:
    def __init__(self, n: int) -> None:
        self.n = n
        self.procs = {i: Proc(i) for i in range(1, n + 1)}
        self.up = set(range(1, n + 1))
        self.outbox: list[tuple[int, int, str, int]] = []  # (dst, src, kind, value)
        self.counts = {"ELECTION": 0, "OK": 0, "COORDINATOR": 0}
        self.starts = 0

    def send(self, dst: int, src: int, kind: str, value: int = 0) -> None:
        self.counts[kind] += 1
        self.outbox.append((dst, src, kind, value))

    def start_election(self, p: Proc, t: int) -> None:  # @line L2
        self.starts += 1
        p.electing = True
        p.coord_deadline = None
        for j in range(p.uid + 1, self.n + 1):
            self.send(j, p.uid, "ELECTION")
        p.ok_deadline = t + T_OK  # @line L3

    def become_coordinator(self, p: Proc) -> None:  # @line L7
        p.coord = p.uid
        p.electing = False
        p.ok_deadline = None
        p.coord_deadline = None
        for j in range(1, p.uid):
            self.send(j, p.uid, "COORDINATOR", p.uid)

    def step(self, t: int, inbox: list[tuple[int, int, str, int]]) -> None:
        for dst, src, kind, value in inbox:
            if dst not in self.up:
                continue
            p = self.procs[dst]
            if kind == "ELECTION":  # @line L4
                self.send(src, dst, "OK")
                if not p.electing:
                    self.start_election(p, t)
            elif kind == "OK":  # @line L5
                if p.electing and p.ok_deadline is not None:
                    p.ok_deadline = None
                    p.coord_deadline = t + T_COORD
            elif kind == "COORDINATOR":  # @line L8
                if value < p.uid:
                    if not p.electing:
                        self.start_election(p, t)
                else:
                    p.coord = value
                    p.electing = False
                    p.ok_deadline = None
                    p.coord_deadline = None
        for i in sorted(self.up):
            p = self.procs[i]
            if p.ok_deadline == t:  # @line L6
                self.become_coordinator(p)
            elif p.coord_deadline == t:  # @line L9
                p.coord_deadline = None
                self.start_election(p, t)

    def run(self, events: list[tuple[int, str, int]], horizon: int, poll: int = 0, seed: int = 0) -> None:
        """events: (time, "crash" | "recover" | "detect", process).

        "detect" makes the process start an election at that time. With poll > 0,
        each process also checks its coordinator every poll steps, at a seeded
        offset, and starts an election when the coordinator is down or unknown.
        """
        rng = random.Random(seed)
        offset = {i: rng.randrange(poll) if poll else 0 for i in self.procs}
        by_time: dict[int, list[tuple[str, int]]] = {}
        for t, kind, i in events:
            by_time.setdefault(t, []).append((kind, i))
        for t in range(horizon):
            inbox, self.outbox = self.outbox, []
            for kind, i in by_time.get(t, []):
                p = self.procs[i]
                if kind == "crash":
                    self.up.discard(i)
                elif kind == "recover" and i not in self.up:
                    self.up.add(i)
                    self.procs[i] = Proc(i)
                    self.start_election(self.procs[i], t)  # @line L1
                elif kind == "detect" and i in self.up and not p.electing:
                    self.start_election(p, t)  # @line L1
            self.step(t, inbox)
            if poll:
                for i in sorted(self.up):
                    p = self.procs[i]
                    if (t - offset[i]) % poll == 0 and not p.electing:
                        if p.coord is None or p.coord not in self.up:
                            self.start_election(p, t)  # @line L1

    def total(self) -> int:
        return sum(self.counts.values())

    def coordinators(self) -> dict[int, int | None]:
        return {i: self.procs[i].coord for i in sorted(self.up)}


def bully(n: int, events: list[tuple[int, str, int]], horizon: int = 0, poll: int = 0, seed: int = 0) -> Bully:
    """Run the bully algorithm on processes 1..n and return the finished system."""
    last = max((t for t, _, _ in events), default=0)
    sim = Bully(n)
    sim.run(events, horizon or last + 8 * n + 20, poll, seed)
    return sim


def worst_case_messages(n: int, old_coordinator_crashed: bool) -> int:
    """The derived count when the lowest process starts and nothing fails during the election."""
    if old_coordinator_crashed:
        return n * n - n - 1
    return n * n - 1
