# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lifelong-planning-a-star/. The authors are listed in prov/X7W103.jsonl.

"""Lifelong Planning A* (Koenig, Likhachev and Furcy 2004).

The graph is finite and directed, with positive edge costs. A cost may be
math.inf, which means that the edge is blocked. The heuristic h estimates the
distance from a vertex to the goal and must be consistent for every version
of the costs: h(goal) = 0 and h(u) <= c(u, v) + h(v) for each edge.

Each vertex has g, the current estimate of its start distance, and rhs, the
one-step lookahead value. The queue holds exactly the vertices with g != rhs.
It is a binary heap with lazy deletion: the dict self.key holds the current
key of each queued vertex, and an entry whose key is not that one is skipped.
The basic version of the paper is used: UpdateVertex recomputes rhs as a
minimum over all predecessors.
"""

import heapq
import itertools
import math
from collections.abc import Callable, Hashable, Iterable, Iterator

INF = math.inf


class LPAStar:
    def __init__(self, succ: dict, start: Hashable, goal: Hashable, h: Callable[[Hashable], float]):
        """INITIALIZE. succ maps each vertex to a dict {successor: cost}. Every vertex must be a key."""
        self.succ = {u: dict(vs) for u, vs in succ.items()}
        self.pred = {u: {} for u in self.succ}
        for u, vs in self.succ.items():
            for v, c in vs.items():
                if v == u:
                    raise ValueError("self-loops are not allowed")
                if not c > 0:
                    raise ValueError("edge costs must be positive")
                self.pred[v][u] = c
        self.start, self.goal, self.h = start, goal, h
        self.key: dict = {}  # @line L2
        self.heap: list = []
        self.tie = itertools.count()
        self.g = {u: INF for u in self.succ}  # @line L3
        self.rhs = {u: INF for u in self.succ}
        self.rhs[start] = 0  # @line L4
        self._insert(start)  # @line L5
        self.calls: list[list[tuple]] = []  # per call: (vertex, "over" or "under", key)

    # -- the priority queue U -------------------------------------------------
    def calculate_key(self, s) -> tuple:
        m = min(self.g[s], self.rhs[s])
        return (m + self.h(s), m)  # @line L1

    def _insert(self, s) -> None:
        k = self.calculate_key(s)
        self.key[s] = k
        heapq.heappush(self.heap, (k, next(self.tie), s))

    def _clean(self) -> None:
        while self.heap and self.key.get(self.heap[0][2]) != self.heap[0][0]:
            heapq.heappop(self.heap)

    def top_key(self) -> tuple:
        self._clean()
        return self.heap[0][0] if self.heap else (INF, INF)

    def _pop(self):
        self._clean()
        _, _, u = heapq.heappop(self.heap)
        del self.key[u]
        return u

    # -- the algorithm ---------------------------------------------------------
    def update_vertex(self, u) -> None:
        if u != self.start:  # @line L6
            self.rhs[u] = min((self.g[p] + c for p, c in self.pred[u].items()), default=INF)
        self.key.pop(u, None)  # @line L7
        if self.g[u] != self.rhs[u]:  # @line L8
            self._insert(u)

    def compute_shortest_path(self) -> float:
        """Repair g until the goal is locally consistent and no queued key is smaller."""
        log: list[tuple] = []
        goal = self.goal
        while self.top_key() < self.calculate_key(goal) or self.rhs[goal] != self.g[goal]:  # @line L9
            k = self.top_key()
            u = self._pop()  # @line L10
            if self.g[u] > self.rhs[u]:  # @line L11
                log.append((u, "over", k))
                self.g[u] = self.rhs[u]  # @line L12
                for s in self.succ[u]:  # @line L13
                    self.update_vertex(s)
            else:  # @line L14
                log.append((u, "under", k))
                self.g[u] = INF  # @line L15
                for s in list(self.succ[u]) + [u]:  # @line L16
                    self.update_vertex(s)
        self.calls.append(log)
        return self.g[goal]

    def set_cost(self, u, v, c: float) -> None:
        """Change the cost of the existing edge u -> v and repair rhs(v)."""
        if not c > 0:
            raise ValueError("edge costs must be positive")
        self.succ[u][v] = c  # @line L22
        self.pred[v][u] = c
        self.update_vertex(v)  # @line L23

    def path(self) -> list | None:
        """Trace a shortest path back from the goal through minimizing predecessors."""
        if self.g[self.goal] == INF:
            return None
        out = [self.goal]
        s = self.goal
        while s != self.start:
            s = min(self.pred[s], key=lambda p: self.g[p] + self.pred[s][p])
            out.append(s)
        out.reverse()
        return out

    @property
    def expansions(self) -> int:
        return len(self.calls[-1]) if self.calls else 0


def lifelong_planning_a_star(
    succ: dict, start: Hashable, goal: Hashable, h: Callable[[Hashable], float], batches: Iterable[Iterable[tuple]]
) -> Iterator[tuple[float, list | None, int]]:
    """MAIN. Yield (cost, path, expansions) first for succ, then after each batch of (u, v, new cost)."""
    lpa = LPAStar(succ, start, goal, h)  # @line L17
    batches = iter(batches)
    while True:  # @line L18
        cost = lpa.compute_shortest_path()  # @line L19
        yield cost, lpa.path(), lpa.expansions
        batch = next(batches, None)  # @line L20
        if batch is None:
            return
        for u, v, c in batch:  # @line L21
            lpa.set_cost(u, v, c)
