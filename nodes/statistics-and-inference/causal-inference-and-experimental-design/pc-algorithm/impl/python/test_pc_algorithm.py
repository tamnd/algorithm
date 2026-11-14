# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pc-algorithm/. The authors are listed in prov/MTZ8ME.jsonl.

import itertools
import math
import random

from pc_algorithm import cpdag_edges, d_separated, dsep_oracle, gaussian_ci_test, pc

EXAMPLE = {"A": set(), "B": {"A"}, "C": {"A"}, "D": {"B", "C"}, "E": {"D"}}


def all_dags(n):
    """Every DAG on nodes 0..n-1, as parent dicts."""
    pairs = list(itertools.combinations(range(n), 2))
    out = []
    for choice in itertools.product((0, 1, 2), repeat=len(pairs)):
        parents = {v: set() for v in range(n)}
        for (u, v), c in zip(pairs, choice):
            if c == 1:
                parents[v].add(u)
            elif c == 2:
                parents[u].add(v)
        if is_acyclic(parents):
            out.append(parents)
    return out


def is_acyclic(parents):
    state = {}

    def visit(v):
        if state.get(v) == 1:
            return False
        if state.get(v) == 2:
            return True
        state[v] = 1
        ok = all(visit(p) for p in parents[v])
        state[v] = 2
        return ok

    return all(visit(v) for v in parents)


def edges(parents):
    return {(p, v) for v in parents for p in parents[v]}


def dsep_signature(parents):
    nodes = sorted(parents)
    sig = []
    for a, b in itertools.combinations(nodes, 2):
        rest = [v for v in nodes if v not in (a, b)]
        for k in range(len(rest) + 1):
            for s in itertools.combinations(rest, k):
                sig.append(d_separated(parents, {a}, {b}, set(s)))
    return tuple(sig)


def cpdag_from_class(dags):
    """Directed edges shared by all DAGs of the class; the other edges are undirected."""
    common = set.intersection(*(edges(d) for d in dags))
    skel = {frozenset(e) for e in edges(dags[0])}
    undirected = sorted(tuple(sorted(e)) for e in skel if not any(set(e) == {u, v} for u, v in common))
    return sorted(common), undirected


def v_structures(parents):
    out = set()
    for c in parents:
        for a, b in itertools.combinations(sorted(parents[c]), 2):
            if a not in parents[b] and b not in parents[a]:
                out.add((a, c, b))
    return out


def test_worked_example():
    res = pc(EXAMPLE, dsep_oracle(EXAMPLE))
    sep = {tuple(sorted(k)): sorted(v) for k, v in res.sepset.items()}
    assert sep == {("A", "E"): ["D"], ("B", "C"): ["A"], ("B", "E"): ["D"], ("C", "E"): ["D"], ("A", "D"): ["B", "C"]}
    directed, undirected = cpdag_edges(res.adj, res.arrows)
    assert directed == [("B", "D"), ("C", "D"), ("D", "E")]
    assert undirected == [("A", "B"), ("A", "C")]
    assert res.tests == 64


def check_all_dags(n, n_dags, n_classes):
    dags = all_dags(n)
    assert len(dags) == n_dags
    classes = {}
    for d in dags:
        classes.setdefault(dsep_signature(d), []).append(d)
    assert len(classes) == n_classes
    for members in classes.values():
        want = cpdag_from_class(members)
        for d in members:
            res = pc(d, dsep_oracle(d))
            assert cpdag_edges(res.adj, res.arrows) == want


def test_all_dags_on_three_nodes():
    check_all_dags(3, 25, 11)


def test_all_dags_on_four_nodes():
    check_all_dags(4, 543, 185)


def random_dag(rng, n, p):
    order = list(range(n))
    rng.shuffle(order)
    parents = {v: set() for v in range(n)}
    for i, j in itertools.combinations(range(n), 2):
        if rng.random() < p:
            parents[order[j]].add(order[i])
    return parents


def markov_class_by_orientation(parents):
    """All DAGs with the skeleton and v-structures of the DAG (Verma and Pearl)."""
    skel = sorted(tuple(sorted(e)) for e in edges(parents))
    vs = v_structures(parents)
    out = []
    for bits in itertools.product((0, 1), repeat=len(skel)):
        cand = {v: set() for v in parents}
        for (u, v), bit in zip(skel, bits):
            if bit:
                cand[v].add(u)
            else:
                cand[u].add(v)
        if is_acyclic(cand) and v_structures(cand) == vs:
            out.append(cand)
    return out


def test_random_dags_against_class_enumeration():
    rng = random.Random(20261114)
    checked = 0
    while checked < 25:
        g = random_dag(rng, rng.choice((5, 6, 7)), 0.35)
        if len(edges(g)) > 11:
            continue
        res = pc(g, dsep_oracle(g))
        assert cpdag_edges(res.adj, res.arrows) == cpdag_from_class(markov_class_by_orientation(g))
        checked += 1


def test_number_of_tests_bound():
    rng = random.Random(7)
    for _ in range(30):
        n = rng.choice((5, 6, 7, 8))
        g = random_dag(rng, n, 0.3)
        q = max(len(g[v]) + sum(v in g[w] for w in g) for v in g)
        res = pc(g, dsep_oracle(g))
        bound = n * (n - 1) * sum(math.comb(n - 2, k) for k in range(q + 1))
        assert res.tests <= bound


def test_relabelling_gives_same_class():
    rng = random.Random(11)
    for _ in range(20):
        g = random_dag(rng, 6, 0.4)
        perm = list(range(6))
        rng.shuffle(perm)
        h = {perm[v]: {perm[p] for p in g[v]} for v in g}
        a = pc(g, dsep_oracle(g))
        b = pc(h, dsep_oracle(h))
        da, ua = cpdag_edges(a.adj, a.arrows)
        db, ub = cpdag_edges(b.adj, b.arrows)
        assert sorted((perm[u], perm[v]) for u, v in da) == db
        assert sorted(tuple(sorted((perm[u], perm[v]))) for u, v in ua) == ub


def sample_example(seed, n, c_coef):
    # Linear Gaussian model on the example graph, nodes A..E = 0..4.
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        a = rng.gauss(0, 1)
        b = 0.8 * a + rng.gauss(0, 1)
        c = c_coef * a + rng.gauss(0, 1)
        d = 0.6 * b + 0.6 * c + rng.gauss(0, 1)
        e = 0.9 * d + rng.gauss(0, 1)
        rows.append([a, b, c, d, e])
    return rows


def test_gaussian_data_measured():
    # Measured, not proved: 48 of 50 seeds recover the CPDAG at n = 500 and at n = 2000.
    want = ([(1, 3), (2, 3), (3, 4)], [(0, 1), (0, 2)])
    hits = 0
    for seed in range(10):
        res = pc(range(5), gaussian_ci_test(sample_example(seed, 500, 0.7), alpha=0.01))
        hits += cpdag_edges(res.adj, res.arrows) == want
    assert hits >= 9


def test_near_unfaithful_example_fails():
    # With C = -0.7 A the two paths from A to D nearly cancel (Cov(A, D) = 0.06),
    # so the level-0 test removes A - D and the orientations go wrong.
    res = pc(range(5), gaussian_ci_test(sample_example(0, 500, -0.7), alpha=0.01))
    assert 3 not in res.adj[0]
    assert cpdag_edges(res.adj, res.arrows) != ([(1, 3), (2, 3), (3, 4)], [(0, 1), (0, 2)])
