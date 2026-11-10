# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/planar-steiner-tree-ptas/. The authors are listed in prov/H3DF34.jsonl.

import random
from itertools import combinations
from math import comb

from planar_steiner_tree_ptas import (boundary_cycle, connects, grid_graph, mortar_grid, non_crossing,
                                      portal_partitions, portals, scheme, spanning_tree, steiner_exact,
                                      tree_weight, two_approx)


def catalan(k):
    return comb(2 * k, k) // (k + 1)


def brute_steiner(g, terminals):
    """The least spanning tree of the induced subgraph, over all vertex sets that contain the terminals."""
    others = [v for v in g if v not in terminals]
    best = None
    for r in range(len(others) + 1):
        for extra in combinations(others, r):
            keep = set(terminals) | set(extra)
            edges = {(u, v) for u in keep for v in g[u] if v in keep and u < v}
            tree = spanning_tree(g, edges)
            if len(tree) == len(keep) - 1 and (best is None or tree_weight(g, tree) < best):
                best = tree_weight(g, tree)
    return best


def seeded_instance(seed):
    rng = random.Random(seed)
    g = grid_graph(9, 9, lambda u, v: rng.randint(1, 9))
    return g, sorted(rng.sample(sorted(g), 4))


def test_hand_example() -> None:
    g = grid_graph(9, 9, lambda u, v: 1)
    terminals = [(2, 3), (2, 5)]
    assert steiner_exact(g, terminals)[0] == 2  # the path through (2, 4) on the mortar line c = 4
    found = {}
    for spacing in (4, 2, 1):
        stats = {}
        value, edges = scheme(g, 9, 9, terminals, 4, spacing, stats)
        assert connects(edges, terminals)
        found[spacing] = (value, stats["plus"], stats["portals"])
    assert found == {4: (6, 6, 4), 2: (2, 2, 8), 1: (2, 2, 16)}
    assert stats["mortar"] == 45 and stats["bricks"] == 4 and stats["plus_vertices"] == 145


def test_seeded_instance() -> None:
    g, terminals = seeded_instance(13)
    assert terminals == [(0, 4), (2, 8), (4, 8), (6, 0)]
    assert steiner_exact(g, terminals)[0] == 61 and tree_weight(g, two_approx(g, terminals)) == 70
    assert [scheme(g, 9, 9, terminals, 4, s)[0] for s in (4, 2, 1)] == [66, 63, 61]


def test_exact_solver_against_brute_force() -> None:
    rng = random.Random(1971)
    for trial in range(16):
        rows, cols = (4, 4) if trial < 2 else rng.choice([(3, 3), (3, 4)])
        g = grid_graph(rows, cols, lambda u, v: rng.randint(1, 6))
        terminals = rng.sample(sorted(g), rng.randint(2, 4))
        value, edges = steiner_exact(g, terminals)
        assert value == brute_steiner(g, terminals) == tree_weight(g, edges)
        assert connects(edges, terminals)


def test_two_approximation() -> None:
    rng = random.Random(1981)
    for _ in range(15):
        g = grid_graph(7, 7, lambda u, v: rng.randint(1, 9))
        k = rng.randint(2, 6)
        terminals = rng.sample(sorted(g), k)
        opt = steiner_exact(g, terminals)[0]
        tree = two_approx(g, terminals)
        assert connects(tree, terminals) and opt <= tree_weight(g, tree) <= 2 * (1 - 1 / k) * opt


def test_portal_graph_bounds() -> None:
    for seed in range(8):
        g, terminals = seeded_instance(seed)
        opt = steiner_exact(g, terminals)[0]
        _, bricks = mortar_grid(9, 9, 4)
        rings = sum(tree_weight(g, list(zip(c, c[1:] + c[:1]))) for c in map(boundary_cycle, bricks))
        previous = None
        for spacing in (4, 2, 1):
            stats = {}
            value, edges = scheme(g, 9, 9, terminals, 4, spacing, stats)
            assert connects(edges, terminals)
            assert opt <= value <= stats["plus"] <= opt + 2 * rings  # the simple bound of Lemma 3
            assert previous is None or stats["plus"] <= previous  # nested portals can only help
            previous = stats["plus"]
        assert previous == opt  # every boundary vertex a portal: no loss


def test_brick_states() -> None:
    g = grid_graph(3, 3, lambda u, v: 1)
    brick = (0, 0, 2, 2)
    ring = boundary_cycle(brick)
    assert len(ring) == 8
    every = portal_partitions(g, brick, ring)
    assert all(non_crossing(p) for p in every)
    assert len(every) == 673 <= catalan(8)
    corners = portals(brick, 2)
    assert corners == [(0, 0), (0, 2), (2, 2), (2, 0)]
    assert len(portal_partitions(g, brick, corners)) == catalan(4)
