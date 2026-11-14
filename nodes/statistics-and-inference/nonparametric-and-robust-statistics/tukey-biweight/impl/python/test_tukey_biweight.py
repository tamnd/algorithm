# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tukey-biweight/. The authors are listed in prov/9NDW0S.jsonl.

import random
from fractions import Fraction
from statistics import NormalDist

import pytest

from tukey_biweight import (
    biweight_location, biweight_step, exact_median, mad_scale, objective, psi, weight,
)


def test_one_step_by_hand() -> None:
    # x = (2, 4, 5, 6, 7, 30), theta = 11/2, sigma = 2, c = 3.
    x = [2, 4, 5, 6, 7, 30]
    th = exact_median(x)
    assert th == Fraction(11, 2)
    w = [weight(Fraction(v - th) / 2, Fraction(3)) for v in x]
    assert w == [Fraction(9025, 20736), Fraction(225, 256), Fraction(20449, 20736),
                 Fraction(20449, 20736), Fraction(225, 256), 0]
    assert biweight_step(x, th, Fraction(3), Fraction(2)) == Fraction(63352, 12339)


def test_page_example() -> None:
    x = [2, 4, 5, 6, 7, 30]
    trace = []
    t = biweight_location(x, trace=trace)
    assert mad_scale(x) == pytest.approx(1.5 / 0.6744897501960817)
    assert [round(v, 4) for v in trace[:4]] == [5.5, 4.9134, 4.8494, 4.8425]
    assert t == pytest.approx(4.841634, abs=1e-6)
    # The point 30 has weight 0 at the end.
    assert weight((30 - t) / mad_scale(x), 4.685) == 0


def test_monotone_descent_and_stationarity() -> None:
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(3, 40)
        x = [rng.gauss(0.0, 1.0) for _ in range(n)]
        for _ in range(rng.randint(0, n // 2 - 1 if n >= 4 else 0)):
            x[rng.randrange(n)] = rng.uniform(-100.0, 100.0)
        c = rng.choice([2.0, 3.0, 4.685, 6.0])
        sigma = mad_scale(x)
        trace = []
        t = biweight_location(x, c=c, trace=trace)
        if sigma == 0:
            continue
        q = [objective(x, v, c, sigma) for v in trace]
        assert all(b <= a + 1e-12 for a, b in zip(q, q[1:]))
        assert q[0] < n * c * c / 6  # the start has a point inside, so the weights stay positive
        assert abs(sum(psi((v - t) / sigma, c) for v in x)) <= 1e-8 * n


def test_exact_steps_do_not_increase_the_objective() -> None:
    rng = random.Random(2)
    for _ in range(60):
        n = rng.randint(2, 12)
        x = [rng.randint(-20, 20) for _ in range(n)] + [rng.randint(100, 200)]
        c, sigma = Fraction(rng.randint(2, 6)), Fraction(rng.randint(1, 5))
        th = exact_median(x)
        for _ in range(3):
            if sum(weight((v - th) / sigma, c) for v in x) == 0:
                break
            new = biweight_step(x, th, c, sigma)
            assert objective(x, new, c, sigma) <= objective(x, th, c, sigma)
            th = new


def test_far_outliers_have_no_influence() -> None:
    rng = random.Random(3)
    for _ in range(50):
        clean = [rng.gauss(10.0, 2.0) for _ in range(rng.randint(5, 30))]
        a = biweight_location(clean + [1e6, 2e6])
        b = biweight_location(clean + [1e9, 5e12])
        assert a == b


def test_efficiency_at_the_normal() -> None:
    # Simpson's rule: E psi^2 / (E psi')^2 = 1 / 0.95 for c = 4.685.
    phi = NormalDist().pdf
    c, m = 4.685, 4000
    h = 2 * c / m

    def simpson(f):
        s = f(-c) + f(c)
        for i in range(1, m):
            s += (4 if i % 2 else 2) * f(-c + i * h)
        return s * h / 3

    e2 = simpson(lambda z: psi(z, c) ** 2 * phi(z))
    e1 = simpson(lambda z: (1 - (z / c) ** 2) * (1 - 5 * (z / c) ** 2) * phi(z))
    assert e1 * e1 / e2 == pytest.approx(0.95, abs=1e-4)


def test_empirical_breakdown() -> None:
    rng = random.Random(4)
    for n in (5, 6, 9, 10, 15):
        clean_all = [rng.uniform(0.0, 10.0) for _ in range(n)]
        for s in (1e6, 1e12):
            for m in range((n + 1) // 2 + 1):
                clean = clean_all[: n - m]
                t = biweight_location(clean + [s] * m)
                if 2 * m < n:
                    assert min(clean) <= t <= max(clean)
                else:
                    assert t >= s / 4


def test_errors() -> None:
    with pytest.raises(ValueError):
        biweight_location([])
    assert biweight_location([4, 4, 4, 9]) == 4
