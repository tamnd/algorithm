# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floodmax/. The authors are listed in prov/ZNV8N8.jsonl.

"""FloodMax leader election in a synchronous network (Lynch, Section 4.1).

The network is a connected undirected graph given by adjacency lists; node v
holds the identifier ids[v]. All nodes know a bound d >= diam. The run is in
lock-step rounds: in each round every node sends, then every node receives.

FloodMax sends max on every edge in both directions in each round, so it
sends exactly 2 m d messages. The variant OptFloodMax sends only in round 1
and after its max has changed.
"""

import random
from collections import deque


class Process:
    """The local state of one node."""

    def __init__(self, uid: int, nbrs: list[int]) -> None:
        self.uid = uid
        self.nbrs = nbrs
        self.max = uid  # @line L1
        self.status = "unknown"
        self.changed = True

    def outgoing(self, opt: bool) -> list[tuple[int, int]]:
        if opt and not self.changed:
            return []
        return [(w, self.max) for w in self.nbrs]  # @line L3

    def receive(self, values: list[int]) -> None:
        self.changed = False
        for v in values:  # @line L4
            if v > self.max:  # @line L5
                self.max = v
                self.changed = True

    def decide(self) -> None:
        if self.max == self.uid:  # @line L6
            self.status = "leader"
        else:
            self.status = "non-leader"  # @line L7


def floodmax(adj: list[list[int]], ids: list[int], d: int, opt: bool = False) -> dict:
    """Run d rounds of FloodMax (or OptFloodMax) and return the result."""
    n = len(adj)
    if len(set(ids)) != n:
        raise ValueError("identifiers must be distinct")
    procs = [Process(ids[v], adj[v]) for v in range(n)]
    messages = 0
    history = [[p.max for p in procs]]
    for _ in range(d):  # @line L2
        inbox: list[list[int]] = [[] for _ in range(n)]
        for v in range(n):
            for w, val in procs[v].outgoing(opt):
                inbox[w].append(val)
                messages += 1
        for v in range(n):
            procs[v].receive(inbox[v])
        history.append([p.max for p in procs])
    for p in procs:
        p.decide()
    return {
        "status": [p.status for p in procs],
        "known": [p.max for p in procs],
        "leaders": [v for v in range(n) if procs[v].status == "leader"],
        "messages": messages,
        "history": history,
    }


def diameter(adj: list[list[int]]) -> int:
    """The diameter of a connected graph, by a BFS from every node."""
    best = 0
    for s in range(len(adj)):
        dist = {s: 0}
        q = deque([s])
        while q:
            v = q.popleft()
            for w in adj[v]:
                if w not in dist:
                    dist[w] = dist[v] + 1
                    q.append(w)
        if len(dist) != len(adj):
            raise ValueError("graph is not connected")
        best = max(best, max(dist.values()))
    return best


def random_connected_graph(n: int, extra: int, seed: int) -> list[list[int]]:
    """A random tree on n nodes plus up to extra random edges, seeded."""
    rng = random.Random(seed)
    edges = set()
    for v in range(1, n):
        u = rng.randrange(v)
        edges.add((u, v))
    for _ in range(extra):
        u, v = rng.sample(range(n), 2) if n > 1 else (0, 0)
        if u != v:
            edges.add((min(u, v), max(u, v)))
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in sorted(edges):
        adj[u].append(v)
        adj[v].append(u)
    return adj
