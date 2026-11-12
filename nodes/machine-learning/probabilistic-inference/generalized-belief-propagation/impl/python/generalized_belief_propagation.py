# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-belief-propagation/. The authors are listed in prov/7XZC5Z.jsonl.

"""Generalized belief propagation: the parent-to-child algorithm of Yedidia,
Freeman and Weiss on a cluster variation (Kikuchi) region graph.

A model is a list card of variable cardinalities and a list of factors
(scope, table), with table mapping each assignment of the scope to a positive
number; p(x) = prod_a f_a(x_a) / Z.

The region graph is built from a list of outer regions (sets of variables).
Every factor must lie inside some outer region. The regions are the outer
regions and all their intersections, closed under intersection. A region R
holds the factors whose scopes lie inside R (A_R), has the counting number
c_R = 1 - sum of c_S over the regions S that strictly contain R, and has an
edge to each region directly below it (a strict subset with no region in
between). Messages go from a parent P to a child R and are functions of x_R.
"""

import itertools
import math


class RegionGraph:
    def __init__(self, card, factors, outer):
        self.card = card
        self.factors = factors
        regions = {frozenset(r) for r in outer}
        while True:  # close under intersection
            new = {a & b for a in regions for b in regions if a != b and a & b} - regions
            if not new:
                break
            regions |= new
        for scope, _ in factors:
            if not any(set(scope) <= r for r in regions):
                raise ValueError("a factor is not inside any region")
        # Larger regions first, so that the counting numbers can be computed in order.
        self.regions = sorted(regions, key=lambda r: (-len(r), sorted(r)))
        self.vars = [tuple(sorted(r)) for r in self.regions]
        self.index = {r: k for k, r in enumerate(self.regions)}
        self.counting = []
        for r in self.regions:
            self.counting.append(1 - sum(self.counting[self.index[s]] for s in self.regions if r < s))
        self.inside = [[a for a, (scope, _) in enumerate(factors) if set(scope) <= r] for r in self.regions]
        self.edges = []
        for p in self.regions:
            for c in self.regions:
                if c < p and not any(c < s < p for s in self.regions):
                    self.edges.append((self.index[p], self.index[c]))
        # E(R): R and all its descendants (all regions inside R, since edges are the Hasse diagram).
        self.desc = [{self.index[s] for s in self.regions if s <= r} for r in self.regions]
        # M(R): the edges (I, J) with J in E(R) and I not in E(R).
        self.into = [[e for e in self.edges if e[1] in self.desc[r] and e[0] not in self.desc[r]]
                     for r in range(len(self.regions))]
        self.num = {}
        self.den = {}
        for p, r in self.edges:
            ep, er = self.desc[p], self.desc[r]
            # N(P, R): (I, J) with J in E(P) minus E(R), and I outside E(P).
            self.num[(p, r)] = [e for e in self.edges if e[1] in ep - er and e[0] not in ep]
            # D(P, R): (I, J) with J in E(R), I in E(P) minus E(R), other than (P, R).
            self.den[(p, r)] = [e for e in self.edges if e[1] in er and e[0] in ep - er and e != (p, r)]

    def assignments(self, k):
        return list(itertools.product(*[range(self.card[v]) for v in self.vars[k]]))

    def restrict(self, k, sub, x):
        """The assignment of region sub inside the assignment x of region k."""
        pos = {v: i for i, v in enumerate(self.vars[k])}
        return tuple(x[pos[v]] for v in self.vars[sub])

    def factor_product(self, k, x, factor_ids):
        pos = {v: i for i, v in enumerate(self.vars[k])}
        w = 1.0
        for a in factor_ids:
            scope, table = self.factors[a]
            w *= table[tuple(x[pos[v]] for v in scope)]
        return w

    def belief(self, k, msgs):
        """b_R(x_R) proportional to prod_{a in A_R} f_a times the messages M(R)."""
        b = {}
        for x in self.assignments(k):
            w = self.factor_product(k, x, self.inside[k])
            for (i, j) in self.into[k]:
                w *= msgs[(i, j)][self.restrict(k, j, x)]
            b[x] = w
        s = sum(b.values())
        return {x: v / s for x, v in b.items()}


def _normalize(d):
    s = sum(d.values())
    return {k: v / s for k, v in d.items()}


