# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/water-jug-problem/. The authors are listed in prov/DYGENX.jsonl.
"""The water jug problem: the gcd rule, breadth-first search, and the two pouring strategies.

Two jugs hold a and b units (a, b >= 1) and start empty. A step fills a jug
from the tap, empties a jug, or pours one jug into the other until the
first is empty or the second is full. The target is c units in one jug.
"""

from collections import deque
from math import gcd
from typing import Dict, List, Optional, Sequence, Tuple

State = Tuple[int, ...]


def measurable(a: int, b: int, c: int) -> bool:
    """True when c units can be left in one of the two jugs."""
    return 0 <= c <= max(a, b) and c % gcd(a, b) == 0


def two_jug_moves(s: State, a: int, b: int) -> List[Tuple[str, State]]:
    x, y = s
    t = min(x, b - y)
    u = min(y, a - x)
    return [
        ("fill A", (a, y)),
        ("fill B", (x, b)),
        ("empty A", (0, y)),
        ("empty B", (x, 0)),
        ("pour A into B", (x - t, y + t)),
        ("pour B into A", (x + u, y - u)),
    ]


def bfs(a: int, b: int) -> Tuple[Dict[State, int], Dict[State, Tuple[State, str]]]:
    """Distances from (0, 0) and parent links over the (a + 1)(b + 1) states."""
    start = (0, 0)
    dist = {start: 0}
    parent: Dict[State, Tuple[State, str]] = {}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        for name, t in two_jug_moves(s, a, b):
            if t not in dist:
                dist[t] = dist[s] + 1
                parent[t] = (s, name)
                queue.append(t)
    return dist, parent


def shortest_plan(a: int, b: int, c: int) -> Optional[List[str]]:
    """A shortest list of steps that leaves c units in one jug, or None."""
    dist, parent = bfs(a, b)
    goals = [s for s in dist if c in s]
    if not goals:
        return None
    s = min(goals, key=dist.__getitem__)
    plan = []
    while s != (0, 0):
        s, name = parent[s]
        plan.append(name)
    return plan[::-1]


def strategy_steps(a: int, b: int, c: int) -> Optional[int]:
    """Steps of the better of the two cycling strategies, or None if c is never seen.

    Strategy "A to B": fill A when it is empty, empty B when it is full, else
    pour A into B. Strategy "B to A" is the mirror. A run stops when it
    repeats a state, so it ends for every target.
    """
    if c == 0:
        return 0
    best = None
    for p, q in ((a, b), (b, a)):
        x = y = 0
        steps = 0
        seen = {(0, 0)}
        while True:
            if x == 0:
                x = p
            elif y == q:
                y = 0
            else:
                t = min(x, q - y)
                x, y = x - t, y + t
            steps += 1
            if x == c or y == c:
                if best is None or steps < best:
                    best = steps
                break
            if (x, y) in seen:
                break
            seen.add((x, y))
    return best


def pour_only_bfs(caps: Sequence[int], start: State) -> Dict[State, int]:
    """Distances when the only step is pouring one jug into another (no tap, no drain)."""
    dist = {tuple(start): 0}
    queue = deque([tuple(start)])
    k = len(caps)
    while queue:
        s = queue.popleft()
        for i in range(k):
            for j in range(k):
                if i == j or s[i] == 0 or s[j] == caps[j]:
                    continue
                t = min(s[i], caps[j] - s[j])
                n = list(s)
                n[i] -= t
                n[j] += t
                nt = tuple(n)
                if nt not in dist:
                    dist[nt] = dist[s] + 1
                    queue.append(nt)
    return dist
