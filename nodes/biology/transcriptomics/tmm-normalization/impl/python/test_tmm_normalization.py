# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tmm-normalization/. The authors are listed in prov/TKHD07.jsonl.

import math
import random

import pytest

from biostoch import poisson
from tmm_normalization import (
    average_ranks,
    effective_library_sizes,
    norm_factors,
    quantile7,
    reference_column,
    tmm_factor,
)


def brute_force(obs, ref, m_trim=0.3, a_trim=0.05):
    """The same rule with ranks found by counting: rank = #smaller + (#equal + 1) / 2."""
    no, nr = sum(obs), sum(ref)
    genes = [(o, r) for o, r in zip(obs, ref) if o > 0 and r > 0]
    if not genes:
        return 1.0
    ms = [math.log2((o / no) / (r / nr)) for o, r in genes]
    av = [(math.log2(o / no) + math.log2(r / nr)) / 2 for o, r in genes]
    vs = [(no - o) / no / o + (nr - r) / nr / r for o, r in genes]
    if max(abs(x) for x in ms) < 1e-6:
        return 1.0
    n = len(ms)

    def rank(xs, i):
        return sum(x < xs[i] for x in xs) + (sum(x == xs[i] for x in xs) + 1) / 2

    lo_m = int(n * m_trim) + 1
    lo_a = int(n * a_trim) + 1
    kept = [i for i in range(n)
            if lo_m <= rank(ms, i) <= n + 1 - lo_m and lo_a <= rank(av, i) <= n + 1 - lo_a]
    if not kept:
        return 1.0
    return 2 ** (sum(ms[i] / vs[i] for i in kept) / sum(1 / vs[i] for i in kept))


def test_average_ranks():
    assert average_ranks([3.0, 1.0, 3.0, 2.0]) == [3.5, 1.0, 3.5, 2.0]
    assert average_ranks([5, 5, 5]) == [2.0, 2.0, 2.0]
    assert average_ranks([]) == []


def test_matches_brute_force_with_ties():
    rng = random.Random(21)
    for _ in range(200):
        n = rng.randint(1, 60)
        obs = [rng.randint(0, 12) for _ in range(n)]
        ref = [rng.randint(0, 12) for _ in range(n)]
        if sum(obs) == 0 or sum(ref) == 0:
            continue
        assert math.isclose(tmm_factor(obs, ref), brute_force(obs, ref), rel_tol=1e-12)


def test_swapping_the_samples_inverts_the_factor():
    # Real-valued counts, so that no two M values tie; with ties, rounding can
    # break them differently in the two directions.
    rng = random.Random(22)
    for _ in range(200):
        n = rng.randint(1, 80)
        obs = [rng.uniform(0.5, 40) for _ in range(n)]
        ref = [rng.uniform(0.5, 40) for _ in range(n)]
        assert math.isclose(tmm_factor(obs, ref) * tmm_factor(ref, obs), 1.0, rel_tol=1e-12)


def test_a_sample_against_itself_is_one():
    assert tmm_factor([5, 0, 7, 9], [5, 0, 7, 9]) == 1.0
    assert tmm_factor([0, 3], [4, 0]) == 1.0


