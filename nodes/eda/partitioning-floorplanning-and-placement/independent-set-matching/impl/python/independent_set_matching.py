# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independent-set-matching/. The authors are listed in prov/CJ581B.jsonl.

"""Independent set matching for detailed placement.

Cells 0 .. n-1 sit on sites: cell i has the integer left edge x[i], the row row[i] and the
integer width W[i]; rows have height h. A pin of a net is a cell index i < n, which stands for the
center of cell i, or an index n + j, which stands for the fixed pad pads[j] = (px, py).
Net k has the pin list nets[k] and the weight weights[k]. Wirelength is HPWL, computed exactly.
"""

from fractions import Fraction
from typing import Sequence


def pin_point(p, x, row, W, pads, h):
    n = len(x)
    if p < n:
        return Fraction(x[p]) + Fraction(W[p], 2), Fraction(row[p] * h) + Fraction(h, 2)
    px, py = pads[p - n]
    return Fraction(px), Fraction(py)


def net_hpwl(pins, x, row, W, pads, h=1) -> Fraction:
    pts = [pin_point(p, x, row, W, pads, h) for p in pins]
    xs = [a for a, _ in pts]
    ys = [b for _, b in pts]
    return (max(xs) - min(xs)) + (max(ys) - min(ys))


def total_hpwl(x, row, W, nets, weights, pads, h=1) -> Fraction:
    return sum(Fraction(weights[k]) * net_hpwl(nets[k], x, row, W, pads, h) for k in range(len(nets)))


def nets_of_cells(n: int, nets) -> list:
    out = [[] for _ in range(n)]
    for k, pins in enumerate(nets):
        for p in set(pins):
            if p < n:
                out[p].append(k)
    return out


def choose_set(seed, x, row, W, cell_nets, k, wx, wy) -> list:
    """Greedy independent set: the seed, then cells of the same width in the window, nearest first,
    each taken only if it shares no net with the cells taken before."""
    used = set(cell_nets[seed])
    chosen = [seed]
    cand = [c for c in range(len(x)) if c != seed and W[c] == W[seed]
            and abs(x[c] - x[seed]) <= wx and abs(row[c] - row[seed]) <= wy]
    cand.sort(key=lambda c: (abs(x[c] - x[seed]) + abs(row[c] - row[seed]), c))
    for c in cand:
        if len(chosen) == k:
            break
        if used.isdisjoint(cell_nets[c]):
            chosen.append(c)
            used.update(cell_nets[c])
    return chosen


def cost_matrix(S, x, row, W, nets, weights, pads, cell_nets, h=1) -> list:
    """cost[a][b]: the weighted HPWL of the nets of cell S[a] with S[a] at the slot of S[b]
    and every other cell where it is."""
    slots = [(x[c], row[c]) for c in S]
    cost = []
    for c in S:
        line = []
        old = (x[c], row[c])
        for sx, sr in slots:
            x[c], row[c] = sx, sr
            line.append(sum(Fraction(weights[k]) * net_hpwl(nets[k], x, row, W, pads, h) for k in cell_nets[c]))
        x[c], row[c] = old
        cost.append(line)
    return cost


def hungarian(cost) -> tuple:
    """Minimum cost perfect assignment of a square matrix by shortest augmenting paths with
    potentials, O(k^3). Returns (assign, value) with assign[a] = the column of row a."""
    k = len(cost)
    INF = None
    u = [Fraction(0)] * (k + 1)
    v = [Fraction(0)] * (k + 1)
    p = [0] * (k + 1)  # p[j]: the row matched to column j (1-based), 0 if none
    way = [0] * (k + 1)
    for i in range(1, k + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (k + 1)
        done = [False] * (k + 1)
        while True:
            done[j0] = True
            i0 = p[j0]
            delta, j1 = INF, 0
            for j in range(1, k + 1):
                if not done[j]:
                    cur = Fraction(cost[i0 - 1][j - 1]) - u[i0] - v[j]
                    if minv[j] is None or cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if delta is None or minv[j] < delta:
                        delta, j1 = minv[j], j
            for j in range(k + 1):
                if done[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    assign = [0] * k
    for j in range(1, k + 1):
        assign[p[j] - 1] = j - 1
    return assign, sum(Fraction(cost[a][assign[a]]) for a in range(k))


def ism(x, row, W, nets, weights, pads, k=5, wx=4, wy=1, passes=1, h=1):
    """Return new (x, row) after the given number of passes of independent set matching.
    The input lists are not changed."""
    x, row = list(x), list(row)
    n = len(x)
    cell_nets = nets_of_cells(n, nets)
    for _ in range(passes):  # @line L1
        for seed in sorted(range(n), key=lambda c: (row[c], x[c], c)):  # @line L2
            S = choose_set(seed, x, row, W, cell_nets, k, wx, wy)  # @line L3
            if len(S) < 2:  # @line L4
                continue
            slots = [(x[c], row[c]) for c in S]  # @line L5
            cost = cost_matrix(S, x, row, W, nets, weights, pads, cell_nets, h)  # @line L6
            assign, _ = hungarian(cost)  # @line L7
            for a, c in enumerate(S):  # @line L8
                x[c], row[c] = slots[assign[a]]
    return x, row
