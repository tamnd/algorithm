# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rosenbaum-sensitivity-analysis/. The authors are listed in prov/4KS2ZT.jsonl.

import itertools
import math
import random
from fractions import Fraction as Fr

import pytest

from rosenbaum_sensitivity_analysis import (
    bernoulli_sum_law,
    doubled_midranks,
    normal_upper_bound,
    sensitivity_value,
    sign_test_bounds,
    signed_rank_bounds,
)

# The example of the page (the same differences as the signed-rank test page).
EX = [Fr(18, 10), Fr(-6, 10), Fr(31, 10), Fr(24, 10), Fr(-13, 10), Fr(9, 10), Fr(22, 10), 0, Fr(15, 10), Fr(-4, 10)]


def wplus(d):
    kept = [v for v in d if v != 0]
    r2 = doubled_midranks([abs(v) for v in kept])
    return Fr(sum(r for r, v in zip(r2, kept) if v > 0), 2)


def test_worked_example():
    t, lo, hi = signed_rank_bounds(EX, 1)
    assert t == 38 and lo == hi == Fr(19, 512)
    t, lo, hi = signed_rank_bounds(EX, Fr(3, 2))
    assert lo == Fr(19712, 1953125) and hi == Fr(201933, 1953125)
    t, lo, hi = signed_rank_bounds(EX, 2)
    assert lo == Fr(67, 19683) and hi == Fr(3584, 19683)
    g = sensitivity_value(lambda x: float(signed_rank_bounds(EX, Fr(x))[2]), 0.05)
    assert abs(g - 1.1133) < 1e-3
    g10 = sensitivity_value(lambda x: float(signed_rank_bounds(EX, Fr(x))[2]), 0.10)
    assert abs(g10 - 1.4775) < 1e-3
    # the sign test on the same differences: 6 of 9 signs positive
    assert sign_test_bounds(6, 9, 1) == (Fr(130, 512), Fr(130, 512))
    # exercise 2 of the page
    assert sign_test_bounds(9, 10, 1)[1] == Fr(11, 1024)
    assert sign_test_bounds(9, 10, 2)[1] == Fr(6144, 59049)


def test_hammond_binary_pairs():
    """110 of 122 discordant pairs had the lung cancer death in the smoker."""
    lo, hi = sign_test_bounds(110, 122, 1)
    assert lo == hi and hi < Fr(1, 10**20)
    _, hi5 = sign_test_bounds(110, 122, 5)
    _, hi6 = sign_test_bounds(110, 122, 6)
    assert 0.023 < hi5 < 0.0235 and 0.096 < hi6 < 0.098
    g = sensitivity_value(lambda x: float(sign_test_bounds(110, 122, Fr(x))[1]), 0.05)
    assert 5.4 < g < 5.5


def test_gamma_one_is_the_exact_signed_rank_p_value():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(0, 9)
        d = [rng.randint(-4, 4) for _ in range(n)]
        t, lo, hi = signed_rank_bounds(d, 1)
        kept = [v for v in d if v != 0]
        a = [abs(v) for v in kept]
        count = 0
        for signs in itertools.product((1, -1), repeat=len(kept)):
            if wplus([s * v for s, v in zip(signs, a)]) >= t:
                count += 1
        assert lo == hi == Fr(count, 2 ** len(kept))


def exact_tail(r1, r2, pi, t_obs):
    """Pr[W+ >= t_obs] when unit 1 of pair s is treated with probability pi[s], under the sharp null."""
    total = Fr(0)
    for z in itertools.product((0, 1), repeat=len(pi)):
        pr = Fr(1)
        for zs, p in zip(z, pi):
            pr *= p if zs else 1 - p
        d = [(a - b) if zs else (b - a) for zs, a, b in zip(z, r1, r2)]
        if wplus(d) >= t_obs:
            total += pr
    return total


