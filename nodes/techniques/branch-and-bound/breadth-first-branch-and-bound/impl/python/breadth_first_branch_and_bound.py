# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breadth-first-branch-and-bound/. The authors are listed in prov/Z9RZB6.jsonl.

from collections import deque
from collections.abc import Callable, Iterable, Sequence
from typing import TypeVar

N = TypeVar("N")


def breadth_first_branch_and_bound(
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
    no leaf. Live nodes wait in a FIFO queue, so the tree is expanded level
    by level.
    """
    if stats is None:
        stats = {}
    stats.update(expanded=0, generated=1, max_live=1)
    z = float("-inf")  # @line L1
    best: N | None = None  # @line L1
    queue: deque[N] = deque([root])  # @line L2
    while queue:  # @line L3
        node = queue.popleft()  # @line L4
        if upper_bound(node) <= z:  # @line L5
            continue
        if is_leaf(node):  # @line L6
            v = value(node)
            if v > z:  # @line L7
                z, best = v, node
            continue  # @line L8
        stats["expanded"] += 1
        kept = [c for c in children(node) if upper_bound(c) > z]  # @line L9 @line L10
        stats["generated"] += len(kept)
        queue.extend(kept)  # @line L10
        stats["max_live"] = max(stats["max_live"], len(queue))
    return z, best  # @line L11


Item = tuple[float, float]  # (value, weight)
KNode = tuple[int, float, float, tuple[int, ...]]  # (level, weight, value, taken)


def knapsack(values: Sequence[float], weights: Sequence[float], capacity: float, stats: dict[str, int] | None = None) -> tuple[float, list[int]]:
    """0-1 knapsack by breadth-first branch and bound with the fractional bound.

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

    z, best = breadth_first_branch_and_bound((0, 0.0, 0.0, ()), kids, ub, lambda x: x[0] == n, lambda x: x[2], stats)
    assert best is not None
    return z, sorted(best[3])
