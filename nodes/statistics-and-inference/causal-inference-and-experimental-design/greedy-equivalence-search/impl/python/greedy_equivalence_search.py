# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-equivalence-search/. The authors are listed in prov/08T080.jsonl.
"""Greedy equivalence search (GES) of Chickering (2002).

The state is a CPDAG: a graph with directed edges (pa, ch) and undirected
edges (nb) that stands for a Markov equivalence class of DAGs. The score is
decomposable: score(dag) = sum of local(v, parents of v). The forward phase
applies the best Insert operator while it raises the score; the backward
phase applies the best Delete operator while it raises the score.

The module also has the Gaussian BIC local score, computed from a covariance
matrix, and helpers that make covariances of linear models exactly with
fractions.
"""

import itertools
import math
from fractions import Fraction
from typing import NamedTuple


class PDAG:
    """Partially directed graph: pa[v] -> v, v -> ch[v], v - nb[v]."""

    def __init__(self, nodes):
        self.nodes = list(nodes)
        self.pa = {v: set() for v in self.nodes}
        self.ch = {v: set() for v in self.nodes}
        self.nb = {v: set() for v in self.nodes}

    def copy(self):
        g = PDAG(self.nodes)
        for v in self.nodes:
            g.pa[v] = set(self.pa[v])
            g.ch[v] = set(self.ch[v])
            g.nb[v] = set(self.nb[v])
        return g

    def adj(self, v):
        return self.pa[v] | self.ch[v] | self.nb[v]

    def adjacent(self, a, b):
        return b in self.adj(a)

    def add_arrow(self, a, b):
        self.ch[a].add(b)
        self.pa[b].add(a)

    def add_line(self, a, b):
        self.nb[a].add(b)
        self.nb[b].add(a)

    def remove(self, a, b):
        for d in (self.pa, self.ch, self.nb):
            d[a].discard(b)
            d[b].discard(a)

    def orient(self, a, b):
        """Turn the undirected edge a - b into a -> b."""
        self.nb[a].discard(b)
        self.nb[b].discard(a)
        self.add_arrow(a, b)

    def edges(self):
        arrows = sorted((a, b) for a in self.nodes for b in self.ch[a])
        lines = sorted((a, b) for a in self.nodes for b in self.nb[a] if str(a) < str(b))
        return arrows, lines


def is_clique(g, s):
    return all(g.adjacent(a, b) for a, b in itertools.combinations(s, 2))


def blocks_semi_directed(g, y, x, block):
    """True if every semi-directed path from y to x meets the set block."""
    seen, stack = {y}, [y]
    while stack:
        v = stack.pop()
        for w in g.ch[v] | g.nb[v]:
            if w == x:
                return False
            if w not in seen and w not in block:
                seen.add(w)
                stack.append(w)
    return True


# ---------------------------------------------------------------------------
# From a PDAG to a DAG and from a DAG to its CPDAG


def consistent_extension(g):
    """A DAG with the skeleton and the arrows of g and no new v-structure
    (Dor and Tarsi 1992). Returns parents as a dict, or None if there is none."""
    h = g.copy()
    parents = {v: set(g.pa[v]) for v in g.nodes}
    left = set(g.nodes)
    while left:
        for x in sorted(left, key=str):
            if h.ch[x]:
                continue
            others = h.adj(x)
            if all(others - {y} <= h.adj(y) for y in h.nb[x]):
                for y in h.nb[x]:
                    parents[x].add(y)  # orient y -> x
                for y in list(h.adj(x)):
                    h.remove(x, y)
                left.discard(x)
                break
        else:
            return None
    return parents


def cpdag_of_dag(nodes, parents):
    """The CPDAG of a DAG: arrows of v-structures, then Meek's rules R1 to R3."""
    g = PDAG(nodes)
    for v in nodes:
        for p in parents[v]:
            g.add_line(p, v)
    for c in nodes:
        for a, b in itertools.combinations(sorted(parents[c], key=str), 2):
            if not g.adjacent(a, b):
                for u in (a, b):
                    if u in g.nb[c]:
                        g.orient(u, c)
    changed = True
    while changed:
        changed = False
        for b in nodes:
            for c in list(g.nb[b]):
                if c not in g.nb[b]:
                    continue
                r1 = any(not g.adjacent(a, c) for a in g.pa[b])
                r2 = any(a in g.pa[c] for a in g.ch[b])
                r3 = any(not g.adjacent(a1, a2) and {a1, a2} <= g.pa[c]
                         for a1, a2 in itertools.combinations(g.nb[b], 2))
                if r1 or r2 or r3:
                    g.orient(b, c)
                    changed = True
    return g


# ---------------------------------------------------------------------------
# GES


class GESResult(NamedTuple):
    cpdag: PDAG
    steps: list        # ("insert" or "delete", x, y, set, delta)
    evaluations: int   # number of operators whose score change was computed


