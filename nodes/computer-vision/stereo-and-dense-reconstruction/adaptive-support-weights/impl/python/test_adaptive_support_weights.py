# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-support-weights/. The authors are listed in prov/WDQMCM.jsonl.

import math
import random

import pytest

from adaptive_support_weights import (
    asw_cost_brute,
    asw_disparity,
    rgb_to_lab,
    support_weights,
)


def random_rgb(rng, w, h, lo=0, hi=255):
    return [[tuple(rng.randint(lo, hi) for _ in range(3)) for _ in range(w)] for _ in range(h)]


def wta_brute(left, right, D, r, gc, gp, T):
    h, w = len(left), len(left[0])
    out = []
    for v in range(h):
        row = []
        for u in range(w):
            costs = [asw_cost_brute(left, right, u, v, d, r, gc, gp, T) for d in range(min(D - 1, u) + 1)]
            row.append(costs.index(min(costs)))
        out.append(row)
    return out


def two_layer_scene(rng, w, h, box, d_back, d_front):
    """A bluish background at disparity d_back and a reddish square, the
    columns x0..x1 - 1 and rows y0..y1 - 1 of the left image, at d_front."""
    x0, x1, y0, y1 = box

    def inside(u, v):
        return y0 <= v < y1 and x0 <= u < x1

    def back():
        g = rng.randint(40, 120)
        return (g // 2, g // 2 + rng.randint(0, 20), g + rng.randint(0, 40))

    def front():
        g = rng.randint(120, 230)
        return (g, g // 3 + rng.randint(0, 30), g // 4)

    B = [[back() for _ in range(w + 10)] for _ in range(h)]
    F = [[front() for _ in range(w + 10)] for _ in range(h)]
    left = [[F[v][u] if inside(u, v) else B[v][u] for u in range(w)] for v in range(h)]
    right = [[F[v][x + d_front] if inside(x + d_front, v) else B[v][x + d_back] for x in range(w)]
             for v in range(h)]
    truth = [[d_front if inside(u, v) else d_back for u in range(w)] for v in range(h)]
    return left, right, truth


def test_lab_reference_colors():
    L, a, b = rgb_to_lab((255, 255, 255))
    assert L == pytest.approx(100.0, abs=0.05) and abs(a) < 0.05 and abs(b) < 0.05
    assert rgb_to_lab((0, 0, 0)) == pytest.approx((0.0, 0.0, 0.0), abs=1e-9)
    L, a, b = rgb_to_lab((128, 128, 128))
    assert abs(a) < 0.05 and abs(b) < 0.05
    # red has a large positive a
    assert rgb_to_lab((200, 30, 30))[1] > 50


def test_worked_example_weights():
    lab = [[rgb_to_lab(c) for c in [(200, 30, 30), (200, 30, 30), (30, 30, 200)]]]
    wts = support_weights(lab, 0, 0, 1, 5.0, 17.5)
    # offsets in row-major order; the middle row is index 3, 4, 5
    assert wts[4] == pytest.approx(1.0)
    assert wts[5] == pytest.approx(math.exp(-1 / 17.5))
    assert wts[3] is None and wts[0] is None
    wts = support_weights(lab, 1, 0, 1, 5.0, 17.5)
    assert wts[5] < 1e-11


def test_weights_are_symmetric():
    rng = random.Random(1)
    img = random_rgb(rng, 6, 5)
    lab = [[rgb_to_lab(c) for c in row] for row in img]
    r = 2
    for v in range(5):
        for u in range(6):
            wp = support_weights(lab, u, v, r, 7.0, 9.0)
            k = 0
            for dv in range(-r, r + 1):
                for du in range(-r, r + 1):
                    if wp[k] is not None:
                        wq = support_weights(lab, u + du, v + dv, r, 7.0, 9.0)
                        back = (r - dv) * (2 * r + 1) + (r - du)
                        assert wq[back] == pytest.approx(wp[k], rel=1e-12)
                    k += 1


def test_matches_brute_force():
    rng = random.Random(2)
    left, right = random_rgb(rng, 9, 6), random_rgb(rng, 9, 6)
    for r, gc, gp, T in ((1, 5.0, 17.5, 40.0), (2, 10.0, 3.0, 100.0), (0, 5.0, 17.5, 40.0)):
        assert asw_disparity(left, right, 4, r, gc, gp, T) == wta_brute(left, right, 4, r, gc, gp, T)


def test_uniform_weights_give_the_box_mean():
    rng = random.Random(3)
    left, right = random_rgb(rng, 8, 6), random_rgb(rng, 8, 6)
    r, T = 1, 60.0
    for u, v, d in ((4, 3, 2), (1, 0, 1), (7, 5, 3)):
        terms = []
        for dv in range(-r, r + 1):
            for du in range(-r, r + 1):
                x, y = u + du, v + dv
                if 0 <= y < 6 and 0 <= x < 8 and 0 <= x - d < 8:
                    terms.append(min(sum(abs(p - q) for p, q in zip(left[y][x], right[y][x - d])), T))
        mean = sum(terms) / len(terms)
        assert asw_cost_brute(left, right, u, v, d, r, 1e12, 1e12, T) == pytest.approx(mean, rel=1e-9)


def test_recovers_a_constant_disparity():
    rng = random.Random(4)
    w, h, D, true_d = 24, 10, 7, 4
    scene = random_rgb(rng, w + 10, h)
    right = [[scene[v][x + true_d] for x in range(w)] for v in range(h)]
    left = [[scene[v][u] for u in range(w)] for v in range(h)]
    disp = asw_disparity(left, right, D, r=3)
    for v in range(h):
        for u in range(true_d, w):
            assert disp[v][u] == true_d


def test_keeps_depth_edges_better_than_a_box():
    rng = random.Random(4)
    w, h, D, r = 32, 20, 9, 4
    box = (14, 24, 6, 14)
    left, right, truth = two_layer_scene(rng, w, h, box, 2, 7)
    asw = asw_disparity(left, right, D, r)
    flat = asw_disparity(left, right, D, r, gamma_c=1e9, gamma_p=1e9)
    x0, x1, y0, y1 = box

    def near_edge(u, v):
        band = y0 - r <= v < y1 + r and x0 - r <= u < x1 + r
        core = y0 + r <= v < y1 - r and x0 + r <= u < x1 - r
        hidden = y0 <= v < y1 and x0 - 5 <= u < x0  # no true match
        return band and not core and not hidden

    def errors(m):
        return sum(m[v][u] != truth[v][u] for v in range(h) for u in range(D + r, w) if near_edge(u, v))

    assert errors(asw) == 0
    assert errors(flat) >= 10


def test_bad_arguments():
    img = [[(0, 0, 0)] * 3]
    with pytest.raises(ValueError):
        asw_disparity(img, img, 0)
    with pytest.raises(ValueError):
        asw_disparity(img, img, 2, r=-1)
