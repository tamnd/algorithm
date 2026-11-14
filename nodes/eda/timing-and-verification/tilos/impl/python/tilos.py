# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tilos/. The authors are listed in prov/Q10RHR.jsonl.
"""TILOS: greedy upsizing on the critical path (Fishburn and Dunlop, 1985).

The circuit is a DAG of gates 0..n-1 in topological order. Gate i has an
intrinsic delay p[i], a drive resistance r[i] / x for size x, an input
capacitance c[i] * x, an area a[i] * x, a fixed load f[i] (wire and, for an
output, the external load) and a list sizes[i] of allowed sizes in
increasing order. Its delay is

    D_i = p[i] + r[i] / x_i * (f[i] + sum of c[j] * x_j over fanouts j),

an Elmore delay of a switch-level RC model. A gate without fanins starts at
time 0, the arrival time of a gate is the latest fanin arrival plus its own
delay, and the circuit delay is the latest arrival over all gates. All
arithmetic is exact with Fractions.
"""

from fractions import Fraction


class Circuit:
    def __init__(self, fanin, p, r, c, a, f, sizes):
        self.n = len(fanin)
        self.fanin = [list(v) for v in fanin]
        self.fanout = [[] for _ in range(self.n)]
        for j, ins in enumerate(self.fanin):
            for i in ins:
                assert i < j  # topological order
                self.fanout[i].append(j)
        self.p, self.r, self.c, self.a, self.f = p, r, c, a, f
        self.sizes = [sorted(s) for s in sizes]


def gate_delay(ckt, x, i):
    load = ckt.f[i] + sum(ckt.c[j] * x[j] for j in ckt.fanout[i])
    return ckt.p[i] + Fraction(ckt.r[i]) / x[i] * load


def arrivals(ckt, x):
    """Arrival time of each gate and the fanin that sets it (or None)."""
    arr, pred = [], []
    for i in range(ckt.n):
        best, who = Fraction(0), None
        for k in ckt.fanin[i]:
            if who is None or arr[k] > best:
                best, who = arr[k], k
        arr.append(best + gate_delay(ckt, x, i))
        pred.append(who)
    return arr, pred


def delay(ckt, x):
    return max(arrivals(ckt, x)[0])


def area(ckt, x):
    return sum(ckt.a[i] * x[i] for i in range(ckt.n))


def critical_path(ckt, x):
    arr, pred = arrivals(ckt, x)
    g = max(range(ckt.n), key=lambda i: (arr[i], -i))
    path = []
    while g is not None:
        path.append(g)
        g = pred[g]
    return path[::-1]


def path_delay(ckt, x, path):
    return sum(gate_delay(ckt, x, g) for g in path)


def tilos(ckt, target):
    """Return the sizes found by TILOS, or None if it gets stuck."""
    x = [s[0] for s in ckt.sizes]  # @line L1
    step = [0] * ckt.n
    while True:
        if delay(ckt, x) <= target:  # @line L2
            return x
        path = critical_path(ckt, x)  # @line L3
        best, best_ratio = None, None
        on_path = set(path)
        for g in path:  # @line L4
            if step[g] + 1 == len(ckt.sizes[g]):
                continue
            y = list(x)
            y[g] = ckt.sizes[g][step[g] + 1]
            # only g and its fanins change their delay
            touched = [g] + [k for k in ckt.fanin[g] if k in on_path]
            gain = path_delay(ckt, x, touched) - path_delay(ckt, y, touched)  # @line L5
            ratio = gain / (ckt.a[g] * (y[g] - x[g]))
            if gain > 0 and (best is None or ratio > best_ratio):  # @line L6
                best, best_ratio = g, ratio
        if best is None:  # @line L7
            return None
        step[best] += 1  # @line L8
        x[best] = ckt.sizes[best][step[best]]
