# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-mst/. The authors are listed in prov/59V4HH.jsonl.

"""A Borůvka-style MST in the CONGEST model (SynchGHS with fixed phases).

The network runs in lock-step rounds. In each round every node sends at most
one message on each incident edge, then every node receives, then every node
computes. Each message must fit in a budget of B = 8 ceil(log2(n + 1)) + 16
bits, which is O(log n) when the weights are at most n^3.

The nodes know n. The algorithm has ceil(log2 n) phases of 3n + 2 rounds.
In a phase each fragment:
  1. tells all neighbours its fragment id (1 round),
  2. finds its minimum outgoing edge (MOE) by a convergecast to its root
     (n rounds),
  3. broadcasts the MOE weight from the root (n rounds),
  4. sends Connect over the MOE (1 round),
  5. lets the larger end of each core edge flood its id as the new fragment
     id over the new tree (n rounds).
Each fragment merges with at least one other in each phase, so after
ceil(log2 n) phases one fragment is left.
"""

import math
import random

INF = math.inf


def message_bits(msg: tuple) -> int:
    """Bits of an encoded message: a 4-bit tag, then 2 + the binary length of
    each integer field (2 bits for infinity)."""
    bits = 4
    for x in msg[1:]:
        bits += 2 if x == INF else 2 + max(1, int(x).bit_length())
    return bits


def budget(n: int) -> int:
    return 8 * math.ceil(math.log2(n + 1)) + 16


class Node:
    def __init__(self, uid: int, n: int, w: dict[int, int]) -> None:
        self.uid, self.n, self.w = uid, n, w  # w: neighbour -> edge weight
        self.frag = uid
        self.parent: int | None = None
        self.tree: set[int] = set()  # tree neighbours
        self.children: set[int] = set()
        self.nbr_frag: dict[int, int] = {}
        self.best = INF  # the lightest outgoing edge known in my subtree
        self.waiting: set[int] = set()
        self.sent_up = False
        self.moe = INF  # the MOE of my fragment, after the broadcast
        self.forward_moe = False
        self.connect_on: int | None = None
        self.new_lead: int | None = None
        self.forward_lead = False

    def send(self, t: int) -> list[tuple[int, tuple]]:
        """Messages for offset t of the phase."""
        n, out = self.n, []
        if t == 0:
            out = [(j, ("id", self.frag)) for j in self.w]
        elif 1 <= t <= n:  # convergecast of the minimum
            if not self.waiting and not self.sent_up and self.parent is not None:
                out = [(self.parent, ("best", self.best))]
                self.sent_up = True
        elif n + 1 <= t <= 2 * n:  # broadcast of the MOE weight
            if t == n + 1 and self.parent is None:
                self.moe, self.forward_moe = self.best, True
            if self.forward_moe:
                out = [(c, ("moe", self.moe)) for c in self.children]
                self.forward_moe = False
        elif t == 2 * n + 1:  # Connect on the MOE
            for j, wt in self.w.items():
                if wt == self.moe and self.nbr_frag[j] != self.frag:
                    self.connect_on = j
                    self.tree.add(j)
                    out = [(j, ("connect",))]
        else:  # flood the id of the new root
            if t == 2 * n + 2 and self.new_lead == self.uid:
                self.frag, self.parent = self.uid, None
                self.children = set(self.tree)
                self.forward_lead = True
            if self.forward_lead:
                out = [(c, ("lead", self.frag)) for c in self.children]
                self.forward_lead = False
        return out

    def receive(self, t: int, inbox: list[tuple[int, tuple]]) -> None:
        n = self.n
        for j, msg in inbox:
            kind = msg[0]
            if kind == "id":
                self.nbr_frag[j] = msg[1]
            elif kind == "best":
                self.waiting.discard(j)
                self.best = min(self.best, msg[1])
            elif kind == "moe":
                self.moe, self.forward_moe = msg[1], True
            elif kind == "connect":
                self.tree.add(j)
                if self.connect_on == j:  # both ends chose j: j is a core
                    self.new_lead = max(self.uid, j)
            elif kind == "lead":  # the new tree is a tree, so this comes once
                self.frag, self.parent = msg[1], j
                self.children = self.tree - {j}
                self.forward_lead = True
        if t == 0:  # start of the phase: local minimum, then wait for children
            out = [wt for j, wt in self.w.items() if self.nbr_frag[j] != self.frag]
            self.best = min(out, default=INF)
            self.waiting = set(self.children)
            self.sent_up = False
            self.moe, self.connect_on, self.new_lead = INF, None, None


def distributed_mst(n: int, edges: list[tuple[int, int, int]]) -> dict:
    """Run the algorithm. edges holds (u, v, weight) with distinct weights and
    the graph is connected. Returns the MST weights, the rounds, the messages,
    the largest message in bits and the number of fragments after each phase."""
    adj: list[dict[int, int]] = [dict() for _ in range(n)]
    for u, v, w in edges:
        adj[u][v] = w
        adj[v][u] = w
    nodes = [Node(u, n, adj[u]) for u in range(n)]
    phases = math.ceil(math.log2(n)) if n > 1 else 0
    length = 3 * n + 2
    B = budget(n)
    stats = {"rounds": 0, "messages": 0, "max_bits": 0, "fragments": []}
    for p in range(phases):
        for t in range(length):
            inbox: list[list[tuple[int, tuple]]] = [[] for _ in range(n)]
            for u in range(n):
                used = set()
                for v, msg in nodes[u].send(t):
                    assert v not in used, "two messages on one edge in one round"
                    used.add(v)
                    bits = message_bits(msg)
                    assert bits <= B, "message over the CONGEST budget"
                    stats["max_bits"] = max(stats["max_bits"], bits)
                    stats["messages"] += 1
                    inbox[v].append((u, msg))
            for u in range(n):
                nodes[u].receive(t, inbox[u])
            stats["rounds"] += 1
        stats["fragments"].append(len({x.frag for x in nodes}))
    mst = {adj[u][j] for u in range(n) for j in nodes[u].tree}
    stats["mst"] = mst
    return stats


def kruskal(n: int, edges: list[tuple[int, int, int]]) -> set[int]:
    """The MST weights by Kruskal with union-find (the oracle)."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = set()
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            out.add(w)
    return out


def random_connected_graph(n: int, extra: int, rng: random.Random) -> list[tuple[int, int, int]]:
    """A random tree plus extra edges, with distinct weights from 1 to n^3."""
    pairs = {(rng.randrange(v), v) for v in range(1, n)}
    others = [(u, v) for u in range(n) for v in range(u + 1, n) if (u, v) not in pairs]
    rng.shuffle(others)
    pairs |= set(others[:extra])
    weights = rng.sample(range(1, max(n**3, len(pairs)) + 1), len(pairs))
    return [(u, v, w) for (u, v), w in zip(sorted(pairs), weights)]
