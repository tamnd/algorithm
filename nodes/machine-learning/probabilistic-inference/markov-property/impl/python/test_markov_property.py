# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-property/. The authors are listed in prov/2VPWEJ.jsonl.

import itertools
import random
from fractions import Fraction

from markov_property import factorizes, global_, local, local_directed, pairwise


def graph(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def uniform_on(points):
    return {x: Fraction(1, len(points)) for x in points}


def gibbs(n, adj, rng, low=1):
    """A random distribution with one positive factor per edge and per vertex."""
    pot = {}
    for a in range(n):
        pot[a, a] = {xy: Fraction(rng.randint(low, 9)) for xy in itertools.product((0, 1), repeat=2)}
        for b in adj[a]:
            if a < b:
                pot[a, b] = {xy: Fraction(rng.randint(low, 9)) for xy in itertools.product((0, 1), repeat=2)}
    un = {}
    for x in itertools.product((0, 1), repeat=n):
        p = Fraction(1)
        for (a, b), t in pot.items():
            p *= t[x[a], x[b]]
        if p:
            un[x] = p
    z = sum(un.values())
    return {x: p / z for x, p in un.items()}


def test_pairwise_without_local_or_global():
    # X = Y = Z, a fair coin, on the graph with no edges.
    pj = uniform_on([(0, 0, 0), (1, 1, 1)])
    adj = graph(3, [])
    assert pairwise(pj, 3, adj)
    assert not local(pj, 3, adj)
    assert not global_(pj, 3, adj)


def test_local_without_global():
    # Path U - W - X - Y - Z with U, Z fair coins, W = U, Y = Z, X = W * Y.
    pts = [(u, u, u * z, z, z) for u in (0, 1) for z in (0, 1)]
    pj = uniform_on(pts)
    adj = graph(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
    assert pairwise(pj, 5, adj)
    assert local(pj, 5, adj)
    assert not global_(pj, 5, adj)


def test_all_three_hold_for_positive_factorizing_distributions():
    rng = random.Random(1996)
    for _ in range(40):
        n = rng.randint(2, 4)
        adj = graph(n, [e for e in itertools.combinations(range(n), 2) if rng.random() < 0.5])
        pj = gibbs(n, adj, rng)
        assert pairwise(pj, n, adj) and local(pj, n, adj) and global_(pj, n, adj)


def test_implications_hold_on_degenerate_distributions():
    rng = random.Random(3)
    seen = set()
    for _ in range(300):
        n = rng.randint(3, 4)
        adj = graph(n, [e for e in itertools.combinations(range(n), 2) if rng.random() < 0.4])
        pts = rng.sample(list(itertools.product((0, 1), repeat=n)), rng.randint(1, 4))
        pj = {x: Fraction(rng.randint(1, 3)) for x in pts}
        z = sum(pj.values())
        pj = {x: p / z for x, p in pj.items()}
        g, l, p = global_(pj, n, adj), local(pj, n, adj), pairwise(pj, n, adj)
        assert (not g or l) and (not l or p)
        seen.add((g, l, p))
    assert (False, False, True) in seen


def test_directed_local_property_iff_factorization():
    rng = random.Random(1990)
    for _ in range(150):
        n = rng.randint(2, 4)
        order = list(range(n))
        rng.shuffle(order)
        pairs = [(order[i], order[j]) for i in range(n) for j in range(i + 1, n)]
        g = [e for e in pairs if rng.random() < 0.5]
        # the distribution comes from a random sub-DAG of the same order, or not
        h = [e for e in pairs if rng.random() < 0.5]
        pa = [sorted(a for a, b in h if b == v) for v in range(n)]
        lo = rng.choice((0, 1))  # with lo = 0 some tables are deterministic
        cpt = [{k: Fraction(rng.randint(lo, 4), 4) for k in itertools.product((0, 1), repeat=len(pa[v]))} for v in range(n)]
        pj = {}
        for x in itertools.product((0, 1), repeat=n):
            p = Fraction(1)
            for v in range(n):
                q = cpt[v][tuple(x[u] for u in pa[v])]
                p *= q if x[v] else 1 - q
            if p:
                pj[x] = p
        assert local_directed(pj, n, g) == factorizes(pj, n, g)
        if set(h) <= set(g):
            assert factorizes(pj, n, g)
