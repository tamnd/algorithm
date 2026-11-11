# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convergecast/. The authors are listed in prov/T9HDCH.jsonl.

"""Convergecast on a rooted spanning tree, and the broadcast-convergecast pair (PIF).

The tree is given by a parent array (parent[root] == root). Each node holds a
value x[v]. Every node combines its own value with the values of its
children by an associative and commutative operation and sends the result
to its parent, after all its children have reported. The root outputs the
combination of all values. The run sends exactly n - 1 messages and takes
as many rounds as the height of the tree.
Cost of the simulation: O(n log n) time.
"""

import heapq
import random
from typing import Callable

Op = Callable[[int, int], int]


class CastNode:
    """Local state: accumulator and the number of children still to report."""

    def __init__(self, v: int, is_root: bool, parent: int, n_children: int, x: int, op: Op) -> None:
        self.v = v
        self.is_root = is_root
        self.parent = parent
        self.waiting = n_children
        self.acc = x
        self.op = op
        self.output: int | None = None

    def start(self) -> list[tuple[int, int]]:  # @line L1
        if self.waiting == 0:
            return self.finish()
        return []

    def receive(self, y: int) -> list[tuple[int, int]]:  # @line L2
        self.acc = self.op(self.acc, y)
        self.waiting -= 1
        if self.waiting == 0:  # @line L3
            return self.finish()
        return []

    def finish(self) -> list[tuple[int, int]]:  # @line L4
        if self.is_root:
            self.output = self.acc
            return []
        return [(self.parent, self.acc)]  # @line L5


def _nodes(parent: list[int], x: list[int], op: Op) -> tuple[list[CastNode], int]:
    n = len(parent)
    root = next(v for v in range(n) if parent[v] == v)
    kids = [0] * n
    for v in range(n):
        if v != root:
            kids[parent[v]] += 1
    return [CastNode(v, v == root, parent[v], kids[v], x[v], op) for v in range(n)], root


def convergecast_sync(parent: list[int], x: list[int], op: Op) -> dict:
    """Synchronous run. Values sent in round r arrive in round r."""
    nodes, root = _nodes(parent, x, op)
    outbox = []
    for nd in nodes:
        outbox += [(nd.v, w, y) for w, y in nd.start()]
    messages, rnd = 0, 0
    while outbox:
        rnd += 1
        messages += len(outbox)
        nxt = []
        for src, dst, y in outbox:
            nxt += [(dst, w, z) for w, z in nodes[dst].receive(y)]
        outbox = nxt
    return {"result": nodes[root].output, "messages": messages, "rounds": rnd}


def convergecast_async(parent: list[int], x: list[int], op: Op, seed: int = 0) -> dict:
    """Asynchronous run with seeded delays in (0, 1]."""
    rng = random.Random(seed)
    nodes, root = _nodes(parent, x, op)
    queue: list[tuple[float, int, int, int]] = []
    seq, messages, now = 0, 0, 0.0
    pending = [(nd.v, out) for nd in nodes for out in nd.start()]
    while True:
        for src, (dst, y) in pending:
            seq += 1
            messages += 1
            heapq.heappush(queue, (now + rng.uniform(0.01, 1.0), seq, dst, y))
        if not queue:
            break
        now, _, dst, y = heapq.heappop(queue)
        pending = [(dst, out) for out in nodes[dst].receive(y)]
    return {"result": nodes[root].output, "messages": messages, "time": now}


def pif_sync(parent: list[int], x: list[int], op: Op) -> dict:
    """Broadcast down the tree, then convergecast up (Segall's PIF on a known tree).

    In the broadcast phase a node starts its convergecast part when the
    broadcast reaches it, so a leaf at depth d reports in round d + 1.
    """
    n = len(parent)
    nodes, root = _nodes(parent, x, op)
    children: list[list[int]] = [[] for _ in range(n)]
    for v in range(n):
        if v != root:
            children[parent[v]].append(v)
    messages, rnd = 0, 0
    outbox: list[tuple[int, int, str, int]] = [(root, c, "B", 0) for c in children[root]]
    if not children[root]:
        nodes[root].start()  # a single node outputs its own value
    while outbox:
        rnd += 1
        messages += len(outbox)
        nxt: list[tuple[int, int, str, int]] = []
        for src, dst, kind, y in outbox:
            if kind == "B":
                nxt += [(dst, c, "B", 0) for c in children[dst]]
                outs = nodes[dst].start()
            else:
                outs = nodes[dst].receive(y)
            nxt += [(dst, w, "C", z) for w, z in outs]
        outbox = nxt
    return {"result": nodes[root].output, "messages": messages, "rounds": rnd}


def tree_height(parent: list[int]) -> int:
    n = len(parent)
    best = 0
    for v in range(n):
        d, x = 0, v
        while parent[x] != x:
            x = parent[x]
            d += 1
        best = max(best, d)
    return best
