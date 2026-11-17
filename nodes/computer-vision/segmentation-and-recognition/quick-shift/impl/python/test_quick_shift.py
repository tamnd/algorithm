# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quick-shift/. The authors are listed in prov/5E6C9Y.jsonl.

import math
import random

from quick_shift import cut, quick_shift


def brute_parents(img, dens, tau, lam):
    """Search all pixels, not a window, for the nearest pixel with a larger key."""
    h, w = len(img), len(img[0])
    feat = [(u, v, lam * img[v][u]) for v in range(h) for u in range(w)]
    out = []
    for i, fi in enumerate(feat):
        cands = [(math.dist(fi, fj), j) for j, fj in enumerate(feat) if (dens[j], j) > (dens[i], i)]
        cands = [c for c in cands if c[0] <= tau]
        out.append(min(cands)[1] if cands else i)
    return out


def random_image(rng, w, h, levels):
    return [[rng.randrange(levels) for _ in range(w)] for _ in range(h)]


def test_row_example():
    img = [[0, 1, 1, 0, 5, 6, 5]]
    lab, parent, dist, dens = quick_shift(img, 1.0, 2.0)
    expected = [1.4611, 2.0565, 2.0565, 1.4611, 1.5033, 1.7358, 1.5032]
    assert all(abs(a - b) < 1e-4 for a, b in zip(dens, expected))
    assert 0 < dens[2] - dens[1] < 1e-4  # pixel 2 sees the bright pixels a little more
    assert parent == [1, 2, 2, 2, 5, 5, 5]
    assert lab == [[2, 2, 2, 2, 5, 5, 5]]
    lab, parent, dist, _ = quick_shift(img, 1.0, math.inf)
    assert parent == [1, 2, 2, 2, 5, 2, 5]
    assert abs(dist[5] - math.sqrt(34)) < 1e-12
    assert lab == [[2] * 7]
    assert cut(parent, dist, 2.0, 7, 1) == [[2, 2, 2, 2, 5, 5, 5]]


def test_equal_densities_are_broken_by_the_index():
    lab, parent, dist, dens = quick_shift([[3, 3]], 1.0, 2.0)
    assert dens[0] == dens[1]
    assert parent == [1, 1] and dist[0] == 1.0 and lab == [[1, 1]]


def test_window_search_equals_brute_force():
    rng = random.Random(7)
    for _ in range(12):
        img = random_image(rng, 6, 5, 4)
        sigma = rng.choice([0.7, 1.0, 1.5])
        tau = rng.choice([1.0, 1.5, 2.5, 4.0])
        lam = rng.choice([0.5, 1.0, 2.0])
        _, parent, _, dens = quick_shift(img, sigma, tau, lam)
        assert parent == brute_parents(img, dens, tau, lam)


def test_links_form_a_forest_with_increasing_keys():
    rng = random.Random(8)
    for _ in range(10):
        img = random_image(rng, 7, 6, 5)
        lab, parent, dist, dens = quick_shift(img, 1.0, 3.0)
        w = 7
        for i, j in enumerate(parent):
            if j != i:
                assert (dens[j], j) > (dens[i], i)
                assert dist[i] <= 3.0
            else:
                assert dist[i] == math.inf
        for i in range(len(parent)):
            r = lab[i // w][i % w]
            assert parent[r] == r


def test_cut_of_the_full_tree_equals_a_smaller_tau():
    rng = random.Random(9)
    for _ in range(8):
        img = random_image(rng, 6, 6, 6)
        _, parent, dist, _ = quick_shift(img, 1.0, math.inf)
        roots = {r for row in quick_shift(img, 1.0, math.inf)[0] for r in row}
        assert len(roots) == 1
        for t in (1.0, 1.5, 2.0, 3.0):
            assert cut(parent, dist, t, 6, 6) == quick_shift(img, 1.0, t)[0]


def test_two_flat_regions_give_two_segments():
    img = [[0] * 4 + [1] * 4 for _ in range(6)]
    lab, _, _, _ = quick_shift(img, 2.0, 4.0, lam=10.0)
    left = {lab[v][u] for v in range(6) for u in range(4)}
    right = {lab[v][u] for v in range(6) for u in range(4, 8)}
    assert len(left) == 1 and len(right) == 1 and left != right


def test_adding_a_constant_to_the_image_changes_nothing():
    rng = random.Random(10)
    img = random_image(rng, 6, 5, 5)
    brighter = [[x + 7 for x in row] for row in img]
    a = quick_shift(img, 1.0, 2.0)
    b = quick_shift(brighter, 1.0, 2.0)
    assert a[0] == b[0] and a[1] == b[1]
