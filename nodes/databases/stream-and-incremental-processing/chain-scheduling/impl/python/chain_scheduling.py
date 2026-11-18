# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chain-scheduling/. The authors are listed in prov/XJAPP3.jsonl.

"""Chain operator scheduling (Babcock, Babu, Datar and Motwani, SIGMOD 2003).

A query is a chain of operators o_1, ..., o_k. A tuple enters with size s_0
and has size s_j after o_j; the last size s_k is 0 because the output leaves
the system. Operator o_j takes time t_j per tuple. The progress chart of the
query is the polyline through the points (T_j, s_j) with T_j = t_1 + ... + t_j.
Chain gives each operator the slope (the size lost per unit of time) of the
segment of the lower envelope of the chart that covers it, and at each step
runs the waiting tuple whose next operator has the highest priority, the
oldest tuple first on a tie.

The simulator uses unit times (t_j = 1), one operator step per time unit and
one processor. lower_envelope accepts any positive times.
"""

from fractions import Fraction
from typing import Sequence


def check_chart(sizes: Sequence) -> list:
    sizes = [Fraction(s) for s in sizes]
    if len(sizes) < 2 or sizes[-1] != 0:
        raise ValueError("a chart needs at least one operator and must end at size 0")
    if any(b > a for a, b in zip(sizes, sizes[1:])) or sizes[0] <= 0:
        raise ValueError("sizes must be positive at the start and must not grow")
    return sizes


def lower_envelope(sizes: Sequence, times: Sequence | None = None) -> list:
    """The Chain priority of each operator o_1..o_k: the slope of its envelope segment."""
    sizes = check_chart(sizes)
    k = len(sizes) - 1
    times = [1] * k if times is None else list(times)
    if len(times) != k or any(t <= 0 for t in times):
        raise ValueError("one positive time per operator")
    T = [0]
    for t in times:
        T.append(T[-1] + t)
    prio = [None] * k
    i = 0  # @line L1
    while i < k:  # @line L2
        # the point after i with the steepest descent from point i; the farthest on a tie
        best, best_slope = None, None
        for j in range(i + 1, k + 1):  # @line L3
            slope = Fraction(sizes[i] - sizes[j]) / (T[j] - T[i])
            if best is None or slope >= best_slope:
                best, best_slope = j, slope
        for j in range(i, best):  # @line L4
            prio[j] = best_slope
        i = best  # @line L5
    return prio


class Tuple_:
    __slots__ = ("query", "arrival", "seq", "pos")

    def __init__(self, query: int, arrival: int, seq: int):
        self.query, self.arrival, self.seq, self.pos = query, arrival, seq, 0


def simulate(charts: Sequence[Sequence], arrivals: Sequence[tuple[int, int]], horizon: int, policy: str = "chain"):
    """Run one operator step per time unit for horizon units.

    charts[q] are the sizes s_0..s_k of query q, with unit operator times.
    arrivals are (time, q) pairs: a tuple of query q enters before step time.
    Returns the memory (the total size of the waiting tuples) after each step.
    """
    charts = [check_chart(c) for c in charts]
    prios = [lower_envelope(c) for c in charts]
    by_time: dict[int, list[int]] = {}
    for t, q in arrivals:
        by_time.setdefault(t, []).append(q)
    waiting: list[Tuple_] = []
    memory = Fraction(0)
    trace = []
    seq = 0
    for now in range(horizon):
        for q in by_time.get(now, []):  # @line L6
            waiting.append(Tuple_(q, now, seq))
            seq += 1
            memory += charts[q][0]
        if waiting:  # @line L7
            if policy == "chain":
                key = lambda x: (-prios[x.query][x.pos], x.arrival, x.seq)
            elif policy == "fifo":
                key = lambda x: (x.arrival, x.seq)
            elif policy == "greedy":  # the largest drop of the next step only
                key = lambda x: (charts[x.query][x.pos + 1] - charts[x.query][x.pos], x.arrival, x.seq)
            else:
                raise ValueError("unknown policy")
            x = min(waiting, key=key)  # @line L8
            c = charts[x.query]
            memory -= c[x.pos] - c[x.pos + 1]  # @line L9
            x.pos += 1
            if x.pos == len(c) - 1:  # @line L10
                waiting.remove(x)  # the output leaves the system
        trace.append(memory)
    return trace


def best_memory(charts: Sequence[Sequence], arrivals: Sequence[tuple[int, int]], horizon: int):
    """The least memory after each step over all schedules, by search over states.

    A state is the position of every tuple in its chain. Idling never helps,
    because sizes do not grow, so every step runs some waiting tuple."""
    charts = [check_chart(c) for c in charts]
    tuples = sorted((t, q) for t, q in arrivals)
    n = len(tuples)
    states = {tuple([0] * n)}
    out = []
    for now in range(horizon):
        here = [i for i, (t, _) in enumerate(tuples) if t <= now]
        nxt = set()
        for st in states:
            moves = [i for i in here if st[i] < len(charts[tuples[i][1]]) - 1]
            if not moves:
                nxt.add(st)
            for i in moves:
                s2 = list(st)
                s2[i] += 1
                nxt.add(tuple(s2))
        states = nxt
        out.append(min(sum(charts[tuples[i][1]][st[i]] for i in here) for st in states))
    return out
