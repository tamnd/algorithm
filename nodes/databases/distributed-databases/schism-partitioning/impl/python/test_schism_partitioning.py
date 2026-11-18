# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schism-partitioning/. The authors are listed in prov/RGG5F9.jsonl.

import random
from collections import Counter
from itertools import combinations

import pytest

from schism_partitioning import (balance_cap, brute_force_partition, build_graph, build_replicated_graph,
                                 coarsen, cut_weight, distributed_count, hash_placement, is_distributed, make_txn,
                                 partition, placement_from, predict, replication_placement, schism,
                                 touched, train_tree, tree_rules)

PAGE_DB = {i: {"id": i, "wid": 1 if i <= 3 else (2 if i <= 6 else 0)} for i in range(1, 9)}
PAGE_WORKLOAD = [
    make_txn([7], [1, 2]),
    make_txn([8], [2, 3]),
    make_txn([7], [4, 5]),
    make_txn([8], [5, 6]),
    make_txn([], [1, 3]),
    make_txn([], [4, 6]),
]


def ident(t):
    return t


def random_workload(rng, n, q, max_size=3, write_rate=0.4):
    out = []
    for _ in range(q):
        ts = rng.sample(range(n), rng.randint(1, min(max_size, n)))
        writes = [t for t in ts if rng.random() < write_rate]
        out.append(make_txn([t for t in ts if t not in writes], writes))
    return out


def local_by_definition(x, placement, k):
    for p in range(k):
        if all(p in placement[t] for t in touched(x)) and all(placement[t] == {p} for t in x[1]):
            return True
    return False


def test_page_example_without_replication():
    r = schism(PAGE_DB, PAGE_WORKLOAD, 2, replicate=False, h=ident)
    assert len(r.graph.weight) == 8 and len(r.graph.edges) == 14 and set(r.graph.edges.values()) == {1}
    assert cut_weight(r.graph, r.part) == 4 == brute_force_partition(r.graph, 2)[0]
    assert r.costs == {"hash": 4, "replication": 6, "tree": 2, "lookup": 2}
    assert r.choice == "tree"


def test_page_example_with_replication():
    r = schism(PAGE_DB, PAGE_WORKLOAD, 2, replicate=True, h=ident)
    g = r.graph
    assert len(g.weight) == 24 and len(g.edges) == 26 and sum(g.edges.values()) == 38
    assert cut_weight(g, r.part) == 0
    look = r.placements["lookup"]
    assert look[7] == look[8] == {0, 1}
    assert look[1] == look[2] == look[3] and look[4] == look[5] == look[6] and look[1] != look[4]
    assert r.costs == {"hash": 4, "replication": 6, "tree": 0, "lookup": 0}
    assert r.choice == "tree"
    rules = tree_rules(r.tree)
    assert len(rules) == 3
    for t in PAGE_DB:
        assert r.placements["tree"][t] == look[t]


def test_graph_matches_definition():
    rng = random.Random(1)
    for _ in range(30):
        w = random_workload(rng, 6, rng.randint(1, 8))
        g = build_graph(w)
        for u, v in combinations(range(6), 2):
            expect = sum(1 for x in w if {u, v} <= touched(x))
            assert g.edges.get(frozenset((u, v)), 0) == expect
        assert g.weight == dict(Counter(t for x in w for t in touched(x)))


