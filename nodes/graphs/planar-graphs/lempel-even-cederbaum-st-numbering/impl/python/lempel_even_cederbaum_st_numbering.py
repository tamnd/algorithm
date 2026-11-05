# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lempel-even-cederbaum-st-numbering/. The authors are listed in prov/SJ9RE7.jsonl.
"""st-numbering of a 2-connected graph in linear time.

This is the depth-first version of Even and Tarjan in the streamlined form of
Tarjan (1986): one DFS computes low points, then each vertex is inserted
into a linked list just before or just after its DFS parent.

The graph is given by adjacency lists adj[v]. No embedding is needed. The
edge st is treated as present even if adj lacks it.
"""


def st_numbering(adj, s, t):
    """Return num with num[s] = 1, num[t] = n, and every other vertex having
    a neighbour with a smaller and one with a larger number.

    Raises ValueError if s == t, or if the graph plus the edge st is not
    2-connected.
    """
    n = len(adj)
    if s == t or not (0 <= s < n and 0 <= t < n):
        raise ValueError("need two different vertices s and t")
    pre = [-1] * n
    parent = [-1] * n
    low = [0] * n  # low[v] is a preorder number
    order = []
    pre[s] = 0
    order.append(s)
    # the DFS from s takes the edge st first, so t is the only child of s
    pre[t] = 1  # @line L1
    parent[t] = s
    order.append(t)
    low[s], low[t] = 0, 1
    stack = [(t, iter(adj[t]))]
    while stack:
        v, it = stack[-1]
        advanced = False
        for w in it:
            if pre[w] == -1:
                pre[w] = len(order)
                parent[w] = v
                low[w] = pre[w]
                order.append(w)
                stack.append((w, iter(adj[w])))
                advanced = True
                break
            if w != parent[v] and pre[w] < low[v]:
                low[v] = pre[w]
        if advanced:
            continue
        stack.pop()
        if parent[v] != -1 and low[v] < low[parent[v]]:
            low[parent[v]] = low[v]
    if len(order) != n:
        raise ValueError("graph is not connected")  # @line L2
    for v in order[2:]:
        if low[v] >= pre[parent[v]]:
            raise ValueError("graph plus st is not 2-connected")
    minus, plus = False, True
    sign = [plus] * n
    nxt = [-1] * n
    prv = [-1] * n
    nxt[s], prv[t] = t, s  # @line L3
    sign[s] = minus
    for v in order[2:]:  # @line L4
        p = parent[v]
        if sign[order[low[v]]] == minus:  # @line L5
            a = prv[p]  # @line L6
            nxt[a], prv[v], nxt[v], prv[p] = v, a, p, v
            sign[p] = plus
        else:  # @line L7
            b = nxt[p]  # @line L8
            nxt[p], prv[v], nxt[v] = v, p, b
            if b != -1:
                prv[b] = v
            sign[p] = minus
    num = [0] * n
    v, k = s, 1
    while v != -1:  # @line L9
        num[v] = k
        k += 1
        v = nxt[v]
    return num  # @line L10
