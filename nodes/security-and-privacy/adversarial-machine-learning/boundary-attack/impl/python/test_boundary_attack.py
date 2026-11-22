# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-attack/. The authors are listed in prov/0K6SWG.jsonl.

"""Tests of the boundary attack, on seeded synthetic models only."""

import math
import random

import mlkit as m
from boundary_attack import boundary_attack, candidate

# The worked example of the page: label 1 when x_1 + x_2 > 0.8, else 0.
XE = [0.5, 0.5]
START = [0.1, 0.1]


def label_e(u):
    return 1 if u[0] + u[1] > 0.8 else 0


def linear_label(w, b):
    return lambda u: 1 if m.dot(w, u) + b > 0 else 0


def test_page_example() -> None:
    dmin = 0.2 / math.sqrt(2)
    adv, queries = boundary_attack(label_e, XE, 1, START, 200, random.Random(1))
    assert label_e(adv) == 0
    assert dmin <= math.dist(adv, XE) <= 1.001 * dmin
    assert queries <= 400
    # the table of the page
    for steps, q, dist in ((10, 20, 0.19724), (20, 39, 0.14251), (50, 82, 0.14251), (100, 157, 0.14167), (200, 295, 0.14144)):
        adv, queries = boundary_attack(label_e, XE, 1, START, steps, random.Random(1))
        assert queries == q and abs(math.dist(adv, XE) - dist) < 1e-5


def test_three_class_example() -> None:
    # the row of the boundary attack in the table of the page evasion-attack
    w = [[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0]]
    lab = lambda u: m.argmax([m.dot(r, u) for r in w])
    x = [0.6, 0.4]
    adv, queries = boundary_attack(lab, x, 0, [0.0, 1.0], 200, random.Random(1))
    assert lab(adv) != 0 and queries == 297
    assert abs(math.dist(adv, x) - 0.14146) < 1e-5


def test_edges() -> None:
    adv, queries = boundary_attack(label_e, XE, 1, START, 0, random.Random(1))
    assert adv == START and queries == 0
    ortho, full = candidate([0.5, 0.5], [0.5, 0.3], [1.0, 0.0], 0.1, 0.5)
    assert abs(math.dist(ortho, [0.5, 0.5]) - 0.2) < 1e-12
    assert abs(math.dist(full, [0.5, 0.5]) - 0.1) < 1e-12


def test_candidates_never_move_away() -> None:
    # The orthogonal candidate keeps the distance D (before the clip) and the full
    # candidate is at (1 - beta) D. The clip is the projection onto a convex set that
    # contains x, so it can only shorten both distances.
    rng = random.Random(7701)
    for _ in range(500):
        d = rng.randint(1, 6)
        x = [rng.uniform(0, 1) for _ in range(d)]
        adv = [rng.uniform(0, 1) for _ in range(d)]
        noise = [rng.gauss(0, 1) for _ in range(d)]
        alpha, beta = rng.uniform(0.01, 1.0), rng.uniform(0.0, 0.9)
        dist = math.dist(adv, x)
        ortho, full = candidate(x, adv, noise, alpha, beta)
        assert math.dist(ortho, x) <= dist + 1e-12
        assert math.dist(full, x) <= (1 - beta) * dist + 1e-12
        assert all(0.0 <= a <= 1.0 for a in ortho + full)


def test_linear_models_approach_the_closed_form_distance() -> None:
    # For label 1 iff w.x + b > 0, no input of label 0 is closer to x than f(x) / ||w||.
    rng = random.Random(7702)
    for trial in range(500):
        d = rng.randint(1, 4)
        w = [rng.choice([-1, 1]) * rng.uniform(0.3, 2.0) for _ in range(d)]
        x = [rng.uniform(0.3, 0.7) for _ in range(d)]
        dmin = rng.uniform(0.05, 0.3)
        b = dmin * m.norm2(w) - m.dot(w, x)
        lab = linear_label(w, b)
        start = [0.0 if wi > 0 else 1.0 for wi in w]
        if lab(start) == 1:
            continue
        adv, queries = boundary_attack(lab, x, 1, start, 120, random.Random(trial))
        assert lab(adv) == 0
        assert all(0.0 <= a <= 1.0 for a in adv)
        assert queries <= 240
        assert dmin - 1e-12 <= math.dist(adv, x) <= math.dist(start, x)
        # a measured bound for these seeds, not a theorem: after 120 steps the worst ratio was below 1.07
        assert math.dist(adv, x) <= 1.1 * dmin


def test_relu_nets_stay_adversarial() -> None:
    rng = random.Random(7703)
    for trial in range(100):
        d, h, k = rng.randint(1, 4), rng.randint(2, 8), rng.randint(2, 4)
        net = m.tiny_relu_net(rng, d, h, k)
        lab = lambda u: m.argmax(m.forward(net, u))
        x = [rng.uniform(0, 1) for _ in range(d)]
        y = lab(x)
        start = None
        for _ in range(50):
            u = [rng.uniform(0, 1) for _ in range(d)]
            if lab(u) != y:
                start = u
                break
        if start is None:
            continue
        adv, queries = boundary_attack(lab, x, y, start, 60, random.Random(trial))
        assert lab(adv) != y
        assert math.dist(adv, x) <= math.dist(start, x) + 1e-12
        assert queries <= 120
