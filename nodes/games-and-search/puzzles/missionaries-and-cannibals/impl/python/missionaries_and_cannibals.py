# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/missionaries-and-cannibals/. The authors are listed in prov/YW0KDJ.jsonl.
"""Missionaries and cannibals: breadth-first search over the states of the river.

A state (m, c, b) gives the missionaries and cannibals on the start bank and
the side of the boat (b = 1: start bank, b = 0: far bank). A bank is safe when
it has no missionaries or at least as many missionaries as cannibals. A
crossing carries between 1 and k people, and both banks must be safe after it.
"""

from collections import deque
from typing import Dict, List, Optional, Tuple

State = Tuple[int, int, int]


def safe(m: int, c: int, n: int) -> bool:
    return (m == 0 or m >= c) and (n - m == 0 or n - m >= n - c)


def loads(k: int) -> List[Tuple[int, int]]:
    """All boat loads (missionaries, cannibals) with 1 to k people."""
    return [(i, j) for i in range(k + 1) for j in range(k + 1 - i) if i + j >= 1]


def successors(s: State, n: int, k: int, boat_safe: bool = False) -> List[State]:
    m, c, b = s
    out = []
    sign = -1 if b == 1 else 1
    for i, j in loads(k):
        if boat_safe and 0 < i < j:
            continue
        nm, nc = m + sign * i, c + sign * j
        if 0 <= nm <= n and 0 <= nc <= n and safe(nm, nc, n):
            out.append((nm, nc, 1 - b))
    return out


def bfs(n: int, k: int, boat_safe: bool = False) -> Tuple[Dict[State, int], Dict[State, State]]:
    start = (n, n, 1)
    dist = {start: 0}
    parent: Dict[State, State] = {}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        for t in successors(s, n, k, boat_safe):
            if t not in dist:
                dist[t] = dist[s] + 1
                parent[t] = s
                queue.append(t)
    return dist, parent


def shortest_crossings(n: int, k: int, boat_safe: bool = False) -> Optional[int]:
    """Fewest crossings that bring n missionaries and n cannibals across, or None."""
    dist, _ = bfs(n, k, boat_safe)
    return dist.get((0, 0, 0))


def shortest_plan(n: int, k: int, boat_safe: bool = False) -> Optional[List[State]]:
    """The states of one shortest solution, from (n, n, 1) to (0, 0, 0)."""
    dist, parent = bfs(n, k, boat_safe)
    goal = (0, 0, 0)
    if goal not in dist:
        return None
    path = [goal]
    while path[-1] != (n, n, 1):
        path.append(parent[path[-1]])
    return path[::-1]


def count_shortest(n: int, k: int) -> int:
    """The number of different shortest solutions."""
    dist, _ = bfs(n, k)
    ways = {(n, n, 1): 1}
    for s in sorted(dist, key=dist.__getitem__):
        for t in successors(s, n, k):
            if dist.get(t) == dist[s] + 1:
                ways[t] = ways.get(t, 0) + ways[s]
    return ways.get((0, 0, 0), 0)
