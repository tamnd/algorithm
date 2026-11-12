# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kleinberg-impossibility-theorem/. The authors are listed in prov/TFYKXG.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from kleinberg_impossibility_theorem import (
    all_partitions,
    check_consistency,
    check_richness,
    check_scale_invariance,
    grid_distances,
    is_transformation,
    refines,
    single_linkage_alpha,
    single_linkage_k,
    single_linkage_r,
)

N = 3
GRID = grid_distances(N, range(1, 7))  # all 216 distance functions with values 1..6
SCALES = [Fraction(1, 3), Fraction(1, 2), Fraction(2), Fraction(3), Fraction(7, 3)]


def sl_k(n, d):
    return single_linkage_k(n, d, 2)


def sl_r(n, d):
    return single_linkage_r(n, d, 3)


def sl_alpha(n, d):
    return single_linkage_alpha(n, d, Fraction(1, 2))


def P(*blocks):
    return frozenset(frozenset(b) for b in blocks)


def is_antichain(parts) -> bool:
    return not any(p != q and refines(p, q) for p in parts for q in parts)


def test_grid_and_partitions() -> None:
    assert len(GRID) == 216
    assert len(all_partitions(3)) == 5 and len(all_partitions(4)) == 15


def test_k_cluster_condition() -> None:
    assert check_scale_invariance(sl_k, N, GRID, SCALES) == []
    assert check_consistency(sl_k, N, GRID) == []
    # Not rich: only the three partitions with two blocks occur.
    assert check_richness(sl_k, N, GRID) == {P([0, 1, 2]), P([0], [1], [2])}
    rng = {sl_k(N, d) for d in GRID}
    assert is_antichain(rng)


def test_distance_r_condition() -> None:
    assert check_consistency(sl_r, N, GRID) == []
    assert check_richness(sl_r, N, GRID) == set()
    # Not scale invariant: all distances 2 give one cluster; doubled, they give singletons.
    d = {(0, 1): 2, (0, 2): 2, (1, 2): 2}
    assert sl_r(N, d) == P([0, 1, 2])
    assert sl_r(N, {e: 2 * v for e, v in d.items()}) == P([0], [1], [2])
    assert check_scale_invariance(sl_r, N, GRID, SCALES) != []


def test_scale_alpha_condition() -> None:
    assert check_scale_invariance(sl_alpha, N, GRID, SCALES) == []
    assert check_richness(sl_alpha, N, GRID) == set()
    # Not consistent: stretch one distance across the two clusters, and the threshold grows.
    d = {(0, 1): 2, (0, 2): 3, (1, 2): 4}
    p = sl_alpha(N, d)
    assert p == P([0, 1], [2])
    d2 = {(0, 1): 2, (0, 2): 3, (1, 2): 6}
    assert is_transformation(p, d, d2)
    assert sl_alpha(N, d2) == P([0, 1, 2])
    assert check_consistency(sl_alpha, N, GRID) != []


def test_scale_alpha_needs_three_points() -> None:
    # With n = 2 and alpha < 1 the single cluster never occurs, so richness fails.
    grid2 = grid_distances(2, range(1, 7))
    assert check_richness(sl_alpha, 2, grid2) == {P([0, 1])}


def test_consistency_on_random_larger_inputs() -> None:
    rng = random.Random(5)
    n = 6
    pairs = list(combinations(range(n), 2))
    for _ in range(300):
        d = {e: rng.randrange(1, 10) for e in pairs}
        for f in (lambda m, x: single_linkage_k(m, x, 3), lambda m, x: single_linkage_r(m, x, 4)):
            p = f(n, d)
            d2 = {}
            for e in pairs:
                inside = any(e[0] in b and e[1] in b for b in p)
                d2[e] = rng.randrange(1, d[e] + 1) if inside else d[e] + rng.randrange(0, 5)
            assert is_transformation(p, d, d2)
            assert f(n, d2) == p
