# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounding-box-regression/. The authors are listed in prov/TRRBN0.jsonl.

import math
import random
from fractions import Fraction

from bounding_box_regression import (
    DEFAULT_CLIP,
    box_loss,
    decode,
    encode,
    encode_shift,
    fit_ridge,
    giou,
    iou,
    smooth_l1,
    smooth_l1_grad,
)


def rand_box(rng, lo=-50.0, hi=50.0):
    x1, y1 = rng.uniform(lo, hi), rng.uniform(lo, hi)
    return (x1, y1, x1 + rng.uniform(1.0, 60.0), y1 + rng.uniform(1.0, 60.0))


def close(a, b, tol=1e-9):
    return all(abs(p - q) <= tol * max(1.0, abs(p), abs(q)) for p, q in zip(a, b))


def test_page_example():
    a, g = (0, 0, 10, 10), (2, 1, 14, 9)
    assert encode_shift(a, g) == (Fraction(3, 10), Fraction(0))
    t = encode(a, g)
    assert close(t, (0.3, 0.0, math.log(1.2), math.log(0.8)))
    assert close(decode(a, t), g)


def test_decode_inverts_encode():
    rng = random.Random(1)
    for _ in range(300):
        a, g = rand_box(rng), rand_box(rng)
        assert close(decode(a, encode(a, g)), g, 1e-9)
        w = (10.0, 10.0, 5.0, 5.0)
        assert close(decode(a, encode(a, g, w), w), g, 1e-9)


def test_encode_inverts_decode():
    rng = random.Random(2)
    for _ in range(300):
        a = rand_box(rng)
        t = tuple(rng.uniform(-2.0, 2.0) for _ in range(4))
        assert close(encode(a, decode(a, t)), t, 1e-9)


def test_inclusive_round_trip():
    rng = random.Random(3)
    for _ in range(100):
        x1, y1 = rng.randint(0, 50), rng.randint(0, 50)
        a = (x1, y1, x1 + rng.randint(0, 40), y1 + rng.randint(0, 40))
        x1, y1 = rng.randint(0, 50), rng.randint(0, 50)
        g = (x1, y1, x1 + rng.randint(0, 40), y1 + rng.randint(0, 40))
        assert close(decode(a, encode(a, g, inclusive=True), inclusive=True), g, 1e-9)


def test_invariance_under_scaling_and_shift():
    rng = random.Random(4)
    for _ in range(200):
        a, g = rand_box(rng), rand_box(rng)
        sx, sy = rng.uniform(0.1, 10.0), rng.uniform(0.1, 10.0)
        bx, by = rng.uniform(-100, 100), rng.uniform(-100, 100)

        def m(b):
            return (sx * b[0] + bx, sy * b[1] + by, sx * b[2] + bx, sy * b[3] + by)

        assert close(encode(m(a), m(g)), encode(a, g), 1e-9)


def test_iou_after_one_coordinate_error():
    # A center error e (in widths) gives IoU (1 - |e|) / (1 + |e|); a log-width error e gives exp(-|e|).
    rng = random.Random(5)
    for _ in range(100):
        g = rand_box(rng)
        t = encode(g, g)
        e = rng.uniform(-0.9, 0.9)
        shifted = decode(g, (t[0] + e, t[1], t[2], t[3]))
        assert abs(iou(shifted, g) - (1 - abs(e)) / (1 + abs(e))) < 1e-9
        grown = decode(g, (t[0], t[1], t[2] + e, t[3]))
        assert abs(iou(grown, g) - math.exp(-abs(e))) < 1e-9


def test_clip_caps_growth():
    a = (0.0, 0.0, 16.0, 16.0)
    b = decode(a, (0.0, 0.0, 50.0, 50.0), clip=DEFAULT_CLIP)
    assert abs((b[2] - b[0]) - 1000.0) < 1e-6


def test_smooth_l1_values_and_gradient():
    assert smooth_l1(0.5) == 0.125
    assert smooth_l1(-2.0) == 1.5
    assert smooth_l1(1.0) == 0.5
    for x in [-3.0, -1.2, -0.7, -0.1, 0.0, 0.3, 0.99, 1.5, 4.0]:
        h = 1e-6
        num = (smooth_l1(x + h) - smooth_l1(x - h)) / (2 * h)
        assert abs(num - smooth_l1_grad(x)) < 1e-5
    assert box_loss((0.5, -2.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0)) == 1.625


def test_iou_and_giou_check_values():
    assert iou((0, 0, 2, 2), (1, 1, 3, 3)) == Fraction(1, 7)
    assert iou((0, 0, 10, 10), (5, 0, 15, 10)) == Fraction(1, 3)
    assert giou((0, 0, 2, 2), (1, 1, 3, 3)) == Fraction(-5, 63)
    assert giou((0, 0, 1, 1), (2, 0, 3, 1)) == Fraction(-1, 3)
    rng = random.Random(6)
    for _ in range(200):
        a, b = rand_box(rng), rand_box(rng)
        assert -1.0 < giou(a, b) <= iou(a, b) + 1e-12


def test_ridge_recovers_linear_targets():
    rng = random.Random(7)
    w_true = [0.5, -1.0, 2.0, 0.25]
    feats = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(80)]
    ys = [sum(w * f for w, f in zip(w_true, row)) for row in feats]
    w = fit_ridge(feats, ys, 1e-9)
    assert close(w, w_true, 1e-6)
    # A large lambda shrinks the weights toward zero.
    w_big = fit_ridge(feats, ys, 1e6)
    assert max(abs(v) for v in w_big) < 1e-3
