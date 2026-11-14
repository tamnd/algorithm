# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sample-size-determination/. The authors are listed in prov/43QS5G.jsonl.

import math
import random

import pytest

from sample_size_determination import (
    t_power, t_sample_size, z_power, z_sample_size, z_sample_size_formula, z_width_sample_size,
)
from stdist import norm_ppf, t_ppf


def test_known_values() -> None:
    # Two samples, d = 0.5, alpha = 0.05 two-sided, power 0.8: 63 by z, 64 by t.
    assert z_sample_size_formula(0.5, 1.0, groups=2) == 63
    assert z_sample_size(0.5, 1.0, groups=2) == 63
    assert t_sample_size(0.5, 1.0, groups=2) == 64
    # One sample, d = 0.5: 32 by z, 34 by t.
    assert z_sample_size(0.5, 1.0) == 32
    assert t_sample_size(0.5, 1.0) == 34
    # Only delta / sigma matters.
    assert t_sample_size(5.0, 10.0, groups=2) == 64


def test_formula_matches_closed_form() -> None:
    z = norm_ppf(0.975) + norm_ppf(0.8)
    for d in [0.1, 0.25, 0.5, 1.0, 2.0]:
        assert z_sample_size_formula(d, 1.0) == math.ceil((z / d) ** 2)
        assert z_sample_size_formula(d, 1.0, groups=2) == math.ceil(2 * (z / d) ** 2)


def brute_smallest(power_fn, target: float, start: int) -> int:
    n = start
    while power_fn(n) < target:
        n += 1
    return n


@pytest.mark.parametrize("sides", [1, 2])
@pytest.mark.parametrize("groups", [1, 2])
def test_z_search_against_upward_scan(sides: int, groups: int) -> None:
    for d in [0.3, 0.45, 0.8, 1.3]:
        for target in [0.3, 0.5, 0.8, 0.95]:
            got = z_sample_size(d, 1.0, 0.05, target, sides, groups)
            want = brute_smallest(lambda n: z_power(n, d, 1.0, 0.05, sides, groups), target, 1)
            assert got == want


def test_far_tail_can_save_one_observation() -> None:
    # alpha = 0.05, power 0.3, d = 0.05: the closed form says 825, the exact power gives 824.
    assert z_sample_size_formula(0.05, 1.0, 0.05, 0.3) == 825
    assert z_sample_size(0.05, 1.0, 0.05, 0.3) == 824


@pytest.mark.parametrize("sides", [1, 2])
@pytest.mark.parametrize("groups", [1, 2])
def test_t_power_at_the_null_is_alpha(sides: int, groups: int) -> None:
    for n in [2, 3, 5, 12, 40, 200]:
        for alpha in [0.001, 0.01, 0.05, 0.2]:
            assert abs(t_power(n, 1e-12, 1.0, alpha, sides, groups) - alpha) < 1e-8


def test_t_power_is_below_z_power() -> None:
    for n in [2, 5, 10, 30]:
        for d in [0.2, 0.5, 1.0]:
            for sides in (1, 2):
                assert t_power(n, d, 1.0, 0.05, sides) <= z_power(n, d, 1.0, 0.05, sides) + 1e-9


def simulated_t_power(n: int, delta: float, groups: int, r: int, rng: random.Random) -> float:
    """Monte Carlo power of the two-sided t-test at level 0.05, sigma = 1."""
    nu = groups * (n - 1)
    c = t_ppf(0.975, nu)
    hits = 0
    for _ in range(r):
        x = [rng.gauss(delta, 1.0) for _ in range(n)]
        mx = math.fsum(x) / n
        ss = math.fsum((v - mx) ** 2 for v in x)
        if groups == 1:
            se = math.sqrt(ss / (n - 1) / n)
            diff = mx
        else:
            y = [rng.gauss(0.0, 1.0) for _ in range(n)]
            my = math.fsum(y) / n
            ss += math.fsum((v - my) ** 2 for v in y)
            se = math.sqrt(ss / nu * 2.0 / n)
            diff = mx - my
        hits += abs(diff / se) > c
    return hits / r


@pytest.mark.parametrize("n,delta,groups,seed", [(10, 1.0, 1, 1), (6, 1.2, 2, 2), (3, 2.0, 1, 3)])
def test_t_power_against_monte_carlo(n: int, delta: float, groups: int, seed: int) -> None:
    r = 6000
    exact = t_power(n, delta, 1.0, 0.05, 2, groups)
    sim = simulated_t_power(n, delta, groups, r, random.Random(seed))
    assert abs(sim - exact) < 4.0 * math.sqrt(exact * (1.0 - exact) / r)


def test_t_sample_size_is_the_smallest() -> None:
    for d, groups in [(0.8, 1), (1.0, 2), (1.5, 1)]:
        n = t_sample_size(d, 1.0, groups=groups)
        assert n == brute_smallest(lambda m: t_power(m, d, 1.0, 0.05, 2, groups), 0.8, 2)
        assert t_power(n, d, 1.0, 0.05, 2, groups) >= 0.8 > t_power(n - 1, d, 1.0, 0.05, 2, groups)


def test_width() -> None:
    # Half-width 0.5 with sigma = 2: (1.96 * 2 / 0.5)^2 = 61.46, so 62.
    assert z_width_sample_size(0.5, 2.0) == 62
    n = z_width_sample_size(0.1, 1.0, 0.01)
    z = norm_ppf(0.995)
    assert z / math.sqrt(n) <= 0.1 < z / math.sqrt(n - 1)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        z_sample_size(0.0, 1.0)
    with pytest.raises(ValueError):
        t_power(10, 0.5, -1.0)
    with pytest.raises(ValueError):
        z_sample_size(0.5, 1.0, sides=3)
