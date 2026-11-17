# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genomic-control/. The authors are listed in prov/MQGC1J.jsonl.

import math
import random
from fractions import Fraction

from biostoch import chi2_sf
from genomic_control import (
    CHI2_1_MEDIAN,
    association_scan,
    genomic_control,
    inflation_factor,
    median,
    trend_statistic,
)


def armitage_from_table(cases, controls):
    """The textbook form on a 2 by 3 table with scores 0, 1, 2 (exact)."""
    R, S = sum(cases), sum(controls)
    N = R + S
    n = [cases[k] + controls[k] for k in range(3)]
    u = sum(k * (S * cases[k] - R * controls[k]) for k in range(3))
    v = Fraction(R * S, N) * (N * sum(k * k * n[k] for k in range(3)) - sum(k * n[k] for k in range(3)) ** 2)
    return Fraction(N * u * u) / (N * v)


def expand(cases, controls):
    dosage, status = [], []
    for k in range(3):
        dosage += [k] * cases[k] + [k] * controls[k]
        status += [1] * cases[k] + [0] * controls[k]
    return dosage, status


def lambda_sd(lam, m):
    """Large-sample sd of median/0.454936 for m values of lam * chi2_1."""
    x = CHI2_1_MEDIAN
    dens = math.exp(-x / 2) / math.sqrt(2 * math.pi * x)
    return lam / (2 * dens * math.sqrt(m)) / x


def test_median_constant():
    assert abs(CHI2_1_MEDIAN - 0.454936) < 1e-6
    assert abs(chi2_sf(CHI2_1_MEDIAN, 1) - 0.5) < 1e-12
    assert median([3, 1, 2]) == 2
    assert median([4, 1, 3, 2]) == 2.5


def test_trend_equals_armitage_form():
    cases, controls = (20, 50, 30), (35, 45, 20)
    d, s = expand(cases, controls)
    t = trend_statistic(d, s, exact=True)
    assert t == armitage_from_table(cases, controls)
    # N = 200, N Sxy - Sx Sy = 2500, N Sxx - Sx^2 = 20975, N Sy - Sy^2 = 10000.
    assert t == Fraction(200 * 2500 ** 2, 20975 * 10000) == Fraction(5000, 839)
    rng = random.Random(3)
    for _ in range(50):
        ca = tuple(rng.randint(0, 30) for _ in range(3))
        co = tuple(rng.randint(0, 30) for _ in range(3))
        n = [ca[k] + co[k] for k in range(3)]
        if sum(ca) == 0 or sum(co) == 0 or sum(1 for x in n if x) < 2:
            continue
        d, s = expand(ca, co)
        assert trend_statistic(d, s, exact=True) == armitage_from_table(ca, co)


def test_hand_example_of_the_page():
    stats = [0.10, 0.30, 0.62, 0.95, 2.40]
    lam, adj, p = genomic_control(stats)
    assert abs(lam - 0.62 / 0.454936423119572) < 1e-12
    assert abs(adj[4] - 2.40 / lam) < 1e-12
    assert abs(p[4] - chi2_sf(2.40 / lam, 1)) < 1e-15
    # A deflated scan is left alone.
    lam2, adj2, _ = genomic_control([0.1, 0.2, 0.3])
    assert lam2 == 1.0 and adj2 == [0.1, 0.2, 0.3]


def test_scaled_chi_square_recovers_lambda():
    rng = random.Random(11)
    m, lam0 = 20000, 1.3
    stats = [lam0 * rng.gauss(0.0, 1.0) ** 2 for _ in range(m)]
    lam, adj, p = genomic_control(stats)
    assert abs(lam - lam0) <= 4 * lambda_sd(lam0, m)
    assert abs(median(adj) - CHI2_1_MEDIAN) < 1e-12
    # After the correction, the share of p-values below 0.05 is near 0.05.
    k = sum(1 for x in p if x < 0.05)
    assert abs(k / m - 0.05) <= 4 * math.sqrt(0.05 * 0.95 / m)


def simulate_case_control(rng, n_per_pop, m, fst, case_rate):
    """Two populations of n_per_pop people each, m null SNPs.

    For each SNP: an ancestral frequency p ~ Uniform(0.1, 0.9), then a
    Balding-Nichols frequency for each population. Then, person by person,
    the status (case with probability case_rate[pop]) and the m genotypes.
    """
    c = (1 - fst) / fst
    freqs = []
    for _ in range(m):
        p = 0.1 + 0.8 * rng.random()
        freqs.append((rng.betavariate(c * p, c * (1 - p)), rng.betavariate(c * p, c * (1 - p))))
    G, y = [], []
    for pop in (0, 1):
        for _ in range(n_per_pop):
            y.append(1 if rng.random() < case_rate[pop] else 0)
            G.append([(rng.random() < f[pop]) + (rng.random() < f[pop]) for f in freqs])
    return G, y


def test_stratified_scan_is_inflated_and_corrected():
    rng = random.Random(5)
    m = 1500
    G, y = simulate_case_control(rng, 200, m, 0.01, (0.7, 0.3))
    stats, lam, adj, p = association_scan(G, y)
    assert lam > 1.0 + 4 * lambda_sd(1.0, m)
    assert abs(median(adj) - CHI2_1_MEDIAN) < 1e-12
    # Without a difference in case rates, the same structure gives no inflation.
    G2, y2 = simulate_case_control(rng, 200, m, 0.01, (0.5, 0.5))
    stats2 = association_scan(G2, y2)[0]
    assert abs(inflation_factor(stats2) - 1.0) <= 4 * lambda_sd(1.0, m)