def test_bounds_against_enumeration_of_worst_case_assignments():
    rng = random.Random(2026)
    for _ in range(80):
        n = rng.randint(1, 6)
        r1 = [rng.randint(0, 5) for _ in range(n)]
        r2 = [rng.randint(0, 5) for _ in range(n)]
        z_obs = [rng.randint(0, 1) for _ in range(n)]
        d_obs = [(a - b) if z else (b - a) for z, a, b in zip(z_obs, r1, r2)]
        gamma = Fr(rng.randint(2, 8), 2)
        lo_p, hi_p = 1 / (1 + gamma), gamma / (1 + gamma)
        t, lo, hi = signed_rank_bounds(d_obs, gamma)
        tails = [exact_tail(r1, r2, pi, t) for pi in itertools.product((lo_p, hi_p), repeat=n)]
        assert max(tails) == hi and min(tails) == lo
        # an interior law also stays inside the bounds
        pi = [lo_p + (hi_p - lo_p) * Fr(rng.randint(0, 10), 10) for _ in range(n)]
        assert lo <= exact_tail(r1, r2, pi, t) <= hi


def test_sign_test_bounds_against_enumeration():
    rng = random.Random(4)
    for _ in range(100):
        n = rng.randint(1, 7)
        k = rng.randint(0, n)
        gamma = Fr(rng.randint(2, 9), 2)
        lo_p, hi_p = 1 / (1 + gamma), gamma / (1 + gamma)
        tails = []
        for pi in itertools.product((lo_p, hi_p), repeat=n):
            tail = Fr(0)
            for z in itertools.product((0, 1), repeat=n):
                if sum(z) >= k:
                    pr = Fr(1)
                    for zs, p in zip(z, pi):
                        pr *= p if zs else 1 - p
                    tail += pr
            tails.append(tail)
        assert (min(tails), max(tails)) == sign_test_bounds(k, n, gamma)


def test_monotone_in_gamma():
    rng = random.Random(9)
    for _ in range(100):
        d = [rng.randint(-5, 9) for _ in range(rng.randint(1, 12))]
        prev_lo, prev_hi = None, None
        for g in (1, Fr(5, 4), Fr(3, 2), 2, 3, 5):
            _, lo, hi = signed_rank_bounds(d, g)
            assert lo <= hi
            if prev_hi is not None:
                assert hi >= prev_hi and lo <= prev_lo
            prev_lo, prev_hi = lo, hi


def test_law_moments_match_normal_approximation_inputs():
    rng = random.Random(12)
    for _ in range(100):
        q = [rng.randint(1, 12) for _ in range(rng.randint(1, 10))]
        p = Fr(rng.randint(1, 9), 10)
        law = bernoulli_sum_law(q, p)
        assert sum(law) == 1
        mean = sum(v * w for v, w in enumerate(law))
        var = sum(v * v * w for v, w in enumerate(law)) - mean * mean
        assert mean == p * sum(q) and var == p * (1 - p) * sum(x * x for x in q)


def test_normal_approximation_is_close_for_moderate_n():
    rng = random.Random(1)
    d = [round(rng.gauss(0.3, 1), 1) for _ in range(40)]
    for g in (1.0, 1.5, 2.0):
        exact = float(signed_rank_bounds([Fr(str(v)) for v in d], Fr(g))[2])
        assert abs(normal_upper_bound(d, g) - exact) < 0.03


def test_float_gamma_and_errors():
    _, lo, hi = signed_rank_bounds([float(v) for v in EX], 2.0)
    assert math.isclose(hi, 3584 / 19683, rel_tol=1e-12)
    assert math.isclose(lo, 67 / 19683, rel_tol=1e-12)
    with pytest.raises(ValueError):
        signed_rank_bounds(EX, Fr(1, 2))
    with pytest.raises(ValueError):
        sign_test_bounds(5, 4, 2)
    assert signed_rank_bounds([0, 0], 3) == (0, 1, 1)
    assert sensitivity_value(lambda g: 0.5, 0.05) == 1.0
    assert sensitivity_value(lambda g: 0.0, 0.05, hi=50.0) == 50.0
