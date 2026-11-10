# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arora-euclidean-k-median-ptas/. The authors are listed in prov/PXSWAG.jsonl.

import random
from fractions import Fraction
from itertools import combinations
from math import comb, dist, sqrt

from arora_euclidean_k_median_ptas import (best_over_shifts, boundary_portals, child_counts, depth_count, detour,
                                           distance_profile, is_smooth, portal_cost, random_shift,
                                           smooth_profile_bound, snap_to_grid)


def brute_k_median(points, k, size):
    """The best k centres among all grid cells, by trying all sets."""
    cells = [(x, y) for x in range(size) for y in range(size)]
    best = (float("inf"), ())
    for cs in combinations(cells, k):
        best = min(best, (sum(min(dist(p, c) for c in cs) for p in points), cs))
    return best


def crossings_to_centres(points, centres):
    total = 0
    for p in points:
        c = min(centres, key=lambda c: dist(p, c))
        total += abs(p[0] - c[0]) + abs(p[1] - c[1])
    return total


def portal_mean(points, centres, size, m):
    return sum(portal_cost(points, centres, size, m, (a, b)) for a in range(size) for b in range(size)) / size ** 2


EXAMPLE = [(0, 0), (1, 0), (1, 1), (2, 1), (6, 6), (6, 7), (7, 5)]


def test_example() -> None:
    size = 8
    opt, centres = brute_k_median(EXAMPLE, 2, size)
    assert centres == ((1, 0), (6, 6)) and abs(opt - (3 + 2 * sqrt(2))) < 1e-9
    assert crossings_to_centres(EXAMPLE, centres) == 7
    assert detour((0, 0), (1, 0), size, 2, (3, 5)) == 1
    assert abs(portal_cost(EXAMPLE, centres, size, 2, (3, 5)) - (6 + 2 * sqrt(2))) < 1e-9
    means = [round(portal_mean(EXAMPLE, centres, size, m), 6) for m in (1, 2, 4, 8)]
    assert means == [14.328427, 9.203427, 7.078427, 6.203427]
    for m, mean in zip((1, 2, 4, 8), means):
        assert mean <= opt + Fraction(depth_count(size), m) * 7 + 1e-9


def test_structure_bound_for_several_eps() -> None:
    rng = random.Random(1998)
    size = 8
    depth = depth_count(size)
    for _ in range(6):
        pts = sorted({(rng.randrange(size), rng.randrange(size)) for _ in range(rng.randint(3, 7))})
        k = rng.randint(1, 2)
        opt, centres = brute_k_median(pts, k, size)
        for eps in (1.0, 0.5):
            m = 1
            while m < 2 * sqrt(2) * depth / eps:
                m *= 2
            mean = portal_mean(pts, centres, size, m)
            assert opt - 1e-9 <= mean <= opt + float(Fraction(depth, m)) * crossings_to_centres(pts, centres) + 1e-9
            assert mean <= (1 + eps / 2) * opt + 1e-9


def test_detour_is_at_most_one_gap_per_crossing() -> None:
    rng = random.Random(1999)
    for _ in range(300):
        size, m = rng.choice([(8, 1), (8, 4), (16, 2)])
        p, q = (rng.randrange(size), rng.randrange(size)), (rng.randrange(size), rng.randrange(size))
        shift = random_shift(size, rng)
        crossings = abs(p[0] - q[0]) + abs(p[1] - q[1])
        assert 0 <= detour(p, q, size, m, shift) <= crossings * Fraction(2 * size, 2 * m)
        assert detour(p, q, size, m, shift) == detour(q, p, size, m, shift)


def test_snap_split_and_best_shift() -> None:
    rng = random.Random(2001)
    for _ in range(50):
        pts = [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(rng.randint(1, 20))]
        gap = rng.choice([0.5, 1.0, 2.5])
        cells, size = snap_to_grid(pts, gap)
        x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
        for x, y in pts:
            cx, cy = int((x - x0) // gap), int((y - y0) // gap)
            assert (cx, cy) in cells
            assert dist((x, y), (x0 + (cx + 0.5) * gap, y0 + (cy + 0.5) * gap)) <= gap / sqrt(2) + 1e-9
        assert size & (size - 1) == 0 and all(c < size for p in cells for c in p)
    for j in range(6):
        ways = child_counts(j)
        assert len(ways) == comb(j + 3, 3) and all(sum(w) == j and min(w) >= 0 for w in ways)
    size = 8
    _, centres = brute_k_median(EXAMPLE, 2, size)
    best, shift = best_over_shifts(EXAMPLE, centres, size, 2)
    assert best <= portal_mean(EXAMPLE, centres, size, 2)
    assert best == portal_cost(EXAMPLE, centres, size, 2, shift)


def test_profiles_are_smooth_and_counted() -> None:
    rng = random.Random(2000)
    for side, m in ((4, 2), (8, 2), (8, 4)):
        seen = set()
        top = 0
        for _ in range(300):
            x0, y0 = rng.randrange(-4, 8), rng.randrange(-4, 8)
            centres = [(rng.randrange(-8, 16), rng.randrange(-8, 16)) for _ in range(rng.randint(1, 3))]
            portals = boundary_portals(x0, y0, side, m)
            assert len(portals) == 4 * m == len(set(portals))
            prof = distance_profile(portals, centres, Fraction(side, m))
            assert is_smooth(prof)
            # the state stores the profile relative to its least value
            low = min(prof)
            rel = tuple(v - low for v in prof)
            top = max(top, max(rel))
            seen.add(rel)
        assert len(seen) <= smooth_profile_bound(4 * m, top)
        assert top <= 2 * m  # two portals of one square are at most a diagonal apart, under 2m gaps
