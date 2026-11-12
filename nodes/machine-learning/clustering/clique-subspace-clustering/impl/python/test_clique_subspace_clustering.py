# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clique-subspace-clustering/. The authors are listed in prov/M7PPXT.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from clique_subspace_clustering import (
    adjacent,
    clique,
    clusters_in_subspace,
    count_units,
    dense_units,
    dense_units_brute_force,
    describe,
    grid_cells,
    join_and_prune,
    maximal_region,
    minimal_cover,
    points_in_cluster,
    region_units,
)


def random_cells(rng, n, d, xi):
    # a few planted boxes in random subspaces, plus uniform noise
    cells = []
    for _ in range(rng.randint(1, 3)):
        dims = rng.sample(range(d), rng.randint(1, d))
        center = {a: rng.randrange(xi) for a in dims}
        for _ in range(rng.randint(n // 4, n // 2)):
            cells.append(tuple(
                min(xi - 1, max(0, center[a] + rng.choice((0, 0, 1)))) if a in center else rng.randrange(xi)
                for a in range(d)))
    while len(cells) < n:
        cells.append(tuple(rng.randrange(xi) for _ in range(d)))
    return cells


def test_bottom_up_dense_units_equal_brute_force_over_all_subspaces():
    rng = random.Random(1)
    for _ in range(60):
        d = rng.randint(1, 6)
        xi = rng.randint(1, 5)
        cells = random_cells(rng, rng.randint(5, 60), d, xi)
        tau = Fraction(rng.randint(0, 30), 100)
        levels = dense_units(cells, tau)
        found = set().union(*levels) if levels else set()
        assert found == dense_units_brute_force(cells, tau)
        for k, level in enumerate(levels, 1):
            assert all(len(u) == k for u in level)


def test_downward_closure():
    rng = random.Random(2)
    for _ in range(40):
        d = rng.randint(2, 6)
        cells = random_cells(rng, rng.randint(10, 60), d, rng.randint(2, 5))
        tau = Fraction(rng.randint(1, 25), 100)
        found = set().union(*dense_units(cells, tau) or [set()])
        for u in found:
            for k in range(1, len(u)):
                for sub in combinations(u, k):
                    assert sub in found
        # and the count of a projection is at least the count of the unit
        counts = count_units(cells, found)
        for u in found:
            for j in range(len(u)):
                if len(u) > 1:
                    assert counts[u[:j] + u[j + 1:]] >= counts[u]


def test_candidates_are_exactly_the_units_with_all_projections_dense():
    rng = random.Random(3)
    for _ in range(30):
        d = rng.randint(2, 5)
        xi = rng.randint(2, 4)
        cells = random_cells(rng, 40, d, xi)
        levels = dense_units(cells, Fraction(1, 10))
        for k in range(1, len(levels)):
            prev = levels[k - 1]
            expected = set()
            for dims in combinations(range(d), k + 1):
                units = [()]
                for a in dims:
                    units = [u + ((a, x),) for u in units for x in range(xi)]
                for u in units:
                    if all(u[:j] + u[j + 1:] in prev for j in range(k + 1)):
                        expected.add(u)
            assert join_and_prune(prev) == expected


def test_clusters_are_the_connected_components():
    rng = random.Random(4)
    for _ in range(40):
        k = rng.randint(1, 3)
        dims = tuple(sorted(rng.sample(range(5), k)))
        units = {tuple((a, rng.randrange(4)) for a in dims) for _ in range(rng.randint(1, 20))}
        comps = clusters_in_subspace(units)
        assert sorted(u for c in comps for u in c) == sorted(units)
        label = {u: i for i, c in enumerate(comps) for u in c}
        # union-find over all adjacent pairs gives the same classes
        parent = {u: u for u in units}

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        for u, v in combinations(sorted(units), 2):
            if adjacent(u, v):
                parent[find(u)] = find(v)
        for u, v in combinations(sorted(units), 2):
            assert (find(u) == find(v)) == (label[u] == label[v])


def test_cover_is_exact_maximal_and_irredundant():
    rng = random.Random(5)
    for _ in range(60):
        k = rng.randint(1, 3)
        dims = tuple(range(k))
        units = {tuple((a, rng.randrange(4)) for a in dims) for _ in range(rng.randint(1, 25))}
        for comp in clusters_in_subspace(units):
            cl = set(comp)
            cover = minimal_cover(cl)
            covered = set()
            for r in cover:
                ru = set(region_units(r))
                assert ru <= cl
                covered |= ru
                # maximal: no side can be pushed out by one interval
                for j, (a, lo, hi) in enumerate(r):
                    for grown in ((a, lo - 1, hi), (a, lo, hi + 1)):
                        g = r[:j] + (grown,) + r[j + 1:]
                        assert not set(region_units(g)) <= cl
                # irredundant: each region covers a unit that no other region covers
                others = set()
                for s in cover:
                    if s != r:
                        others |= set(region_units(s))
                assert not ru <= others
            assert covered == cl


def test_staircase_cover_drops_a_redundant_region():
    cl = {((0, 0), (1, 0)), ((0, 0), (1, 1)), ((0, 1), (1, 1)), ((0, 1), (1, 2))}
    assert maximal_region(((0, 0), (1, 0)), cl) == ((0, 0, 0), (1, 0, 1))
    assert maximal_region(((0, 1), (1, 1)), cl) == ((0, 0, 1), (1, 1, 1))
    assert minimal_cover(cl) == [((0, 0, 0), (1, 0, 1)), ((0, 1, 1), (1, 1, 2))]


def test_worked_example():
    pts = [
        (0.5, 0.5, 0.5), (1.0, 1.5, 2.5), (1.5, 1.0, 4.5), (0.5, 1.5, 6.5), (1.5, 0.5, 1.5),
        (2.5, 0.5, 3.5), (3.0, 1.5, 5.5), (3.5, 1.0, 7.5), (2.5, 1.5, 0.5), (3.5, 0.5, 2.5),
        (0.5, 4.5, 6.5), (2.5, 5.5, 7.0), (4.5, 4.5, 6.5), (5.5, 5.0, 7.5), (6.5, 4.5, 6.5), (7.5, 5.5, 7.5),
        (5.0, 2.5, 1.0), (7.0, 7.5, 2.5), (5.5, 6.5, 4.5), (6.5, 3.0, 0.5),
    ]
    bounds = [(0, 8)] * 3
    tau = Fraction(1, 5)
    cells = grid_cells(pts, 4, bounds)
    levels = dense_units(cells, tau)
    assert [len(level) for level in levels] == [6, 3]
    assert len(join_and_prune(levels[0])) == 12 and join_and_prune(levels[1]) == set()
    assert levels[1] == {((0, 0), (1, 0)), ((0, 1), (1, 0)), ((1, 2), (2, 3))}
    result = {(dims, tuple(map(tuple, cover))) for dims, _, cover in clique(pts, 4, tau, bounds)}
    assert ((0, 1), (((0, 0, 1), (1, 0, 0)),)) in result
    assert ((1, 2), (((1, 2, 2), (2, 3, 3)),)) in result
    assert len(result) == 7
    assert describe(((0, 0, 1), (1, 0, 0)), 4, bounds) == [(0, 0, 4), (1, 0, 2)]
    a = [c for dims, c, _ in clique(pts, 4, tau, bounds) if dims == (0, 1)][0]
    assert points_in_cluster(cells, a) == list(range(10))


def test_grid_cells_and_edge_cases():
    assert grid_cells([(0,), (5,), (9,), (10,)], 5, [(0, 10)]) == [(0,), (2,), (4,), (4,)]
    assert grid_cells([(3, 1), (3, 2)], 4) == [(0, 0), (0, 3)]
    assert dense_units([(0,)] * 3, Fraction(0)) == [{((0, 0),)}]
    try:
        clique([(0.0,)], 2, 1)
        assert False
    except ValueError:
        pass
