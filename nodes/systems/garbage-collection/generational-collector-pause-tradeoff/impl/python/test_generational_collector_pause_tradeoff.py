# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generational-collector-pause-tradeoff/. The authors are listed in prov/RPKRXJ.jsonl.

import itertools
import random
from fractions import Fraction

from generational_collector_pause_tradeoff import (
    copied_per_collection,
    cost_per_allocation,
    finite,
    geometric,
    geometric_p,
    mixture,
    p_sum,
    promoted_per_collection,
    promotion_rate,
    simulate,
)


def test_model_equals_exact_expectation_over_all_lifetimes() -> None:
    dist = {0: Fraction(1, 2), 2: Fraction(1, 4), 5: Fraction(1, 8), 9: Fraction(1, 8)}
    s = finite(dist)
    for n, t in [(1, 1), (2, 1), (2, 2), (3, 1), (1, 3), (1, 4)]:
        j = t + 1  # a collection whose t windows are all full
        size = j * n
        exp_copied = exp_promoted = Fraction(0)
        for lives in itertools.product(dist, repeat=size):
            w = Fraction(1)
            for life in lives:
                w *= dist[life]
            copied, promoted = simulate(list(lives), n, t)[j - 1]
            exp_copied += w * copied
            exp_promoted += w * promoted
        assert exp_copied == copied_per_collection(s, n, t)
        assert exp_promoted == promoted_per_collection(s, n, t)


def test_page_table() -> None:
    def p(n: int) -> float:
        return 0.9 * geometric_p(10, n) + 0.1 * geometric_p(10_000, n)

    s = mixture([(0.9, geometric(10, exact=False)), (0.1, geometric(10_000, exact=False))])
    rows = {}
    for n, t in [(100, 1), (1000, 1), (10000, 1), (1000, 2), (500, 2)]:
        c = copied_per_collection(s, n, t)
        assert abs(c - p(t * n)) < 1e-6
        rows[(n, t)] = (round(c, 2), round(promotion_rate(s, n, t), 4))
    assert rows[(100, 1)] == (18.95, 0.1895)
    assert rows[(1000, 1)] == (104.17, 0.1042)
    assert rows[(10000, 1)] == (641.14, 0.0641)
    assert rows[(1000, 2)] == (190.28, 0.0861)
    assert rows[(500, 2)] == (104.17, 0.0928)
    short = mixture([(0.9, geometric(10, exact=False))])  # the short-lived group only
    assert [round(promotion_rate(short, n, 1), 4) for n in (100, 1000, 10000)] == [0.09, 0.009, 0.0009]
    assert round(geometric_p(10_000, 1000), 1) == 951.7


def nonincreasing_survival(rng: random.Random) -> list[Fraction]:
    vals = sorted((Fraction(rng.randint(0, 20), 20) for _ in range(30)), reverse=True)
    return [Fraction(1)] + vals


def test_pause_grows_and_cost_per_allocation_falls_with_n() -> None:
    rng = random.Random(42)
    for _ in range(40):
        table = nonincreasing_survival(rng)
        s = lambda a: table[a] if a < len(table) else Fraction(0)
        for n in range(1, 30):
            assert p_sum(s, n + 1) >= p_sum(s, n)  # longer pauses
            assert p_sum(s, n + 1) / (n + 1) <= p_sum(s, n) / n  # less work per allocation
            assert promotion_rate(s, n + 1, 1) <= promotion_rate(s, n, 1)


def test_aging_trades_pause_for_promotion() -> None:
    s = mixture([(Fraction(9, 10), geometric(10)), (Fraction(1, 10), geometric(1000))])
    n = 50
    for t in range(1, 6):
        assert copied_per_collection(s, n, t + 1) > copied_per_collection(s, n, t)
        assert promotion_rate(s, n, t + 1) < promotion_rate(s, n, t)


def test_simulation_agrees_with_model() -> None:
    rng = random.Random(1997)
    n, t = 40, 2
    lifetimes = []
    for _ in range(40_000):
        mean = 8 if rng.random() < 0.9 else 400
        life = 1  # P(life > a) = (1 - 1/mean)^a
        while rng.random() >= 1.0 / mean:
            life += 1
        lifetimes.append(life)
    runs = simulate(lifetimes, n, t)[t:]
    avg_c = sum(c for c, _ in runs) / len(runs)
    avg_p = sum(p for _, p in runs) / len(runs)
    s = mixture([(0.9, geometric(8, exact=False)), (0.1, geometric(400, exact=False))])
    assert abs(avg_c - copied_per_collection(s, n, t)) < 0.6
    assert abs(avg_p - promoted_per_collection(s, n, t)) < 0.4


def test_cost_per_allocation() -> None:
    s = finite({0: Fraction(3, 4), 10: Fraction(1, 4)})
    assert p_sum(s, 4) == 1  # only the long-lived quarter survives
    assert cost_per_allocation(s, 4, 1, 2, 1) == Fraction(3, 4)
