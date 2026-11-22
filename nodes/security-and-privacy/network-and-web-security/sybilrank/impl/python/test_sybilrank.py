# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sybilrank/. The authors are listed in prov/S4HXC8.jsonl.

import random
from fractions import Fraction

from sybilrank import default_iterations, propagate, rank, sybilrank

# The graph of Figure 4 of Cao et al.: A..E are honest, F..I are Sybils, E-F is the attack edge.
EDGES = ["AB", "AC", "BC", "BE", "CD", "DE", "EF", "FG", "FH", "GH", "GI", "HI"]


def build(edges) -> dict:
    adj: dict = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    return {v: sorted(n) for v, n in adj.items()}


def oracle(adj: dict, seeds: list, total: Fraction, w: int) -> dict:
    """Exact trust by w products with the dense transition matrix, in fractions."""
    nodes = sorted(adj, key=str)
    idx = {v: i for i, v in enumerate(nodes)}
    n = len(nodes)
    p = [[Fraction(0)] * n for _ in range(n)]  # p[i][j]: from i to j
    for u in nodes:
        for v in adj[u]:
            p[idx[u]][idx[v]] += Fraction(1, len(adj[u]))
    x = [total / len(seeds) if v in seeds else Fraction(0) for v in nodes]
    for _ in range(w):
        x = [sum(x[i] * p[i][j] for i in range(n)) for j in range(n)]
    return {v: x[idx[v]] for v in nodes}


def test_example() -> None:
    adj = build(EDGES)
    t = propagate(adj, ["C", "D"], 648.0, 4)
    want = {"A": 92, "B": 144, "C": 131, "D": 93, "E": 90, "F": 54, "G": 16, "H": 16, "I": 12}
    for v, x in want.items():
        assert abs(t[v] - x) < 1e-9
    assert oracle(adj, ["C", "D"], Fraction(648), 4) == {v: Fraction(x) for v, x in want.items()}
    order = rank(adj, t)
    assert order[:4] == ["G", "H", "I", "F"]  # every Sybil is below every honest node
    assert set(order[4:]) == set("ABCDE")
    # After many iterations the trust is proportional to degree: 27 per edge end.
    t = propagate(adj, ["C", "D"], 648.0, 200)
    for v in adj:
        assert abs(t[v] - 27 * len(adj[v])) < 1e-6


def test_edges() -> None:
    adj = build(["AB"])
    assert propagate(adj, ["A"], 1.0, 0) == {"A": 1.0, "B": 0.0}
    assert propagate(adj, ["A"], 1.0, 1) == {"A": 0.0, "B": 1.0}
    assert rank(adj, {"A": 0.5, "B": 0.5}) == ["A", "B"]  # ties by name
    assert default_iterations(1) == 1 and default_iterations(2) == 1
    assert default_iterations(9) == 4 and default_iterations(1024) == 10
    assert sybilrank(build(EDGES), ["C", "D"])[:4] == ["G", "H", "I", "F"]


def random_graph(rng: random.Random, n: int) -> dict:
    adj = {v: set() for v in range(n)}
    for v in range(1, n):
        u = rng.randrange(v)
        adj[u].add(v)
        adj[v].add(u)
    for _ in range(rng.randrange(0, 2 * n)):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            adj[a].add(b)
            adj[b].add(a)
    return {v: sorted(s) for v, s in adj.items()}


def test_random_against_oracle() -> None:
    """Floating power iteration agrees with the exact matrix oracle and keeps the total."""
    rng = random.Random(2012)
    for _ in range(500):
        n = rng.randrange(2, 13)
        adj = random_graph(rng, n)
        seeds = rng.sample(range(n), rng.randrange(1, n + 1))
        w = rng.randrange(0, 6)
        got = propagate(adj, seeds, 1.0, w)
        want = oracle(adj, seeds, Fraction(1), w)
        assert sum(want.values()) == 1
        for v in adj:
            assert abs(got[v] - float(want[v])) < 1e-12


def two_regions(rng: random.Random, nh: int, ns: int, g: int, extra: int) -> tuple[dict, set]:
    """An honest region and a Sybil region, each a random connected graph, joined by g attack edges."""
    adj = {v: set() for v in range(nh + ns)}

    def add(a: int, b: int) -> None:
        if a != b:
            adj[a].add(b)
            adj[b].add(a)

    for lo, size in ((0, nh), (nh, ns)):
        for v in range(1, size):
            add(lo + v, lo + rng.randrange(v))
        for _ in range(extra * size):
            add(lo + rng.randrange(size), lo + rng.randrange(size))
    attack = set()
    while len(attack) < g:
        e = (rng.randrange(nh), nh + rng.randrange(ns))
        attack.add(e)
        add(*e)
    return {v: sorted(s) for v, s in adj.items()}, attack


def test_escape_bound() -> None:
    """Trust in the Sybil region after w steps is at most the sum, over steps, of the flow on attack edges."""
    rng = random.Random(197)
    for _ in range(200):
        nh, ns = rng.randrange(5, 31), rng.randrange(2, 31)
        adj, attack = two_regions(rng, nh, ns, rng.randrange(1, 4), 2)
        seeds = rng.sample(range(nh), rng.randrange(1, 4))
        w = default_iterations(nh + ns)
        flow = 0.0
        for i in range(w):
            t = propagate(adj, seeds, 1.0, i)
            flow += sum(t[u] / len(adj[u]) for u, _ in attack)
        t = propagate(adj, seeds, 1.0, w)
        assert sum(t[v] for v in range(nh, nh + ns)) <= flow + 1e-12


def test_ranking_measurement() -> None:
    """With few attack edges most Sybils fall in the bottom of the ranking (a measurement, not a bound)."""
    rng = random.Random(210)
    caught = total = 0
    for _ in range(40):
        nh, ns = 30, 30
        adj, _ = two_regions(rng, nh, ns, 2, 3)
        order = sybilrank(adj, rng.sample(range(nh), 3))
        caught += sum(1 for v in order[:ns] if v >= nh)
        total += ns
    assert caught / total > 0.8
