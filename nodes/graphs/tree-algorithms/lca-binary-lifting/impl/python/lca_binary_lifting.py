# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lca-binary-lifting/. The authors are listed in prov/T1VPR2.jsonl.

from collections import deque


class LcaBinaryLifting:
    """Lowest common ancestors in a static rooted tree by binary lifting.

    The tree has the vertices 0 .. n-1 (n >= 1), is unweighted, and is given
    by its n - 1 undirected edges and a root. Preprocessing takes
    O(n log n) time and memory; each query takes O(log n) time.
    """

    def __init__(self, n: int, edges: list[tuple[int, int]], root: int = 0) -> None:
        if n < 1 or len(edges) != n - 1 or not 0 <= root < n:
            raise ValueError("a tree needs n >= 1 vertices, n - 1 edges and a root in range")
        adj: list[list[int]] = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        parent = [-1] * n
        depth = [0] * n
        parent[root] = root
        seen = [False] * n
        seen[root] = True
        queue = deque([root])  # @line L1
        while queue:
            x = queue.popleft()
            for y in adj[x]:
                if not seen[y]:
                    seen[y] = True
                    parent[y] = x
                    depth[y] = depth[x] + 1
                    queue.append(y)
        if not all(seen):
            raise ValueError("the edges do not connect all vertices")
        self.n = n
        self.depth = depth
        self.K = max(1, (n - 1).bit_length())  # @line L2
        up = [parent[:]]  # @line L3
        for k in range(1, self.K):  # @line L4
            prev = up[k - 1]
            up.append([prev[prev[v]] for v in range(n)])
        self.up = up

    def kth_ancestor(self, v: int, d: int) -> int:
        """The ancestor of v at distance d, for 0 <= d <= depth(v)."""
        if not 0 <= d <= self.depth[v]:
            raise ValueError("d must be between 0 and the depth of v")
        k = 0
        while d:
            if d & 1:
                v = self.up[k][v]
            d >>= 1
            k += 1
        return v

    def lca(self, u: int, v: int) -> int:
        """The deepest vertex that is an ancestor of both u and v."""
        up = self.up
        if self.depth[u] < self.depth[v]:  # @line L5
            u, v = v, u
        d = self.depth[u] - self.depth[v]  # @line L6
        u = self.kth_ancestor(u, d)  # @line L7
        if u == v:  # @line L8
            return u
        for k in range(self.K - 1, -1, -1):  # @line L9
            if up[k][u] != up[k][v]:  # @line L10
                u = up[k][u]
                v = up[k][v]
        return up[0][u]  # @line L11

    def distance(self, u: int, v: int) -> int:
        """The number of edges on the path from u to v."""
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]
