# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tanh-sinh-quadrature/. The authors are listed in prov/FDAEA3.jsonl.

import math
import random

from tanh_sinh_quadrature import tanh_sinh, tanh_sinh_node


def counted(f):
    calls = [0]

    def g(*args):
        calls[0] += 1
        return f(*args)

    return g, calls


def beta_integral(a, b, alpha, beta):
    """Exact value of the integral of (x - a)^alpha (b - x)^beta on [a, b]."""
    lg = math.lgamma(alpha + 1) + math.lgamma(beta + 1) - math.lgamma(alpha + beta + 2)
    return (b - a) ** (alpha + beta + 1) * math.exp(lg)


def test_edges_and_orientation():
    assert tanh_sinh(math.exp, 0.7, 0.7) == (0.0, 0.0, 0)
    v, _, _ = tanh_sinh(math.exp, 0.0, 1.0)
    w, _, _ = tanh_sinh(math.exp, 1.0, 0.0)
    assert abs(v - (math.e - 1)) < 1e-14
    assert w == -v
    # a very short interval far from 0
    v, _, _ = tanh_sinh(math.cos, 1e6, 1e6 + 1e-3)
    exact = math.sin(1e6 + 1e-3) - math.sin(1e6)
    # nodes closer than half an ulp of 1e6 to an end are evaluated at the end
    assert abs(v - exact) < 1e-9 * 1e-3


def test_node_formulas():
    d, w = tanh_sinh_node(0.0)
    assert d == 1.0 and abs(w - math.pi / 2) < 1e-15
    for t in (0.1, 0.5, 1.0, 2.0):
        u = math.pi / 2 * math.sinh(t)
        d, w = tanh_sinh_node(t)
        assert abs(d - (1 - math.tanh(u))) < 1e-15
        assert abs(w - math.pi / 2 * math.cosh(t) / math.cosh(u) ** 2) < 1e-15 * max(1.0, w)
    # far out: no overflow, correct underflow
    d, w = tanh_sinh_node(7.0)
    assert d == 0.0 and w == 0.0
    d, w = tanh_sinh_node(5.0)
    assert 0.0 < d < 1e-100 and 0.0 < w < 1e-90
    # weights integrate the constant 1 on [-1, 1]: h * sum w = 2
    h = 1 / 16
    s = h * math.fsum(tanh_sinh_node(j * h)[1] for j in range(-96, 97))
    assert abs(s - 2.0) < 1e-15


def test_endpoint_singularities():
    cases = [
        (math.log, 0.0, 1.0, -1.0),
        (lambda x: x ** -0.5, 0.0, 1.0, 2.0),
        (lambda x: x ** -0.9, 0.0, 1.0, 10.0),
        (lambda x: math.sqrt(x) * math.log(x), 0.0, 1.0, -4 / 9),
        (lambda x: math.sqrt(1 - x * x), -1.0, 1.0, math.pi / 2),
        (lambda x: math.log(x) * math.log(1 - x) if x < 1 else 0.0, 0.0, 1.0, 2 - math.pi ** 2 / 6),
    ]
    for f, a, b, exact in cases:
        v, est, n = tanh_sinh(f, a, b)
        assert abs(v - exact) < 2e-13 * max(1.0, abs(exact)), (exact, v)
        assert n < 1000


def test_distances_keep_accuracy_at_nonzero_end():
    # (1 - x)^(-1/2) on [0, 1]: x near 1 cannot be stored accurately
    v, _, _ = tanh_sinh(lambda x: (1 - x) ** -0.5, 0.0, 1.0)
    err_plain = abs(v - 2.0)
    v, _, _ = tanh_sinh(lambda x, da, db: db ** -0.5, 0.0, 1.0, with_distances=True)
    err_dist = abs(v - 2.0)
    assert err_plain > 1e-10
    assert err_dist < 1e-14
    # arcsine density on [-1, 1]
    v, _, n = tanh_sinh(lambda x, da, db: 1 / math.sqrt(da * db), -1.0, 1.0, with_distances=True)
    assert abs(v - math.pi) < 1e-14 and n < 200


