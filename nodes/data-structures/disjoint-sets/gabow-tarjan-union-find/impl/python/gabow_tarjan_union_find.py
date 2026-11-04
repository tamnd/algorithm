# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gabow-tarjan-union-find/. The authors are listed in prov/1DC4F6.jsonl.

from collections.abc import Sequence


class GabowTarjanUnionFind:
    """Static tree set union with microsets in words and a macro union-find forest.

    The tree is given by parent[v], with parent[root] == -1. link(v) unites the
    set of v with the set of its parent; find(v) returns the nearest ancestor
    of v, v included, that has not been linked. The tree is split into
    microsets of at most b nodes; inside a microset, the marks and the
    ancestor sets are bit masks, and a find inside it is one AND and one
    bit_length. A general union-find forest on the microset roots handles the
    jumps between microsets.
    """

    def __init__(self, parent: Sequence[int], b: int | None = None) -> None:
        n = len(parent)
        self.parent = list(parent)
        roots = [v for v in range(n) if parent[v] == -1]
        if n and len(roots) != 1:
            raise ValueError("parent must describe one rooted tree")
        if b is None:
            b = max(1, n.bit_length())  # @line L1
        self.b = b
        self.marked = [False] * n
        self.micro = [0] * n  # microset of each node
        self.local = [0] * n  # local index of each node in its microset
        self.anc = [0] * n  # mask of the ancestors of the node inside its piece
        self.members: list[list[int]] = []  # nodes of each microset, by local index
        self.mroot: list[int] = []  # root r(S) of each microset, or -1
        self.mask: list[int] = []  # marked nodes of each microset
        if n:
            self._partition(roots[0])  # @line L2
        for s, nodes in enumerate(self.members):  # @line L3
            for i, x in enumerate(nodes):
                self.local[x] = i
            for x in nodes:
                p = self.parent[x]
                inside = p != -1 and self.micro[p] == s
                self.anc[x] = (self.anc[p] if inside else 0) | (1 << self.local[x])
        # macro forest on the microset roots, with union by size and path compression
        self.mp: dict[int, int] = {}
        self.msize: dict[int, int] = {}
        self.mname: dict[int, int] = {}
        for r in self.mroot:  # @line L4
            if r != -1 and r not in self.mp:
                self.mp[r] = r
                self.msize[r] = 1
                self.mname[r] = r

    def _partition(self, root: int) -> None:
        """Split the tree into microsets of at most b nodes, bottom up."""
        n = len(self.parent)
        children: list[list[int]] = [[] for _ in range(n)]
        for v in range(n):
            if self.parent[v] != -1:
                children[self.parent[v]].append(v)
        order: list[int] = []
        stack = [root]
        while stack:
            v = stack.pop()
            order.append(v)
            stack.extend(children[v])
        order.reverse()  # children before parents
        half = (self.b + 1) // 2
        nxt = [-1] * n
        head = [-1] * n  # open list of each node, as a linked list
        tail = [-1] * n
        size = [0] * n

        def close(h: int, r: int) -> None:
            s = len(self.members)
            nodes = []
            while h != -1:
                nodes.append(h)
                self.micro[h] = s
                h = nxt[h]
            # the list is in preorder: each node comes after its parent in the piece
            self.members.append(nodes)
            self.mroot.append(r)
            self.mask.append(0)

        for v in order:
            gh, gt, gs = -1, -1, 0
            for c in children[v]:
                if gh == -1:
                    gh, gt = head[c], tail[c]
                else:
                    nxt[gt] = head[c]
                    gt = tail[c]
                gs += size[c]
                if gs >= half:
                    close(gh, v)
                    gh, gt, gs = -1, -1, 0
            nxt[v] = gh
            head[v], tail[v], size[v] = v, (gt if gh != -1 else v), gs + 1
        close(head[root], -1)

    def link(self, v: int) -> None:
        """Unite the set of v with the set of its parent. v must not be the root."""
        if self.parent[v] == -1:
            raise ValueError("the root cannot be linked")
        self.marked[v] = True
        self.mask[self.micro[v]] |= 1 << self.local[v]  # @line L5

    def _micro_find(self, x: int) -> int:
        s = self.micro[x]
        u = self.anc[x] & ~self.mask[s]  # @line L6
        if u == 0:  # @line L7
            return -1
        return self.members[s][u.bit_length() - 1]  # @line L8

    def _macro_name(self, y: int) -> int:
        r = y
        while self.mp[r] != r:
            r = self.mp[r]
        while self.mp[y] != r:
            nx = self.mp[y]
            self.mp[y] = r
            y = nx
        return self.mname[r]

    def _macro_union(self, z: int, y: int) -> None:
        name = self._macro_name(y)
        a, c = self._macro_root(z), self._macro_root(y)
        if self.msize[a] > self.msize[c]:
            a, c = c, a
        self.mp[a] = c
        self.msize[c] += self.msize[a]
        self.mname[c] = name

    def _macro_root(self, y: int) -> int:
        while self.mp[y] != y:
            y = self.mp[y]
        return y

    def find(self, v: int) -> int:
        """Return the nearest ancestor of v, v included, that has not been linked."""
        w = self._micro_find(v)  # @line L9
        if w != -1:
            return w
        z = self._macro_name(self.mroot[self.micro[v]])  # @line L10
        while True:
            w = self._micro_find(z)  # @line L11
            if w != -1:
                break
            self._macro_union(z, self.mroot[self.micro[z]])  # @line L12
            z = self._macro_name(z)  # @line L13
        return w  # @line L14

    def check_invariant(self) -> None:
        """Check the partition, the masks, and the names of the macro sets."""
        n = len(self.parent)
        seen = [0] * n
        for s, nodes in enumerate(self.members):
            assert 1 <= len(nodes) <= self.b
            m = 0
            for i, x in enumerate(nodes):
                seen[x] += 1
                assert self.micro[x] == s and self.local[x] == i
                p = self.parent[x]
                assert p == self.mroot[s] or (p != -1 and self.micro[p] == s)
                if p != -1 and self.micro[p] == s:
                    assert self.local[p] < i
                if self.marked[x]:
                    m |= 1 << i
            assert m == self.mask[s]
        assert all(c == 1 for c in seen)
        for y in self.mp:
            name = self._macro_name(y)
            a = y
            while a != name:  # the name is an ancestor of every member
                a = self.parent[a]
                assert a != -1
