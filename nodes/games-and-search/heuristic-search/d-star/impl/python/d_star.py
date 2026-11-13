# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-star/. The authors are listed in prov/X5ZAVD.jsonl.

"""D* (Stentz 1994), the basic version without the focussing heuristic.

The search runs backward from the goal. h[x] is the cost of the path from
x to the goal through the back pointers b, and k[x] is the key of x on the
OPEN list: the least value of h[x] since x was last put on OPEN. A state
with k[x] < h[x] is a RAISE state and a state with k[x] == h[x] is a LOWER
state. c(a, b) is the cost of moving from a to b, math.inf when the arc is
blocked or missing. The paper writes c(X, Y) for the arc from Y to X; this
file uses the usual order.

OPEN is a binary heap with lazy deletion: an entry whose key is not the
current k of an OPEN state is skipped.
"""

import heapq
import itertools
import math
from collections.abc import Callable, Hashable

INF = math.inf
NEW, OPEN, CLOSED = "NEW", "OPEN", "CLOSED"


class DStar:
    def __init__(self, succ: dict, goal: Hashable):
        """succ maps each state to a dict {successor: cost}: the map that the robot believes."""
        self.succ = {u: dict(vs) for u, vs in succ.items()}
        self.pred: dict = {u: {} for u in self.succ}
        for u, vs in self.succ.items():
            for v, c in vs.items():
                if v == u:
                    raise ValueError("self-loops are not allowed")
                if not c > 0:
                    raise ValueError("arc costs must be positive")
                self.pred[v][u] = c
        self.nbrs = {u: set(self.succ[u]) | set(self.pred[u]) for u in self.succ}
        self.goal = goal
        self.t = {u: NEW for u in self.succ}
        self.h = {u: INF for u in self.succ}
        self.k = {u: INF for u in self.succ}
        self.b: dict = {}
        self.heap: list = []
        self.tie = itertools.count()
        self.processed = 0  # number of PROCESS-STATE calls that removed a state
        self.insert(goal, 0)

    def c(self, a, b) -> float:
        return self.succ[a].get(b, INF)

    # -- the OPEN list ---------------------------------------------------------
    def _clean(self) -> None:
        while self.heap:
            k, _, x = self.heap[0]
            if self.t[x] == OPEN and self.k[x] == k:
                return
            heapq.heappop(self.heap)

    def min_state(self):
        self._clean()
        return self.heap[0][2] if self.heap else None

    def get_kmin(self) -> float:
        self._clean()
        return self.heap[0][0] if self.heap else -1

    def insert(self, x, h_new: float) -> None:
        if self.t[x] == NEW:  # @line L21
            self.k[x] = h_new
        elif self.t[x] == OPEN:  # @line L22
            self.k[x] = min(self.k[x], h_new)
        else:  # @line L23
            self.k[x] = min(self.h[x], h_new)
        self.h[x] = h_new  # @line L24
        self.t[x] = OPEN
        heapq.heappush(self.heap, (self.k[x], next(self.tie), x))

    # -- the algorithm ---------------------------------------------------------
    def process_state(self) -> float:
        x = self.min_state()  # @line L1
        if x is None:  # @line L2
            return -1
        k_old = self.get_kmin()  # @line L3
        self.t[x] = CLOSED
        self.processed += 1
        h, b, c = self.h, self.b, self.c
        if k_old < h[x]:  # @line L4
            for y in self.nbrs[x]:  # @line L5
                if h[y] <= k_old and h[x] > h[y] + c(x, y):  # @line L6
                    b[x] = y  # @line L7
                    h[x] = h[y] + c(x, y)
        if k_old == h[x]:  # @line L8
            for y in self.nbrs[x]:  # @line L9
                cyx = c(y, x)
                if (
                    self.t[y] == NEW
                    or (b.get(y) == x and h[y] != h[x] + cyx)
                    or (b.get(y) != x and h[y] > h[x] + cyx)
                ):  # @line L10
                    b[y] = x  # @line L11
                    self.insert(y, h[x] + cyx)
        else:  # @line L12
            for y in self.nbrs[x]:  # @line L13
                cyx = c(y, x)
                if self.t[y] == NEW or (b.get(y) == x and h[y] != h[x] + cyx):  # @line L14
                    b[y] = x  # @line L15
                    self.insert(y, h[x] + cyx)
                elif b.get(y) != x and h[y] > h[x] + cyx:  # @line L16
                    self.insert(x, h[x])  # @line L17
                elif b.get(y) != x and h[x] > h[y] + c(x, y) and self.t[y] == CLOSED and h[y] > k_old:  # @line L18
                    self.insert(y, h[y])  # @line L19
        return self.get_kmin()  # @line L20

    def modify_cost(self, y, x, cval: float) -> float:
        """The arc from y to x gets the cost cval."""
        if not cval > 0:
            raise ValueError("arc costs must be positive")
        if x not in self.succ[y]:
            self.nbrs[x].add(y)
            self.nbrs[y].add(x)
        self.succ[y][x] = cval  # @line L25
        self.pred[x][y] = cval
        if self.t[x] == CLOSED:  # @line L26
            self.insert(x, self.h[x])
        return self.get_kmin()  # @line L27

    def plan_first(self, robot) -> float:
        """Process states until the robot state is closed or OPEN is empty."""
        while self.t[robot] != CLOSED:  # @line L29
            if self.process_state() == -1:
                break
        return self.h[robot]

    def replan(self, robot) -> float:
        """Process states until k_min >= h(robot) or OPEN is empty."""
        k_min = self.get_kmin()
        while k_min != -1 and k_min < self.h[robot]:  # @line L34
            k_min = self.process_state()
        return self.h[robot]

    def path(self, robot) -> list:
        """The states from robot to the goal along the back pointers."""
        p = [robot]
        while p[-1] != self.goal:
            p.append(self.b[p[-1]])
            if len(p) > len(self.succ):
                raise RuntimeError("the back pointers have a cycle")
        return p


def d_star(
    succ: dict,
    start: Hashable,
    goal: Hashable,
    sense: Callable[[Hashable, dict], list],
) -> tuple[list | None, DStar]:
    """Move a robot from start to goal on a map that it learns while it moves.

    succ is the first map. After each move, sense(robot, believed_succ)
    returns the list of (u, v, cost) whose cost differs from the map. The
    result is the walk of the robot, or None when the map shows that the
    goal cannot be reached, and the planner.
    """
    succ = {u: dict(vs) for u, vs in succ.items()}
    for u, v, c in sense(start, succ):  # the first map includes what the robot sees at the start
        succ[u][v] = c
    d = DStar(succ, goal)  # @line L28
    robot = start
    d.plan_first(robot)
    walk = [robot]
    while robot != goal:  # @line L30
        if d.h[robot] == INF:  # @line L31
            return None, d
        robot = d.b[robot]  # @line L32
        walk.append(robot)
        changes = sense(robot, d.succ)
        if changes:
            for u, v, c in changes:  # @line L33
                d.modify_cost(u, v, c)
            d.replan(robot)
    return walk, d