def test_replicated_graph_matches_definition():
    rng = random.Random(2)
    for _ in range(30):
        w = random_workload(rng, 5, rng.randint(1, 7))
        g = build_replicated_graph(w)
        writes = Counter(t for x in w for t in x[1])
        star = sum(writes[t] * sum(1 for x in w if t in touched(x)) for t in range(5))
        clique = sum(len(touched(x)) * (len(touched(x)) - 1) // 2 for x in w)
        assert sum(g.edges.values()) == star + clique
        assert sum(g.weight.values()) == sum(len(touched(x)) for x in w)


@pytest.mark.parametrize("seed", range(40))
def test_is_distributed_matches_definition(seed):
    rng = random.Random(100 + seed)
    k = rng.randint(1, 3)
    placement = {t: frozenset(rng.sample(range(k), rng.randint(1, k))) for t in range(6)}
    for x in random_workload(rng, 6, 10):
        assert is_distributed(x, placement) == (not local_by_definition(x, placement, k))


@pytest.mark.parametrize("seed", range(40))
def test_distributed_count_at_most_cut_for_any_partition(seed):
    rng = random.Random(200 + seed)
    k = rng.randint(2, 3)
    w = random_workload(rng, 7, rng.randint(1, 10))
    for replicated in (False, True):
        g = build_replicated_graph(w) if replicated else build_graph(w)
        for _ in range(5):
            part = {v: rng.randrange(k) for v in g.weight}
            placement = placement_from(g, part, replicated)
            assert distributed_count(w, placement) <= cut_weight(g, part)


@pytest.mark.parametrize("seed", range(20))
def test_cut_equals_distributed_for_pairs(seed):
    rng = random.Random(300 + seed)
    w = random_workload(rng, 7, 12, max_size=2)
    g = build_graph(w)
    part = {v: rng.randrange(3) for v in g.weight}
    assert distributed_count(w, placement_from(g, part, False)) == cut_weight(g, part)


def _no_improving_step(g, part, k, cap):
    load = [0] * k
    for v, q in part.items():
        load[q] += g.weight[v]
    c = cut_weight(g, part)
    nodes = list(g.weight)
    for u in nodes:
        for q in range(k):
            if q != part[u] and load[q] + g.weight[u] <= cap:
                if cut_weight(g, {**part, u: q}) < c:
                    return False
    for u, v in combinations(nodes, 2):
        a, b = part[u], part[v]
        if a != b and load[a] - g.weight[u] + g.weight[v] <= cap and load[b] - g.weight[v] + g.weight[u] <= cap:
            if cut_weight(g, {**part, u: b, v: a}) < c:
                return False
    return True


@pytest.mark.parametrize("seed", range(30))
def test_partitioner_is_balanced_local_optimum_and_not_below_brute_force(seed):
    rng = random.Random(400 + seed)
    k = rng.randint(2, 3)
    w = random_workload(rng, 8, rng.randint(2, 9))
    g = build_graph(w)
    part = partition(g, k, eps=0.1, seed=seed)
    cap = balance_cap(g.weight, k, 0.1)
    load = Counter()
    for v, q in part.items():
        load[q] += g.weight[v]
    assert max(load.values()) <= cap
    assert set(part) == set(g.weight)
    assert _no_improving_step(g, part, k, cap)
    assert cut_weight(g, part) >= brute_force_partition(g, k, 0.1)[0]


@pytest.mark.parametrize("seed", range(15))
def test_coarsening_keeps_weights_and_cuts(seed):
    rng = random.Random(500 + seed)
    w = random_workload(rng, 9, 12)
    g = build_replicated_graph(w) if seed % 2 else build_graph(w)
    coarse, cmap = coarsen(g, rng, limit=4)
    assert sum(coarse.weight.values()) == sum(g.weight.values())
    assert max(Counter(cmap.values()).values()) <= 2
    for _ in range(5):
        cpart = {c: rng.randrange(3) for c in coarse.weight}
        assert cut_weight(coarse, cpart) == cut_weight(g, {v: cpart[cmap[v]] for v in g.weight})


def test_planted_warehouses_beat_hashing():
    rng = random.Random(7)
    k, per = 4, 6
    db = {(wid, j): {"wid": wid, "j": j} for wid in range(k) for j in range(per)}
    db.update({("item", j): {"wid": -1, "j": j} for j in range(3)})
    w = []
    for i in range(40):
        wid = i % k  # the same number of transactions per warehouse, so a perfect split is balanced
        ts = rng.sample(range(per), 2)
        w.append(make_txn([("item", rng.randrange(3))], [(wid, ts[0]), (wid, ts[1])]))
    r = schism(db, w, k, replicate=True, seed=3)
    assert r.costs["lookup"] == 0 == r.costs["tree"]
    assert r.costs["hash"] > 20
    assert r.costs["replication"] == 40
    plain = schism(db, w, k, replicate=False, seed=3)
    assert plain.costs["lookup"] > 0  # the shared items cannot sit with every warehouse without copies


def test_full_replication():
    rng = random.Random(8)
    reads = [make_txn(rng.sample(range(6), 3), []) for _ in range(10)]
    placement = replication_placement(range(6), 3)
    assert distributed_count(reads, placement) == 0
    assert is_distributed(make_txn([0], [1]), placement)
    assert not is_distributed(make_txn([0], [1]), replication_placement(range(6), 1))


def test_tree_fits_distinct_rows():
    rng = random.Random(9)
    for _ in range(20):
        n = rng.randint(1, 15)
        pts = rng.sample([(a, b) for a in range(5) for b in range(5)], n)
        rows = [{"a": a, "b": b} for a, b in pts]
        labels = [rng.randrange(3) for _ in rows]
        tree = train_tree(rows, labels)
        assert [predict(tree, r) for r in rows] == labels
        rules = tree_rules(tree)
        for r, lab in zip(rows, labels):
            hits = [l for path, l in rules if all((r[a] <= t) if op == "<=" else (r[a] > t) for a, op, t in path)]
            assert hits == [lab]


def test_tree_finds_ranges():
    rows = [{"x": x, "y": (7 * x) % 11} for x in range(30)]
    labels = [0 if x < 10 else (1 if x < 20 else 2) for x in range(30)]
    tree = train_tree(rows, labels, max_depth=2)
    assert [predict(tree, r) for r in rows] == labels
    assert {(path, lab) for path, lab in tree_rules(tree)} == {
        ((("x", "<=", 9),), 0), ((("x", ">", 9), ("x", "<=", 19)), 1), ((("x", ">", 9), ("x", ">", 19)), 2)}


def test_edge_cases():
    assert schism({1: {"a": 1}}, [], 2).costs == {"hash": 0, "replication": 0, "tree": 0, "lookup": 0}
    r = schism(PAGE_DB, PAGE_WORKLOAD, 1)
    assert set(r.costs.values()) == {0}
    with pytest.raises(KeyError):
        schism(PAGE_DB, [make_txn([99], [])], 2)
    with pytest.raises(ValueError):
        partition(build_graph(PAGE_WORKLOAD), 0)
    assert hash_placement([5], 2, ident) == {5: frozenset([1])}
