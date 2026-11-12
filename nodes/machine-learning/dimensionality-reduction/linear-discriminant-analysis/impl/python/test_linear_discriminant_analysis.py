# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-discriminant-analysis/. The authors are listed in prov/SMRZT0.jsonl.

import math
import random

import pytest

from linear_discriminant_analysis import (
    GaussianLDA,
    fisher_lda,
    fisher_two_class,
    mat_vec,
    predict_in_fisher_space,
    quad,
    rayleigh,
    scatter_matrices,
)

A = [[1.0, 2.0], [2.0, 3.0], [3.0, 3.0], [2.0, 4.0]]
B = [[4.0, 4.0], [5.0, 6.0], [6.0, 5.0], [5.0, 5.0]]


def gaussian_classes(rng: random.Random, k: int, d: int, per: int) -> tuple[list, list]:
    mix = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(d)]
    xs, ys = [], []
    for c in range(k):
        centre = [rng.uniform(-3, 3) for _ in range(d)]
        for _ in range(per):
            z = [rng.gauss(0, 1) for _ in range(d)]
            xs.append([centre[i] + sum(mix[i][j] * z[j] for j in range(d)) for i in range(d)])
            ys.append(c)
    return xs, ys


def test_worked_example() -> None:
    _, means, _, s_w, s_b = scatter_matrices(A + B, [0] * 4 + [1] * 4)
    assert means[0] == [2.0, 3.0] and means[1] == [5.0, 5.0]
    assert s_w == [[4.0, 2.0], [2.0, 4.0]]
    lam, dirs = fisher_lda(A + B, [0] * 4 + [1] * 4)
    assert lam[0] == pytest.approx(14 / 3)
    w = dirs[0]
    assert w[0] / w[1] == pytest.approx(4.0)
    assert rayleigh([3.0, 2.0], s_b, s_w) == pytest.approx(169 / 38)
    clf = GaussianLDA(A + B, [0] * 4 + [1] * 4)
    # The boundary is 4 x1 + x2 = 18.
    assert clf.predict([4.0, 1.9]) == 0 and clf.predict([4.0, 2.1]) == 1


def test_rayleigh_optimum_against_fine_search() -> None:
    rng = random.Random(3)
    for _ in range(5):
        xs, ys = gaussian_classes(rng, 3, 2, 15)
        _, _, _, s_w, s_b = scatter_matrices(xs, ys)
        lam, dirs = fisher_lda(xs, ys)
        best = max(rayleigh([math.cos(t), math.sin(t)], s_b, s_w)
                   for t in (math.pi * i / 20000 for i in range(20000)))
        assert lam[0] == pytest.approx(rayleigh(dirs[0], s_b, s_w), rel=1e-10)
        assert lam[0] >= best - 1e-9
        assert lam[0] - best < 1e-6 * lam[0]


def test_generalized_eigen_equation_and_normalisation() -> None:
    rng = random.Random(5)
    xs, ys = gaussian_classes(rng, 4, 5, 12)
    _, _, _, s_w, s_b = scatter_matrices(xs, ys)
    lam, dirs = fisher_lda(xs, ys, r=5)
    for i, w in enumerate(dirs):
        lhs, rhs = mat_vec(s_b, w), mat_vec(s_w, w)
        assert all(abs(a - lam[i] * b) < 1e-8 * (1 + abs(a)) for a, b in zip(lhs, rhs))
        for j, v in enumerate(dirs):
            assert quad(w, s_w, v) == pytest.approx(1.0 if i == j else 0.0, abs=1e-9)
    assert lam == sorted(lam, reverse=True)


def test_rank_bound_k_minus_one() -> None:
    rng = random.Random(7)
    for k, d in [(2, 4), (3, 5), (4, 6)]:
        xs, ys = gaussian_classes(rng, k, d, 10)
        lam, _ = fisher_lda(xs, ys, r=d)
        assert all(v > 1e-6 for v in lam[: k - 1])
        assert all(abs(v) < 1e-9 * lam[0] for v in lam[k - 1:])


def test_two_classes_direction() -> None:
    rng = random.Random(11)
    for _ in range(5):
        xs, ys = gaussian_classes(rng, 2, 4, 20)
        _, dirs = fisher_lda(xs, ys)
        w2 = fisher_two_class(xs, ys)
        w = dirs[0]
        cos = sum(a * b for a, b in zip(w, w2)) / math.sqrt(sum(a * a for a in w) * sum(b * b for b in w2))
        assert abs(cos) == pytest.approx(1.0, abs=1e-10)
        clf = GaussianLDA(xs, ys)
        normal = [clf.coef[1][i] - clf.coef[0][i] for i in range(4)]
        cos2 = sum(a * b for a, b in zip(normal, w2)) / math.sqrt(sum(a * a for a in normal) * sum(b * b for b in w2))
        assert cos2 == pytest.approx(1.0, abs=1e-10)


def test_fisher_space_classifier_equals_gaussian_lda() -> None:
    rng = random.Random(13)
    xs, ys = gaussian_classes(rng, 3, 4, 20)
    clf = GaussianLDA(xs, ys)
    for _ in range(200):
        q = [rng.uniform(-6, 6) for _ in range(4)]
        assert predict_in_fisher_space(xs, ys, q) == clf.predict(q)


def test_singular_within_class_scatter() -> None:
    xs = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    ys = [0, 0, 1, 1]
    with pytest.raises(ValueError):
        fisher_lda(xs, ys)
