# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pgd-attack/. The authors are listed in prov/YAKX8W.jsonl.

"""Tests of the PGD attack, on seeded synthetic models only."""

import itertools
import math
import random

import mlkit as m
from pgd_attack import ascent_direction, pgd_attack, project, random_start

TOL = 1e-9
W = [1.5, -2.0, 0.5, 1.0, -0.5, 3.0]
B = 1.0
X = [0.2, 0.9, 0.5, 0.0, 1.0, 0.4]


def logistic(w, b):
    return (lambda u, t: m.grad_x_logistic(w, b, u, t)), (lambda u, t: m.logistic_loss(w, b, u, t))


def feasible(xa, x, eps, norm) -> bool:
    dist = m.norminf(m.sub(xa, x)) if norm == "inf" else m.norm2(m.sub(xa, x))
    return dist <= eps + TOL and all(-TOL <= a <= 1 + TOL for a in xa)


def test_page_example() -> None:
    g, f = logistic(W, B)
    xa = pgd_attack(g, f, X, 1, 0.1, 0.025, 10)
    assert all(abs(a - e) < TOL for a, e in zip(xa, [0.1, 1.0, 0.4, 0.0, 1.0, 0.3]))
    assert abs(m.dot(W, xa) + B + 0.25) < TOL
    # after 2 steps of 0.025 each moved coordinate is 0.05 from x
    x2 = pgd_attack(g, f, X, 1, 0.1, 0.025, 2)
    assert all(abs(a - e) < TOL for a, e in zip(x2, [0.15, 0.95, 0.45, 0.0, 1.0, 0.35]))


def test_page_network_example() -> None:
    # the seeded network of the page: FGSM keeps label 0, PGD reaches label 1 at step 7
    net = m.tiny_relu_net(random.Random(2744), 2, 4, 2)
    g = lambda u, t: m.input_gradient(net, u, t)
    f = lambda u, t: m.cross_entropy(m.forward(net, u), t)
    x = [0.63, 0.46]
    one = pgd_attack(g, f, x, 0, 0.1, 0.1, 1)
    assert all(abs(a - e) < TOL for a, e in zip(one, [0.53, 0.36]))
    assert m.argmax(m.forward(net, one)) == 0
    xa = pgd_attack(g, f, x, 0, 0.1, 0.025, 10)
    assert all(abs(a - e) < TOL for a, e in zip(xa, [0.73, 0.36]))
    assert m.argmax(m.forward(net, xa)) == 1
    assert m.argmax(m.forward(net, pgd_attack(g, f, x, 0, 0.1, 0.025, 6))) == 0
    assert m.argmax(m.forward(net, pgd_attack(g, f, x, 0, 0.1, 0.025, 7))) == 1


def test_edges() -> None:
    g, f = logistic(W, B)
    assert pgd_attack(g, f, X, 1, 0.1, 0.025, 0) == X
    assert pgd_attack(g, f, X, 1, 0.0, 0.025, 5) == X
    assert project([2.0, -1.0], [0.5, 0.5], 0.25, "inf") == [0.75, 0.25]
    assert project([0.5, 0.5], [0.5, 0.5], 0.25, "2") == [0.5, 0.5]
    assert ascent_direction([0.0, 0.0], "2") == [0.0, 0.0]


def test_one_step_from_x_is_fgsm() -> None:
    rng = random.Random(7201)
    for _ in range(500):
        d, h, k = rng.randint(1, 5), rng.randint(2, 8), rng.randint(2, 4)
        net = m.tiny_relu_net(rng, d, h, k)
        x = [rng.uniform(0, 1) for _ in range(d)]
        y = rng.randrange(k)
        eps = rng.uniform(0, 0.4)
        g = lambda u, t: m.input_gradient(net, u, t)
        f = lambda u, t: m.cross_entropy(m.forward(net, u), t)
        gx = g(x, y)
        fgsm = [min(max(a + eps * (1 if s > 0 else -1 if s < 0 else 0), 0.0), 1.0) for a, s in zip(x, gx)]
        one = pgd_attack(g, f, x, y, eps, eps, 1)
        if f(fgsm, y) > f(x, y):
            assert all(abs(a - b) < TOL for a, b in zip(one, fgsm))
        assert f(one, y) >= f(x, y) - TOL


