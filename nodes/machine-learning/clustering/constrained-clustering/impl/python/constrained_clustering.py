# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constrained-clustering/. The authors are listed in prov/PBR52S.jsonl.

"""Feasibility of must-link (ML) and cannot-link (CL) constraints for a
clustering into exactly k nonempty clusters (Davidson and Ravi 2005).

ML constraints alone are always feasible when the number of ML components
is at least k: take the transitive closure with a disjoint-set forest.
With CL constraints the question is k-coloring of the graph of CL edges
between ML components, which is NP-complete for k >= 3; here it is solved
by backtracking, and for k = 2 by a bipartiteness test.
"""


class DisjointSets:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[max(ra, rb)] = min(ra, rb)


def ml_components(n, ml):
    """Component index of each point under the transitive closure of ML."""
    ds = DisjointSets(n)
    for a, b in ml:
        ds.union(a, b)
    roots = sorted({ds.find(i) for i in range(n)})
    index = {r: t for t, r in enumerate(roots)}
    return [index[ds.find(i)] for i in range(n)], len(roots)


def _color(m, adj, k):
    """k-color a graph with m vertices by backtracking; None if impossible."""
    order = sorted(range(m), key=lambda v: (-len(adj[v]), v))
    color = [-1] * m

    def place(pos, used):
        if pos == m:
            return True
        v = order[pos]
        for c in range(min(k, used + 1)):  # a new color only as the next one
            if all(color[u] != c for u in adj[v]):
                color[v] = c
                if place(pos + 1, max(used, c + 1)):
                    return True
                color[v] = -1
        return False

    return color if place(0, 0) else None


def _two_color(m, adj):
    """Bipartiteness test by breadth-first search."""
    color = [-1] * m
    for s in range(m):
        if color[s] != -1:
            continue
        color[s] = 0
        queue = [s]
        for v in queue:
            for u in adj[v]:
                if color[u] == -1:
                    color[u] = 1 - color[v]
                    queue.append(u)
                elif color[u] == color[v]:
                    return None
    return color


def feasible(n, ml, cl, k):
    """Return labels in range(k) with every label used, every ML pair
    together and every CL pair apart; or None if no such labels exist."""
    comp, m = ml_components(n, ml)  # @line L1
    if m < k:  # @line L2
        return None
    adj = [set() for _ in range(m)]
    for a, b in cl:
        if comp[a] == comp[b]:  # @line L3
            return None
        adj[comp[a]].add(comp[b])
        adj[comp[b]].add(comp[a])
    color = _two_color(m, adj) if k == 2 else _color(m, adj, k)  # @line L4
    if color is None:
        return None
    # make every label used: move a component out of a class with two or more
    for c in range(k):  # @line L5
        if c not in color:
            counts = {}
            for v in range(m):
                counts[color[v]] = counts.get(color[v], 0) + 1
            v = next(v for v in range(m) if counts[color[v]] >= 2)
            color[v] = c
    return [color[comp[i]] for i in range(n)]


def satisfies(labels, ml, cl):
    return all(labels[a] == labels[b] for a, b in ml) and all(labels[a] != labels[b] for a, b in cl)
