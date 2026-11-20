# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orlin-fisher-market-algorithm/. The authors are listed in prov/XBSFVW.jsonl.
"""A toy of Orlin's Delta-scaling algorithm for linear Fisher markets.

This is the weakly polynomial scaling algorithm (ScalingAlgorithm with PriceAndAugment), written
for small inputs in exact Fractions. It is a toy: prices are stored explicitly, augmenting paths
come from breadth-first search instead of the Fibonacci heap of the paper, and the extra steps that
make the algorithm strongly polynomial (fertile components and MakeFertile) are left out. The
utilities are not perturbed, so the final step computes the prices of the candidate support and
accepts them only after an exact max-flow check.

Buyers are 0, ..., nb - 1 and goods are 0, ..., ng - 1, one unit each. U[i][j] >= 0 is the
utility of buyer i for all of good j and e[i] > 0 her budget. x[i][j] is money, not goods.
"""

from collections import deque
from fractions import Fraction


def _bang(U, p, i):
    return max(Fraction(U[i][j]) / p[j] for j in range(len(p)) if U[i][j] > 0)


def _equality(U, p, i, j, alpha):
    return U[i][j] > 0 and Fraction(U[i][j]) / p[j] == alpha[i]


def _max_flow(num_nodes, cap, s, t):
    res, adj = {}, [[] for _ in range(num_nodes)]
    for (a, b), c in cap.items():
        adj[a].append(b)
        adj[b].append(a)
        res[(a, b)] = c
        res.setdefault((b, a), Fraction(0))
    value = Fraction(0)
    while True:
        prev, queue = {s: None}, deque([s])
        while queue and t not in prev:
            a = queue.popleft()
            for b in adj[a]:
                if b not in prev and res[(a, b)] > 0:
                    prev[b] = a
                    queue.append(b)
        if t not in prev:
            return value, {arc: c - res[arc] for arc, c in cap.items()}
        path, b = [], t
        while prev[b] is not None:
            path.append((prev[b], b))
            b = prev[b]
        push = min(res[arc] for arc in path)
        for a, b in path:
            res[(a, b)] -= push
            res[(b, a)] += push
        value += push


def certify(U, e, p):
    """Return the money x[i][j] of an equilibrium at prices p, or None if p are not equilibrium
    prices. The test is a maximum flow on the edges of maximum bang per buck."""
    nb, ng = len(U), len(U[0])
    if any(q is None or q <= 0 for q in p) or sum(p) != sum(e):
        return None
    alpha = [_bang(U, p, i) for i in range(nb)]
    src, snk = 0, nb + ng + 1
    cap = {(src, 1 + j): p[j] for j in range(ng)}
    for i in range(nb):
        cap[(1 + ng + i, snk)] = e[i]
        for j in range(ng):
            if _equality(U, p, i, j, alpha):
                cap[(1 + j, 1 + ng + i)] = sum(e) + 1
    value, flow = _max_flow(snk + 1, cap, src, snk)
    if value != sum(e):
        return None
    return [[flow.get((1 + j, 1 + ng + i), Fraction(0)) for j in range(ng)] for i in range(nb)]


def basic_prices(U, e, support):
    """The prices fixed by a set of edges: equal bang per buck along the edges of each buyer, and
    on each connected part the prices add up to the budgets. None if they are not well defined."""
    nb, ng = len(U), len(U[0])
    nbr = {}
    for i, j in support:
        nbr.setdefault(("b", i), []).append(("g", j))
        nbr.setdefault(("g", j), []).append(("b", i))
    if len(nbr) != nb + ng:
        return None
    rel, p = {}, [None] * ng
    for j0 in range(ng):
        if ("g", j0) in rel:
            continue
        rel[("g", j0)] = Fraction(1)
        comp, stack = [("g", j0)], [("g", j0)]
        while stack:
            a = stack.pop()
            for c in nbr[a]:
                i, j = (a[1], c[1]) if a[0] == "b" else (c[1], a[1])
                val = Fraction(U[i][j]) / rel[a]
                if c not in rel:
                    rel[c] = val
                    comp.append(c)
                    stack.append(c)
                elif rel[c] != val:
                    return None
        money = sum(e[a[1]] for a in comp if a[0] == "b")
        scale = money / sum(rel[a] for a in comp if a[0] == "g")
        for a in comp:
            if a[0] == "g":
                p[a[1]] = rel[a] * scale
    return p


def _price_and_augment(U, e, p, x, r, delta):
    """Raise the prices of the goods reachable from buyer r until some reachable good j has
    b_j <= 0, then send delta along a residual path from r to j."""
    nb, ng = len(U), len(U[0])
    while True:
        alpha = [_bang(U, p, i) for i in range(nb)]
        prev = {("b", r): None}  # @line L4
        queue = deque([("b", r)])
        while queue:
            kind, a = queue.popleft()
            nxt = []
            if kind == "b":
                nxt = [("g", j) for j in range(ng) if _equality(U, p, a, j, alpha)]
            else:
                nxt = [("b", i) for i in range(nb) if x[i][a] > 0]
            for v in nxt:
                if v not in prev:
                    prev[v] = (kind, a)
                    queue.append(v)
        back = [j for (kind, j) in prev if kind == "g" and sum(x[i][j] for i in range(nb)) - p[j] <= 0]
        if back:
            break
        act_goods = [j for (kind, j) in prev if kind == "g"]
        act_buyers = [i for (kind, i) in prev if kind == "b"]
        q = None  # @line L5
        for j in act_goods:  # b_j reaches 0
            cand = sum(x[i][j] for i in range(nb)) / p[j]
            q = cand if q is None else min(q, cand)
        for i in act_buyers:  # a new equality edge to a good that is not reachable yet
            for j in range(ng):
                if ("g", j) not in prev and U[i][j] > 0:
                    q = min(q, alpha[i] * p[j] / U[i][j])
        for j in act_goods:
            p[j] *= q
    j = min(back)  # @line L6
    node = ("g", j)
    while prev[node] is not None:
        before = prev[node]
        if before[0] == "b":
            x[before[1]][node[1]] += delta  # forward arc: buyer spends more on the good
        else:
            x[node[1]][before[1]] -= delta  # backward arc: buyer spends less on the good
        node = before


def orlin_scaling(U, e, trace=None):
    """Return (p, x): exact equilibrium prices and money spent. If trace is a list, a tuple
    (delta, p, x) is appended to it at the end of each scaling phase."""
    nb, ng = len(U), len(U[0])
    n = nb + ng
    e = [Fraction(v) for v in e]
    delta = max(e) / n  # @line L1
    p = [max(Fraction(U[i][j]) * e[i] / (n * sum(U[i])) for i in range(nb)) for j in range(ng)]
    x = [[Fraction(0)] * ng for _ in range(nb)]
    while True:  # @line L2
        while True:  # @line L3
            r = next((i for i in range(nb) if e[i] - sum(x[i]) >= delta), None)
            if r is None:
                break
            _price_and_augment(U, e, p, x, r, delta)
        if trace is not None:
            trace.append((delta, list(p), [list(row) for row in x]))
        support = [(i, j) for i in range(nb) for j in range(ng) if x[i][j] >= 4 * n * delta]  # @line L7
        cand = basic_prices(U, e, support)  # @line L8
        if cand is not None:
            exact = certify(U, e, cand)
            if exact is not None:
                return cand, exact
        delta /= 2  # @line L9
        for j in range(ng):
            if sum(x[i][j] for i in range(nb)) - p[j] > delta:
                i = next(i for i in range(nb) if x[i][j] > 0)
                x[i][j] -= delta
