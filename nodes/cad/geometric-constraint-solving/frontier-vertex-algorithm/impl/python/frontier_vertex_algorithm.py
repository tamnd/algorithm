# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frontier-vertex-algorithm/. The authors are listed in prov/HMKXPX.jsonl.

"""The Frontier vertex algorithm for a DR-plan of a weighted constraint graph.

Entities are the vertices 0..n-1, each with weight vertex_weight (its degrees of freedom), and constraints are the
edges, each with weight edge_weight. A set X is dense when rho(X) = w(E(X)) - w(X) >= -D. The default weights are
points and distances in the plane: 2, 1 and D = 3.

The planner first makes every constraint a cluster. Then it repeats: find a minimal dense set X of the simplified
graph that does not lie inside one cluster, by maximum closure computations with network flow; record the cluster
that X stands for; and simplify, which keeps the frontier vertices of the cluster (those with constraints to the
outside) and replaces the rest by one core vertex of weight D joined to each frontier vertex f by an edge of
weight w(f)."""

from collections import deque
from typing import Optional, Sequence

Edge = tuple[int, int]
BIG = 1 << 60


def max_flow(cap: list[dict[int, int]], s: int, t: int) -> int:
    """Edmonds-Karp on a residual graph given as a list of dicts; cap is changed into the residual graph."""
    flow = 0
    while True:
        parent = {s: s}
        queue = deque([s])
        while queue and t not in parent:
            x = queue.popleft()
            for y, c in cap[x].items():
                if c > 0 and y not in parent:
                    parent[y] = x
                    queue.append(y)
        if t not in parent:
            return flow
        push, y = BIG, t
        while y != s:
            push = min(push, cap[parent[y]][y])
            y = parent[y]
        y = t
        while y != s:
            x = parent[y]
            cap[x][y] -= push
            cap[y][x] = cap[y].get(x, 0) + push
            y = x
        flow += push


