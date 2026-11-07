# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-raphson-method/. The authors are listed in prov/WV8WGC.jsonl.

import math
import random
from decimal import Decimal, getcontext
from fractions import Fraction

from newton_raphson_method import newton

COS_ROOT = 0.7390851332151607


def test_worked_example_table():
    xs = []

    def f(x):
        xs.append(x)
        return math.cos(x) - x

    r = newton(f, lambda x: -math.sin(x) - 1, 1.0)
    assert xs == [1.0, 0.7503638678402439, 0.7391128909113617, 0.739085133385284,
                  0.7390851332151607]
    assert r.reason == "root" and r.root == COS_ROOT
    assert (r.f_evals, r.df_evals, r.iterations) == (5, 4, 5)


def test_known_roots():
    cases = [
        (lambda x: math.exp(x) - 2, math.exp, 1.0, math.log(2)),
        (lambda x: x ** 3 - x - 2, lambda x: 3 * x * x - 1, 1.5, 1.5213797068045676),
        (lambda x: (x - 1) * (x + 2) * (x - 3.5), lambda x: 3 * x * x - 5 * x - 4.5,
         3.0, 3.5),
    ]
    for f, df, x0, root in cases:
        r = newton(f, df, x0)
        assert r.converged
        assert abs(r.root - root) <= 4e-16 * max(1.0, abs(root))


def test_complex_root():
    r = newton(lambda z: z * z + 1, lambda z: 2 * z, complex(0.5, 0.5))
    assert r.converged and abs(r.root - 1j) < 1e-15


def test_quadratic_order_in_exact_arithmetic():
    getcontext().prec = 80
    root = Decimal(2).sqrt()
    xs = []

    def f(x):
        xs.append(x)
        return x * x - 2

    newton(f, lambda x: 2 * x, Fraction(1), tol_abs=1e-40, tol_rel=0.0, max_iter=6)
    errs = [abs(Decimal(x.numerator) / Decimal(x.denominator) - root) for x in xs]
    for k in range(3, len(errs) - 1):
        q = float((errs[k + 1] / errs[k]).ln() / (errs[k] / errs[k - 1]).ln())
        assert abs(q - 2) < 0.02
    assert abs(float(errs[-1] / errs[-2] ** 2) - 0.3535533905932738) < 1e-9


def test_step_error_bound():
    # Claim 2, item 4: |e_(k+1)| <= 4 M s_k^2 with M from the interval [1, 2].
    getcontext().prec = 80
    root = Decimal(2).sqrt()
    m = Fraction(1, 2)  # max|f''| / (2 min|f'|) = 2 / (2 * 2) on [1, 2]
    x = Fraction(2)
    for _ in range(5):
        s = -(x * x - 2) / (2 * x)
        x = x + s
        e = abs(Decimal(x.numerator) / Decimal(x.denominator) - root)
        bound = 4 * m * s * s
        assert e <= Decimal(bound.numerator) / Decimal(bound.denominator)


def test_double_root_is_linear():
    xs = []

    def f(x):
        xs.append(x)
        return x ** 3 - 3 * x + 2

    getcontext().prec = 60
    newton(f, lambda x: 3 * x * x - 3, Decimal(2), tol_abs=Decimal("1e-12"), tol_rel=Decimal(0),
           max_iter=30)
    ratios = [float((xs[k + 1] - 1) / (xs[k] - 1)) for k in range(15, 20)]
    assert all(abs(q - 0.5) < 1e-4 for q in ratios)


def test_root_at_start_and_zero_derivative():
    r = newton(lambda x: x - 2.0, lambda x: 1.0, 2.0)
    assert r.reason == "root" and (r.f_evals, r.df_evals) == (1, 0)
    r = newton(lambda x: x * x - 1, lambda x: 2 * x, 0.0)
    assert r.reason == "failure" and r.root == 0.0


def test_cycle_hits_max_iterations():
    xs = []

    def f(x):
        xs.append(x)
        return x ** 3 - 2 * x + 2

    r = newton(f, lambda x: 3 * x * x - 2, 0.0, max_iter=10)
    assert r.reason == "kmax reached" and r.f_evals == 10 and r.df_evals == 10
    assert xs == [0.0, 1.0] * 5


def test_nan_and_overflow():
    r = newton(lambda x: float("nan"), lambda x: 1.0, 1.0)
    assert r.reason == "failure"
    r = newton(lambda x: math.atan(x), lambda x: 1 / (1 + x * x), 1.5, max_iter=2000)
    assert not r.converged


def test_float_cycle_needs_relative_test():
    r = newton(lambda x: x * x - 2, lambda x: 2 * x, 1.0, tol_abs=1e-17, tol_rel=0.0,
               max_iter=50)
    assert r.reason == "kmax reached"
    r = newton(lambda x: x * x - 2, lambda x: 2 * x, 1.0)
    assert r.reason == "converged" and r.iterations == 6
    assert abs(r.root - math.sqrt(2)) <= 2.3e-16


def test_random_cubics_with_known_roots():
    rng = random.Random(20261107)
    for _ in range(600):
        roots = sorted(rng.uniform(-5, 5) for _ in range(3))
        if roots[1] - roots[0] < 1 or roots[2] - roots[1] < 1:
            continue
        a, b, c = roots

        def f(x, a=a, b=b, c=c):
            return (x - a) * (x - b) * (x - c)

        def df(x, a=a, b=b, c=c):
            return (x - b) * (x - c) + (x - a) * (x - c) + (x - a) * (x - b)

        target = rng.choice(roots)
        r = newton(f, df, target + rng.uniform(-0.05, 0.05))
        assert r.converged and abs(r.root - target) <= 1e-13
        assert r.f_evals - r.df_evals in (0, 1)
