# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-bound-propagation/. The authors are listed in prov/2XBS61.jsonl.

"""Tests of linear bound propagation (CROWN) on seeded synthetic ReLU networks only."""

import itertools
import random

import mlkit as m
from linear_bound_propagation import (
    backward_bound,
    certify_crown,
    forward,
    layers_from_net,
    linear_bound_propagation,
    margin_spec,
    relaxation,
)

TOL = 1e-9

# The network of the worked example: two inputs, two hidden ReLUs, two logits.
EXAMPLE = [([[2.0, -1.0], [1.0, -2.0]], [0.0, 0.5]), ([[1.0, -1.0], [-2.0, 2.0]], [1.0, 0.0])]


def box(x, epsilon):
    return [max(a - epsilon, 0.0) for a in x], [min(a + epsilon, 1.0) for a in x]


def exact_range(layers, lower, upper, row):
    """Exact (min, max) of row times the output of layers over a 2-dimensional box.

    The oracle enumerates every activation pattern of the hidden units. On the region
    of one pattern the network is affine, so its extremes over the region are at
    vertices; each vertex is the meet of two constraint lines, solved by Cramer's rule.
    """
    d = len(lower)
    assert d == 2
    sizes = [len(w) for w, _ in layers[:-1]]
    best_lo, best_hi = None, None
    for pat in itertools.product([0, 1], repeat=sum(sizes)):
        cons = [([1.0, 0.0], -lower[0]), ([-1.0, 0.0], upper[0]), ([0.0, 1.0], -lower[1]), ([0.0, -1.0], upper[1])]
        a = [[1.0, 0.0], [0.0, 1.0]]
        c = [0.0, 0.0]
        p = 0
        for k, (w, b) in enumerate(layers):
            a2 = [[sum(w[i][t] * a[t][j] for t in range(len(a))) for j in range(d)] for i in range(len(w))]
            c2 = [sum(w[i][t] * c[t] for t in range(len(c))) + b[i] for i in range(len(w))]
            if k < len(layers) - 1:
                for i in range(len(w)):
                    if pat[p]:
                        cons.append((a2[i], c2[i]))
                    else:
                        cons.append(([-v for v in a2[i]], -c2[i]))
                        a2[i], c2[i] = [0.0] * d, 0.0
                    p += 1
            a, c = a2, c2
        g = [sum(row[i] * a[i][j] for i in range(len(row))) for j in range(d)]
        g0 = sum(row[i] * c[i] for i in range(len(row)))
        for (r1, c1), (r2, c2v) in itertools.combinations(cons, 2):
            det = r1[0] * r2[1] - r1[1] * r2[0]
            if abs(det) < 1e-12:
                continue
            x0 = (-c1 * r2[1] + r1[1] * c2v) / det
            x1 = (-r1[0] * c2v + c1 * r2[0]) / det
            if all(r[0] * x0 + r[1] * x1 + cc >= -1e-9 for r, cc in cons):
                v = g[0] * x0 + g[1] * x1 + g0
                best_lo = v if best_lo is None else min(best_lo, v)
                best_hi = v if best_hi is None else max(best_hi, v)
    return best_lo, best_hi


def random_layers(rng: random.Random, sizes: list[int]) -> list:
    out = []
    for n_in, n_out in zip(sizes, sizes[1:]):
        out.append(([[rng.uniform(-2, 2) for _ in range(n_in)] for _ in range(n_out)], [rng.uniform(-1, 1) for _ in range(n_out)]))
    return out


def test_example():
    ok, lo = certify_crown(EXAMPLE, [0.5, 0.5], 0, 0.25)
    assert ok and abs(lo[0] - 0.25) < TOL
    ok, lo = certify_crown(EXAMPLE, [0.5, 0.5], 0, 0.1)
    assert ok and abs(lo[0] - 1.6) < TOL
    lower, upper = box([0.5, 0.5], 0.25)
    assert exact_range(EXAMPLE, lower, upper, [1.0, -1.0])[0] == 1.0
    assert relaxation(-0.25, 1.25) == (1.25 / 1.5, 1.25 / 1.5 * 0.25, 1.0, 0.0)
    assert relaxation(-0.75, 0.75) == (0.5, 0.375, 1.0, 0.0)


def test_example_radius_is_5_over_18():
    lo, hi = 0.0, 0.5
    for _ in range(60):
        mid = (lo + hi) / 2
        if certify_crown(EXAMPLE, [0.5, 0.5], 0, mid)[0]:
            lo = mid
        else:
            hi = mid
    assert abs(lo - 5 / 18) < 1e-9


