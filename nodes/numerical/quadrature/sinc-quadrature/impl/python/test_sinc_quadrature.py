# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sinc-quadrature/. The authors are listed in prov/T9V8KG.jsonl.

import math
import random

import pytest

from sinc_quadrature import sinc_nodes, sinc_parameters, sinc_quadrature


def beta_integral(a, b, p, q):
    """Exact integral of (x - a)^(p-1) (b - x)^(q-1) over [a, b]."""
    return (b - a) ** (p + q - 1) * math.exp(math.lgamma(p) + math.lgamma(q) - math.lgamma(p + q))


def test_parameters():
    M, N, h = sinc_parameters(16, 1.0, 1.0, math.pi / 2)
    assert (M, N) == (16, 16) and abs(h - math.sqrt(math.pi ** 2 / 16)) < 1e-15
    M, N, h = sinc_parameters(10, 0.5, 1.0, math.pi / 2)
    assert (M, N) == (10, 5)
    M, N, h = sinc_parameters(10, 2.0, 1.0, 1.0)
    assert (M, N) == (10, 20)
    for bad in ((0, 1, 1, 1), (5, 0, 1, 1), (5, 1, -1, 1), (5, 1, 1, math.pi)):
        with pytest.raises(ValueError):
            sinc_parameters(*bad)


def test_nodes_and_weights_match_the_formulas():
    a, b = -2.0, 3.0
    M, N, h = sinc_parameters(8, 1.0, 1.0, math.pi / 2)
    nodes = sinc_nodes(a, b, M, N, h)
    assert len(nodes) == M + N + 1
    for k, (x, da, db, w) in zip(range(-M, N + 1), nodes):
        e = math.exp(k * h)
        assert abs(x - (a + b * e) / (1 + e)) < 1e-14
        assert abs(da - (x - a)) < 1e-14 and abs(db - (b - x)) < 1e-14
        assert abs(w - h * da * db / (b - a)) < 1e-15
        # phi(x_k) = log((x - a)/(b - x)) = k h
        assert abs(math.log(da / db) - k * h) < 1e-12
    xs = [x for x, _, _, _ in nodes]
    assert xs == sorted(xs) and a < xs[0] and xs[-1] < b


def test_edges():
    assert sinc_quadrature(math.exp, 2.0, 2.0, 10) == 0.0
    v = sinc_quadrature(math.exp, 0.0, 1.0, 64)
    w = sinc_quadrature(math.exp, 1.0, 0.0, 64)
    assert w == -v and abs(v - (math.e - 1)) < 1e-9
    with pytest.raises(ValueError):
        sinc_quadrature(math.exp, 0.0, math.inf, 10)
    # a single node per side
    v = sinc_quadrature(lambda x: 1.0, 0.0, 1.0, 1)
    assert 0.5 < v < 1.5


def test_endpoint_singularities():
    cases = [
        (math.log, 1.0, 1.0, -1.0),
        (lambda x: x ** -0.5, 0.5, 1.0, 2.0),
        (lambda x: math.sqrt(x) * math.log(x), 1.5, 1.0, -4 / 9),
        (lambda x: x ** -0.9, 0.1, 1.0, 10.0),
    ]
    for f, alpha, beta, exact in cases:
        n = math.ceil(math.log(1e10) ** 2 / (math.pi ** 2 * alpha))
        v = sinc_quadrature(f, 0.0, 1.0, n, alpha, beta)
        assert abs(v - exact) < 1e-8 * abs(exact), (exact, v)


def test_rate_is_exp_minus_c_sqrt_n():
    exact = math.e - 1
    errs = {n: abs(sinc_quadrature(math.exp, 0.0, 1.0, n) - exact) for n in (16, 64)}
    # error about exp(-pi sqrt(n)): quadrupling n doubles the exponent
    ratio = math.log(errs[64]) / math.log(errs[16])
    assert 1.6 < ratio < 2.6
    assert errs[64] < 1e-9


def test_random_beta_integrals_against_gamma_oracle():
    rng = random.Random(1)
    worst = 0.0
    for _ in range(500):
        a = rng.uniform(-5, 5)
        b = a + rng.uniform(0.01, 10)
        p, q = rng.uniform(0.3, 2.5), rng.uniform(0.3, 2.5)
        exact = beta_integral(a, b, p, q)
        n = math.ceil(math.log(1e10) ** 2 / (math.pi ** 2 * p))
        v = sinc_quadrature(lambda x, da, db: da ** (p - 1) * db ** (q - 1), a, b, n, p, q, with_distances=True)
        worst = max(worst, abs(v - exact) / exact)
    assert worst < 1e-8


def test_distances_at_a_nonzero_end():
    n = math.ceil(math.log(1e12) ** 2 / (math.pi ** 2 * 0.5))
    plain = sinc_quadrature(lambda x: (1 - x) ** -0.5, 0.0, 1.0, n, 1.0, 0.5)
    exact_d = sinc_quadrature(lambda x, da, db: db ** -0.5, 0.0, 1.0, n, 1.0, 0.5, with_distances=True)
    assert abs(exact_d - 2.0) < 1e-11
    assert abs(plain - 2.0) > abs(exact_d - 2.0)


def test_nearby_poles_need_a_smaller_d():
    f = lambda x: 1 / (1 + 25 * x * x)
    exact = 0.4 * math.atan(5)
    wrong = abs(sinc_quadrature(f, -1.0, 1.0, 64) - exact)
    right = abs(sinc_quadrature(f, -1.0, 1.0, 64, d=0.39) - exact)
    assert wrong > 1e-3 and right < 1e-5


def test_interior_jump_converges_slowly():
    j = lambda x: 1.0 if x > 0.3 else 0.0
    errs = [abs(sinc_quadrature(j, 0.0, 1.0, n) - 0.7) for n in (16, 64, 256)]
    assert all(e > 1e-3 for e in errs)
    assert errs[2] < errs[0]


def test_evaluation_count():
    calls = [0]

    def f(x):
        calls[0] += 1
        return math.cos(x)

    M, N, _ = sinc_parameters(20, 1.0, 0.5, math.pi / 2)
    sinc_quadrature(f, 0.0, 1.0, 20, 1.0, 0.5)
    assert calls[0] == M + N + 1 == 20 + 40 + 1
