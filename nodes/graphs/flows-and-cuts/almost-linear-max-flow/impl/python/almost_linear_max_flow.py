# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/almost-linear-max-flow/. The authors are listed in prov/8Q450K.jsonl.
"""The l1 interior point method of Chen, Kyng, Liu, Peng, Probst Gutenberg and
Sachdeva (2022), with exact min-ratio cycles in place of their dynamic data
structure, followed by rounding and an exact finish.

Integer capacities, directed edges. Antiparallel and parallel edges are kept as
separate variables. The answer is always exact: the interior point phase only
brings the flow close to optimal, and the finish makes it optimal.
"""

import math
from collections import deque


def _min_ratio_cycle(N, arcs, tol=1e-12):
    """Return (ratio, cycle) minimizing sum(w)/sum(l) over directed cycles of
    the arc list (tail, head, w, l, edge, sign), or (0.0, None) if no cycle has
    negative ratio. Dinkelbach iteration with Bellman-Ford as the oracle."""
    lam, best = 0.0, None
    while True:
        cyc = _negative_cycle(N, arcs, lam, tol)
        if cyc is None:
            return lam, best
        w = sum(arcs[i][2] for i in cyc)
        l = sum(arcs[i][3] for i in cyc)
        r = w / l
        if best is not None and r >= lam - tol * (1 + abs(lam)):
            return lam, best
        lam, best = r, cyc


def _negative_cycle(N, arcs, lam, tol):
    dist = [0.0] * N
    pred = [-1] * N
    x = -1
    for _ in range(N):
        x = -1
        for i, (a, b, w, l, _, _) in enumerate(arcs):
            nd = dist[a] + w - lam * l
            if nd < dist[b] - tol * (1 + abs(dist[b])):
                dist[b] = nd
                pred[b] = i
                x = b
        if x < 0:
            return None
    for _ in range(N):
        x = arcs[pred[x]][0]
    cyc, v = [], x
    while True:
        i = pred[v]
        cyc.append(i)
        v = arcs[i][0]
        if v == x:
            break
    cyc.reverse()
    return cyc


def _bfs_path(n, cap, adj, s, t):
    par = [-1] * n
    par[s] = -2
    q = deque([s])
    while q:
        v = q.popleft()
        for x in adj[v]:
            w = cap[x][1]
            if par[w] == -1 and cap[x][0] > 0:
                par[w] = x
                if w == t:
                    return par
                q.append(w)
    return None


def almost_linear_max_flow(n, edges, s, t, max_steps=None, on_step=None):
    """Maximum s-t flow for integer capacities.

    edges: list of (u, v, c) with c a nonnegative int. Returns (value, flow)
    with flow[i] the integer flow on edges[i]. on_step(k, gap) is called after
    interior point step k with gap = c^T f - F_lo, and once more at the end as
    on_step(-1, number of augmenting paths used by the finish).
    """
    if s == t:
        raise ValueError("s and t must differ")
    for _, _, c in edges:
        if not isinstance(c, int) or c < 0:
            raise TypeError("capacities must be nonnegative integers")
    U = sum(c for u, v, c in edges if u == s and v != s)  # @line L1
    var = []  # (tail, head, hi, cost, original index or -1)
    for i, (u, v, c) in enumerate(edges):
        if c > 0 and u != v:
            var.append((u, v, c, 0, i))
    flow = [0] * len(edges)
    if U == 0:
        return 0, flow
    var.append((t, s, U, -1, -1))
    f = [hi / 2 for _, _, hi, _, _ in var]
    imb = [0.0] * n
    for (a, b, _, _, _), x in zip(var, f):
        imb[a] -= x
        imb[b] += x
    z = n
    M = 4
    for v in range(n):  # @line L2
        if imb[v] > 0:
            var.append((v, z, 2 * imb[v], M, -2))
            f.append(imb[v])
        elif imb[v] < 0:
            var.append((z, v, -2 * imb[v], M, -2))
            f.append(-imb[v])
    m = len(var)
    F_lo = -U - 1
    alpha = 1.0 / (4 * math.log(4 * m * U + 4))
    coef = 20 * m

    def phi(g):
        cost = sum(e[3] * x for e, x in zip(var, g))
        val = coef * math.log(cost - F_lo)
        for e, x in zip(var, g):
            a, b = e[2] - x, x
            if a <= 0 or b <= 0:
                return math.inf
            val += a ** -alpha + b ** -alpha
        return val

    steps = 0
    limit = max_steps if max_steps is not None else 30 * m
    cur = phi(f)
    while steps < limit:  # @line L3
        cost = sum(e[3] * x for e, x in zip(var, f))
        gap = cost - F_lo
        arcs = []
        for j, (a, b, hi, c, _) in enumerate(var):  # @line L4
            up, lo = hi - f[j], f[j]
            g = coef * c / gap + alpha * up ** (-alpha - 1) - alpha * lo ** (-alpha - 1)
            l = up ** (-alpha - 1) + lo ** (-alpha - 1)
            arcs.append((a, b, g, l, j, 1))
            arcs.append((b, a, -g, l, j, -1))
        ratio, cyc = _min_ratio_cycle(n + 1, arcs)  # @line L5
        if cyc is None or ratio > -1e-9:
            break
        delta = {}
        L = sum(arcs[i][3] for i in cyc)
        for i in cyc:
            j, sg = arcs[i][4], arcs[i][5]
            delta[j] = delta.get(j, 0.0) + sg / L
        room = min(((var[j][2] - f[j]) / d if d > 0 else f[j] / -d)
                   for j, d in delta.items() if d != 0)
        eta = 0.5 * room
        while eta > 1e-15:  # @line L6
            g2 = list(f)
            for j, d in delta.items():
                g2[j] += eta * d
            new = phi(g2)
            if new < cur:
                f, cur = g2, new
                break
            eta /= 2
        else:
            break
        steps += 1
        if on_step:
            on_step(steps, sum(e[3] * x for e, x in zip(var, f)) - F_lo)
    x = _round(n + 1, var, f)  # @line L7
    _cancel_aux(n, var, x)  # @line L8
    for j, e in enumerate(var):
        if e[4] >= 0:
            flow[e[4]] = x[j]
    cap, adj = [], [[] for _ in range(n)]
    for i, (u, v, c) in enumerate(edges):
        adj[u].append(len(cap))
        cap.append([c - flow[i], v])
        adj[v].append(len(cap))
        cap.append([flow[i], u])
    aug = 0
    while True:  # @line L9
        par = _bfs_path(n, cap, adj, s, t)
        if par is None:
            break
        b, v = math.inf, t
        while v != s:
            b = min(b, cap[par[v]][0])
            v = cap[par[v] ^ 1][1]
        v = t
        while v != s:
            cap[par[v]][0] -= b
            cap[par[v] ^ 1][0] += b
            v = cap[par[v] ^ 1][1]
        aug += 1
    for i in range(len(edges)):
        flow[i] = cap[2 * i + 1][0]
    value = sum(flow[i] for i, (u, v, _) in enumerate(edges) if u == s) - \
        sum(flow[i] for i, (u, v, _) in enumerate(edges) if v == s)
    if on_step:
        on_step(-1, aug)
    return value, flow


