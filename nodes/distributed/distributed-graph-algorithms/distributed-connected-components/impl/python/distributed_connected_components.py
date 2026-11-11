# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-connected-components/. The authors are listed in prov/BCTDPX.jsonl.

"""Connected components when the network is the input graph.

Two synchronous CONGEST algorithms on an undirected graph H that need not be
connected. Messages travel only over the edges of H.

label_propagation: each node keeps the smallest identifier it has heard of
and sends its label to all neighbours when it changes. A node has its final
label after d(v, min of its component) rounds.

boruvka_components: Borůvka-style merging (SynchGHS with fixed phases). Each
fragment finds its lightest outgoing edge by a convergecast, the fragments
merge along these edges, and the new root floods its identifier. The edge
weights u*n + v + 1 (u < v) are distinct, so the merging never closes a cycle.
After ceil(log2 n) phases of 3n + 2 rounds each fragment is a component.
"""

import math

INF = math.inf


def message_bits(msg: tuple) -> int:
    """A 4-bit tag, then 2 + the binary length of each integer field."""
    bits = 4
    for x in msg[1:]:
        bits += 2 if x == INF else 2 + max(1, int(x).bit_length())
    return bits


def budget(n: int) -> int:
    return 8 * math.ceil(math.log2(n + 1)) + 16


def label_propagation(n: int, edges: list[tuple[int, int]]) -> dict:
    """Return the labels, the round of the last change, the rounds that are
    run (n - 1, the bound that the nodes know) and the messages."""
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    label = list(range(n))
    changed = [True] * n  # round 1: every node sends its own label
    last, messages = 0, 0
    for r in range(1, n):
        inbox: list[list[int]] = [[] for _ in range(n)]
        for u in range(n):
            if changed[u]:
                for v in adj[u]:
                    inbox[v].append(label[u])
                    messages += 1
        changed = [False] * n
        for v in range(n):
            if inbox[v] and min(inbox[v]) < label[v]:
                label[v] = min(inbox[v])
                changed[v] = True
                last = r
    return {"labels": label, "last_change": last, "rounds": max(n - 1, 0), "messages": messages}


class Node:
    def __init__(self, uid: int, n: int, w: dict[int, int]) -> None:
        self.uid, self.n, self.w = uid, n, w  # w: neighbour -> edge weight
        self.frag = uid
        self.parent: int | None = None
        self.tree: set[int] = set()
        self.children: set[int] = set()
        self.nbr_frag: dict[int, int] = {}
        self.best = INF
        self.waiting: set[int] = set()
        self.sent_up = False
        self.moe = INF
        self.forward_moe = False
        self.connect_on: int | None = None
        self.new_lead: int | None = None
        self.forward_lead = False

    def send(self, t: int) -> list[tuple[int, tuple]]:
        n, out = self.n, []
        if t == 0:  # tell the neighbours my fragment
            out = [(j, ("id", self.frag)) for j in self.w]
        elif 1 <= t <= n:  # convergecast of the lightest outgoing edge
            if not self.waiting and not self.sent_up and self.parent is not None:
                out = [(self.parent, ("best", self.best))]
                self.sent_up = True
        elif n + 1 <= t <= 2 * n:  # broadcast of the choice
            if t == n + 1 and self.parent is None:
                self.moe, self.forward_moe = self.best, True
            if self.forward_moe:
                out = [(c, ("moe", self.moe)) for c in self.children]
                self.forward_moe = False
        elif t == 2 * n + 1:  # Connect over the chosen edge
            for j, wt in self.w.items():
                if wt == self.moe and self.nbr_frag[j] != self.frag:
                    self.connect_on = j
                    self.tree.add(j)
                    out = [(j, ("connect",))]
        else:  # the larger end of each core floods its id
            if t == 2 * n + 2 and self.new_lead == self.uid:
                self.frag, self.parent = self.uid, None
                self.children = set(self.tree)
                self.forward_lead = True
            if self.forward_lead:
                out = [(c, ("lead", self.frag)) for c in self.children]
                self.forward_lead = False
        return out

    def receive(self, t: int, inbox: list[tuple[int, tuple]]) -> None:
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
                if self.connect_on == j:  # both ends chose this edge: a core
                    self.new_lead = max(self.uid, j)
            elif kind == "lead":
                self.frag, self.parent = msg[1], j
                self.children = self.tree - {j}
                self.forward_lead = True
        if t == 0:
            out = [wt for j, wt in self.w.items() if self.nbr_frag[j] != self.frag]
            self.best = min(out, default=INF)
            self.waiting = set(self.children)
            self.sent_up = False
            self.moe, self.connect_on, self.new_lead = INF, None, None


def boruvka_components(n: int, edges: list[tuple[int, int]]) -> dict:
    """Return the fragment id of each node, the rounds, the messages, the
    largest message in bits and the number of fragments after each phase."""
    adj: list[dict[int, int]] = [dict() for _ in range(n)]
    for u, v in edges:
        a, b = min(u, v), max(u, v)
        adj[a][b] = adj[b][a] = a * n + b + 1
    nodes = [Node(u, n, adj[u]) for u in range(n)]
    phases = math.ceil(math.log2(n)) if n > 1 else 0
    B = budget(n)
    st = {"rounds": 0, "messages": 0, "max_bits": 0, "fragments": [n], "phase_messages": []}
    for _ in range(phases):
        before = st["messages"]
        for t in range(3 * n + 2):
            inbox: list[list[tuple[int, tuple]]] = [[] for _ in range(n)]
            for u in range(n):
                used = set()
                for v, msg in nodes[u].send(t):
                    assert v not in used, "two messages on one edge in one round"
                    used.add(v)
                    bits = message_bits(msg)
                    assert bits <= B, "message over the CONGEST budget"
                    st["max_bits"] = max(st["max_bits"], bits)
                    st["messages"] += 1
                    inbox[v].append((u, msg))
            for u in range(n):
                nodes[u].receive(t, inbox[u])
            st["rounds"] += 1
        st["phase_messages"].append(st["messages"] - before)
        st["fragments"].append(len({x.frag for x in nodes}))
    st["labels"] = [x.frag for x in nodes]
    return st


def union_find_labels(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """The oracle: the smallest node of each component, by union-find."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            parent[max(a, b)] = min(a, b)
    return [find(v) for v in range(n)]
