# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morris-counter/. The authors are listed in prov/V4GE3S.jsonl.

import math
import random
from fractions import Fraction

from morris_counter import (
    MorrisCounter,
    copies_for,
    exact_distribution,
    morris_counter,
    morris_plus,
    morris_plus_plus,
)


def moments_by_bit_strings(n: int) -> tuple[Fraction, Fraction]:
    """E and Var of 2^X - 1, by enumeration of every string of coin bits.

    At state X the counter draws X fair bits; each of the 2^X strings has
    weight 2^(-X), and only the all-zero string raises X.
    """
    mean = Fraction(0)
    second = Fraction(0)
    stack = [(0, 0, Fraction(1))]  # (events done, X, probability)
    while stack:
        t, x, p = stack.pop()
        if t == n:
            v = 2**x - 1
            mean += p * v
            second += p * v * v
            continue
        w = p / 2**x
        for bits in range(2**x):
            stack.append((t + 1, x + 1 if bits == 0 else x, w))
    return mean, second - mean * mean


def moments_by_outcomes(n: int, a: Fraction) -> tuple[Fraction, Fraction]:
    """E and Var of ((1 + a)^X - 1) / a over every raise or no-raise sequence."""
    mean = Fraction(0)
    second = Fraction(0)
    stack = [(0, 0, Fraction(1))]
    while stack:
        t, x, p = stack.pop()
        if t == n:
            v = ((1 + a) ** x - 1) / a
            mean += p * v
            second += p * v * v
            continue
        q = (1 + a) ** (-x)
        stack.append((t + 1, x + 1, p * q))
        if q != 1:
            stack.append((t + 1, x, p * (1 - q)))
    return mean, second - mean * mean


def test_unbiased_and_variance_over_all_coin_bits() -> None:
    for n in range(0, 6):
        mean, var = moments_by_bit_strings(n)
        assert mean == n
        assert var == Fraction(n * (n - 1), 2)


def test_unbiased_and_variance_over_all_outcomes() -> None:
    for a in (Fraction(1), Fraction(1, 2), Fraction(1, 5)):
        for n in range(0, 13):
            mean, var = moments_by_outcomes(n, a)
            assert mean == n
            assert var == a * n * (n - 1) / 2


def test_exact_distribution_moments() -> None:
    for n in (0, 1, 2, 3, 10, 40):
        dist = exact_distribution(n)
        assert sum(dist) == 1
        mean = sum(p * (2**x - 1) for x, p in enumerate(dist))
        second = sum(p * (2**x - 1) ** 2 for x, p in enumerate(dist))
        assert mean == n
        assert second - mean * mean == Fraction(n * (n - 1), 2)
    a = Fraction(1, 3)
    dist = exact_distribution(25, a)
    mean = sum(p * ((1 + a) ** x - 1) / a for x, p in enumerate(dist))
    assert mean == 25


def test_worked_example_distribution() -> None:
    assert exact_distribution(3) == [0, Fraction(1, 4), Fraction(5, 8), Fraction(1, 8)]
    dist = exact_distribution(4)
    assert dist == [0, Fraction(1, 8), Fraction(19, 32), Fraction(17, 64), Fraction(1, 64)]
    estimates = [2**x - 1 for x in range(5)]
    assert sum(p * e for p, e in zip(dist, estimates)) == 4
    assert sum(p * e * e for p, e in zip(dist, estimates)) == 22


def test_simulation_matches_exact_distribution() -> None:
    n, runs = 20, 20000
    dist = exact_distribution(n)
    for method in ("pseudocode", "class", "skip"):
        rng = random.Random(7)
        counts = [0] * (n + 1)
        for _ in range(runs):
            if method == "pseudocode":
                est = morris_counter(range(n), rng)
                x = (est + 1).bit_length() - 1
            elif method == "class":
                c = MorrisCounter(rng)
                for _ in range(n):
                    c.increment()
                x = c.x
            else:
                c = MorrisCounter(rng)
                c.increment_by(n)
                x = c.x
            counts[x] += 1
        for x in range(n + 1):
            p = float(dist[x])
            tol = 4.5 * math.sqrt(p * (1 - p) / runs) + 1e-3
            assert abs(counts[x] / runs - p) <= tol, (method, x)


def test_morris_plus_fails_less_than_one_third() -> None:
    eps = 0.5
    s, _ = copies_for(eps, 0.1)
    assert s == 6
    rng = random.Random(11)
    n, runs = 1000, 3000
    bad = sum(abs(morris_plus(n, s, rng) - n) > eps * n for _ in range(runs))
    assert bad / runs <= 1 / 3 + 3 * math.sqrt((1 / 3) * (2 / 3) / runs)


def test_morris_plus_plus_failure_rate() -> None:
    eps, delta = 0.5, 0.2
    s, t = copies_for(eps, delta)
    assert t % 2 == 1 and (8 / 9) ** (t / 2) <= delta
    rng = random.Random(12)
    n, runs = 1000, 1500
    bad = sum(abs(morris_plus_plus(n, s, t, rng) - n) > eps * n for _ in range(runs))
    assert bad / runs <= delta + 3 * math.sqrt(delta * (1 - delta) / runs)


def test_register_stays_small() -> None:
    rng = random.Random(13)
    n = 10**6
    xs = []
    for _ in range(300):
        c = MorrisCounter(rng)
        c.increment_by(n)
        xs.append(c.x)
    # Markov on E[2^X] = n + 1: P[X > log2(n + 1) + 10] < 2^(-10).
    assert max(xs) <= math.log2(n + 1) + 10
    assert max(xs).bit_length() <= 5


def test_base_change_mean() -> None:
    rng = random.Random(14)
    n, runs, a = 500, 4000, 0.1
    values = []
    for _ in range(runs):
        c = MorrisCounter(rng, a)
        c.increment_by(n)
        values.append(c.estimate())
    mean = sum(values) / runs
    sd = math.sqrt(a * n * (n - 1) / 2)
    assert abs(mean - n) <= 4 * sd / math.sqrt(runs)
