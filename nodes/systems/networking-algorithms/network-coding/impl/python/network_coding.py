# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/network-coding/. The authors are listed in prov/S62752.jsonl.
"""Linear network coding for multicast over a prime field F_q.

A network is a directed acyclic multigraph given by n and a list of edges (u, v).
Each edge carries one symbol of F_q^L per use. The source s holds h messages.
Every edge sends a linear combination of what its tail received; the packet
header holds the global coding vector, so a sink decodes by Gaussian elimination.
"""

from collections import deque


def inv(a, q):
    return pow(a, q - 2, q)


def _eliminate(rows, ncols, q):
    """Row reduce rows in place over F_q, on the first ncols columns. Returns the pivot columns."""
    pivots = []
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(rows)) if rows[i][c] % q), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        f = inv(rows[r][c], q)
        rows[r] = [x * f % q for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                m = rows[i][c]
                rows[i] = [(x - m * y) % q for x, y in zip(rows[i], rows[r])]
        pivots.append(c)
        r += 1
    return pivots


def rank(vectors, q):
    rows = [list(v) for v in vectors]
    return len(_eliminate(rows, len(rows[0]) if rows else 0, q))


def solve(A, Y, q):
    """Find the h messages x with A x = Y, where A is k x h. Returns None if rank(A) < h."""
    h = len(A[0])
    rows = [list(a) + list(y) for a, y in zip(A, Y)]
    if len(_eliminate(rows, h, q)) < h:
        return None
    return [row[h:] for row in rows[:h]]


def topological_edges(n, edges):
    indeg = [0] * n
    out = [[] for _ in range(n)]
    for j, (u, v) in enumerate(edges):
        indeg[v] += 1
        out[u].append(j)
    order, queue = [], deque(u for u in range(n) if indeg[u] == 0)
    while queue:
        u = queue.popleft()
        for j in out[u]:
            order.append(j)
            v = edges[j][1]
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if len(order) != len(edges):
        raise ValueError("the network has a cycle")
    return order


def random_coefficients(rng, q):
    """Local coefficients drawn uniformly from F_q, once for each pair (input, edge)."""
    table = {}

    def coef(i, j):
        if (i, j) not in table:
            table[(i, j)] = rng.randrange(q)
        return table[(i, j)]

    return coef


def multicast(n, edges, s, sinks, data, q, coef):
    """Send the h messages in data (each a list of L field elements) from s to every sink.

    Returns (global coding vectors by edge, decoded messages by sink or None)."""
    h = len(data)
    into = [[] for _ in range(n)]
    for j, (u, v) in enumerate(edges):
        into[v].append(j)
    g, y = {}, {}
    for k in range(h):  # @line L1 virtual edges into s carry the unit vectors and the messages
        g[("s", k)] = [int(i == k) for i in range(h)]
        y[("s", k)] = [x % q for x in data[k]]
    L = len(data[0]) if h else 0
    for j in topological_edges(n, edges):  # @line L2
        u = edges[j][0]
        inputs = [("s", k) for k in range(h)] if u == s else into[u]
        gv, yv = [0] * h, [0] * L
        for i in inputs:
            b = coef(i, j) % q  # @line L3 the hole: the local coefficient
            if b:
                gv = [(a + b * c) % q for a, c in zip(gv, g[i])]  # @line L4 global coding vector
                yv = [(a + b * c) % q for a, c in zip(yv, y[i])]  # @line L5 payload
        g[j], y[j] = gv, yv
    decoded = {}
    for t in sinks:  # @line L6
        A = [g[j] for j in into[t]]  # @line L7
        Y = [y[j] for j in into[t]]
        if A and rank(A, q) == h:
            decoded[t] = solve(A, Y, q)  # @line L8 Gaussian elimination over F_q
        else:
            decoded[t] = None  # @line L9 the sink cannot decode
    return g, decoded


def min_cut(n, edges, s, t):
    """Maximum number of edge-disjoint s-t paths (unit capacities), by augmenting paths."""
    cap = {}
    adj = [set() for _ in range(n)]
    for u, v in edges:
        cap[(u, v)] = cap.get((u, v), 0) + 1
        cap.setdefault((v, u), 0)
        adj[u].add(v)
        adj[v].add(u)
    flow = 0
    while True:
        parent = {s: None}
        queue = deque([s])
        while queue and t not in parent:
            u = queue.popleft()
            for v in adj[u]:
                if v not in parent and cap[(u, v)] > 0:
                    parent[v] = u
                    queue.append(v)
        if t not in parent:
            return flow
        v = t
        while parent[v] is not None:
            u = parent[v]
            cap[(u, v)] -= 1
            cap[(v, u)] += 1
            v = u
        flow += 1


def butterfly():
    """s=0, a=1, b=2, c=3, d=4, t1=5, t2=6."""
    edges = [(0, 1), (0, 2), (1, 5), (1, 3), (2, 3), (2, 6), (3, 4), (4, 5), (4, 6)]
    return 7, edges, 0, [5, 6]


def routing_max_min(n, edges, s, sinks, h):
    """Brute force over all routing (store and forward) choices for one use of the network.

    Each edge carries one message that its tail has received, or nothing. Returns the
    largest value of the smallest number of distinct messages that a sink receives."""
    order = topological_edges(n, edges)

    def received(part):
        got = [set() for _ in range(n)]
        got[s] = set(range(h))
        for i, m in enumerate(part):
            if m is not None:
                got[edges[order[i]][1]].add(m)
        return got

    best = 0
    stack = [[]]
    while stack:
        part = stack.pop()
        got = received(part)
        if len(part) == len(order):
            best = max(best, min(len(got[t]) for t in sinks))
            continue
        u = edges[order[len(part)]][0]
        for m in [None] + sorted(got[u]):
            stack.append(part + [m])
    return best


def reaches(n, edges, s, targets):
    """True if every target is reachable from s using the given edges."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    seen, stack = {s}, [s]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return all(t in seen for t in targets)


def random_dag(n, p, rng):
    return [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
