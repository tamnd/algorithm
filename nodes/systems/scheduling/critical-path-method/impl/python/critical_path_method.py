# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/critical-path-method/. The authors are listed in prov/EQ6EWJ.jsonl.

from dataclasses import dataclass
from typing import Sequence


@dataclass
class CpmResult:
    length: int  # the least project duration T
    es: list[int]  # earliest start
    ef: list[int]  # earliest finish
    ls: list[int]  # latest start that does not delay the project
    lf: list[int]  # latest finish
    total_float: list[int]  # ls - es
    free_float: list[int]  # delay that does not move any successor's earliest start
    critical_path: list[int]  # one longest chain of activities, first to last


def topological_order(n: int, succ: Sequence[Sequence[int]]) -> list[int]:
    """Kahn's algorithm. Raise ValueError if the precedence graph has a cycle."""
    indeg = [0] * n
    for i in range(n):
        for j in succ[i]:
            indeg[j] += 1
    stack = [i for i in range(n - 1, -1, -1) if indeg[i] == 0]
    order = []
    while stack:
        i = stack.pop()
        order.append(i)
        for j in succ[i]:
            indeg[j] -= 1
            if indeg[j] == 0:
                stack.append(j)
    if len(order) != n:
        raise ValueError("the precedence graph has a cycle")
    return order


def critical_path_method(p: Sequence[int], arcs: Sequence[tuple[int, int]]) -> CpmResult:
    """The critical path method on an activity-on-node network.

    Activity j takes p[j] >= 0 time units; an arc (i, j) means that j starts
    only after i finishes. A forward pass in topological order gives the
    earliest times, a backward pass gives the latest times for the least
    project duration. Cost: O(n + m) time and space for n activities and m arcs.
    """
    n = len(p)
    if any(x < 0 for x in p):
        raise ValueError("durations must be nonnegative")
    succ: list[list[int]] = [[] for _ in range(n)]
    pred: list[list[int]] = [[] for _ in range(n)]
    for i, j in arcs:
        succ[i].append(j)
        pred[j].append(i)
    order = topological_order(n, succ)  # @line L1

    es = [0] * n
    for j in order:  # forward pass
        es[j] = max((es[i] + p[i] for i in pred[j]), default=0)  # @line L2
    ef = [es[j] + p[j] for j in range(n)]
    length = max(ef, default=0)  # @line L3

    lf = [length] * n
    for i in reversed(order):  # backward pass
        lf[i] = min((lf[j] - p[j] for j in succ[i]), default=length)  # @line L4
    ls = [lf[j] - p[j] for j in range(n)]

    total_float = [ls[j] - es[j] for j in range(n)]  # @line L5
    free_float = [min((es[k] for k in succ[j]), default=length) - ef[j] for j in range(n)]  # @line L6

    path: list[int] = []
    if n:
        # start at a critical activity with no critical predecessor, follow tight arcs
        j = next(j for j in order if total_float[j] == 0 and es[j] == 0)  # @line L7
        path.append(j)
        while ef[j] < length:
            j = next(k for k in succ[j] if total_float[k] == 0 and es[k] == ef[j])
            path.append(j)
    return CpmResult(length, es, ef, ls, lf, total_float, free_float, path)  # @line L8
