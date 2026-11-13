# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conflict-based-search/. The authors are listed in prov/DBEXMS.jsonl.

"""Conflict-based search (Sharon, Stern, Felner and Sturtevant) for multi-agent pathfinding on a grid.

The agents move on a 4-connected grid in discrete time steps. In each step an
agent moves to a free neighbour or waits. Two agents may not be in one cell at
one time (a vertex conflict) and may not swap cells in one step (an edge
conflict). An agent stays at its goal after it arrives, and its cost is the
time of its last arrival at the goal. CBS minimizes the sum of these costs.

The high level searches a binary constraint tree. The low level is a
space-time A* for one agent that obeys the constraints of that agent.
"""

import heapq
from collections import deque

MOVES = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Grid:
    def __init__(self, rows: list[str]):
        """rows[y][x] is '#' for a wall."""
        self.rows = rows
        self.h, self.w = len(rows), len(rows[0]) if rows else 0

    def free(self, cell) -> bool:
        x, y = cell
        return 0 <= x < self.w and 0 <= y < self.h and self.rows[y][x] != "#"

    def neighbours(self, cell):
        x, y = cell
        for dx, dy in MOVES:
            if self.free((x + dx, y + dy)):
                yield x + dx, y + dy

    def distances(self, goal):
        """Breadth-first distances to goal, the heuristic of the low level."""
        dist = {goal: 0}
        queue = deque([goal])
        while queue:
            u = queue.popleft()
            for v in self.neighbours(u):
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        return dist


def at(path, t):
    """The cell of an agent at time t; it stays at its goal after the end of its path."""
    return path[min(t, len(path) - 1)]


def first_conflict(paths):
    """The earliest conflict as ('vertex', i, j, cell, t) or ('edge', i, j, u, v, t), or None.

    An edge conflict means that agent i moves from u to v and agent j from v to u, arriving at time t.
    """
    horizon = max(len(p) for p in paths)
    for t in range(horizon):
        for i in range(len(paths)):
            for j in range(i + 1, len(paths)):
                if at(paths[i], t) == at(paths[j], t):
                    return ("vertex", i, j, at(paths[i], t), t)
                if t > 0:
                    u, v = at(paths[i], t - 1), at(paths[i], t)
                    if u != v and at(paths[j], t - 1) == v and at(paths[j], t) == u:
                        return ("edge", i, j, u, v, t)
    return None


def low_level(grid, start, goal, constraints, dist):
    """Space-time A* for one agent. constraints holds (cell, t) and (u, v, t) entries.

    Return a shortest list of cells from time 0 to the last arrival at goal that obeys the constraints, or None.
    """
    if start not in dist:
        return None
    vertex = {c for c in constraints if len(c) == 2}
    edge = {c for c in constraints if len(c) == 3}
    last = max((c[-1] for c in constraints), default=0)  # after this time nothing is forbidden
    goal_block = max((t for cell, t in vertex if cell == goal), default=-1)
    if (start, 0) in vertex:
        return None
    heap = [(dist[start], 0, start)]  # @line L13
    parent = {(start, 0): None}
    closed = set()
    while heap:  # @line L14
        _, t, v = heapq.heappop(heap)
        key = (v, min(t, last + 1))  # from time last + 1 on, a later visit of v is never better
        if key in closed:
            continue
        closed.add(key)
        if v == goal and t > goal_block:  # @line L15
            path = [v]
            state = (v, t)
            while parent[state] is not None:
                state = parent[state]
                path.append(state[0])
            return path[::-1]
        for w in (v, *grid.neighbours(v)):  # @line L16
            if (w, t + 1) in vertex or (v, w, t + 1) in edge:
                continue
            if (w, min(t + 1, last + 1)) in closed or (w, t + 1) in parent:
                continue
            parent[(w, t + 1)] = (v, t)
            heapq.heappush(heap, (t + 1 + dist[w], t + 1, w))
    return None  # @line L17


def cost(path):
    return len(path) - 1


def conflict_based_search(rows, starts, goals, max_nodes=None):
    """Return (paths, sum of costs, number of constraint tree nodes expanded), or (None, None, n).

    The search does not stop on an unsolvable instance unless max_nodes is given.
    """
    grid = Grid(rows)
    k = len(starts)
    if len(goals) != k or len(set(starts)) != k or len(set(goals)) != k:
        raise ValueError("the agents need distinct starts and distinct goals")
    if not all(grid.free(c) for c in (*starts, *goals)):
        raise ValueError("starts and goals must be free cells")
    dists = [grid.distances(g) for g in goals]
    constraints = tuple(frozenset() for _ in range(k))  # @line L1
    paths = []
    for i in range(k):
        p = low_level(grid, starts[i], goals[i], constraints[i], dists[i])
        if p is None:
            return None, None, 0
        paths.append(p)
    tie = 0
    open_list = [(sum(map(cost, paths)), tie, constraints, paths)]  # @line L2
    expanded = 0
    while open_list:  # @line L3
        total, _, constraints, paths = heapq.heappop(open_list)  # @line L4
        expanded += 1
        conflict = first_conflict(paths)  # @line L5
        if conflict is None:
            return paths, total, expanded  # @line L6
        if max_nodes is not None and expanded >= max_nodes:
            break
        if conflict[0] == "vertex":  # @line L7
            _, i, j, cell, t = conflict
            new = ((i, (cell, t)), (j, (cell, t)))
        else:  # @line L8
            _, i, j, u, v, t = conflict
            new = ((i, (u, v, t)), (j, (v, u, t)))
        for a, c in new:  # @line L9
            child = list(constraints)
            child[a] = constraints[a] | {c}  # @line L10
            p = low_level(grid, starts[a], goals[a], child[a], dists[a])
            if p is not None:  # @line L11
                child_paths = list(paths)
                child_paths[a] = p
                tie += 1
                heapq.heappush(open_list, (sum(map(cost, child_paths)), tie, tuple(child), child_paths))
    return None, None, expanded  # @line L12
