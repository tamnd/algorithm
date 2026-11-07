# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-square-root/. The authors are listed in prov/MBGG7T.jsonl.

import math
import random
from decimal import Decimal, localcontext
from fractions import Fraction

from newton_square_root import heron_iterates, newton_sqrt


def test_worked_example():
    xs = heron_iterates(2.0, 1.0, 5)
    assert xs == [1.0, 1.5, 1.4166666666666665, 1.4142156862745097, 1.4142135623746899, 1.414213562373095]
    r = newton_sqrt(2.0)
    assert r.reason == "converged" and r.iterations == 5 and r.divisions == 5
    assert r.root == 1.414213562373095  # one unit below the correctly rounded value
    assert math.sqrt(2.0) - r.root == math.ulp(1.4)


def test_fraction_iterates_and_identity():
    xs = heron_iterates(Fraction(2), Fraction(1), 4)
    assert xs == [1, Fraction(3, 2), Fraction(17, 12), Fraction(577, 408), Fraction(665857, 470832)]
    # t_k = (x_k - 3)/(x_k + 3) satisfies t_{k+1} = t_k^2 exactly for a = 9
    xs = heron_iterates(Fraction(9), Fraction(1), 6)
    ts = [(x - 3) / (x + 3) for x in xs]
    assert ts[0] == Fraction(-1, 2)
    for k in range(6):
        assert ts[k + 1] == ts[k] ** 2


def test_monotone_after_first_step():
    for x0 in (1e-3, 0.5, 1.0, 7.0, 1e3):
        xs = heron_iterates(Fraction(5), Fraction(x0), 6)
        for k in range(1, 6):
            assert xs[k] ** 2 >= 5 and xs[k + 1] <= xs[k]


def test_observed_order_two():
    with localcontext() as ctx:
        ctx.prec = 300
        a = Decimal(3)
        r = a.sqrt()
        xs = heron_iterates(a, Decimal(1), 8)
        e = [abs(x - r) for x in xs]
        for k in range(3, 8):
            q = (e[k + 1].ln() - e[k].ln()) / (e[k].ln() - e[k - 1].ln())
            assert abs(q - 2) < 0.05
        # the constant: e_{k+1}/e_k^2 tends to 1/(2 sqrt a)
        assert abs(e[8] / e[7] ** 2 - 1 / (2 * r)) < Decimal("1e-10")


def test_edge_inputs():
    assert newton_sqrt(-1.0).reason == "invalid"
    assert math.isnan(newton_sqrt(math.nan).root)
    assert newton_sqrt(math.inf).root == math.inf
    assert newton_sqrt(0.0).root == 0.0
    z = newton_sqrt(-0.0).root
    assert z == 0.0 and math.copysign(1.0, z) == -1.0
    assert newton_sqrt(5e-324).root == math.sqrt(5e-324)
    big = newton_sqrt(1.7976931348623157e308)
    assert abs(big.root - math.sqrt(1.7976931348623157e308)) <= math.ulp(big.root)


def test_kmax_reached():
    r = newton_sqrt(3.0, max_iter=1)
    assert r.reason == "kmax reached" and r.iterations == 1 and r.divisions == 1
    assert r.root == 1.7321428571428572


def test_perfect_squares_exact():
    rng = random.Random(11)
    for _ in range(2000):
        k = rng.randint(1, 2**26)
        assert newton_sqrt(float(k * k)).root == k


def test_random_within_one_ulp():
    rng = random.Random(20261107)
    for _ in range(5000):
        a = math.ldexp(rng.uniform(0.5, 1.0), rng.randint(-1070, 1020))
        r = newton_sqrt(a)
        assert r.reason == "converged" and r.iterations <= 6
        with localcontext() as ctx:
            ctx.prec = 40
            exact = Decimal(a).sqrt()
        assert abs(Decimal(r.root) - exact) <= Decimal(math.ulp(r.root))
