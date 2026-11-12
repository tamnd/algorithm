# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-projection/. The authors are listed in prov/R90KN4.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from random_projection import dot, draw_entry, fit_transform, project_rows, random_matrix, sq_dist


def exact_rademacher_moments(x, y):
    """E and Var of (r . x)(r . y) over all 2^d sign vectors r, in exact arithmetic."""
    m1 = m2 = Fraction(0)
    p = Fraction(1, 2 ** len(x))
    for r in itertools.product((-1, 1), repeat=len(x)):
        v = Fraction(dot(r, x)) * dot(r, y)
        m1 += p * v
        m2 += p * v * v
    return m1, m2 - m1 * m1


def test_rademacher_inner_product_is_unbiased_with_exact_variance():
    x, y = [3, 1, -2, 0, 1], [1, -1, 1, 2, 2]
    mean, var = exact_rademacher_moments(x, y)
    assert mean == dot(x, y)
    # Var = ||x||^2 ||y||^2 + (x . y)^2 - 2 sum x_i^2 y_i^2 for +-1 entries.
    nx, ny, xy = dot(x, x), dot(y, y), dot(x, y)
    assert var == nx * ny + xy * xy - 2 * sum(a * a * b * b for a, b in zip(x, y))


def test_rademacher_squared_norm_variance():
    x = [1, 2, -2, 0]
    mean, var = exact_rademacher_moments(x, x)
    assert mean == 9
    assert var == 2 * 81 - 2 * 33


def test_entry_distributions_have_unit_variance():
    rng = random.Random(0)
    for kind in ("gaussian", "rademacher", "achlioptas"):
        vals = [draw_entry(kind, rng) for _ in range(30000)]
        mean = sum(vals) / len(vals)
        var = sum(v * v for v in vals) / len(vals)
        assert abs(mean) < 0.03
        assert abs(var - 1) < 0.04


def test_unknown_distribution():
    with pytest.raises(ValueError):
        draw_entry("cauchy", random.Random(0))


def test_projection_is_reproducible_with_the_seed():
    rng = random.Random(1)
    x = [[rng.gauss(0, 1) for _ in range(20)] for _ in range(5)]
    a, _ = fit_transform(x, 6, "rademacher", random.Random(5))
    b, _ = fit_transform(x, 6, "rademacher", random.Random(5))
    assert a == b


def test_pairwise_distances_within_eps_for_each_distribution():
    rng = random.Random(2)
    n, d, k, eps = 25, 300, 200, 0.5
    x = [[rng.gauss(0, 1) for _ in range(d)] for _ in range(n)]
    for seed, kind in enumerate(("gaussian", "rademacher", "achlioptas")):
        y, _ = fit_transform(x, k, kind, random.Random(10 + seed))
        for i in range(n):
            for j in range(i + 1, n):
                ratio = sq_dist(y[i], y[j]) / sq_dist(x[i], x[j])
                assert 1 - eps < ratio < 1 + eps


def test_inner_products_of_unit_vectors_are_close():
    # For unit x and y, the error of the projected inner product is about sqrt(2/k).
    rng = random.Random(3)
    d, k = 200, 400
    x = [rng.gauss(0, 1) for _ in range(d)]
    y = [a + rng.gauss(0, 1) for a in x]
    nx, ny = dot(x, x) ** 0.5, dot(y, y) ** 0.5
    x = [a / nx for a in x]
    y = [a / ny for a in y]
    r = random_matrix(d, k, "gaussian", random.Random(4))
    px, py = project_rows([x, y], r)
    assert abs(dot(px, py) - dot(x, y)) < 4 * (2 / k) ** 0.5


def test_project_rows_matches_definition():
    r = [[1.0, 0.0], [2.0, -1.0], [0.0, 3.0]]
    (y,) = project_rows([[1.0, 1.0, 1.0]], r)
    assert y == pytest.approx([3.0 / 2 ** 0.5, 2.0 / 2 ** 0.5])
