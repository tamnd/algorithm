# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-cut-tree/. The authors are listed in prov/FD84D6.jsonl.

from bisect import bisect_right


def _blocks(n: int, edges: list[tuple[int, int]]) -> tuple[list[list[int]], list[bool]]:
    """Hopcroft-Tarjan with a stack of edges; loops are ignored.

    Returns the vertex sets of the blocks with at least one non-loop edge, in the
    order in which the search closes them, and the articulation point marks.
    """
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if u != v:
            adj[u].append((v, i))
            adj[v].append((u, i))
    d = [0] * n
    low = [0] * n
    t = 0
    estack: list[int] = []
    is_cut = [False] * n
    blocks: list[list[int]] = []
    for r in range(n):
        if d[r]:
            continue
        children = 0
        t += 1
        d[r] = low[r] = t
        frames = [(r, -1, 0)]
        while frames:
            u, p, k = frames[-1]
            if k < len(adj[u]):
                frames[-1] = (u, p, k + 1)
                v, e = adj[u][k]
                if e == p:
                    continue
                if d[v] == 0:
                    estack.append(e)
                    children += u == r
                    t += 1
                    d[v] = low[v] = t
                    frames.append((v, e, 0))
                elif d[v] < d[u]:
                    estack.append(e)
                    low[u] = min(low[u], d[v])
                continue
            frames.pop()
            if not frames:
                break
            w = frames[-1][0]
            low[w] = min(low[w], low[u])
            if low[u] >= d[w]:
                verts: set[int] = set()
                while True:
                    x = estack.pop()
                    verts.update(edges[x])
                    if x == p:
                        break
                blocks.append(sorted(verts))
                if w != r:
                    is_cut[w] = True
        if children >= 2:
            is_cut[r] = True
    return blocks, is_cut


class BlockCutTree:
    """The block-cut forest of an undirected graph on the vertices 0 .. n-1.

    Precondition: edges[i] = (u, v) with 0 <= u, v < n; parallel edges and loops are
    allowed, and loops are ignored. Block nodes are 0 .. b-1 and the cut node of the
    articulation point x is b + (its index among the articulation points). A vertex
    with no non-loop edge gets a block of its own. Each tree is rooted at a block node.
    Build time O(n + m) and space O(n + m); node and same_block take O(1) time, and
    separates takes O(log n) time.
    """

    def __init__(self, n: int, edges: list[tuple[int, int]]) -> None:
        blocks, is_cut = _blocks(n, edges)  # @line L1
        seen = [False] * n
        for b in blocks:
            for v in b:
                seen[v] = True
        for v in range(n):
            if not seen[v]:
                blocks.append([v])
        self.n = n
        self.blocks = blocks  # @line L2
        self.cuts = [v for v in range(n) if is_cut[v]]
        nb = len(blocks)
        self.num_nodes = nb + len(self.cuts)
        cut_node = [-1] * n
        for j, x in enumerate(self.cuts):
            cut_node[x] = nb + j
        self.adj: list[list[int]] = [[] for _ in range(self.num_nodes)]
        self.vertex_node = [-1] * n
        for i, b in enumerate(blocks):
            for x in b:
                if is_cut[x]:  # @line L3
                    self.adj[i].append(cut_node[x])
                    self.adj[cut_node[x]].append(i)
                else:
                    self.vertex_node[x] = i  # @line L4
        for x in self.cuts:
            self.vertex_node[x] = cut_node[x]
        # @line L5: root each tree at the last block that the search closed for it.
        self.parent = [-1] * self.num_nodes
        self.tin = [0] * self.num_nodes
        self.tout = [0] * self.num_nodes
        self.children: list[list[int]] = [[] for _ in range(self.num_nodes)]
        self.child_tin: list[list[int]] = [[] for _ in range(self.num_nodes)]
        visited = [False] * self.num_nodes
        clock = 0
        for root in reversed(range(nb)):
            if visited[root]:
                continue
            visited[root] = True
            clock += 1
            self.tin[root] = clock
            stack = [(root, 0)]
            while stack:
                a, k = stack[-1]
                if k < len(self.adj[a]):
                    stack[-1] = (a, k + 1)
                    c = self.adj[a][k]
                    if not visited[c]:
                        visited[c] = True
                        self.parent[c] = a
                        self.children[a].append(c)
                        clock += 1
                        self.tin[c] = clock
                        self.child_tin[a].append(clock)
                        stack.append((c, 0))
                else:
                    stack.pop()
                    self.tout[a] = clock

    def is_cut_node(self, a: int) -> bool:
        return a >= len(self.blocks)

    def node(self, v: int) -> int:
        """The tree node of the vertex v: its cut node, or the one block that holds it."""
        return self.vertex_node[v]

    def ancestor(self, a: int, c: int) -> bool:
        """Is the node a an ancestor of the node c (or equal to it)?"""
        return self.tin[a] <= self.tin[c] and self.tout[c] <= self.tout[a]  # @line L6

    def child_toward(self, a: int, c: int) -> int:
        """The child of a whose subtree holds c; a must be a proper ancestor of c."""
        j = bisect_right(self.child_tin[a], self.tin[c]) - 1  # @line L7
        return self.children[a][j]

    def separates(self, x: int, u: int, v: int) -> bool:
        """Does every path from u to v pass through x? u, v, x distinct, u, v joined."""
        if not self.is_cut_node(self.vertex_node[x]):  # @line L8
            return False
        g = self.vertex_node[x]  # @line L9
        a, b = self.vertex_node[u], self.vertex_node[v]
        p, q = self.ancestor(g, a), self.ancestor(g, b)
        if p != q:  # @line L10
            return True
        if not p:  # @line L11
            return False
        return self.child_toward(g, a) != self.child_toward(g, b)  # @line L12

    def same_block(self, u: int, v: int) -> bool:
        """Do the distinct vertices u and v lie in a common block?"""
        a, b = self.vertex_node[u], self.vertex_node[v]  # @line L13
        ca, cb = self.is_cut_node(a), self.is_cut_node(b)
        par = self.parent
        if not ca and not cb:  # @line L14
            return a == b
        if ca != cb:  # @line L15
            if cb:
                a, b = b, a
            return par[b] == a or par[a] == b
        pa, pb = par[a], par[b]  # @line L16
        return (pa >= 0 and par[pa] == b) or (pb >= 0 and par[pb] == a) or pa == pb

    def check_invariant(self) -> None:
        """Assert that the structure is a bipartite forest of blocks and cut nodes."""
        nb = len(self.blocks)
        edges = sum(len(x) for x in self.adj) // 2
        roots = sum(1 for a in range(self.num_nodes) if self.parent[a] == -1)
        assert edges == self.num_nodes - roots  # a forest
        for a in range(self.num_nodes):
            for c in self.adj[a]:
                assert (a < nb) != (c < nb)  # bipartite
            if self.parent[a] == -1:
                assert a < nb  # roots are blocks
            else:
                assert self.ancestor(self.parent[a], a)
        for j, x in enumerate(self.cuts):
            assert len(self.adj[nb + j]) >= 2  # a cut vertex lies in two blocks
            assert self.vertex_node[x] == nb + j
        covered = [0] * self.n
        for b in self.blocks:
            for x in b:
                covered[x] += 1
        for x in range(self.n):
            assert covered[x] >= 1
            assert (covered[x] >= 2) == (self.vertex_node[x] >= nb)
