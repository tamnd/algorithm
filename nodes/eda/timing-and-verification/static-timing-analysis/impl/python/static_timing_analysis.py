# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/static-timing-analysis/. The authors are listed in prov/84BFXG.jsonl.

from collections import deque
from typing import Mapping, Optional, Sequence


def topological_order(n: int, edges: Sequence[tuple[int, int, object]]) -> list[int]:
    """Kahn's algorithm. Raises ValueError if the graph has a cycle."""
    indeg = [0] * n
    out: list[list[int]] = [[] for _ in range(n)]
    for u, v, _ in edges:
        out[u].append(v)
        indeg[v] += 1
    queue = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in out[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if len(order) != n:
        raise ValueError("the timing graph has a cycle")
    return order


def static_timing_analysis(
    n: int,
    edges: Sequence[tuple[int, int, object]],
    at_start: Mapping[int, object],
    rt_end: Mapping[int, object],
    early: bool = False,
):
    """Block-based static timing analysis on a timing DAG.

    The vertices are 0 .. n-1. Each edge is (u, v, d) with delay d (int or
    Fraction). at_start gives the arrival time of every vertex with no in-edge
    (a start point), and rt_end the required time of every vertex with no
    out-edge (an endpoint).

    Late mode (early=False, the setup check):
        AT(v) = max over edges (u, v) of AT(u) + d,
        RT(u) = min over edges (u, v) of RT(v) - d,
        slack(v) = RT(v) - AT(v).
    Early mode (early=True, the hold check) swaps max and min, and
        slack(v) = AT(v) - RT(v).
    A negative slack is a violation in both modes.

    Returns (AT, RT, slack) as lists. Raises ValueError on a cycle or a
    missing start or end time. Time and extra space: O(V + E).
    """
    pick_at = min if early else max
    pick_rt = max if early else min
    ins: list[list[tuple[int, object]]] = [[] for _ in range(n)]
    outs: list[list[tuple[int, object]]] = [[] for _ in range(n)]
    for u, v, d in edges:
        ins[v].append((u, d))
        outs[u].append((v, d))
    order = topological_order(n, edges)  # @line L1
    at: list[Optional[object]] = [None] * n
    for v in order:  # @line L2
        if not ins[v]:  # @line L3
            if v not in at_start:
                raise ValueError(f"start point {v} has no arrival time")
            at[v] = at_start[v]
        else:
            at[v] = pick_at(at[u] + d for u, d in ins[v])  # @line L4
    rt: list[Optional[object]] = [None] * n
    for u in reversed(order):  # @line L5
        if not outs[u]:  # @line L6
            if u not in rt_end:
                raise ValueError(f"endpoint {u} has no required time")
            rt[u] = rt_end[u]
        else:
            rt[u] = pick_rt(rt[v] - d for v, d in outs[u])  # @line L7
    if early:  # @line L8
        slack = [at[v] - rt[v] for v in range(n)]
    else:
        slack = [rt[v] - at[v] for v in range(n)]
    return at, rt, slack  # @line L9


def critical_path(
    n: int,
    edges: Sequence[tuple[int, int, object]],
    at: Sequence[object],
    slack: Sequence[object],
    early: bool = False,
) -> list[int]:
    """A path of least slack, from a start point to an endpoint.

    Start at an endpoint of least slack and walk back along in-edges whose
    delay sets the arrival time (AT(u) + d == AT(v)).
    """
    ins: list[list[tuple[int, object]]] = [[] for _ in range(n)]
    outdeg = [0] * n
    for u, v, d in edges:
        ins[v].append((u, d))
        outdeg[u] += 1
    ends = [v for v in range(n) if outdeg[v] == 0]
    v = min(ends, key=lambda x: slack[x])
    path = [v]
    while ins[v]:
        v = next(u for u, d in ins[v] if at[u] + d == at[v])
        path.append(v)
    path.reverse()
    return path
