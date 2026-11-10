# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ben-or-consensus/. The authors are listed in prov/G8VCBD.jsonl.

"""Ben-Or's randomized binary consensus for crash failures, n > 2f.

The run is a deterministic discrete event simulation. A seeded scheduler
picks the next message to deliver from the set of messages in transit. A
process crashes when it tries its (k + 1)-th send, where k = crash_after[p],
so a crash can fall in the middle of a broadcast. Each process has its own
seeded coin. No threads, no sockets, no clocks.
"""

import random
from typing import Optional

Q = "?"  # the "no value" proposal


class Network:
    """Messages in transit, a seeded scheduler and crash injection by send count."""

    def __init__(self, n: int, rng: random.Random, crash_after: Optional[dict[int, int]] = None, mode: str = "random") -> None:
        self.n, self.rng, self.mode = n, rng, mode
        self.crash_after = dict(crash_after or {})
        self.crashed: set[int] = set()
        self.sent = [0] * n
        self.pending: list[tuple[int, int, tuple]] = []
        self.procs: list = []

    def send(self, src: int, dest: int, msg: tuple) -> bool:
        if src in self.crashed:
            return False
        if src in self.crash_after and self.sent[src] >= self.crash_after[src]:
            self.crashed.add(src)  # the crash may cut a broadcast in two
            return False
        self.sent[src] += 1
        self.pending.append((dest, src, msg))
        return True

    def broadcast(self, src: int, msg: tuple) -> None:
        for dest in range(self.n):
            if not self.send(src, dest, msg):
                return

    def pick(self) -> int:
        if self.mode == "fifo":
            return 0
        if self.mode == "lifo":
            # newest first, but every 8th pick takes the oldest, so the
            # schedule stays fair and each message is delivered in the end
            self.picks = getattr(self, "picks", 0) + 1
            return 0 if self.picks % 8 == 0 else len(self.pending) - 1
        if self.mode == "split":
            return self._pick_split()
        return self.rng.randrange(len(self.pending))

    def _pick_split(self) -> int:
        """An adversary that sees the values and tries to keep each process
        from seeing a majority in phase 1. Other messages go in random order."""
        order = list(range(len(self.pending)))
        self.rng.shuffle(order)
        for i in order:
            dest, _, msg = self.pending[i]
            p = self.procs[dest]
            if msg[0] != "R" or msg[1] != p.r or p.phase != 1:
                continue
            got = list(p.reports.get(p.r, {}).values())
            ones = sum(1 for v in got if v == 1)
            zeros = len(got) - ones
            if (msg[2] == 1 and ones <= zeros) or (msg[2] == 0 and zeros <= ones):
                return i
        for i in order:
            dest, _, msg = self.pending[i]
            p = self.procs[dest]
            if not (msg[0] == "R" and msg[1] == p.r and p.phase == 1):
                return i
        return order[0]

    def step(self) -> bool:
        if not self.pending:
            return False
        dest, src, msg = self.pending.pop(self.pick())
        if dest not in self.crashed:
            self.procs[dest].receive(src, msg)
        return True


class BenOrProcess:
    def __init__(self, i: int, x: int, n: int, f: int, net: Network, coin: random.Random) -> None:
        self.i, self.n, self.f, self.net, self.coin = i, n, f, net, coin
        self.x = x  # @line L1
        self.r = 1
        self.decision: Optional[int] = None
        self.decided_round: Optional[int] = None
        self.phase = 1
        self.reports: dict[int, dict[int, int]] = {}
        self.proposals: dict[int, dict[int, object]] = {}
        self.history: list[int] = []

    def start(self) -> None:
        self.net.broadcast(self.i, ("R", self.r, self.x))  # @line L3

    def receive(self, src: int, msg: tuple) -> None:
        kind, r, v = msg
        box = self.reports if kind == "R" else self.proposals
        box.setdefault(r, {})[src] = v
        self._progress()

    def _progress(self) -> None:
        n, f = self.n, self.f
        while self.i not in self.net.crashed:  # @line L2
            if self.phase == 1:
                got = self.reports.get(self.r, {})
                if len(got) < n - f:  # @line L4
                    return
                vals = list(got.values())[: n - f]
                prop: object = Q
                for v in (0, 1):
                    if 2 * vals.count(v) > n:  # @line L5
                        prop = v
                self.phase = 2
                self.net.broadcast(self.i, ("P", self.r, prop))  # @line L6
            else:
                got = self.proposals.get(self.r, {})
                if len(got) < n - f:  # @line L7
                    return
                vals = list(got.values())[: n - f]
                real = [v for v in vals if v != Q]
                for v in (0, 1):
                    if vals.count(v) >= f + 1 and self.decision is None:  # @line L8
                        self.decision, self.decided_round = v, self.r
                if real:
                    self.x = real[0]  # @line L9
                else:
                    self.x = self.coin.randrange(2)  # @line L10
                self.history.append(self.x)  # x at the end of round r
                self.r += 1  # @line L11
                self.phase = 1
                self.net.broadcast(self.i, ("R", self.r, self.x))  # @line L3


def run(inputs: list[int], f: int, seed: int, crash_after: Optional[dict[int, int]] = None, mode: str = "random", max_steps: int = 200000) -> dict:
    """Run Ben-Or until each process that never crashes has decided."""
    n = len(inputs)
    assert n > 2 * f
    crash_after = dict(crash_after or {})
    assert len(crash_after) <= f
    net = Network(n, random.Random(seed), crash_after, mode)
    procs = [BenOrProcess(i, inputs[i], n, f, net, random.Random(seed * 7919 + i)) for i in range(n)]
    net.procs = procs
    for p in procs:
        p.start()
    correct = [i for i in range(n) if i not in crash_after]
    steps = 0
    while any(procs[i].decision is None for i in correct):
        if not net.step() or steps >= max_steps:
            break
        steps += 1
    decisions = {i: p.decision for i, p in enumerate(procs) if p.decision is not None}
    rounds = max((procs[i].decided_round or 0) for i in correct)
    return {
        "decisions": decisions,
        "rounds": rounds,
        "steps": steps,
        "crashed": sorted(net.crashed),
        "correct": correct,
        "sent": list(net.sent),
        "decided_round": {i: p.decided_round for i, p in enumerate(procs) if p.decision is not None},
        "history": [list(p.history) for p in procs],
    }


def violations(inputs: list[int], result: dict) -> list[str]:
    """The consensus properties that a finished run breaks."""
    bad = []
    vals = set(result["decisions"].values())
    if len(vals) > 1:
        bad.append("agreement")
    if len(set(inputs)) == 1 and vals - set(inputs):
        bad.append("validity")
    if any(i not in result["decisions"] for i in result["correct"]):
        bad.append("termination")
    return bad
