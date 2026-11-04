# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-first-branch-and-bound/. The authors are listed in prov/0SPYHN.jsonl.

import heapq
import itertools
from collections.abc import Callable, Iterable, Sequence
from typing import TypeVar

N = TypeVar("N")


def best_first_branch_and_bound(
    root: N,
    children: Callable[[N], Iterable[N]],
    upper_bound: Callable[[N], float],
    is_leaf: Callable[[N], bool],
    value: Callable[[N], float],
    stats: dict[str, int] | None = None,
) -> tuple[float, N | None]:
    """Maximise value over the leaves of the tree below root.

    children(n) yields the feasible children of an inner node in the order
    to try them. upper_bound(n) must be at least value(x) for every leaf x
    below n. Returns (best value, best leaf), or (-inf, None) if the tree has
    no leaf. Live nodes wait in a binary heap keyed by their bound; among
    nodes with equal bounds, the one generated first is taken first.
    """
    if stats is None:
        stats = {}
    stats.update(expanded=0, generated=1, max_live=1)
    z = float("-inf")  # @line L1
    best: N | None = None  # @line L1
    tick = itertools.count()
    heap: list[tuple[float, int, N]] = [(-upper_bound(root), next(tick), root)]  # @line L2
    while heap:  # @line L3
        neg_ub, _, node = heapq.heappop(heap)  # @line L4
        if -neg_ub <= z:  # @line L5
            break
        if is_leaf(node):  # @line L6
            v = value(node)
            if v > z:  # @line L7
                z, best = v, node
            continue  # @line L8
        stats["expanded"] += 1
        for child in children(node):  # @line L9
            b = upper_bound(child)
            if b > z:  # @line L10
                heapq.heappush(heap, (-b, next(tick), child))
                stats["generated"] += 1
        stats["max_live"] = max(stats["max_live"], len(heap))
    return z, best  # @line L11


Item = tuple[float, float]  # (value, weight)
KNode = tuple[int, float, float, tuple[int, ...]]  # (level, weight, value, taken)


def knapsack(values: Sequence[float], weights: Sequence[float], capacity: float, stats: dict[str, int] | None = None) -> tuple[float, list[int]]:
    """0-1 knapsack by best-first branch and bound with the fractional bound.

    Returns the best value and the sorted list of chosen item indices.
    Items with weight 0 are allowed; weights and values must be nonnegative.
    """
    n = len(values)
    order = sorted(range(n), key=lambda i: (-(values[i] / weights[i]) if weights[i] > 0 else float("-inf"), i))

    def ub(node: KNode) -> float:
        k, w, v, _ = node
        room = capacity - w
        for j in order[k:]:
            if weights[j] <= room:
                room -= weights[j]
                v += values[j]
            else:
                return v + values[j] * room / weights[j]
        return v

    def kids(node: KNode) -> list[KNode]:
        k, w, v, taken = node
        j = order[k]
        out: list[KNode] = []
        if w + weights[j] <= capacity:
            out.append((k + 1, w + weights[j], v + values[j], taken + (j,)))
        out.append((k + 1, w, v, taken))
        return out

    z, best = best_first_branch_and_bound((0, 0.0, 0.0, ()), kids, ub, lambda x: x[0] == n, lambda x: x[2], stats)
    assert best is not None
    return z, sorted(best[3])
