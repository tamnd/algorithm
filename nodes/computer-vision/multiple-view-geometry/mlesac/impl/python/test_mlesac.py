# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mlesac/. The authors are listed in prov/3GWPBP.jsonl.

import math
import random

from mlesac import (em_mixing, fit_line_weighted, line_through, mixture_nll, mlesac,
                    point_line_distance, ransac_trials)

EXAMPLE = [(0, 0), (1, 0.1), (2, 0), (3, 0.1), (4, 0), (1, 2), (3, -2)]


def residuals(line, data):
    return [point_line_distance(line, x) for x in data]


def planted(rng, n_in, n_out, a=0.5, b=2.0, sigma=0.0, gap=1.0):
    pts = []
    for _ in range(n_in):
        x = rng.uniform(0.0, 10.0)
        pts.append((x, a * x + b + (rng.gauss(0.0, sigma) if sigma else 0.0)))
    true_line = line_through([(0.0, b), (1.0, a + b)])
    while len(pts) < n_in + n_out:
        q = (rng.uniform(0.0, 10.0), rng.uniform(-5.0, 12.0))
        if point_line_distance(true_line, q) > gap:
            pts.append(q)
    return pts, true_line


def line_angle(l1, l2):
    return math.atan2(abs(l1[0] * l2[1] - l1[1] * l2[0]), abs(l1[0] * l2[0] + l1[1] * l2[1]))


def best_gamma(e, sigma, v):
    """Ternary search; the log-likelihood is concave in gamma."""
    lo, hi = 0.0, 1.0
    for _ in range(200):
        a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if mixture_nll(e, a, sigma, v) < mixture_nll(e, b, sigma, v):
            hi = b
        else:
            lo = a
    return lo


def test_example_values():
    y01 = residuals(line_through([(1, 0.1), (3, 0.1)]), EXAMPLE)
    slanted = residuals(line_through([(2, 0), (1, 2)]), EXAMPLE)
    y0 = residuals(line_through([(0, 0), (4, 0)]), EXAMPLE)
    expect = [(y01, 0.6903, 0.704, 3.304), (slanted, 0.4181, 0.4139, 9.7382), (y0, 0.6925, 0.705, 2.8107)]
    for e, g1, g5, nll in expect:
        assert abs(em_mixing(e, 0.1, 10.0, steps=1) - g1) < 5e-5
        g = em_mixing(e, 0.1, 10.0)
        assert abs(g - g5) < 5e-5
        assert abs(mixture_nll(e, g, 0.1, 10.0) - nll) < 5e-5
    assert ransac_trials(0.99, 0.705, 2) == 7


def test_example_run():
    model, gamma, nll, t = mlesac(EXAMPLE, 0.1, 10.0, random.Random(1))
    assert abs(nll - 2.8107) < 5e-5 and abs(gamma - 0.705) < 5e-5 and t == 7
    assert abs(model[0]) < 1e-12 and abs(model[2] + 0.0398) < 5e-5


def test_em_ascent_and_limit():
    data, line = planted(random.Random(4), 30, 20, sigma=0.1, gap=0.5)
    e = residuals(line, data)
    g, prev = 0.5, mixture_nll(e, 0.5, 0.1, 20.0)
    for _ in range(50):
        g = em_mixing(e, 0.1, 20.0, steps=1, gamma=g)
        cur = mixture_nll(e, g, 0.1, 20.0)
        assert cur <= prev + 1e-12
        prev = cur
    assert abs(g - best_gamma(e, 0.1, 20.0)) < 1e-6


def test_nll_is_least_among_sampled_models():
    for seed in range(3):
        data, _ = planted(random.Random(seed), 30, 30, sigma=0.05, gap=0.5)
        seen = []

        def solver(sample):
            line = line_through(sample)
            if line is not None:
                seen.append(mixture_nll(residuals(line, data), em_mixing(residuals(line, data), 0.05, 20.0),
                                        0.05, 20.0))
            return line

        _, _, nll, t = mlesac(data, 0.05, 20.0, random.Random(70 + seed), fit_minimal=solver)
        assert len(seen) == t
        assert abs(nll - min(seen)) < 1e-9


def test_planted_line():
    data, true_line = planted(random.Random(3), 50, 50, sigma=0.05, gap=0.5)
    model, gamma, _, _ = mlesac(data, 0.05, 20.0, random.Random(5))
    assert line_angle(model, true_line) < math.radians(1.0)
    assert abs(gamma - 0.5) < 0.1


def test_degenerate():
    assert mlesac([(1.0, 1.0)] * 4, 0.1, 10.0, random.Random(0), max_trials=10)[:3] == (None, 0.0, math.inf)
    assert mlesac([(0.0, 0.0)], 0.1, 10.0, random.Random(0)) == (None, 0.0, math.inf, 0)
    assert fit_line_weighted([(0.0, 0.0), (1.0, 1.0)], [0.0, 0.0]) is None
