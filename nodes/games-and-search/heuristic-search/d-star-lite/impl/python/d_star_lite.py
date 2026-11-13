# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-star-lite/. The authors are listed in prov/TCGXBA.jsonl.

"""D* Lite (Koenig and Likhachev 2002), the basic version of Figure 3.

The search runs backward, from the goal to the robot. g(s) estimates the
distance from s to the goal and rhs(s) is the one-step lookahead value
min over successors s' of c(s, s') + g(s'). The heuristic h(a, b) estimates
the distance between two vertices. It must be nonnegative, at most the true
distance, and satisfy h(a, c) <= h(a, b) + h(b, c). Edge costs are positive,
and math.inf means that the edge is blocked.

The queue is a binary heap with lazy deletion: self.key holds the key of
each queued vertex, and a heap entry with another key is skipped. Keys are
lower bounds after the robot moves; the variable km keeps them in order.
"""

import heapq
import itertools
import math
from collections.abc import Callable, Hashable

INF = math.inf


class DStarLite:
    def __init__(self, succ: dict, start: Hashable, goal: Hashable, h: Callable[[Hashable, Hashable], float]):
        """succ maps each vertex to a dict {successor: cost}: the map that the robot believes."""
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
        self.km = 0
        self.g = {u: INF for u in self.succ}  # @line L3
        self.rhs = {u: INF for u in self.succ}
        self.rhs[goal] = 0  # @line L4
        self._insert(goal)  # @line L5
        self.calls: list[list[tuple]] = []  # per call: (vertex, "over" or "under", key)
        self.reinserts = 0

    # -- the priority queue U -------------------------------------------------
    def calculate_key(self, s) -> tuple:
        m = min(self.g[s], self.rhs[s])
        return (m + self.h(self.start, s) + self.km, m)  # @line L1

    def _insert(self, s, k=None) -> None:
        k = self.calculate_key(s) if k is None else k
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
        if u != self.goal:  # @line L6
            self.rhs[u] = min((c + self.g[s] for s, c in self.succ[u].items()), default=INF)
        self.key.pop(u, None)  # @line L7
        if self.g[u] != self.rhs[u]:  # @line L8
            self._insert(u)

    def compute_shortest_path(self) -> float:
        log: list[tuple] = []
        start = self.start
        while self.top_key() < self.calculate_key(start) or self.rhs[start] != self.g[start]:  # @line L9
            k_old = self.top_key()
            u = self._pop()  # @line L10
            k_new = self.calculate_key(u)
            if k_old < k_new:  # @line L11
                self.reinserts += 1
                self._insert(u, k_new)
            elif self.g[u] > self.rhs[u]:  # @line L12
                log.append((u, "over", k_old))
                self.g[u] = self.rhs[u]  # @line L13
                for s in self.pred[u]:  # @line L14
                    self.update_vertex(s)
            else:  # @line L15
                log.append((u, "under", k_old))
                self.g[u] = INF  # @line L16
                for s in list(self.pred[u]) + [u]:  # @line L17
                    self.update_vertex(s)
        self.calls.append(log)
        return self.g[start]

    def next_vertex(self):
        """The successor of the robot that minimizes c + g."""
        return min(self.succ[self.start], key=lambda s: self.succ[self.start][s] + self.g[s])

    def set_cost(self, u, v, c: float) -> None:
        if not c > 0:
            raise ValueError("edge costs must be positive")
        self.succ[u][v] = c  # @line L29
        self.pred[v][u] = c
        self.update_vertex(u)  # @line L30


def d_star_lite(
    succ: dict,
    start: Hashable,
    goal: Hashable,
    h: Callable[[Hashable, Hashable], float],
    sense: Callable[[Hashable, dict], list],
) -> tuple[list | None, DStarLite]:
    """Move a robot from start to goal on a map that it learns while it moves.

    succ is the first map, usually with every unknown edge assumed free. After
    each move, sense(robot, believed_succ) returns the list of (u, v, cost)
    whose cost differs from the map. The result is the walk of the robot, or
    None when the map shows that the goal cannot be reached, and the planner.
    """
    succ = {u: dict(vs) for u, vs in succ.items()}
    for u, v, c in sense(start, succ):  # the first map includes what the robot sees at the start
        succ[u][v] = c
    s_last = start  # @line L18
    d = DStarLite(succ, start, goal, h)  # @line L19
    d.compute_shortest_path()
    walk = [start]
    while d.start != goal:  # @line L20
        if d.g[d.start] == INF:  # @line L21
            return None, d
        d.start = d.next_vertex()  # @line L22
        walk.append(d.start)  # @line L23
        changes = sense(d.start, d.succ)  # @line L24
        if changes:  # @line L25
            d.km += d.h(s_last, d.start)  # @line L26
            s_last = d.start  # @line L27
            for u, v, c in changes:  # @line L28
                d.set_cost(u, v, c)
            d.compute_shortest_path()  # @line L31
    return walk, d
