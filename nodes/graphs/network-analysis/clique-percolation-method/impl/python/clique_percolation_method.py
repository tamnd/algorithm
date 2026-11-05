# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clique-percolation-method/. The authors are listed in prov/8MV6VW.jsonl.


def k_cliques(adj: list[list[int]], k: int) -> list[tuple[int, ...]]:
    """List every clique with exactly k vertices once, as an increasing tuple."""
    nbrs = [set(a) for a in adj]
    out: list[tuple[int, ...]] = []
    stack: list[tuple[tuple[int, ...], list[int]]] = []
    for v in range(len(adj)):
        stack.append(((v,), sorted(w for w in nbrs[v] if w > v)))
        while stack:
            clique, cand = stack.pop()
            if len(clique) == k:
                out.append(clique)
                continue
            for idx, w in enumerate(cand):
                rest = [x for x in cand[idx + 1:] if x in nbrs[w]]
                if len(clique) + 1 + len(rest) >= k:
                    stack.append((clique + (w,), rest))
    return out


def clique_percolation_method(adj: list[list[int]], k: int) -> list[frozenset[int]]:
    """Return the k-clique communities of a simple undirected graph.

    The vertices are 0 .. n-1 and adj[v] lists the neighbours of v; each edge is
    in both lists. Two k-cliques are adjacent when they share k - 1 vertices, and
    a community is the union of the k-cliques of one class of this relation. The
    communities may overlap; vertices in no k-clique are in none. The result is
    sorted by the least vertex of each community. Requires k >= 2.
    """
    if k < 2:
        raise ValueError("k must be at least 2")
    cliques = k_cliques(adj, k)  # @line L1
    parent = list(range(len(cliques)))  # @line L2: a union-find forest

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    first: dict[tuple[int, ...], int] = {}  # @line L3
    for c, members in enumerate(cliques):  # @line L4
        for x in members:  # @line L5
            face = tuple(y for y in members if y != x)  # @line L6
            if face in first:  # @line L7
                ra, rb = find(c), find(first[face])
                if ra != rb:
                    parent[ra] = rb
            else:
                first[face] = c
    groups: dict[int, set[int]] = {}  # @line L8
    for c, members in enumerate(cliques):
        groups.setdefault(find(c), set()).update(members)
    return sorted((frozenset(g) for g in groups.values()), key=min)  # @line L9