class FrontierPlanner:
    def __init__(self, n: int, edges: Sequence[Edge], vertex_weight: int = 2, edge_weight: int = 1,
                 D: int = 3) -> None:
        self.n, self.D = n, D
        self.vertex_weight, self.edge_weight = vertex_weight, edge_weight
        self.w: dict[int, int] = {v: vertex_weight for v in range(n)}
        self.adj: dict[int, dict[int, int]] = {v: {} for v in range(n)}
        for u, v in edges:
            if u == v:
                raise ValueError("loop")
            self.adj[u][v] = self.adj[u].get(v, 0) + edge_weight
            self.adj[v][u] = self.adj[v].get(u, 0) + edge_weight
        self.edges = list(edges)
        self.clusters: list[dict] = []
        self.core_of: dict[int, int] = {}
        self.next_id = n

    # ----- the simplified graph -----

    def orig(self, x: int) -> frozenset:
        return frozenset([x]) if x < self.n else self.clusters[self.core_of[x]]["vertices"]

    def density(self, X: set) -> int:
        inside = sum(wt for x in X for y, wt in self.adj[x].items() if y in X) // 2
        return inside - sum(self.w[x] for x in X)

    def close(self, Z: set, Y: set) -> set:
        """Add the frontier of every core in Z; this never lowers the density."""
        Z = set(Z)
        for c in [x for x in Z if x >= self.n]:
            Z |= {f for f in self.adj[c] if f in Y}
        return Z

    def max_closure(self, Y: set, T: set) -> tuple[int, set]:
        """The largest density of a set Z with T <= Z <= Y, and such a set, by one minimum cut."""
        ys = sorted(Y)
        idx = {x: i + 2 for i, x in enumerate(ys)}
        es = [(x, y, wt) for x in ys for y, wt in self.adj[x].items() if y in Y and x < y]
        cap: list[dict[int, int]] = [dict() for _ in range(2 + len(ys) + len(es))]
        for k, (x, y, wt) in enumerate(es):
            e = 2 + len(ys) + k
            cap[0][e] = wt
            cap[e][idx[x]] = BIG
            cap[e][idx[y]] = BIG
        for x in ys:
            if x not in T:
                cap[idx[x]][1] = self.w[x]
        f = max_flow(cap, 0, 1)
        seen, queue = {0}, deque([0])
        while queue:
            a = queue.popleft()
            for b, c in cap[a].items():
                if c > 0 and b not in seen:
                    seen.add(b)
                    queue.append(b)
        Z = {x for x in ys if idx[x] in seen} | set(T)
        return sum(wt for _, _, wt in es) - f - sum(self.w[x] for x in T), Z

    def candidate_pairs(self, Y: set) -> list[tuple[int, int]]:
        """Pairs that every dense set not inside one cluster must contain one of: the two ends of a constraint
        that is not yet in a cluster, or two cores whose frontiers share a vertex."""
        pairs = set()
        for x in Y:
            nbrs = sorted(y for y in self.adj[x] if y in Y)
            if x < self.n:
                pairs |= {(x, y) for y in nbrs if y < self.n and x < y}
                cores = [y for y in nbrs if y >= self.n]
                pairs |= {(a, b) for i, a in enumerate(cores) for b in cores[i + 1:]}
        return sorted(pairs)

    def find_dense(self, Y: set) -> Optional[set]:
        for a, b in self.candidate_pairs(Y):  # @line L4
            value, Z = self.max_closure(Y, {a, b})  # @line L5
            if value >= -self.D:  # @line L5
                return self.close(Z, Y)
        return None

    def minimal(self, X: set) -> set:
        """Shrink a dense set to one that has no proper dense subset outside every cluster."""
        changed = True
        while changed:  # @line L7
            changed = False
            for c in sorted(x for x in X if x >= self.n):
                Y = set(X) - {c}
                Y = {y for y in Y if any(z in Y for z in self.adj[y])}
                Z = self.find_dense(Y)  # @line L8
                if Z is not None:
                    X, changed = Z, True  # @line L9
                    break
        return X

    def original_density(self, U: frozenset) -> int:
        inside = sum(self.edge_weight for u, v in self.edges if u in U and v in U)
        return inside - self.vertex_weight * len(U)

    def simplify(self, X: set) -> int:
        U = frozenset().union(*(self.orig(x) for x in X))  # @line L10
        rho = self.original_density(U)
        cores = {c for c in self.core_of if c in self.adj and self.orig(c) <= U}  # @line L11
        Xp = set(X) | cores
        children = sorted(self.core_of[c] for c in cores)
        covered = frozenset().union(*(self.clusters[i]["vertices"] for i in children))
        frontier = {x for x in Xp if any(y not in Xp for y in self.adj[x])}  # @line L12
        assert all(x < self.n for x in frontier)
        for x in Xp:
            for y in list(self.adj[x]):
                if y in Xp:
                    del self.adj[x][y]
        for x in Xp - frontier:  # @line L13
            for y in self.adj.pop(x):
                del self.adj[y][x]
            del self.w[x]
        c = self.next_id  # @line L14
        self.next_id += 1
        self.w[c] = self.D
        self.adj[c] = {}
        for f in frontier:
            self.adj[c][f] = self.adj[f][c] = self.w[f]  # @line L14
        self.core_of[c] = len(self.clusters)
        self.clusters.append({"vertices": U, "children": children, "leaves": sorted(U - covered),
                              "frontier": frozenset(frontier), "density": rho})  # @line L15
        return c

    # ----- the algorithm -----

    def run(self) -> list[dict]:
        for u, v in self.edges:  # @line L1
            if u in self.adj and v in self.adj[u]:
                self.simplify({u, v})  # @line L2
        while True:  # @line L3
            X = self.find_dense(set(self.adj))  # @line L4
            if X is None:
                break  # @line L6
            X = self.minimal(X)  # @line L7
            self.simplify(X)  # @line L10
        return self.clusters  # @line L16

    def roots(self) -> list[frozenset]:
        """The clusters that are not children of another cluster, and the vertices in no cluster."""
        live = [self.clusters[i]["vertices"] for c, i in self.core_of.items() if c in self.adj]
        covered = frozenset().union(*live) if live else frozenset()
        return live + [frozenset([v]) for v in range(self.n) if v not in covered]


def frontier_dr_plan(n: int, edges: Sequence[Edge], vertex_weight: int = 2, edge_weight: int = 1,
                     D: int = 3) -> tuple[list[dict], list[frozenset]]:
    """The clusters of the DR-plan, in the order made, and its roots."""
    planner = FrontierPlanner(n, edges, vertex_weight, edge_weight, D)
    clusters = planner.run()
    return clusters, planner.roots()
