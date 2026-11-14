# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheffe-method/. The authors are listed in prov/JFSS0K.jsonl.

import math
import random
from fractions import Fraction

import pytest

from scheffe_method import best_contrast, scheffe, summary
from stdist import f_ppf, f_sf

EXAMPLE = [[5, 7, 6, 8, 4], [9, 11, 10, 12, 8], [6, 8, 7, 5, 9]]


def exact_parts(groups: list[list[int]]) -> tuple[list[Fraction], Fraction, Fraction]:
    """Group means, SSB and MSE in exact arithmetic."""
    n = [len(g) for g in groups]
    means = [Fraction(sum(g), len(g)) for g in groups]
    grand = sum(ni * m for ni, m in zip(n, means)) / sum(n)
    ssb = sum(ni * (m - grand) ** 2 for ni, m in zip(n, means))
    ssw = sum((v - m) ** 2 for g, m in zip(groups, means) for v in g)
    return means, ssb, ssw / (sum(n) - len(groups))


def t2(c: list[Fraction], groups: list[list[int]], means: list[Fraction], mse: Fraction) -> Fraction:
    """psi_hat^2 / se^2 of the contrast c, exactly."""
    psi = sum(ci * m for ci, m in zip(c, means))
    return psi * psi / (mse * sum(ci * ci / len(g) for ci, g in zip(c, groups)))


def test_example() -> None:
    res = scheffe(EXAMPLE, [[1, -1, 0], [0, 1, -1], [1, -0.5, -0.5]])
    mult = math.sqrt(2.0 * f_ppf(0.95, 2, 12))
    assert abs(mult - 2.7875773835545417) < 1e-9
    assert [r.estimate for r in res] == [-4.0, 3.0, -2.5]
    assert abs(res[0].se - 1.0) < 1e-12 and abs(res[2].se - math.sqrt(0.75)) < 1e-12
    assert abs(res[0].f - 8.0) < 1e-12 and abs(res[1].f - 4.5) < 1e-12
    assert abs(res[1].p - 0.03481542554547846) < 1e-10
    assert abs(res[1].lo - (3.0 - mult)) < 1e-12 and res[1].lo > 0.0
    assert res[2].hi < 0.0


def test_supremum_over_contrasts_is_k_minus_one_times_f() -> None:
    rng = random.Random(1)
    for _ in range(40):
        groups = [[rng.randint(0, 30) for _ in range(rng.randint(1, 6))] for _ in range(rng.randint(2, 5))]
        k, big_n = len(groups), sum(len(g) for g in groups)
        if big_n <= k:
            continue
        means, ssb, mse = exact_parts(groups)
        if mse == 0 or ssb == 0:
            continue
        top = ssb / mse
        best = [Fraction(len(g)) * (m - sum(len(h) * mh for h, mh in zip(groups, means)) / big_n)
                for g, m in zip(groups, means)]
        assert sum(best) == 0 and t2(best, groups, means, mse) == top  # attained, exactly
        for _ in range(200):  # no contrast does better
            c = [Fraction(rng.randint(-9, 9)) for _ in range(k)]
            c[-1] -= sum(c)
            if any(c):
                assert t2(c, groups, means, mse) <= top
        # the float code's best contrast gives the F-test: (k - 1) F = SSB / MSE
        f_test = float(ssb / (k - 1) / mse)
        r = scheffe(groups, [best_contrast(groups)])[0]
        assert abs(r.f - f_test) <= 1e-9 * f_test
        assert abs(r.p - f_sf(f_test, k - 1, big_n - k)) < 1e-12


def test_random_search_approaches_the_bound() -> None:
    rng = random.Random(2)
    groups = [[rng.gauss(mu, 1.0) for _ in range(n)] for mu, n in ((0.0, 4), (0.8, 6), (0.3, 5), (1.1, 7))]
    n, means, mse, _ = summary(groups)
    grand = sum(ni * m for ni, m in zip(n, means)) / sum(n)
    top = sum(ni * (m - grand) ** 2 for ni, m in zip(n, means)) / mse
    value = lambda c: (sum(ci * m for ci, m in zip(c, means))) ** 2 / (mse * sum(ci * ci / ni for ci, ni in zip(c, n)))
    c = [1.0, -1.0, 0.0, 0.0]
    for _ in range(4000):  # random local search over the contrast space
        d = [ci + rng.gauss(0.0, 0.1) for ci in c]
        mean_d = sum(d) / len(d)
        d = [di - mean_d for di in d]
        assert value(d) <= top * (1 + 1e-12)
        if value(d) > value(c):
            c = d
    assert value(c) > 0.999 * top


def test_f_test_rejects_iff_some_contrast_interval_excludes_zero() -> None:
    rng = random.Random(3)
    for _ in range(300):
        groups = [[rng.gauss(rng.choice((0.0, 0.6)), 1.0) for _ in range(4)] for _ in range(4)]
        n, means, mse, nu = summary(groups)
        grand = sum(means) / 4
        f = sum(4 * (m - grand) ** 2 for m in means) / 3 / mse
        rejects = f_sf(f, 3, nu) <= 0.05
        best = scheffe(groups, [best_contrast(groups)])[0]
        assert rejects == (best.lo > 0.0 or best.hi < 0.0)
        pairwise = scheffe(groups, [[1 if t == i else -1 if t == j else 0 for t in range(4)]
                                    for i in range(4) for j in range(i + 1, 4)])
        if any(r.lo > 0.0 or r.hi < 0.0 for r in pairwise):
            assert rejects  # a significant pair implies a significant F-test, not conversely


def test_simultaneous_coverage() -> None:
    rng = random.Random(4)
    reps, misses = 3000, 0
    mu = [0.0, 1.0, -0.5]
    for _ in range(reps):
        groups = [[rng.gauss(m, 2.0) for _ in range(n)] for m, n in zip(mu, (3, 5, 8))]
        best = best_contrast([[v - m for v in g] for g, m in zip(groups, mu)])
        r = scheffe(groups, [best])[0]
        truth = sum(c * m for c, m in zip(best, mu))
        misses += not (r.lo <= truth <= r.hi)  # the worst contrast misses iff any contrast misses
    assert abs(misses / reps - 0.05) < 4.0 * math.sqrt(0.05 * 0.95 / reps)


def test_errors() -> None:
    with pytest.raises(ValueError):
        scheffe(EXAMPLE, [[1, 1, 0]])
    with pytest.raises(ValueError):
        scheffe(EXAMPLE, [[1, -1]])
    with pytest.raises(ValueError):
        scheffe([[1.0, 1.0], [2.0, 2.0]], [[1, -1]])
