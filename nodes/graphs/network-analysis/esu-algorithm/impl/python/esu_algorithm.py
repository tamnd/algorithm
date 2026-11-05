# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/esu-algorithm/. The authors are listed in prov/EG33JY.jsonl.


def esu_algorithm(n: int, edges: list[tuple[int, int]], k: int) -> list[tuple[int, ...]]:
    """Return every connected induced subgraph of k vertices once, as a sorted tuple of vertices.

    The graph is undirected on the vertices 0 .. n-1; edges holds pairs (u, v),
    and loops and repeated pairs are ignored. The order of the output is the
    order of the ESU-tree: roots by increasing vertex, and inside one call the
    extension list is taken from the front. Requires k >= 1.
    Time O(n + m + k Δ s), where s counts the connected sets of at most k vertices.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    adj: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)
    nbrs = [sorted(a) for a in adj]
    out: list[tuple[int, ...]] = []

    def extend(sub: list[int], ext: list[int], closed: set[int], v: int) -> None:
        if len(sub) == k:  # @line L5
            out.append(tuple(sorted(sub)))  # @line L6
            return
        ext = ext[:]
        while ext:  # @line L7
            w = ext.pop(0)  # @line L8
            new = [u for u in nbrs[w] if u > v and u not in closed]  # @line L9
            closed_w = closed | set(nbrs[w])
            extend(sub + [w], ext + new, closed_w, v)  # @line L10

    for v in range(n):  # @line L1
        ext = [u for u in nbrs[v] if u > v]  # @line L2
        closed = {v} | adj[v]
        extend([v], ext, closed, v)  # @line L3
    return out  # @line L4
