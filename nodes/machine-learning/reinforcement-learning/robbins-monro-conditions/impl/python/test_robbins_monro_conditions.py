# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robbins-monro-conditions/. The authors are listed in prov/W0MVTZ.jsonl.

import random
from fractions import Fraction

import pytest

from robbins_monro_conditions import exact_mse, noise_floor, noisy_iteration, power_steps_meet_conditions, reach

GAUSS = lambda r: r.gauss(0.0, 1.0)  # noqa: E731


def test_power_steps() -> None:
    assert power_steps_meet_conditions(Fraction(1)) == (True, True)
    assert power_steps_meet_conditions(Fraction(3, 4)) == (True, True)
    assert power_steps_meet_conditions(Fraction(1, 2)) == (True, False)
    assert power_steps_meet_conditions(Fraction(2, 5)) == (True, False)
    assert power_steps_meet_conditions(Fraction(2)) == (False, True)
    with pytest.raises(ValueError):
        power_steps_meet_conditions(Fraction(0))


def test_harmonic_steps_give_sigma2_over_n_exactly() -> None:
    # With a_n = 1/(n+1) the iterate is the sample mean, so e_n = sigma^2 / n for n >= 1.
    e = exact_mse(lambda n: Fraction(1, n + 1), 200, Fraction(7), Fraction(3))
    assert all(e[n] == Fraction(3, n) for n in range(1, 201))


def test_harmonic_steps_converge_with_seeds() -> None:
    finals = [noisy_iteration(0.0, 1.0, lambda n: 1.0 / (n + 1), 1000, GAUSS, random.Random(s))[-1] for s in range(400)]
    mse = sum(x * x for x in finals) / len(finals)
    assert 0.0008 < mse < 0.0012  # the exact value is 0.001
    assert max(abs(x) for x in finals) < 0.15


def test_power_three_quarters_converges() -> None:
    e = exact_mse(lambda n: (n + 1) ** -0.75, 10000, 1.0, 1.0)
    assert e[10000] < 6e-4
    assert all(e[n + 1] <= e[n] + 1e-15 for n in range(10, 10000))


def test_constant_step_leaves_a_noise_floor() -> None:
    a = Fraction(1, 10)
    assert noise_floor(a, Fraction(1)) == Fraction(1, 19)
    e = exact_mse(lambda n: 0.1, 2000, 1.0, 1.0)
    assert abs(e[-1] - 1 / 19) < 1e-12
    # Seeds: the empirical mean square error at n = 1000 stays at the floor, not near 0.
    finals = [noisy_iteration(0.0, 1.0, lambda n: 0.1, 1000, GAUSS, random.Random(500 + s))[-1] for s in range(400)]
    mse = sum(x * x for x in finals) / len(finals)
    assert 0.045 < mse < 0.060


def test_floor_is_a_fixed_point_of_the_recursion() -> None:
    for a in (Fraction(1, 3), Fraction(1, 2), Fraction(3, 2)):
        f = noise_floor(a, Fraction(5))
        assert (1 - a) ** 2 * f + a * a * 5 == f


def test_summable_steps_stop_short_without_noise() -> None:
    # a_n = 2^-(n+1): x_n - theta = prod (1 - 2^-k) (x_0 - theta), which tends to 0.2888 and not to 0.
    xs = noisy_iteration(0.0, 1.0, lambda n: 2.0 ** -(n + 1), 60, lambda r: 0.0, random.Random(0))
    assert abs(xs[-1] - 0.288788095086602) < 1e-12


def test_summable_steps_bound_the_distance_travelled() -> None:
    # Bounded field and bounded noise: |h + M| <= 2, and sum a_n < 1, so |x_n - x_0| < 2.
    def run(rng: random.Random) -> list[float]:
        xs, x = [5.0], 5.0
        for n in range(200):
            h = max(-1.0, min(1.0, -x))
            x = x + 2.0 ** -(n + 1) * (h + rng.uniform(-1.0, 1.0))
            xs.append(x)
        return xs

    limit = reach(lambda n: 2.0 ** -(n + 1), 200, 2.0)
    for seed in range(200):
        xs = run(random.Random(seed))
        assert all(abs(x - 5.0) <= limit for x in xs)
        assert min(abs(x) for x in xs) >= 3.0


def test_rm2_is_not_necessary_for_the_linear_field() -> None:
    # p = 0.4 breaks sum a_n^2 < infinity, yet the mean square error still tends to 0.
    e = exact_mse(lambda n: (n + 1) ** -0.4, 100000, 1.0, 1.0)
    assert e[1000] < 0.04 and e[100000] < 0.006
    assert e[100000] < e[10000] < e[1000]
