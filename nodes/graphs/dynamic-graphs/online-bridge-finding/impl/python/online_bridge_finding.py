# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-bridge-finding/. The authors are listed in prov/6AA8GQ.jsonl.

"""Online bridge finding: the bridges of a graph under edge insertions.

The 2-edge-connected components are kept in a union-find. Contracting them
turns each connected component into a tree (the bridge tree), stored by parent
pointers between component representatives. A second union-find keeps the
connected components. An edge between two trees links them, after rerooting
the smaller one; an edge inside one tree closes a cycle, and every bridge on
the tree path between its ends stops being a bridge. Insertions only;
deterministic; O(m log n) total time for m insertions, up to an alpha factor.
"""


class OnlineBridges:
    def __init__(self, n: int) -> None:
        self.n = n
        self.par = [-1] * n  # bridge-tree parent (any vertex of the parent 2ECC)
        self.ecc = list(range(n))  # union-find of 2-edge-connected components
        self.ecc_size = [1] * n
        self.cc = list(range(n))  # union-find of connected components
        self.cc_size = [1] * n
        self.bridges = 0
        self._mark = [0] * n
        self._stamp = 0

    def find_2ecc(self, v: int) -> int:
        root = v
        while self.ecc[root] != root:
            root = self.ecc[root]
        while self.ecc[v] != root:
            self.ecc[v], v = root, self.ecc[v]
        return root

    def find_cc(self, v: int) -> int:
        v = self.find_2ecc(v)
        root = v
        while self.cc[root] != root:
            root = self.cc[root]
        while self.cc[v] != root:
            self.cc[v], v = root, self.cc[v]
        return root

    def _parent(self, v: int) -> int:
        p = self.par[v]
        return -1 if p == -1 else self.find_2ecc(p)

    def _reroot(self, v: int) -> None:
        """Make the 2ECC v the root of its bridge tree."""
        old = self.find_cc(v)
        size = self.cc_size[old]
        root = v
        child = -1
        while v != -1:
            p = self._parent(v)  # @line L9
            self.par[v] = child
            self.cc[v] = root
            child = v
            v = p
        self.cc[old] = root
        self.cc[root] = root
        self.cc_size[root] = size

    def _merge_path(self, a: int, b: int) -> None:
        """a and b are 2ECCs in one tree; merge the tree path between them."""
        self._stamp += 1
        path_a: list[int] = []
        path_b: list[int] = []
        lca = -1
        while lca == -1:  # @line L7
            if a != -1:
                if self._mark[a] == self._stamp:
                    lca = a
                    break
                self._mark[a] = self._stamp
                path_a.append(a)
                a = self._parent(a)
            if b != -1:
                if self._mark[b] == self._stamp:
                    lca = b
                    break
                self._mark[b] = self._stamp
                path_b.append(b)
                b = self._parent(b)
        up = self.par[lca]  # the bridge above the merged component stays
        rep = lca
        for path in (path_a, path_b):
            for v in path:
                if v == lca:
                    break
                if self.ecc_size[v] > self.ecc_size[rep]:
                    v, rep = rep, v
                self.ecc[v] = rep  # @line L8
                self.ecc_size[rep] += self.ecc_size[v]
                self.bridges -= 1
        self.par[rep] = up

    def add_edge(self, a: int, b: int) -> None:
        a, b = self.find_2ecc(a), self.find_2ecc(b)  # @line L1
        if a == b:
            return
        ca, cb = self.find_cc(a), self.find_cc(b)  # @line L2
        if ca != cb:
            self.bridges += 1  # @line L3
            if self.cc_size[ca] > self.cc_size[cb]:
                a, b, ca, cb = b, a, cb, ca  # @line L4
            self._reroot(a)  # @line L5
            self.par[a] = b
            self.cc[a] = b
            self.cc_size[cb] += self.cc_size[a]
        else:
            self._merge_path(a, b)  # @line L6

    def two_edge_connected(self, u: int, v: int) -> bool:
        return self.find_2ecc(u) == self.find_2ecc(v)

    def connected(self, u: int, v: int) -> bool:
        return self.find_cc(u) == self.find_cc(v)

    def is_bridge(self, u: int, v: int) -> bool:
        """For an inserted edge {u, v}: is it currently a bridge?"""
        a, b = self.find_2ecc(u), self.find_2ecc(v)
        return a != b
