# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dpsv-algorithm/. The authors are listed in prov/MZRKQA.jsonl.
"""The primal-dual algorithm of Devanur, Papadimitriou, Saberi and Vazirani for linear Fisher markets.

Buyers are 0, ..., n - 1 and goods are 0, ..., m - 1, with one unit of each good. u[i][j] >= 0
is the utility of buyer i for all of good j, and e[i] > 0 is the budget of buyer i. Every buyer
must like some good and every good must be liked by some buyer. This is the simple version of
the algorithm (Algorithm 1 of the paper): prices only go up, by a common factor on the active
goods, until a set of goods goes tight and is frozen. All numbers are exact Fractions.
"""

from collections import deque
from fractions import Fraction


def max_flow(num_nodes, cap, s, t):
    """Edmonds-Karp maximum flow. cap maps (a, b) to a capacity. Returns the flow value, the
    flow on each arc of cap, and the residual capacities."""
    res = {}
    adj = [[] for _ in range(num_nodes)]
    for (a, b), c in cap.items():
        if (a, b) not in res and (b, a) not in res:
            adj[a].append(b)
            adj[b].append(a)
        res[(a, b)] = res.get((a, b), Fraction(0)) + c
        res.setdefault((b, a), Fraction(0))
    value = Fraction(0)
    while True:
        prev = {s: None}
        queue = deque([s])
        while queue and t not in prev:
            a = queue.popleft()
            for b in adj[a]:
                if b not in prev and res[(a, b)] > 0:
                    prev[b] = a
                    queue.append(b)
        if t not in prev:
            break
        path, b = [], t
        while prev[b] is not None:
            path.append((prev[b], b))
            b = prev[b]
        push = min(res[arc] for arc in path)
        for a, b in path:
            res[(a, b)] -= push
            res[(b, a)] += push
        value += push
    flow = {arc: c - res[arc] for arc, c in cap.items()}
    return value, flow, res, adj


def reaches_sink(num_nodes, res, adj, t):
    """The nodes that can reach t in the residual graph."""
    seen = {t}
    queue = deque([t])
    while queue:
        b = queue.popleft()
        for a in adj[b]:
            if a not in seen and res[(a, b)] > 0:
                seen.add(a)
                queue.append(a)
    return seen


def bang(u, p, i, goods):
    """The maximum bang per buck of buyer i over the given goods."""
    return max(Fraction(u[i][j]) / p[j] for j in goods)


def tight_set(u, e, p, goods, buyers, edges):
    """Section 6 of the paper: the least factor x >= 1 at which a set of the given goods goes
    tight, and the largest such set S. A set S is tight at x when x p(S) = e(Gamma(S)), where
    Gamma(S) is the set of buyers joined to S by an edge."""
    S = set(goods)
    while True:
        nbrs = {i for (i, j) in edges if j in S}
        x = sum(e[i] for i in nbrs) / sum(p[j] for j in S)
        m = len(u[0])
        src, snk = 0, len(u) + m + 1
        big = sum(e) * (x + 1) + 1  # larger than any finite cut, so never cut
        cap = {}
        for j in S:
            cap[(src, 1 + j)] = x * p[j]
        for i, j in edges:
            if j in S:
                cap[(1 + j, 1 + m + i)] = big
        for i in nbrs:
            cap[(1 + m + i, snk)] = e[i]
        value, _, res, adj = max_flow(snk + 1, cap, src, snk)
        if value == sum(e[i] for i in nbrs):
            return x, S
        to_sink = reaches_sink(snk + 1, res, adj, snk)
        # the largest minimum cut: every node that cannot reach the sink stays on the source side
        S = {j for j in S if 1 + j not in to_sink}


def equality_flow(u, e, p):
    """A maximum flow in the network N(p): source to good j with capacity p_j, good j to buyer i
    on every equality edge, buyer i to sink with capacity e_i. Returns (value, x) with x[i][j]
    the money that buyer i spends on good j."""
    n, m = len(u), len(u[0])
    src, snk = 0, n + m + 1
    alpha = [bang(u, p, i, range(m)) for i in range(n)]
    cap = {}
    for j in range(m):
        cap[(src, 1 + j)] = p[j]
    for i in range(n):
        cap[(1 + m + i, snk)] = e[i]
        for j in range(m):
            if u[i][j] > 0 and Fraction(u[i][j]) / p[j] == alpha[i]:
                cap[(1 + j, 1 + m + i)] = sum(e) + 1
    value, flow, _, _ = max_flow(snk + 1, cap, src, snk)
    x = [[flow.get((1 + j, 1 + m + i), Fraction(0)) for j in range(m)] for i in range(n)]
    return value, x


def dpsv(u, e, trace=None):
    """Return equilibrium prices p and money spent x[i][j] for the linear Fisher market (u, e).
    If trace is a list, one tuple (factor, event, goods) is appended per raise of prices."""
    n, m = len(u), len(u[0])
    e = [Fraction(b) for b in e]
    p = [min(e) / m for _ in range(m)]  # @line L1
    alpha = [bang(u, p, i, range(m)) for i in range(n)]
    for j in range(m):  # @line L2
        p[j] = max(Fraction(u[i][j]) / alpha[i] for i in range(n) if u[i][j] > 0)
    active_goods = set(range(m))  # @line L3
    frozen = []  # list of (goods, buyers) of frozen components
    while active_goods:  # @line L4
        frozen_buyers = set().union(*[b for _, b in frozen]) if frozen else set()
        active_buyers = [i for i in range(n) if i not in frozen_buyers]
        a = {i: bang(u, p, i, active_goods) for i in active_buyers}
        edges = [(i, j) for i in active_buyers for j in active_goods
                 if u[i][j] > 0 and Fraction(u[i][j]) / p[j] == a[i]]
        x1, S = tight_set(u, e, p, active_goods, active_buyers, edges)  # @line L5
        x2, edge2 = None, None
        for i in active_buyers:  # @line L6
            for j in range(m):
                if j not in active_goods and u[i][j] > 0:
                    x = a[i] * p[j] / u[i][j]
                    if x2 is None or x < x2:
                        x2, edge2 = x, (i, j)
        x = x1 if x2 is None or x1 <= x2 else x2
        for j in active_goods:  # @line L7
            p[j] *= x
        if x2 is not None and x2 < x1:  # @line L8
            k = next(c for c, (goods, _) in enumerate(frozen) if edge2[1] in goods)
            goods, _ = frozen.pop(k)
            active_goods |= goods
            if trace is not None:
                trace.append((x, "unfreeze", sorted(goods)))
        else:  # @line L9
            buyers = {i for (i, j) in edges if j in S}
            frozen.append((set(S), buyers))
            active_goods -= S
            if trace is not None:
                trace.append((x, "freeze", sorted(S)))
    value, x = equality_flow(u, e, p)  # @line L10
    return p, x  # @line L11
