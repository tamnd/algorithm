# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frederickson-topology-trees/. The authors are listed in prov/ZS0KCA.jsonl.

"""Frederickson's clustering method for fully dynamic minimum spanning forests.

The minimum spanning forest F is cut into connected clusters of at most z
vertices. For every pair of clusters, the non-tree edges between them are
kept in a table, so the lightest edge across a cut of F can be found by
looking at pairs of clusters instead of at edges. This is the one-level
structure of Frederickson (1985). His topology trees build the clusters into
a hierarchy, and his two-dimensional topology trees keep the minima over
pairs of clusters of all levels, which lowers the update time to O(m^(1/2)).

build_topology_tree builds the multilevel partition of a tree of degree at
most three that a topology tree records.

Edges are ordered by (weight, smaller end, larger end), so the forest is unique.
"""

from math import ceil
from typing import Optional

Key = tuple[float, int, int]


def _key(u: int, v: int, w: float) -> Key:
    return (w, u, v) if u < v else (w, v, u)


class DynamicMSF:
    def __init__(self, n: int) -> None:
        self.n = n
        self.tadj: list[dict[int, Key]] = [dict() for _ in range(n)]   # forest edges
        self.weight: dict[tuple[int, int], float] = {}                # all edges
        self.nontree: dict[tuple[int, int], Key] = {}
        self.nt_at: list[set[tuple[int, int]]] = [set() for _ in range(n)]
        self.updates = 0
        self._recluster()

    # ---- clusters -------------------------------------------------------
    def _recluster(self) -> None:
        """Greedy bottom-up partition of each tree of F into connected clusters of size at most z."""
        n = self.n
        self.z = max(1, ceil(n ** (2 / 3)))
        self.cid = [-1] * n
        self.members: dict[int, set[int]] = {}
        self.next_id = 0
        seen = [False] * n
        for r in range(n):
            if seen[r]:
                continue
            order, parent, st = [], {r: -1}, [r]
            seen[r] = True
            while st:
                x = st.pop()
                order.append(x)
                for y in self.tadj[x]:
                    if not seen[y]:
                        seen[y] = True
                        parent[y] = x
                        st.append(y)
            open_set: dict[int, set[int]] = {}
            for x in reversed(order):  # children before parents
                cur = {x}
                for y in self.tadj[x]:
                    if parent.get(y) == x:
                        part = open_set.pop(y)
                        if len(cur) + len(part) <= self.z:
                            cur |= part
                        else:
                            self._new_cluster(part)
                open_set[x] = cur
            self._new_cluster(open_set.pop(r))
        # cluster tree and table of non-tree edges by pairs of clusters
        self.ctree: dict[int, dict[int, int]] = {c: {} for c in self.members}
        for u in range(n):
            for v in self.tadj[u]:
                if u < v:
                    self._ct_add(self.cid[u], self.cid[v])
        self.table: dict[tuple[int, int], dict[tuple[int, int], Key]] = {}
        for e, k in self.nontree.items():
            self._tab_add(e, k)

    def _new_cluster(self, vs: set[int]) -> int:
        c = self.next_id
        self.next_id += 1
        self.members[c] = vs
        for v in vs:
            self.cid[v] = c
        return c

    def _ct_add(self, a: int, b: int) -> None:
        if a != b:
            self.ctree[a][b] = self.ctree[a].get(b, 0) + 1
            self.ctree[b][a] = self.ctree[b].get(a, 0) + 1

    def _ct_del(self, a: int, b: int) -> None:
        if a != b:
            for x, y in ((a, b), (b, a)):
                self.ctree[x][y] -= 1
                if not self.ctree[x][y]:
                    del self.ctree[x][y]

    def _pair(self, e: tuple[int, int]) -> tuple[int, int]:
        a, b = self.cid[e[0]], self.cid[e[1]]
        return (a, b) if a <= b else (b, a)

    def _tab_add(self, e: tuple[int, int], k: Key) -> None:
        self.table.setdefault(self._pair(e), {})[e] = k

    def _tab_del(self, e: tuple[int, int]) -> None:
        p = self._pair(e)
        del self.table[p][e]
        if not self.table[p]:
            del self.table[p]

    def _move(self, vs: set[int], new: int) -> None:
        """Move the vertices vs into the cluster new, fixing the cluster tree and the table."""
        old = self.cid[next(iter(vs))]
        touched = set()
        for v in vs:
            for y in self.tadj[v]:
                self._ct_del(self.cid[v], self.cid[y])
            touched |= self.nt_at[v]
        for e in touched:
            self._tab_del(e)
        for v in vs:
            self.members[self.cid[v]].discard(v)
        for v in vs:
            self.cid[v] = new
            self.members[new].add(v)
        for v in vs:
            for y in self.tadj[v]:
                self._ct_add(self.cid[v], self.cid[y])
        for e in touched:
            self._tab_add(e, self.nontree[e])
        if not self.members[old]:
            del self.members[old]
            del self.ctree[old]

    # ---- forest edges ---------------------------------------------------
    def _add_tree(self, u: int, v: int, k: Key) -> None:
        self.tadj[u][v] = k
        self.tadj[v][u] = k
        self._ct_add(self.cid[u], self.cid[v])
        a, b = self.cid[u], self.cid[v]
        if a != b and len(self.members[a]) + len(self.members[b]) <= self.z:
            small, big = (a, b) if len(self.members[a]) <= len(self.members[b]) else (b, a)
            self._move(set(self.members[small]), big)

    def _del_tree(self, u: int, v: int) -> None:
        del self.tadj[u][v]
        del self.tadj[v][u]
        c = self.cid[u]
        if c != self.cid[v]:
            self._ct_del(c, self.cid[v])
            return
        side = self._reach_in_cluster(u, c)  # @line L4
        if v in side:
            raise AssertionError("tree edge was on a cycle")
        rest = self.members[c] - side
        new = self._new_cluster(set())
        self.ctree[new] = {}
        self._move(side if len(side) <= len(rest) else rest, new)

    def _reach_in_cluster(self, s: int, c: int) -> set[int]:
        seen, st = {s}, [s]
        while st:
            x = st.pop()
            for y in self.tadj[x]:
                if y not in seen and self.cid[y] == c:
                    seen.add(y)
                    st.append(y)
        return seen

    def _side(self, c: int) -> set[int]:
        """Clusters in the tree of the cluster c, by a walk on the cluster tree."""
        seen, st = {c}, [c]
        while st:
            x = st.pop()
            for y in self.ctree[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        return seen

    def _path_max(self, u: int, v: int) -> Optional[Key]:
        """Heaviest forest edge on the path from u to v, inside the clusters of the cluster path."""
        cu, cv = self.cid[u], self.cid[v]
        prev = {cu: -1}
        st = [cu]
        while st:
            x = st.pop()
            for y in self.ctree[x]:
                if y not in prev:
                    prev[y] = x
                    st.append(y)
        if cv not in prev:
            return None
        allowed = set()
        x = cv
        while x != -1:
            allowed.add(x)
            x = prev[x]
        par = {u: (-1, None)}
        st = [u]
        while st:
            x = st.pop()
            for y, k in self.tadj[x].items():
                if y not in par and self.cid[y] in allowed:
                    par[y] = (x, k)
                    st.append(y)
        best, x = None, v
        while x != u:
            x, k = par[x]
            if best is None or k > best:
                best = k
        return best

    # ---- the algorithm --------------------------------------------------
    def insert(self, u: int, v: int, w: float) -> None:
        if u == v:
            return
        e = (min(u, v), max(u, v))
        if e in self.weight:
            raise ValueError("edge already present")
        k = _key(u, v, w)
        self.weight[e] = w
        if self.cid[v] not in self._side(self.cid[u]):
            self._add_tree(u, v, k)  # @line L1
        else:
            mx = self._path_max(u, v)  # @line L2
            if k < mx:
                a, b = mx[1], mx[2]
                self._del_tree(a, b)
                self._add_tree(u, v, k)
                self._add_nontree((a, b), mx)  # @line L3
            else:
                self._add_nontree(e, k)
        self._tick()

    def delete(self, u: int, v: int) -> None:
        e = (min(u, v), max(u, v))
        del self.weight[e]
        if e in self.nontree:
            self._remove_nontree(e)
            self._tick()
            return
        self._del_tree(u, v)
        A, B = self._side(self.cid[u]), self._side(self.cid[v])
        best = None
        for a in A:  # @line L5
            for b in B:
                p = (a, b) if a <= b else (b, a)
                if p in self.table:
                    k = min(self.table[p].values())
                    if best is None or k < best:
                        best = k
        if best is not None:
            r = (best[1], best[2])
            self._remove_nontree(r)
            self._add_tree(r[0], r[1], best)  # @line L6
        self._tick()

    def _add_nontree(self, e: tuple[int, int], k: Key) -> None:
        self.nontree[e] = k
        self.nt_at[e[0]].add(e)
        self.nt_at[e[1]].add(e)
        self._tab_add(e, k)

    def _remove_nontree(self, e: tuple[int, int]) -> None:
        self._tab_del(e)
        del self.nontree[e]
        self.nt_at[e[0]].discard(e)
        self.nt_at[e[1]].discard(e)

    def _tick(self) -> None:
        self.updates += 1
        if self.updates % self.z == 0:
            self._recluster()  # @line L7

    def forest(self) -> set[tuple[int, int]]:
        return {(u, v) for u in range(self.n) for v in self.tadj[u] if u < v}

    def total(self) -> float:
        return sum(self.weight[e] for e in self.forest())


def build_topology_tree(n: int, edges: list[tuple[int, int]]) -> list[list[frozenset[int]]]:
    """Levels of a restricted multilevel partition of a forest of degree at most 3.

    Level 0 has one cluster per vertex. Each higher level joins pairs of
    adjacent clusters of the level below: a cluster of external degree 3 is
    joined only with a neighbor of external degree 1, and a cluster of
    degree at most 2 with a neighbor of degree at most 2, or with a degree 1
    neighbor. A greedy maximal set of such pairs is joined; the other
    clusters are copied up. It stops when no pair can be joined.
    """
    adj: list[set[int]] = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    if any(len(s) > 3 for s in adj):
        raise ValueError("degree above 3")
    cl = list(range(n))  # cluster index of each vertex
    levels = [[frozenset([v]) for v in range(n)]]
    while True:  # @line L8
        k = len(levels[-1])
        nb: list[set[int]] = [set() for _ in range(k)]
        deg = [0] * k
        for a, b in edges:
            if cl[a] != cl[b]:
                nb[cl[a]].add(cl[b])
                nb[cl[b]].add(cl[a])
                deg[cl[a]] += 1
                deg[cl[b]] += 1
        mate = [-1] * k
        for x in range(k):
            if mate[x] != -1:
                continue
            for y in sorted(nb[x]):
                if mate[y] == -1 and (min(deg[x], deg[y]) == 1 or max(deg[x], deg[y]) <= 2):
                    mate[x], mate[y] = y, x  # @line L9
                    break
        if all(m == -1 for m in mate):
            return levels
        new_index = [-1] * k
        nxt: list[frozenset[int]] = []
        for x in range(k):
            if new_index[x] == -1:
                group = levels[-1][x] | (levels[-1][mate[x]] if mate[x] != -1 else frozenset())
                new_index[x] = len(nxt)
                if mate[x] != -1:
                    new_index[mate[x]] = len(nxt)
                nxt.append(group)  # @line L10
        cl = [new_index[c] for c in cl]
        levels.append(nxt)
