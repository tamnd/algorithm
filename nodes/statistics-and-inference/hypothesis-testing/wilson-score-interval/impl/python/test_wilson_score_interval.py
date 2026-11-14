# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wilson-score-interval/. The authors are listed in prov/H3CD21.jsonl.

import math
from fractions import Fraction
from statistics import NormalDist

import pytest

from wilson_score_interval import wilson_score_interval

Z = NormalDist().inv_cdf(0.975)


def test_page_examples() -> None:
    assert wilson_score_interval(3, 10) == pytest.approx((0.107791, 0.603222), abs=1e-6)
    assert wilson_score_interval(7, 20) == pytest.approx((0.181192, 0.567146), abs=1e-6)
    assert wilson_score_interval(0, 10) == (0.0, pytest.approx(Z * Z / (10 + Z * Z), abs=1e-15))
    lo, hi = wilson_score_interval(10, 10)
    assert hi == 1.0 and lo == pytest.approx(10 / (10 + Z * Z), abs=1e-15)


def test_ends_solve_the_score_equation() -> None:
    # (x - n p)^2 = z^2 n p (1 - p) at both ends, checked in exact arithmetic on the floats.
    z2 = Fraction(Z) ** 2
    for n in (1, 2, 7, 30, 1000, 10**9):
        for x in sorted({0, 1, 2, n // 3, n // 2, n - 1, n}):
            if not 0 <= x <= n:
                continue
            for p in wilson_score_interval(x, n):
                q = Fraction(p)
                residual = (x - n * q) ** 2 - z2 * n * q * (1 - q)
                scale = x * x + z2 * n + 1
                assert abs(residual) / scale < 1e-12, (x, n, p)


def test_small_x_has_no_cancellation() -> None:
    # The naive center - half loses all digits here; the product form keeps them.
    n = 10**12
    lo, hi = wilson_score_interval(1, n)
    z2 = Z * Z
    product = (1 / n) / (n + z2)
    assert lo * hi == pytest.approx(product, rel=1e-14)
    assert lo > 0


def test_inverts_the_score_test() -> None:
    for n in (5, 12, 40):
        for x in range(n + 1):
            lo, hi = wilson_score_interval(x, n)
            for k in range(1, 1000):
                p0 = k / 1000
                if min(abs(p0 - lo), abs(p0 - hi)) < 1e-9:
                    continue
                accept = abs(x - n * p0) <= Z * math.sqrt(n * p0 * (1 - p0))
                assert accept == (lo <= p0 <= hi), (n, x, p0)


def test_symmetry_and_order() -> None:
    for n in (1, 9, 50):
        rows = [wilson_score_interval(x, n, 0.1) for x in range(n + 1)]
        for x in range(n + 1):
            lo, hi = rows[x]
            assert 0.0 <= lo < x / n + 1e-15 or x == 0
            assert lo <= x / n <= hi
            assert lo == pytest.approx(1 - rows[n - x][1], abs=1e-14)
        assert all(a[0] < b[0] and a[1] < b[1] for a, b in zip(rows, rows[1:]))


def exact_coverage(n: int, p: float, rows: list[tuple[float, float]]) -> float:
    w = [math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)]
    return math.fsum(w[x] for x in range(n + 1) if rows[x][0] <= p <= rows[x][1])


def test_measured_coverage_on_a_grid() -> None:
    # Coverage is not guaranteed; it is measured by exact binomial sums.
    table = {10: (0.8424, 0.017), 20: (0.8516, 0.008), 50: (0.8605, 0.003)}
    for n, (minimum, where) in table.items():
        rows = [wilson_score_interval(x, n) for x in range(n + 1)]
        grid = [k / 1000 for k in range(1, 1000)]
        cover = [exact_coverage(n, p, rows) for p in grid]
        i = min(range(len(grid)), key=cover.__getitem__)
        assert cover[i] == pytest.approx(minimum, abs=1e-4)
        assert grid[i] == where
        mean = sum(cover) / len(cover)
        assert 0.945 < mean < 0.96
        assert sum(c < 0.95 for c in cover) > 300


def test_proved_dip_near_zero() -> None:
    # Just below p = lam*/n, only x = 0 covers p, so the coverage is (1 - p)^n < exp(-lam*).
    z2 = Z * Z
    lam = ((2 + z2) - math.sqrt((2 + z2) ** 2 - 4)) / 2
    assert math.exp(-lam) == pytest.approx(0.83818, abs=1e-5)
    for n in (1, 2, 5, 10, 37, 100, 1000):
        p = lam / n * (1 - 1e-9)
        rows = [wilson_score_interval(x, n) for x in range(n + 1)]
        assert [x for x in range(n + 1) if rows[x][0] <= p <= rows[x][1]] == [0]
        assert exact_coverage(n, p, rows) == pytest.approx((1 - p) ** n, rel=1e-12)
        assert exact_coverage(n, p, rows) < math.exp(-lam)


def test_errors() -> None:
    for bad in ((3, 2), (-1, 5), (0, 0)):
        with pytest.raises(ValueError):
            wilson_score_interval(*bad)
    with pytest.raises(ValueError):
        wilson_score_interval(1, 5, 0.0)
