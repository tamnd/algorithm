# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flooding/. The authors are listed in prov/0WMBJP.jsonl.

"""Flooding broadcast from one source, in a synchronous and an asynchronous network.

The network is a connected undirected graph given by adjacency lists. The
source s holds a message M. Each node forwards M once, on its first receipt,
to every neighbour except the one it got the first copy from. The run sends
exactly 2m - (n - 1) messages in every timing model.

flood_sync runs lock-step rounds (send, then receive, then compute) and
returns the round in which each node got M. flood_async runs a discrete
event simulation in which a seeded scheduler gives each message a delay in
(0, 1], so one time unit is the largest delay.
Cost of the simulation: O(n + m log m) time.
"""

import heapq
import random


class FloodNode:
    """The local state of one node: reached, parent, and the time of first receipt."""

    def __init__(self, v: int, nbrs: list[int]) -> None:
        self.v = v
        self.nbrs = nbrs
        self.reached = False
        self.parent: int | None = None
        self.when: float | None = None

    def start(self) -> list[tuple[int, str]]:  # @line L1
        self.reached = True  # @line L2
        self.parent = self.v
        self.when = 0
        return [(w, "M") for w in self.nbrs]  # @line L3

    def receive(self, u: int, now: float) -> list[tuple[int, str]]:  # @line L4
        if self.reached:  # @line L5
            return []  # @line L6
        self.reached = True  # @line L7
        self.parent = u
        self.when = now
        return [(w, "M") for w in self.nbrs if w != u]  # @line L8


def flood_sync(adj: list[list[int]], s: int) -> dict:
    """Synchronous flooding. Returns parent, round of first receipt, messages and rounds.

    In a round in which a node gets several first copies, it takes the
    sender with the smallest index as its parent.
    """
    n = len(adj)
    nodes = [FloodNode(v, adj[v]) for v in range(n)]
    outbox = {s: nodes[s].start()}
    messages = 0
    rnd = 0
    per_round = []
    while outbox:
        rnd += 1
        inbox: dict[int, list[int]] = {}
        sent = 0
        for v in sorted(outbox):
            for w, _ in outbox[v]:
                inbox.setdefault(w, []).append(v)
                sent += 1
        messages += sent
        per_round.append(sent)
        outbox = {}
        for w in sorted(inbox):
            senders = sorted(inbox[w])
            out = nodes[w].receive(senders[0], rnd)
            if out:
                outbox[w] = out
    return {
        "parent": [x.parent for x in nodes],
        "round": [x.when for x in nodes],
        "messages": messages,
        "rounds": rnd,
        "per_round": per_round,
    }


class AsyncNet:
    """A seeded asynchronous network. Each message gets a delay in (0, 1].

    schedule: "random" (uniform delays), "slow" (messages from the node
    `slow` take the full unit, all others are fast), or "lifo" (a message
    sent later gets a shorter delay, so delivery order is close to reversed).
    """

    def __init__(self, n: int, seed: int = 0, schedule: str = "random", slow: int = -1) -> None:
        self.rng = random.Random(seed)
        self.schedule = schedule
        self.slow = slow
        self.queue: list[tuple[float, int, int, int, object]] = []
        self.seq = 0
        self.now = 0.0
        self.messages = 0

    def delay(self, src: int) -> float:
        if self.schedule == "slow":
            return 1.0 if src == self.slow else self.rng.uniform(0.001, 0.01)
        if self.schedule == "lifo":
            return max(0.0005, 1.0 - 0.0005 * self.seq)
        return self.rng.uniform(0.01, 1.0)

    def send(self, src: int, dst: int, msg: object) -> None:
        self.seq += 1
        self.messages += 1
        t = self.now + self.delay(src)
        key = -self.seq if self.schedule == "lifo" else self.seq
        heapq.heappush(self.queue, (t, key, src, dst, msg))

    def pop(self) -> tuple[int, int, object]:
        t, _, src, dst, msg = heapq.heappop(self.queue)
        self.now = t
        return src, dst, msg


def flood_async(adj: list[list[int]], s: int, seed: int = 0, schedule: str = "random", slow: int = -1) -> dict:
    """Asynchronous flooding under a seeded scheduler. Returns parent, messages and time."""
    n = len(adj)
    nodes = [FloodNode(v, adj[v]) for v in range(n)]
    net = AsyncNet(n, seed, schedule, slow)
    for w, msg in nodes[s].start():
        net.send(s, w, msg)
    while net.queue:
        src, dst, _ = net.pop()
        for w, msg in nodes[dst].receive(src, net.now):
            net.send(dst, w, msg)
    return {
        "parent": [x.parent for x in nodes],
        "reached_at": [x.when for x in nodes],
        "messages": net.messages,
        "time": net.now,
    }


# ------------------------------------------------------------ graph helpers


def edges_to_adj(n: int, edges: set[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in sorted(edges):
        adj[u].append(v)
        adj[v].append(u)
    return adj


def random_tree(n: int, rng: random.Random) -> set[tuple[int, int]]:
    return {(rng.randrange(v), v) for v in range(1, n)}


def make_graph(kind: str, n: int, seed: int) -> list[list[int]]:
    """Seeded connected graphs: tree, path, grid (about n nodes) or gnp (G(n, p) plus a tree)."""
    rng = random.Random(seed)
    if kind == "path":
        return edges_to_adj(n, {(v - 1, v) for v in range(1, n)})
    if kind == "tree":
        return edges_to_adj(n, random_tree(n, rng))
    if kind == "grid":
        a = max(1, int(n ** 0.5))
        b = max(1, n // a)
        edges = set()
        for i in range(a):
            for j in range(b):
                v = i * b + j
                if j + 1 < b:
                    edges.add((v, v + 1))
                if i + 1 < a:
                    edges.add((v, v + b))
        return edges_to_adj(a * b, edges)
    if kind == "gnp":
        p = rng.uniform(0.05, 0.5)
        edges = random_tree(n, rng)
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < p:
                    edges.add((u, v))
        return edges_to_adj(n, edges)
    raise ValueError(kind)


def bfs_dist(adj: list[list[int]], s: int) -> list[int]:
    dist = [-1] * len(adj)
    dist[s] = 0
    frontier = [s]
    while frontier:
        nxt = []
        for v in frontier:
            for w in adj[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    nxt.append(w)
        frontier = nxt
    return dist
