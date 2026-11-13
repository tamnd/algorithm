# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplified-memory-bounded-a-star/. The authors are listed in prov/S5JTNJ.jsonl.

"""SMA*, simplified memory-bounded A* (Russell 1992), as a tree search.

At most `memory` nodes are in memory at a time. Each step takes the node of
least f (ties: deepest, then newest) among the nodes that are goals or have
a successor that is not in memory, and makes one more successor of it:
the next one never made, or else the forgotten one of least stored value.
When memory is full, the code first deletes the leaf of highest f (ties:
shallowest, then oldest), and its parent keeps its f as the value of the
forgotten slot. When every successor of a node has been made at least once,
its f becomes the least value over its slots, and the change goes up the
tree. A non-goal node at depth memory - 1, or with no successor, gets
f = infinity: no solution path through it fits in memory.

This page's version keeps one stored value for each forgotten slot. A
successor that is already on the path to its parent is not made, so the tree
is finite on a finite graph. max_steps guards the loop in tests.
"""

import itertools
from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
INF = float("inf")


class _Node:
    __slots__ = ("state", "g", "depth", "f", "parent", "index", "succ", "slots", "born")

    def __init__(self, state, g, depth, parent, index, born):
        self.state, self.g, self.depth = state, g, depth
        self.parent, self.index, self.born = parent, index, born
        self.f: Number = 0
        self.succ: list = []
        self.slots: list = []  # None: never made; _Node: in memory; number: forgotten


@dataclass
class SearchResult:
    path: Optional[list]  # states from the start to a goal, or None
    cost: Optional[Number]  # cost of that path, or None
    steps: int = 0  # successors made, line L6
    deletions: int = 0  # nodes deleted to free memory, line L10
    peak: int = 0  # most nodes in memory at one time


def sma_star(
    start: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, Number]]],
    is_goal: Callable[[Hashable], bool],
    h: Callable[[Hashable], Number],
    memory: int,
    max_steps: int = 10**6,
) -> SearchResult:
    """Search with at most `memory` nodes; see the page for what is proved.

    Precondition: memory >= 2, positive costs, a finite graph, admissible h.
    If the search returns a path, its cost is the least cost of a solution
    with at most memory - 1 actions; failure means that no such solution
    exists. Cost: O(memory) nodes, each with O(b) slots.
    """
    if memory < 2:
        raise ValueError("memory must be at least 2")
    res = SearchResult(None, None)
    born = itertools.count()

    def is_node(s):
        return isinstance(s, _Node)

    def on_path(x):
        out = set()
        while x is not None:
            out.add(x.state)
            x = x.parent
        return out

    def make(state, g, parent, index, floor):
        depth = 0 if parent is None else parent.depth + 1
        x = _Node(state, g, depth, parent, index, next(born))
        if not is_goal(state):
            seen = on_path(x)
            x.succ = [(m, c) for m, c in successors(state) if m not in seen]
            x.slots = [None] * len(x.succ)
        if not is_goal(state) and (x.depth >= memory - 1 or not x.succ):  # @line L7
            x.f = INF
        else:
            x.f = max(floor, g + h(state))
        return x

    def backup(x):  # @line L12
        while x is not None and all(s is not None for s in x.slots):
            low = min((s.f if is_node(s) else s for s in x.slots), default=INF)
            if low <= x.f:
                return
            x.f = low
            x = x.parent

    root = make(start, 0, None, None, 0)  # @line L1
    live = [root]
    while res.steps <= max_steps:  # @line L2
        queue = [x for x in live if is_goal(x.state) or not all(map(is_node, x.slots))]
        if not queue:
            return res
        n = min(queue, key=lambda x: (x.f, -x.depth, -x.born))  # @line L3
        if n.f == INF:  # @line L4
            return res
        if is_goal(n.state):  # @line L5
            p, x = [], n
            while x is not None:
                p.append(x.state)
                x = x.parent
            res.path, res.cost = p[::-1], n.g
            return res
        if None in n.slots:  # @line L6
            i = n.slots.index(None)
            floor = n.f
        else:
            gone = [j for j, s in enumerate(n.slots) if not is_node(s)]
            i = min(gone, key=lambda j: n.slots[j])
            floor = max(n.f, n.slots[i])
        res.steps += 1
        if len(live) >= memory:  # @line L8
            leaves = [x for x in live
                      if x is not root and x is not n and not any(map(is_node, x.slots))]
            z = max(leaves, key=lambda x: (x.f, -x.depth, -x.born))  # @line L9
            z.parent.slots[z.index] = z.f  # @line L10
            live.remove(z)
            res.deletions += 1
        m, c = n.succ[i]
        s = make(m, n.g + c, n, i, floor)
        n.slots[i] = s  # @line L11
        live.append(s)
        res.peak = max(res.peak, len(live))
        backup(n)
    raise RuntimeError("step limit reached")