def parent_to_child_message(g, msgs, p, r):
    """m_{P->R}(x_R) = sum_{x_{P minus R}} prod_{A_P minus A_R} f prod_{N(P,R)} m / prod_{D(P,R)} m."""
    extra = [a for a in g.inside[p] if a not in g.inside[r]]
    out = {y: 0.0 for y in g.assignments(r)}
    for x in g.assignments(p):
        w = g.factor_product(p, x, extra)
        for (i, j) in g.num[(p, r)]:
            w *= msgs[(i, j)][g.restrict(p, j, x)]
        out[g.restrict(p, r, x)] += w
    for y in out:
        for (i, j) in g.den[(p, r)]:
            out[y] /= msgs[(i, j)][g.restrict(r, j, y)]
    return _normalize(out)


def gbp(card, factors, outer, damping=0.5, tol=1e-10, max_iter=5000):
    """Run parent-to-child GBP with a sequential schedule: in each sweep the
    messages are updated one at a time, those into larger children first, and
    each update uses the newest values of the others. Return (region graph,
    beliefs per region, sweeps, converged)."""
    if not 0.0 <= damping < 1.0:
        raise ValueError("damping must be in [0, 1)")
    g = RegionGraph(card, factors, outer)  # @line L1
    msgs = {e: _normalize({y: 1.0 for y in g.assignments(e[1])}) for e in g.edges}  # @line L2
    order = sorted(g.edges, key=lambda e: (-len(g.vars[e[1]]), e))
    converged = False
    it = 0
    for it in range(1, max_iter + 1):  # @line L3
        delta = 0.0
        for e in order:
            new = parent_to_child_message(g, msgs, *e)  # @line L4
            delta = max(delta, max(abs(new[y] - msgs[e][y]) for y in new))  # @line L5
            msgs[e] = _normalize({y: (1 - damping) * new[y] + damping * msgs[e][y] for y in new})  # @line L6
        if delta < tol:  # @line L7
            converged = True
            break
    beliefs = [g.belief(k, msgs) for k in range(len(g.regions))]  # @line L8
    return g, beliefs, it, converged


def variable_marginals(g, beliefs):
    """The marginal of each variable from the smallest region that holds it."""
    out = []
    for v in range(len(g.card)):
        k = min((k for k, r in enumerate(g.regions) if v in r), key=lambda k: len(g.regions[k]))
        pos = g.vars[k].index(v)
        m = [0.0] * g.card[v]
        for x, prob in beliefs[k].items():
            m[x[pos]] += prob
        out.append(m)
    return out


def kikuchi_free_energy(g, beliefs):
    """F_K(b) = sum_R c_R sum_{x_R} b_R(x_R) [log b_R(x_R) - log prod_{a in A_R} f_a(x_a)]."""
    total = 0.0
    for k, b in enumerate(beliefs):
        if g.counting[k] == 0:
            continue
        s = 0.0
        for x, prob in b.items():
            if prob > 0:
                s += prob * (math.log(prob) - math.log(g.factor_product(k, x, g.inside[k])))
        total += g.counting[k] * s
    return total


def exact_marginals(card, factors):
    marg = [[0.0] * c for c in card]
    z = 0.0
    for x in itertools.product(*[range(c) for c in card]):
        w = 1.0
        for scope, table in factors:
            w *= table[tuple(x[j] for j in scope)]
        z += w
        for i, xi in enumerate(x):
            marg[i][xi] += w
    return [[v / z for v in m] for m in marg], math.log(z)


def ising_factors(n, fields, couplings):
    """Spins in {-1, +1}, state 0 is -1: unary exp(h s) and pairwise exp(J s t)."""
    spin = (-1, 1)
    factors = [((i,), {(a,): math.exp(h * spin[a]) for a in range(2)}) for i, h in enumerate(fields)]
    for i, j, w in couplings:
        factors.append(((i, j), {(a, b): math.exp(w * spin[a] * spin[b]) for a in range(2) for b in range(2)}))
    return [2] * n, factors


def grid_edges(rows, cols):
    idx = lambda r, c: r * cols + c
    edges = [(idx(r, c), idx(r, c + 1)) for r in range(rows) for c in range(cols - 1)]
    edges += [(idx(r, c), idx(r + 1, c)) for r in range(rows - 1) for c in range(cols)]
    return edges


def plaquettes(rows, cols):
    """The outer regions of the cluster variation method on a grid: all 2x2 squares."""
    idx = lambda r, c: r * cols + c
    return [{idx(r, c), idx(r, c + 1), idx(r + 1, c), idx(r + 1, c + 1)}
            for r in range(rows - 1) for c in range(cols - 1)]
