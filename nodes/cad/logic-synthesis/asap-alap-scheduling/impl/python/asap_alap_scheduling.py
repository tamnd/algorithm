# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asap-alap-scheduling/. The authors are listed in prov/5S0Z4R.jsonl.

"""ASAP and ALAP schedules of a data flow graph.

Operations are 0 .. n-1. Operation v takes delay[v] >= 1 control steps.
An edge (u, v) says that v reads the result of u, so v may start only
after u ends: t(v) >= t(u) + delay[u]. Steps are numbered from 1, and an
operation that starts at step t uses the steps t .. t + delay[v] - 1.
A schedule meets the latency bound L when every operation ends by step L.
"""

from typing import Optional


def topological_order(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Kahn's algorithm. Raises ValueError on a cycle."""
    succ: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for (u, v) in edges:
        succ[u].append(v)
        indeg[v] += 1
    order = []
    ready = [v for v in range(n) if indeg[v] == 0]
    while ready:
        u = ready.pop()
        order.append(u)
        for v in succ[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    if len(order) < n:
        raise ValueError("the data flow graph has a cycle")
    return order


def asap(n: int, delay: list[int], edges: list[tuple[int, int]]) -> list[int]:
    """The earliest start step of each operation."""
    pred: list[list[int]] = [[] for _ in range(n)]
    for (u, v) in edges:
        pred[v].append(u)
    t = [0] * n
    order = topological_order(n, edges)  # @line L1
    for v in order:  # @line L2
        t[v] = max([1] + [t[u] + delay[u] for u in pred[v]])  # @line L3
    return t  # @line L4


def alap(n: int, delay: list[int], edges: list[tuple[int, int]], latency: int) -> Optional[list[int]]:
    """The latest start step of each operation with every operation done by
    step latency. None if the latency is shorter than the critical path."""
    succ: list[list[int]] = [[] for _ in range(n)]
    for (u, v) in edges:
        succ[u].append(v)
    t = [0] * n
    order = topological_order(n, edges)
    for v in reversed(order):  # @line L5
        t[v] = min([latency + 1] + [t[w] for w in succ[v]]) - delay[v]  # @line L6
    if any(x < 1 for x in t):  # @line L7
        return None
    return t  # @line L8


def latency_of(start: list[int], delay: list[int]) -> int:
    """The last step that the schedule uses."""
    return max((s + dl - 1 for s, dl in zip(start, delay)), default=0)


def mobility(n: int, delay: list[int], edges: list[tuple[int, int]], latency: int) -> Optional[list[int]]:
    """ALAP minus ASAP for each operation, or None if the latency is too short."""
    late = alap(n, delay, edges, latency)
    if late is None:
        return None
    early = asap(n, delay, edges)
    return [b - a for a, b in zip(early, late)]  # @line L9
