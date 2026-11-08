# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quasi-monte-carlo-integration/. The authors are listed in prov/Y77BXY.jsonl.

import math
import random
from fractions import Fraction

import pytest

from quasi_monte_carlo_integration import (
    first_primes,
    halton_point,
    qmc_integrate,
    radical_inverse,
    star_discrepancy_1d,
    star_discrepancy_2d,
)


def reverse_digits_oracle(i, base):
    """Radical inverse by writing the digits as a list and reflecting them."""
    digits = []
    while i > 0:
        digits.append(i % base)
        i //= base
    return sum(Fraction(d, base ** (k + 1)) for k, d in enumerate(digits))


def dstar_1d_oracle(points):
    """Star discrepancy from the definition: open and closed counts at each point and at 1."""
    N = len(points)
    best = 0.0
    for t in list(points) + [1.0]:
        opn = sum(1 for x in points if x < t)
        closed = sum(1 for x in points if x <= t)
        best = max(best, t - opn / N, closed / N - t)
    return best


def dstar_2d_oracle(points):
    N = len(points)
    xs = [p[0] for p in points] + [1.0]
    ys = [p[1] for p in points] + [1.0]
    best = 0.0
    for tx in xs:
        for ty in ys:
            opn = sum(1 for p in points if p[0] < tx and p[1] < ty)
            closed = sum(1 for p in points if p[0] <= tx and p[1] <= ty)
            best = max(best, tx * ty - opn / N, closed / N - tx * ty)
    return best


def test_first_primes():
    assert first_primes(10) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert first_primes(1) == [2]


def test_radical_inverse_against_digit_reversal():
    rng = random.Random(11)
    for _ in range(600):
        base = rng.choice([2, 3, 5, 7, 11, 13, 29, 97])
        i = rng.randrange(0, 10 ** rng.randint(1, 9))
        exact = reverse_digits_oracle(i, base)
        assert abs(radical_inverse(i, base) - exact) <= 1e-15
    assert radical_inverse(0, 2) == 0.0
    assert radical_inverse(1, 2) == 0.5 and radical_inverse(6, 2) == 0.375
    with pytest.raises(ValueError):
        radical_inverse(3, 1)


def test_elementary_boxes_contain_one_point_each():
    # any 2^m consecutive van der Corput points hit each [j/2^m, (j+1)/2^m) once
    for start in (0, 1, 37):
        pts = [radical_inverse(i, 2) for i in range(start, start + 16)]
        assert sorted(int(x * 16) for x in pts) == list(range(16))
    # any 2^3 3^2 = 72 consecutive Halton points hit each box of size 1/8 by 1/9 once
    # (the 1e-9 guards points such as 1/3 that lie on a box edge but round below it)
    for start in (0, 1, 500):
        cells = sorted((int(p[0] * 8 + 1e-9), int(p[1] * 9 + 1e-9)) for p in (halton_point(i, [2, 3]) for i in range(start, start + 72)))
        assert cells == [(a, b) for a in range(8) for b in range(9)]


def test_star_discrepancy_1d_against_definition():
    rng = random.Random(5)
    for _ in range(500):
        N = rng.randint(1, 30)
        pts = [rng.randrange(0, 64) / 64 if rng.random() < 0.5 else rng.random() for _ in range(N)]
        assert abs(star_discrepancy_1d(pts) - dstar_1d_oracle(pts)) < 1e-12
    # the midpoint set is optimal: D* = 1/(2N)
    for N in (1, 7, 50):
        assert abs(star_discrepancy_1d([(2 * i + 1) / (2 * N) for i in range(N)]) - 1 / (2 * N)) < 1e-15


def test_star_discrepancy_2d_against_definition():
    rng = random.Random(6)
    for _ in range(300):
        N = rng.randint(1, 12)
        pts = [(rng.randrange(0, 8) / 8, rng.randrange(0, 8) / 8) for _ in range(N)]
        assert abs(star_discrepancy_2d(pts) - dstar_2d_oracle(pts)) < 1e-12
    for _ in range(50):
        pts = [(rng.random(), rng.random()) for _ in range(rng.randint(1, 15))]
        assert abs(star_discrepancy_2d(pts) - dstar_2d_oracle(pts)) < 1e-12


