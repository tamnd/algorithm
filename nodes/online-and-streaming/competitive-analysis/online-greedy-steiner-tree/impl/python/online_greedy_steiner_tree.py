# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-greedy-steiner-tree/. The authors are listed in prov/HET07A.jsonl.

import heapq
from typing import Dict, Hashable, Iterable, List, Set, Tuple

Vertex = Hashable
Graph = Dict[Vertex, Dict[Vertex, float]]
Edge = Tuple[Vertex, Vertex]


class OnlineGreedySteiner:
    """The online greedy Steiner tree rule on an undirected graph with nonnegative weights.

    graph[u][v] is the weight of the edge {u, v}; it must equal graph[v][u].
    Call add(t) for each terminal, in the order of arrival. The rule connects t to the
    current tree by a shortest path to the nearest vertex of the tree, and buys that path.
    """

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.vertices: Set[Vertex] = set()  # @line L1
        self.edges: List[Edge] = []
        self.cost = 0  # @line L2

    def add(self, t: Vertex) -> float:
        """Connect terminal t and return the cost of this step."""
        if t not in self.graph:
            raise KeyError(t)
        if not self.vertices or t in self.vertices:  # @line L4
            self.vertices.add(t)
            return 0
        dist, parent, hit = self._nearest_tree_vertex(t)  # @line L5
        step = dist
        y = hit
        while y != t:  # @line L6
            p = parent[y]
            self.edges.append((p, y))
            self.vertices.add(p)
            y = p
        self.cost += step  # @line L7
        return step

    def _nearest_tree_vertex(self, t: Vertex):
        """Dijkstra from t until the first vertex of the tree is settled."""
        dist = {t: 0}
        parent: Dict[Vertex, Vertex] = {}
        heap = [(0, 0, t)]
        order = 1
        done: Set[Vertex] = set()
        while heap:
            d, _, u = heapq.heappop(heap)
            if u in done:
                continue
            done.add(u)
            if u in self.vertices:
                return d, parent, u
            for v, wt in self.graph[u].items():
                if wt < 0:
                    raise ValueError("edge weights must be nonnegative")
                nd = d + wt
                if v not in dist or nd < dist[v]:
                    dist[v] = nd
                    parent[v] = u
                    heapq.heappush(heap, (nd, order, v))
                    order += 1
        raise ValueError("the terminal cannot reach the tree")


def online_greedy_steiner_tree(graph: Graph, terminals: Iterable[Vertex]) -> Tuple[float, List[Edge], List[float]]:
    """Serve the terminals online with the greedy rule.

    Returns (total cost, bought edges, cost of each step). Each step runs one Dijkstra
    search, so k terminals take O(k (n + e) log n) time on n vertices and e edges.
    """
    alg = OnlineGreedySteiner(graph)
    steps = []
    for t in terminals:  # @line L3
        steps.append(alg.add(t))
    return alg.cost, alg.edges, steps  # @line L8
