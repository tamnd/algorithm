# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epidemic-broadcast-tree/. The authors are listed in prov/HVTE8H.jsonl.

"""Plumtree, the epidemic broadcast tree (Leitao, Pereira and Rodrigues, SRDS 2007).

Every node splits its overlay neighbours into eager peers, which get the full
payload (GOSSIP), and lazy peers, which get only an announcement (IHAVE). A
duplicate GOSSIP moves its sender to the lazy set and is answered with PRUNE.
A node that hears IHAVE for a message it lacks starts a timer; if the message
has not come when the timer fires, it sends GRAFT to the announcer, which
moves the link back to the eager set and sends the payload.

The simulator is deterministic and seeded. The overlay is static. Every
message takes one time step. A failed link drops everything sent over it,
and the membership layer reports the failure to both ends (NeighborDown).
"""

import random
from collections import defaultdict

GOSSIP, IHAVE, PRUNE, GRAFT = "GOSSIP", "IHAVE", "PRUNE", "GRAFT"
Msg = tuple[int, int, str, int, int]  # (src, dst, type, message id, round)


class PlumtreeNode:
    def __init__(self, ident: int, neighbours: list[int], timeout1: int = 3, timeout2: int = 1) -> None:
        self.id = ident
        self.eager = set(neighbours)
        self.lazy: set[int] = set()
        self.received: dict[int, int] = {}  # message id -> hops when delivered
        self.missing: list[tuple[int, int, int]] = []  # (message id, announcer, round)
        self.timers: dict[int, int] = {}  # message id -> time the timer fires
        self.timeout1, self.timeout2 = timeout1, timeout2

    def _push(self, mid: int, rnd: int, skip: int) -> list[Msg]:
        out = [(self.id, p, GOSSIP, mid, rnd) for p in sorted(self.eager) if p != skip]
        out += [(self.id, p, IHAVE, mid, rnd) for p in sorted(self.lazy) if p != skip]
        return out

    def broadcast(self, mid: int) -> list[Msg]:
        self.received[mid] = 0
        return self._push(mid, 1, self.id)  # @line L1

    def on_message(self, src: int, kind: str, mid: int, rnd: int, now: int) -> list[Msg]:
        if kind == GOSSIP:
            if mid not in self.received:
                self.received[mid] = rnd
                self.timers.pop(mid, None)
                self.missing = [m for m in self.missing if m[0] != mid]
                out = self._push(mid, rnd + 1, src)  # @line L2
                self.lazy.discard(src)
                self.eager.add(src)
                return out
            self.eager.discard(src)
            self.lazy.add(src)
            return [(self.id, src, PRUNE, mid, 0)]  # @line L3
        if kind == PRUNE:
            self.eager.discard(src)
            self.lazy.add(src)  # @line L4
            return []
        if kind == IHAVE:
            if mid not in self.received:
                if mid not in self.timers:
                    self.timers[mid] = now + self.timeout1  # @line L5
                self.missing.append((mid, src, rnd))
            return []
        if kind == GRAFT:
            self.lazy.discard(src)
            self.eager.add(src)
            if mid in self.received:
                return [(self.id, src, GOSSIP, mid, self.received[mid] + 1)]  # @line L7
            return []
        raise ValueError(kind)

    def on_timer(self, mid: int, now: int) -> list[Msg]:
        if mid in self.received:
            return []
        for i, (m, node, rnd) in enumerate(self.missing):
            if m == mid:
                del self.missing[i]
                self.timers[mid] = now + self.timeout2
                self.lazy.discard(node)
                self.eager.add(node)
                return [(self.id, node, GRAFT, mid, rnd)]  # @line L6
        del self.timers[mid]
        return []

    def neighbour_down(self, node: int) -> None:
        self.eager.discard(node)
        self.lazy.discard(node)
        self.missing = [m for m in self.missing if m[1] != node]  # @line L8


class Network:
    """Lock-step network. Messages sent at time t arrive at time t + 1."""

    def __init__(self, adj: list[list[int]], rng: random.Random, timeout1: int = 3, timeout2: int = 1) -> None:
        self.nodes = [PlumtreeNode(i, adj[i], timeout1, timeout2) for i in range(len(adj))]
        self.rng = rng
        self.dead: set[frozenset[int]] = set()
        self.now = 0
        self.counts: dict[str, int] = defaultdict(int)

    def fail_link(self, u: int, v: int) -> None:
        self.dead.add(frozenset((u, v)))
        self.nodes[u].neighbour_down(v)
        self.nodes[v].neighbour_down(u)

    def broadcast(self, source: int, mid: int, max_steps: int = 500) -> dict[str, int]:
        """Broadcast one message and run until the network is quiet."""
        self.counts = defaultdict(int)
        queue = self.nodes[source].broadcast(mid)
        for _ in range(max_steps):
            self.now += 1
            for m in queue:
                self.counts[m[2]] += 1
            arriving = [m for m in queue if frozenset((m[0], m[1])) not in self.dead]
            self.rng.shuffle(arriving)
            queue = []
            for src, dst, kind, m, rnd in arriving:
                if kind == GOSSIP:
                    self.counts["payload received"] += 1
                queue += self.nodes[dst].on_message(src, kind, m, rnd, self.now)
            for node in self.nodes:
                for m, t in sorted(node.timers.items()):
                    if t <= self.now:
                        queue += node.on_timer(m, self.now)
            if not queue and not any(node.timers for node in self.nodes):
                break
        got = [nd.received[mid] for nd in self.nodes if mid in nd.received]
        self.counts["delivered"] = len(got)
        self.counts["ldh"] = max(got)
        return dict(self.counts)

    def tree_edges(self) -> set[frozenset[int]]:
        """Links that both ends hold as eager."""
        return {frozenset((u.id, v)) for u in self.nodes for v in u.eager if u.id in self.nodes[v].eager}

    def one_sided_eager(self) -> int:
        return sum(1 for u in self.nodes for v in u.eager if u.id not in self.nodes[v].eager)


def random_overlay(n: int, cycles: int, rng: random.Random) -> list[list[int]]:
    """The union of random Hamiltonian cycles, without repeated links."""
    nbrs: list[set[int]] = [set() for _ in range(n)]
    for _ in range(cycles):
        order = list(range(n))
        rng.shuffle(order)
        for i in range(n):
            u, v = order[i], order[(i + 1) % n]
            nbrs[u].add(v)
            nbrs[v].add(u)
    return [sorted(s) for s in nbrs]


def is_tree(n: int, edges: set[frozenset[int]]) -> bool:
    if len(edges) != n - 1:
        return False
    adj: dict[int, list[int]] = defaultdict(list)
    for e in edges:
        u, v = tuple(e)
        adj[u].append(v)
        adj[v].append(u)
    seen, stack = {0}, [0]
    while stack:
        for v in adj[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n
