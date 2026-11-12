# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/denclue/. The authors are listed in prov/HSSEG3.jsonl.

import math
import random

import pytest

from denclue import (NOISE, climb_fixed_point, climb_fixed_step, denclue, density, gradient,
                     segment_above)


def mixture_1d(rng, n):
    centers = rng.sample([0.0, 3.0, 6.0, 10.0], rng.randrange(1, 4))
    return [(rng.gauss(rng.choice(centers), rng.uniform(0.3, 0.8)),) for _ in range(n)]


def grid_mode(x0, pts, sigma, step=0.001):
    """Walk on a fine grid to the higher neighbor until none is higher."""
    x = round(x0 / step) * step
    while True:
        here = density((x,), pts, sigma)
        up, down = density((x + step,), pts, sigma), density((x - step,), pts, sigma)
        if up > here and up >= down:
            x += step
        elif down > here:
            x -= step
        else:
            return x


def near_a_minimum(x, pts, sigma, radius):
    xs = [x + radius * k / 20 for k in range(-20, 21)]
    fs = [density((v,), pts, sigma) for v in xs]
    return any(fs[i] <= fs[i - 1] and fs[i] <= fs[i + 1] for i in range(1, len(fs) - 1))


def test_gradient_matches_finite_differences():
    rng = random.Random(1)
    for _ in range(30):
        pts = [(rng.gauss(0, 2), rng.gauss(0, 2)) for _ in range(rng.randrange(1, 12))]
        sigma = rng.uniform(0.5, 2)
        x = (rng.uniform(-3, 3), rng.uniform(-3, 3))
        g = gradient(x, pts, sigma)
        e = 1e-6
        for k in range(2):
            up = tuple(x[i] + (e if i == k else 0) for i in range(2))
            down = tuple(x[i] - (e if i == k else 0) for i in range(2))
            fd = (density(up, pts, sigma) - density(down, pts, sigma)) / (2 * e)
            assert abs(g[k] / sigma ** 2 - fd) < 1e-5 * (1 + abs(fd))


def test_fixed_step_climb_rises_and_stops_correctly():
    rng = random.Random(2)
    for _ in range(30):
        pts = [(rng.gauss(0, 2), rng.gauss(0, 2)) for _ in range(rng.randrange(1, 15))]
        sigma, delta = rng.uniform(0.5, 2), rng.uniform(0.02, 0.3)
        trace = []
        x, fx = climb_fixed_step(pts[0], pts, sigma, delta, trace=trace)
        values = [density(y, pts, sigma) for y in trace]
        assert all(b >= a for a, b in zip(values, values[1:]))
        assert all(abs(math.dist(a, b) - delta) < 1e-9 for a, b in zip(trace, trace[1:]))
        assert abs(fx - density(x, pts, sigma)) < 1e-12
        g = gradient(x, pts, sigma)
        norm = math.sqrt(sum(v * v for v in g))
        if norm > 0:
            nxt = tuple(a + delta * v / norm for a, v in zip(x, g))
            assert density(nxt, pts, sigma) < fx


def test_attractors_are_near_the_modes_in_1d():
    rng = random.Random(3)
    checked = 0
    for _ in range(10):
        pts = mixture_1d(rng, rng.randrange(3, 20))
        sigma, delta = rng.uniform(0.3, 1.0), 0.02
        for p in pts:
            if near_a_minimum(p[0], pts, sigma, 0.05):
                continue
            mode = grid_mode(p[0], pts, sigma)
            x, _ = climb_fixed_step(p, pts, sigma, delta)
            assert abs(x[0] - mode) <= delta + 0.002
            y, _ = climb_fixed_point(p, pts, sigma, tol=1e-13)
            assert abs(y[0] - mode) <= 0.01
            checked += 1
    assert checked > 50


def test_fixed_point_step_never_lowers_density():
    rng = random.Random(4)
    for _ in range(30):
        pts = [(rng.gauss(0, 2), rng.gauss(0, 2)) for _ in range(rng.randrange(1, 15))]
        sigma = rng.uniform(0.3, 2)
        trace = []
        climb_fixed_point((rng.uniform(-4, 4), rng.uniform(-4, 4)), pts, sigma, tol=1e-12, max_iter=300, trace=trace)
        values = [density(y, pts, sigma) for y in trace]
        assert all(b >= a - 1e-12 for a, b in zip(values, values[1:]))


