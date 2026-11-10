# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/invitation-algorithm/. The authors are listed in prov/2ZVXPK.jsonl.

"""The invitation algorithm (Garcia-Molina 1982), simplified, in a simulator.

Processes 0..n-1 have priority equal to their index. Each process is in a group
with a unique group number gid = (counter, coordinator). Time goes in integer
ticks. Each message takes a seeded random delay. A partition is a map from
process to component; a message between different components is lost, and so
is a message to or from a crashed process.

The timeouts assume a delay of at most D, but the simulator can also make some
messages much slower, so that timeouts fire wrongly. The safety property must
hold anyway; the merge into one group is promised only when delays are at most
D and the network is stable.
"""

import random

D = 3            # the delay that the timeouts assume
PERIOD = 10      # how often a process checks
WAIT = PERIOD + D  # the merge wait per step of priority


class Proc:
    def __init__(self, i: int, n: int) -> None:
        self.i = i
        self.counter = 0
        self.up = True
        self.recover()
        self.check_at = 0

    def recover(self) -> None:  # @line L1
        self.counter += 1
        self.gid = (self.counter, self.i)
        self.coord = self.i
        self.members = {self.i}
        self.state = "normal"
        self.accepted: set[int] = set()
        self.found: set[int] = set()
        self.merge_at: int | None = None
        self.deadline: int | None = None
        self.ayt_deadline: int | None = None


