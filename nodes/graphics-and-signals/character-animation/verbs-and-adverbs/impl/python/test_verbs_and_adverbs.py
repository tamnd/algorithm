# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verbs-and-adverbs/. The authors are listed in prov/G3VDNR.jsonl.
"""Tests of verbs and adverbs interpolation.

The interpolant reproduces every example, reproduces linear data exactly
everywhere with zero radial weights, has a least squares linear part (the
residuals are orthogonal to the columns), and is only linear far from the
examples. On a smooth nonlinear verb, the error at new adverbs is measured
against the linear part alone. Examples are made in code with a fixed seed.
"""

import math
import random

import verbs_and_adverbs as va


def curve(p, samples=8):
    """Control values of a joint curve for adverbs p = (speed, turn)."""
    speed, turn = p
    return [0.4 * speed * math.sin(2 * math.pi * k / samples) + 0.3 * turn * math.cos(speed + k)
            + 0.1 * speed * turn for k in range(samples)]


def examples(rng, n):
    P = [(rng.uniform(0.5, 2.5), rng.uniform(-1.0, 1.0)) for _ in range(n)]
    return P, [curve(p) for p in P]


def test_bspline_values():
    assert va.bspline(0.0) == 2.0 / 3.0
    assert abs(va.bspline(1.0) - 1.0 / 6.0) < 1e-15
    assert va.bspline(2.0) == 0.0 and va.bspline(3.0) == 0.0
    h = 1e-5
    for s in (1.0,):
        d1 = (va.bspline(s + h) - va.bspline(s - h)) / (2 * h)
        assert abs(d1 + 0.5) < 1e-6


def test_examples_are_reproduced():
    rng = random.Random(1)
    P, Y = examples(rng, 12)
    v = va.Verb(P, Y)
    for p, y in zip(P, Y):
        assert max(abs(a - b) for a, b in zip(v(p), y)) < 1e-9


def test_linear_data_is_exact():
    rng = random.Random(2)
    P = [(rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(10)]
    f = lambda p: [1.0 + 2.0 * p[0] - p[1] + 0.5 * p[2], -3.0 + p[2]]
    v = va.Verb(P, [f(p) for p in P])
    assert max(abs(x) for row in v.w for x in row) < 1e-9
    for _ in range(50):
        p = (rng.uniform(-1, 2), rng.uniform(-1, 2), rng.uniform(-1, 2))
        assert max(abs(a - b) for a, b in zip(v(p), f(p))) < 1e-9


def test_linear_part_is_least_squares():
    rng = random.Random(3)
    P, Y = examples(rng, 15)
    v = va.Verb(P, Y)
    for k in range(v.q):
        r = [v.resid[i][k] for i in range(v.n)]
        assert abs(sum(r)) < 1e-9
        for l in range(v.a):
            assert abs(sum(ri * p[l] for ri, p in zip(r, P))) < 1e-9


def test_far_from_examples_only_linear():
    rng = random.Random(4)
    P, Y = examples(rng, 10)
    v = va.Verb(P, Y)
    far = (20.0, 20.0)
    assert v(far) == v.linear(far)


def test_measured_error_against_linear_only():
    rng = random.Random(5)
    P, Y = examples(rng, 25)
    v = va.Verb(P, Y)
    err_full = err_lin = 0.0
    for _ in range(200):
        p = (rng.uniform(0.7, 2.3), rng.uniform(-0.8, 0.8))
        y = curve(p)
        err_full += sum((a - b) ** 2 for a, b in zip(v(p), y))
        err_lin += sum((a - b) ** 2 for a, b in zip(v.linear(p), y))
    # measured on this seed: the radial part lowers the squared error
    assert err_full < err_lin
