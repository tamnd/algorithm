# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boyer-myrvold-planarity-test/. The authors are listed in prov/1RE4H8.jsonl.
"""Boyer-Myrvold edge addition planarity test.

Input: adjacency lists adj[v] of a simple undirected graph on 0..n-1.
No embedding is given. Output of planar_embedding: a rotation system
rot[v], the neighbours of v in counterclockwise order, or None if the
graph is not planar.

The code follows Boyer and Myrvold (2004): vertices are processed in
decreasing DFS order; Walkup marks the pertinent part of the embedding for
the back edges into v, and Walkdown adds those back edges along the
external faces of the biconnected components, merging components at cut
vertices. Flips are lazy: a flipped component gets sign -1 on its root
tree edge, and one pass at the end fixes the orientation of every list.
The short-circuit edges of the paper are left out; they do not change the
result. Everything is iterative.

kuratowski_subgraph returns the edges of a subdivision of K5 or K3,3 for
a non-planar graph. It deletes edges while the graph stays non-planar,
which takes O(m) runs of the test; the paper's isolator does it in linear
time but is much longer.
"""


def _check_simple(adj):
    n = len(adj)
    for v in range(n):
        seen = set()
        for w in adj[v]:
            if not 0 <= w < n or w == v or w in seen:
                raise ValueError("graph must be simple, without loops")
            seen.add(w)
        for w in adj[v]:
            if v not in adj[w]:
                raise ValueError("adjacency lists must be symmetric")


