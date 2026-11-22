# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-adversarial-perturbation/. The authors are listed in prov/NQDGS5.jsonl.

"""Tests of the universal perturbation algorithm, on seeded synthetic models only."""

import math
import random

import mlkit as m
from universal_adversarial_perturbation import fooling_rate, minimal_step, project_ball, universal_perturbation

# The worked example of the page: a linear two-class model in the plane and five points.
WE = [1.0, 1.0]
BE = -0.6
DATA = [[0.5, 0.3], [0.4, 0.5], [0.6, 0.5], [0.7, 0.6], [0.5, 0.6]]


def binary(w, b):
    """Two logits: 0 for class 0 and w.x + b for class 1."""
    return (lambda u: [0.0, m.dot(w, u) + b]), (lambda u: [[0.0] * len(w), w])


def test_page_example() -> None:
    lg, jac = binary(WE, BE)
    v, rate = universal_perturbation(lg, jac, DATA, 0.3, norm="2", target_rate=1.0, max_passes=3)
    s = 0.3 / math.sqrt(2)
    assert all(abs(a + s) < 1e-12 for a in v)
    assert rate == 0.4
    v, rate = universal_perturbation(lg, jac, DATA, 0.3, norm="inf", target_rate=1.0, max_passes=3)
    assert all(abs(a + 0.3) < 1e-12 for a in v)
    assert rate == 0.8


def test_page_network_example() -> None:
    # seed 26: one vector fits on 40 points and fools 22 of them, and 116 of 200 new points
    rng = random.Random(26)
    net = m.tiny_relu_net(rng, 4, 8, 3)
    lg = lambda u: m.forward(net, u)
    jac = lambda u: m.logits_jacobian(net, u)
    train = [[rng.uniform(0, 1) for _ in range(4)] for _ in range(40)]
    test = [[rng.uniform(0, 1) for _ in range(4)] for _ in range(200)]
    v, rate = universal_perturbation(lg, jac, train, 0.3, norm="2", target_rate=0.8, max_passes=10)
    assert abs(m.norm2(v) - 0.3) < 1e-9
    assert abs(rate - 0.55) < 1e-12
    assert abs(fooling_rate(lg, test, v) - 0.58) < 1e-12


def test_edges() -> None:
    lg, jac = binary(WE, BE)
    v, rate = universal_perturbation(lg, jac, DATA, 0.0)
    assert v == [0.0, 0.0] and rate == 0.0
    assert fooling_rate(lg, [], [0.0, 0.0]) == 0.0
    assert math.dist(project_ball([3.0, 4.0], 1.0, "2"), [0.6, 0.8]) < 1e-12
    assert project_ball([3.0, -4.0], 1.0, "inf") == [1.0, -1.0]
    # a point already of another label needs no step
    assert minimal_step(lg, jac, [0.1, 0.1], 1) == [0.0, 0.0]


def test_linear_binary_models_reach_the_best_universal_rate() -> None:
    # All points have label 1 and f_i = w.x_i + b > 0. A vector v with ||v||_2 <= epsilon
    # fools x_i exactly when f_i + w.v <= 0, and w.v >= -epsilon ||w||_2, so no v fools more
    # than the points with f_i <= epsilon ||w||_2; the l_infinity bound uses ||w||_1.
    rng = random.Random(7601)
    for _ in range(500):
        d, n = rng.randint(1, 4), rng.randint(1, 12)
        w = [rng.choice([-1, 1]) * rng.uniform(0.2, 2.0) for _ in range(d)]
        data = [[rng.uniform(0.3, 0.7) for _ in range(d)] for _ in range(n)]
        b = -min(m.dot(w, x) for x in data) + rng.uniform(0.01, 0.4)
        eps = rng.uniform(0.0, 0.3)
        f = [m.dot(w, x) + b for x in data]
        lg, jac = binary(w, b)
        for norm, wn in (("2", m.norm2(w)), ("inf", m.norm1(w))):
            if min(abs(fi - eps * wn) for fi in f) < 1e-6:
                continue  # too close to a tie
            best = sum(1 for fi in f if fi <= eps * wn) / n
            v, rate = universal_perturbation(lg, jac, data, eps, norm=norm, target_rate=1.0, max_passes=4)
            assert rate == fooling_rate(lg, data, v)
            assert rate <= best
            size = m.norm2(v) if norm == "2" else m.norminf(v)
            assert size <= eps + 1e-12
            if norm == "2":
                assert rate == best


def test_relu_nets_keep_the_perturbation_in_the_ball() -> None:
    rng = random.Random(7602)
    for _ in range(40):
        d, h, k = rng.randint(1, 4), rng.randint(2, 6), rng.randint(2, 3)
        net = m.tiny_relu_net(rng, d, h, k)
        lg = lambda u: m.forward(net, u)
        jac = lambda u: m.logits_jacobian(net, u)
        data = [[rng.uniform(0, 1) for _ in range(d)] for _ in range(10)]
        eps = rng.uniform(0.05, 0.5)
        norm = rng.choice(["2", "inf"])
        v, rate = universal_perturbation(lg, jac, data, eps, norm=norm, target_rate=0.5, max_passes=3)
        size = m.norm2(v) if norm == "2" else m.norminf(v)
        assert size <= eps + 1e-12
        assert rate == fooling_rate(lg, data, v)
