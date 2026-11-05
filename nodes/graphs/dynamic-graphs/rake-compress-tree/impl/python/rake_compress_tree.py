# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rake-compress-tree/. The authors are listed in prov/0SFSXB.jsonl.

"""Rake-compress trees (RC-trees) built by randomized tree contraction.

The forest is contracted in rounds. In each round every leaf rakes into its
neighbor, every isolated vertex finalizes, and an independent set of degree-2
vertices chosen by coin flips compresses. Each removed vertex v becomes a
cluster C(v), a node of the RC-tree whose children are the clusters that met
at v. Every cluster is a connected set of edges with at most two boundary
vertices; a binary cluster stores the weight of the path between its two
boundary vertices. The RC-tree has O(log n) depth in expectation.

Queries walk up from the cluster of a vertex: connected(u, v) compares roots,
and path_weight(u, v) sums the weights on the tree path. Fully dynamic links
and cuts; this implementation rebuilds the contraction after each update in
O(n) expected time, where change propagation would take O(log n) expected
time on trees of bounded degree. The coins are a fixed function of the vertex,
the round and a seed, so the result does not depend on the update history.
"""


class Cluster:
    __slots__ = ("rep", "bound", "weight", "children", "parent")

    def __init__(self, rep: int | None, bound: tuple[int, ...], weight: int,
                 children: list["Cluster"]) -> None:
        self.rep = rep            # the vertex whose removal formed it; None for an edge
        self.bound = bound        # boundary vertices, at most two
        self.weight = weight      # for a binary cluster, the path weight between them
        self.children = children
        self.parent: Cluster | None = None
        for c in children:
            c.parent = self


def _coin(seed: int, v: int, rnd: int) -> int:
    x = (v * 0x9E3779B1 + rnd * 0x85EBCA77 + seed * 0xC2B2AE3D) & 0xFFFFFFFF
    x ^= x >> 16
    x = (x * 0x7FEB352D) & 0xFFFFFFFF
    x ^= x >> 15
    return x & 1


class RCForest:
    def __init__(self, n: int, seed: int = 1) -> None:
        self.n, self.seed = n, seed
        self.edges: dict[tuple[int, int], int] = {}
        self._build()

    @staticmethod
    def _key(u: int, v: int) -> tuple[int, int]:
        return (u, v) if u < v else (v, u)

    def link(self, u: int, v: int, w: int) -> None:
        if self.connected(u, v):
            raise ValueError("link would close a cycle")
        self.edges[self._key(u, v)] = w
        self._build()

    def cut(self, u: int, v: int) -> None:
        del self.edges[self._key(u, v)]
        self._build()

    def _build(self) -> None:
        n = self.n
        # nbr[v][x] is the binary cluster between v and x; unary[v] the clusters hanging at v.
        nbr: list[dict[int, Cluster]] = [dict() for _ in range(n)]
        unary: list[list[Cluster]] = [[] for _ in range(n)]
        for (a, b), w in self.edges.items():  # @line L1
            c = Cluster(None, (a, b), w, [])
            nbr[a][b] = c
            nbr[b][a] = c
        self.cluster: list[Cluster | None] = [None] * n
        self.round = [0] * n
        live = set(range(n))
        rnd = 0
        while live:  # @line L2
            rnd += 1
            final, rake, comp = [], [], []
            for v in live:
                d = len(nbr[v])
                if d == 0:
                    final.append(v)  # @line L3
                elif d == 1:
                    (u,) = nbr[v]
                    if len(nbr[u]) > 1 or v < u:
                        rake.append((v, u))  # @line L4
                elif d == 2:
                    a, b = nbr[v]
                    if (_coin(self.seed, v, rnd) and not _coin(self.seed, a, rnd)
                            and not _coin(self.seed, b, rnd)
                            and len(nbr[a]) > 1 and len(nbr[b]) > 1):
                        comp.append(v)  # @line L5
            for v in final:
                self._make(v, (), 0, unary[v], rnd)
                live.discard(v)
            for v, u in rake:
                c = nbr[v].pop(u)
                del nbr[u][v]
                k = self._make(v, (u,), 0, [c] + unary[v], rnd)  # @line L6
                unary[u].append(k)
                live.discard(v)
            for v in comp:
                (a, ca), (b, cb) = nbr[v].items()
                del nbr[a][v], nbr[b][v]
                nbr[v].clear()
                k = self._make(v, (a, b), ca.weight + cb.weight, [ca, cb] + unary[v], rnd)  # @line L7
                nbr[a][b] = k
                nbr[b][a] = k
                live.discard(v)
        self.rounds = rnd

    def _make(self, v: int, bound: tuple[int, ...], weight: int,
              children: list[Cluster], rnd: int) -> Cluster:
        k = Cluster(v, bound, weight, children)
        self.cluster[v] = k
        self.round[v] = rnd
        return k

    def _root(self, v: int) -> Cluster:
        c = self.cluster[v]
        while c.parent is not None:
            c = c.parent
        return c

    def connected(self, u: int, v: int) -> bool:
        return self._root(u) is self._root(v)  # @line L8

    def _climb(self, u: int) -> dict[int, tuple[Cluster, dict[int, int]]]:
        """For each cluster C(z) above u: the distances from u to z and the boundary."""
        c = self.cluster[u]
        # Distances from u to the boundary of C(u), through its binary children.
        dist = {u: 0}
        for ch in c.children:
            if len(ch.bound) == 2:
                other = ch.bound[0] if ch.bound[1] == u else ch.bound[1]
                dist[other] = ch.weight
        out = {c.rep: (c, dict(dist))}
        while c.parent is not None:  # @line L9
            p = c.parent
            z = p.rep
            dz = dist[z]
            nd = {z: dz}
            for x in p.bound:
                if x in dist:
                    nd[x] = dist[x]  # the path to x stays inside c
                else:
                    # the path goes through z, then along the binary child from z to x
                    for ch in p.children:
                        if len(ch.bound) == 2 and x in ch.bound and z in ch.bound:
                            nd[x] = dz + ch.weight
            dist, c = nd, p
            out[z] = (c, dict(dist))
        return out

    def path_weight(self, u: int, v: int) -> int | None:
        if not self.connected(u, v):
            return None
        up = self._climb(u)
        c = self.cluster[v]
        dv = self._climb(v)
        while c.rep not in up:  # @line L10
            c = c.parent
        z = c.rep
        return up[z][1][z] + dv[z][1][z]  # @line L11

    def depth(self) -> int:
        best = 0
        for v in range(self.n):
            d, c = 0, self.cluster[v]
            while c.parent is not None:
                c, d = c.parent, d + 1
            best = max(best, d)
        return best
