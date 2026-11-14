# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clock-skew-scheduling/. The authors are listed in prov/K3PCDZ.jsonl.
"""Clock skew scheduling: the least clock period and a clock schedule.

Registers are 0 to n - 1. A path (i, j, dmax, dmin) is a combinational path
from register i to register j with largest delay dmax and smallest delay
dmin. With clock arrival times c, the period T is valid when every path has

    setup:  c_i + dmax + t_setup <= c_j + T
    hold:   c_i + dmin >= c_j + t_hold

Each is a difference constraint x_u - x_v <= w, an edge v -> u of weight w,
and the weight of an edge is a T + b with a in {0, 1}. The period T is valid
if and only if the graph has no negative cycle. The least valid period is
found by cycle ratio iteration: while Bellman-Ford finds a negative cycle at
the current T, raise T to the ratio at which that cycle has weight 0.

All arithmetic is exact with Fractions or integers.
"""

from fractions import Fraction


def constraint_edges(n, paths, t_setup, t_hold):
    """Edges (v, u, a, b) meaning c_u - c_v <= a T + b."""
    edges = []
    for i, j, dmax, dmin in paths:
        edges.append((j, i, 1, -(dmax + t_setup)))  # setup: c_i - c_j <= T - dmax - t_setup
        edges.append((i, j, 0, dmin - t_hold))  # hold: c_j - c_i <= dmin - t_hold
    return edges


def bellman_ford(n, edges, T):
    """Return (None, dist) when no cycle is negative at period T, else
    (cycle, None) with the edge indices of one negative simple cycle."""
    dist = [Fraction(0)] * n
    pred = [None] * n
    last = None
    for _ in range(n):
        last = None
        for k, (v, u, a, b) in enumerate(edges):
            w = a * T + b
            if dist[v] + w < dist[u]:
                dist[u] = dist[v] + w
                pred[u] = k
                last = u
        if last is None:
            return None, dist
    x = last
    for _ in range(n):
        x = edges[pred[x]][0]
    cycle, y = [], x
    while True:
        k = pred[y]
        cycle.append(k)
        y = edges[k][0]
        if y == x:
            break
    cycle.reverse()
    return cycle, None


def min_period(n, paths, t_setup=0, t_hold=0):
    """Return (T, c, rounds): the least clock period, a clock schedule that
    meets it with min(c) = 0, and the number of Bellman-Ford rounds. Return
    None when the hold constraints alone have a negative cycle, since then
    no period works."""
    edges = constraint_edges(n, paths, t_setup, t_hold)
    hold = [e for e in edges if e[2] == 0]
    cyc, _ = bellman_ford(n, hold, Fraction(0))
    if cyc is not None:  # @line L1
        return None
    if not paths:
        return Fraction(0), [Fraction(0)] * n, 0
    # start at the largest bound of a 2-cycle (the setup and hold edge of one path)
    T = max(Fraction(dmax - dmin + t_setup + t_hold) for _, _, dmax, dmin in paths)  # @line L2
    rounds = 0
    while True:  # @line L3
        rounds += 1
        cyc, dist = bellman_ford(n, edges, T)  # @line L4
        if cyc is None:  # @line L5
            low = min(dist)
            return T, [d - low for d in dist], rounds  # @line L6
        k = sum(edges[e][2] for e in cyc)  # @line L7
        s = -sum(edges[e][3] for e in cyc)
        T = Fraction(s, k)  # @line L8
