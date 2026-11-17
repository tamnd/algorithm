# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/median-of-ratios-normalization/. The authors are listed in prov/NF2283.jsonl.

import math
import random

import pytest

from biostoch import poisson
from median_of_ratios_normalization import log_geometric_means, normalized_counts, size_factors

PAGE = [
    [100, 200, 100],
    [50, 100, 50],
    [20, 40, 20],
    [300, 600, 3000],
    [0, 10, 5],
]


def close(a, b, rel=1e-12):
    return all(math.isclose(x, y, rel_tol=rel) for x, y in zip(a, b, strict=True))


def geomean(xs):
    return math.exp(sum(math.log(x) for x in xs) / len(xs))


def brute_force(counts):
    """Ratios on the plain scale, an explicit sort, and the median of the middle one or two."""
    m = len(counts[0])
    rows = [row for row in counts if all(k > 0 for k in row)]
    out = []
    for j in range(m):
        ratios = sorted(row[j] / math.prod(row) ** (1.0 / m) for row in rows)
        n = len(ratios)
        if n % 2:
            out.append(ratios[n // 2])
        else:
            out.append(math.sqrt(ratios[n // 2 - 1] * ratios[n // 2]))
    return out


def test_page_example():
    s = size_factors(PAGE)
    assert close(s, [2 ** (-1 / 3), 2 ** (2 / 3), 2 ** (-1 / 3)])
    assert math.isinf(log_geometric_means(PAGE)[4])


def test_exact_product_form_gives_factors_over_their_geometric_mean():
    rng = random.Random(11)
    for _ in range(50):
        m = rng.randint(2, 6)
        n = rng.randint(1, 30)
        s = [rng.uniform(0.2, 5.0) for _ in range(m)]
        q = [rng.uniform(1.0, 1000.0) for _ in range(n)]
        counts = [[s[j] * q[g] for j in range(m)] for g in range(n)]
        g = geomean(s)
        assert close(size_factors(counts), [x / g for x in s], rel=1e-10)


def test_matches_brute_force_on_random_counts():
    rng = random.Random(12)
    for _ in range(200):
        m = rng.randint(1, 5)
        n = rng.randint(1, 25)
        counts = [[rng.randint(0, 50) for _ in range(m)] for _ in range(n)]
        if not any(all(k > 0 for k in row) for row in counts):
            with pytest.raises(ValueError):
                size_factors(counts)
            continue
        assert close(size_factors(counts), brute_force(counts), rel=1e-9)


def test_a_majority_of_unchanged_genes_fixes_the_factors():
    rng = random.Random(13)
    s = [0.5, 1.0, 3.0]
    for _ in range(100):
        stable = rng.randint(3, 12)
        changed = rng.randint(0, stable - 1)
        counts = []
        for _ in range(stable):
            q = rng.uniform(5, 500)
            counts.append([s[j] * q for j in range(3)])
        for _ in range(changed):
            counts.append([rng.uniform(1, 5000) for _ in range(3)])
        rng.shuffle(counts)
        g = geomean(s)
        assert close(size_factors(counts), [x / g for x in s], rel=1e-10)


def test_scaling_one_sample_scales_its_ratio_to_the_others():
    rng = random.Random(14)
    for _ in range(50):
        counts = [[rng.randint(1, 100) for _ in range(4)] for _ in range(rng.randint(1, 20))]
        c = rng.choice([0.25, 2.0, 3.0, 10.0])
        scaled = [row[:2] + [row[2] * c] + row[3:] for row in counts]
        a = size_factors(counts)
        b = size_factors(scaled)
        for j in (0, 1, 3):
            assert math.isclose((b[2] / b[j]) / (a[2] / a[j]), c, rel_tol=1e-10)


def test_fixed_reference_scales_new_samples_the_same_way():
    rng = random.Random(15)
    counts = [[rng.randint(1, 200) for _ in range(5)] for _ in range(40)]
    lg = log_geometric_means(counts)
    full = size_factors(counts)
    part = size_factors([row[1:3] for row in counts], log_geo_means=lg)
    assert close(part, full[1:3])


def test_normalized_counts_divide_by_the_factors():
    s = size_factors(PAGE)
    nc = normalized_counts(PAGE)
    for g, row in enumerate(PAGE):
        assert close(nc[g], [row[j] / s[j] for j in range(3)])
    assert close(nc[0], [100 * 2 ** (1 / 3)] * 3)


def test_errors():
    with pytest.raises(ValueError):
        size_factors([])
    with pytest.raises(ValueError):
        size_factors([[0, 1], [3, 0]])
    with pytest.raises(ValueError):
        size_factors([[1, 2], [3]])
    with pytest.raises(ValueError):
        size_factors([[1, -2]])


def test_poisson_counts_measurement():
    # A measurement, not a theorem: with Poisson counts of mean s_j q_g and
    # q_g from 50 to 1000, the factors come within 3 percent of s / geomean(s).
    rng = random.Random(16)
    s = [0.5, 1.0, 2.0, 4.0]
    counts = []
    for _ in range(600):
        q = math.exp(rng.uniform(math.log(50), math.log(1000)))
        counts.append([poisson(rng, s[j] * q) for j in range(4)])
    g = geomean(s)
    est = size_factors(counts)
    for j in range(4):
        assert abs(est[j] / (s[j] / g) - 1) < 0.03