def ges(nodes, local):
    """Greedy equivalence search with the decomposable local score local(v, frozenset)."""
    g = PDAG(nodes)  # @line L1
    steps = []
    evals = 0

    def s(v, ps):
        return local(v, frozenset(ps))

    while True:  # @line L2
        best = None
        for x in g.nodes:
            for y in g.nodes:
                if x == y or g.adjacent(x, y):
                    continue
                na = g.nb[y] & g.adj(x)
                t0 = sorted(g.nb[y] - g.adj(x), key=str)
                for k in range(len(t0) + 1):
                    for t in itertools.combinations(t0, k):  # @line L3
                        t = set(t)
                        if not is_clique(g, na | t) or not blocks_semi_directed(g, y, x, na | t):  # @line L4
                            continue
                        evals += 1
                        base = na | t | g.pa[y]
                        delta = s(y, base | {x}) - s(y, base)  # @line L5
                        if best is None or delta > best[0]:
                            best = (delta, x, y, t)
        if best is None or best[0] <= 0:  # @line L6
            break
        delta, x, y, t = best
        h = g.copy()
        h.add_arrow(x, y)
        for u in t:
            h.orient(u, y)
        g = cpdag_of_dag(g.nodes, consistent_extension(h))  # @line L7
        steps.append(("insert", x, y, t, delta))

    while True:  # @line L8
        best = None
        for x in g.nodes:
            for y in g.nodes:
                if x == y or not (x in g.pa[y] or x in g.nb[y]):
                    continue
                na = g.nb[y] & g.adj(x)
                h0 = sorted(na, key=str)
                for k in range(len(h0) + 1):
                    for hs in itertools.combinations(h0, k):  # @line L9
                        hs = set(hs)
                        if not is_clique(g, na - hs):  # @line L10
                            continue
                        evals += 1
                        base = (na - hs) | g.pa[y]
                        delta = s(y, base - {x}) - s(y, base | {x})  # @line L11
                        if best is None or delta > best[0]:
                            best = (delta, x, y, hs)
        if best is None or best[0] <= 0:  # @line L12
            break
        delta, x, y, hs = best
        h = g.copy()
        h.remove(x, y)
        for u in hs:
            if u in h.nb[y]:
                h.orient(y, u)
            if u in h.nb[x]:
                h.orient(x, u)
        g = cpdag_of_dag(g.nodes, consistent_extension(h))  # @line L13
        steps.append(("delete", x, y, hs, delta))
    return GESResult(g, steps, evals)  # @line L14


# ---------------------------------------------------------------------------
# Gaussian BIC score


def conditional_variance(cov, v, ps):
    """Var(v | ps) = cov[v][v] - cov[v,P] cov[P,P]^-1 cov[P,v], by elimination.
    Works with floats or with exact fractions."""
    ps = list(ps)
    k = len(ps)
    a = [[cov[p][q] for q in ps] + [cov[p][v]] for p in ps]
    for i in range(k):
        piv = max(range(i, k), key=lambda r: abs(a[r][i]))
        a[i], a[piv] = a[piv], a[i]
        for r in range(i + 1, k):
            f = a[r][i] / a[i][i]
            for c in range(i, k + 1):
                a[r][c] -= f * a[i][c]
    beta = [0] * k
    for i in reversed(range(k)):
        beta[i] = (a[i][k] - sum(a[i][j] * beta[j] for j in range(i + 1, k))) / a[i][i]
    return cov[v][v] - sum(cov[v][p] * b for p, b in zip(ps, beta))


def gaussian_bic(cov, n_samples):
    """local(v, P) = -(N/2) log Var(v | P) - (|P|/2) log N, with a cache."""
    cache = {}
    half_log_n = 0.5 * math.log(n_samples)

    def local(v, ps):
        key = (v, ps)
        if key not in cache:
            var = conditional_variance(cov, v, sorted(ps, key=str))
            cache[key] = -0.5 * n_samples * math.log(var) - half_log_n * len(ps)
        return cache[key]

    return local


def sem_covariance(nodes, weights):
    """Exact covariance of X_v = sum_p w[p, v] X_p + e_v with unit noise
    variances; weights maps (p, v) to a Fraction and nodes is a topological order."""
    cov = {u: {} for u in nodes}
    for i, v in enumerate(nodes):
        pas = [(p, w) for (p, c), w in weights.items() if c == v]
        for u in nodes[:i]:
            cov[u][v] = cov[v][u] = sum((w * cov[p][u] for p, w in pas), Fraction(0))
        cov[v][v] = Fraction(1) + sum((w1 * w2 * cov[p1][p2] for p1, w1 in pas for p2, w2 in pas), Fraction(0))
    return cov


def sample_covariance(rows, nodes):
    n = len(rows)
    means = {v: sum(r[v] for r in rows) / n for v in nodes}
    return {u: {v: sum((r[u] - means[u]) * (r[v] - means[v]) for r in rows) / n for v in nodes} for u in nodes}


def sample_sem(nodes, weights, n, rng):
    rows = []
    for _ in range(n):
        x = {}
        for v in nodes:
            x[v] = rng.gauss(0.0, 1.0) + sum(float(w) * x[p] for (p, c), w in weights.items() if c == v)
        rows.append(x)
    return rows


if __name__ == "__main__":
    nodes = ["A", "B", "C", "D", "E"]
    w = {("A", "B"): Fraction(4, 5), ("A", "C"): Fraction(7, 10), ("B", "D"): Fraction(3, 5),
         ("C", "D"): Fraction(3, 5), ("D", "E"): Fraction(9, 10)}
    res = ges(nodes, gaussian_bic(sem_covariance(nodes, w), 1000))
    for st in res.steps:
        print(st[0], st[1], st[2], sorted(st[3]), round(st[4], 2))
    print(res.cpdag.edges(), res.evaluations)
