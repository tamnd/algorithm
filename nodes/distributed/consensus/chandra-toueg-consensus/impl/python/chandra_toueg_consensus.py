# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandra-toueg-consensus/. The authors are listed in prov/AKDA5X.jsonl.

"""The Chandra-Toueg rotating coordinator consensus algorithm with a
simulated eventually strong failure detector (diamond-S), n > 2f.

The run is a deterministic discrete event simulation. Time is the step
count. In each step a seeded scheduler delivers one message in transit, then
every live process runs its guards again, because a guard can also become true
when the failure detector changes its output.

The failure detector makes random mistakes until a seeded time GST. After
GST it suspects every crashed process (strong completeness) and never
suspects one chosen correct process (eventual weak accuracy). It may still
suspect other correct processes after GST, which diamond-S allows.

A process crashes when it tries its (k + 1)-th send, where k = crash_after[p],
so a crash can fall in the middle of a broadcast, also of a relay in the
reliable broadcast of the decision.
"""

import random
from typing import Optional


class Network:
    def __init__(self, n: int, rng: random.Random, crash_after: dict[int, int], mode: str) -> None:
        self.n, self.rng, self.mode = n, rng, mode
        self.crash_after = dict(crash_after)
        self.crashed: set[int] = set()
        self.sent = [0] * n
        self.pending: list[tuple[int, int, tuple]] = []
        self.picks = 0

    def send(self, src: int, dest: int, msg: tuple) -> bool:
        if src in self.crashed:
            return False
        if src in self.crash_after and self.sent[src] >= self.crash_after[src]:
            self.crashed.add(src)
            return False
        self.sent[src] += 1
        self.pending.append((dest, src, msg))
        return True

    def broadcast(self, src: int, msg: tuple, skip_self: bool = False) -> None:
        for dest in range(self.n):
            if skip_self and dest == src:
                continue
            if not self.send(src, dest, msg):
                return

    def pop(self) -> Optional[tuple[int, int, tuple]]:
        if not self.pending:
            return None
        self.picks += 1
        if self.mode == "lifo" and self.picks % 8:
            i = len(self.pending) - 1  # newest first, but fair: every 8th pick is the oldest
        elif self.mode == "lifo":
            i = 0
        else:
            i = self.rng.randrange(len(self.pending))
        return self.pending.pop(i)


class DiamondS:
    """A simulated diamond-S failure detector."""

    def __init__(self, seed: int, gst: int, trusted: int, net: Network, rate: float = 0.3) -> None:
        self.seed, self.gst, self.trusted, self.net, self.rate = seed, gst, trusted, net, rate
        self.mistakes = 0

    def suspects(self, t: int, p: int, q: int) -> bool:
        if p == q:
            return False
        if t >= self.gst:
            if q in self.net.crashed:
                return True
            if q == self.trusted:
                return False
        coin = random.Random(((self.seed * 1000003 + t) * 1009 + p) * 1013 + q).random()
        out = coin < self.rate
        if out and q not in self.net.crashed:
            self.mistakes += 1
        return out


class CTProcess:
    def __init__(self, i: int, v: int, n: int, net: Network, fd: DiamondS, log: dict) -> None:
        self.i, self.n, self.net, self.fd, self.log = i, n, net, fd, log
        self.est, self.ts, self.r = v, 0, 0  # @line L1
        self.decision: Optional[int] = None
        self.relayed = False
        self.ests: dict[int, list[tuple[int, int]]] = {}
        self.props: dict[int, int] = {}
        self.replies: dict[int, list[str]] = {}
        self.stage = "new"
        self.majority = n // 2 + 1  # = ceil((n + 1) / 2)

    def coord(self, r: int) -> int:
        return r % self.n

    def receive(self, src: int, msg: tuple) -> None:
        kind = msg[0]
        if kind == "EST":
            self.ests.setdefault(msg[1], []).append((msg[2], msg[3]))
        elif kind == "PROP":
            self.props[msg[1]] = msg[2]
        elif kind == "REPLY":
            self.replies.setdefault(msg[1], []).append(msg[2])
        elif kind == "DEC" and not self.relayed:  # @line L14
            self.relayed = True
            self.net.broadcast(self.i, msg, skip_self=True)  # relay first, then decide
            if self.i not in self.net.crashed and self.decision is None:
                self.decision = msg[1]
                self.log["decisions"].append((self.i, msg[1], self.r))

    def progress(self, t: int) -> None:
        net, i = self.net, self.i
        while i not in net.crashed and self.decision is None:  # @line L2
            r, c = self.r, self.coord(self.r)
            if self.stage == "new":
                self.r += 1  # @line L3
                r, c = self.r, self.coord(self.r)
                net.send(i, c, ("EST", r, self.est, self.ts))  # @line L4
                self.stage = "p2" if i == c else "p3"  # @line L5
            elif self.stage == "p2":
                got = self.ests.get(r, [])
                if len(got) < self.majority:  # @line L6
                    return
                v = max(got[: self.majority], key=lambda e: e[1])[0]
                self.log["proposals"].append((r, v))
                net.broadcast(i, ("PROP", r, v))  # @line L7
                self.stage = "p3"
            elif self.stage == "p3":
                if r in self.props:  # @line L8
                    self.est, self.ts = self.props[r], r  # @line L9
                    net.send(i, c, ("REPLY", r, "ack"))
                elif self.fd.suspects(t, i, c):
                    net.send(i, c, ("REPLY", r, "nack"))  # @line L10
                else:
                    return
                self.stage = "p4" if i == c else "new"  # @line L11
            elif self.stage == "p4":
                got = self.replies.get(r, [])
                if len(got) < self.majority:  # @line L12
                    return
                if all(x == "ack" for x in got[: self.majority]):
                    self.log["rbcast"].append((r, self.est))
                    net.broadcast(i, ("DEC", self.est))  # @line L13
                self.stage = "new"


def run(inputs: list[int], f: int, seed: int, gst: int, crash_after: Optional[dict[int, int]] = None, mode: str = "random", max_steps: int = 100000) -> dict:
    n = len(inputs)
    assert n > 2 * f
    crash_after = dict(crash_after or {})
    assert len(crash_after) <= f
    rng = random.Random(seed)
    net = Network(n, rng, crash_after, mode)
    correct = [p for p in range(n) if p not in crash_after]
    fd = DiamondS(seed, gst, rng.choice(correct), net)
    log: dict = {"decisions": [], "proposals": [], "rbcast": []}
    procs = [CTProcess(i, inputs[i], n, net, fd, log) for i in range(n)]
    t = 0
    while t < max_steps and any(procs[p].decision is None for p in correct):
        for p in procs:
            p.progress(t)
        m = net.pop()
        if m is not None and m[0] not in net.crashed:
            procs[m[0]].receive(m[1], m[2])
        t += 1
    return {
        "decisions": {p: d for p, d, _ in log["decisions"]},
        "rounds": max((procs[p].r for p in correct), default=0),
        "steps": t,
        "correct": correct,
        "trusted": fd.trusted,
        "mistakes": fd.mistakes,
        "log": log,
        "sent": list(net.sent),
        "crashed": sorted(net.crashed),
    }


def violations(inputs: list[int], res: dict) -> list[str]:
    bad = []
    vals = set(res["decisions"].values())
    if len(vals) > 1:
        bad.append("agreement")
    if vals - set(inputs):
        bad.append("validity")
    if any(p not in res["decisions"] for p in res["correct"]):
        bad.append("termination")
    return bad
