# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/potts-model/. The authors are listed in prov/H16W80.jsonl.

"""The q-state Potts model on a graph: exact partition function by
enumeration, the random-cluster (Fortuin and Kasteleyn) sum, and a
single-site Gibbs sampler.

A configuration x gives each vertex a state in 0 .. q - 1. With coupling
K = beta * J, its weight is exp(K * a(x)), where a(x) is the number of edges
whose ends have the same state.
"""

import itertools
import math
import random


def grid(rows: int, cols: int) -> tuple[int, list[tuple[int, int]]]:
    edges = []
    for r in range(rows):
        for c in range(cols):
            v = r * cols + c
            if c + 1 < cols:
                edges.append((v, v + 1))
            if r + 1 < rows:
                edges.append((v, v + cols))
    return rows * cols, edges


def agreements(x, edges) -> int:
    return sum(1 for u, v in edges if x[u] == x[v])


def agreement_counts(n: int, edges, q: int) -> list[int]:
    """c[k] = the number of configurations with exactly k agreeing edges."""
    c = [0] * (len(edges) + 1)
    for x in itertools.product(range(q), repeat=n):
        c[agreements(x, edges)] += 1
    return c


def partition_function(n: int, edges, q: int, w):
    """Z = sum over configurations of w ** a(x), with w = exp(K). Exact if w is exact."""
    return sum(ck * w ** k for k, ck in enumerate(agreement_counts(n, edges, q)))


def random_cluster_sum(n: int, edges, q: int, w):
    """Z = sum over edge subsets A of q ** k(A) * (w - 1) ** |A| (Fortuin and Kasteleyn)."""
    total = 0
    for mask in range(1 << len(edges)):
        parent = list(range(n))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a
        size, comps = 0, n
        for i, (u, v) in enumerate(edges):
            if mask >> i & 1:
                size += 1
                ru, rv = find(u), find(v)
                if ru != rv:
                    parent[ru] = rv
                    comps -= 1
        total += q ** comps * (w - 1) ** size
    return total


def exact_agreement_distribution(n: int, edges, q: int, K: float) -> list[float]:
    """P(a(X) = k) under the Potts distribution, by enumeration."""
    c = agreement_counts(n, edges, q)
    wts = [ck * math.exp(K * k) for k, ck in enumerate(c)]
    z = sum(wts)
    return [t / z for t in wts]


def gibbs_sampler(n: int, edges, q: int, K: float, sweeps: int, rng: random.Random, burn_in: int = 100):
    """Systematic-scan Gibbs sampling. Yields the configuration after each sweep."""
    nbr = [[] for _ in range(n)]
    for u, v in edges:
        nbr[u].append(v)
        nbr[v].append(u)
    x = [rng.randrange(q) for _ in range(n)]
    for t in range(burn_in + sweeps):
        for v in range(n):
            # P(x_v = s | rest) is proportional to exp(K * number of neighbours in state s)
            same = [0] * q
            for u in nbr[v]:
                same[x[u]] += 1
            wts = [math.exp(K * s) for s in same]
            r = rng.random() * sum(wts)
            s = 0
            while r >= wts[s] and s < q - 1:
                r -= wts[s]
                s += 1
            x[v] = s
        if t >= burn_in:
            yield tuple(x)