class Invitation:
    def __init__(self, n: int, seed: int, slow: float = 0.0) -> None:
        self.n = n
        self.rng = random.Random(seed)
        self.slow = slow
        self.p = [Proc(i, n) for i in range(n)]
        for q in self.p:
            q.check_at = self.rng.randrange(PERIOD)
        self.comp = [0] * n
        self.queue: dict[int, list[tuple[int, int, str, tuple]]] = {}
        self.counts: dict[str, int] = {}
        self.merges = 0

    # the network
    def send(self, t: int, src: int, dst: int, kind: str, data: tuple = ()) -> None:
        self.counts[kind] = self.counts.get(kind, 0) + 1
        if self.comp[src] != self.comp[dst]:
            return
        delay = self.rng.randint(1, D)
        if self.slow and self.rng.random() < self.slow:
            delay = self.rng.randint(D + 1, 6 * D)
        self.queue.setdefault(t + delay, []).append((src, dst, kind, data))

    # the algorithm
    def merge(self, t: int, c: Proc) -> None:  # @line L4
        self.merges += 1
        others = (c.found | c.members) - {c.i}
        c.counter += 1
        c.gid = (c.counter, c.i)
        c.state = "election"
        c.accepted = {c.i}
        c.found = set()
        c.merge_at = None
        for j in sorted(others):
            self.send(t, c.i, j, "INVITE", (c.gid,))
        c.deadline = t + 3 * D + 1

    def handle(self, t: int, src: int, q: Proc, kind: str, data: tuple) -> None:
        if kind == "AYC":  # @line L2
            if q.state == "normal" and q.coord == q.i:
                self.send(t, q.i, src, "AYC_YES")
        elif kind == "AYC_YES":  # @line L3
            if q.state == "normal" and q.coord == q.i:
                q.found.add(src)
                if q.merge_at is None:
                    # wait for the other answers, then longer for a lower priority
                    q.merge_at = t + 2 * D + WAIT * (self.n - 1 - q.i)
        elif kind == "INVITE":  # @line L5
            (gid,) = data
            if q.state != "normal":
                return
            if q.coord == q.i:
                for j in sorted(q.members - {q.i}):  # @line L6
                    self.send(t, q.i, j, "INVITE", (gid,))
            q.state = "reorganizing"  # @line L7
            q.gid = gid
            q.coord = gid[1]
            q.members = {q.i}
            q.merge_at = None
            q.ayt_deadline = None
            self.send(t, q.i, gid[1], "ACCEPT", (gid,))
            q.deadline = t + 5 * D + 2
        elif kind == "ACCEPT":  # @line L8
            (gid,) = data
            if q.state == "election" and q.gid == gid:
                q.accepted.add(src)
        elif kind == "READY":  # @line L10
            gid, members = data
            if q.state == "reorganizing" and q.gid == gid:
                q.state = "normal"
                q.deadline = None
        elif kind == "AYT":  # @line L11
            (gid,) = data
            ok = q.state == "normal" and q.coord == q.i and q.gid == gid and src in q.members
            self.send(t, q.i, src, "AYT_ANSWER", (gid, ok))
        elif kind == "AYT_ANSWER":
            gid, ok = data
            if q.state == "normal" and q.gid == gid and q.coord != q.i:
                q.ayt_deadline = None
                if not ok:
                    q.recover()  # @line L12

    def timers(self, t: int, q: Proc) -> None:
        if q.state == "election" and q.deadline == t:  # @line L9
            q.members = set(q.accepted)
            q.state = "normal"
            q.coord = q.i
            q.deadline = None
            for j in sorted(q.members - {q.i}):
                self.send(t, q.i, j, "READY", (q.gid, tuple(sorted(q.members))))
        elif q.state == "reorganizing" and q.deadline == t:
            q.recover()  # @line L12
        elif q.state == "normal" and q.ayt_deadline == t:
            q.recover()  # @line L12
        if q.state == "normal" and q.coord == q.i and q.merge_at == t:
            self.merge(t, q)
        if q.state == "normal" and t >= q.check_at:
            q.check_at = t + PERIOD
            if q.coord == q.i:
                for j in range(self.n):  # @line L2
                    if j != q.i:
                        self.send(t, q.i, j, "AYC")
            elif q.ayt_deadline is None:
                self.send(t, q.i, q.coord, "AYT", (q.gid,))  # @line L11
                q.ayt_deadline = t + 2 * D + 1

    def run(self, events: list[tuple[int, str, object]], horizon: int, check=None) -> None:
        """events: (t, "crash" | "recover", i) or (t, "partition", list of components)."""
        by_time: dict[int, list[tuple[str, object]]] = {}
        for t, kind, x in events:
            by_time.setdefault(t, []).append((kind, x))
        for t in range(horizon):
            for kind, x in by_time.get(t, []):
                if kind == "crash":
                    self.p[x].up = False
                elif kind == "recover" and not self.p[x].up:
                    self.p[x].up = True
                    self.p[x].recover()
                    self.p[x].check_at = t
                elif kind == "partition":
                    self.comp = list(x)
            for src, dst, kind, data in self.queue.pop(t, []):
                if self.p[dst].up and self.p[src].up and self.comp[src] == self.comp[dst]:
                    self.handle(t, src, self.p[dst], kind, data)
            for q in self.p:
                if q.up:
                    self.timers(t, q)
            if check:
                check(self)


def safety_violations(sim: Invitation) -> list[str]:
    """Garcia-Molina's assertion, in the form tested here.

    Two normal processes in the same group have the same coordinator, and a
    normal member is in the member list of its coordinator if the coordinator
    is still normal in that group.
    """
    bad = []
    seen: dict[tuple, int] = {}
    for q in sim.p:
        if not q.up or q.state != "normal":
            continue
        if seen.setdefault(q.gid, q.coord) != q.coord:
            bad.append(f"group {q.gid} has two coordinators")
        c = sim.p[q.coord]
        if c.up and c.state == "normal" and c.gid == q.gid and q.i not in c.members:
            bad.append(f"{q.i} is not in the list of {c.i}")
    return bad


def groups(sim: Invitation) -> dict[tuple, list[int]]:
    out: dict[tuple, list[int]] = {}
    for q in sim.p:
        if q.up:
            out.setdefault(q.gid if q.state == "normal" else ("busy", q.i), []).append(q.i)
    return out
