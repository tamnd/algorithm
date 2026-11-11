# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-sampling-over-lattices/. The authors are listed in prov/MWVGYZ.jsonl.
# Statistical tests with fixed seeds. The chi-square limits are loose
# (degrees of freedom plus five standard deviations) so that they test the
# shape of the distribution, not the luck of one seed.

import math
import random
from collections import Counter

from gaussian_sampling_over_lattices import CDTSampler, gram_schmidt, klein, sample_z_rejection, smoothing_parameter_z_bound


def chi_square(counts, probs, total):
    """Pool the tail cells with expected count below 5 into one cell."""
    stat, df, pool_obs, pool_exp = 0.0, -1, 0, 0.0
    for key, p in probs.items():
        exp = p * total
        if exp < 5:
            pool_obs += counts.get(key, 0)
            pool_exp += exp
            continue
        stat += (counts.get(key, 0) - exp) ** 2 / exp
        df += 1
    if pool_exp > 0:
        stat += (pool_obs - pool_exp) ** 2 / max(pool_exp, 1.0)
        df += 1
    return stat, df


def test_cdt_matches_pmf():
    rng = random.Random(1)
    cdt = CDTSampler(s=6.0)
    n = 20000
    counts = Counter(cdt.sample(rng) for _ in range(n))
    stat, df = chi_square(counts, dict(zip(cdt.values, cdt.pmf)), n)
    assert stat < df + 5 * math.sqrt(2 * df)


def test_cdt_variance_close_to_sigma_squared():
    rng = random.Random(2)
    s = 10.0
    cdt = CDTSampler(s)
    xs = [cdt.sample(rng) for _ in range(20000)]
    var = sum(x * x for x in xs) / len(xs)
    sigma2 = s * s / (2 * math.pi)  # s is far above the smoothing parameter of Z
    assert abs(var - sigma2) < 0.05 * sigma2


def test_rejection_sampler_with_center():
    rng = random.Random(3)
    s, c = 5.0, 0.3
    n = 20000
    xs = [sample_z_rejection(s, c, rng) for _ in range(n)]
    support = range(-20, 21)
    w = {x: math.exp(-math.pi * (x - c) ** 2 / s ** 2) for x in support}
    total = sum(w.values())
    stat, df = chi_square(Counter(xs), {x: w[x] / total for x in support}, n)
    assert stat < df + 5 * math.sqrt(2 * df)
    assert abs(sum(xs) / n - c) < 0.05


def test_klein_2d_outputs_lattice_points_with_gaussian_law():
    rng = random.Random(4)
    basis = [[2, 1], [1, 3]]
    gs = gram_schmidt(basis)
    s, c = 9.0, (0.5, 0.25)
    n = 12000
    pts = [tuple(klein(basis, s, c, rng, gs)) for _ in range(n)]
    # every output is an integer combination of the basis (det = 5)
    for x, y in pts[:200]:
        a = (3 * x - y) / 5
        b = (2 * y - x) / 5
        assert a == int(a) and b == int(b)
    # compare with D_{L,s,c} on the lattice points of a large box
    lattice = {(2 * a + b, a + 3 * b) for a in range(-30, 31) for b in range(-30, 31)}
    w = {p: math.exp(-math.pi * ((p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2) / s ** 2) for p in lattice}
    total = sum(w.values())
    stat, df = chi_square(Counter(pts), {p: w[p] / total for p in lattice}, n)
    assert stat < df + 5 * math.sqrt(2 * df)


def test_smoothing_bound_value():
    # eta_eps(Z) <= sqrt(ln(2 + 2/eps) / pi); for eps = 2^-64 this is about 3.8
    assert 3.7 < smoothing_parameter_z_bound(2.0 ** -64) < 3.9
