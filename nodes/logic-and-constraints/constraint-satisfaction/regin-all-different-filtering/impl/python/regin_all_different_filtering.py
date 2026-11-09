# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regin-all-different-filtering/. The authors are listed in prov/A7F2AJ.jsonl.

from collections import deque
from collections.abc import Hashable, Sequence

Value = Hashable


def _hopcroft_karp(adj: list[list[int]], n_right: int) -> list[int]:
    """Maximum matching of a bipartite graph, left vertices 0..len(adj)-1.

    adj[x] lists the right vertices adjacent to the left vertex x.
    Returns match_left, where match_left[x] is the right partner of x or -1.
    Time O(sqrt(V) E). No recursion: the augmenting search uses a stack.
    """
    n_left = len(adj)
    match_left = [-1] * n_left
    match_right = [-1] * n_right
    inf = n_left + n_right + 1
    while True:
        # BFS from the free left vertices builds the layers.
        dist = [inf] * n_left
        q: deque[int] = deque()
        for x in range(n_left):
            if match_left[x] == -1:
                dist[x] = 0
                q.append(x)
        found = False
        while q:
            x = q.popleft()
            for a in adj[x]:
                y = match_right[a]
                if y == -1:
                    found = True
                elif dist[y] == inf:
                    dist[y] = dist[x] + 1
                    q.append(y)
        if not found:
            return match_left
        # DFS along the layers, with an explicit stack, for each free left vertex.
        ptr = [0] * n_left
        for root in range(n_left):
            if match_left[root] != -1:
                continue
            stack = [root]
            path_values: list[int] = []
            while stack:
                x = stack[-1]
                advanced = False
                while ptr[x] < len(adj[x]):
                    a = adj[x][ptr[x]]
                    ptr[x] += 1
                    y = match_right[a]
                    if y == -1:
                        # Augment along the stack.
                        path_values.append(a)
                        for xx, aa in zip(stack, path_values):
                            match_left[xx] = aa
                            match_right[aa] = xx
                        stack = []
                        advanced = True
                        break
                    if dist[y] == dist[x] + 1:
                        path_values.append(a)
                        stack.append(y)
                        advanced = True
                        break
                if not advanced:
                    dist[x] = inf  # dead vertex for this phase
                    stack.pop()
                    if path_values:
                        path_values.pop()


def _scc_ids(succ: list[list[int]]) -> list[int]:
    """Strongly connected component number of each vertex (iterative Tarjan)."""
    n = len(succ)
    index = [-1] * n
    low = [0] * n
    on_stack = [False] * n
    comp = [-1] * n
    st: list[int] = []
    counter = 0
    ncomp = 0
    for s in range(n):
        if index[s] != -1:
            continue
        work = [(s, 0)]
        index[s] = low[s] = counter
        counter += 1
        st.append(s)
        on_stack[s] = True
        while work:
            v, k = work[-1]
            if k < len(succ[v]):
                work[-1] = (v, k + 1)
                w = succ[v][k]
                if index[w] == -1:
                    index[w] = low[w] = counter
                    counter += 1
                    st.append(w)
                    on_stack[w] = True
                    work.append((w, 0))
                elif on_stack[w]:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    u = work[-1][0]
                    low[u] = min(low[u], low[v])
                if low[v] == index[v]:
                    while True:
                        w = st.pop()
                        on_stack[w] = False
                        comp[w] = ncomp
                        if w == v:
                            break
                    ncomp += 1
    return comp


def regin_all_different_filtering(domains: Sequence[Sequence[Value]]) -> list[list[Value]] | None:
    """Generalized arc consistency for all-different(x_0, ..., x_{n-1}).

    domains[i] is the domain of x_i (duplicates are ignored). Returns the
    filtered domains, in the input order of values, where a value stays if
    and only if some solution of the constraint gives it to its variable.
    Returns None when the constraint has no solution.
    Time O(sqrt(n) E) with E the sum of the domain sizes, so O(n^(3/2) d).
    """
    n = len(domains)
    # L1: the value graph. Values get the numbers 0..k-1.
    vid: dict[Value, int] = {}
    vals: list[Value] = []
    adj: list[list[int]] = []
    for dom in domains:  # @line L1
        row: list[int] = []
        for a in dom:
            if a not in vid:
                vid[a] = len(vals)
                vals.append(a)
            if vid[a] not in row:
                row.append(vid[a])
        adj.append(row)
    k = len(vals)
    match_left = _hopcroft_karp(adj, k)  # @line L2
    if any(m == -1 for m in match_left):  # @line L3
        return None
    match_right = [-1] * k
    for x, a in enumerate(match_left):
        match_right[a] = x
    # L4: vertices 0..n-1 are variables, n..n+k-1 are values.
    succ: list[list[int]] = [[] for _ in range(n + k)]
    for x in range(n):  # @line L4
        for a in adj[x]:
            if match_left[x] == a:
                succ[x].append(n + a)
            else:
                succ[n + a].append(x)
    # L5: values reachable from a free value.
    reach = [False] * (n + k)
    q: deque[int] = deque()
    for a in range(k):  # @line L5
        if match_right[a] == -1:
            reach[n + a] = True
            q.append(n + a)
    while q:
        v = q.popleft()
        for w in succ[v]:
            if not reach[w]:
                reach[w] = True
                q.append(w)
    comp = _scc_ids(succ)  # @line L6
    out: list[list[Value]] = []
    for x in range(n):
        keep: list[Value] = []
        for a in adj[x]:  # @line L7
            if match_left[x] != a and not reach[n + a] and comp[x] != comp[n + a]:  # @line L8
                continue  # @line L9
            keep.append(vals[a])
        out.append(keep)
    return out  # @line L10
