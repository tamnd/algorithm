# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/junction-tree/. The authors are listed in prov/1CEHTH.jsonl.

"""A junction tree (clique tree) of a graph, built from an elimination order.

The graph has vertices 0 .. n-1 and a list of edges. The build triangulates the
graph along the order, keeps the maximal cliques of the filled graph, and joins
them by a maximum weight spanning tree of the clique graph, where the weight of
a pair of cliques is the size of their intersection (Jensen and Jensen 1994).
The result has the running intersection property: for each vertex, the cliques
that hold it form a connected subtree. Build time O(n^3 + k^2 log k) for k
cliques (k <= n) in this simple form.
"""

from itertools import combinations
from typing import Dict, FrozenSet, Iterable, List, Optional, Sequence, Set, Tuple

Edge = Tuple[int, int]


class JunctionTree:
    def __init__(self) -> None:
        self.n = 0
        self.cliques: List[FrozenSet[int]] = []
        self.tree_edges: List[Tuple[int, int]] = []

    @classmethod
    def build(cls, n: int, edges: Iterable[Edge], order: Sequence[int]) -> "JunctionTree":
        """Build the junction tree of the graph triangulated along the order."""
        if sorted(order) != list(range(n)):
            raise ValueError("the order must hold each vertex once")
        jt = cls()
        jt.n = n
        adj: Dict[int, Set[int]] = {v: set() for v in range(n)}  # @line L1
        for u, v in edges:
            if u != v:
                adj[u].add(v)
                adj[v].add(u)
        for v in order:  # @line L2
            bag = frozenset(adj[v] | {v})  # @line L3
            nb = adj.pop(v)  # @line L4
            for a, b in combinations(nb, 2):
                adj[a].add(b)
                adj[b].add(a)
            for a in nb:
                adj[a].discard(v)
            if not any(bag <= c for c in jt.cliques):  # @line L5
                jt.cliques.append(bag)
        k = len(jt.cliques)
        pairs = [(len(jt.cliques[i] & jt.cliques[j]), i, j) for i, j in combinations(range(k), 2)]  # @line L6
        pairs.sort(key=lambda t: (-t[0], t[1], t[2]))  # @line L7
        parent = list(range(k))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for _, i, j in pairs:  # @line L8
            ri, rj = find(i), find(j)
            if ri != rj:  # @line L9
                parent[ri] = rj
                jt.tree_edges.append((i, j))  # @line L10
        return jt

    def separators(self) -> List[FrozenSet[int]]:
        """The separator of each tree edge, in the order of tree_edges."""
        return [self.cliques[i] & self.cliques[j] for i, j in self.tree_edges]

    def width(self) -> int:
        return max((len(c) for c in self.cliques), default=1) - 1

    def neighbours(self) -> Dict[int, List[int]]:
        nb: Dict[int, List[int]] = {i: [] for i in range(len(self.cliques))}
        for i, j in self.tree_edges:
            nb[i].append(j)
            nb[j].append(i)
        return nb

    def find_clique(self, scope: Iterable[int]) -> Optional[int]:
        """The index of a smallest clique that holds the whole scope, or None."""
        s = frozenset(scope)
        best = None
        for i, c in enumerate(self.cliques):
            if s <= c and (best is None or len(c) < len(self.cliques[best])):
                best = i
        return best

    def path(self, a: int, b: int) -> List[int]:
        """The cliques on the tree path from a to b."""
        nb = self.neighbours()
        prev = {a: a}
        stack = [a]
        while stack:
            x = stack.pop()
            for y in nb[x]:
                if y not in prev:
                    prev[y] = x
                    stack.append(y)
        out = [b]
        while out[-1] != a:
            out.append(prev[out[-1]])
        return out[::-1]

    def check_invariant(self, edges: Iterable[Edge] = ()) -> None:
        """Raise AssertionError unless this is a junction tree that covers the edges."""
        k = len(self.cliques)
        assert len(self.tree_edges) == max(k - 1, 0)
        if k:
            seen, stack, nb = {0}, [0], self.neighbours()
            while stack:
                x = stack.pop()
                for y in nb[x]:
                    if y not in seen:
                        seen.add(y)
                        stack.append(y)
            assert len(seen) == k, "the clique tree is not connected"
        for v in range(self.n):
            assert any(v in c for c in self.cliques), "a vertex is in no clique"
        for u, v in edges:
            assert any(u in c and v in c for c in self.cliques), "an edge is in no clique"
        for a, b in combinations(range(k), 2):
            common = self.cliques[a] & self.cliques[b]
            for c in self.path(a, b):
                assert common <= self.cliques[c], "running intersection property fails"
