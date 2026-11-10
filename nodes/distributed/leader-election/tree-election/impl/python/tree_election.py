# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-election/. The authors are listed in prov/5X8NA5.jsonl.

"""Leader election on a tree by saturation.

Messages: ("W",) wakes a process, ("M", x) carries the largest id of a
subtree towards the parent, ("L", x) tells the leader's id outwards from the
two saturated processes. The network is asynchronous and not FIFO: the
scheduler delivers any message in transit, chosen by a seeded generator, or
all of them in lock step when sync is true (every message takes one time
unit).
"""

import random


class Proc:
    def __init__(self, ident: int, nbrs: list[int]) -> None:
        self.id = ident
        self.nbrs = nbrs
        self.state = "asleep"
        self.best = ident
        self.heard: set[int] = set()
        self.parent = None
        self.leader = None

    def wake(self, sender, out: list, wakeup: bool) -> None:  # @line L1
        self.state = "awake"
        self.self_started = sender is None
        if wakeup:
            for q in self.nbrs:
                if q != sender:
                    out.append((q, ("W",)))
        if len(self.nbrs) == 1:  # @line L2
            self.send_m(out)
        elif not self.nbrs:
            self.state = "saturated"
            self.leader = self.id

    def send_m(self, out: list) -> None:
        rest = [q for q in self.nbrs if q not in self.heard]
        self.parent = rest[0]
        out.append((self.parent, ("M", self.best)))
        self.state = "processing"

    def receive(self, me: int, sender: int, msg: tuple, out: list, wakeup: bool) -> None:
        if self.state == "asleep":
            self.wake(sender, out, wakeup)
        if msg[0] == "M":  # @line L3
            self.best = max(self.best, msg[1])
            self.heard.add(sender)
            if self.state == "awake" and len(self.nbrs) - len(self.heard) == 1:  # @line L4
                self.send_m(out)
            elif self.state == "processing":  # @line L5
                assert sender == self.parent
                self.state = "saturated"
                self.leader = self.best
                for q in self.nbrs:
                    if q != self.parent:
                        out.append((q, ("L", self.best)))
        elif msg[0] == "L":  # @line L6
            self.leader = msg[1]
            for q in self.nbrs:
                if q != sender:
                    out.append((q, ("L", msg[1])))


def tree_election(adj: list[list[int]], ids: list[int], initiators: list[int] | None = None,
                  seed: int = 0, sync: bool = False, wakeup: bool = True) -> dict:
    """Run one election. Without wake-up, every process starts at time 0."""
    n = len(adj)
    rng = random.Random(seed)
    procs = [Proc(ids[v], adj[v]) for v in range(n)]
    if not wakeup:
        initiators = list(range(n))
    elif initiators is None:
        initiators = [rng.randrange(n)]
    transit: list[tuple] = []  # (src, dst, msg)
    counts = {"W": 0, "M": 0, "L": 0}
    time = 0

    def emit(src: int, out: list) -> None:
        for dst, msg in out:
            transit.append((src, dst, msg))
            counts[msg[0]] += 1

    if sync:
        for v in initiators:
            out: list = []
            procs[v].wake(None, out, wakeup)
            emit(v, out)
        while transit:
            time += 1
            batch, transit[:] = list(transit), []
            for src, dst, msg in batch:
                out = []
                procs[dst].receive(dst, src, msg, out, wakeup)
                emit(dst, out)
    else:
        pending = list(initiators)
        while transit or pending:
            k = rng.randrange(len(transit) + len(pending))
            if k < len(pending):
                v = pending.pop(k)
                if procs[v].state == "asleep":
                    out = []
                    procs[v].wake(None, out, wakeup)
                    emit(v, out)
                continue
            src, dst, msg = transit.pop(k - len(pending))
            out = []
            procs[dst].receive(dst, src, msg, out, wakeup)
            emit(dst, out)
    # A process counts as a starter if it woke up on its own, not by a message.
    starters = sum(1 for p in procs if p.self_started)
    return {
        "leaders": [v for v in range(n) if procs[v].leader == ids[v]],  # @line L7
        "known": [p.leader for p in procs],
        "saturated": [v for v in range(n) if procs[v].state == "saturated"],
        "counts": counts,
        "messages": sum(counts.values()),
        "time": time,
        "starters": starters,
    }


def random_tree(n: int, rng: random.Random) -> list[list[int]]:
    """A random labelled tree: vertex v > 0 joins a random earlier vertex."""
    adj: list[list[int]] = [[] for _ in range(n)]
    order = list(range(n))
    rng.shuffle(order)
    for k in range(1, n):
        u, v = order[k], order[rng.randrange(k)]
        adj[u].append(v)
        adj[v].append(u)
    for lst in adj:
        rng.shuffle(lst)
    return adj


def diameter(adj: list[list[int]]) -> int:
    def far(s: int) -> tuple[int, int]:
        dist = {s: 0}
        stack = [s]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w not in dist:
                    dist[w] = dist[u] + 1
                    stack.append(w)
        v = max(dist, key=dist.get)
        return v, dist[v]

    a, _ = far(0)
    return far(a)[1]
