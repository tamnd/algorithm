# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopcroft-tarjan-planarity-test/. The authors are listed in prov/QDYX9D.jsonl.
"""Hopcroft-Tarjan path addition planarity test, decision version.

The graph is given by adjacency lists adj[v] of a simple undirected graph.
No embedding is given or returned: the function only answers whether the
graph is planar. The test follows the formulation of Hopcroft and Tarjan
(1974) in the form of Mehlhorn: split into biconnected components, order the
arcs of a depth-first search by low points, and check each segment for
strong planarity with a stack of blocks of attachments.

Recursion is replaced by explicit stacks, so deep graphs are fine.
"""

# Attachment lists are singly linked lists sorted in decreasing order, so
# that the head is the largest attachment and the tail the smallest.
# They are stored in two global arrays and handled as [head, tail] pairs.


class _Lists:
    def __init__(self):
        self.val = []
        self.nxt = []

    def single(self, x):
        self.val.append(x)
        self.nxt.append(-1)
        i = len(self.val) - 1
        return [i, i]

    def concat(self, a, b):
        """Append list b to list a (in place on a) and return a."""
        if b[0] == -1:
            return a
        if a[0] == -1:
            a[0], a[1] = b[0], b[1]
            return a
        self.nxt[a[1]] = b[0]
        a[1] = b[1]
        return a

    def pop_head(self, a):
        i = a[0]
        a[0] = self.nxt[i]
        if a[0] == -1:
            a[1] = -1


def _check_simple(adj):
    n = len(adj)
    for v in range(n):
        seen = set()
        for w in adj[v]:
            if not 0 <= w < n or w == v or w in seen:
                raise ValueError("graph must be simple, without loops")
            seen.add(w)
    for v in range(n):
        for w in adj[v]:
            if v not in adj[w]:
                raise ValueError("adjacency lists must be symmetric")


def _blocks(adj):
    """Biconnected components with at least 5 vertices, as lists of edges.
    Iterative Hopcroft-Tarjan biconnectivity with an edge stack."""
    n = len(adj)
    num = [-1] * n
    low = [0] * n
    out = []
    counter = 0
    for r in range(n):
        if num[r] != -1:
            continue
        num[r] = low[r] = counter
        counter += 1
        estack = []
        stack = [(r, -1, 0)]
        while stack:
            v, p, i = stack[-1]
            if i < len(adj[v]):
                stack[-1] = (v, p, i + 1)
                w = adj[v][i]
                if num[w] == -1:
                    num[w] = low[w] = counter
                    counter += 1
                    estack.append((v, w))
                    stack.append((w, v, 0))
                elif w != p and num[w] < num[v]:
                    estack.append((v, w))
                    if num[w] < low[v]:
                        low[v] = num[w]
            else:
                stack.pop()
                if p == -1:
                    continue
                if low[v] < low[p]:
                    low[p] = low[v]
                if low[v] >= num[p]:
                    comp = []
                    while True:
                        e = estack.pop()
                        comp.append(e)
                        if e == (p, v):
                            break
                    out.append(comp)
    return out


