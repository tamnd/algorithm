# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/density-peak-clustering/. The authors are listed in prov/E4EF5R.jsonl.

import math
import random

import pytest

from density_peak_clustering import (delta_and_parent, density_peak_clustering, euclidean,
                                     local_density)


def blobs(rng, n, centers, spread):
    return [(cx + rng.gauss(0, spread), cy + rng.gauss(0, spread))
            for cx, cy in (rng.choice(centers) for _ in range(n))]


def higher(rho, j, i):
    """j has higher density than i under the tie rule of the page."""
    return rho[j] > rho[i] or (rho[j] == rho[i] and j < i)


def test_rho_and_delta_match_definitions():
    rng = random.Random(1)
    for _ in range(40):
        n = rng.randrange(1, 30)
        pts = [(float(rng.randrange(8)), float(rng.randrange(8))) for _ in range(n)]  # many ties
        d_c = rng.choice([1.0, 1.5, 2.0, 3.0])
        rho = local_density(pts, d_c)
        for i in range(n):
            assert rho[i] == sum(1 for j in range(n) if j != i and euclidean(pts[i], pts[j]) < d_c)
        order, delta, parent = delta_and_parent(pts, rho)
        top = order[0]
        assert all(not higher(rho, j, top) for j in range(n))
        for i in range(n):
            above = [j for j in range(n) if higher(rho, j, i)]
            if not above:
                assert i == top and parent[i] == -1
                assert delta[i] == max(euclidean(pts[i], q) for q in pts)
            else:
                want = min(euclidean(pts[i], pts[j]) for j in above)
                assert delta[i] == want
                assert parent[i] in above and euclidean(pts[i], pts[parent[i]]) == want


def test_assignment_follows_parents_to_one_center():
    rng = random.Random(2)
    for _ in range(40):
        n = rng.randrange(1, 40)
        pts = blobs(rng, n, [(0, 0), (6, 0), (3, 5)], 1.0)
        kernel = rng.choice(["cutoff", "gaussian"])
        k = rng.randrange(1, 5)
        labels, centers = density_peak_clustering(pts, 1.0, n_centers=k, kernel=kernel)
        rho = local_density(pts, 1.0, kernel)
        order, delta, parent = delta_and_parent(pts, rho)
        assert 1 <= len(centers) <= max(k, 1)
        assert order[0] in centers
        for c, p in enumerate(centers):
            assert labels[p] == c
        center_set = set(centers)
        for i in range(n):
            # Follow the nearest higher density points until the first center.
            j = i
            while j not in center_set:
                j = parent[j]
            assert labels[i] == labels[j]
            if i not in center_set:
                assert labels[i] == labels[parent[i]]


def test_centers_by_gamma_and_by_thresholds():
    rng = random.Random(3)
    pts = blobs(rng, 60, [(0, 0)], 0.5) + blobs(rng, 60, [(8, 0)], 0.5) + blobs(rng, 60, [(4, 7)], 0.5)
    labels, centers = density_peak_clustering(pts, 0.8, n_centers=3)
    assert len(centers) == 3
    for block in range(3):
        assert len({labels[i] for i in range(60 * block, 60 * block + 60)}) == 1
    rho = local_density(pts, 0.8)
    order, delta, parent = delta_and_parent(pts, rho)
    labels2, centers2 = density_peak_clustering(pts, 0.8, rho_min=5, delta_min=3)
    assert set(centers2) == set(centers)


def test_gaussian_density_is_permutation_invariant():
    rng = random.Random(4)
    for _ in range(10):
        pts = blobs(rng, 30, [(0, 0), (5, 0)], 0.8)
        labels, _ = density_peak_clustering(pts, 1.0, n_centers=2, kernel="gaussian")
        perm = list(range(30))
        rng.shuffle(perm)
        labels2, _ = density_peak_clustering([pts[p] for p in perm], 1.0, n_centers=2, kernel="gaussian")
        for a in range(30):
            for b in range(30):
                assert (labels[perm[a]] == labels[perm[b]]) == (labels2[a] == labels2[b])


def test_ties_follow_the_index():
    # Four points on a square: every density is 2, so the order is the index order.
    pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)]
    rho = local_density(pts, 1.2)
    assert rho == [2, 2, 2, 2]
    order, delta, parent = delta_and_parent(pts, rho)
    assert order == [0, 1, 2, 3]
    assert parent == [-1, 0, 0, 1]
    assert delta[0] == math.sqrt(2)


def test_example_of_the_page():
    pts = [(x,) for x in (0, 1, 2, 3, 4, 10, 11, 12, 20)]
    rho = local_density(pts, 1.5)
    assert rho == [1, 2, 2, 2, 1, 1, 2, 1, 0]
    order, delta, parent = delta_and_parent(pts, rho)
    assert order == [1, 2, 3, 6, 0, 4, 5, 7, 8]
    assert delta == [1, 19, 1, 1, 1, 1, 8, 1, 8]
    assert parent == [1, -1, 1, 2, 3, 6, 3, 6, 7]
    labels, centers = density_peak_clustering(pts, 1.5, rho_min=0.5, delta_min=4)
    assert centers == [1, 6]
    assert labels == [0, 0, 0, 0, 0, 1, 1, 1, 1]
    # With n_centers = 3 the outlier 20 (low rho, high delta) has gamma 0 and is not
    # chosen. The third largest gamma is 2, shared by the indices 2 and 3, and the
    # tie rule picks index 2, the earlier one in the density order.
    labels3, centers3 = density_peak_clustering(pts, 1.5, n_centers=3)
    assert centers3 == [1, 2, 6]
    assert labels3 == [0, 0, 1, 1, 1, 2, 2, 2, 2]


def test_halo():
    pts = [(x,) for x in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)]
    labels, centers, is_halo = density_peak_clustering(pts, 1.5, n_centers=2, with_halo=True)
    rho = local_density(pts, 1.5)
    for c in set(labels):
        members = [i for i in range(10) if labels[i] == c]
        border = [i for i in members if any(labels[j] != c and abs(pts[i][0] - pts[j][0]) < 1.5 for j in range(10))]
        rho_b = max(rho[i] for i in border) if border else -math.inf
        for i in members:
            assert is_halo[i] == (rho[i] <= rho_b)


def test_edges():
    assert density_peak_clustering([], 1.0, n_centers=1) == ([], [])
    assert density_peak_clustering([(5.0,)], 1.0, n_centers=3) == ([0], [0])
    with pytest.raises(ValueError):
        density_peak_clustering([(0.0,)], 1.0)
