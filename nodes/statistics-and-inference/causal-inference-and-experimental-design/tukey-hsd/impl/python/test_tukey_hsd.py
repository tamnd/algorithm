# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tukey-hsd/. The authors are listed in prov/N35W2Z.jsonl.

import math
import random
from fractions import Fraction

import pytest

from srange import range_sf, srange_ppf, srange_sf
from stdist import norm_sf, t_sf
from tukey_hsd import means_and_mse, tukey_hsd

EXAMPLE = [[5, 7, 6, 8, 4], [9, 11, 10, 12, 8], [6, 8, 7, 5, 9]]


def test_two_means_is_the_t_law() -> None:
    # With k = 2 the range is |Z1 - Z2| = sqrt(2) |N(0, 1)|, so P(Q > q) = 2 P(T > q / sqrt(2)).
    for nu in (1, 2, 5, 12, 40, 1000):
        for q in (0.2, 1.0, 2.0, 3.5, 6.0, 10.0):
            assert abs(srange_sf(q, 2, nu) - 2.0 * t_sf(q / math.sqrt(2.0), nu)) < 1e-12
    for w in (0.1, 1.0, 3.0, 6.0):
        assert abs(range_sf(w, 2) - 2.0 * norm_sf(w / math.sqrt(2.0))) < 1e-15


def test_range_of_three_closed_form() -> None:
    # Known values of P(R <= w) for the range of 3 standard normals (k = 3, nu = inf):
    # the 0.95 quantile is 3.314 and the 0.99 quantile is 4.120 to the 3 decimals of the tables.
    assert abs(srange_ppf(0.95, 3, math.inf) - 3.314) < 5e-4
    assert abs(srange_ppf(0.99, 3, math.inf) - 4.120) < 5e-4


def test_table_values() -> None:
    # Upper 5% points of the studentized range, as printed to 3 decimals.
    for k, nu, q in ((3, 10, 3.877), (5, 5, 5.673), (10, 20, 5.008)):
        assert abs(srange_ppf(0.95, k, nu) - q) < 5e-4


def test_against_monte_carlo() -> None:
    rng = random.Random(4)
    reps, k, nu = 20000, 4, 10
    draws = []
    for _ in range(reps):
        z = [rng.gauss(0.0, 1.0) for _ in range(k)]
        s = math.sqrt(sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu)) / nu)
        draws.append((max(z) - min(z)) / s)
    for q in (2.0, 3.0, 4.0, 5.0):
        p = srange_sf(q, k, nu)
        observed = sum(d > q for d in draws) / reps
        assert abs(observed - p) < 4.5 * math.sqrt(p * (1 - p) / reps)


def test_example() -> None:
    q_crit, pairs = tukey_hsd(EXAMPLE)
    assert abs(q_crit - 3.7729289657270066) < 1e-8
    got = {(p.i, p.j): p for p in pairs}
    assert [round(got[key].diff, 12) for key in ((0, 1), (0, 2), (1, 2))] == [-4.0, -1.0, 3.0]
    assert abs(got[0, 1].q - 4.0 * math.sqrt(2.0)) < 1e-12
    assert abs(got[0, 1].p - 0.004634080571702173) < 1e-9
    assert abs(got[1, 2].p - 0.02772191558007049) < 1e-9
    assert abs(got[0, 2].p - 0.590770608320337) < 1e-9
    assert got[0, 1].hi < 0.0 and got[1, 2].lo > 0.0 and got[0, 2].lo < 0.0 < got[0, 2].hi


def test_statistic_against_fractions() -> None:
    rng = random.Random(7)
    for _ in range(40):
        groups = [[rng.randint(0, 40) for _ in range(rng.randint(1, 6))] for _ in range(rng.randint(2, 5))]
        k, big_n = len(groups), sum(len(g) for g in groups)
        means = [Fraction(sum(g), len(g)) for g in groups]
        ssw = sum((v - m) ** 2 for g, m in zip(groups, means) for v in g)
        if big_n <= k or ssw == 0:
            continue
        mse = ssw / (big_n - k)
        _, mse_f, nu = means_and_mse(groups)
        assert nu == big_n - k and abs(mse_f - float(mse)) <= 1e-12 * float(mse)
        for i in range(k):
            for j in range(i + 1, k):
                q2 = (means[i] - means[j]) ** 2 / (mse / 2 * (Fraction(1, len(groups[i])) + Fraction(1, len(groups[j]))))
                se = math.sqrt(0.5 * mse_f * (1.0 / len(groups[i]) + 1.0 / len(groups[j])))
                q = abs(float(means[i] - means[j])) / se
                assert abs(q * q - float(q2)) <= 1e-10 * max(1.0, float(q2))


def test_two_groups_match_the_pooled_t_test() -> None:
    rng = random.Random(8)
    for _ in range(3):
        x = [rng.gauss(0.0, 1.0) for _ in range(rng.randint(2, 8))]
        y = [rng.gauss(0.7, 1.0) for _ in range(rng.randint(2, 8))]
        _, [pair] = tukey_hsd([x, y])
        mx, my = sum(x) / len(x), sum(y) / len(y)
        sp2 = (sum((v - mx) ** 2 for v in x) + sum((v - my) ** 2 for v in y)) / (len(x) + len(y) - 2)
        t = (mx - my) / math.sqrt(sp2 * (1 / len(x) + 1 / len(y)))
        assert abs(pair.q - math.sqrt(2.0) * abs(t)) < 1e-12
        assert abs(pair.p - 2.0 * t_sf(abs(t), len(x) + len(y) - 2)) < 1e-12


def family_wise_error(seed: int, sizes: list[int], reps: int) -> float:
    rng = random.Random(seed)
    k, nu = len(sizes), sum(sizes) - len(sizes)
    q_crit = srange_ppf(0.95, k, nu)
    hits = 0
    for _ in range(reps):
        groups = [[rng.gauss(0.0, 1.0) for _ in range(n)] for n in sizes]
        means, mse, _ = means_and_mse(groups)
        worst = max(abs(means[i] - means[j]) / math.sqrt(0.5 * mse * (1 / sizes[i] + 1 / sizes[j]))
                    for i in range(k) for j in range(i + 1, k))
        hits += worst > q_crit
    return hits / reps


def test_family_wise_error_is_alpha_when_balanced() -> None:
    reps = 6000
    rate = family_wise_error(1, [5, 5, 5, 5], reps)
    assert abs(rate - 0.05) < 4.0 * math.sqrt(0.05 * 0.95 / reps)


def test_tukey_kramer_is_conservative() -> None:
    reps = 6000
    rate = family_wise_error(3, [2, 2, 30, 30], reps)
    assert rate < 0.05 + 3.0 * math.sqrt(0.05 * 0.95 / reps)


def test_errors() -> None:
    with pytest.raises(ValueError):
        tukey_hsd([[1.0, 2.0]])
    with pytest.raises(ValueError):
        tukey_hsd([[1.0, 1.0], [2.0, 2.0]])
    with pytest.raises(ValueError):
        srange_ppf(1.0, 3, 10)