def test_noise_is_points_with_weak_attractors():
    rng = random.Random(5)
    for _ in range(8):
        pts = [(rng.gauss(0, 0.4), rng.gauss(0, 0.4)) for _ in range(20)]
        pts += [(rng.uniform(5, 15), rng.uniform(5, 15)) for _ in range(5)]
        sigma, xi = 0.5, rng.uniform(1.5, 4)
        labels, _ = denclue(pts, sigma, xi, shape="center")
        for p, lab in zip(pts, labels):
            _, fx = climb_fixed_step(p, pts, sigma, sigma / 10)
            assert (lab == NOISE) == (fx < xi)
        assert all(lab != NOISE for lab in labels[:20])


def test_arbitrary_shape_joins_attractors_on_a_dense_path():
    # Two bumps joined by a ridge: one cluster for a low xi, two for a high xi,
    # and always two center-defined clusters.
    # The density along the segment from 0 to 3 has its minimum, about 5.09, at 1.5.
    pts = [(0.0, 0.0)] * 10 + [(3.0, 0.0)] * 10 + [(1.0, 0.0), (2.0, 0.0)]
    sigma = 0.8
    assert 5.0 < density((1.5, 0.0), pts, sigma) < 5.2
    low, _ = denclue(pts, sigma, 3.0)
    assert low == [0] * 22
    high, _ = denclue(pts, sigma, 8.0)
    assert high == [0] * 10 + [1] * 10 + [0, 1]
    center, _ = denclue(pts, sigma, 3.0, shape="center")
    assert center == high


def test_arbitrary_shape_labels_are_components_of_the_segment_graph():
    rng = random.Random(6)
    for _ in range(6):
        pts = [(rng.gauss(cx, 0.5), rng.gauss(0, 0.5)) for cx in (0, 2, 6) for _ in range(8)]
        sigma, xi = 0.6, rng.uniform(1, 4)
        labels, _ = denclue(pts, sigma, xi)
        center, reps = denclue(pts, sigma, xi, shape="center")
        groups = sorted({c for c in center if c != NOISE})
        # Map center-defined labels to their attractor representatives.
        strong = {}
        for j, c in enumerate(center):
            if c != NOISE:
                strong.setdefault(c, climb_fixed_step(pts[j], pts, sigma, sigma / 10)[0])
        adj = {a: [b for b in groups if b != a and segment_above(strong[a], strong[b], pts, sigma, xi, 20)] for a in groups}
        comp, k = {}, 0
        for s in groups:
            if s in comp:
                continue
            stack, comp[s] = [s], k
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if v not in comp:
                        comp[v] = k
                        stack.append(v)
            k += 1
        for a in range(len(pts)):
            assert (labels[a] == NOISE) == (center[a] == NOISE)
            for b in range(len(pts)):
                if center[a] != NOISE and center[b] != NOISE:
                    assert (labels[a] == labels[b]) == (comp[center[a]] == comp[center[b]])


def test_example_of_the_page():
    pts = [(x,) for x in (0.0, 0.5, 1.0, 4.0, 4.5, 5.0, 9.0)]
    labels, reps = denclue(pts, 0.5, 1.2, delta=0.05)
    assert labels == [0, 0, 0, 1, 1, 1, NOISE]
    assert [round(r[0], 2) for r in reps] == [0.5, 4.5, 9.0]
    assert round(density((0.5,), pts, 0.5), 3) == 2.213 and density((9.0,), pts, 0.5) < 1.2
    labels, reps = denclue(pts, 1.5, 1.2, delta=0.05)
    assert labels == [0, 0, 0, 0, 0, 0, NOISE]
    assert [round(r[0], 2) for r in reps] == [0.7, 4.35, 8.7]
    assert denclue(pts, 1.5, 1.2, delta=0.05, shape="center")[0] == [0, 0, 0, 1, 1, 1, NOISE]


def test_edges():
    assert denclue([], 1.0, 0.5) == ([], [])
    labels, reps = denclue([(2.0, 3.0)], 1.0, 0.5)
    assert labels == [0] and reps == [(2.0, 3.0)]
    assert denclue([(2.0, 3.0)], 1.0, 1.5)[0] == [NOISE]
    with pytest.raises(ValueError):
        denclue([(0.0,)], 0, 1)
