# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-phi-sieve/. The authors are listed in prov/1P82VA.jsonl.

import random
from math import gcd

from euler_phi_sieve import euler_phi_sieve


def phi_by_definition(m: int) -> int:
    return sum(1 for j in range(1, m + 1) if gcd(j, m) == 1)


def phi_by_trial_division(m: int) -> int:
    result, rest, d = m, m, 2
    while d * d <= rest:
        if rest % d == 0:
            result -= result // d
            while rest % d == 0:
                rest //= d
        d += 1
    if rest > 1:
        result -= result // rest
    return result


def test_example() -> None:
    assert euler_phi_sieve(12) == [0, 1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4]


def test_edges() -> None:
    assert euler_phi_sieve(0) == [0]
    assert euler_phi_sieve(1) == [0, 1]
    assert euler_phi_sieve(2) == [0, 1, 1]
    assert euler_phi_sieve(3) == [0, 1, 1, 2]


def test_against_definition_up_to_600() -> None:
    table = euler_phi_sieve(600)
    for m in range(1, 601):
        assert table[m] == phi_by_definition(m)


def test_every_n_up_to_2000() -> None:
    full = [0] + [phi_by_trial_division(m) for m in range(1, 2001)]
    for n in range(2001):
        assert euler_phi_sieve(n) == full[: n + 1]


def test_random_larger_n() -> None:
    rng = random.Random(1763)
    for _ in range(5):
        n = rng.randint(2001, 60000)
        table = euler_phi_sieve(n)
        assert len(table) == n + 1
        for m in rng.sample(range(1, n + 1), 300):
            assert table[m] == phi_by_trial_division(m)
        assert table[n] == phi_by_trial_division(n)


def test_sum_of_totients() -> None:
    assert sum(euler_phi_sieve(1000)) == 304192