def planar_embedding(adj):
    """Return a planar rotation system of the graph, or None."""
    _check_simple(adj)
    n = len(adj)
    m = sum(len(a) for a in adj) // 2
    if n >= 3 and m > 3 * n - 6:  # @line L1
        return None
    if n == 0:
        return []

    # Depth-first search: dfi, parent, lowpoint, least ancestor.  # @line L2
    dfi = [-1] * n
    vert = []
    par = [-1] * n  # in DFI labels
    nb = [None] * n  # neighbours in DFI labels, filled below
    for r in range(n):
        if dfi[r] != -1:
            continue
        dfi[r] = len(vert)
        vert.append(r)
        stack = [(r, 0)]
        while stack:
            u, i = stack[-1]
            if i < len(adj[u]):
                stack[-1] = (u, i + 1)
                x = adj[u][i]
                if dfi[x] == -1:
                    dfi[x] = len(vert)
                    vert.append(x)
                    par[dfi[x]] = dfi[u]
                    stack.append((x, 0))
            else:
                stack.pop()
    for v in range(n):
        nb[v] = [dfi[x] for x in adj[vert[v]]]
    children = [[] for _ in range(n)]
    for v in range(n):
        if par[v] != -1:
            children[par[v]].append(v)
    least = list(range(n))  # least ancestor by a direct back edge
    fwd = [[] for _ in range(n)]  # descendants w with a back edge (w, v)
    for v in range(n):
        for w in nb[v]:
            if w < v and w != par[v]:
                if w < least[v]:
                    least[v] = w
            elif w > v and par[w] != v:
                fwd[v].append(w)
    low = least[:]
    for v in range(n - 1, -1, -1):
        p = par[v]
        if p != -1 and low[v] < low[p]:
            low[p] = low[v]
    buckets = [[] for _ in range(n)]
    for c in range(n):
        if par[c] != -1:
            buckets[low[c]].append(c)
    sep = [[] for _ in range(n)]  # children sorted by lowpoint
    for b in buckets:
        for c in b:
            sep[par[c]].append(c)
    sp = [0] * n
    merged = [False] * n

    # Embedding structure. Nodes 0..n-1 are vertices, n + c is the root
    # copy of par[c] in the component of the tree edge (par[c], c).
    N = 2 * n
    head = [[-1] * N, [-1] * N]  # the two ends of each adjacency list
    to = []
    lk = [[], []]  # lk[s][a]: the neighbour of arc a toward end s
    sign = [1] * n

    def new_arc_pair(x, y):
        to.extend((y, x))
        lk[0].extend((-1, -1))
        lk[1].extend((-1, -1))
        return len(to) - 2

    def insert(x, a, s):
        h = head[s][x]
        lk[s][a] = -1
        lk[1 - s][a] = h
        if h == -1:
            head[1 - s][x] = a
        else:
            lk[s][h] = a
        head[s][x] = a

    def ext_next(x, e):
        """Leave x on the side other than e; return (y, side of arrival).
        If y has one arc, both sides are that arc, and the walk keeps its
        side, as it would in a consistently oriented component."""
        a = head[1 - e][x]
        y = to[a]
        b = a ^ 1
        if head[0][y] == head[1][y]:
            return y, e
        return y, (0 if head[0][y] == b else 1)

    for c in range(n):  # @line L3
        if par[c] != -1:
            a = new_arc_pair(n + c, c)
            insert(n + c, a, 0)
            insert(c, a ^ 1, 0)

    bflag = [-1] * n
    visited = [-1] * N
    pr = [[] for _ in range(n)]  # pertinent roots: internal first, then external
    pr_head = [0] * n

    def ext_active(w, v):
        if least[w] < v:
            return True
        s = sep[w]
        i = sp[w]
        while i < len(s) and merged[s[i]]:
            i += 1
        sp[w] = i
        return i < len(s) and low[s[i]] < v

    def pertinent(w, v):
        return bflag[w] == v or pr_head[w] < len(pr[w])

    def first_active(rc, e, v):
        """First vertex on the external face from root rc, leaving on the
        side other than e, that is pertinent or externally active."""
        y, ye = ext_next(rc, e)
        while y != rc and not pertinent(y, v) and not ext_active(y, v):
            y, ye = ext_next(y, ye)
        return y, ye

    def walkup(v, w):
        bflag[w] = v  # @line L11
        x = w
        while True:
            if visited[x] == v:
                return
            visited[x] = v
            zig = (x, 1)
            zag = (x, 0)
            root = -1
            while root == -1:  # @line L12
                for k in range(2):
                    y, e = ext_next(*(zig if k == 0 else zag))
                    if y >= n:
                        root = y
                        break
                    if visited[y] == v:
                        return
                    visited[y] = v
                    if k == 0:
                        zig = (y, e)
                    else:
                        zag = (y, e)
            if visited[root] == v:
                return
            visited[root] = v
            c = root - n
            p = par[c]
            if p == v:
                return
            lst = pr[p]
            if low[c] < v:  # externally active component goes last  # @line L13
                lst.append(root)
            else:  # internally active component goes first
                if pr_head[p] > 0:
                    pr_head[p] -= 1
                    lst[pr_head[p]] = root
                else:
                    lst.insert(0, root)
            x = p

    def merge(u, ue, rc, dc):
        c = rc - n
        if dc == ue:  # flip the child component  # @line L24
            a = head[0][rc]
            while a != -1:
                nxt = lk[1][a]
                lk[0][a], lk[1][a] = lk[1][a], lk[0][a]
                a = nxt
            head[0][rc], head[1][rc] = head[1][rc], head[0][rc]
            sign[c] = -1
        a = head[0][rc]
        while a != -1:
            to[a ^ 1] = u
            a = lk[1][a]
        s = ue  # @line L25
        hu = head[s][u]
        lk[s][hu] = head[1 - s][rc]
        lk[1 - s][head[1 - s][rc]] = hu
        head[s][u] = head[s][rc]
        head[0][rc] = head[1][rc] = -1
        pr_head[u] += 1
        merged[c] = True

    def walkdown(v, R):
        for d in (0, 1):  # @line L14
            stack = []
            w, e = ext_next(R, 1 - d)  # @line L15
            while w != R:  # @line L16
                if w >= n:
                    break
                if bflag[w] == v:  # @line L17
                    while stack:
                        u, ue, rc, dc = stack.pop()
                        merge(u, ue, rc, dc)
                    a = new_arc_pair(R, w)
                    insert(R, a, d)
                    insert(w, a ^ 1, e)
                    bflag[w] = -1
                if pr_head[w] < len(pr[w]):  # @line L18
                    rc = pr[w][pr_head[w]]
                    x, xe = first_active(rc, 1, v)  # @line L19
                    y, ye = first_active(rc, 0, v)
                    if pertinent(x, v) and not ext_active(x, v):
                        choice = (x, xe, 0)
                    elif pertinent(y, v) and not ext_active(y, v):
                        choice = (y, ye, 1)
                    elif pertinent(x, v):
                        choice = (x, xe, 0)
                    else:
                        choice = (y, ye, 1)
                    stack.append((w, e, rc, choice[2]))  # @line L20
                    w, e = choice[0], choice[1]
                elif not ext_active(w, v):  # inactive: skip it  # @line L21
                    w, e = ext_next(w, e)
                else:  # stopping vertex  # @line L22
                    break
            if stack:  # @line L23
                return

    for v in range(n - 1, -1, -1):  # @line L4
        for w in fwd[v]:
            walkup(v, w)  # @line L5
        for c in children[v]:
            walkdown(v, n + c)  # @line L6
        for w in fwd[v]:
            if bflag[w] == v:  # a back edge was not embedded  # @line L7
                return None

    # Join the remaining components at their cut vertices.  # @line L8
    for c in range(n):
        if par[c] != -1 and not merged[c]:
            u, rc = par[c], n + c
            a = head[0][rc]
            while a != -1:
                to[a ^ 1] = u
                a = lk[1][a]
            if head[0][u] == -1:
                head[0][u], head[1][u] = head[0][rc], head[1][rc]
            else:
                lk[1][head[1][u]] = head[0][rc]
                lk[0][head[0][rc]] = head[1][u]
                head[1][u] = head[1][rc]

    # Fix orientations: a vertex is reversed if the product of signs on
    # its tree path is -1.  # @line L9
    orient = [1] * n
    rot = [None] * n
    for v in range(n):
        if par[v] != -1:
            orient[v] = orient[par[v]] * sign[v]
        lst = []
        a = head[0][v]
        while a != -1:
            lst.append(vert[to[a]])
            a = lk[1][a]
        if orient[v] == -1:
            lst.reverse()
        rot[vert[v]] = lst
    return rot  # @line L10


def is_planar(adj):
    return planar_embedding(adj) is not None


def kuratowski_subgraph(adj):
    """Return the edge list of a subdivision of K5 or K3,3 in a non-planar
    graph, or None if the graph is planar."""
    if is_planar(adj):
        return None
    n = len(adj)
    cur = [set(a) for a in adj]
    edges = [(u, w) for u in range(n) for w in adj[u] if u < w]
    for u, w in edges:
        cur[u].discard(w)
        cur[w].discard(u)
        if planar_embedding([sorted(s) for s in cur]) is not None:
            cur[u].add(w)
            cur[w].add(u)
    return [(u, w) for u in range(n) for w in cur[u] if u < w]
