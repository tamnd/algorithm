# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lagrangian-relaxation-gate-sizing/. The authors are listed in prov/AB69M9.jsonl.
"""Gate sizing by Lagrangian relaxation (Chen, Chu and Wong, 1999).

The circuit is a DAG of gates 0..n-1 in topological order. Gate i has an
intrinsic delay p[i], a drive resistance r[i] / x for size x, an input
capacitance c[i] * x, an area a[i] * x, a fixed load f[i] and a size range
lo[i] <= x <= hi[i]. Its delay is

    D_i = p[i] + r[i] / x_i * (f[i] + sum of c[j] * x_j over fanouts j).

The timing graph has a source s with an edge to each gate without fanins,
the circuit edges, and an edge from each gate without fanouts to a sink t.
A multiplier mu[e] >= 0 sits on every edge. The problem is: least area such
that every arrival time is at most the target T. Arithmetic is in floating
point, since the local resizing uses square roots.
"""

import math


class Circuit:
    def __init__(self, fanin, p, r, c, a, f, lo, hi):
        self.n = len(fanin)
        self.fanin = [list(v) for v in fanin]
        self.fanout = [[] for _ in range(self.n)]
        for j, ins in enumerate(self.fanin):
            for i in ins:
                assert i < j
                self.fanout[i].append(j)
        self.p, self.r, self.c, self.a, self.f = p, r, c, a, f
        self.lo, self.hi = lo, hi
        # edges as (tail, head); tail -1 is the source, head n is the sink
        self.edges = [(-1, j) for j in range(self.n) if not self.fanin[j]]
        self.edges += [(i, j) for j in range(self.n) for i in self.fanin[j]]
        self.edges += [(i, self.n) for i in range(self.n) if not self.fanout[i]]


def gate_delay(ckt, x, i):
    load = ckt.f[i] + sum(ckt.c[j] * x[j] for j in ckt.fanout[i])
    return ckt.p[i] + ckt.r[i] / x[i] * load


def arrivals(ckt, x):
    arr = []
    for i in range(ckt.n):
        arr.append(max([arr[k] for k in ckt.fanin[i]], default=0.0) + gate_delay(ckt, x, i))
    return arr


def delay(ckt, x):
    return max(arrivals(ckt, x))


def area(ckt, x):
    return sum(ckt.a[i] * x[i] for i in range(ckt.n))


def flow_through(ckt, mu):
    """lambda_i: the sum of the multipliers on the edges into gate i."""
    lam = [0.0] * ckt.n
    for e, (u, v) in enumerate(ckt.edges):
        if v < ckt.n:
            lam[v] += mu[e]
    return lam


def project(ckt, mu):
    """Restore flow conservation: scale the edges into each gate, from the
    outputs back to the inputs, so that they carry what leaves the gate."""
    mu = list(mu)
    into = [[] for _ in range(ckt.n)]
    out_of = [[] for _ in range(ckt.n)]
    for e, (u, v) in enumerate(ckt.edges):
        if v < ckt.n:
            into[v].append(e)
        if u >= 0:
            out_of[u].append(e)
    for i in reversed(range(ckt.n)):
        need = sum(mu[e] for e in out_of[i])
        have = sum(mu[e] for e in into[i])
        for e in into[i]:
            mu[e] = need * mu[e] / have if have > 0 else need / len(into[i])
    return mu


def local_resize(ckt, lam, x, sweeps=200, tol=1e-12):
    """Solve min sum a_i x_i + sum lam_i D_i(x) over the box, one gate at a
    time in closed form, until no size moves."""
    x = list(x)
    for _ in range(sweeps):
        moved = 0.0
        for i in range(ckt.n):
            load = ckt.f[i] + sum(ckt.c[j] * x[j] for j in ckt.fanout[i])
            up = sum(lam[k] * ckt.r[k] / x[k] for k in ckt.fanin[i])
            den = ckt.a[i] + ckt.c[i] * up
            best = math.sqrt(lam[i] * ckt.r[i] * load / den) if lam[i] * load > 0 else ckt.lo[i]
            best = min(max(best, ckt.lo[i]), ckt.hi[i])  # @line L4
            moved = max(moved, abs(best - x[i]) / x[i])
            x[i] = best
        if moved < tol:
            break
    return x


def lr_sizing(ckt, target, rounds=3000, power=1.0):
    """Return (sizes, multipliers) after the given number of rounds.

    The multipliers are updated by the multiplicative rule: an edge into a
    gate is scaled by (arrival through the edge) / (arrival at the gate),
    which is 1 on a critical edge and below 1 otherwise, and an edge into the
    sink is scaled by (arrival) / target. Multipliers stay positive, so the
    projection can always move flow back to an edge that becomes critical."""
    mu = [1.0 if v == ckt.n else 0.0 for (u, v) in ckt.edges]  # @line L1
    mu = project(ckt, mu)
    x = list(ckt.lo)
    for _ in range(rounds):  # @line L2
        lam = flow_through(ckt, mu)  # @line L3
        x = local_resize(ckt, lam, x)
        arr = arrivals(ckt, x)  # @line L5
        new = []
        for e, (u, v) in enumerate(ckt.edges):  # @line L6
            if v == ckt.n:
                ratio = arr[u] / target
            else:
                start = 0.0 if u < 0 else arr[u]
                ratio = (start + gate_delay(ckt, x, v)) / arr[v]
            new.append(mu[e] * ratio ** power)
        mu = project(ckt, new)  # @line L7
    return x, mu  # @line L8
