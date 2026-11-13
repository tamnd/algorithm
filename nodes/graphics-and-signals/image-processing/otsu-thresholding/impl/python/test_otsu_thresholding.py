# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/otsu-thresholding/. The authors are listed in prov/5FBGX8.jsonl.

import itertools
import random
from fractions import Fraction

from otsu_thresholding import (
    between_class_variances,
    binarize,
    histogram,
    multi_otsu_from_histogram,
    otsu_threshold,
    otsu_threshold_from_histogram,
)

EXAMPLE = [
    [0, 1, 1, 2, 6, 7],
    [1, 1, 2, 2, 6, 6],
    [1, 0, 2, 5, 6, 7],
]


def pixels(img):
    return [v for row in img for v in row]


def mean(xs):
    return Fraction(sum(xs), len(xs))


def var(xs):
    m = mean(xs)
    return sum((Fraction(x) - m) ** 2 for x in xs) / len(xs)


def brute_force(img, levels):
    """Every threshold, scored by the within-class variance from the pixel lists."""
    px = pixels(img)
    n = len(px)
    scores = {}
    for t in range(levels - 1):
        c0 = [v for v in px if v <= t]
        c1 = [v for v in px if v > t]
        if not c0 or not c1:
            continue
        w0 = Fraction(len(c0), n)
        w1 = Fraction(len(c1), n)
        within = w0 * var(c0) + w1 * var(c1)
        between = w0 * (mean(c0) - mean(px)) ** 2 + w1 * (mean(c1) - mean(px)) ** 2
        scores[t] = (within, between)
    if not scores:
        return None, scores
    least = min(w for w, _ in scores.values())
    return min(t for t, (w, _) in scores.items() if w == least), scores


def random_image(rng, h, w, levels):
    kind = rng.randrange(3)
    if kind == 0:
        return [[rng.randrange(levels) for _ in range(w)] for _ in range(h)]
    a = rng.randrange(levels)
    b = rng.randrange(levels)
    spread = rng.randrange(1, 3)
    return [
        [min(levels - 1, max(0, (a if rng.random() < 0.5 else b) + rng.randint(-spread, spread))) for _ in range(w)]
        for _ in range(h)
    ]


def test_example():
    h = histogram(EXAMPLE, 8)
    assert h == [2, 5, 4, 0, 0, 1, 4, 2]
    assert otsu_threshold(EXAMPLE, 8) == 2
    sb = between_class_variances(h)
    assert sb[2] == Fraction(36481, 6237)
    assert sb[5] == Fraction(841, 162)
    assert var(pixels(EXAMPLE)) - sb[2] == Fraction(109, 231)
    assert multi_otsu_from_histogram(h, 3) == (1, 2)
    assert sb[3] == sb[2] and sb[4] == sb[2]
    assert binarize(EXAMPLE, 2)[0] == [0, 0, 0, 0, 1, 1]


def test_against_brute_force():
    rng = random.Random(1979)
    for _ in range(400):
        levels = rng.randrange(2, 12)
        img = random_image(rng, rng.randrange(1, 5), rng.randrange(1, 6), levels)
        t_bf, scores = brute_force(img, levels)
        assert otsu_threshold(img, levels) == t_bf
        sb = between_class_variances(histogram(img, levels))
        total = var(pixels(img))
        for t, (within, between) in scores.items():
            assert sb[t] == between
            assert within + between == total


def test_max_between_is_min_within():
    rng = random.Random(7)
    for _ in range(200):
        levels = rng.randrange(2, 10)
        img = random_image(rng, 3, 4, levels)
        _, scores = brute_force(img, levels)
        if not scores:
            continue
        best_b = max(b for _, b in scores.values())
        best_w = min(w for w, _ in scores.values())
        assert {t for t, (_, b) in scores.items() if b == best_b} == {
            t for t, (w, _) in scores.items() if w == best_w
        }


def test_constant_image():
    assert otsu_threshold([[3, 3], [3, 3]], 8) is None
    assert otsu_threshold([[0, 7]], 8) == 0


def test_invariant_under_affine_map_of_levels():
    rng = random.Random(11)
    for _ in range(100):
        img = random_image(rng, 3, 5, 6)
        t = otsu_threshold(img, 6)
        shifted = [[2 * v + 3 for v in row] for row in img]
        t2 = otsu_threshold(shifted, 16)
        if t is None:
            assert t2 is None
            continue
        assert binarize(img, t) == binarize(shifted, t2)


def multi_brute(h, classes):
    big_l = len(h)
    best = None
    for cuts in itertools.combinations(range(big_l - 1), classes - 1):
        bounds = [-1] + list(cuts) + [big_l - 1]
        val = Fraction(0)
        for a, b in zip(bounds, bounds[1:]):
            cnt = sum(h[a + 1 : b + 1])
            s = sum(i * h[i] for i in range(a + 1, b + 1))
            if cnt:
                val += Fraction(s * s, cnt)
        if best is None or val > best:
            best = val
    return best


def multi_value(h, cuts):
    bounds = [-1] + list(cuts) + [len(h) - 1]
    val = Fraction(0)
    for a, b in zip(bounds, bounds[1:]):
        cnt = sum(h[a + 1 : b + 1])
        s = sum(i * h[i] for i in range(a + 1, b + 1))
        if cnt:
            val += Fraction(s * s, cnt)
    return val


def test_multi_otsu_against_brute_force():
    rng = random.Random(3)
    for _ in range(150):
        big_l = rng.randrange(2, 9)
        h = [rng.randrange(0, 5) for _ in range(big_l)]
        if sum(h) == 0:
            h[0] = 1
        for m in range(1, min(4, big_l) + 1):
            cuts = multi_otsu_from_histogram(h, m)
            assert len(cuts) == m - 1
            assert list(cuts) == sorted(set(cuts))
            assert multi_value(h, cuts) == multi_brute(h, m)


def test_two_class_multi_matches_otsu():
    rng = random.Random(5)
    for _ in range(100):
        h = [rng.randrange(0, 6) for _ in range(rng.randrange(2, 10))]
        t = otsu_threshold_from_histogram(h)
        if t is None:
            continue
        (t2,) = multi_otsu_from_histogram(h, 2)
        assert multi_value(h, (t2,)) == multi_value(h, (t,))
