# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simulated-annealing-placement/. The authors are listed in prov/ZEMFMQ.jsonl.
"""Simulated annealing placement in the style of TimberWolf.

Cells have integer widths W[i] and sit on K rows of S unit sites; row r has height 1.
A cell is given by its row r[i] and its left site x[i]; its pin is at its center.
Pads are fixed points; pin index n + j is pad j. During the annealing cells may overlap.
All costs are kept in doubled integer units so that the deltas are exact:
cost = 2 HPWL + mu * overlap, where overlap counts the sites held by more than one cell.
"""

import math
import random


def pin2(p, x, r, W, n, pads):
    """The doubled coordinates of pin p."""
    if p < n:
        return 2 * x[p] + W[p], 2 * r[p] + 1
    return 2 * pads[p - n][0], 2 * pads[p - n][1]


def net_cost2(e, x, r, W, n, pads):
    """Twice the HPWL of the net e."""
    xs, ys = zip(*(pin2(p, x, r, W, n, pads) for p in e))
    return max(xs) - min(xs) + max(ys) - min(ys)


def overlap(x, r, W, K, S):
    """The number of extra cells over all sites: sum of max(0, occupancy - 1)."""
    occ = [[0] * S for _ in range(K)]
    for i in range(len(x)):
        for s in range(x[i], x[i] + W[i]):
            occ[r[i]][s] += 1
    return sum(max(0, c - 1) for row in occ for c in row)


def full_cost(x, r, W, nets, pads, K, S, mu):
    n = len(x)
    return sum(net_cost2(e, x, r, W, n, pads) for e in nets) + mu * overlap(x, r, W, K, S)


class State:
    """A placement with its occupancy, its overlap and its cost, updated by moves."""

    def __init__(self, x, r, W, nets, pads, K, S, mu):
        self.x, self.r, self.W = list(x), list(r), W
        self.nets, self.pads, self.K, self.S, self.mu = nets, pads, K, S, mu
        self.n = len(x)
        self.cell_nets = [[] for _ in range(self.n)]
        for k, e in enumerate(nets):
            for p in set(e):
                if p < self.n:
                    self.cell_nets[p].append(k)
        self.occ = [[0] * S for _ in range(K)]
        self.over = 0
        for i in range(self.n):
            self._add(i)
        self.cost = sum(net_cost2(e, self.x, self.r, W, self.n, pads) for e in nets) + mu * self.over

    def _add(self, i):
        row = self.occ[self.r[i]]
        for s in range(self.x[i], self.x[i] + self.W[i]):
            if row[s] >= 1:
                self.over += 1
            row[s] += 1

    def _remove(self, i):
        row = self.occ[self.r[i]]
        for s in range(self.x[i], self.x[i] + self.W[i]):
            row[s] -= 1
            if row[s] >= 1:
                self.over -= 1

    def apply(self, moves):
        """Apply moves [(cell, new x, new row), ...] and return (delta, the reverse moves)."""
        cells = [c for c, _, _ in moves]
        touched = {k for c in cells for k in self.cell_nets[c]}
        before = sum(net_cost2(self.nets[k], self.x, self.r, self.W, self.n, self.pads) for k in touched)
        over0 = self.over
        back = [(c, self.x[c], self.r[c]) for c in cells]
        for c in cells:
            self._remove(c)
        for c, nx, nr in moves:
            self.x[c], self.r[c] = nx, nr
        for c in cells:
            self._add(c)
        after = sum(net_cost2(self.nets[k], self.x, self.r, self.W, self.n, self.pads) for k in touched)
        delta = after - before + self.mu * (self.over - over0)
        self.cost += delta
        return delta, back


def propose(st, rng, wx, wr, p_swap):
    """A displacement or a swap inside the range limiter window, or None."""
    i = rng.randrange(st.n)
    if rng.random() < p_swap and st.n > 1:
        j = rng.randrange(st.n - 1)
        j += j >= i
        if abs(st.x[j] - st.x[i]) > wx or abs(st.r[j] - st.r[i]) > wr:
            return None
        return [(i, min(st.x[j], st.S - st.W[i]), st.r[j]), (j, min(st.x[i], st.S - st.W[j]), st.r[i])]
    nx = min(max(st.x[i] + rng.randint(-wx, wx), 0), st.S - st.W[i])
    nr = min(max(st.r[i] + rng.randint(-wr, wr), 0), st.K - 1)
    if (nx, nr) == (st.x[i], st.r[i]):
        return None
    return [(i, nx, nr)]


def pack_row(cells, tx, W, S):
    """Left sites for the cells of one row of S sites whose widths fit: in the order of
    their targets, each goes to the site nearest its target but right of the previous cell;
    then a pass from the right pulls the cells back inside the row."""
    order = sorted(cells, key=lambda i: (tx[i], i))
    pos, end = {}, 0
    for i in order:
        want = int(round(tx[i] - W[i] / 2))
        pos[i] = max(end, min(max(want, 0), S - W[i]))
        end = pos[i] + W[i]
    limit = S
    for i in reversed(order):
        pos[i] = min(pos[i], limit - W[i])
        limit = pos[i]
    return pos


def pack_rows(x, r, W, K, S):
    """Move cells out of overfull rows to the nearest row with room, then pack each row."""
    r = list(r)
    load = [0] * K
    for i in range(len(x)):
        load[r[i]] += W[i]
    for k in range(K):
        while load[k] > S:
            i = min((c for c in range(len(x)) if r[c] == k), key=lambda c: (W[c], c))
            room = [q for q in range(K) if load[q] + W[i] <= S]
            if not room:
                raise ValueError("no row has room for a cell of an overfull row")
            q = min(room, key=lambda q: (abs(q - k), q))
            load[k] -= W[i]
            load[q] += W[i]
            r[i] = q
    tx = [x[i] + W[i] / 2 for i in range(len(x))]
    nx = list(x)
    for k in range(K):
        for i, p in pack_row([c for c in range(len(x)) if r[c] == k], tx, W, S).items():
            nx[i] = p
    return nx, r


def anneal(n, nets, pads, W, K, S, seed=0, T0=None, T_end=0.05, alpha=0.9,
           moves_per_cell=20, mu=8, p_swap=0.5, trace=None):
    """Anneal a placement and return a legal one as (x, r)."""
    rng = random.Random(seed)
    st = State([rng.randint(0, S - W[i]) for i in range(n)], [rng.randrange(K) for _ in range(n)],
               W, nets, pads, K, S, mu)  # @line L1
    if T0 is None:  # a start temperature that accepts about 90% of the uphill moves
        ups = []
        for _ in range(4 * n):
            mv = propose(st, rng, S, K, p_swap)
            if mv:
                d, back = st.apply(mv)
                st.apply(back)
                if d > 0:
                    ups.append(d)
        T0 = (sum(ups) / len(ups) if ups else 1) / math.log(1 / 0.9)
    T = T0
    while T > T_end:  # @line L2
        frac = math.log(T / T_end) / math.log(T0 / T_end) if T0 > T_end else 0
        wx, wr = max(1, round(S * frac)), max(1, round(K * frac))  # @line L3
        for _ in range(moves_per_cell * n):  # @line L4
            mv = propose(st, rng, wx, wr, p_swap)  # @line L5
            if mv is None:
                continue
            d, back = st.apply(mv)  # @line L6
            if d > 0 and rng.random() >= math.exp(-d / T):  # @line L7
                st.apply(back)
        if trace is not None:
            trace.append((T, st.cost))
        T *= alpha  # @line L8
    return pack_rows(st.x, st.r, W, K, S)  # @line L9
