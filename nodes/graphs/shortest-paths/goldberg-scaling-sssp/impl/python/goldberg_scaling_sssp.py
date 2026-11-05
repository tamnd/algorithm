# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldberg-scaling-sssp/. The authors are listed in prov/A13K1H.jsonl.

import heapq
import math

INF = math.inf


def goldberg_scaling(
    adj: list[list[tuple[int, int]]], s: int, trace: list | None = None
) -> tuple[list, list] | None:
    """Single-source shortest paths with integer weights, by Goldberg's scaling method.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u, and
    every w must be an integer (negative allowed). Returns (d, parent) with d[v] the
    distance from s (math.inf if unreachable) and parent[v] the previous vertex on a
    shortest path, or None if a negative cycle is reachable from s. Negative cycles
    that s does not reach are ignored. If trace is a list, one entry
    (scale, case, number of vertices fixed) is appended per refinement step.
    """
    n = len(adj)
    for u in range(n):
        for _, w in adj[u]:
            if not isinstance(w, int):
                raise ValueError("weights must be integers")
    # restrict to the vertices reachable from s
    seen = [False] * n  # @line L1
    seen[s] = True
    stack = [s]
    while stack:
        u = stack.pop()
        for v, _ in adj[u]:
            if not seen[v]:
                seen[v] = True
                stack.append(v)
    edges = [(u, v, w) for u in range(n) if seen[u] for v, w in adj[u]]
    big = max([-w for _, _, w in edges] + [0])
    b = big.bit_length()
    p = [0] * n
    for i in range(1, b + 1):  # @line L2
        shift = b - i
        wi = [-((-w) >> shift) for _, _, w in edges]  # ceil(w / 2^shift)
        p = [2 * x for x in p]  # @line L3
        if not _refine(n, edges, wi, p, seen, i, trace):
            return None
    # all reduced costs are now >= 0: Dijkstra, then undo the potentials
    radj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        radj[u].append((v, w + p[u] - p[v]))
    dr = [INF] * n
    parent: list = [None] * n
    dr[s] = 0
    heap = [(0, s)]
    while heap:  # @line L11
        du, u = heapq.heappop(heap)
        if du > dr[u]:
            continue
        for v, r in radj[u]:
            if du + r < dr[v]:
                dr[v], parent[v] = du + r, u
                heapq.heappush(heap, (dr[v], v))
    d = [dr[v] - p[s] + p[v] if dr[v] < INF else INF for v in range(n)]
    return d, parent


def _refine(n, edges, wi, p, live, scale, trace) -> bool:
    """Make every reduced cost wi + p[u] - p[v] (all >= -1) nonnegative by changing p.

    Returns False if it finds that the weights wi have a negative cycle."""
    out: list[list[int]] = [[] for _ in range(n)]
    for e, (u, _, _) in enumerate(edges):
        out[u].append(e)

    def cost(e):
        u, v, _ = edges[e]
        return wi[e] + p[u] - p[v]

    while True:
        improvable = {edges[e][1] for e in range(len(edges)) if cost(e) == -1}  # @line L4
        k = len(improvable)
        if k == 0:
            return True
        comp, order = _scc(n, out, edges, cost, live)  # @line L5
        for e in range(len(edges)):
            u, v, _ = edges[e]
            if comp[u] == comp[v] and cost(e) == -1:
                return False
        # layers: d(C) = least admissible-path cost ending in component C
        dc = [0] * len(order)  # @line L6
        via: list = [None] * len(order)  # the -1 or 0 edge that achieves dc
        for c in range(len(order)):  # topological order of the components
            for u in order[c]:
                for e in out[u]:
                    v = edges[e][1]
                    ce = cost(e)
                    if ce <= 0 and comp[v] != c and dc[c] + ce < dc[comp[v]]:
                        dc[comp[v]], via[comp[v]] = dc[c] + ce, e
        layer: dict[int, int] = {}
        for v in improvable:
            layer[dc[comp[v]]] = layer.get(dc[comp[v]], 0) + 1
        j, size = min(layer.items(), key=lambda kv: (-kv[1], kv[0]))
        if size * size >= k:  # @line L7
            for v in range(n):
                if live[v] and dc[comp[v]] <= j:
                    p[v] -= 1
            if trace is not None:
                trace.append((scale, "cut", size))
            continue
        # a path whose -1 edges enter x_1, ..., x_L: walk back from the deepest component
        c = min(range(len(order)), key=lambda c: dc[c])  # @line L8
        xs = []
        while via[c] is not None:
            e = via[c]
            if cost(e) == -1:
                xs.append(edges[e][1])
            c = comp[edges[e][0]]
        xs.reverse()
        big_l = len(xs)
        # D(v) = min(0, min_j dist+(x_j, v) - j), with lengths max(cost, 0), by buckets
        lab = [0] * n
        for jj, x in enumerate(xs, start=1):
            lab[x] = min(lab[x], -jj)
        buckets: list[list[int]] = [[] for _ in range(big_l + 1)]
        for v in range(n):
            if live[v]:
                buckets[lab[v] + big_l].append(v)
        done = [False] * n
        for level in range(-big_l, 1):
            for u in buckets[level + big_l]:
                if done[u] or lab[u] != level:
                    continue
                done[u] = True
                for e in out[u]:
                    v = edges[e][1]
                    nl = level + max(cost(e), 0)
                    if nl < lab[v]:
                        lab[v] = nl
                        buckets[nl + big_l].append(v)
        for v in range(n):
            if live[v]:
                p[v] += lab[v]  # @line L9
        for x in xs:  # @line L10
            for e in range(len(edges)):
                if edges[e][1] == x and cost(e) == -1:
                    return False  # only possible with a negative cycle
        if trace is not None:
            trace.append((scale, "path", big_l))


def _scc(n, out, edges, cost, live):
    """Strongly connected components of the admissible graph (cost <= 0), by Tarjan.

    Returns comp[v] and the components as vertex lists in topological order."""
    index = [-1] * n
    low = [0] * n
    on = [False] * n
    comp = [-1] * n
    st: list[int] = []
    comps: list[list[int]] = []
    counter = 0
    for r in range(n):
        if not live[r] or index[r] != -1:
            continue
        work = [(r, 0)]
        index[r] = low[r] = counter
        counter += 1
        st.append(r)
        on[r] = True
        while work:
            u, k = work[-1]
            if k < len(out[u]):
                work[-1] = (u, k + 1)
                e = out[u][k]
                if cost(e) > 0:
                    continue
                v = edges[e][1]
                if index[v] == -1:
                    index[v] = low[v] = counter
                    counter += 1
                    st.append(v)
                    on[v] = True
                    work.append((v, 0))
                elif on[v]:
                    low[u] = min(low[u], index[v])
            else:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[u])
                if low[u] == index[u]:
                    members = []
                    while True:
                        x = st.pop()
                        on[x] = False
                        comp[x] = len(comps)
                        members.append(x)
                        if x == u:
                            break
                    comps.append(members)
    # Tarjan finds components in reverse topological order
    m = len(comps)
    comp = [m - 1 - c if c != -1 else -1 for c in comp]
    return comp, comps[::-1]
