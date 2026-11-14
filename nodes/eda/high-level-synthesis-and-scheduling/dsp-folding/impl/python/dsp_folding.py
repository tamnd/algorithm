# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dsp-folding/. The authors are listed in prov/PNFW75.jsonl.

"""Folding transformation of a data flow graph (Parhi).

A graph has nodes with a kind: "in" (the host, which emits x(k) in
iteration k), "add" (sum of the inputs) or "mul" (a constant times the
product of the inputs). Arithmetic is modulo MOD, and every node maps all
zero inputs to zero, so registers that start at zero stand for samples
before time 0. Edges are (u, v, w) with w >= 0 delays, and every cycle has
at least one delay.

A folding set gives each operation a hardware unit and an order in
{0, ..., N - 1}. Unit h is pipelined with P[h] >= 1 stages. The host is a
unit with order 0 and P = 0.
"""

MOD = 1_000_003


def node_value(kind, coef, inputs):
    if kind == "add":
        return sum(inputs) % MOD
    prod = coef
    for a in inputs:
        prod = prod * a % MOD
    return prod


def topo_zero_delay(nodes, edges):
    indeg = {v: 0 for v in nodes}
    for u, v, w in edges:
        if w == 0:
            indeg[v] += 1
    order = [v for v in nodes if indeg[v] == 0]
    for v in order:
        for a, b, w in edges:
            if a == v and w == 0:
                indeg[b] -= 1
                if indeg[b] == 0:
                    order.append(b)
    if len(order) != len(nodes):
        raise ValueError("a cycle with no delay")
    return order


def simulate(graph, x, out):
    """Run the graph for len(x) iterations; return the values of node out."""
    nodes, edges, kind, coef = graph["nodes"], graph["edges"], graph["kind"], graph["coef"]
    order = topo_zero_delay(nodes, edges)
    val = {v: [] for v in nodes}
    for k in range(len(x)):
        for v in order:
            if kind[v] == "in":
                val[v].append(x[k] % MOD)
                continue
            ins = [val[u][k - w] if k - w >= 0 else 0 for (u, b, w) in edges if b == v]
            val[v].append(node_value(kind[v], coef.get(v, 1), ins))
    return val[out]


def folding_delays(graph, unit, order, P, N, r=None):
    """D_F(U -> V) = N w_r(e) - P_U + v - u for every edge, in edge order."""
    r = r or {}
    res = []
    for u, v, w in graph["edges"]:
        wr = w + r.get(v, 0) - r.get(u, 0)
        res.append(N * wr - P[unit[u]] + order[v] - order[u])  # @line L1
    return res


def folding_retiming(graph, unit, order, P, N):
    """Least r >= 0 with r(U) - r(V) <= floor(D_F(e) / N) on every edge.

    Each row reads r(V) >= r(U) - c with c = floor(D_F(e) / N). Start from
    r = 0 and raise r(V) to r(U) - c until no row is violated, as in
    Bellman-Ford for longest paths. If a pass still raises a value after
    |V| passes, a cycle has a positive sum of -c, and no retiming exists.
    The host has no input edge, so it keeps r = 0.
    """
    nodes = graph["nodes"]
    r = {v: 0 for v in nodes}
    rows = [(u, v, d // N) for (u, v, w), d in zip(graph["edges"], folding_delays(graph, unit, order, P, N))]
    for _ in range(len(nodes) + 1):
        changed = False
        for u, v, c in rows:  # @line L3
            if r[u] - c > r[v]:
                r[v] = r[u] - c
                changed = True
        if not changed:
            return r
    return None


def fold(graph, unit, order, P, N):
    """Return (r, D) with D the register count of each folded edge, or None."""
    for v in graph["nodes"]:
        if not 0 <= order[v] < N:
            raise ValueError("order out of range")
    slots = set()
    for v in graph["nodes"]:
        key = (unit[v], order[v])
        if key in slots:
            raise ValueError("two operations in one slot of one unit")
        slots.add(key)
    # A retiming of all zeros is returned when no D_F is negative.
    r = folding_retiming(graph, unit, order, P, N)  # @line L2
    if r is None:
        return None  # @line L4
    return r, folding_delays(graph, unit, order, P, N, r)  # @line L5 L9


def simulate_folded(graph, unit, order, P, N, r, D, x, out):
    """Clock-by-clock run of the folded architecture.

    In cycle t, unit h runs the operation whose order is t mod N. Its result
    leaves the unit P[h] cycles later. The input of V along edge e is the
    output of the unit of U as it was D[e] cycles earlier. The host emits
    x(l - r(host)) at cycle N l. Return y(0), ..., y(len(x) - 1) read at
    the output of node out.
    """
    nodes, edges, kind, coef = graph["nodes"], graph["edges"], graph["kind"], graph["coef"]
    host = [v for v in nodes if kind[v] == "in"]
    shift = max(r.values())
    L = len(x) + shift + 2
    T = N * L + max(P.values()) + 1
    emit = {h: {} for h in set(unit.values())}
    by_slot = {}
    for v in nodes:
        if kind[v] != "in":
            by_slot.setdefault((unit[v], order[v]), v)
    ins_of = {v: [(i, e) for i, e in enumerate(edges) if e[1] == v] for v in nodes}
    for t in range(T):
        if t % N == 0:
            for h in host:
                l = t // N - r[h]
                emit[unit[h]][t] = x[l] % MOD if 0 <= l < len(x) else 0
        for hw in emit:
            v = by_slot.get((hw, t % N))  # @line L8
            if v is None:
                continue
            ins = []
            for i, (u, _, _) in ins_of[v]:  # @line L6
                ins.append(emit[unit[u]].get(t - D[i], 0))  # @line L7
            emit[hw][t + P[hw]] = node_value(kind[v], coef.get(v, 1), ins)
    y = []
    for l in range(len(x)):
        y.append(emit[unit[out]].get(N * (l + r[out]) + order[out] + P[unit[out]], 0))
    return y
