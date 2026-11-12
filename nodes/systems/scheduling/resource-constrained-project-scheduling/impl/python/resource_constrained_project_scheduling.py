# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/resource-constrained-project-scheduling/. The authors are listed in prov/NND7DR.jsonl.

from typing import Optional, Sequence

Arc = tuple[int, int]


def _preds(n: int, arcs: Sequence[Arc]) -> list[list[int]]:
    pred: list[list[int]] = [[] for _ in range(n)]
    for i, j in arcs:
        pred[j].append(i)
    return pred


def latest_finish_times(p: Sequence[int], arcs: Sequence[Arc]) -> list[int]:
    """LFT of each activity by the backward pass of the critical path method,
    with the resources ignored. Raise ValueError on a cycle."""
    n = len(p)
    succ: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for i, j in arcs:
        succ[i].append(j)
        indeg[j] += 1
    order, stack = [], [i for i in range(n) if indeg[i] == 0]
    while stack:
        i = stack.pop()
        order.append(i)
        for j in succ[i]:
            indeg[j] -= 1
            if indeg[j] == 0:
                stack.append(j)
    if len(order) != n:
        raise ValueError("the precedence graph has a cycle")
    es = [0] * n
    for i in order:
        for j in succ[i]:
            es[j] = max(es[j], es[i] + p[i])
    length = max((es[j] + p[j] for j in range(n)), default=0)
    lf = [length] * n
    for i in reversed(order):
        for j in succ[i]:
            lf[i] = min(lf[i], lf[j] - p[j])
    return lf


def usage_at(t: int, start: dict[int, int], p: Sequence[int], r: Sequence[Sequence[int]], k: int) -> int:
    """The amount of resource k in use at time t (an activity uses it on [S, S + p))."""
    return sum(r[j][k] for j, s in start.items() if s <= t < s + p[j])


def serial_sgs(
    p: Sequence[int],
    arcs: Sequence[Arc],
    r: Sequence[Sequence[int]],
    cap: Sequence[int],
    activity_list: Sequence[int],
) -> list[int]:
    """The serial schedule generation scheme (Kolisch 1996).

    Take the activities in the order of a precedence-feasible list. Start each one
    at the earliest time at which its predecessors have finished and every
    resource k has r[j][k] units free for its whole duration. Return the start times.
    Cost as written: O(n^3 K) time; a resource profile gives O(n^2 K).
    """
    n = len(p)
    pred = _preds(n, arcs)
    start: dict[int, int] = {}
    for j in activity_list:  # @line L3
        if any(i not in start for i in pred[j]):
            raise ValueError("the activity list is not precedence feasible")
        if any(r[j][k] > cap[k] for k in range(len(cap))):
            raise ValueError("an activity needs more than a resource holds")
        t = max((start[i] + p[i] for i in pred[j]), default=0)  # @line L4
        # candidate start times: t, then each finish time later than t
        cands = sorted({t} | {s + p[i] for i, s in start.items() if s + p[i] > t})
        for c in cands:  # @line L5
            # usage only rises at start times, so check c and the starts inside (c, c + p_j)
            points = [c] + [s for s in start.values() if c < s < c + p[j]]
            if p[j] == 0 or all(  # @line L6
                usage_at(x, start, p, r, k) + r[j][k] <= cap[k] for x in points for k in range(len(cap))
            ):
                start[j] = c  # @line L7
                break
    return [start[j] for j in range(n)]  # @line L8


def priority_list(p: Sequence[int], arcs: Sequence[Arc], priority: Sequence[int]) -> list[int]:
    """A precedence-feasible list: at each step take the eligible activity with the
    smallest priority value, ties by index."""
    n = len(p)
    pred = _preds(n, arcs)
    done: set[int] = set()
    out = []
    while len(out) < n:
        eligible = [j for j in range(n) if j not in done and all(i in done for i in pred[j])]
        if not eligible:
            raise ValueError("the precedence graph has a cycle")
        j = min(eligible, key=lambda j: (priority[j], j))
        done.add(j)
        out.append(j)
    return out


def serial_sgs_lft(
    p: Sequence[int], arcs: Sequence[Arc], r: Sequence[Sequence[int]], cap: Sequence[int]
) -> list[int]:
    """The serial SGS with the latest finish time (LFT) priority rule."""
    lf = latest_finish_times(p, arcs)  # @line L1
    activity_list = priority_list(p, arcs, lf)  # @line L2
    return serial_sgs(p, arcs, r, cap, activity_list)


def makespan(p: Sequence[int], start: Sequence[int]) -> int:
    return max((s + d for s, d in zip(start, p)), default=0)


def is_feasible(
    p: Sequence[int],
    arcs: Sequence[Arc],
    r: Sequence[Sequence[int]],
    cap: Sequence[int],
    start: Sequence[int],
) -> Optional[str]:
    """None when the start times respect every arc and every capacity at every time; else a reason."""
    for i, j in arcs:
        if start[j] < start[i] + p[i]:
            return f"arc {i} -> {j}"
    if any(s < 0 for s in start):
        return "negative start"
    horizon = makespan(p, start)
    for t in range(horizon):
        for k in range(len(cap)):
            use = sum(r[j][k] for j in range(len(p)) if start[j] <= t < start[j] + p[j])
            if use > cap[k]:
                return f"resource {k} at time {t}"
    return None
