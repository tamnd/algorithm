# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deepfool/. The authors are listed in prov/A515G9.jsonl.

"""Tests of DeepFool, on seeded synthetic models only."""

import math
import random

import mlkit as m
from deepfool import deepfool, nearest_boundary_step

WE = [[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0]]
BE = [0.0, 0.0, 0.0]
XE = [0.6, 0.4]


def affine(w, b):
    return (lambda u: [m.dot(r, u) + bi for r, bi in zip(w, b)]), (lambda u: w)


def min_distance(w, b, x):
    """Brute force over all classes: l2 distance from x to the complement of its region."""
    z = [m.dot(r, x) + bi for r, bi in zip(w, b)]
    y = m.argmax(z)
    return min((z[y] - z[j]) / m.norm2(m.sub(w[y], w[j])) for j in range(len(w)) if j != y)


def test_page_example() -> None:
    lg, jac = affine(WE, BE)
    p, it = deepfool(lg, jac, XE)
    assert it == 1
    assert m.argmax(lg(p)) == 1
    step = nearest_boundary_step(lg(XE), jac(XE), 0)
    assert all(abs(a - e) < 1e-9 for a, e in zip(step, [-0.1, 0.1]))
    assert abs(math.dist(p, XE) - 1.02 * 0.2 / math.sqrt(2)) < 1e-9


def test_page_network_examples() -> None:
    # seed 3: two iterations, label 1, distance 0.41925
    net = m.tiny_relu_net(random.Random(3), 2, 4, 3)
    lg = lambda u: m.forward(net, u)
    jac = lambda u: m.logits_jacobian(net, u)
    x = [0.5, 0.5]
    assert m.argmax(lg(x)) == 0
    p, it = deepfool(lg, jac, x)
    assert it == 2 and m.argmax(lg(p)) == 1
    assert all(abs(a - e) < 1e-4 for a, e in zip(p, [0.5891, 0.0903]))
    assert abs(math.dist(p, x) - 0.41925) < 1e-4
    # seed 131: the clip at the box makes the loop creep for 20 iterations
    net = m.tiny_relu_net(random.Random(131), 2, 4, 3)
    p, it = deepfool(lg, jac, x)
    assert it == 20 and m.argmax(lg(p)) != m.argmax(lg(x))
    assert abs(math.dist(p, x) - 0.551) < 1e-3


def test_edges() -> None:
    lg, jac = affine([[1.0, 0.0], [1.0, 0.0]], [1.0, 0.0])
    # equal gradients: no boundary can be reached by a linear step, so the input stays
    p, it = deepfool(lg, jac, [0.5, 0.5], max_iter=3)
    assert p == [0.5, 0.5] and it == 3
    lg, jac = affine(WE, BE)
    p, it = deepfool(lg, jac, XE, max_iter=0)
    assert p == XE and it == 0


def test_binary_affine_step_is_the_closed_form() -> None:
    # For f(x) = w.x + b the step is -(f(x) / ||w||^2) w, the projection onto the hyperplane.
    rng = random.Random(7401)
    for _ in range(500):
        d = rng.randint(1, 8)
        w = [rng.uniform(-2, 2) for _ in range(d)]
        b = rng.uniform(-1, 1)
        x = [rng.uniform(0, 1) for _ in range(d)]
        f = m.dot(w, x) + b
        z = [0.0, f]  # class 1 has logit f, class 0 has logit 0, so z_1 - z_0 = f
        jz = [[0.0] * d, w]
        k0 = 1 if f > 0 else 0
        step = nearest_boundary_step(z, jz, k0)
        target = m.scale(-f / m.dot(w, w), w)
        assert m.norm2(m.sub(step, target)) < 1e-9 * (1 + m.norm2(target))
        assert abs(m.dot(w, m.add(x, step)) + b) < 1e-9


def test_affine_multiclass_one_iteration_and_minimal() -> None:
    rng = random.Random(7402)
    for _ in range(500):
        d, k = rng.randint(1, 4), rng.randint(2, 5)
        w = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(k)]
        b = [rng.uniform(-0.3, 0.3) for _ in range(k)]
        x = [rng.uniform(0.3, 0.7) for _ in range(d)]
        lg, jac = affine(w, b)
        dmin = min_distance(w, b, x)
        if dmin > 0.25:
            continue  # keep the boundary point inside the box
        p, it = deepfool(lg, jac, x)
        assert it == 1
        assert m.argmax(lg(p)) != m.argmax(lg(x))
        assert abs(math.dist(p, x) - 1.02 * dmin) < 1e-9


def test_relu_nets_label_changes_and_box() -> None:
    rng = random.Random(7403)
    done = 0
    for _ in range(500):
        d, h, k = rng.randint(1, 4), rng.randint(2, 8), rng.randint(2, 4)
        net = m.tiny_relu_net(rng, d, h, k)
        lg = lambda u: m.forward(net, u)
        jac = lambda u: m.logits_jacobian(net, u)
        x = [rng.uniform(0, 1) for _ in range(d)]
        p, it = deepfool(lg, jac, x, max_iter=20)
        assert all(0.0 <= a <= 1.0 for a in p)
        if it < 20:
            done += 1
            assert m.argmax(lg(p)) != m.argmax(lg(x))
    # Some seeded nets keep one label over the whole box, so the loop cannot always stop early.
    assert done > 200
