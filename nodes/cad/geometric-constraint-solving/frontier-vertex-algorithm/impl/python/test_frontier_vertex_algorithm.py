# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frontier-vertex-algorithm/. The authors are listed in prov/HMKXPX.jsonl.

import random
from itertools import combinations

from frontier_vertex_algorithm import FrontierPlanner, frontier_dr_plan


def laman_rank(vertices, edges):
    """The generic rank in the plane by the Laman count: a greedy basis, each step checked by brute force
    over all vertex subsets of size k >= 2 (at most 2k - 3 edges each)."""
    vs = sorted(vertices)
    subsets = [set(X) for k in range(2, len(vs) + 1) for X in combinations(vs, k)]
    count = [0] * len(subsets)
    rank = 0
    for u, v in edges:
        if u not in vertices or v not in vertices:
            continue
        hit = [i for i, X in enumerate(subsets) if u in X and v in X]
        if all(count[i] < 2 * len(subsets[i]) - 3 for i in hit):
            rank += 1
            for i in hit:
                count[i] += 1
    return rank


def is_rigid(U, edges):
    return len(U) >= 2 and laman_rank(U, edges) == 2 * len(U) - 3


def rigid_components(n, edges):
    """The maximal vertex sets with at least two vertices that are generically rigid in the plane."""
    rigid = [frozenset(X) for k in range(2, n + 1) for X in combinations(range(n), k) if is_rigid(set(X), edges)]
    return {X for X in rigid if not any(X < Y for Y in rigid)}


def random_graph(rng, n, prob):
    return [e for e in combinations(range(n), 2) if rng.random() < prob]


def check_plan(n, edges):
    clusters, roots = frontier_dr_plan(n, edges)
    for c in clusters:
        U = c["vertices"]
        # every cluster is rigid by the Laman count, and its density is at least -3
        assert is_rigid(set(U), edges), (edges, sorted(U))
        assert c["density"] >= -3
        # every node is the union of its children and its leaves, and each child is a proper subset
        parts = [clusters[i]["vertices"] for i in c["children"]] + [frozenset([v]) for v in c["leaves"]]
        assert frozenset().union(*parts) == U
        assert all(P < U for P in parts)
        assert all(i < clusters.index(c) for i in c["children"])
    # the plan covers the graph: every edge lies in a root, and every vertex in exactly the roots listed
    for u, v in edges:
        assert any(u in R and v in R for R in roots)
    assert frozenset().union(*roots) == frozenset(range(n)) if n else True
    # each cluster is a child of at most one later cluster, so the roots are the clusters never used as children
    used = [i for c in clusters for i in c["children"]]
    assert len(used) == len(set(used))
    return clusters, roots


def test_random_graphs_clusters_rigid_and_plan_covers():
    rng = random.Random(1)
    for _ in range(40):
        n = rng.randint(2, 7)
        edges = random_graph(rng, n, rng.choice([0.4, 0.6, 0.8]))
        check_plan(n, edges)


def test_roots_are_the_rigid_components():
    rng = random.Random(2)
    for _ in range(25):
        n = rng.randint(3, 6)
        edges = random_graph(rng, n, rng.choice([0.5, 0.7]))
        _, roots = check_plan(n, edges)
        assert {R for R in roots if len(R) >= 2} == rigid_components(n, edges)


def test_prism():
    edges = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4), (2, 5)]
    clusters, roots = check_plan(6, edges)
    big = [c["vertices"] for c in clusters if len(c["vertices"]) >= 3]
    assert big == [frozenset({0, 1, 2}), frozenset({3, 4, 5}), frozenset(range(6))]
    assert roots == [frozenset(range(6))]
    last = clusters[-1]
    assert len(last["children"]) == 5 and last["density"] == -3


def test_shared_vertex_kept_by_frontier():
    """Vertex 0 lies in the triangle 012 and in the triangle 034; it stays a frontier vertex after 012 becomes a
    cluster, so the triangle 034 is still found, inside the rigid cluster 0345."""
    edges = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (0, 4), (1, 5)]
    clusters, roots = check_plan(6, edges)
    tri = next(c for c in clusters if c["vertices"] == frozenset({0, 1, 2}))
    assert 0 in tri["frontier"]
    sets = [c["vertices"] for c in clusters]
    assert frozenset({0, 3, 4, 5}) in sets
    assert roots == [frozenset(range(6))]
    assert clusters[-1]["density"] == -3


def test_hinged_bodies_are_two_roots():
    edges = [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4)]
    _, roots = check_plan(5, edges)
    assert sorted(map(sorted, roots)) == [[0, 1, 2], [2, 3, 4]]


def test_over_constrained_k4():
    edges = list(combinations(range(4), 2))
    clusters, roots = check_plan(4, edges)
    assert roots == [frozenset(range(4))]
    assert clusters[-1]["density"] == -2


def test_isolated_vertex_is_a_root():
    _, roots = check_plan(4, [(0, 1), (1, 2), (0, 2)])
    assert frozenset([3]) in roots and frozenset([0, 1, 2]) in roots


def test_frontier_vertices_are_reported():
    planner = FrontierPlanner(5, [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (2, 4)])
    clusters = planner.run()
    tri = next(c for c in clusters if c["vertices"] == frozenset({0, 1, 2}))
    assert tri["frontier"] == frozenset({2})
