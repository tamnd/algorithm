# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wait-for-graph/. The authors are listed in prov/T6DVQD.jsonl.

"""A wait-for graph with an incremental cycle check, and the probe method.

An edge p -> q means that process p waits for process q (q holds a lock
that p asked for). The graph keeps successor and predecessor sets so that
a process can be removed in time proportional to its degree.
"""

import random
from typing import Hashable, Optional

P = Hashable


class WaitForGraph:
    def __init__(self) -> None:
        self.succ: dict[P, set[P]] = {}  # @line L1
        self.pred: dict[P, set[P]] = {}

    def _node(self, p: P) -> None:
        self.succ.setdefault(p, set())
        self.pred.setdefault(p, set())

    def add_wait(self, p: P, q: P) -> Optional[list[P]]:
        """Add p -> q. Return a cycle p, q, ..., (back to p) if the edge closes one.

        Precondition: p != q. If the graph had no cycle before, the returned
        cycle is the only kind of cycle after. Cost: O(n + e) for the search.
        """
        self._node(p)
        self._node(q)
        self.succ[p].add(q)  # @line L2
        self.pred[q].add(p)
        path = self._path(q, p)  # @line L3
        if path is not None:  # @line L4
            return [p] + path[:-1]
        return None  # @line L5

    def _path(self, s: P, t: P) -> Optional[list[P]]:
        """A path from s to t, by iterative depth-first search, or None."""
        parent: dict[P, Optional[P]] = {s: None}
        stack = [s]
        while stack:
            v = stack.pop()
            if v == t:
                out = [v]
                while parent[out[-1]] is not None:
                    out.append(parent[out[-1]])
                return out[::-1]
            for w in self.succ.get(v, ()):
                if w not in parent:
                    parent[w] = v
                    stack.append(w)
        return None

    def remove_wait(self, p: P, q: P) -> None:
        """p got what it waited for from q. Cost: O(1)."""
        self.succ[p].discard(q)  # @line L6
        self.pred[q].discard(p)

    def remove_process(self, p: P) -> None:
        """p finished or was aborted. Cost: O(deg p)."""
        for q in self.succ.pop(p, set()):  # @line L7
            self.pred[q].discard(p)
        for x in self.pred.pop(p, set()):
            self.succ[x].discard(p)

    def edges(self) -> set[tuple]:
        return {(p, q) for p, qs in self.succ.items() for q in qs}

    def deadlocked(self) -> set[P]:
        """The processes that can reach a cycle (single unit resources). Cost: O(n + e)."""
        out = {v: len(ws) for v, ws in self.succ.items()}
        stack = [v for v, d in out.items() if d == 0]
        gone = set(stack)
        while stack:
            w = stack.pop()
            for v in self.pred.get(w, ()):
                out[v] -= 1
                if out[v] == 0:
                    gone.add(v)
                    stack.append(v)
        return set(out) - gone


def probe(succ: dict[P, set[P]], initiator: P, seed: int) -> tuple[bool, int]:
    """Edge chasing in the style of Chandy, Misra and Haas, on a fixed graph.

    The initiator sends probe (i, i, k) to each k it waits for. A blocked
    process k that gets a probe of initiator i for the first time forwards
    (i, k, l) to every l it waits for. The initiator declares a deadlock when
    a probe of its own comes back. Messages are delivered in a random order
    given by the seed. Returns (deadlock declared, messages sent).
    Precondition: the graph does not change during the run (a deadlock is
    stable, so a cycle stays). Cost: at most one message per edge.
    """
    rng = random.Random(seed)
    in_transit = [(initiator, initiator, k) for k in sorted(succ.get(initiator, ()), key=repr)]
    sent = len(in_transit)
    seen: set[P] = set()
    found = False
    while in_transit:
        i, j, k = in_transit.pop(rng.randrange(len(in_transit)))
        if k == i:
            found = True
            continue
        if k in seen or not succ.get(k):
            continue  # already forwarded, or k is not blocked
        seen.add(k)
        for l in sorted(succ[k], key=repr):
            in_transit.append((i, k, l))
            sent += 1
    return found, sent
