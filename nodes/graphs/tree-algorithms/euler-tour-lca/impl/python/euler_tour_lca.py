# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-tour-lca/. The authors are listed in prov/SKXZFC.jsonl.


class EulerTourLca:
    """Lowest common ancestors by an Euler tour and a sparse table.

    The tree has the vertices 0 .. n-1 (n >= 1), is unweighted, and is given
    by its n - 1 undirected edges and a root. Children are visited in
    increasing label order. Preprocessing takes O(n log n) time and memory;
    each query takes O(1) time. No recursion is used.
    """

    def __init__(self, n: int, edges: list[tuple[int, int]], root: int = 0) -> None:
        if n < 1 or len(edges) != n - 1 or not 0 <= root < n:
            raise ValueError("a tree needs n >= 1 vertices, n - 1 edges and a root in range")
        adj: list[list[int]] = [[] for _ in range(n)]
        for a, b in edges:
            if not (0 <= a < n and 0 <= b < n) or a == b:
                raise ValueError("edge endpoints must be distinct vertices in range")
            adj[a].append(b)
            adj[b].append(a)
        for lst in adj:
            lst.sort()
        depth = [-1] * n
        first = [0] * n
        nxt = [0] * n  # index of the next neighbour of each vertex to try
        depth[root] = 0  # @line L1
        first[root] = 0
        euler = [root]
        stack = [root]
        while stack:  # @line L2
            v = stack[-1]  # @line L3
            nbrs = adj[v]
            i = nxt[v]
            while i < len(nbrs) and depth[nbrs[i]] != -1:
                i += 1
            nxt[v] = i + 1
            if i < len(nbrs):  # @line L4
                c = nbrs[i]
                depth[c] = depth[v] + 1  # @line L5
                first[c] = len(euler)
                euler.append(c)
                stack.append(c)
            else:
                stack.pop()  # @line L6
                if stack:
                    euler.append(stack[-1])
        if len(euler) != 2 * n - 1:
            raise ValueError("the edges do not form a tree")
        self.n = n
        self.root = root
        self.depth = depth
        self.first = first
        self.euler = euler
        table = [euler[:]]  # @line L7
        m = len(euler)
        k = 1
        while (1 << k) <= m:  # @line L8
            prev = table[-1]
            half = 1 << (k - 1)
            # @line L9
            row = [a if depth[a] <= depth[b] else b for a, b in zip(prev[: m - (1 << k) + 1], prev[half:])]
            table.append(row)
            k += 1
        self._table = table

    def lca(self, u: int, v: int) -> int:
        """Return the lowest common ancestor of u and v."""
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("vertex out of range")
        lo, hi = self.first[u], self.first[v]  # @line L10
        if lo > hi:
            lo, hi = hi, lo
        k = (hi - lo + 1).bit_length() - 1  # @line L11
        row = self._table[k]
        a, b = row[lo], row[hi - (1 << k) + 1]  # @line L12
        return a if self.depth[a] <= self.depth[b] else b

    def distance(self, u: int, v: int) -> int:
        """Return the number of edges on the path between u and v."""
        w = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[w]
