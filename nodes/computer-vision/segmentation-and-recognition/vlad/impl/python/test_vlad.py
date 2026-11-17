# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vlad/. The authors are listed in prov/D9847P.jsonl.

import math
import random

from vlad import (cell_means, l2_normalize, nearest_center, power_normalize,
                  sum_match_kernel, vlad, vlad_blocks)

CENTERS = [[0.0, 0.0], [4.0, 0.0]]
X = [[1.0, 1.0], [-1.0, 2.0], [3.0, 1.0], [5.0, -1.0], [6.0, 0.0]]
TOL = 1e-12


def close(a, b, tol=TOL):
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


def random_set(rng, n, D):
    return [[rng.uniform(-3.0, 3.0) for _ in range(D)] for _ in range(n)]


def test_example_of_the_page():
    assert vlad_blocks(X, CENTERS) == [[0.0, 3.0], [2.0, 0.0]]
    assert close(vlad(X, CENTERS), [0.0, 3 / math.sqrt(13), 2 / math.sqrt(13), 0.0])
    assert close(vlad(X, CENTERS, alpha=0.5), [0.0, math.sqrt(3 / 5), math.sqrt(2 / 5), 0.0])
    h = 1 / math.sqrt(2)
    assert close(vlad(X, CENTERS, intra=True), [0.0, h, h, 0.0])


def test_residuals_cancel_in_a_cell():
    # (3, 1) and (5, -1) have residuals (-1, 1) and (1, -1) to (4, 0): they cancel.
    assert vlad_blocks([[3.0, 1.0], [5.0, -1.0]], CENTERS) == [[0.0, 0.0], [0.0, 0.0]]


def test_tie_goes_to_smaller_index():
    assert nearest_center([2.0, 5.0], CENTERS) == 0


def test_dimension_and_unit_norm():
    rng = random.Random(1)
    for K, D in [(1, 3), (4, 2), (8, 5)]:
        C = random_set(rng, K, D)
        z = vlad(random_set(rng, 30, D), C, alpha=0.5)
        assert len(z) == K * D
        assert abs(sum(t * t for t in z) - 1.0) < 1e-12


def test_order_of_descriptors_does_not_matter():
    rng = random.Random(2)
    C = random_set(rng, 5, 4)
    xs = random_set(rng, 40, 4)
    ys = list(xs)
    rng.shuffle(ys)
    assert close(vlad(xs, C, alpha=0.5, intra=True), vlad(ys, C, alpha=0.5, intra=True), 1e-12)


def test_block_is_count_times_mean_minus_center():
    rng = random.Random(3)
    C = random_set(rng, 6, 3)
    xs = random_set(rng, 50, 3)
    v = vlad_blocks(xs, C)
    counts, means = cell_means(xs, C)
    for k in range(6):
        if counts[k] == 0:
            assert v[k] == [0.0, 0.0, 0.0]
        else:
            expect = [counts[k] * (m - c) for m, c in zip(means[k], C[k])]
            assert close(v[k], expect, 1e-9)


def test_inner_product_is_the_sum_match_kernel():
    rng = random.Random(4)
    for _ in range(5):
        C = random_set(rng, 4, 3)
        xs, ys = random_set(rng, 15, 3), random_set(rng, 12, 3)
        a = vlad(xs, C, l2=False)
        b = vlad(ys, C, l2=False)
        dot = sum(s * t for s, t in zip(a, b))
        assert abs(dot - sum_match_kernel(xs, ys, C)) < 1e-9


def test_equals_hard_fisher_mean_gradient_up_to_scale():
    # Fisher vector mean part with hard assignment, w_k = 1/K and sigma = 1:
    # G_k = (1 / (T sqrt(w_k))) sum over the cell of (x - mu_k).
    rng = random.Random(5)
    K, D, T = 5, 3, 40
    C = random_set(rng, K, D)
    xs = random_set(rng, T, D)
    g = [[0.0] * D for _ in range(K)]
    for x in xs:
        k = nearest_center(x, C)
        for i in range(D):
            g[k][i] += (x[i] - C[k][i]) / (T * math.sqrt(1.0 / K))
    flat_g = [t for block in g for t in block]
    v = vlad(xs, C, l2=False)
    assert close(flat_g, [math.sqrt(K) / T * t for t in v], 1e-12)
    assert close(l2_normalize(flat_g), vlad(xs, C), 1e-12)


def test_intra_normalization_blocks():
    rng = random.Random(6)
    C = random_set(rng, 6, 4)
    xs = random_set(rng, 8, 4)
    z = vlad(xs, C, intra=True, l2=False)
    for k in range(6):
        s = sum(t * t for t in z[4 * k:4 * k + 4])
        assert abs(s - 1.0) < 1e-12 or s == 0.0


def test_power_normalization_keeps_sign():
    z = [-4.0, 0.0, 9.0, -0.25]
    assert power_normalize(z, 0.5) == [-2.0, 0.0, 3.0, -0.5]
    assert power_normalize(z, 1.0) == z


def test_empty_set_gives_zero_vector():
    assert vlad([], CENTERS) == [0.0, 0.0, 0.0, 0.0]
