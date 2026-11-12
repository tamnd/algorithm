# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-throughput-routing/. The authors are listed in prov/NC7YNV.jsonl.
"""Maximum concurrent flow: the largest lam such that lam * d_j can be routed for every commodity j.

A network is n nodes and a list of directed edges (u, v) with capacities. A commodity is
(s, t, d). garg_konemann is the (1 - eps)^3 approximation of Garg and Konemann; exact_lp
solves the path formulation exactly with Fractions, as a reference for small networks.
"""

import heapq
import math
from collections import deque
from fractions import Fraction


def shortest_path(n, edges, length, s, t):
    """Dijkstra. Returns the list of edge indices of a shortest s-t path, or None."""
    out = [[] for _ in range(n)]
    for j, (u, v) in enumerate(edges):
        out[u].append(j)
    dist = [math.inf] * n
    via = [None] * n
    dist[s] = 0.0
    heap = [(0.0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == t:
            break
        for j in out[u]:
            v = edges[j][1]
            nd = d + length[j]
            if nd < dist[v]:
                dist[v], via[v] = nd, j
                heapq.heappush(heap, (nd, v))
    if dist[t] == math.inf:
        return None
    path, v = [], t
    while v != s:
        j = via[v]
        path.append(j)
        v = edges[j][0]
    return path[::-1]


def max_flow(n, edges, cap, s, t):
    """Edmonds-Karp on the directed edges, for the single-commodity bound."""
    res = {}
    adj = [set() for _ in range(n)]
    for (u, v), c in zip(edges, cap):
        res[(u, v)] = res.get((u, v), 0) + c
        res.setdefault((v, u), 0)
        adj[u].add(v)
        adj[v].add(u)
    total = 0
    while True:
        parent = {s: None}
        queue = deque([s])
        while queue and t not in parent:
            u = queue.popleft()
            for v in adj[u]:
                if v not in parent and res[(u, v)] > 0:
                    parent[v] = u
                    queue.append(v)
        if t not in parent:
            return total
        path, v = [], t
        while parent[v] is not None:
            path.append((parent[v], v))
            v = parent[v]
        b = min(res[e] for e in path)
        for u, v in path:
            res[(u, v)] -= b
            res[(v, u)] += b
        total += b


def garg_konemann(n, edges, cap, commodities, eps):
    """Approximate maximum concurrent flow.

    Returns (lam, flow, routed): flow[j][e] is the flow of commodity j on edge e, the flows
    together respect the capacities, and commodity j carries routed[j] >= lam * d_j."""
    m, k = len(edges), len(commodities)
    # Scale demands so that 1 <= OPT <= k, which bounds the number of phases.
    z = min(max_flow(n, edges, cap, s, t) / d for s, t, d in commodities)
    if z == 0:
        return 0.0, [[0.0] * m for _ in range(k)], [0.0] * k
    demand = [d * z / k for _, _, d in commodities]
    delta = (1 + eps) / ((1 + eps) * m) ** (1 / eps)
    length = [delta / c for c in cap]
    D = delta * m  # D = sum of length[e] * cap[e]
    flow = [[0.0] * m for _ in range(k)]
    routed = [0.0] * k
    while D < 1:  # one phase routes every demand once
        for j, (s, t, _) in enumerate(commodities):
            rest = demand[j]
            while D < 1 and rest > 0:
                path = shortest_path(n, edges, length, s, t)
                u = min(rest, min(cap[e] for e in path))
                for e in path:
                    flow[j][e] += u
                    old = length[e]
                    length[e] *= 1 + eps * u / cap[e]
                    D += (length[e] - old) * cap[e]
                rest -= u
                routed[j] += u
    scale = math.log((1 + eps) / delta, 1 + eps)  # no edge carries more than scale * capacity
    flow = [[f / scale for f in fj] for fj in flow]
    routed = [r / scale for r in routed]
    lam = min(r / d for r, (_, _, d) in zip(routed, commodities))
    return lam, flow, routed


def simple_paths(n, edges, s, t):
    """All simple s-t paths, as lists of edge indices, by an explicit-stack search."""
    out = [[] for _ in range(n)]
    for j, (u, v) in enumerate(edges):
        out[u].append(j)
    paths = []
    stack = [(s, [], {s})]
    while stack:
        u, path, seen = stack.pop()
        if u == t:
            paths.append(path)
            continue
        for j in out[u]:
            v = edges[j][1]
            if v not in seen:
                stack.append((v, path + [j], seen | {v}))
    return paths


def simplex_max(c, A, b):
    """max c.x subject to A x <= b, x >= 0, with b >= 0. Exact, with Bland's rule."""
    m, n = len(A), len(c)
    T = [[Fraction(a) for a in A[i]] + [Fraction(int(i == r)) for r in range(m)] + [Fraction(b[i])] for i in range(m)]
    z = [-Fraction(x) for x in c] + [Fraction(0)] * (m + 1)
    basis = [n + i for i in range(m)]
    while True:
        col = next((j for j in range(n + m) if z[j] < 0), None)
        if col is None:
            break
        cands = [(T[i][-1] / T[i][col], basis[i], i) for i in range(m) if T[i][col] > 0]
        if not cands:
            raise ValueError("unbounded")
        _, _, r = min(cands)
        piv = T[r][col]
        T[r] = [x / piv for x in T[r]]
        for i in range(m):
            if i != r and T[i][col]:
                f = T[i][col]
                T[i] = [x - f * y for x, y in zip(T[i], T[r])]
        f = z[col]
        z = [x - f * y for x, y in zip(z, T[r])]
        basis[r] = col
    x = [Fraction(0)] * n
    for i, bj in enumerate(basis):
        if bj < n:
            x[bj] = T[i][-1]
    return z[-1], x


def exact_lp(n, edges, cap, commodities):
    """The maximum concurrent flow lam*, exactly, from the path formulation."""
    paths = [simple_paths(n, edges, s, t) for s, t, _ in commodities]
    cols = [(j, p) for j, ps in enumerate(paths) for p in ps]
    # Variables: lam, then one per path. Rows: edge capacities, then lam*d_j - sum x_P <= 0.
    nv = 1 + len(cols)
    A, b = [], []
    for e in range(len(edges)):
        A.append([0] + [int(e in p) for _, p in cols])
        b.append(cap[e])
    for j, (_, _, d) in enumerate(commodities):
        A.append([d] + [-int(i == j) for i, _ in cols])
        b.append(0)
    c = [1] + [0] * (nv - 1)
    lam, _ = simplex_max(c, A, b)
    return lam


def sparsest_cut_ratio(n, edges, cap, commodities):
    """min over node sets S of cap(S -> not S) / demand(S -> not S): an upper bound on lam*."""
    best = None
    for mask in range(1, (1 << n) - 1):
        dem = sum(d for s, t, d in commodities if mask >> s & 1 and not mask >> t & 1)
        if dem == 0:
            continue
        c = sum(cp for (u, v), cp in zip(edges, cap) if mask >> u & 1 and not mask >> v & 1)
        r = Fraction(c, dem)
        if best is None or r < best:
            best = r
    return best
