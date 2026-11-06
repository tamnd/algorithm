# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mobius-sieve/. The authors are listed in prov/E7NA3A.jsonl.

import random

from mobius_sieve import mobius_sieve


def mu_by_trial_division(m: int) -> int:
    """The Möbius function from its definition, by factoring m."""
    sign, d = 1, 2
    while d * d <= m:
        if m % d == 0:
            m //= d
            if m % d == 0:
                return 0
            sign = -sign
        d += 1
    if m > 1:
        sign = -sign
    return sign


def mu_by_divisor_sum(n: int) -> list[int]:
    """mu from sum over d | m of mu(d) = [m = 1], an independent quadratic-time oracle."""
    mu = [0] * (n + 1)
    for m in range(1, n + 1):
        mu[m] = (1 if m == 1 else 0) - sum(mu[d] for d in range(1, m) if m % d == 0)
    return mu


def test_example() -> None:
    assert mobius_sieve(12) == [0, 1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0]
    assert sum(mobius_sieve(30)) == -3


def test_edges() -> None:
    assert mobius_sieve(0) == [0]
    assert mobius_sieve(1) == [0, 1]
    assert mobius_sieve(2) == [0, 1, -1]
    assert mobius_sieve(4) == [0, 1, -1, -1, 0]


def test_against_divisor_sum_up_to_500() -> None:
    assert mobius_sieve(500) == mu_by_divisor_sum(500)


def test_every_n_up_to_2000() -> None:
    full = [0] + [mu_by_trial_division(m) for m in range(1, 2001)]
    for n in range(2001):
        assert mobius_sieve(n) == full[: n + 1]


def test_random_larger_n() -> None:
    rng = random.Random(1832)
    for _ in range(5):
        n = rng.randint(2001, 60000)
        mu = mobius_sieve(n)
        for m in rng.sample(range(1, n + 1), 400) + [n]:
            assert mu[m] == mu_by_trial_division(m)


def test_squarefree_count() -> None:
    assert sum(abs(v) for v in mobius_sieve(10**4)) == 6083
