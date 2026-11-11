# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/synchronizer/. The authors are listed in prov/S5XWV5.jsonl.

"""Awerbuch's synchronizers alpha and beta, run on a seeded asynchronous network.

A synchronous algorithm is given as a factory make(v, nbrs) that returns an
object with two methods:
    send(p)          -> list of (neighbour, message) for round p
    receive(p, msgs) -> None, msgs is the list of (sender, message) of round p
and an attribute `out`. run_sync runs it in lock-step rounds 1..P. run_alpha
and run_beta run the same algorithm on an asynchronous network with delays
in (0, 1] and return the same outputs, the same received messages per round,
and the counts of the extra messages:

    alpha: one ACK per algorithm message, and SAFE(p) on every edge in both
           directions in every pulse: M_S + 2 m P extra messages, time <= 3P.
    beta:  one ACK per algorithm message, and per pulse a convergecast and
           a broadcast on a rooted spanning tree of height h:
           M_S + 2 (n - 1) P extra messages, time <= P (2h + 2).
"""

import heapq
import random
from typing import Callable

Factory = Callable[[int, list[int]], object]


def _key(item: tuple) -> tuple:
    return (item[0], repr(item[1]))


def run_sync(adj: list[list[int]], make: Factory, P: int) -> dict:
    n = len(adj)
    algs = [make(v, adj[v]) for v in range(n)]
    trace: list[list[list]] = [[] for _ in range(n)]
    messages = 0
    for p in range(1, P + 1):
        inbox: list[list] = [[] for _ in range(n)]
        for v in range(n):
            for w, x in algs[v].send(p):
                inbox[w].append((v, x))
                messages += 1
        for v in range(n):
            got = sorted(inbox[v], key=_key)
            trace[v].append(got)
            algs[v].receive(p, got)
    return {"out": [a.out for a in algs], "trace": trace, "alg_messages": messages}


class _Net:
    def __init__(self, seed: int) -> None:
        self.rng = random.Random(seed)
        self.queue: list = []
        self.seq = 0
        self.now = 0.0
        self.count: dict[str, int] = {}

    def send(self, src: int, dst: int, msg: tuple) -> None:
        self.seq += 1
        self.count[msg[0]] = self.count.get(msg[0], 0) + 1
        heapq.heappush(self.queue, (self.now + self.rng.uniform(0.01, 1.0), self.seq, src, dst, msg))

    def run(self, nodes: list) -> None:
        while self.queue:
            t, _, src, dst, msg = heapq.heappop(self.queue)
            self.now = t
            nodes[dst].on_message(src, msg)


class _Base:
    def __init__(self, v: int, nbrs: list[int], alg: object, net: _Net, P: int) -> None:
        self.v = v
        self.nbrs = nbrs
        self.alg = alg
        self.net = net
        self.P = P
        self.p = 0
        self.pending = 0
        self.safe = False
        self.buffer: dict[int, list] = {}
        self.trace: list[list] = []
        self.finished_at = 0.0

    def start_pulse(self, p: int) -> None:  # @line L1
        self.p, self.safe = p, False
        out = self.alg.send(p)
        self.pending = len(out)
        for w, x in out:
            self.net.send(self.v, w, ("ALG", p, x))
        if self.pending == 0:
            self.become_safe()

    def on_alg(self, u: int, p: int, x: object) -> None:  # @line L2
        self.buffer.setdefault(p, []).append((u, x))
        self.net.send(self.v, u, ("ACK", p))

    def on_ack(self) -> None:
        self.pending -= 1
        if self.pending == 0:
            self.become_safe()

    def deliver(self, p: int) -> None:  # @line L5
        got = sorted(self.buffer.pop(p, []), key=_key)
        self.trace.append(got)
        self.alg.receive(p, got)
        self.finished_at = self.net.now
        if p < self.P:
            self.start_pulse(p + 1)

    def become_safe(self) -> None:
        raise NotImplementedError


class AlphaNode(_Base):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.safe_from: dict[int, int] = {}

    def become_safe(self) -> None:  # @line L3
        self.safe = True
        for w in self.nbrs:
            self.net.send(self.v, w, ("SAFE", self.p))
        self.check()

    def check(self) -> None:  # @line L4
        if self.safe and self.safe_from.get(self.p, 0) == len(self.nbrs):
            self.safe_from.pop(self.p, None)
            self.deliver(self.p)

    def on_message(self, u: int, msg: tuple) -> None:
        if msg[0] == "ALG":
            self.on_alg(u, msg[1], msg[2])
        elif msg[0] == "ACK":
            self.on_ack()
        else:
            self.safe_from[msg[1]] = self.safe_from.get(msg[1], 0) + 1
            self.check()


class BetaNode(_Base):
    def __init__(self, v, nbrs, alg, net, P, parent: int, children: list[int]) -> None:
        super().__init__(v, nbrs, alg, net, P)
        self.parent = parent
        self.children = children
        self.reported = 0

    def become_safe(self) -> None:
        self.safe = True
        self.check()

    def check(self) -> None:
        if self.safe and self.reported == len(self.children):
            self.reported = 0
            self.safe = False
            if self.parent == self.v:
                self.go(self.p)
            else:
                self.net.send(self.v, self.parent, ("SUBTREE_SAFE", self.p))

    def go(self, p: int) -> None:
        for c in self.children:
            self.net.send(self.v, c, ("PULSE", p))
        self.deliver(p)

    def on_message(self, u: int, msg: tuple) -> None:
        kind = msg[0]
        if kind == "ALG":
            self.on_alg(u, msg[1], msg[2])
        elif kind == "ACK":
            self.on_ack()
        elif kind == "SUBTREE_SAFE":
            self.reported += 1
            self.check()
        else:
            self.go(msg[1])


def _finish(nodes: list, algs: list, net: _Net) -> dict:
    return {
        "out": [a.out for a in algs],
        "trace": [x.trace for x in nodes],
        "alg_messages": net.count.get("ALG", 0),
        "count": dict(net.count),
        "time": max(x.finished_at for x in nodes),
    }


def run_alpha(adj: list[list[int]], make: Factory, P: int, seed: int = 0) -> dict:
    n = len(adj)
    net = _Net(seed)
    algs = [make(v, adj[v]) for v in range(n)]
    nodes = [AlphaNode(v, adj[v], algs[v], net, P) for v in range(n)]
    for x in nodes:
        x.start_pulse(1)
    net.run(nodes)
    return _finish(nodes, algs, net)


def run_beta(adj: list[list[int]], parent: list[int], make: Factory, P: int, seed: int = 0) -> dict:
    """parent describes a rooted spanning tree of the graph (parent[root] == root)."""
    n = len(adj)
    net = _Net(seed)
    algs = [make(v, adj[v]) for v in range(n)]
    children: list[list[int]] = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] != v:
            children[parent[v]].append(v)
    nodes = [BetaNode(v, adj[v], algs[v], net, P, parent[v], children[v]) for v in range(n)]
    for x in nodes:
        x.start_pulse(1)
    net.run(nodes)
    return _finish(nodes, algs, net)
