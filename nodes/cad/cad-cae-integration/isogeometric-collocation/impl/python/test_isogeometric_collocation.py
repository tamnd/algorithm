# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isogeometric-collocation/. The authors are listed in prov/AE2H60.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from ig2kit import all_basis, greville, open_uniform_knots
from isogeometric_collocation import collocate_poisson, evaluate, max_error, uniform_solve


def random_knots(rng: random.Random, p: int, max_mult: int) -> list:
    """Open knot vector on [0, 1] with random rational interior knots of multiplicity <= max_mult."""
    m = rng.randint(1, 4)
    inner = sorted({F(rng.randint(1, 15), 16) for _ in range(m)})
    knots = [F(0)] * (p + 1)
    for t in inner:
        knots += [t] * rng.randint(1, max_mult)
    return knots + [F(1)] * (p + 1)


def test_worked_example() -> None:
    knots = open_uniform_knots(2, 2, F(0), F(1))
    assert greville(knots, 2) == [0, F(1, 4), F(3, 4), 1]
    assert all_basis(knots, 2, F(1, 4), 2)[2] == [8, -12, 4, 0]
    c, _ = collocate_poisson(knots, 2, lambda x: F(1), F(0), F(0))
    assert c == [0, F(1, 8), F(1, 8), 0]
    for k in range(9):
        x = F(k, 8)
        assert evaluate(knots, 2, c, x) == x * (1 - x) / 2


def test_cubic_example() -> None:
    knots = open_uniform_knots(3, 4, F(0), F(1))
    c, tau = collocate_poisson(knots, 3, lambda x: F(1), F(0), F(0))
    assert tau == [0, F(1, 12), F(1, 4), F(1, 2), F(3, 4), F(11, 12), 1]
    assert c == [0, F(1, 24), F(5, 48), F(13, 96), F(5, 48), F(1, 24), 0]


def test_exact_on_random_splines() -> None:
    """If the solution is in the spline space, collocation returns it exactly."""
    rng = random.Random(4211)
    for _ in range(150):
        p = rng.randint(2, 5)
        knots = random_knots(rng, p, p - 1)
        n = len(knots) - p - 1
        u = [F(0)] + [F(rng.randint(-20, 20), rng.randint(1, 9)) for _ in range(n - 2)] + [F(0)]
        u[-1] = F(rng.randint(-5, 5))
        f = lambda x, u=u, knots=knots, p=p: -evaluate(knots, p, u, x, 2)
        c, _ = collocate_poisson(knots, p, f, u[0], u[-1])
        assert c == u


def test_exact_on_polynomials() -> None:
    """u = sum a_k x^k of degree <= p: the method reproduces it exactly."""
    rng = random.Random(77)
    for _ in range(100):
        p = rng.randint(2, 5)
        knots = random_knots(rng, p, p - 1)
        a = [F(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(p + 1)]
        u = lambda x: sum(ak * x**k for k, ak in enumerate(a))
        f = lambda x: -sum(k * (k - 1) * ak * x ** (k - 2) for k, ak in enumerate(a) if k >= 2)
        c, _ = collocate_poisson(knots, p, f, u(F(0)), u(F(1)))
        for j in range(11):
            x = F(j, 10)
            assert evaluate(knots, p, c, x) == u(x)


def test_singular_with_multiplicity_p() -> None:
    """Pitfall: an interior knot of multiplicity p allows a kink with u'' = 0."""
    knots = [F(0)] * 3 + [F(1, 2)] * 2 + [F(1)] * 3
    with pytest.raises(ValueError):
        collocate_poisson(knots, 2, lambda x: F(1), F(0), F(0))


def test_error_and_rates_against_exact() -> None:
    f = lambda x: math.pi**2 * math.sin(math.pi * x)
    exact = lambda x: math.sin(math.pi * x)
    for p in (2, 3, 4, 5):
        errs = []
        for ne in (8, 16, 32):
            knots, c = uniform_solve(p, ne, f)
            errs.append(max_error(knots, p, c, exact, 400))
        rates = [math.log2(errs[i] / errs[i + 1]) for i in range(2)]
        expected = p if p % 2 == 0 else p - 1
        assert abs(rates[-1] - expected) < 0.2, (p, rates)
    knots, c = uniform_solve(4, 16, f)
    assert max_error(knots, 4, c, exact, 400) < 1e-5


def test_second_derivative_rate() -> None:
    f = lambda x: math.pi**2 * math.sin(math.pi * x)
    for p in (2, 3, 4):
        errs = []
        for ne in (16, 32):
            knots, c = uniform_solve(p, ne, f)
            errs.append(max(abs(float(evaluate(knots, p, c, k / 200, 2)) + f(k / 200)) for k in range(201)))
        assert abs(math.log2(errs[0] / errs[1]) - (p - 1)) < 0.2
