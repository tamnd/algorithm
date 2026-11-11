# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadlock-detection/. The authors are listed in prov/YGHDZH.jsonl.

"""Deadlock detection for reusable resources.

A state has n processes and m resource types: avail[r] free units,
alloc[i][r] units held by process i, and req[i][r] units that process i
waits for. A process is deadlocked when it is blocked in every future.
"""

from typing import Callable, Optional

Vec = list[int]
Mat = list[list[int]]


def detect(avail: Vec, alloc: Mat, req: Mat) -> list[int]:
    """The deadlocked processes, by graph reduction.

    Precondition: all entries are nonnegative and the matrices are n x m.
    Cost: O(m n^2) time, O(m + n) extra space.
    """
    n, m = len(alloc), len(avail)
    work = list(avail)  # @line L1
    finish = [False] * n
    while True:  # @line L2
        progress = False  # @line L3
        for i in range(n):  # @line L4
            if not finish[i] and all(req[i][r] <= work[r] for r in range(m)):  # @line L5
                for r in range(m):  # @line L6
                    work[r] += alloc[i][r]
                finish[i] = True
                progress = True
        if not progress:  # @line L7
            return [i for i in range(n) if not finish[i]]  # @line L8


def detect_fast(avail: Vec, alloc: Mat, req: Mat) -> list[int]:
    """The same set as detect(), with sorted requests and wait counts.

    For each type the processes are sorted by their request; a pointer per
    type moves forward as the free units grow, and a count per process says
    on how many types it still waits. Cost: O(m n log n) for the sorts and
    O(m n) for the rest.
    """
    n, m = len(alloc), len(avail)
    work = list(avail)
    order = [sorted(range(n), key=lambda i, r=r: req[i][r]) for r in range(m)]
    ptr = [0] * m
    waits = [m] * n
    ready: list[int] = []

    def advance(r: int) -> None:
        while ptr[r] < n and req[order[r][ptr[r]]][r] <= work[r]:
            i = order[r][ptr[r]]
            ptr[r] += 1
            waits[i] -= 1
            if waits[i] == 0:
                ready.append(i)

    for r in range(m):
        advance(r)
    if m == 0:
        ready = list(range(n))
    done = [False] * n
    while ready:
        i = ready.pop()
        done[i] = True
        for r in range(m):
            if alloc[i][r]:
                work[r] += alloc[i][r]
                advance(r)
    return [i for i in range(n) if not done[i]]


def deadlocked_in_wait_for_graph(succ: dict[int, set[int]]) -> set[int]:
    """Single unit resources: the processes that can reach a cycle.

    Peel processes that wait for nobody still present, as in a topological
    sort; the rest can reach a cycle. Cost: O(n + e).
    """
    pred: dict[int, list[int]] = {v: [] for v in succ}
    out = {v: len(succ[v]) for v in succ}
    for v, ws in succ.items():
        for w in ws:
            pred.setdefault(w, []).append(v)
            out.setdefault(w, 0)
    stack = [v for v, d in out.items() if d == 0]
    gone = set(stack)
    while stack:
        w = stack.pop()
        for v in pred.get(w, ()):
            out[v] -= 1
            if out[v] == 0:
                gone.add(v)
                stack.append(v)
    return set(out) - gone


def find_cycle(succ: dict[int, set[int]]) -> Optional[list[int]]:
    """One cycle of a directed graph, or None, by iterative depth-first search. Cost: O(n + e)."""
    color: dict[int, int] = {}
    for s in sorted(succ):
        if color.get(s):
            continue
        color[s] = 1
        path = [s]
        stack = [iter(sorted(succ.get(s, ())))]
        while stack:
            w = next(stack[-1], None)
            if w is None:
                color[path.pop()] = 2
                stack.pop()
            elif color.get(w, 0) == 1:
                return path[path.index(w):]
            elif color.get(w, 0) == 0:
                color[w] = 1
                path.append(w)
                stack.append(iter(sorted(succ.get(w, ()))))
    return None


def recover(avail: Vec, alloc: Mat, req: Mat, cost: Callable[[int], float]) -> list[int]:
    """Abort deadlocked processes, cheapest first, until no deadlock is left.

    An aborted process gives back all its units and drops its request.
    Returns the victims in order. Cost: O(m n^3) with detect().
    """
    avail = list(avail)
    alloc = [row[:] for row in alloc]
    req = [row[:] for row in req]
    victims: list[int] = []
    while True:
        dead = detect(avail, alloc, req)
        if not dead:
            return victims
        v = min(dead, key=lambda i: (cost(i), i))
        victims.append(v)
        for r in range(len(avail)):
            avail[r] += alloc[v][r]
            alloc[v][r] = 0
            req[v][r] = 0
