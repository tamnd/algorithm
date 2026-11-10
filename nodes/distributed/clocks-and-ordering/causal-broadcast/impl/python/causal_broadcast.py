# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/causal-broadcast/. The authors are listed in prov/Y3V5CE.jsonl.

"""Causal broadcast with vector timestamps (Birman, Schiper and Stephenson 1991).

Each process keeps a vector VC, where VC[k] counts the messages of p_k that
it has delivered. A broadcast carries VT, the sender's VC with its own entry
raised by 1. A receiver buffers a message from p_j until VT[j] = VC[j] + 1
and VT[k] <= VC[k] for every k != j, then delivers it and raises VC[j].
The layer runs on top of a reliable broadcast. The module also has a seeded
simulator: eager reliable broadcast over a network with arbitrary delays,
and processes that crash in the middle of sending.
Costs: O(n) per test of one buffered message, n integers per message.
"""

import random

Msg = tuple[int, tuple[int, ...], int]  # (sender, VT, message id)


class CausalBroadcastProcess:
    """The causal layer at process i of n."""

    def __init__(self, i: int, n: int) -> None:
        self.i = i
        self.vc = [0] * n  # @line L1
        self.pending: list[Msg] = []
        self.delivered: list[int] = []

    def broadcast(self, mid: int) -> Msg:
        """Stamp a new message, deliver it locally, and return it for the reliable broadcast layer."""
        vt = list(self.vc)  # @line L2
        vt[self.i] += 1
        msg = (self.i, tuple(vt), mid)  # @line L3
        self.delivered.append(mid)  # @line L4
        self.vc[self.i] += 1
        return msg

    def deliverable(self, msg: Msg) -> bool:
        j, vt, _ = msg
        if vt[j] != self.vc[j] + 1:
            return False
        return all(vt[k] <= self.vc[k] for k in range(len(vt)) if k != j)

    def on_rb_deliver(self, msg: Msg) -> list[int]:
        """Handle a message from another process; return the ids delivered now, in order."""
        self.pending.append(msg)  # @line L5
        out: list[int] = []
        progress = True
        while progress:  # @line L6
            progress = False
            for m in self.pending:
                if self.deliverable(m):
                    self.pending.remove(m)  # @line L7
                    self.delivered.append(m[2])
                    self.vc[m[0]] += 1
                    out.append(m[2])
                    progress = True
                    break
        return out


class Simulation:
    """Eager reliable broadcast plus the causal layer, with seeded delays and crashes."""

    def __init__(self, n: int, rng: random.Random, crash_prob: float = 0.0) -> None:
        self.n = n
        self.rng = rng
        self.crash_prob = crash_prob
        self.procs = [CausalBroadcastProcess(i, n) for i in range(n)]
        self.crashed: set[int] = set()
        self.seen: list[set[int]] = [set() for _ in range(n)]
        self.network: list[tuple[int, Msg]] = []  # (destination, message)
        self.received: list[list[int]] = [[] for _ in range(n)]  # reliable-broadcast delivery order
        self.deps: dict[int, frozenset[int]] = {}  # ground truth: what the sender had delivered
        self.sender: dict[int, int] = {}
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
