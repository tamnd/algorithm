# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/data-augmentation/. The authors are listed in prov/B4MG5J.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

from data_augmentation import (augmented_square_loss, augmented_stream, cross_entropy, cutout, cyclic_shifts,
                               flip_horizontal, mixup_batch, mixup_pair, one_hot, orbit_average,
                               orbit_mean_and_covariance, random_crop)

IMG = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]


def test_flip_and_crop_keep_the_shape_and_the_pixels() -> None:
    assert flip_horizontal(flip_horizontal(IMG)) == IMG
    rng = random.Random(0)
    for _ in range(20):
        out = random_crop(IMG, 1, rng)
        assert len(out) == 3 and all(len(r) == 4 for r in out)
        shifted = lambda di, dj: [[IMG[i + di][j + dj] if 0 <= i + di < 3 and 0 <= j + dj < 4 else 0
                                   for j in range(4)] for i in range(3)]
        assert any(out == shifted(di, dj) for di in (-1, 0, 1) for dj in (-1, 0, 1))


def test_cutout_zeroes_exactly_the_clipped_square() -> None:
    rng = random.Random(1)
    img = [[1] * 7 for _ in range(6)]
    for _ in range(50):
        out, (ci, cj) = cutout(img, 3, rng)
        zeros = {(i, j) for i in range(6) for j in range(7) if out[i][j] == 0}
        want = {(i, j) for i in range(ci - 1, ci + 2) for j in range(cj - 1, cj + 2) if 0 <= i < 6 and 0 <= j < 7}
        assert zeros == want


def test_mixup_labels_are_the_same_convex_combination() -> None:
    lam = F(7, 10)
    x, y = mixup_pair([F(1), F(0)], [F(1), F(0), F(0)], [F(0), F(1)], [F(0), F(0), F(1)], lam)
    assert x == [F(7, 10), F(3, 10)] and y == [F(7, 10), F(0), F(3, 10)]
    rng = random.Random(2)
    xs = [[rng.gauss(0.0, 1.0) for _ in range(3)] for _ in range(8)]
    ys = [one_hot(rng.randrange(4), 4) for _ in range(8)]
    mx, my, lam, perm = mixup_batch(xs, ys, 0.4, rng)
    assert 0 < lam < 1
    for i, k in enumerate(perm):
        assert math.isclose(sum(my[i]), 1.0)
        assert all(math.isclose(a, lam * b + (1 - lam) * c) for a, b, c in zip(mx[i], xs[i], xs[k]))
        assert all(math.isclose(a, lam * b + (1 - lam) * c) for a, b, c in zip(my[i], ys[i], ys[k]))


def test_cross_entropy_of_mixed_label_is_the_mixed_cross_entropy() -> None:
    probs = [0.5, 0.2, 0.3]
    _, y = mixup_pair([0.0], one_hot(0, 3), [0.0], one_hot(2, 3), 0.7)
    want = 0.7 * cross_entropy(one_hot(0, 3), probs) + 0.3 * cross_entropy(one_hot(2, 3), probs)
    assert math.isclose(cross_entropy(y, probs), want)


def test_orbit_average_is_invariant() -> None:
    f = lambda x: x[0] * 3 - x[1] + x[0] * x[2]
    f_bar = orbit_average(f, cyclic_shifts)
    x = [F(1), F(2), F(-1), F(5)]
    assert all(f_bar(z) == f_bar(x) for z in cyclic_shifts(x))


def test_orbit_average_lowers_the_risk_by_the_orbit_variance() -> None:
    xs = [list(map(F, bits)) for bits in itertools.product((0, 1), repeat=4)]
    data = [(x, sum(x) + noise) for x in xs for noise in (F(-1, 2), F(1, 2))]
    w = [F(1), F(2), F(0), F(-1)]
    f = lambda x: sum(a * b for a, b in zip(w, x)) + F(1, 3)
    f_bar = orbit_average(f, cyclic_shifts)
    risk = lambda h: sum((h(x) - y) ** 2 for x, y in data) / len(data)
    gap = sum(sum((f(z) - f_bar(x)) ** 2 for z in cyclic_shifts(x)) / 4 for x, _ in data) / len(data)
    assert risk(f) - risk(f_bar) == gap and gap > 0


def test_augmented_square_loss_is_loss_on_mean_plus_penalty() -> None:
    assert augmented_square_loss([1, 0, 0, 0], [F(1), F(0), F(0), F(2)], 1, cyclic_shifts) == F(3, 4)
    rng = random.Random(3)
    for _ in range(10):
        x = [F(rng.randint(-3, 3)) for _ in range(4)]
        w = [F(rng.randint(-3, 3), 2) for _ in range(4)]
        y = F(rng.randint(-5, 5))
        mean, cov = orbit_mean_and_covariance(x, cyclic_shifts)
        fit = (sum(a * b for a, b in zip(w, mean)) - y) ** 2
        pen = sum(w[i] * cov[i][j] * w[j] for i in range(4) for j in range(4))
        assert augmented_square_loss(w, x, y, cyclic_shifts) == fit + pen


def test_stream_draws_a_new_transform_each_time() -> None:
    data = [(IMG, 0)]
    seen = {tuple(map(tuple, x)) for x, _ in augmented_stream(data, [lambda im: im, flip_horizontal],
                                                              random.Random(4), 30)}
    assert seen == {tuple(map(tuple, IMG)), tuple(map(tuple, flip_horizontal(IMG)))}
