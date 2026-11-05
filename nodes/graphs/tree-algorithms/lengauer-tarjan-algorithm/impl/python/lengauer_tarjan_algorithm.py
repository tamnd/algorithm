# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lengauer-tarjan-algorithm/. The authors are listed in prov/206HCM.jsonl.


def _run(n: int, edges: list[tuple[int, int]], root: int) -> tuple[list[int], list[int]]:
    if n < 1 or not 0 <= root < n:
        raise ValueError("a flow graph needs n >= 1 vertices and a root in range")
    succ: list[list[int]] = [[] for _ in range(n)]
    pred: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        if not (0 <= a < n and 0 <= b < n):
            raise ValueError("edge endpoint out of range")
        succ[a].append(b)
        pred[b].append(a)

    # L1: iterative depth-first search; vertices are renamed by preorder number.
    dfn = [-1] * n  # @line L1
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
    preds = [[dfn[u] for u in pred[vertex[i]] if dfn[u] != -1] for i in range(k)]

    semi = list(range(k))  # @line L2
    label = list(range(k))
    ancestor = [-1] * k
    idom = [0] * k
    bucket: list[list[int]] = [[] for _ in range(k)]

    def evaluate(v: int) -> int:
        if ancestor[v] == -1:  # @line L12
            return v
        path = []  # @line L13
        x = v
        while ancestor[ancestor[x]] != -1:  # @line L14
            path.append(x)
            x = ancestor[x]
        for x in reversed(path):  # @line L15
            a = ancestor[x]
            if semi[label[a]] < semi[label[x]]:
                label[x] = label[a]
            ancestor[x] = ancestor[a]
        return label[v]

    for w in range(k - 1, 0, -1):  # @line L3
        for v in preds[w]:  # @line L4
            u = evaluate(v)  # @line L5
            if semi[u] < semi[w]:
                semi[w] = semi[u]
        bucket[semi[w]].append(w)  # @line L6
        p = parent[w]
        ancestor[w] = p
        for v in bucket[p]:  # @line L7
            u = evaluate(v)  # @line L8
            idom[v] = u if semi[u] < semi[v] else p
        bucket[p] = []  # @line L9
    for w in range(1, k):  # @line L10
        if idom[w] != semi[w]:  # @line L11
            idom[w] = idom[idom[w]]

    idom_out = [-1] * n
    semi_out = [-1] * n
    for w in range(1, k):
        idom_out[vertex[w]] = vertex[idom[w]]
        semi_out[vertex[w]] = vertex[semi[w]]
    return idom_out, semi_out


def lengauer_tarjan(n: int, edges: list[tuple[int, int]], root: int = 0) -> list[int]:
    """Immediate dominators of a flow graph, by the simple Lengauer-Tarjan algorithm.

    The graph is directed and unweighted, with vertices 0 .. n-1 (n >= 1) and
    edges (a, b) meaning a -> b; self-loops and parallel edges are allowed.
    Returns idom with idom[root] = -1 and idom[v] = -1 for every vertex that
    root cannot reach. Time O(m log n), no recursion.
    """
    return _run(n, edges, root)[0]


def semidominators(n: int, edges: list[tuple[int, int]], root: int = 0) -> list[int]:
    """Semidominators, as vertex labels, for the depth-first search that visits
    successors in the order of the edge list; -1 for the root and unreachable
    vertices."""
    return _run(n, edges, root)[1]
