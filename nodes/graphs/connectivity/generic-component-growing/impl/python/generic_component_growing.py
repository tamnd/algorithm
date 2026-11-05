# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-component-growing/. The authors are listed in prov/753N4R.jsonl.

from typing import Callable

Pick = Callable[[int], int]


def _last(size: int) -> int:
    return size - 1


def grow(
    adj: list[list[int]],
    s: int,
    k: int,
    comp: list[int | None],
    parent: list[int | None],
    pick: Pick = _last,
) -> None:
    """Give the label k to every vertex that is reachable from s and has no label yet.

    Precondition: adj is the adjacency lists of an undirected graph on 0 .. n-1, with
    each edge {u, v} in the lists of both ends; parallel edges and loops are allowed.
    comp[s] is None. pick(size) returns any index in range(size): it chooses which
    vertex of the frontier is scanned next. Sets parent[v] for each new vertex except s.
    Time O(n_s + m_s) for the component of s if pick is O(1); extra space O(n_s).
    """
    nxt: dict[int, int] = {s: 0}
    comp[s] = k  # @line L1
    frontier = [s]  # @line L2
    while frontier:  # @line L3
        j = pick(len(frontier))  # @line L4
        u = frontier[j]
        if nxt[u] == len(adj[u]):  # @line L5
            frontier[j] = frontier[-1]  # swap with the last item, then pop: O(1)
            frontier.pop()
            continue
        v = adj[u][nxt[u]]  # @line L6
        nxt[u] += 1
        if comp[v] is None:  # @line L7
            comp[v] = k  # @line L8
            parent[v] = u
            nxt[v] = 0
            frontier.append(v)


def components(
    adj: list[list[int]], pick: Pick = _last
) -> tuple[list[int | None], list[int | None], int]:
    """Label the connected components of an undirected graph.

    Precondition: as for grow. Returns (comp, parent, k): comp[v] in 0 .. k-1 is the
    label of the component of v, labels are given in the order of the smallest vertex
    of each component, and the parent pointers form a spanning forest whose roots are
    the smallest vertices of the components. Time O(n + m), extra space O(n).
    """
    n = len(adj)
    comp: list[int | None] = [None] * n  # @line L9
    parent: list[int | None] = [None] * n
    k = 0
    for s in range(n):  # @line L10
        if comp[s] is None:  # @line L11
            grow(adj, s, k, comp, parent, pick)
            k += 1
    return comp, parent, k  # @line L12
