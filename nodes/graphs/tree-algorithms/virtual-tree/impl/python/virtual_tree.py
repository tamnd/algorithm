# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/virtual-tree/. The authors are listed in prov/Q53SNA.jsonl.


class VirtualTree:
    """Virtual trees of key sets in a fixed rooted tree.

    The tree has the vertices 0 .. n-1, the n - 1 given edges and the root
    `root`; it is not weighted. The constructor computes the preorder entry
    times, the depths and a binary lifting table in Theta(n log n) time,
    without recursion. build(keys) returns the virtual tree of the keys.
    """

    def __init__(self, n: int, edges: list[tuple[int, int]], root: int = 0) -> None:
        adj: list[list[int]] = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        self.n = n
        self.root = root
        self.parent = [-1] * n
        self.depth = [0] * n
        self.tin = [0] * n
        seen = [False] * n
        seen[root] = True
        stack = [root]
        t = 0
        while stack:  # iterative preorder
            v = stack.pop()
            self.tin[v] = t
            t += 1
            for u in reversed(adj[v]):
                if not seen[u]:
                    seen[u] = True
                    self.parent[u] = v
                    self.depth[u] = self.depth[v] + 1
                    stack.append(u)
        self.log = max(1, (n - 1).bit_length())
        up0 = [p if p >= 0 else v for v, p in enumerate(self.parent)]
        self.up = [up0]
        for _ in range(1, self.log):
            prev = self.up[-1]
            self.up.append([prev[prev[v]] for v in range(n)])

    def lca(self, u: int, v: int) -> int:
        """Lowest common ancestor by binary lifting, O(log n)."""
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        diff = self.depth[u] - self.depth[v]
        j = 0
        while diff:
            if diff & 1:
                u = self.up[j][u]
            diff >>= 1
            j += 1
        if u == v:
            return u
        for j in range(self.log - 1, -1, -1):
            if self.up[j][u] != self.up[j][v]:
                u, v = self.up[j][u], self.up[j][v]
        return self.up[0][u]

    def build(self, keys: list[int]) -> tuple[list[int], list[int]]:
        """Return (nodes, par) for the virtual tree of a non-empty key list.

        nodes are the vertices of the virtual tree in preorder; par[i] is the
        position in nodes of the virtual parent of nodes[i], or -1 for
        nodes[0], the LCA of all keys. The edge from nodes[i] to its parent
        stands for a path of depth[nodes[i]] - depth[nodes[par[i]]] edges.
        """
        tin = self.tin
        ks = sorted(set(keys), key=tin.__getitem__)  # @line L1
        a = list(ks)  # @line L2
        for i in range(1, len(ks)):  # @line L3
            a.append(self.lca(ks[i - 1], ks[i]))
        nodes = sorted(set(a), key=tin.__getitem__)  # @line L4
        pos = {v: i for i, v in enumerate(nodes)}
        par = [-1] * len(nodes)  # @line L5
        for i in range(1, len(nodes)):  # @line L6
            par[i] = pos[self.lca(nodes[i - 1], nodes[i])]  # @line L7
        return nodes, par  # @line L8
