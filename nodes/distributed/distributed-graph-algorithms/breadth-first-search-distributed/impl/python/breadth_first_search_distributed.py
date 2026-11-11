# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breadth-first-search-distributed/. The authors are listed in prov/2CY7S7.jsonl.

"""Distributed breadth-first search from a root r, in three forms.

bfs_sync      the synchronous layered algorithm: one layer per round,
              exactly 2m - (n - 1) messages, the tree is a BFS tree.
bfs_bellman   the asynchronous Bellman-Ford style algorithm: a node takes
              any smaller distance it hears and forwards it. At most
              deg(r) + sum over v of (n - dist(v)) (deg(v) - 1) messages.
bfs_layered   the asynchronous layer-by-layer algorithm: the root runs
              phases; phase k grows the tree by layer k, with a broadcast
              (PULSE) down the tree, EXPLORE and ACK or REJECT on the edges
              of layer k - 1, and a convergecast (REPORT) back to the root.

The asynchronous runs use seeded delays in (0, 1], so one time unit is the
largest delay. Cost of each simulation: O(n m log(n m)) time at most.
"""

import heapq
import random

INF = float("inf")


# ---------------------------------------------------------------- synchronous


class SyncBFSNode:
    def __init__(self, v: int, nbrs: list[int]) -> None:
        self.v = v
        self.nbrs = nbrs
        self.dist: float = INF
        self.parent: int | None = None

    def start(self) -> list[tuple[int, int]]:  # @line L1
        self.dist = 0
        self.parent = self.v
        return [(w, 0) for w in self.nbrs]

    def round(self, received: list[tuple[int, int]]) -> list[tuple[int, int]]:  # @line L2
        if self.dist == INF:  # @line L3
            d, u = min((d, u) for u, d in received)  # @line L4
            self.dist = d + 1
            self.parent = u
            return [(w, self.dist) for w in self.nbrs if w != u]  # @line L5
        return []  # @line L6


def bfs_sync(adj: list[list[int]], r: int) -> dict:
    n = len(adj)
    nodes = [SyncBFSNode(v, adj[v]) for v in range(n)]
    outbox = {r: nodes[r].start()}
    messages, rnd = 0, 0
    while outbox:
        rnd += 1
        inbox: dict[int, list[tuple[int, int]]] = {}
        for v, msgs in outbox.items():
            for w, d in msgs:
                inbox.setdefault(w, []).append((v, d))
                messages += 1
        outbox = {}
        for w, got in inbox.items():
            out = nodes[w].round(got)
            if out:
                outbox[w] = out
    return {
        "dist": [x.dist for x in nodes],
        "parent": [x.parent for x in nodes],
        "messages": messages,
        "rounds": rnd,
    }


# ------------------------------------------------------- asynchronous network


class Net:
    def __init__(self, seed: int, schedule: str = "random") -> None:
        self.rng = random.Random(seed)
        self.schedule = schedule
        self.queue: list[tuple[float, int, int, int, tuple]] = []
        self.seq = 0
        self.now = 0.0
        self.messages = 0
        self.by_kind: dict[str, int] = {}

    def send(self, src: int, dst: int, msg: tuple) -> None:
        self.seq += 1
        self.messages += 1
        self.by_kind[msg[0]] = self.by_kind.get(msg[0], 0) + 1
        if self.schedule == "skewed":
            # Messages on edges to larger ids are slow, so long paths win races.
            d = 1.0 if dst > src + 1 else self.rng.uniform(0.001, 0.01)
        else:
            d = self.rng.uniform(0.01, 1.0)
        heapq.heappush(self.queue, (self.now + d, self.seq, src, dst, msg))

    def run(self, handle) -> None:
        while self.queue:
            t, _, src, dst, msg = heapq.heappop(self.queue)
            self.now = t
            handle(src, dst, msg)


def bfs_bellman(adj: list[list[int]], r: int, seed: int = 0, schedule: str = "random") -> dict:
    """Asynchronous Bellman-Ford BFS. Returns dist, parent, messages, updates and time."""
    n = len(adj)
    dist = [INF] * n
    parent: list[int | None] = [None] * n
    updates = [0] * n
    net = Net(seed, schedule)
    dist[r] = 0
    parent[r] = r
    for w in adj[r]:
        net.send(r, w, ("D", 0))

    def handle(u: int, v: int, msg: tuple) -> None:
        d = msg[1]
        if d + 1 < dist[v]:
            dist[v] = d + 1
            parent[v] = u
            updates[v] += 1
            for w in adj[v]:
                if w != u:
                    net.send(v, w, ("D", d + 1))

    net.run(handle)
    return {"dist": dist, "parent": parent, "messages": net.messages, "updates": updates, "time": net.now}


def bfs_layered(adj: list[list[int]], r: int, seed: int = 0, schedule: str = "random") -> dict:
    """Asynchronous layer-by-layer BFS. Returns dist, parent, messages by kind, phases and time."""
    n = len(adj)
    depth: list[int | None] = [None] * n
    parent: list[int | None] = [None] * n
    children: list[list[int]] = [[] for _ in range(n)]
    pending = [0] * n  # replies still expected by a frontier node
    waiting = [0] * n  # reports still expected from children
    found = [False] * n
    net = Net(seed, schedule)
    state = {"phases": 0, "done_at": 0.0}
    depth[r] = 0
    parent[r] = r

    def report(v: int, k: int) -> None:
        if v != r:
            net.send(v, parent[v], ("REPORT", k, found[v]))
        elif found[r]:
            start_phase(k + 1)
        else:
            state["done_at"] = net.now

    def pulse(v: int, k: int) -> None:
        found[v] = False
        if depth[v] == k - 1:
            nbrs = [w for w in adj[v] if w != parent[v] or v == r]
            pending[v] = len(nbrs)
            for w in nbrs:
                net.send(v, w, ("EXPLORE", k))
            if not nbrs:
                report(v, k)
        else:
            waiting[v] = len(children[v])
            for c in children[v]:
                net.send(v, c, ("PULSE", k))
            if not children[v]:
                report(v, k)

    def start_phase(k: int) -> None:
        state["phases"] = k
        pulse(r, k)

    def handle(u: int, v: int, msg: tuple) -> None:
        kind, k = msg[0], msg[1]
        if kind == "PULSE":
            pulse(v, k)
        elif kind == "EXPLORE":
            if depth[v] is None:
                depth[v] = k
                parent[v] = u
                net.send(v, u, ("ACK", k))
            else:
                net.send(v, u, ("REJECT", k))
        elif kind in ("ACK", "REJECT"):
            if kind == "ACK":
                children[v].append(u)
                found[v] = True
            pending[v] -= 1
            if pending[v] == 0:
                report(v, k)
        else:  # REPORT from a child
            found[v] = found[v] or msg[2]
            waiting[v] -= 1
            if waiting[v] == 0:
                report(v, k)

    start_phase(1)
    net.run(handle)
    return {
        "dist": depth,
        "parent": parent,
        "messages": net.messages,
        "by_kind": net.by_kind,
        "phases": state["phases"],
        "time": state["done_at"],
    }