def test_relaxation_is_sound():
    rng = random.Random(1)
    for _ in range(500):
        l = rng.uniform(-2, 2)
        u = l + rng.uniform(0, 3)
        su, iu, sl, il = relaxation(l, u)
        for t in range(21):
            z = l + (u - l) * t / 20
            assert sl * z + il <= max(z, 0.0) + 1e-12 <= su * z + iu + 2e-12


def test_first_layer_bounds_are_the_exact_intervals():
    rng = random.Random(2)
    for _ in range(200):
        d = rng.randint(1, 4)
        layers = random_layers(rng, [d, 3])
        lower = [rng.uniform(0, 0.5) for _ in range(d)]
        upper = [a + rng.uniform(0, 0.5) for a in lower]
        eye = [[1.0 if i == t else 0.0 for t in range(3)] for i in range(3)]
        lo = backward_bound(layers, 0, eye, [], lower, upper)
        corners = [forward(layers, list(c)) for c in itertools.product(*zip(lower, upper))]
        for i in range(3):
            assert abs(lo[i] - min(v[i] for v in corners)) < 1e-9


def test_point_box_is_exact():
    rng = random.Random(3)
    for _ in range(100):
        layers = random_layers(rng, [3, 4, 3, 2])
        x = [rng.random() for _ in range(3)]
        lo = linear_bound_propagation(layers, x, x, [[1.0, -1.0], [-1.0, 1.0]])
        z = forward(layers, x)
        assert abs(lo[0] - (z[0] - z[1])) < 1e-9 and abs(lo[1] - (z[1] - z[0])) < 1e-9


def test_mlkit_network_conversion():
    rng = random.Random(4)
    net = m.tiny_relu_net(rng, 4, 6, 3)
    layers = layers_from_net(net)
    for _ in range(20):
        x = [rng.random() for _ in range(4)]
        assert all(abs(a - b) < 1e-12 for a, b in zip(forward(layers, x), m.forward(net, x)))


def test_sound_against_enumeration_and_sampling():
    rng = random.Random(2018)
    stable_exact = 0
    for case in range(500):
        if case % 3 == 2:
            sizes = [2, 2, 2, 2]
        else:
            sizes = [2, rng.randint(1, 4), rng.randint(2, 3)]
        layers = random_layers(rng, sizes)
        x = [rng.random(), rng.random()]
        epsilon = rng.choice([0.0, 0.05, 0.1, 0.2, 0.4])
        y = rng.randrange(sizes[-1])
        lower, upper = box(x, epsilon)
        spec = margin_spec(sizes[-1], y)
        lo = linear_bound_propagation(layers, lower, upper, spec)
        j = rng.randrange(len(spec))
        ex_lo, ex_hi = exact_range(layers, lower, upper, spec[j])
        assert lo[j] <= ex_lo + 1e-9
        hi = -linear_bound_propagation(layers, lower, upper, [[-v for v in spec[j]]])[0]
        assert ex_hi <= hi + 1e-9
        for _ in range(30):
            p = [rng.uniform(a, b) for a, b in zip(lower, upper)]
            z = forward(layers, p)
            margins = [sum(s * v for s, v in zip(row, z)) for row in spec]
            assert all(a - 1e-9 <= b for a, b in zip(lo, margins))
        if len(sizes) == 3:
            eye = [[1.0 if i == t else 0.0 for t in range(sizes[1])] for i in range(sizes[1])]
            l1 = backward_bound(layers, 0, eye, [], lower, upper)
            u1 = [-v for v in backward_bound(layers, 0, [[-v for v in r] for r in eye], [], lower, upper)]
            if all(a >= 0.0 or b <= 0.0 for a, b in zip(l1, u1)):
                stable_exact += 1
                assert abs(lo[j] - ex_lo) < 1e-7
        ok, _ = certify_crown(layers, x, y, epsilon)
        if ok:
            assert min(exact_range(layers, lower, upper, row)[0] for row in spec) > 0.0
    assert stable_exact > 50


def test_certified_points_have_no_sampled_counterexample():
    rng = random.Random(11)
    net = m.tiny_relu_net(rng, 3, 5, 3)
    layers = layers_from_net(net)
    count = 0
    for _ in range(200):
        x = [rng.random() for _ in range(3)]
        y = m.argmax(m.forward(net, x))
        ok, _ = certify_crown(layers, x, y, 0.05)
        if ok:
            count += 1
            lower, upper = box(x, 0.05)
            for _ in range(20):
                p = [rng.uniform(a, b) for a, b in zip(lower, upper)]
                assert m.argmax(m.forward(net, p)) == y
    assert count > 0