def _round(N, var, f):
    """Make every variable integral by pushing around cycles of fractional
    variables in the direction that does not raise the cost."""
    x = list(f)
    eps = 1e-9
    for j in range(len(x)):
        r = round(x[j])
        if abs(x[j] - r) < eps:
            x[j] = float(r)
    while True:
        frac = [j for j in range(len(x)) if abs(x[j] - round(x[j])) >= eps]
        if not frac:
            return [int(round(v)) for v in x]
        adj = {}
        for j in frac:
            a, b = var[j][0], var[j][1]
            adj.setdefault(a, []).append((b, j, 1))
            adj.setdefault(b, []).append((a, j, -1))
        cyc = _undirected_cycle(adj, var[frac[0]][0])
        cost = sum(var[j][3] * sg for j, sg in cyc)
        d = 1 if cost <= 0 else -1
        amt = min((math.ceil(x[j] - eps) - x[j]) if sg * d > 0 else (x[j] - math.floor(x[j] + eps))
                  for j, sg in cyc)
        for j, sg in cyc:
            x[j] += sg * d * amt
            r = round(x[j])
            if abs(x[j] - r) < eps:
                x[j] = float(r)


def _undirected_cycle(adj, start):
    """Cycle in the multigraph of fractional variables, as (var, sign) pairs."""
    stack = [(start, -1)]
    seen = {start: None}  # vertex -> (parent vertex, var, sign)
    while stack:
        v, via = stack.pop()
        for w, j, sg in adj[v]:
            if j == via:
                continue
            if w in seen:
                pv, pw = _path(seen, v), _path(seen, w)
                k = 0
                while k < min(len(pv), len(pw)) and pv[k] == pw[k]:
                    k += 1
                return ([(jj, s2) for (_, jj, s2) in pv[k:]] + [(j, sg)]
                        + [(jj, -s2) for (_, jj, s2) in reversed(pw[k:])])
            seen[w] = (v, j, sg)
            stack.append((w, j))
    raise AssertionError("no cycle among fractional variables")


def _path(seen, v):
    p = []
    while seen[v] is not None:
        u, j, sg = seen[v]
        p.append((u, j, sg))
        v = u
    p.reverse()
    return p


def _cancel_aux(n, var, x):
    """Remove all flow on the auxiliary edges by cancelling cycles through z."""
    z = n
    out = {}
    for j, e in enumerate(var):
        out.setdefault(e[0], []).append(j)
    while True:
        par = {z: None}
        q = deque([z])
        back = None
        while q and back is None:
            v = q.popleft()
            for j in out.get(v, []):
                if x[j] <= 0:
                    continue
                w = var[j][1]
                if w == z:
                    back = j
                    break
                if w not in par:
                    par[w] = j
                    q.append(w)
        if back is None:
            return
        cyc, v = [back], var[back][0]
        while v != z:
            cyc.append(par[v])
            v = var[par[v]][0]
        amt = min(x[j] for j in cyc)
        for j in cyc:
            x[j] -= amt
