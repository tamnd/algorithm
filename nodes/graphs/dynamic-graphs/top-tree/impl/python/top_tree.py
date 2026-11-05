# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/top-tree/. The authors are listed in prov/YS9H4Q.jsonl.

"""Top trees built by contraction around an exposed pair of vertices.

A cluster is a connected set of edges with at most two boundary vertices.
Every cluster above the edges is the merge of exactly two clusters that share
a vertex: a compress joins two path clusters (a, c) and (c, b) at a vertex c
of degree 2 into (a, b), and a rake joins a point cluster at c onto another
cluster at c. The root of a top tree for expose(u, v) has the boundary
{u, v}, so its path value is the aggregate of the path from u to v.

Clusters hold user information combined by two functions, here the path sum,
the path maximum and the total weight. This implementation builds the top
tree of the exposed tree from scratch on each query, in O(size of the tree)
expected time, and keeps the forest as an edge set; a self-adjusting or
balanced top tree reaches O(log n) per operation.
"""

from dataclasses import dataclass, field
from typing import Optional

NEG = float("-inf")


@dataclass
class Cluster:
    bound: tuple[int, ...]       # boundary vertices, at most two
    psum: int = 0                # path sum between the two boundary vertices
    pmax: float = NEG            # path maximum between them
    total: int = 0               # sum of all edge weights in the cluster
    kind: str = "edge"           # "edge", "compress", "rake" or "empty"
    children: list["Cluster"] = field(default_factory=list)


def _compress(a: Cluster, b: Cluster, c: int) -> Cluster:
    """Join the path clusters (x, c) and (c, y) into (x, y)."""
    x = a.bound[0] if a.bound[1] == c else a.bound[1]
    y = b.bound[0] if b.bound[1] == c else b.bound[1]
    return Cluster((x, y), a.psum + b.psum, max(a.pmax, b.pmax),
                   a.total + b.total, "compress", [a, b])


def _rake(point: Cluster, onto: Cluster, bound: tuple[int, ...]) -> Cluster:
    """Join a point cluster onto another cluster at a common vertex."""
    return Cluster(bound, onto.psum, onto.pmax, point.total + onto.total, "rake", [point, onto])


def _coin(seed: int, v: int, rnd: int) -> int:
    x = (v * 0x9E3779B1 + rnd * 0x85EBCA77 + seed * 0xC2B2AE3D) & 0xFFFFFFFF
    x ^= x >> 16
    x = (x * 0x7FEB352D) & 0xFFFFFFFF
    x ^= x >> 15
    return x & 1


class TopTreeForest:
    def __init__(self, n: int, seed: int = 1) -> None:
        self.n, self.seed = n, seed
        self.adj: list[dict[int, int]] = [dict() for _ in range(n)]

    def _component(self, u: int) -> list[int]:
        seen, st = {u}, [u]
        while st:
            x = st.pop()
            for y in self.adj[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        return list(seen)

    def connected(self, u: int, v: int) -> bool:
        return v in set(self._component(u))

    def link(self, u: int, v: int, w: int) -> None:
        if self.connected(u, v):
            raise ValueError("link would close a cycle")
        self.adj[u][v] = w
        self.adj[v][u] = w

    def cut(self, u: int, v: int) -> None:
        del self.adj[u][v]
        del self.adj[v][u]

    def expose(self, u: int, v: int) -> Optional[Cluster]:
        """The root of a top tree of the tree of u with external vertices u and v."""
        comp = self._component(u)
        if v not in set(comp):
            return None
        ext = {u, v}
        nbr: dict[int, dict[int, Cluster]] = {x: {} for x in comp}
        point: dict[int, Optional[Cluster]] = {x: None for x in comp}
        for x in comp:  # @line L1
            for y, w in self.adj[x].items():
                if x < y:
                    c = Cluster((x, y), w, w, w)
                    nbr[x][y] = c
                    nbr[y][x] = c
        live = set(comp)
        rnd = 0
        while len(live) > len(ext):  # @line L2
            rnd += 1
            rake, comp_set = [], []
            for x in live:
                if x in ext:
                    continue
                d = len(nbr[x])
                if d == 1:
                    (y,) = nbr[x]
                    if y in ext or len(nbr[y]) > 1 or x < y:
                        rake.append(x)  # @line L3
                elif d == 2:
                    a, b = nbr[x]
                    if (_coin(self.seed, x, rnd) and not _coin(self.seed, a, rnd)
                            and not _coin(self.seed, b, rnd)
                            and (a in ext or len(nbr[a]) > 1)
                            and (b in ext or len(nbr[b]) > 1)):
                        comp_set.append(x)  # @line L4
            if not rake and not comp_set:
                # Only the path between u and v is left; force one compress.
                comp_set.append(min(x for x in live if x not in ext))
            for x in rake:
                ((y, c),) = nbr[x].items()
                del nbr[y][x]
                nbr[x].clear()
                if point[x] is None:
                    c.bound = (y,)  # a leaf edge is a point cluster at y
                    p = c
                else:
                    p = _rake(point[x], c, (y,))  # @line L5
                point[y] = p if point[y] is None else _rake(p, point[y], (y,))
                live.discard(x)
            for x in comp_set:
                (a, ca), (b, cb) = nbr[x].items()
                if point[x] is not None:
                    ca = _rake(point[x], ca, ca.bound)
                k = _compress(ca, cb, x)  # @line L6
                del nbr[a][x], nbr[b][x]
                nbr[x].clear()
                nbr[a][b] = k
                nbr[b][a] = k
                live.discard(x)
        root = nbr[u].get(v) if u != v else None
        for x in (u, v) if u != v else (u,):  # @line L7
            if point[x] is not None:
                root = point[x] if root is None else _rake(point[x], root, root.bound)
        if root is None:
            root = Cluster((u,), 0, NEG, 0, "empty")  # u has no edges
        return root

    def path_sum(self, u: int, v: int) -> Optional[int]:
        r = self.expose(u, v)
        return None if r is None else (r.psum if u != v else 0)  # @line L8

    def path_max(self, u: int, v: int) -> Optional[float]:
        r = self.expose(u, v)
        return None if r is None else (r.pmax if u != v else NEG)

    def tree_total(self, u: int) -> int:
        return self.expose(u, u).total
