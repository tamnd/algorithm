# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-bound-propagation/. The authors are listed in prov/2WWJMG.jsonl.

"""Tests of interval bound propagation on seeded synthetic ReLU networks only."""

import itertools
import random

import mlkit as m
from interval_bound_propagation import (
    certify_ibp,
    forward,
    input_box,
    interval_bound_propagation,
    layers_from_net,
    margin_layers,
)

TOL = 1e-9

# The network of the worked example: two inputs, two hidden ReLUs, two logits.
EXAMPLE = [([[2.0, -1.0], [1.0, -2.0]], [0.0, 0.5]), ([[1.0, -1.0], [-2.0, 2.0]], [1.0, 0.0])]


def exact_range(layers, lower, upper):
    """Exact (min, max) of the single output of layers over a 2-dimensional box.

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
        for (r1, c1), (r2, c2v) in itertools.combinations(cons, 2):
            det = r1[0] * r2[1] - r1[1] * r2[0]
            if abs(det) < 1e-12:
                continue
            x0 = (-c1 * r2[1] + r1[1] * c2v) / det
            x1 = (-r1[0] * c2v + c1 * r2[0]) / det
            if all(r[0] * x0 + r[1] * x1 + cc >= -1e-9 for r, cc in cons):
                v = a[0][0] * x0 + a[0][1] * x1 + c[0]
                best_lo = v if best_lo is None else min(best_lo, v)
                best_hi = v if best_hi is None else max(best_hi, v)
    return best_lo, best_hi


def random_layers(rng: random.Random, sizes: list[int]) -> list:
    out = []
    for n_in, n_out in zip(sizes, sizes[1:]):
        out.append(([[rng.uniform(-2, 2) for _ in range(n_in)] for _ in range(n_out)], [rng.uniform(-1, 1) for _ in range(n_out)]))
    return out


def test_example_table():
    lower, upper = input_box([0.5, 0.5], 0.25)
    assert lower == [0.25, 0.25] and upper == [0.75, 0.75]
    l1, u1 = interval_bound_propagation(EXAMPLE[:1], lower, upper)
    assert l1 == [-0.25, -0.75] and u1 == [1.25, 0.75]
    l2, u2 = interval_bound_propagation(EXAMPLE, lower, upper)
    assert l2 == [0.25, -2.5] and u2 == [2.25, 1.5]
    ok, lo = certify_ibp(EXAMPLE, [0.5, 0.5], 0, 0.25)
    assert not ok and abs(lo[0] + 1.25) < TOL
    lo_ex, _ = exact_range(margin_layers(EXAMPLE, 0), lower, upper)
    assert abs(lo_ex - 1.0) < 1e-9
    ok, lo = certify_ibp(EXAMPLE, [0.5, 0.5], 0, 0.1)
    assert ok and abs(lo[0] - 0.7) < TOL


def test_example_radius_is_5_over_36():
    lo, hi = 0.0, 0.5
    for _ in range(60):
        mid = (lo + hi) / 2
        if certify_ibp(EXAMPLE, [0.5, 0.5], 0, mid)[0]:
            lo = mid
        else:
            hi = mid
    assert abs(lo - 5 / 36) < 1e-9


def test_point_box_gives_the_forward_value():
    rng = random.Random(5)
    for _ in range(50):
        layers = random_layers(rng, [3, 4, 2])
        x = [rng.random() for _ in range(3)]
        lo, hi = interval_bound_propagation(layers, x, x)
        z = forward(layers, x)
        assert all(abs(a - b) < TOL and abs(c - b) < TOL for a, b, c in zip(lo, z, hi))


def test_one_affine_layer_is_tight():
    rng = random.Random(6)
    for _ in range(200):
        d = rng.randint(1, 4)
        layers = random_layers(rng, [d, 3])
        lower = [rng.uniform(0, 0.5) for _ in range(d)]
        upper = [a + rng.uniform(0, 0.5) for a in lower]
        lo, hi = interval_bound_propagation(layers, lower, upper)
        corners = [forward(layers, list(c)) for c in itertools.product(*zip(lower, upper))]
        for i in range(3):
            assert abs(lo[i] - min(v[i] for v in corners)) < 1e-9
            assert abs(hi[i] - max(v[i] for v in corners)) < 1e-9


def test_mlkit_network_conversion():
    rng = random.Random(7)
    net = m.tiny_relu_net(rng, 4, 6, 3)
    layers = layers_from_net(net)
    for _ in range(20):
        x = [rng.random() for _ in range(4)]
        assert all(abs(a - b) < 1e-12 for a, b in zip(forward(layers, x), m.forward(net, x)))


def test_sound_against_enumeration_and_sampling():
    rng = random.Random(2018)
    for case in range(500):
        if case % 3 == 2:
            sizes = [2, 2, 2, 2]
        else:
            sizes = [2, rng.randint(1, 4), rng.randint(2, 3)]
        layers = random_layers(rng, sizes)
        x = [rng.random(), rng.random()]
        epsilon = rng.choice([0.0, 0.05, 0.1, 0.2, 0.4])
        y = rng.randrange(sizes[-1])
        lower, upper = input_box(x, epsilon)
        spec = margin_layers(layers, y)
        lo, hi = interval_bound_propagation(spec, lower, upper)
        j = rng.randrange(len(lo))
        one = [*spec[:-1], ([spec[-1][0][j]], [spec[-1][1][j]])]
        ex_lo, ex_hi = exact_range(one, lower, upper)
        assert lo[j] <= ex_lo + 1e-9 and ex_hi <= hi[j] + 1e-9
        for _ in range(30):
            p = [rng.uniform(a, b) for a, b in zip(lower, upper)]
            v = forward(spec, p)
            assert all(l - 1e-9 <= a <= u + 1e-9 for l, a, u in zip(lo, v, hi))
            assert ex_lo - 1e-9 <= v[j] <= ex_hi + 1e-9
        ok, _ = certify_ibp(layers, x, y, epsilon)
        if ok:
            assert ex_lo > 0.0


def test_nested_boxes_give_nested_bounds():
    rng = random.Random(9)
    for _ in range(200):
        layers = random_layers(rng, [3, 4, 3, 2])
        lower = [rng.uniform(0, 0.4) for _ in range(3)]
        upper = [a + rng.uniform(0, 0.4) for a in lower]
        inner_lo = [a + rng.uniform(0, 1) * (b - a) / 2 for a, b in zip(lower, upper)]
        inner_hi = [max(c, b - rng.uniform(0, 1) * (b - a) / 2) for a, b, c in zip(lower, upper, inner_lo)]
        lo, hi = interval_bound_propagation(layers, lower, upper)
        lo2, hi2 = interval_bound_propagation(layers, inner_lo, inner_hi)
        assert all(a <= b + 1e-9 and c <= d + 1e-9 for a, b, c, d in zip(lo, lo2, hi2, hi))


def test_certified_points_have_no_sampled_counterexample():
    rng = random.Random(11)
    net = m.tiny_relu_net(rng, 3, 5, 3)
    layers = layers_from_net(net)
    count = 0
    for _ in range(200):
        x = [rng.random() for _ in range(3)]
        y = m.argmax(m.forward(net, x))
        ok, _ = certify_ibp(layers, x, y, 0.02)
        if ok:
            count += 1
            lower, upper = input_box(x, 0.02)
            for _ in range(20):
                p = [rng.uniform(a, b) for a, b in zip(lower, upper)]
                assert m.argmax(m.forward(net, p)) == y
    assert count > 0
