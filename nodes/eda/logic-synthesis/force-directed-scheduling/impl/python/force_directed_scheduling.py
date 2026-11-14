# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/force-directed-scheduling/. The authors are listed in prov/CDK7W8.jsonl.

"""Force-directed scheduling (Paulin and Knight) under a latency bound.

Operations are 0 .. n-1, each with a unit type kind[v] (for example
"mul" or "alu") and a delay delay[v] >= 1 in control steps. An edge (u, v)
means t(v) >= t(u) + delay[u]. Steps are 1 .. latency, and an operation
that starts at t uses the steps t .. t + delay[v] - 1. All probabilities
are exact fractions, so the ties and the result do not depend on rounding.
"""

from fractions import Fraction
from typing import Hashable, Optional

Frames = list[tuple[int, int]]


def _order(n: int, edges: list[tuple[int, int]]) -> list[int]:
    succ: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for (u, v) in edges:
        succ[u].append(v)
        indeg[v] += 1
    order, ready = [], [v for v in range(n) if indeg[v] == 0]
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


def time_frames(n: int, delay: list[int], edges: list[tuple[int, int]], latency: int,
                fixed: dict[int, int]) -> Optional[Frames]:
    """The frame [ASAP, ALAP] of each operation when the operations in fixed
    must start at the given steps. None if no schedule meets all of it."""
    pred: list[list[int]] = [[] for _ in range(n)]
    succ: list[list[int]] = [[] for _ in range(n)]
    for (u, v) in edges:
        pred[v].append(u)
        succ[u].append(v)
    order = _order(n, edges)
    lo = [0] * n
    for v in order:
        lo[v] = max([1] + [lo[u] + delay[u] for u in pred[v]])
        if v in fixed:
            if fixed[v] < lo[v]:
                return None
            lo[v] = fixed[v]
    hi = [0] * n
    for v in reversed(order):
        hi[v] = min([latency + 1] + [hi[w] for w in succ[v]]) - delay[v]
        if v in fixed:
            if fixed[v] > hi[v]:
                return None
            hi[v] = fixed[v]
    if any(lo[v] > hi[v] for v in range(n)):
        return None
    return list(zip(lo, hi))


def occupancy(frame: tuple[int, int], d: int) -> dict[int, Fraction]:
    """The probability that the operation uses each step, when each start in
    its frame has the same probability."""
    lo, hi = frame
    p = Fraction(1, hi - lo + 1)
    out: dict[int, Fraction] = {}
    for s in range(lo, hi + 1):
        for t in range(s, s + d):
            out[t] = out.get(t, Fraction(0)) + p
    return out


def distribution_graphs(n: int, kind: list[Hashable], delay: list[int], frames: Frames) -> dict:
    """DG[k][t]: the expected number of operations of type k that use step t."""
    dg: dict = {}
    for v in range(n):
        row = dg.setdefault(kind[v], {})
        for t, p in occupancy(frames[v], delay[v]).items():
            row[t] = row.get(t, Fraction(0)) + p
    return dg


def force(n: int, kind, delay, edges, latency, fixed, frames: Frames, dg, v: int, s: int) -> Optional[Fraction]:
    """The total force of starting v at step s: the self force of v plus the
    forces of the other operations whose frames shrink as a result."""
    new = time_frames(n, delay, edges, latency, {**fixed, v: s})  # @line L8
    if new is None:
        return None
    total = Fraction(0)
    for j in range(n):
        if new[j] == frames[j]:
            continue
        before = occupancy(frames[j], delay[j])
        after = occupancy(new[j], delay[j])
        row = dg[kind[j]]
        for t in set(before) | set(after):
            total += row.get(t, Fraction(0)) * (after.get(t, Fraction(0)) - before.get(t, Fraction(0)))  # @line L9
    return total


def force_directed_schedule(n: int, kind: list[Hashable], delay: list[int], edges: list[tuple[int, int]],
                            latency: int, trace: Optional[list] = None) -> Optional[list[int]]:
    """A start step for each operation with all precedences met and every
    operation done by step latency, or None if the latency is too short.
    If trace is a list, each fixing (v, s, force) is appended to it."""
    fixed: dict[int, int] = {}
    frames = time_frames(n, delay, edges, latency, fixed)  # @line L1
    if frames is None:  # @line L2
        return None
    while True:  # @line L3
        for v in range(n):  # @line L4: an operation whose frame has one step is fixed at no cost
            if v not in fixed and frames[v][0] == frames[v][1]:
                fixed[v] = frames[v][0]
        if len(fixed) == n:  # @line L5
            return [fixed[v] for v in range(n)]
        dg = distribution_graphs(n, kind, delay, frames)  # @line L6
        best = None
        for v in range(n):  # @line L7
            if v in fixed:
                continue
            for s in range(frames[v][0], frames[v][1] + 1):
                f = force(n, kind, delay, edges, latency, fixed, frames, dg, v, s)
                assert f is not None  # every step of a frame extends to a schedule
                if best is None or f < best[0]:  # @line L10: the first least force wins a tie
                    best = (f, v, s)
        f, v, s = best
        if trace is not None:
            trace.append((v, s, f))
        fixed[v] = s  # @line L11
        frames = time_frames(n, delay, edges, latency, fixed)
        assert frames is not None


def resource_usage(n: int, kind: list[Hashable], delay: list[int], start: list[int]) -> dict:
    """The number of units of each type that the schedule needs: the largest
    number of operations of that type that use one step."""
    use: dict = {}
    for v in range(n):
        for t in range(start[v], start[v] + delay[v]):
            use[(kind[v], t)] = use.get((kind[v], t), 0) + 1
    out: dict = {}
    for (k, _), c in use.items():
        out[k] = max(out.get(k, 0), c)
    return out