def test_koksma_hlawka_inequality_holds():
    rng = random.Random(7)
    # one dimension: f = c x^k has variation |c|
    for _ in range(300):
        N = rng.randint(1, 40)
        if rng.random() < 0.5:
            pts = [rng.random() for _ in range(N)]
        else:
            start = rng.randint(0, 100)
            pts = [radical_inverse(i, 2) for i in range(start, start + N)]
        k, c = rng.randint(1, 6), rng.uniform(-3, 3)
        err = abs(math.fsum(c * x ** k for x in pts) / N - c / (k + 1))
        assert err <= abs(c) * star_discrepancy_1d(pts) + 1e-12
    # two dimensions: f = x^a y^b with a, b >= 1 has V_HK = 1 + 1 + 1 = 3
    for _ in range(200):
        N = rng.randint(1, 40)
        pts = [(rng.random(), rng.random()) for _ in range(N)]
        a, b = rng.randint(1, 4), rng.randint(1, 4)
        err = abs(math.fsum(x ** a * y ** b for x, y in pts) / N - 1 / ((a + 1) * (b + 1)))
        assert err <= 3 * star_discrepancy_2d(pts) + 1e-12


def test_low_discrepancy_against_random_points():
    for N in (100, 1000):
        vdc = [radical_inverse(i, 2) for i in range(1, N + 1)]
        assert N * star_discrepancy_1d(vdc) <= math.log2(N) + 1
        rng = random.Random(1)
        rnd = [rng.random() for _ in range(N)]
        assert star_discrepancy_1d(vdc) < star_discrepancy_1d(rnd) / 3
    for N in (256, 1000):
        hal = [halton_point(i, [2, 3]) for i in range(1, N + 1)]
        rng = random.Random(1)
        rnd = [(rng.random(), rng.random()) for _ in range(N)]
        dh, dr = star_discrepancy_2d(hal), star_discrepancy_2d(rnd)
        assert dh < dr / 2
        assert dh * N / math.log(N) ** 2 < 1.0


def test_randomized_qmc_rate_beats_monte_carlo():
    f = lambda x: math.exp(x[0] + x[1])
    exact = (math.e - 1) ** 2
    sigma = math.sqrt(((math.e ** 2 - 1) / 2) ** 2 - exact ** 2)
    rms = {}
    for N in (256, 4096):
        rng = random.Random(3)
        errs = [(qmc_integrate(f, [0, 0], [1, 1], N, replicates=1, rng=rng)[0] - exact) ** 2 for _ in range(20)]
        rms[N] = math.sqrt(math.fsum(errs) / len(errs))
        assert rms[N] < 0.25 * sigma / math.sqrt(N)
    # Monte Carlo would give a ratio of 1/4; quasi-Monte Carlo is near 1/16
    assert rms[4096] / rms[256] < 0.15


def test_shifted_replicates_are_unbiased():
    f = lambda x: x[0] ** 3 + math.sin(3 * x[1]) + x[0] * x[2]
    exact = 0.25 + (1 - math.cos(3)) / 3 + 0.25
    v, se = qmc_integrate(f, [0, 0, 0], [1, 1, 1], 16, replicates=400, rng=random.Random(9))
    assert se is not None and se > 0
    assert abs(v - exact) < 4 * se


def test_edges():
    one = lambda x: 1.0
    # dimension 1
    v, se = qmc_integrate(lambda x: x[0] ** 2, [0.0], [3.0], 2048)
    assert se is None and abs(v - 9.0) < 0.05
    # zero-width box and reversed bounds
    assert qmc_integrate(one, [0.0, 1.0], [2.0, 1.0], 10)[0] == 0.0
    v, _ = qmc_integrate(lambda x: x[0], [1.0], [0.0], 1024)
    assert abs(v + 0.5) < 0.01
    # a single point: the Halton point with index 1
    v, _ = qmc_integrate(lambda x: x[0] + 10 * x[1], [0, 0], [1, 1], 1)
    assert abs(v - (0.5 + 10 / 3)) < 1e-15
    # dimension 20: product of (1 + (x_k - 1/2)/k), integral 1
    g = lambda x: math.prod(1 + (xk - 0.5) / (k + 1) for k, xk in enumerate(x))
    v, _ = qmc_integrate(g, [0.0] * 20, [1.0] * 20, 4096)
    assert abs(v - 1.0) < 1e-2
    # a jump along the diagonal: area of a triangle
    v, _ = qmc_integrate(lambda x: 1.0 if x[0] + x[1] < 1 else 0.0, [0, 0], [1, 1], 4096)
    assert abs(v - 0.5) < 5e-3
    with pytest.raises(ValueError):
        qmc_integrate(one, [0.0], [1.0], 0)
    with pytest.raises(ValueError):
        qmc_integrate(one, [0.0], [math.inf], 10)
    with pytest.raises(ValueError):
        qmc_integrate(one, [0.0], [1.0], 10, replicates=3)
    with pytest.raises(ValueError):
        qmc_integrate(one, [0.0, 0.0], [1.0], 10)


def test_evaluation_count():
    calls = [0]

    def f(x):
        calls[0] += 1
        return x[0]

    qmc_integrate(f, [0, 0], [1, 1], 100, replicates=7, rng=random.Random(2))
    assert calls[0] == 700
