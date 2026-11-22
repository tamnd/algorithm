# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carlini-wagner-attack/. The authors are listed in prov/2XQ46N.jsonl.

"""Tests of the C&W l2 attack, on seeded synthetic models only."""

import math
import random

import mlkit as m
from carlini_wagner_attack import carlini_wagner_attack, from_box, margin, objective_gradient, to_box

# The worked example of the page: three classes in the plane.
WE = [[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0]]
BE = [0.0, 0.0, 0.0]
XE = [0.6, 0.4]


def linear(w, b):
    return (lambda u: [m.dot(r, u) + bi for r, bi in zip(w, b)]), (lambda u: w)


def min_distance(w, b, x, y):
    """Closed form: the l2 distance from x to the complement of the region of class y of an affine classifier."""
    z = [m.dot(r, x) + bi for r, bi in zip(w, b)]
    return min((z[y] - z[j]) / m.norm2(m.sub(w[y], w[j])) for j in range(len(w)) if j != y)


def test_page_example() -> None:
    lg, jac = linear(WE, BE)
    assert m.argmax(lg(XE)) == 0
    dmin = min_distance(WE, BE, XE, 0)
    assert abs(dmin - 0.2 / math.sqrt(2)) < 1e-12
    out = carlini_wagner_attack(lg, jac, XE, 0, steps=100, lr=0.01, search_steps=8)
    assert out is not None and m.argmax(lg(out)) == 1
    assert dmin <= math.dist(out, XE) <= dmin + 0.005
    # with confidence kappa = 0.1 the output has z_1 - z_0 >= 0.1, so it is at least 0.3 / sqrt(2) away
    out = carlini_wagner_attack(lg, jac, XE, 0, kappa=0.1, steps=100, lr=0.01, search_steps=8)
    assert out is not None and lg(out)[1] - lg(out)[0] >= 0.1
    assert 0.3 / math.sqrt(2) <= math.dist(out, XE) <= 0.3 / math.sqrt(2) + 0.005


def test_change_of_variables_and_margin() -> None:
    for x in ([0.0, 1.0, 0.5], [0.25, 0.75, 0.999]):
        back = to_box(from_box(x))
        assert all(abs(a - b) < 1e-8 for a, b in zip(back, x))
    assert margin([3.0, 1.0, 2.0], 0, 0.0) == (1.0, 2)
    assert margin([1.0, 3.0, 2.0], 0, 0.5) == (-0.5, 1)


def test_objective_gradient_matches_finite_differences() -> None:
    rng = random.Random(7301)
    checked = 0
    for _ in range(500):
        d, h, k = rng.randint(1, 4), rng.randint(2, 6), rng.randint(2, 4)
        net = m.tiny_relu_net(rng, d, h, k)
        lg = lambda u: m.forward(net, u)
        jac = lambda u: m.logits_jacobian(net, u)
        x = [rng.uniform(0.1, 0.9) for _ in range(d)]
        y = m.argmax(lg(x))
        w = [a + rng.uniform(-0.3, 0.3) for a in from_box(x)]
        c = rng.uniform(0.1, 5.0)
        kappa = rng.choice([0.0, 0.5])
        xp = to_box(w)
        pre = [m.dot(r, xp) + bi for r, bi in zip(net["W1"], net["b1"])]
        z = lg(xp)
        gaps = sorted(z, reverse=True)
        f, _ = margin(z, y, kappa)
        if min(abs(a) for a in pre) < 1e-3 or gaps[0] - gaps[1] < 1e-3 or abs(f + kappa) < 1e-3:
            continue  # too close to a kink for a finite difference
        _, g = objective_gradient(lg, jac, x, w, y, c, kappa)
        for i in range(d):
            up, dn = list(w), list(w)
            up[i] += 1e-6
            dn[i] -= 1e-6
            fd = (objective_gradient(lg, jac, x, up, y, c, kappa)[0] - objective_gradient(lg, jac, x, dn, y, c, kappa)[0]) / 2e-6
            assert abs(fd - g[i]) < 1e-5
        checked += 1
    assert checked > 300


def test_binary_linear_models_against_closed_form() -> None:
    # With two classes the objective is convex in x', and the true minimum is the
    # distance |z_0 - z_1| / ||w_0 - w_1|| to the hyperplane (inside the box here).
    rng = random.Random(7302)
    for _ in range(300):
        d = rng.randint(1, 4)
        w = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(2)]
        x = [rng.uniform(0.4, 0.6) for _ in range(d)]
        target = rng.uniform(0.02, 0.3)
        diff = m.sub(w[0], w[1])
        if m.norm2(diff) < 0.2:
            continue
        b = [target * m.norm2(diff) - m.dot(diff, x), 0.0]  # z_0 - z_1 = target ||w_0 - w_1||
        lg, jac = linear(w, b)
        dmin = min_distance(w, b, x, 0)
        assert abs(dmin - target) < 1e-9
        out = carlini_wagner_attack(lg, jac, x, 0, steps=40, lr=0.04, search_steps=5)
        assert out is not None
        assert m.argmax(lg(out)) == 1
        assert all(0.0 < a < 1.0 for a in out)
        assert dmin - 1e-12 <= math.dist(out, x) <= dmin + 0.01


def test_multiclass_linear_models_respect_the_lower_bound() -> None:
    # With more classes the margin loss is not convex, and the attack may stop at a
    # boundary that is not the nearest one. Any output is still at least the minimum away.
    rng = random.Random(7303)
    found = 0
    for _ in range(500):
        d, k = rng.randint(1, 3), rng.randint(3, 4)
        w = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(k)]
        b = [rng.uniform(-0.5, 0.5) for _ in range(k)]
        x = [rng.uniform(0.3, 0.7) for _ in range(d)]
        lg, jac = linear(w, b)
        y = m.argmax(lg(x))
        out = carlini_wagner_attack(lg, jac, x, y, steps=25, lr=0.05, search_steps=3)
        if out is not None:
            found += 1
            assert m.argmax(lg(out)) != y
            assert math.dist(out, x) >= min_distance(w, b, x, y) - 1e-12
            assert all(0.0 < a < 1.0 for a in out)
    assert found > 300


def test_relu_nets_outputs_are_adversarial_and_in_the_box() -> None:
    rng = random.Random(7304)
    found = 0
    for _ in range(60):
        d, h, k = rng.randint(1, 4), rng.randint(2, 8), rng.randint(2, 3)
        net = m.tiny_relu_net(rng, d, h, k)
        lg = lambda u: m.forward(net, u)
        jac = lambda u: m.logits_jacobian(net, u)
        x = [rng.uniform(0, 1) for _ in range(d)]
        y = m.argmax(lg(x))
        out = carlini_wagner_attack(lg, jac, x, y, steps=40, lr=0.05, search_steps=4)
        if out is not None:
            found += 1
            assert m.argmax(lg(out)) != y
            assert all(0.0 < a < 1.0 for a in out)
    assert found > 0
