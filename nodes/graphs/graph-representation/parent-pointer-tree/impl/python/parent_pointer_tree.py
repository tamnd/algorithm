# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parent-pointer-tree/. The authors are listed in prov/87C07Z.jsonl.

from typing import Iterator, Optional

NIL = -1


class ParentPointerTree:
    """A rooted forest on the vertices 0, 1, ..., n - 1 stored as one array.

    parent[x] is the parent of x, or NIL (-1) if x is a root. A new tree
    has the single vertex 0 as its root.
    """

    def __init__(self, parent: Optional[list[int]] = None) -> None:
        if parent is None:
            parent = [NIL]
        if not is_forest(parent):
            raise ValueError("the parent array has a cycle or a bad index")
        self.parent: list[int] = list(parent)

    def size(self) -> int:
        return len(self.parent)

    def add_child(self, p: int) -> int:
        """Add a new vertex as a child of p and return it."""
        if not 0 <= p < len(self.parent):
            raise IndexError(p)
        x = len(self.parent)  # @line L1
        self.parent.append(p)  # @line L2
        return x  # @line L3

    def parent_of(self, x: int) -> int:
        return self.parent[x]

    def path_to_root(self, x: int) -> Iterator[int]:
        """Yield x, the parent of x, and so on up to the root."""
        while x != NIL:  # @line L4
            yield x  # @line L5
            x = self.parent[x]  # @line L6

    def root_of(self, x: int) -> int:
        r = x
        for r in self.path_to_root(x):
            pass
        return r

    def depth(self, x: int) -> int:
        return sum(1 for _ in self.path_to_root(x)) - 1

    def child_lists(self) -> tuple[list[int], list[int]]:
        """Return (off, kids): the children of v are kids[off[v]:off[v + 1]],
        in increasing order. Counting sort of the vertices by parent."""
        n = len(self.parent)
        off = [0] * (n + 1)  # @line L7
        for x in range(n):  # @line L8
            if self.parent[x] != NIL:
                off[self.parent[x] + 1] += 1
        for v in range(1, n + 1):  # @line L9
            off[v] += off[v - 1]
        nxt = off[:n]  # @line L10
        kids = [0] * off[n]
        for x in range(n):  # @line L11
            p = self.parent[x]
            if p != NIL:  # @line L12
                kids[nxt[p]] = x  # @line L13
                nxt[p] += 1  # @line L14
        return off, kids  # @line L15

    def children(self, v: int) -> list[int]:
        """The children of v by a scan of the whole array, in Theta(n) time."""
        return [x for x in range(len(self.parent)) if self.parent[x] == v]

    def lca(self, u: int, v: int) -> int:
        """Lowest common ancestor by lifting the deeper vertex, O(1 + depth).
        Returns NIL if u and v are in different trees."""
        du, dv = self.depth(u), self.depth(v)
        while du > dv:
            u, du = self.parent[u], du - 1
        while dv > du:
            v, dv = self.parent[v], dv - 1
        while u != v:
            u, v = self.parent[u], self.parent[v]
        return u


def is_forest(parent: list[int]) -> bool:
    """True if every chain of parent links ends at NIL. Theta(n) time:
    each vertex is coloured once (0 new, 1 on the current chain, 2 done)."""
    n = len(parent)
    for p in parent:
        if p != NIL and not 0 <= p < n:
            return False
    colour = [0] * n
    for s in range(n):
        chain = []
        x = s
        while x != NIL and colour[x] == 0:
            colour[x] = 1
            chain.append(x)
            x = parent[x]
        if x != NIL and colour[x] == 1:
            return False
        for y in chain:
            colour[y] = 2
    return True


def from_bfs(adj: list[list[int]], root: int) -> list[int]:
    """The parent array of a breadth-first search tree of an undirected graph."""
    parent = [NIL] * len(adj)
    seen = [False] * len(adj)
    seen[root] = True
    queue = [root]
    i = 0
    while i < len(queue):
        u = queue[i]
        i += 1
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                queue.append(v)
    return parent
