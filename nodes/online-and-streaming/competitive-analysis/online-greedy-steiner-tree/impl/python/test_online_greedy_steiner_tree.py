# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-greedy-steiner-tree/. The authors are listed in prov/HET07A.jsonl.

import random
from fractions import Fraction

from online_greedy_steiner_tree import OnlineGreedySteiner, online_greedy_steiner_tree


def add_edge(g, u, v, w):
    g.setdefault(u, {})[v] = w
    g.setdefault(v, {})[u] = w


def all_pairs(g):
    vs = list(g)
    inf = float("inf")
    d = {u: {v: (0 if u == v else g[u].get(v, inf)) for v in vs} for u in vs}
    for x in vs:
        for u in vs:
            for v in vs:
                if d[u][x] + d[x][v] < d[u][v]:
                    d[u][v] = d[u][x] + d[x][v]
    return d


def steiner_opt(g, terminals):
    """Exact Steiner tree cost by the Dreyfus-Wagner dynamic program."""
    ts = list(dict.fromkeys(terminals))
    if len(ts) <= 1:
        return 0
    d = all_pairs(g)
    vs = list(g)
    full = (1 << len(ts)) - 1
    dp = [None] * (full + 1)
    for i, t in enumerate(ts):
        dp[1 << i] = {v: d[t][v] for v in vs}
    for mask in range(1, full + 1):
        if dp[mask] is not None:
            continue
        best = {}
        for v in vs:
            b = float("inf")
            sub = (mask - 1) & mask
            while sub:
                if sub < mask ^ sub:
                    b = min(b, dp[sub][v] + dp[mask ^ sub][v])
                sub = (sub - 1) & mask
            best[v] = b
        dp[mask] = {v: min(best[u] + d[u][v] for u in vs) for v in vs}
    return min(dp[full].values())


def random_graph(rng, n):
    g = {v: {} for v in range(n)}
    for v in range(1, n):
        add_edge(g, v, rng.randrange(v), rng.randint(1, 9))
    for _ in range(rng.randint(0, n)):
        u, v = rng.sample(range(n), 2)
        add_edge(g, u, v, rng.randint(1, 9))
    return g


def harmonic(k):
    return sum(Fraction(1, i) for i in range(1, k + 1))


def is_tree_spanning(edges, terminals, g):
    vs = set(terminals)
    for u, v in edges:
        vs.add(u)
        vs.add(v)
    if len(edges) != len(vs) - 1:
        return False
    parent = {v: v for v in vs}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        if v not in g[u]:
            return False
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return len({find(v) for v in vs}) == 1


def cycle_with_center():
    g = {}
    ring = ["t1", "t2", "t3", "t4"]
    for i in range(4):
        add_edge(g, ring[i], ring[(i + 1) % 4], 3)
        add_edge(g, ring[i], "s", 2)
    return g


def test_example() -> None:
    g = cycle_with_center()
    cost, edges, steps = online_greedy_steiner_tree(g, ["t1", "t2", "t3", "t4"])
    assert (cost, steps) == (9, [0, 3, 3, 3])
    cost, edges, steps = online_greedy_steiner_tree(g, ["t1", "t3", "t2", "t4"])
    assert (cost, steps) == (8, [0, 4, 2, 2])
    assert steiner_opt(g, ["t1", "t2", "t3", "t4"]) == 8


def test_bound_against_exact_optimum() -> None:
    rng = random.Random(1991)
    for _ in range(300):
        n = rng.randint(2, 8)
        g = random_graph(rng, n)
        k = rng.randint(1, min(n, 5))
        terms = rng.sample(range(n), k)
        if rng.random() < 0.3:
            terms.append(rng.choice(terms))
        cost, edges, steps = online_greedy_steiner_tree(g, terms)
        opt = steiner_opt(g, terms)
        assert cost == sum(steps) == sum(g[u][v] for u, v in edges)
        assert is_tree_spanning(edges, terms, g)
        assert cost >= opt
        assert cost <= 2 * (harmonic(k) - 1) * opt
        ranked = sorted(steps, reverse=True)
        for j in range(1, k):
            assert ranked[j - 1] * (j + 1) <= 2 * opt


def build_diamond(L):
    """The diamond graph of level L with unit edges, and its segments.

    A segment of level j < L between u and v has two midpoints; each side is the
    pair of child segments through one midpoint.
    """
    g = {}
    segs = []
    counter = [2]

    def rec(u, v, j):
        idx = len(segs)
        segs.append(None)
        if j == L:
            add_edge(g, u, v, 1)
            segs[idx] = (u, v, None, {frozenset((u, v))})
            return idx
        a, b = counter[0], counter[0] + 1
        counter[0] += 2
        ch_a = [rec(u, a, j + 1), rec(a, v, j + 1)]
        ch_b = [rec(u, b, j + 1), rec(b, v, j + 1)]
        es = set().union(*(segs[c][3] for c in ch_a + ch_b))
        segs[idx] = (u, v, ((a, ch_a), (b, ch_b)), es)
        return idx

    root = rec(0, 1, 0)
    return g, segs, root


def run_diamond(L, choose):
    """The adversary of Imase and Waxman against the greedy rule.

    It requests the two ends, then for each level the midpoint of each current
    segment on the side chosen by choose(weight_a, weight_b).
    """
    g, segs, root = build_diamond(L)
    alg = OnlineGreedySteiner(g)
    terms = [0, 1]
    alg.add(0)
    alg.add(1)
    current = [root]
    for j in range(1, L + 1):
        nxt = []
        for s in current:
            _, _, sides, _ = segs[s]
            weights = []
            for _, children in sides:
                side_edges = set().union(*(segs[c][3] for c in children))
                weights.append(sum(1 for e in alg.edges if frozenset(e) in side_edges))
            pick = choose(weights[0], weights[1])
            m, children = sides[pick]
            inc = alg.add(m)
            terms.append(m)
            assert inc + weights[pick] >= 2 ** (L - j)
            nxt += children
        current = nxt
    return alg.cost, terms, g


def test_diamond_lower_bound() -> None:
    for L in range(1, 7):
        cost, terms, g = run_diamond(L, lambda a, b: 0 if a <= b else 1)
        opt = 2 ** L
        assert len(terms) == 2 ** L + 1
        assert len(g) == 2 + 2 * (4 ** L - 1) // 3
        assert 4 * cost >= L * opt
        assert 2 * cost == (2 + L) * opt
        if L <= 3:
            assert steiner_opt(g, terms) == opt


def test_diamond_random_sides() -> None:
    rng = random.Random(7)
    for L in (2, 4, 5):
        for _ in range(10):
            cost, _, _ = run_diamond(L, lambda a, b: rng.randrange(2))
            assert 4 * cost >= L * 2 ** L


def test_edges() -> None:
    g = cycle_with_center()
    assert online_greedy_steiner_tree(g, [])[0] == 0
    assert online_greedy_steiner_tree(g, ["t2"])[0] == 0
    assert online_greedy_steiner_tree(g, ["t2", "t2", "t2"])[0] == 0
    h = {0: {}, 1: {}}
    alg = OnlineGreedySteiner(h)
    alg.add(0)
    try:
        alg.add(1)
    except ValueError:
        pass
    else:
        raise AssertionError("an unreachable terminal must be rejected")
