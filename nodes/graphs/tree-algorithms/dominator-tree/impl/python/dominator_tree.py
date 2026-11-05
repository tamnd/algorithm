# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dominator-tree/. The authors are listed in prov/GK1MNC.jsonl.


def _immediate_dominators(n: int, edges: list[tuple[int, int]], root: int) -> list[int]:
    """Immediate dominators by the simple Lengauer-Tarjan algorithm, O(m log n).

    Returns idom with idom[root] = -1 and idom[v] = -1 for vertices that the
    root cannot reach. Iterative, so long paths do not hit the recursion limit.
    """
    succ: list[list[int]] = [[] for _ in range(n)]
    pred: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        if not (0 <= a < n and 0 <= b < n):
            raise ValueError("edge endpoint out of range")
        succ[a].append(b)
        pred[b].append(a)
    dfn = [-1] * n
    vertex = [root]
    parent = [-1]
    dfn[root] = 0
    stack = [(root, 0)]
    while stack:
        v, i = stack[-1]
        if i < len(succ[v]):
            stack[-1] = (v, i + 1)
            w = succ[v][i]
            if dfn[w] == -1:
                dfn[w] = len(vertex)
                vertex.append(w)
                parent.append(dfn[v])
                stack.append((w, 0))
        else:
            stack.pop()
    k = len(vertex)
    semi = list(range(k))
    idom = [0] * k
    ancestor = [-1] * k
    label = list(range(k))
    bucket: list[list[int]] = [[] for _ in range(k)]

    def evaluate(v: int) -> int:
        if ancestor[v] == -1:
            return v
        path = []
        x = v
        while ancestor[ancestor[x]] != -1:
            path.append(x)
            x = ancestor[x]
        for x in reversed(path):
            a = ancestor[x]
            if semi[label[a]] < semi[label[x]]:
                label[x] = label[a]
            ancestor[x] = ancestor[a]
        return label[v]

    for w in range(k - 1, 0, -1):
        for u0 in pred[vertex[w]]:
            if dfn[u0] == -1:
                continue
            u = evaluate(dfn[u0])
            if semi[u] < semi[w]:
                semi[w] = semi[u]
        bucket[semi[w]].append(w)
        p = parent[w]
        ancestor[w] = p
        for v in bucket[p]:
            u = evaluate(v)
            idom[v] = u if semi[u] < semi[v] else p
        bucket[p] = []
    for w in range(1, k):
        if idom[w] != semi[w]:
            idom[w] = idom[idom[w]]
    result = [-1] * n
    for w in range(1, k):
        result[vertex[w]] = vertex[idom[w]]
    return result


class DominatorTree:
    """The dominator tree of a flow graph.

    The graph is directed and unweighted, with vertices 0 .. n-1 (n >= 1),
    given by a list of edges (a, b) meaning a -> b, and a start vertex root.
    Vertices the root cannot reach are not in the tree. Building takes
    O(m log n) time; dominates(a, b) takes O(1) time.
    """

    def __init__(self, n: int, edges: list[tuple[int, int]], root: int = 0) -> None:
        if n < 1 or not 0 <= root < n:
            raise ValueError("a flow graph needs n >= 1 vertices and a root in range")
        self.n = n
        self.root = root
        self.idom = _immediate_dominators(n, edges, root)  # @line L1
        children: list[list[int]] = [[] for _ in range(n)]
        self.reachable = [False] * n
        self.reachable[root] = True
        for v in range(n):  # @line L2
            if self.idom[v] != -1:
                children[self.idom[v]].append(v)
                self.reachable[v] = True
        self.children = children
        self.tin = [-1] * n
        self.tout = [-1] * n
        self.depth = [-1] * n
        t = 0  # @line L3
        self.depth[root] = 0
        stack = [(root, True)]
        while stack:  # @line L4
            v, entering = stack.pop()  # @line L5
            if entering:  # @line L6
                self.tin[v] = t
                t += 1
                stack.append((v, False))
                for c in reversed(children[v]):
                    self.depth[c] = self.depth[v] + 1
                    stack.append((c, True))
            else:
                self.tout[v] = t  # @line L7

    def dominates(self, a: int, b: int) -> bool:
        """Return True if every path from the root to b passes through a."""
        if not (0 <= a < self.n and 0 <= b < self.n):
            raise IndexError("vertex out of range")
        if not (self.reachable[a] and self.reachable[b]):  # @line L8
            return False
        return self.tin[a] <= self.tin[b] and self.tout[b] <= self.tout[a]  # @line L9

    def dominators(self, v: int) -> list[int]:
        """Return the dominators of v, from v up to the root."""
        if not 0 <= v < self.n:
            raise IndexError("vertex out of range")
        if not self.reachable[v]:
            return []
        out = []
        while v != -1:  # @line L10
            out.append(v)
            v = self.idom[v]
        return out  # @line L11
