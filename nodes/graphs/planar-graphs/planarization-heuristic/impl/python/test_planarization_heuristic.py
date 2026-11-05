# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/planarization-heuristic/. The authors are listed in prov/8EHK3E.jsonl.

import random
from itertools import combinations, permutations, product

from planarization_heuristic import faces, planar_embedding, planarize


def components(rot):
    seen = [False] * len(rot)
    comps = []
    for s in range(len(rot)):
        if seen[s]:
            continue
        seen[s] = True
        comp = [s]
        for x in comp:
            for y in rot[x]:
                if not seen[y]:
                    seen[y] = True
                    comp.append(y)
        comps.append(comp)
    return comps


def euler_ok(rot):
    """Every component with an edge satisfies V - E + F = 2 under the rotation."""
    for v, around in enumerate(rot):
        assert len(set(around)) == len(around), "repeated neighbour"
        for w in around:
            assert v != w and v in rot[w], "rotation not symmetric"
    fs = faces(rot)
    comp_of = {}
    comps = components(rot)
    for i, comp in enumerate(comps):
        for v in comp:
            comp_of[v] = i
    nf = [0] * len(comps)
    for walk in fs:
        nf[comp_of[walk[0][0]]] += 1
    for i, comp in enumerate(comps):
        e = sum(len(rot[v]) for v in comp) // 2
        if e and len(comp) - e + nf[i] != 2:
            return False
    return True


def brute_planar(n, edges):
    """Oracle: try every rotation system of every component."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    for comp in components(adj):
        if len(comp) < 3:
            continue
        choices = []
        for v in comp:
            first, rest = adj[v][0], adj[v][1:]
            choices.append([[first] + list(p) for p in permutations(rest)])
        e = sum(len(adj[v]) for v in comp) // 2
        found = False
        for pick in product(*choices):
            rot = [[] for _ in range(n)]
            for v, around in zip(comp, pick):
                rot[v] = around
            if len(comp) - e + len(faces(rot)) == 2:
                found = True
                break
        if not found:
            return False
    return True


def check(n, edges):
    r = planarize(n, edges)
    rot, chains, kept = r["rot"], r["chains"], r["kept"]
    assert len(rot) == n + r["crossings"]
    assert euler_ok(rot)
    # Every dummy has degree 4, and the two chains through it alternate.
    through = {}
    for i, chain in enumerate(chains):
        assert chain[0] == edges[i][0] and chain[-1] == edges[i][1]
        for t in range(1, len(chain) - 1):
            d = chain[t]
            assert d >= n
            through.setdefault(d, []).append((i, chain[t - 1], chain[t + 1]))
    assert sorted(through) == list(range(n, len(rot)))
    for d, uses in through.items():
        assert len(uses) == 2 and uses[0][0] != uses[1][0]
        assert len(rot[d]) == 4
        (_, a, b), (_, c, e) = uses
        assert {rot[d][0], rot[d][2]} in ({a, b}, {c, e})
        assert {rot[d][1], rot[d][3]} in ({a, b}, {c, e})
    # The chains are exactly the edges of the planarized graph.
    pieces = sorted(tuple(sorted(p)) for ch in chains for p in zip(ch, ch[1:]))
    graph = sorted((v, w) for v in range(len(rot)) for w in rot[v] if v < w)
    assert pieces == graph
    # Every removed edge is crossed at least once (kept edges may be crossed
    # by later insertions).
    for i, chain in enumerate(chains):
        if i not in kept:
            assert len(chain) >= 3
    # Lower bound from the edge bound of planar graphs.
    if n >= 3:
        assert r["crossings"] >= len(edges) - (3 * n - 6)
    return r


def test_small_cases():
    assert planarize(0, [])["crossings"] == 0
    r = check(1, [])
    assert r["rot"] == [[]] and r["crossings"] == 0
    tree = [(0, 1), (1, 2), (1, 3), (3, 4)]
    r = check(5, tree)
    assert r["crossings"] == 0 and r["kept"] == [0, 1, 2, 3]
    k4 = list(combinations(range(4), 2))
    r = check(4, k4)
    assert r["crossings"] == 0 and len(faces(r["rot"])) == 4


def test_kuratowski_graphs():
    k5 = list(combinations(range(5), 2))
    r = check(5, k5)
    assert r["crossings"] == 1 and len(r["kept"]) == 9
    assert r["chains"][-1] == [3, 5, 4]
    k33 = [(a, b) for a in range(3) for b in range(3, 6)]
    r = check(6, k33)
    assert r["crossings"] == 1 and len(r["kept"]) == 8
    k6 = list(combinations(range(6), 2))
    assert check(6, k6)["crossings"] == 3
    assert planar_embedding(5, k5) is None and planar_embedding(6, k33) is None


def test_invalid_input():
    for n, edges in [(2, [(0, 0)]), (2, [(0, 1), (1, 0)]), (2, [(0, 2)])]:
        try:
            planarize(n, edges)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")


def random_graph(rng, n, p):
    edges = [e for e in combinations(range(n), 2) if rng.random() < p]
    rng.shuffle(edges)
    return [(v, u) if rng.random() < 0.5 else (u, v) for u, v in edges]


def test_planarity_against_brute_force():
    rng = random.Random(1)
    for _ in range(600):
        n = rng.randint(1, 6)
        edges = random_graph(rng, n, rng.uniform(0.3, 1.0))
        if len(edges) > 11:
            edges = edges[:11]
        expect = brute_planar(n, edges)
        rot = planar_embedding(n, edges)
        assert (rot is not None) == expect
        if rot is not None:
            assert euler_ok(rot)


def test_maximal_subgraph_against_brute_force():
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randint(3, 6)
        edges = random_graph(rng, n, rng.uniform(0.5, 1.0))[:11]
        r = check(n, edges)
        sub = [edges[i] for i in r["kept"]]
        assert brute_planar(n, sub)
        for i in range(len(edges)):
            if i not in r["kept"]:
                assert not brute_planar(n, sub + [edges[i]])


def test_random_larger_graphs():
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randint(5, 18)
        edges = random_graph(rng, n, rng.uniform(0.1, 0.6))
        r = check(n, edges)
        sub = [edges[i] for i in r["kept"]]
        assert planar_embedding(n, sub) is not None
        for i in range(len(edges)):
            if i not in r["kept"]:
                assert planar_embedding(n, sub + [edges[i]]) is None
