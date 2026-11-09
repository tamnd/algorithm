# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clarke-wright-savings/. The authors are listed in prov/BGTTNH.jsonl.

from typing import Sequence


def savings_list(dist: Sequence[Sequence[int]]) -> list[tuple[int, int, int]]:
    """All savings s(i, j) = c(0, i) + c(0, j) - c(i, j) for customers i < j.

    The list is sorted by saving, largest first, and then by (i, j).
    """
    n = len(dist) - 1
    s = [
        (dist[0][i] + dist[0][j] - dist[i][j], i, j)
        for i in range(1, n + 1)
        for j in range(i + 1, n + 1)
    ]
    s.sort(key=lambda t: (-t[0], t[1], t[2]))
    return s


def clarke_wright_savings(
    dist: Sequence[Sequence[int]],
    demand: Sequence[int],
    capacity: int,
    merges: list[tuple[int, int, int]] | None = None,
) -> list[list[int]]:
    """Parallel Clarke-Wright savings heuristic for the capacitated VRP.

    City 0 is the depot and cities 1..n are customers. dist is a symmetric
    cost matrix of size (n + 1) by (n + 1). demand[i] is the demand of
    customer i (demand[0] is ignored), and 0 <= demand[i] <= capacity.

    Returns a list of routes. Each route lists its customers in visiting
    order; the vehicle starts and ends at the depot. Two routes are merged
    only when the saving is positive. If `merges` is a list, each applied
    merge is appended to it as (saving, i, j).

    Cost: O(n^2 log n) time for the sort and O(n^2) space for the savings.
    """
    n = len(dist) - 1
    if any(not 0 <= demand[i] <= capacity for i in range(1, n + 1)):
        raise ValueError("every demand must be between 0 and the capacity")
    route_of = list(range(n + 1))  # @line L1
    routes: dict[int, list[int]] = {i: [i] for i in range(1, n + 1)}
    load = {i: demand[i] for i in range(1, n + 1)}
    for s, i, j in savings_list(dist):  # @line L2
        if s <= 0:  # @line L3
            break
        ri, rj = route_of[i], route_of[j]
        if ri == rj:  # @line L4
            continue
        a, b = routes[ri], routes[rj]
        if i not in (a[0], a[-1]) or j not in (b[0], b[-1]):  # @line L5
            continue
        if load[ri] + load[rj] > capacity:  # @line L6
            continue
        if a[-1] != i:  # @line L7
            a.reverse()
        if b[0] != j:
            b.reverse()
        a.extend(b)  # @line L8
        load[ri] += load[rj]
        for c in b:
            route_of[c] = ri
        del routes[rj], load[rj]
        if merges is not None:
            merges.append((s, i, j))
    return [routes[k] for k in sorted(routes)]  # @line L9


def routes_cost(dist: Sequence[Sequence[int]], routes: Sequence[Sequence[int]]) -> int:
    """Total cost of the routes, each from the depot and back."""
    total = 0
    for r in routes:
        path = [0, *r, 0]
        total += sum(dist[path[t]][path[t + 1]] for t in range(len(path) - 1))
    return total
