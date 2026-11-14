# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flowmap/. The authors are listed in prov/R5X3KJ.jsonl.

"""FlowMap of Cong and Ding: depth-optimal mapping into k-input LUTs.

The network is a list `fanins` in topological order: every fanin of v is
smaller than v, a node with no fanins is a primary input, and every node
has at most k fanins (the network is k-bounded). `outputs` lists the
nodes that drive primary outputs.

Phase 1 gives each node t a label, the least depth of a LUT mapping of
t. Let p be the largest label of a fanin of t. The label is p when the
cone of t, with t and every node of label p merged into one sink, has a
node cut of at most k nodes between the inputs and the sink; else it is
p + 1. The node cut is found with unit node capacities and augmenting
paths, stopping after k + 1 paths.

Phase 2 builds the LUTs from the outputs down: the LUT of t has the
nodes of its cut as inputs.
"""

from collections import deque
from typing import Sequence

INF = 1 << 30


def cone(fanins: Sequence[Sequence[int]], t: int) -> list:
    """The nodes from which t can be reached, t included, in increasing order."""
    seen, stack = {t}, [t]
    while stack:
        w = stack.pop()
        for u in fanins[w]:
            if u not in seen:
                seen.add(u)
                stack.append(u)
    return sorted(seen)


class FlowNet:
    """A directed graph with integer capacities for augmenting paths."""

    def __init__(self) -> None:
        self.to: list = []
        self.cap: list = []
        self.adj: dict = {}

    def add(self, a, b, c: int) -> None:
        for x in (a, b):
            self.adj.setdefault(x, [])
        self.adj[a].append(len(self.to))
        self.to.append(b)
        self.cap.append(c)
        self.adj[b].append(len(self.to))
        self.to.append(a)
        self.cap.append(0)

    def augment(self, s, t) -> bool:
        """Push one unit along a shortest path with free capacity."""
        prev = {s: None}
        q = deque([s])
        while q and t not in prev:
            x = q.popleft()
            for e in self.adj[x]:
                y = self.to[e]
                if self.cap[e] > 0 and y not in prev:
                    prev[y] = e
                    q.append(y)
        if t not in prev:
            return False
        y = t
        while prev[y] is not None:
            e = prev[y]
            self.cap[e] -= 1
            self.cap[e ^ 1] += 1
            y = self.to[e ^ 1]
        return True

    def reachable(self, s) -> set:
        seen, stack = {s}, [s]
        while stack:
            x = stack.pop()
            for e in self.adj[x]:
                y = self.to[e]
                if self.cap[e] > 0 and y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen


def min_height_cut(fanins, label, t: int, k: int):
    """Return (label of t, the cut of t) as in phase 1 of FlowMap."""
    p = max(label[u] for u in fanins[t])  # @line L3
    if p == 0:  # @line L4
        return 1, frozenset(fanins[t])
    nodes = cone(fanins, t)
    sink = ("sink",)
    merged = {w for w in nodes if w == t or label[w] == p}  # @line L5
    net = FlowNet()  # @line L6
    src = ("src",)

    def head(w):  # where the edges into w arrive
        return sink if w in merged else ("in", w)

    for w in nodes:
        if w in merged:
            continue
        net.add(("in", w), ("out", w), 1)  # each node may be cut once
        if not fanins[w]:
            net.add(src, ("in", w), INF)
    for w in nodes:
        for u in fanins[w]:
            if u not in merged:  # edges out of the sink are not needed
                net.add(("out", u), head(w), INF)
    flow = 0
    while flow <= k and net.augment(src, sink):  # @line L7
        flow += 1
    if flow > k:  # @line L9
        return p + 1, frozenset(fanins[t])  # @line L10
    side = net.reachable(src)  # @line L8
    cut = frozenset(w for w in nodes if w not in merged
                    and ("in", w) in side and ("out", w) not in side)
    return p, cut


def flowmap(fanins: Sequence[Sequence[int]], outputs: Sequence[int], k: int):
    """Return (labels, luts): luts maps each LUT root to its input nodes."""
    for v, fi in enumerate(fanins):
        if len(fi) > k:
            raise ValueError("the network is not k-bounded")
        if any(u >= v for u in fi):
            raise ValueError("fanins must come before the node")
    label = [0] * len(fanins)  # @line L1
    cut: list = [None] * len(fanins)
    for t, fi in enumerate(fanins):  # @line L2
        if fi:
            label[t], cut[t] = min_height_cut(fanins, label, t, k)
    luts: dict = {}
    todo = [v for v in outputs if fanins[v]]  # @line L11
    while todo:  # @line L12
        v = todo.pop()
        if v in luts:
            continue
        luts[v] = cut[v]  # @line L13
        todo.extend(u for u in cut[v] if fanins[u] and u not in luts)
    return label, luts  # @line L14


def lut_depth(fanins, luts, outputs) -> int:
    """Depth of the LUT network: the most LUTs on a path from an input to an output."""
    memo: dict = {}

    def d(v):
        if not fanins[v]:
            return 0
        if v not in memo:
            memo[v] = 1 + max((d(u) for u in luts[v]), default=0)
        return memo[v]

    return max((d(v) for v in outputs), default=0)
