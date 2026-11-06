# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pollard-rho-discrete-logarithm/. The authors are listed in prov/8WE1PE.jsonl.

import random

import pytest

from pollard_rho_discrete_logarithm import pollard_rho_log


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def power_table(g: int, p: int) -> dict[int, int]:
    """Least exponent of every power of g modulo p, by walking the cycle."""
    seen: dict[int, int] = {}
    e, x = 1 % p, 0
    while e not in seen:
        seen[e] = x
        e, x = e * g % p, x + 1
    return seen


def random_prime(rng: random.Random, lo: int, hi: int) -> int:
    while True:
        p = rng.randrange(lo, hi)
        if is_prime(p):
            return p


def check(g: int, h: int, p: int, seed: int = 0) -> None:
    table = power_table(g, p)
    n = len(table)
    x = pollard_rho_log(g, h, n, p, seed)
    if h % p in table:
        assert x == table[h % p]
    else:
        assert x is None


def test_hac_example_3_61() -> None:
    # Subgroup of order 191 in (Z/383Z)^*, collision x_14 = x_28 = 144.
    assert pollard_rho_log(2, 228, 191, 383) == 110


def test_worked_example_no_solution() -> None:
    # 5 is a generator mod 23, so 2 (order 11) does not reach it.
    assert pollard_rho_log(2, 5, 11, 23) is None
    assert pollard_rho_log(5, 14, 22, 23) == 21


def test_trivial_targets() -> None:
    rng = random.Random(1)
    for _ in range(60):
        p = random_prime(rng, 3, 100000)
        g = rng.randrange(2, p)
        n = len(power_table(g, p))
        assert pollard_rho_log(g, 1, n, p) == 0
        assert pollard_rho_log(g, g, n, p) == (1 if n > 1 else 0)


def test_tiny_groups_exhaustive() -> None:
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        for g in range(1, p):
            for h in range(1, p):
                check(g, h, p)


def test_random_small_groups() -> None:
    rng = random.Random(2024)
    for _ in range(300):
        p = random_prime(rng, 3, 3000)
        g = rng.randrange(1, p)
        h = rng.randrange(1, p) if rng.random() < 0.5 else pow(g, rng.randrange(p), p)
        check(g, h, p, rng.randrange(1000))


def test_random_large_groups() -> None:
    rng = random.Random(77)
    for _ in range(60):
        p = random_prime(rng, 10000, 100000)
        g = rng.randrange(2, p)
        table = power_table(g, p)
        n = len(table)
        for _ in range(3):
            x = rng.randrange(n)
            h = pow(g, x, p)
            assert pollard_rho_log(g, h, n, p, rng.randrange(1000)) == table[h]
        outside = rng.randrange(1, p)
        expected = table.get(outside)
        assert pollard_rho_log(g, outside, n, p) == expected


def test_prime_order_subgroups() -> None:
    rng = random.Random(5)
    found = 0
    while found < 40:
        q = random_prime(rng, 3, 300)
        k = rng.randrange(2, 300)
        p = k * q + 1
        if not is_prime(p):
            continue
        g = 1
        while g == 1:
            g = pow(rng.randrange(2, p), k, p)
        assert len(power_table(g, p)) == q
        for _ in range(5):
            x = rng.randrange(q)
            assert pollard_rho_log(g, pow(g, x, p), q, p, rng.randrange(100)) == x
        non_member = next(y for y in range(2, p) if pow(y, q, p) != 1)
        assert pollard_rho_log(g, non_member, q, p) is None
        found += 1


def test_composite_order_subgroups() -> None:
    rng = random.Random(9)
    for _ in range(80):
        p = random_prime(rng, 100, 50000)
        r = p - 1
        divisors = [d for d in range(4, r + 1) if r % d == 0 and not is_prime(d)]
        if not divisors:
            continue
        n = rng.choice(divisors)
        g = 1
        while len(power_table(g, p)) != n:
            g = pow(rng.randrange(2, p), r // n, p)
        for _ in range(4):
            x = rng.randrange(n)
            assert pollard_rho_log(g, pow(g, x, p), n, p, rng.randrange(100)) == x
        check(g, rng.randrange(1, p), p)


def test_seed_independence_of_answer() -> None:
    for seed in range(20):
        assert pollard_rho_log(2, 228, 191, 383, seed) == 110


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        pollard_rho_log(2, 3, 0, 5)
    with pytest.raises(ValueError):
        pollard_rho_log(2, 3, 1, 1)
