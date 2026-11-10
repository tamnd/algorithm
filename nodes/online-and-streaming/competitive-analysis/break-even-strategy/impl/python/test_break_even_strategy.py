# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/break-even-strategy/. The authors are listed in prov/04HWFP.jsonl.

import math
import random
from fractions import Fraction

from break_even_strategy import (
    BreakEven,
    break_even_cost,
    buy_day_cost,
    opt_cost,
    randomized_distribution,
    randomized_expected_cost,
    randomized_ratio,
    sample_buy_day,
    worst_ratio,
)


def test_example_b10() -> None:
    alg = BreakEven(1, 10)
    actions = [alg.day() for _ in range(12)]
    assert actions == ["rent"] * 9 + ["buy", "own", "own"]
    assert break_even_cost(3, 1, 10) == 3
    assert break_even_cost(10, 1, 10) == 19
    assert break_even_cost(100, 1, 10) == 19
    assert opt_cost(10, 1, 10) == 10


def test_worst_ratio_tables() -> None:
    f = Fraction
    assert [worst_ratio(j, 4) for j in range(1, 8)] == [f(4), f(5, 2), f(2), f(7, 4), f(2), f(9, 4), f(5, 2)]
    expected = [f(10), f(11, 2), f(4), f(13, 4), f(14, 5), f(5, 2), f(16, 7), f(17, 8), f(2), f(19, 10), f(2), f(21, 10), f(11, 5)]
    assert [worst_ratio(j, 10) for j in range(1, 14)] == expected
    assert worst_ratio(None, 4) is None


def test_break_even_is_the_unique_best_rule() -> None:
    for b in range(1, 31):
        ratios = {j: worst_ratio(j, b) for j in range(1, 3 * b + 2)}
        best = min(ratios.values())
        assert best == 2 - Fraction(1, b)
        if b >= 2:
            assert [j for j, r in ratios.items() if r == best] == [b]
        # the season that ends on the purchase day forces the ratio
        for j, r in ratios.items():
            assert Fraction(buy_day_cost(j, j, 1, b), opt_cost(j, 1, b)) == r


def test_general_prices() -> None:
    rng = random.Random(4104)
    for _ in range(400):
        rent = Fraction(rng.randint(1, 9), rng.randint(1, 4))
        price = Fraction(rng.randint(1, 60), rng.randint(1, 4))
        m = math.ceil(price / rent)
        bound = 1 + (m - 1) * rent / price
        assert bound < 2
        worst = Fraction(0)
        for n in range(1, m + 3):
            r = Fraction(break_even_cost(n, rent, price)) / opt_cost(n, rent, price)
            assert r <= bound
            worst = max(worst, r)
        assert worst == bound
        assert break_even_cost(m, rent, price) == (m - 1) * rent + price


def test_randomized_rule_is_exact() -> None:
    assert randomized_distribution(4) == [Fraction(x, 175) for x in (27, 36, 48, 64)]
    assert randomized_ratio(4) == Fraction(256, 175)
    for b in range(1, 13):
        dist = randomized_distribution(b)
        assert sum(dist) == 1
        c = randomized_ratio(b)
        for n in range(1, 2 * b + 3):
            assert randomized_expected_cost(n, b) == c * opt_cost(n, 1, b)


def test_yao_distribution_matches() -> None:
    for b in range(2, 11):
        q = Fraction(b - 1, b)
        dist = {i: q**i / (b - 1) for i in range(1, b)}
        dist[2 * b - 1] = q ** (b - 1)
        assert sum(dist.values()) == 1
        e_opt = sum(p * opt_cost(n, 1, b) for n, p in dist.items())
        rules = list(range(1, 2 * b + 1)) + [None]
        best = min(sum(p * buy_day_cost(n, j, 1, b) for n, p in dist.items()) for j in rules)
        assert best / e_opt == randomized_ratio(b)


def test_randomized_ratio_tends_to_e_over_e_minus_1() -> None:
    values = [randomized_ratio(b) for b in range(1, 40)]
    assert all(x < y for x, y in zip(values, values[1:]))
    limit = math.e / (math.e - 1)
    assert all(v < limit for v in values)
    assert abs(float(randomized_ratio(1000)) - limit) < 5e-4
    assert abs(1 / (1 - (1 - 1e-6) ** 1e6) - limit) < 1e-5


def test_sampling_follows_the_distribution() -> None:
    rng = random.Random(77)
    b, trials = 5, 20000
    counts = [0] * (b + 1)
    for _ in range(trials):
        counts[sample_buy_day(b, rng)] += 1
    for j, p in enumerate(randomized_distribution(b), start=1):
        assert abs(counts[j] / trials - float(p)) < 0.02


def test_bad_input() -> None:
    for rent, price in ((0, 1), (1, 0), (-1, 5)):
        try:
            BreakEven(rent, price)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")
