# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/intrinsic-dimension-estimation/. The authors are listed in prov/253A61.jsonl.

import math
import random

import pytest

from intrinsic_dimension_estimation import (
    correlation_dimension,
    correlation_integral,
    embed_cube,
    levina_bickel,
    levina_bickel_local,
    sorted_neighbor_distances,
    twonn,
    twonn_fit,
    twonn_mle,
)

LINE = [[0.0, 0.0], [1.0, 0.0], [3.0, 0.0], [7.0, 0.0], [8.0, 0.0]]


def test_neighbor_distances_on_the_line_example():
    nd = sorted_neighbor_distances(LINE, 3)
    assert nd == [[1.0, 3.0, 7.0], [1.0, 2.0, 6.0], [2.0, 3.0, 4.0], [1.0, 4.0, 6.0], [1.0, 5.0, 7.0]]


def test_levina_bickel_local_by_hand():
    # T = (2, 3, 4), k = 3: m = 2 / (ln 2 + ln(4/3)) = 2 / ln(8/3).
    assert levina_bickel_local([2.0, 3.0, 4.0], 3) == pytest.approx(2 / math.log(8 / 3))
    # Distances that double each time give m = (k - 1) / (ln 2 * sum_{j<k} (k - j)).
    assert levina_bickel_local([1.0, 2.0, 4.0, 8.0], 4) == pytest.approx(3 / (6 * math.log(2)))


def test_twonn_slope_is_exact_on_pareto_quantiles():
    # If mu_(i) = (1 - i/N)^(-1/d), every point lies on y = d x.
    for d in (1.0, 2.5, 7.0):
        n = 200
        mus = [(1 - i / n) ** (-1 / d) for i in range(1, n + 1) if i < n] + [1e9]
        assert twonn_fit(mus, discard=0.1) == pytest.approx(d, rel=1e-12)


def test_twonn_fit_drops_the_infinite_last_point_without_discard():
    mus = [(1 - i / 50) ** (-1 / 3) for i in range(1, 50)] + [1e9]
    assert twonn_fit(mus, discard=0.0) == pytest.approx(3.0, rel=1e-12)


def test_levina_bickel_unbiased_form_on_the_exact_local_model():
    # Under the local Poisson model, given T_k the ratios (T_j / T_k)^m are uniform order statistics.
    rng = random.Random(0)
    m, k, trials = 3.0, 10, 20000
    acc_mle = acc_unbiased = 0.0
    for _ in range(trials):
        us = sorted(rng.random() for _ in range(k - 1))
        t = [u ** (1 / m) for u in us] + [1.0]
        s = sum(math.log(t[k - 1] / t[j]) for j in range(k - 1))
        acc_mle += (k - 1) / s
        acc_unbiased += (k - 2) / s
    # E[(k - 1) / S] = m (k - 1)/(k - 2) and E[(k - 2) / S] = m for S ~ Gamma(k - 1, rate m).
    assert acc_unbiased / trials == pytest.approx(m, rel=0.02)
    assert acc_mle / trials == pytest.approx(m * (k - 1) / (k - 2), rel=0.02)


def test_estimators_are_invariant_under_similarity():
    pts = embed_cube(120, 2, 5, random.Random(1))
    moved = [[3.0 * v + 1.0 for v in p] for p in pts]
    swapped = [list(reversed(p)) for p in pts]
    for f in (lambda q: levina_bickel(q, 5, 8), twonn, twonn_mle):
        a = f(pts)
        assert f(moved) == pytest.approx(a, rel=1e-9)
        assert f(swapped) == pytest.approx(a, rel=1e-9)


def test_embedded_square_in_r10():
    pts = embed_cube(300, 2, 10, random.Random(11))
    assert abs(levina_bickel(pts, 10, 20) - 2) < 0.3
    assert abs(twonn(pts) - 2) < 0.4
    radii = [0.05 * math.sqrt(2) * 1.25 ** i for i in range(6)]
    assert abs(correlation_dimension(pts, radii) - 2) < 0.4


def test_embedded_four_cube_in_r10():
    # Boundary effects bias all three estimates down in higher dimension.
    pts = embed_cube(300, 4, 10, random.Random(12))
    assert 3.4 < levina_bickel(pts, 10, 20) < 4.4
    assert 3.2 < twonn(pts) < 4.4


def test_embedding_keeps_distances():
    # Same seed, so embed_cube draws the same basis and then the same cube points.
    rng_a, rng_b = random.Random(3), random.Random(3)
    pts = embed_cube(6, 3, 8, rng_a)
    for _ in range(3):  # replay the basis draws
        [rng_b.gauss(0, 1) for _ in range(8)]
    cube = [[rng_b.random() for _ in range(3)] for _ in range(6)]
    for i in range(6):
        for j in range(6):
            assert math.dist(pts[i], pts[j]) == pytest.approx(math.dist(cube[i], cube[j]), abs=1e-12)


def test_correlation_integral_counts_pairs():
    assert correlation_integral(LINE, 1.5) == pytest.approx(2 / 10)
    assert correlation_integral(LINE, 100.0) == 1.0
    with pytest.raises(ValueError):
        correlation_dimension(LINE, [0.1, 0.2])


def test_levina_bickel_rejects_bad_k():
    with pytest.raises(ValueError):
        levina_bickel(LINE, 1)
