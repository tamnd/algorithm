# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/active-replication/. The authors are listed in prov/9FZTP1.jsonl.

"""Active replication (the state machine approach) in a discrete event simulator.

Schneider (1990). Every replica runs the same deterministic state machine and
applies every command, in the order fixed by a total-order broadcast. The
simulator gives total-order broadcast as a sequencer service that numbers the
commands and does not fail; the consensus pages show how to build it. Links
have seeded random delays, so numbered commands can arrive out of order, and
each replica holds them back until the next number arrives.

Faults: a replica can crash at a seeded time (it then does nothing), or it can
be Byzantine (it sends a wrong output). A client waits for the first reply when
faults are crashes, and for f + 1 equal replies when up to f replicas are
Byzantine, so 2f + 1 replicas are enough for the vote.
"""

import heapq
import random
from typing import Callable, Hashable

Command = tuple
State = tuple


class Sim:
    """A heap of timed events with seeded message delays and crashes."""

    def __init__(self, seed: int, delay: tuple[int, int] = (1, 10)) -> None:
        self.rng = random.Random(seed)
        self.delay = delay
        self.now = 0
        self.heap: list = []
        self.seq = 0
        self.crashed: set[Hashable] = set()
        self.handlers: dict[Hashable, Callable] = {}
        self.messages = 0

    def at(self, t: int, fn: Callable[[], None]) -> None:
        heapq.heappush(self.heap, (t, self.seq, fn))
        self.seq += 1

    def send(self, src: Hashable, dst: Hashable, msg: tuple) -> None:
        if src in self.crashed:
            return
        self.messages += 1
        t = self.now + self.rng.randint(*self.delay)
        self.at(t, lambda: self.deliver(dst, src, msg))

    def deliver(self, dst: Hashable, src: Hashable, msg: tuple) -> None:
        if dst not in self.crashed:
            self.handlers[dst](src, msg)

    def run(self) -> None:
        while self.heap:
            t, _, fn = heapq.heappop(self.heap)
            self.now = t
            fn()


# ---------------------------------------------------------------- state machine

def kv_apply(state: State, cmd: Command) -> tuple[State, object]:
    """A deterministic key-value store. The state is a sorted tuple of (key, value)."""
    d = dict(state)
    op = cmd[0]
    if op == "put":
        d[cmd[1]] = cmd[2]
        out: object = "ok"
    elif op == "add":
        d[cmd[1]] = d.get(cmd[1], 0) + cmd[2]
        out = d[cmd[1]]
    elif op == "cas":
        ok = d.get(cmd[1]) == cmd[2]
        if ok:
            d[cmd[1]] = cmd[3]
        out = ok
    else:  # get
        out = d.get(cmd[1])
    return tuple(sorted(d.items())), out


def sequential(cmds: list[Command]) -> tuple[list[State], list[object]]:
    """The states s_0, s_1, ... and outputs of one replica that runs cmds in order."""
    s: State = ()
    states, outs = [s], []
    for c in cmds:
        s, o = kv_apply(s, c)
        states.append(s)
        outs.append(o)
    return states, outs


# ---------------------------------------------------------------- processes

class Replica:
    def __init__(self, rid: int, sim: Sim, byzantine: bool = False,
                 apply: Callable = kv_apply) -> None:
        self.rid = rid
        self.sim = sim
        self.byzantine = byzantine
        self.apply = apply
        self.state: State = ()
        self.next = 1
        self.buffer: dict[int, tuple[Command, int]] = {}
        self.history: list[State] = [()]

    def on_message(self, src: Hashable, msg: tuple) -> None:
        _, k, cmd, client = msg  # ("DELIVER", k, cmd, client)
        self.buffer[k] = (cmd, client)  # @line L1
        while self.next in self.buffer:  # @line L2
            cmd, client = self.buffer.pop(self.next)  # @line L3
            self.state, out = self.apply(self.state, cmd)  # @line L4
            self.history.append(self.state)
            if self.byzantine:
                out = ("lie", self.rid, self.next)
            self.sim.send(("R", self.rid), ("C", client), ("REPLY", self.next, out))  # @line L5
            self.next += 1  # @line L6


class Sequencer:
    """Total-order broadcast as a service: number each command, send it to all replicas."""

    def __init__(self, sim: Sim, n: int) -> None:
        self.sim = sim
        self.n = n
        self.k = 0
        self.log: list[Command] = []
        self.sent_at: list[int] = []

    def on_message(self, src: Hashable, msg: tuple) -> None:
        _, cmd, client, t = msg
        self.k += 1
        self.log.append(cmd)
        self.sent_at.append(t)
        for r in range(self.n):
            self.sim.send("SEQ", ("R", r), ("DELIVER", self.k, cmd, client))


class Client:
    def __init__(self, cid: int, sim: Sim, need: int) -> None:
        self.cid = cid
        self.sim = sim
        self.need = need
        self.votes: dict[int, dict[object, int]] = {}
        self.result: dict[int, object] = {}
        self.latency: dict[int, int] = {}

    def invoke(self, cmd: Command) -> None:
        self.sim.send(("C", self.cid), "SEQ", ("BCAST", cmd, self.cid, self.sim.now))  # @line L7

    def on_message(self, src: Hashable, msg: tuple) -> None:
        _, k, out = msg
        if k in self.result:
            return
        box = self.votes.setdefault(k, {})
        box[out] = box.get(out, 0) + 1  # @line L8
        if box[out] >= self.need:
            self.result[k] = out  # @line L9
            self.latency[k] = self.sim.now


def run(seed: int, n: int, cmds: list[Command], crash: dict[int, int] | None = None,
        byzantine: set[int] | None = None, need: int = 1,
        apply: Callable = kv_apply) -> dict:
    """Run one client that sends cmds at times 0, 3, 6, ... to n replicas.

    crash maps a replica to the time of its crash. The result holds the replicas,
    the client, the order fixed by the sequencer and the time at which the client
    sent the k-th command of that order.
    """
    sim = Sim(seed)
    crash = crash or {}
    byzantine = byzantine or set()
    reps = [Replica(i, sim, i in byzantine, apply) for i in range(n)]
    seq = Sequencer(sim, n)
    cl = Client(0, sim, need)
    for r in reps:
        sim.handlers[("R", r.rid)] = r.on_message
    sim.handlers["SEQ"] = seq.on_message
    sim.handlers[("C", 0)] = cl.on_message
    for i, c in enumerate(cmds):
        sim.at(3 * i, lambda c=c: cl.invoke(c))
    for r, t in crash.items():
        sim.at(t, lambda r=r: sim.crashed.add(("R", r)))
    sim.run()
    return {"replicas": reps, "client": cl, "order": seq.log, "sent_at": seq.sent_at, "sim": sim}
