# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whatever-first-search/. The authors are listed in prov/4TP999.jsonl.

from collections import deque


def whatever_first_search(
    adj: list[list[int]], s: int, bag: str = "stack"
) -> tuple[list[int], list[int | None]]:
    """Run whatever-first search from s and return (order, parent).

    The graph has the vertices 0 .. n-1 and the adjacency lists adj. The bag holds
    pairs (p, v): "v was seen from p". With bag="queue" it is a FIFO queue and the
    search is breadth-first. With bag="stack" it is a LIFO stack, and each list is
    pushed in reverse so that the first neighbour is taken first; the search is then
    depth-first. order lists the marked vertices in the order they were marked, and
    parent[v] is the p of the pair that marked v, or None. Time O(n + m).
    """
    if bag not in ("stack", "queue"):
        raise ValueError("bag must be 'stack' or 'queue'")
    n = len(adj)
    marked = [False] * n  # @line L1
    parent: list[int | None] = [None] * n
    order: list[int] = []
    items: deque[tuple[int | None, int]] = deque([(None, s)])  # @line L2
    take = items.pop if bag == "stack" else items.popleft
    while items:  # @line L3
        p, v = take()  # @line L4
        if not marked[v]:  # @line L5
            marked[v] = True  # @line L6
            parent[v] = p
            order.append(v)
            nbrs = reversed(adj[v]) if bag == "stack" else adj[v]
            for w in nbrs:  # @line L7
                if not marked[w]:  # a pair for a marked w would be skipped at L5
                    items.append((v, w))
    return order, parent  # @line L8