def test_digits_roughly_double_per_level():
    f = lambda x: math.sqrt(x) * math.log(x)
    errs, ns = [], []
    for k in range(3):
        v, _, n = tanh_sinh(f, 0.0, 1.0, tol=-1.0, max_level=k, t_max=4.0)
        errs.append(abs(v + 4 / 9))
        ns.append(n)
    # errors 1.0e-2, 5.2e-6, 3.3e-13 with 9, 17, 33 evaluations
    assert ns == [9, 17, 33]
    assert errs[0] > 1e-3 and errs[1] < 1e-5 and errs[2] < 1e-12
    assert -math.log10(errs[2]) > 1.8 * -math.log10(errs[1])


def test_infinite_intervals():
    cases = [
        (lambda x: math.exp(-x), 0.0, math.inf, 1.0),
        (lambda x: math.exp(x), -math.inf, 0.0, 1.0),
        (lambda x: 1 / (1 + x * x), -math.inf, math.inf, math.pi),
        (lambda x: math.exp(-x * x), -math.inf, math.inf, math.sqrt(math.pi)),
        (lambda x: x ** -0.5 * math.exp(-x), 0.0, math.inf, math.sqrt(math.pi)),
    ]
    for f, a, b, exact in cases:
        v, _, _ = tanh_sinh(f, a, b)
        assert abs(v - exact) < 1e-12, (a, b, v, exact)
    v, _, _ = tanh_sinh(lambda x: 1 / (1 + x * x), math.inf, -math.inf)
    assert abs(v + math.pi) < 1e-12


def test_interior_kink_and_jump_are_slow_until_split():
    kink = lambda x: abs(x - 1 / 3)
    exact = (1 / 9 + 4 / 9) / 2
    v, _, n = tanh_sinh(kink, 0.0, 1.0)
    assert abs(v - exact) > 1e-10 and n > 1000
    v1, _, n1 = tanh_sinh(kink, 0.0, 1 / 3)
    v2, _, n2 = tanh_sinh(kink, 1 / 3, 1.0)
    assert abs(v1 + v2 - exact) < 1e-14 and n1 + n2 < 400
    jump = lambda x: 1.0 if x > 0.3 else 0.0
    v, _, _ = tanh_sinh(jump, 0.0, 1.0)
    assert 1e-12 < abs(v - 0.7) < 1e-2


def test_evaluation_count():
    g, calls = counted(math.exp)
    v, _, n = tanh_sinh(g, -1.0, 1.0, tol=-1.0, max_level=3, t_max=3.0)
    assert n == calls[0]
    assert n <= 2 * 3 * 2 ** 3 + 1
    g, calls = counted(lambda x, da, db: 1.0)
    v, _, n = tanh_sinh(g, -1.0, 1.0, tol=-1.0, max_level=3, t_max=3.0, with_distances=True)
    assert n == calls[0] == 2 * 3 * 2 ** 3 + 1
    # the truncation at t_max = 3 drops weight of about 1e-14
    assert abs(v - 2.0) < 1e-13


def test_random_beta_integrals_against_gamma_oracle():
    rng = random.Random(20261108)
    worst = 0.0
    for _ in range(500):
        a = rng.uniform(-5, 5)
        b = a + rng.uniform(0.01, 10)
        alpha = rng.uniform(-0.7, 2.0)
        beta = rng.uniform(-0.7, 2.0)
        exact = beta_integral(a, b, alpha, beta)
        v, est, _ = tanh_sinh(lambda x, da, db: da ** alpha * db ** beta, a, b, with_distances=True)
        rel = abs(v - exact) / exact
        worst = max(worst, rel)
        assert rel < 1e-11, (a, b, alpha, beta, v, exact)
    assert worst < 1e-11


def test_random_polynomials_against_antiderivative():
    rng = random.Random(7)
    for _ in range(200):
        deg = rng.randint(0, 8)
        c = [rng.uniform(-1, 1) for _ in range(deg + 1)]
        a = rng.uniform(-2, 2)
        b = a + rng.uniform(0.1, 3)
        p = lambda x: math.fsum(ck * x ** k for k, ck in enumerate(c))
        P = lambda x: math.fsum(ck * x ** (k + 1) / (k + 1) for k, ck in enumerate(c))
        exact = P(b) - P(a)
        v, _, _ = tanh_sinh(p, a, b)
        scale = math.fsum(abs(ck) * max(abs(a), abs(b)) ** k for k, ck in enumerate(c)) * (b - a)
        assert abs(v - exact) < 1e-13 * max(scale, 1.0)