def _strongly_planar_block(edges):
    """Test a biconnected graph, given as a list of edges, for planarity."""
    label = {}
    for u, v in edges:
        for x in (u, v):
            if x not in label:
                label[x] = len(label)
    k = len(label)
    if k <= 4:
        return True
    if len(edges) > 3 * k - 6:
        return False
    nb = [[] for _ in range(k)]
    for u, v in edges:
        nb[label[u]].append(label[v])
        nb[label[v]].append(label[u])

    # Depth-first search; vertices are renamed by their DFS number.  # @line L3
    num = [-1] * k
    parent = [-1] * k
    num[0] = 0
    order = [0]
    stack = [(0, 0)]
    while stack:
        v, i = stack[-1]
        if i < len(nb[v]):
            stack[-1] = (v, i + 1)
            w = nb[v][i]
            if num[w] == -1:
                num[w] = len(order)
                order.append(w)
                parent[w] = v
                stack.append((w, 0))
        else:
            stack.pop()
    par = [-1] * k
    tree = [[] for _ in range(k)]
    back = [[] for _ in range(k)]
    for v in range(k):
        dv = num[v]
        if parent[v] != -1:
            par[dv] = num[parent[v]]
            tree[num[parent[v]]].append(dv)
        for w in nb[v]:
            dw = num[w]
            if dw < dv and dw != par[dv]:
                back[dv].append(dw)

    # Low points: lowpt1 is the smallest vertex reachable from the subtree
    # by one back arc (or the vertex itself), lowpt2 the second smallest.  # @line L4
    l1 = list(range(k))
    l2 = list(range(k))
    for v in range(k - 1, -1, -1):
        a, b = v, v
        for w in back[v]:
            if w < a:
                a, b = w, a
            elif a < w < b:
                b = w
        for c in tree[v]:
            if l1[c] < a:
                a, b = l1[c], min(a, l2[c])
            elif l1[c] == a:
                b = min(b, l2[c])
            else:
                b = min(b, l1[c])
        l1[v], l2[v] = a, b

    # Order the arcs out of each vertex by cost with a bucket sort.  # @line L5
    buckets = [[] for _ in range(2 * k + 2)]
    for v in range(k):
        for c in tree[v]:
            cost = 2 * l1[c] + (1 if l2[c] < v else 0)
            buckets[cost].append((v, c))
        for w in back[v]:
            buckets[2 * w].append((v, w))
    adj = [[] for _ in range(k)]
    for bucket in buckets:
        for v, w in bucket:
            adj[v].append(w)

    lists = _Lists()

    def spine(y):  # @line L8
        wk = y
        while adj[wk][0] > wk:
            wk = adj[wk][0]
        return wk, adj[wk][0]

    def add_block(S, A):
        B = [A, [-1, -1]]  # [left, right] attachments  # @line L17
        while True:  # @line L18
            if S and S[-1][0][0] != -1 and lists.val[B[0][1]] < lists.val[S[-1][0][0]]:
                S[-1][0], S[-1][1] = S[-1][1], S[-1][0]  # @line L19
            if S and S[-1][0][0] != -1 and lists.val[B[0][1]] < lists.val[S[-1][0][0]]:
                return False  # @line L20
            if S and S[-1][1][0] != -1 and lists.val[B[0][1]] < lists.val[S[-1][1][0]]:
                T = S.pop()  # @line L21
                lists.concat(B[0], T[0])
                lists.concat(B[1], T[1])
            else:
                break  # @line L22
        S.append(B)  # @line L23
        return True

    # A frame is [x, w0, w, i, S]: segment of the tree arc into the spine
    # x -> ... -> w (current vertex), its lowest attachment w0, the next
    # arc index i at w, and the stack S of blocks.
    y0 = adj[0][0]
    wk, w0 = spine(y0)
    frames = [[0, w0, wk, 1, []]]  # @line L9
    result = None
    while frames:
        f = frames[-1]
        if result is not None:
            if not add_block(f[4], result):  # @line L13
                return False
            result = None
        pushed = False
        while f[2] != f[0]:  # @line L10
            w = f[2]
            if f[3] < len(adj[w]):  # @line L11
                t = adj[w][f[3]]
                f[3] += 1
                if t > w:  # tree arc: test its segment first  # @line L12
                    sk, s0 = spine(t)
                    frames.append([w, s0, sk, 1, []])
                    pushed = True
                    break
                if not add_block(f[4], lists.single(t)):  # @line L13
                    return False
            else:
                p = par[w]  # @line L14
                S = f[4]
                while S:
                    L, R = S[-1]
                    while L[0] != -1 and lists.val[L[0]] == p:
                        lists.pop_head(L)
                    while R[0] != -1 and lists.val[R[0]] == p:
                        lists.pop_head(R)
                    if L[0] == -1 and R[0] == -1:
                        S.pop()
                    else:
                        break
                f[2] = p
                f[3] = 1
        if pushed:
            continue
        # The spine is done: collect the attachments of the segment.
        x, s0, S = f[0], f[1], f[4]
        att = [-1, -1]
        while S:
            L, R = S.pop()
            hl = lists.val[L[0]] if L[0] != -1 else -1
            hr = lists.val[R[0]] if R[0] != -1 else -1
            if hl > s0 and hr > s0:
                return False  # @line L15
            lists.concat(att, R if hr > s0 else L)  # @line L16
        if s0 != x:
            lists.concat(att, lists.single(s0))
        frames.pop()
        result = att
    return True  # @line L6


def is_planar(adj):
    """Return True if the simple graph with adjacency lists adj is planar."""
    _check_simple(adj)
    n = len(adj)
    m = sum(len(a) for a in adj) // 2
    if n >= 3 and m > 3 * n - 6:  # @line L1
        return False
    for comp in _blocks(adj):  # @line L2
        if not _strongly_planar_block(comp):  # @line L6
            return False
    return True  # @line L7