def test_twice_as_many_genes_gives_one_half():
    # The case in Robinson and Oshlack (2010): sample A expresses the genes of B
    # at the same level and as many genes again, with the same depth.
    rng = random.Random(23)
    shared = [2 * rng.randint(5, 500) for _ in range(200)]
    depth = sum(shared)
    ref = shared + [0] * 200
    own = [rng.randint(1, 100) for _ in range(200)]
    own = [x * (depth // 2) / sum(own) for x in own]
    obs = [x // 2 for x in shared] + own
    assert tmm_factor(obs, ref, lib_obs=depth, lib_ref=depth) == 0.5


def outlier_case(rng, jitter):
    """Stable genes with obs = 3 r (1 + jitter), and u low and w high outliers, u, w <= floor(0.3 n)."""
    stable = rng.randint(5, 40)
    while True:
        low = rng.randint(0, stable)
        high = rng.randint(0, stable)
        if max(low, high) <= math.floor(0.3 * (stable + low + high)):
            break
    ref, obs = [], []
    for i in range(stable):
        r = rng.randint(10, 1000)
        ref.append(r)
        obs.append(3 * r * (1 + jitter * i))
    for _ in range(low):
        r = rng.randint(10, 1000)
        ref.append(r)
        obs.append(r * 0.01)
    for _ in range(high):
        r = rng.randint(10, 1000)
        ref.append(r)
        obs.append(r * 100)
    return obs, ref, stable


def test_outliers_within_the_trim_do_not_move_the_factor():
    rng = random.Random(24)
    for _ in range(200):
        obs, ref, stable = outlier_case(rng, 1e-5)
        no, nr = sum(obs), sum(ref)
        band = [math.log2((o / no) / (r / nr)) for o, r in zip(obs[:stable], ref[:stable])]
        f = math.log2(tmm_factor(obs, ref))
        assert min(band) - 1e-12 <= f <= max(band) + 1e-12


def test_rounding_can_split_a_tie_and_empty_the_kept_set():
    # With exact ratios 3 r / r, rounding gives two nearby M values; their average
    # ranks can both fall outside the kept range, and the factor falls back to 1.
    rng = random.Random(24)
    fallbacks = 0
    for _ in range(100):
        obs, ref, stable = outlier_case(rng, 0.0)
        if tmm_factor(obs, ref) == 1.0 and 3 * sum(ref) != sum(obs):
            fallbacks += 1
    assert fallbacks >= 1


def test_no_trimming_gives_the_weighted_mean_of_all_genes():
    obs = [10, 20, 30, 40]
    ref = [40, 30, 20, 10]
    no = nr = 100
    ms = [math.log2(o / r) for o, r in zip(obs, ref)]
    vs = [(no - o) / no / o + (nr - r) / nr / r for o, r in zip(obs, ref)]
    f = sum(m / v for m, v in zip(ms, vs)) / sum(1 / v for v in vs)
    assert math.isclose(tmm_factor(obs, ref, m_trim=0.0, a_trim=0.0), 2 ** f, rel_tol=1e-12)
    g = sum(ms) / 4
    assert math.isclose(tmm_factor(obs, ref, m_trim=0.0, a_trim=0.0, weighted=False), 2 ** g, rel_tol=1e-12)


def test_quantile7_and_reference():
    assert quantile7([1, 2, 3, 4], 0.75) == 3.25
    assert quantile7([7], 0.75) == 7
    counts = [[1, 2, 10], [2, 4, 0], [3, 6, 0], [4, 8, 10]]
    lib = [10, 20, 20]
    # upper quartiles over library size: 0.325, 0.325, 0.5; mean 0.383; ties go to the first
    assert reference_column(counts, lib) == 0
    zeros = [[0, 0, 0]] * 7 + [[1, 9, 4]]
    assert reference_column(zeros, [1, 9, 4]) == 1


def test_norm_factors_multiply_to_one_and_offsets():
    rng = random.Random(25)
    counts = [[rng.randint(0, 50) for _ in range(5)] for _ in range(100)] + [[0] * 5]
    f = norm_factors(counts)
    assert math.isclose(math.prod(f), 1.0, rel_tol=1e-12)
    eff = effective_library_sizes(counts, f)
    for j in range(5):
        assert math.isclose(eff[j], sum(row[j] for row in counts) * f[j])
    with pytest.raises(ValueError):
        norm_factors([])


def test_composition_measurement():
    # A measurement, not a theorem: 10 percent of the genes are 4 times higher in
    # sample 0. The true ratio of the factors is sum(q) / sum(q'), and TMM comes
    # within 3 percent of it, while the library sizes alone are about 30 percent off.
    rng = random.Random(26)
    q = [math.exp(rng.uniform(math.log(20), math.log(400))) for _ in range(800)]
    q2 = [x * 4 if g % 10 == 0 else x for g, x in enumerate(q)]
    depth = 100000
    a = [poisson(rng, x * depth / sum(q2)) for x in q2]
    b = [poisson(rng, x * depth / sum(q)) for x in q]
    f = norm_factors([[x, y] for x, y in zip(a, b)])
    truth = sum(q) / sum(q2)
    assert abs((f[0] / f[1]) / truth - 1) < 0.03
