# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fifo-broadcast/. The authors are listed in prov/271TJB.jsonl.

"""FIFO broadcast: reliable broadcast plus per-sender sequence numbers.

Each broadcast carries the sender's sequence number s. A receiver keeps, for
each sender k, the next number next[k] that it expects, buffers messages
that arrive early, and delivers the messages of each sender in the order of
their numbers. Messages of different senders are not ordered against each
other. The module also has a seeded simulator: eager reliable broadcast over
a network with arbitrary delays, and processes that crash in the middle of
sending. Costs: O(1) expected time per delivered message with a hash map,
one integer per message.
"""

import random

Msg = tuple[int, int, int]  # (sender, sequence number, message id)


class FifoBroadcastProcess:
    """The FIFO layer at process i of n."""

    def __init__(self, i: int, n: int) -> None:
        self.i = i
        self.lsn = 0  # @line L1
        self.next = [1] * n
        self.pending: dict[tuple[int, int], int] = {}  # (sender, number) -> message id
        self.delivered: list[int] = []

    def broadcast(self, mid: int) -> Msg:
        """Number a new message, deliver it locally, and return it for the reliable broadcast layer."""
        self.lsn += 1  # @line L2
        msg = (self.i, self.lsn, mid)  # @line L3
        self.delivered.append(mid)  # @line L4
        self.next[self.i] += 1
        return msg

    def on_rb_deliver(self, msg: Msg) -> list[int]:
        """Handle a message from another process; return the ids delivered now, in order."""
        j, s, mid = msg
        self.pending[(j, s)] = mid  # @line L5
        out: list[int] = []
        while (j, self.next[j]) in self.pending:  # @line L6
            m = self.pending.pop((j, self.next[j]))  # @line L7
            self.delivered.append(m)
            self.next[j] += 1
            out.append(m)
        return out


class Simulation:
    """Eager reliable broadcast plus the FIFO layer, with seeded delays and crashes."""

    def __init__(self, n: int, rng: random.Random, crash_prob: float = 0.0) -> None:
        self.n = n
        self.rng = rng
        self.crash_prob = crash_prob
        self.procs = [FifoBroadcastProcess(i, n) for i in range(n)]
        self.crashed: set[int] = set()
        self.seen: list[set[int]] = [set() for _ in range(n)]
        self.network: list[tuple[int, Msg]] = []  # (destination, message)
        self.received: list[list[int]] = [[] for _ in range(n)]  # reliable-broadcast delivery order
        self.deps: dict[int, frozenset[int]] = {}  # ground truth: what the sender had delivered
        self.sender: dict[int, int] = {}
        self.number: dict[int, int] = {}
        self.next_mid = 0

    def fan_out(self, p: int, msg: Msg, may_crash: bool) -> None:
        """Send msg to all others. A process may crash after sending to only some of them."""
        dests = [q for q in range(self.n) if q != p]
        self.rng.shuffle(dests)
        if may_crash and self.rng.random() < self.crash_prob:
            dests = dests[: self.rng.randint(0, len(dests))]
            self.crashed.add(p)
        for q in dests:
            self.network.append((q, msg))

    def broadcast(self, p: int, may_crash: bool = True) -> int:
        mid = self.next_mid
        self.next_mid += 1
        self.deps[mid] = frozenset(self.procs[p].delivered)
        self.sender[mid] = p
        msg = self.procs[p].broadcast(mid)
        self.number[mid] = msg[1]
        self.seen[p].add(mid)
        self.received[p].append(mid)
        self.fan_out(p, msg, may_crash)
        return mid

    def step_network(self, k: int, may_crash: bool = True) -> None:
        """Deliver the k-th packet in transit. Packets to crashed processes are dropped."""
        q, msg = self.network.pop(k)
        if q in self.crashed or msg[2] in self.seen[q]:
            return
        self.seen[q].add(msg[2])
        self.received[q].append(msg[2])
        self.fan_out(q, msg, may_crash)  # eager relay, before the local delivery
        if q not in self.crashed:
            self.procs[q].on_rb_deliver(msg)

    def run(self, steps: int) -> None:
        for _ in range(steps):
            alive = [p for p in range(self.n) if p not in self.crashed]
            if not alive:
                break
            if self.network and self.rng.random() < 0.6:
                self.step_network(self.rng.randrange(len(self.network)))
            else:
                self.broadcast(self.rng.choice(alive))
        while self.network:  # no more crashes; every packet arrives after an arbitrary delay
            self.step_network(self.rng.randrange(len(self.network)), may_crash=False)

    def correct(self) -> list[int]:
        return [p for p in range(self.n) if p not in self.crashed]
