# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/g-means/. The authors are listed in prov/3WDD1J.jsonl.

import math
import random

from g_means import anderson_darling, check_cluster, g_means, normal_cdf, principal_direction


def blobs(rng, centers, m, sd=1.0):
    return [tuple(c + rng.gauss(0, sd) for c in cen) for cen in centers for _ in range(m)]


def test_statistic_matches_second_formula() -> None:
    # A^2 = -n - (1/n) sum_i [(2i - 1) log z_i + (2(n - i) + 1) log(1 - z_i)]
    rng = random.Random(3)
    for _ in range(50):
        n = rng.randrange(8, 60)
        v = [rng.uniform(-3, 3) ** 3 for _ in range(n)]
        mu = sum(v) / n
        sd = math.sqrt(sum((x - mu) ** 2 for x in v) / (n - 1))
        z = sorted(normal_cdf((x - mu) / sd) for x in v)
        s = sum((2 * i - 1) * math.log(z[i - 1]) + (2 * (n - i) + 1) * math.log(1 - z[i - 1]) for i in range(1, n + 1))
        a2 = (-n - s / n) * (1 + 4 / n - 25 / n**2)
        assert abs(anderson_darling(v) - a2) < 1e-9 * max(1.0, abs(a2))


def test_false_alarm_rate_on_gaussian_data() -> None:
    rng = random.Random(11)
    trials = 400
    over_05 = sum(anderson_darling([rng.gauss(0, 1) for _ in range(60)]) > 0.752 for _ in range(trials))
    over_0001 = sum(anderson_darling([rng.gauss(0, 1) for _ in range(60)]) > 1.8692 for _ in range(trials))
    # 0.752 is near the 5 percent point for estimated mean and variance, so the
    # bounds are wide; 1.8692 is the 0.01 percent point used by Hamerly and Elkan.
    assert 0.01 * trials <= over_05 <= 0.10 * trials
    assert over_0001 <= 3


def test_bimodal_projection_is_rejected() -> None:
    rng = random.Random(5)
    v = [rng.gauss(-3, 1) for _ in range(100)] + [rng.gauss(3, 1) for _ in range(100)]
    assert anderson_darling(v) > 1.8692


def test_principal_direction() -> None:
    rng = random.Random(2)
    x = [(rng.gauss(0, 5), rng.gauss(0, 1)) for _ in range(400)]
    s, lam = principal_direction(x, rng)
    assert abs(abs(s[0]) - 1) < 1e-3
    assert 15 < lam < 35


def test_check_cluster() -> None:
    rng = random.Random(9)
    one = blobs(rng, [(0, 0)], 200)
    two = blobs(rng, [(-4, 0), (4, 0)], 100)
    c1 = tuple(sum(p[t] for p in one) / len(one) for t in range(2))
    c2 = tuple(sum(p[t] for p in two) / len(two) for t in range(2))
    assert check_cluster(one, c1, rng, 1.8692)[0] is False
    split, kids = check_cluster(two, c2, rng, 1.8692)
    assert split is True
    assert sorted(round(k[0] / 4) for k in kids) == [-1, 1]


def test_page_example() -> None:
    far = [(float(x),) for x in list(range(10)) + list(range(30, 40))]
    near = [(float(x),) for x in list(range(10)) + list(range(20, 30))]
    assert abs(anderson_darling([p[0] for p in far]) - 2.0019) < 1e-3
    assert abs(anderson_darling(list(range(10))) - 0.1623) < 1e-3
    assert abs(anderson_darling([p[0] for p in near]) - 1.3047) < 1e-3
    centers, _ = g_means(far, random.Random(0))
    assert sorted(c[0] for c in centers) == [4.5, 34.5]
    centers, _ = g_means(near, random.Random(0))
    assert centers == [(14.5,)]


def test_g_means_finds_blobs() -> None:
    for seed in range(3):
        rng = random.Random(seed)
        true = [(0, 0), (10, 0), (0, 10), (10, 10)]
        x = blobs(rng, true, 100)
        centers, labels = g_means(x, rng)
        assert len(centers) == 4
        assert sorted((round(c[0] / 10), round(c[1] / 10)) for c in centers) == [(0, 0), (0, 1), (1, 0), (1, 1)]


def test_g_means_one_blob_and_cap() -> None:
    rng = random.Random(1)
    centers, _ = g_means(blobs(rng, [(2, 2)], 300), rng)
    assert len(centers) == 1
    rng = random.Random(2)
    x = blobs(rng, [(i * 20, 0) for i in range(6)], 40, sd=0.5)
    centers, _ = g_means(x, rng, k_max=3)
    assert len(centers) <= 3
