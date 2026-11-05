# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johnson-elementary-cycles-algorithm/. The authors are listed in prov/S5MRH3.jsonl.


def _least_nontrivial_scc(adj: list[list[int]], s: int) -> list[int] | None:
    """Strong component of G[s .. n-1] with the least vertex among those that have a cycle.

    Iterative Tarjan algorithm restricted to the vertices s .. n-1. A component has a
    cycle if it has two or more vertices or a self-loop. Time O(n + m).
    """
    n = len(adj)
    index = [-1] * n
    low = [0] * n
    on = [False] * n
    comp: list[int] = []
    best: list[int] | None = None
    counter = 0
    for root in range(s, n):
        if index[root] >= 0:
            continue
        work = [(root, 0)]
        index[root] = low[root] = counter
        counter += 1
        comp.append(root)
        on[root] = True
        while work:
            v, i = work[-1]
            if i < len(adj[v]):
                work[-1] = (v, i + 1)
                w = adj[v][i]
                if w < s:
                    continue
                if index[w] < 0:
                    index[w] = low[w] = counter
                    counter += 1
                    comp.append(w)
                    on[w] = True
                    work.append((w, 0))
                elif on[w]:
                    low[v] = min(low[v], index[w])
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                scc = []
                while True:
                    w = comp.pop()
                    on[w] = False
                    scc.append(w)
                    if w == v:
                        break
                if len(scc) > 1 or v in adj[v]:
                    if best is None or min(scc) < min(best):
                        best = scc
    return best


def johnson_elementary_cycles_algorithm(adj: list[list[int]]) -> list[list[int]]:
    """Return every elementary cycle of the directed graph, each one time.

    The graph has the vertices 0 .. n-1 and the adjacency lists adj; parallel arcs are
    merged, since a cycle is reported by its vertices, and a self-loop at v is the cycle
    [v]. Each cycle [v0, v1, ..., vk-1] starts at its least vertex v0 and has the arcs
    v0 -> v1 -> ... -> vk-1 -> v0. Time O((n + m)(c + 1)) for c cycles, extra space
    O(n + m) besides the output.
    """
    n = len(adj)
    succ = [sorted(set(a)) for a in adj]
    out: list[list[int]] = []
    blocked = [False] * n
    bset: list[set[int]] = [set() for _ in range(n)]
    s = 0  # @line L1
    while s < n:  # @line L2
        comp = _least_nontrivial_scc(succ, s)  # @line L3
        if comp is None:  # @line L4
            break
        s = min(comp)  # @line L5
        member = [False] * n
        for v in comp:  # @line L6
            member[v] = True
            blocked[v] = False
            bset[v].clear()
        ak = [[w for w in succ[v] if member[w]] if member[v] else [] for v in range(n)]
        # CIRCUIT(s) with an explicit stack of frames [v, next index, found]
        path = [s]  # @line L7
        blocked[s] = True  # @line L9
        frames = [[s, 0, False]]
        while frames:
            fr = frames[-1]
            v = fr[0]
            if fr[1] < len(ak[v]):  # @line L10
                w = ak[v][fr[1]]
                fr[1] += 1
                if w == s:  # @line L11
                    out.append(list(path))
                    fr[2] = True
                elif not blocked[w]:  # @line L12
                    path.append(w)
                    blocked[w] = True  # @line L9
                    frames.append([w, 0, False])
                continue
            if fr[2]:  # @line L13
                todo = [v]  # UNBLOCK(v), iteratively
                while todo:
                    u = todo.pop()
                    blocked[u] = False  # @line L16
                    for x in bset[u]:  # @line L17
                        if blocked[x]:
                            todo.append(x)
                    bset[u].clear()
            else:  # @line L14
                for w in ak[v]:
                    bset[w].add(v)
            frames.pop()  # @line L15
            path.pop()
            if frames and fr[2]:
                frames[-1][2] = True
        s += 1  # @line L8
    return out
