# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blum-union-find/. The authors are listed in prov/YNSV90.jsonl.


class BlumUnionFind:
    """Blum's k-UF trees: O(log n / log log n) worst-case time per operation.

    The elements 0..n-1 are the leaves. In each tree all leaves are at the
    same depth, the root has at least two children unless it is a leaf, and
    every other inner node has at least k children. find walks from the leaf
    to the root; union moves fewer than k children or adds one edge.
    """

    def __init__(self, n: int, k: int | None = None) -> None:
        if n < 0:
            raise ValueError("n must be non-negative")
        if k is None:
            lg = max(1, (n - 1).bit_length())
            lglg = max(1, lg.bit_length())
            k = max(2, -(-lg // lglg))
        if k < 2:
            raise ValueError("k must be at least 2")
        self.n = n
        self.k = k
        self.parent: list[int] = [-1] * n
        self.children: list[list[int]] = [[] for _ in range(n)]
        self.height: list[int] = [0] * n
        self.name: list[int] = list(range(n))
        self.count = n

    def _root(self, x: int) -> int:
        p = self.parent
        while p[x] != -1:  # @line L1
            x = p[x]
        return x

    def find(self, x: int) -> int:
        """Return the name of the set of x, an element of that set."""
        if not 0 <= x < self.n:
            raise IndexError("no such element")
        return self.name[self._root(x)]  # @line L2

    def connected(self, x: int, y: int) -> bool:
        """Return True if x and y are in the same set."""
        return self._root(x) == self._root(y)

    def _new_node(self, h: int) -> int:
        self.parent.append(-1)
        self.children.append([])
        self.height.append(h)
        self.name.append(-1)
        return len(self.parent) - 1

    def _adopt(self, v: int, c: int) -> None:
        self.parent[c] = v
        self.children[v].append(c)

    def _move_children(self, s: int, v: int) -> None:
        for c in self.children[s]:
            self._adopt(v, c)
        self.children[s] = []

    def _down(self, r: int, h: int) -> int:
        while self.height[r] > h:
            r = self.children[r][0]
        return r

    def union(self, x: int, y: int) -> bool:
        """Merge the sets of x and y. Return False if they were one set."""
        r, s = self._root(x), self._root(y)  # @line L3
        if r == s:
            return False
        self.count -= 1
        k = self.k
        if self.height[r] < self.height[s]:  # @line L4
            r, s = s, r
        if self.height[r] == self.height[s]:  # @line L5
            dr, ds = len(self.children[r]), len(self.children[s])
            if self.height[r] == 0 or (dr >= k and ds >= k):  # @line L6
                t = self._new_node(self.height[r] + 1)
                self.name[t] = self.name[r]
                self._adopt(t, r)
                self._adopt(t, s)
                return True
            if dr < ds:  # @line L7
                r, s = s, r
            self._move_children(s, r)  # @line L8
            return True
        if self.height[s] == 0 or len(self.children[s]) >= k:  # @line L9
            self._adopt(self._down(r, self.height[s] + 1), s)  # @line L10
        else:
            self._move_children(s, self._down(r, self.height[s]))  # @line L11
        return True  # @line L12

    def check_invariant(self) -> None:
        """Check the shape of every k-UF tree and the parent and child links."""
        roots = set()
        for x in range(self.n):
            d, y = 0, x
            while self.parent[y] != -1:
                p = self.parent[y]
                assert y in self.children[p]
                assert self.height[p] == self.height[y] + 1
                y = p
                d += 1
            assert self.height[y] == d  # all leaves of a tree at the same depth
            roots.add(y)
        assert len(roots) == self.count
        live = set()
        for r in roots:
            stack = [r]
            leaves = 0
            while stack:
                v = stack.pop()
                live.add(v)
                ch = self.children[v]
                if self.height[v] == 0:
                    assert not ch and v < self.n
                    leaves += 1
                elif v == r:
                    assert len(ch) >= 2
                else:
                    assert len(ch) >= self.k
                for c in ch:
                    assert self.parent[c] == v
                stack.extend(ch)
            h = self.height[r]
            assert h == 0 or leaves >= 2 * self.k ** (h - 1)
            assert 0 <= self.name[r] < self.n and self._root(self.name[r]) == r
