# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/region-growing/. The authors are listed in prov/M54ARC.jsonl.

import random
from fractions import Fraction

import pytest

from region_growing import BOUNDARY, neighbors, region_means, seeded_region_growing, srg_sorted_list

EXAMPLE = [
    [10, 12, 11, 40, 42, 41],
    [11, 30, 13, 39, 20, 40],
    [12, 11, 14, 38, 41, 43],
    [13, 12, 25, 37, 40, 42],
]
EXAMPLE_SEEDS = [[(0, 0)], [(5, 0)]]


def brute_force(img, seeds, connectivity):
    """The definition, step by step: recompute T, every delta and every mean."""
    h, w = len(img), len(img[0])
    lab = [[0] * w for _ in range(h)]
    for i, region in enumerate(seeds):
        for x, y in region:
            lab[y][x] = i + 1
    steps = []
    while True:
        means = region_means(img, lab, len(seeds))
        cands = []
        for y in range(h):
            for x in range(w):
                if lab[y][x]:
                    continue
                for r in {lab[ny][nx] for nx, ny in neighbors(x, y, w, h, connectivity)} - {0}:
                    cands.append((abs(img[y][x] - means[r]), y, x, r))
        if not cands:
            return lab, steps
        d, y, x, r = min(cands)
        lab[y][x] = r
        steps.append((x, y, r, d))


def random_case(rng, h, w, nseeds):
    img = [[rng.randint(0, 9) for _ in range(w)] for _ in range(h)]
    pixels = [(x, y) for y in range(h) for x in range(w)]
    rng.shuffle(pixels)
    seeds = [[p] for p in pixels[:nseeds]]
    if rng.random() < 0.3 and len(pixels) > nseeds:
        seeds[0].append(pixels[nseeds])  # a seed region with two pixels
    return img, seeds


def components_of_region(lab, r, connectivity):
    h, w = len(lab), len(lab[0])
    seen, comps = set(), []
    for y in range(h):
        for x in range(w):
            if lab[y][x] == r and (x, y) not in seen:
                comp, stack = {(x, y)}, [(x, y)]
                seen.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    for nx, ny in neighbors(cx, cy, w, h, connectivity):
                        if lab[ny][nx] == r and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            comp.add((nx, ny))
                            stack.append((nx, ny))
                comps.append(comp)
    return comps


def test_example():
    lab = seeded_region_growing(EXAMPLE, EXAMPLE_SEEDS, connectivity=4)
    assert lab == [
        [1, 1, 1, 2, 2, 2],
        [1, 1, 1, 2, 2, 2],
        [1, 1, 1, 2, 2, 2],
        [1, 1, 1, 2, 2, 2],
    ]
    means = region_means(EXAMPLE, lab, 2)
    assert means[1] == Fraction(174, 12) and means[2] == Fraction(463, 12)


@pytest.mark.parametrize("connectivity", [4, 8])
def test_against_step_by_step_definition(connectivity):
    rng = random.Random(1994 + connectivity)
    for _ in range(250):
        h, w = rng.randint(1, 5), rng.randint(1, 6)
        img, seeds = random_case(rng, h, w, rng.randint(1, min(3, h * w)))
        assert seeded_region_growing(img, seeds, connectivity) == brute_force(img, seeds, connectivity)[0]


@pytest.mark.parametrize("connectivity", [4, 8])
def test_invariants(connectivity):
    rng = random.Random(641 + connectivity)
    for _ in range(200):
        h, w = rng.randint(1, 6), rng.randint(1, 7)
        img, seeds = random_case(rng, h, w, rng.randint(1, min(4, h * w)))
        for lab in (seeded_region_growing(img, seeds, connectivity), srg_sorted_list(img, seeds, connectivity, flag_boundary=False)):
            # Every pixel is allocated: the grid is connected.
            assert all(v > 0 for row in lab for v in row)
            # Seeds keep their labels.
            for i, region in enumerate(seeds):
                assert all(lab[y][x] == i + 1 for x, y in region)
            # Every connected piece of a region meets that region's seeds.
            for i, region in enumerate(seeds):
                for comp in components_of_region(lab, i + 1, connectivity):
                    assert comp & set(region)


def test_example_order_and_outliers_last():
    _, steps = brute_force(EXAMPLE, EXAMPLE_SEEDS, 4)
    assert len(steps) == 22
    # The three outliers 25, 30 and 20 are the last pixels allocated.
    assert [(x, y, r) for x, y, r, _ in steps[-3:]] == [(2, 3, 1), (1, 1, 1), (4, 1, 2)]
    assert [d for _, _, _, d in steps[-3:]] == [Fraction(131, 10), Fraction(186, 11), Fraction(223, 11)]


def test_frozen_deltas_can_change_the_result():
    # The sorted list keeps delta = 18.5 for the pixel 10, computed against
    # the bright region, after the dark region has grown next to it.
    img = [[15, 4, 10, 13], [28, 26, 29, 28]]
    seeds = [[(0, 0)], [(3, 1)]]
    assert seeded_region_growing(img, seeds, 4) == [[1, 1, 1, 1], [2, 2, 2, 2]]
    assert srg_sorted_list(img, seeds, 4, flag_boundary=False) == [[1, 1, 1, 2], [2, 2, 2, 2]]


def test_sorted_list_boundary_flags():
    rng = random.Random(1997)
    for _ in range(200):
        h, w = rng.randint(2, 6), rng.randint(2, 7)
        img, seeds = random_case(rng, h, w, rng.randint(2, 4))
        seed_pixels = {tuple(p) for s in seeds for p in s}
        lab = srg_sorted_list(img, seeds, 8, flag_boundary=True)
        for y in range(h):
            for x in range(w):
                for nx, ny in neighbors(x, y, w, h, 8):
                    a, b = lab[y][x], lab[ny][nx]
                    # Two different regions never touch, except at given seeds.
                    if a > 0 and b > 0 and a != b:
                        assert (x, y) in seed_pixels and (nx, ny) in seed_pixels
                    # A pixel left out touches no region pixel.
                    if a == 0:
                        assert b <= 0


def test_sorted_list_matches_exact_on_clear_images():
    # Two flat regions with a clear step: both versions agree.
    img = [[5] * 4 + [50] * 4 for _ in range(5)]
    seeds = [[(0, 2)], [(7, 2)]]
    want = [[1] * 4 + [2] * 4 for _ in range(5)]
    assert seeded_region_growing(img, seeds, 8) == want
    assert srg_sorted_list(img, seeds, 8, flag_boundary=False) == want


def test_one_seed_and_bad_seeds():
    lab = seeded_region_growing([[1, 2, 3]], [[(0, 0)]], 4)
    assert lab == [[1, 1, 1]]
    with pytest.raises(ValueError):
        seeded_region_growing([[1, 2]], [[(0, 0)], [(0, 0)]], 4)
    with pytest.raises(ValueError):
        seeded_region_growing([[1, 2]], [[]], 4)
    assert BOUNDARY == -1
