# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ladder-decomposition/. The authors are listed in prov/VJP1A9.jsonl.

from collections import deque


class LadderLevelAncestor:
    """Level ancestor queries by jump pointers and ladders.

    The tree has the vertices 0 .. n-1 (n >= 1), is unweighted, and is given
    by its n - 1 undirected edges and a root. Preprocessing takes
    O(n log n) time and memory (the ladders alone take O(n)); each query
    takes O(1) time. No recursion is used.
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
        parent = [-1] * n
        depth = [-1] * n
        depth[root] = 0
        order = [root]
        queue = deque([root])
        while queue:  # @line L1
            v = queue.popleft()
            for w in adj[v]:
                if depth[w] == -1:
                    depth[w] = depth[v] + 1
                    parent[w] = v
                    order.append(w)
                    queue.append(w)
        if len(order) != n:
            raise ValueError("the edges do not form a tree")
        height = [1] * n  # vertices on the longest downward path
        long_child = [-1] * n
        for v in reversed(order):  # @line L2
            p = parent[v]
            if p != -1:
                c = long_child[p]
                if c == -1 or height[v] > height[c] or (height[v] == height[c] and v < c):
                    long_child[p] = v
                    height[p] = height[v] + 1
        ladder_of = [0] * n
        top = [0] * n
        ladders: list[list[int]] = []
        for v in order:  # @line L3
            if v != root and long_child[parent[v]] == v:
                continue
            path = []  # @line L4
            x = v
            while x != -1:
                path.append(x)
                x = long_child[x]
            k = len(path)
            above = []  # @line L5
            x = parent[v]
            while x != -1 and len(above) < k:
                above.append(x)
                x = parent[x]
            above.reverse()
            ladder_id = len(ladders)
            ladders.append(above + path)
            for x in path:  # @line L6
                ladder_of[x] = ladder_id
                top[x] = depth[v] - len(above)
        up = [[p if p != -1 else root for p in parent]]
        levels = max(1, (n - 1).bit_length())
        for _ in range(1, levels):  # @line L7
            prev = up[-1]
            up.append([prev[prev[v]] for v in range(n)])
        self.n = n
        self.root = root
        self.parent = parent
        self.depth = depth
        self.height = height
        self.long_child = long_child
        self.ladders = ladders
        self.ladder_of = ladder_of
        self.top = top
        self._up = up

    def level_ancestor(self, v: int, d: int) -> int | None:
        """Return the ancestor of v at depth d, or None if 0 <= d <= depth(v) fails."""
        if not 0 <= v < self.n:
            raise IndexError("vertex out of range")
        if d < 0 or d > self.depth[v]:  # @line L8
            return None
        k = self.depth[v] - d  # @line L9
        if k == 0:
            return v
        i = k.bit_length() - 1  # @line L10
        u = self._up[i][v]
        return self.ladders[self.ladder_of[u]][d - self.top[u]]  # @line L11

    def kth_ancestor(self, v: int, k: int) -> int | None:
        """Return the ancestor of v at distance k, or None if it does not exist."""
        if not 0 <= v < self.n:
            raise IndexError("vertex out of range")
        return self.level_ancestor(v, self.depth[v] - k)