def test_linear_model_reaches_the_vertex_optimum_from_a_random_start() -> None:
    # For a linear model the loss is convex in x, so its maximum over the box
    # B_inf(x, eps) cap [0, 1]^d is at a vertex; enumerate the 2^d vertices.
    rng = random.Random(7202)
    for _ in range(500):
        d = rng.randint(1, 4)
        w = [rng.choice([-1, 1]) * rng.uniform(0.1, 3) for _ in range(d)]
        b = rng.uniform(-1, 1)
        x = [rng.choice([0.0, 1.0, rng.uniform(0, 1)]) for _ in range(d)]
        y = rng.randint(0, 1)
        eps = rng.uniform(0.01, 0.5)
        alpha = eps / 4
        g, f = logistic(w, b)
        xa = pgd_attack(g, f, x, y, eps, alpha, 9, "inf", rng)
        assert feasible(xa, x, eps, "inf")
        lo = [max(a - eps, 0.0) for a in x]
        hi = [min(a + eps, 1.0) for a in x]
        best = max(f(list(v), y) for v in itertools.product(*zip(lo, hi)))
        assert abs(f(xa, y) - best) < 1e-9


def test_l2_linear_model_reaches_the_closed_form() -> None:
    # Inside the box, the l2 maximum of a loss that grows along g is x + eps g / ||g||.
    rng = random.Random(7203)
    for _ in range(500):
        d = rng.randint(1, 6)
        w = [rng.uniform(-2, 2) for _ in range(d)]
        b = rng.uniform(-1, 1)
        x = [rng.uniform(0.35, 0.65) for _ in range(d)]
        y = rng.randint(0, 1)
        eps = rng.uniform(0.01, 0.3)
        g, f = logistic(w, b)
        xa = pgd_attack(g, f, x, y, eps, eps / 3, 5, "2")
        assert feasible(xa, x, eps, "2")
        gx = g(x, y)
        target = m.add(x, m.scale(eps / m.norm2(gx), gx))
        assert m.norm2(m.sub(xa, target)) < 1e-9


def test_iterates_stay_feasible_on_relu_nets() -> None:
    rng = random.Random(7204)
    for _ in range(500):
        d, h, k = rng.randint(1, 4), rng.randint(2, 8), rng.randint(2, 3)
        net = m.tiny_relu_net(rng, d, h, k)
        x = [rng.uniform(0, 1) for _ in range(d)]
        y = rng.randrange(k)
        eps = rng.uniform(0, 0.3)
        norm = rng.choice(["inf", "2"])
        g = lambda u, t: m.input_gradient(net, u, t)
        f = lambda u, t: m.cross_entropy(m.forward(net, u), t)
        start = random_start(random.Random(rng.random()), x, eps, norm)
        assert feasible(start, x, eps, norm)
        xa = pgd_attack(g, f, x, y, eps, eps / 4, 6, norm, rng)
        assert feasible(xa, x, eps, norm)


def test_l2_random_start_is_inside_the_ball() -> None:
    rng = random.Random(7205)
    radii = []
    for _ in range(2000):
        u = random_start(rng, [0.5, 0.5], 0.2, "2")
        radii.append(math.dist(u, [0.5, 0.5]))
    assert max(radii) <= 0.2 + TOL
    # uniform in a disc: P(r <= 0.1) = 1/4; 2000 draws give a standard error of about 0.01
    frac = sum(r <= 0.1 for r in radii) / len(radii)
    assert abs(frac - 0.25) < 0.05
