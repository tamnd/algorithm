# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eisenberg-gale-program/. The authors are listed in prov/R0QFZC.jsonl.
"""Solve the Eisenberg-Gale convex program of a linear Fisher market and read off the prices.

Buyers are 0, ..., n - 1 and goods are 0, ..., m - 1, with one unit of each good. u[i][j] >= 0 is
the utility of buyer i for all of good j and e[i] > 0 is her budget. Every buyer likes some good
and every good is liked by some buyer. The program is

    maximize   sum_i e_i log(sum_j u_ij x_ij)
    subject to sum_i x_ij <= 1 for every good j,  x >= 0.

The solver runs mirror ascent with the entropy on each good (exponentiated gradient) in floating
point, with a backtracking step size. From time to time it rounds: it guesses the support of the
optimum, computes the exact prices that this support forces, and accepts them only if they pass
an exact check of the equilibrium conditions (the KKT conditions of the program) in Fractions.
"""

import math
from collections import deque
from fractions import Fraction


def objective(u, e, x):
    n, m = len(u), len(u[0])
    return sum(e[i] * math.log(sum(u[i][j] * x[i][j] for j in range(m))) for i in range(n))


def max_flow(num_nodes, cap, s, t):
    """Edmonds-Karp maximum flow on exact capacities; returns the value and the flow on each arc."""
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


def certify(u, e, p):
    """If p are equilibrium prices, return the exact allocation x[i][j] (amounts of goods);
    else return None. The test is a maximum flow on the edges of maximum bang per buck."""
    n, m = len(u), len(u[0])
    if any(q is None or q <= 0 for q in p):
        return None
    alpha = [max(Fraction(u[i][j]) / p[j] for j in range(m)) for i in range(n)]
    src, snk = 0, n + m + 1
    cap = {(src, 1 + j): p[j] for j in range(m)}
    for i in range(n):
        cap[(1 + m + i, snk)] = e[i]
        for j in range(m):
            if u[i][j] > 0 and Fraction(u[i][j]) / p[j] == alpha[i]:
                cap[(1 + j, 1 + m + i)] = sum(e) + 1
    if sum(p) != sum(e):
        return None
    value, flow = max_flow(snk + 1, cap, src, snk)
    if value != sum(e):
        return None
    return [[flow.get((1 + j, 1 + m + i), Fraction(0)) / p[j] for j in range(m)] for i in range(n)]


def prices_from_support(u, e, support):
    """The prices forced by a set of spending edges: on each connected part, a buyer gets the same
    bang per buck on all her edges, and the prices add up to the money of the part's buyers."""
    n, m = len(u), len(u[0])
    nbr = {}
    for i, j in support:
        nbr.setdefault(("b", i), []).append(("g", j))
        nbr.setdefault(("g", j), []).append(("b", i))
    rel, p = {}, [None] * m
    for start in [("g", j) for j in range(m)]:
        if start in rel or start not in nbr:
            continue
        rel[start] = Fraction(1)
        comp, stack = [start], [start]
        while stack:
            a = stack.pop()
            for b in nbr[a]:
                i, j = (a[1], b[1]) if a[0] == "b" else (b[1], a[1])
                val = Fraction(u[i][j]) / rel[a]  # price from bang, or bang from price
                if b not in rel:
                    rel[b] = val
                    comp.append(b)
                    stack.append(b)
                elif rel[b] != val:
                    return None
        goods = [a for a in comp if a[0] == "g"]
        money = sum(e[a[1]] for a in comp if a[0] == "b")
        scale = money / sum(rel[a] for a in goods)
        for a in goods:
            p[a[1]] = rel[a] * scale
    return p


def eisenberg_gale(u, e, max_rounds=200000, check_every=5):
    """Return (p, x): the exact equilibrium prices and an exact optimal allocation of the program."""
    n, m = len(u), len(u[0])
    e = [Fraction(b) for b in e]
    ef = [float(b) for b in e]
    edges = [(i, j) for i in range(n) for j in range(m) if u[i][j] > 0]
    x = [[0.0] * m for _ in range(n)]
    for j in range(m):  # @line L1
        likers = [i for i in range(n) if u[i][j] > 0]
        for i in likers:
            x[i][j] = 1.0 / len(likers)
    eta = 1.0  # @line L2
    f = objective(u, ef, x)
    for rnd in range(1, max_rounds + 1):  # @line L3
        util = [sum(u[i][j] * x[i][j] for j in range(m)) for i in range(n)]
        g = [[ef[i] * u[i][j] / util[i] for j in range(m)] for i in range(n)]  # @line L4
        while True:
            y = [[0.0] * m for _ in range(n)]
            for j in range(m):  # @line L5
                top = max(eta * g[i][j] for i, jj in edges if jj == j)
                w = {i: x[i][j] * math.exp(eta * g[i][j] - top) for i, jj in edges if jj == j}
                total = sum(w.values())
                for i in w:
                    y[i][j] = w[i] / total
            if min(sum(u[i][j] * y[i][j] for j in range(m)) for i in range(n)) <= 0:
                eta /= 2
                continue
            fy = objective(u, ef, y)
            lin = sum(g[i][j] * (y[i][j] - x[i][j]) for i, j in edges)
            kl = sum(y[i][j] * math.log(y[i][j] / x[i][j]) for i, j in edges if y[i][j] > 0)
            if fy >= f + lin - kl / eta - 1e-12 * abs(f):  # @line L6
                break
            eta /= 2
        x, f, eta = y, fy, eta * 2  # @line L7
        if rnd % check_every == 0:
            for k in range(2, 15):  # @line L8
                support = [(i, j) for i, j in edges if x[i][j] > 10.0 ** (-k)]
                p = prices_from_support(u, e, support)
                if p is not None and None not in p:
                    exact = certify(u, e, p)
                    if exact is not None:
                        return p, exact
    raise RuntimeError("no exact certificate found")
