# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secant-method/. The authors are listed in prov/8VVH8M.jsonl.

import math
import random
from decimal import Decimal, getcontext

from secant_method import secant

PHI = (1 + 5 ** 0.5) / 2


def test_worked_example_table():
    xs = []

    def f(x):
        xs.append(x)
        return math.cos(x) - x

    r = secant(f, 0.0, 1.0)
    assert xs == [0.0, 1.0, 0.6850733573260451, 0.736298997613654, 0.7391193619116293,
                  0.7390851121274639, 0.7390851332150012, 0.7390851332151607]
    assert r.reason == "root" and r.evaluations == 8 and r.root == 0.7390851332151607


def test_known_roots():
    cases = [
        (lambda x: math.exp(x) - 2, 0.0, 1.0, math.log(2)),
        (lambda x: x ** 3 - x - 2, 1.0, 2.0, 1.5213797068045676),
        (lambda x: (x - 1) * (x + 2) * (x - 3.5), 3.0, 4.0, 3.5),
    ]
    for f, a, b, root in cases:
        r = secant(f, a, b)
        assert r.converged and abs(r.root - root) <= 4e-16 * max(1.0, abs(root))


def test_complex_root():
    r = secant(lambda z: z * z + 1, complex(0.5, 0.5), complex(0.6, 0.8))
    assert r.converged and abs(r.root - 1j) < 1e-14


def test_observed_order_is_golden_ratio():
    getcontext().prec = 400
    root = Decimal("1.5213797068045675696")  # refined below
    for _ in range(12):
        root -= (root ** 3 - root - 2) / (3 * root * root - 1)
    xs = []

    def f(x):
        xs.append(x)
        return x ** 3 - x - 2

    secant(f, Decimal(1), Decimal(2), tol_abs=Decimal("1e-300"), tol_rel=Decimal(0),
           max_iter=11)
    errs = [abs(x - root) for x in xs]
    qs = [float((errs[k + 1] / errs[k]).ln() / (errs[k] / errs[k - 1]).ln())
          for k in range(7, len(errs) - 1)]
    assert all(abs(q - PHI) < 0.01 for q in qs)
    c = 6 * root / (2 * (3 * root * root - 1))
    assert abs(float(errs[-1] / errs[-2] ** Decimal(PHI)) - float(c) ** (1 / PHI)) < 1e-2


def test_double_root_is_linear():
    getcontext().prec = 60
    xs = []

    def f(x):
        xs.append(x)
        return x ** 3 - 3 * x + 2

    secant(f, Decimal(2), Decimal("1.5"), tol_abs=Decimal("1e-15"), tol_rel=Decimal(0),
           max_iter=60)
    ratios = [float((xs[k + 1] - 1) / (xs[k] - 1)) for k in range(25, 30)]
    assert all(abs(q - 1 / PHI) < 1e-3 for q in ratios)


def test_evaluation_counts():
    r = secant(lambda x: x - 0.25, 0.0, 1.0)
    # the line is exact: x2 = 0.25 is a root found at the first pass
    assert r.reason == "root" and r.evaluations == 3 and r.iterations == 1
    r = secant(lambda x: x ** 3 - x - 2, 1.0, 2.0, tol_rel=1e-6)
    assert r.reason == "converged" and r.evaluations == r.iterations + 1


def test_edges():
    assert secant(lambda x: x, 0.0, 1.0).reason == "root"
    assert secant(lambda x: x - 1.0, 0.0, 1.0).reason == "root"
    r = secant(lambda x: x * x - 1, -0.5, 0.5)
    assert r.reason == "failure"
    r = secant(lambda x: float("nan"), 0.0, 1.0)
    assert r.reason == "failure"
    r = secant(lambda x: math.atan(x), 2.0, 3.0)
    assert not r.converged
    r = secant(lambda x: x * x + 1, 0.0, 1.0, max_iter=5)
    assert r.reason in ("kmax reached", "failure") and r.evaluations <= 7


def test_random_cubics_with_known_roots():
    rng = random.Random(1618)
    count = 0
    while count < 500:
        roots = sorted(rng.uniform(-5, 5) for _ in range(3))
        if roots[1] - roots[0] < 1 or roots[2] - roots[1] < 1:
            continue
        count += 1
        a, b, c = roots
        target = rng.choice(roots)
        x0 = target + rng.uniform(-0.05, 0.05)
        r = secant(lambda x: (x - a) * (x - b) * (x - c), x0, x0 + 0.01)
        assert r.converged and abs(r.root - target) <= 1e-13
