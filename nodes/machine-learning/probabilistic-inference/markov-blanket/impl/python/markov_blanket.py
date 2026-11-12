# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-blanket/. The authors are listed in prov/7QYGND.jsonl.

"""Markov blankets in a DAG and in an undirected graph, an exact test of the
blanket property on a discrete joint distribution, and the Markov boundaries
found by trying every subset.

A joint distribution is a dict from value tuples to Fractions. Missing keys
have probability 0.
"""

import itertools
from fractions import Fraction

Joint = dict[tuple[int, ...], Fraction]


def blanket_dag(edges: list[tuple[int, int]], v: int) -> set[int]:
    """Parents, children, and the other parents of the children of v."""
    parents = {a for a, b in edges if b == v}
    children = {b for a, b in edges if a == v}
    coparents = {a for a, b in edges if b in children and a != v}
    return parents | children | coparents


def blanket_undirected(adj: list[set[int]], v: int) -> set[int]:
    """In a Markov random field the blanket is the set of neighbours."""
    return set(adj[v])


def joint_bn(n: int, edges: list[tuple[int, int]], cpt: list[dict[tuple[int, ...], Fraction]]) -> Joint:
    """Binary Bayesian network: cpt[v][values of sorted parents] = P(X_v = 1 | parents)."""
    parents = [sorted(a for a, b in edges if b == v) for v in range(n)]
    out = {}
    for x in itertools.product((0, 1), repeat=n):
        p = Fraction(1)
        for v in range(n):
            q = cpt[v][tuple(x[u] for u in parents[v])]
            p *= q if x[v] == 1 else 1 - q
        if p:
            out[x] = p
    return out


def marginal(pj: Joint, keep: list[int]) -> Joint:
    out: Joint = {}
    for x, p in pj.items():
        key = tuple(x[i] for i in keep)
        out[key] = out.get(key, Fraction(0)) + p
    return out


def is_blanket(pj: Joint, n: int, v: int, s: set[int]) -> bool:
    """True if X_v is independent of all other variables given X_s.

    The test is p(v, s, r) p(s) = p(v, s) p(s, r) for every value of
    (v, s, r), where r is the set of the remaining variables.
    """
    S = sorted(s)
    R = [u for u in range(n) if u != v and u not in s]
    full, pvs, psr, ps = marginal(pj, [v] + S + R), marginal(pj, [v] + S), marginal(pj, S + R), marginal(pj, S)
    for a in {k[:1] for k in pvs}:
        for sr in psr:
            b = sr[:len(S)]
            if full.get(a + sr, 0) * ps[b] != pvs.get(a + b, 0) * psr[sr]:
                return False
    return True


def markov_boundaries(pj: Joint, n: int, v: int) -> list[set[int]]:
    """All inclusion-minimal blankets of v, by trying every subset of the others."""
    others = [u for u in range(n) if u != v]
    good = [set(c) for r in range(len(others) + 1) for c in itertools.combinations(others, r)
            if is_blanket(pj, n, v, set(c))]
    return [s for s in good if not any(t < s for t in good)]
