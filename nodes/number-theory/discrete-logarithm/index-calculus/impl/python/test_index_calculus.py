# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/index-calculus/. The authors are listed in prov/C3H4Y5.jsonl.

import random

import pytest

import index_calculus as ic
from index_calculus import index_calculus


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
    x = index_calculus(g, h, n, p, seed=seed)
    if h % p in table:
        assert x == table[h % p]
    else:
        assert x is None


def test_hac_example_3_69() -> None:
    # 6 generates (Z/229Z)^*; HAC finds log_6 13 = 117.
    assert index_calculus(6, 13, 228, 229) == 117


def test_galbraith_example_15_5_4() -> None:
    # 15 has prime order 37 modulo 223; the answer is 13.
    assert index_calculus(15, 68, 37, 223) == 13


def test_hac_factor_base_logs() -> None:
    # The logarithms of 2, 3, 5, 7, 11 to the base 6 modulo 229 from HAC's Example 3.69.
    rels = [([2, 2, 1, 0, 0], 100), ([4, 0, 0, 0, 1], 18), ([0, 1, 1, 0, 1], 12),
            ([1, 0, 0, 1, 1], 62), ([1, 2, 0, 0, 1], 143), ([1, 1, 1, 1, 0], 206)]
    logs = [21, 208, 98, 107, 162]
    for q, m in [(2, 4), (3, 3), (19, 19)]:
        sol = ic._solve(rels, q, m)
        assert sol == [x % m for x in logs]
    for s, x in zip([2, 3, 5, 7, 11], logs):
        assert pow(6, x, 229) == s


def test_solve_reports_missing_pivot() -> None:
    # The prime 7 never occurs, so its column has no pivot.
    rels = [([1, 0, 0, 0], 3), ([0, 1, 0, 0], 4), ([0, 0, 1, 0], 5), ([1, 1, 1, 0], 12)]
    assert ic._solve(rels, 5, 25) is None


def test_worked_example_no_solution() -> None:
    # 5 is a generator mod 23, so 2 (order 11) does not reach it.
    assert index_calculus(2, 5, 11, 23) is None
    assert index_calculus(5, 14, 22, 23) == 21


def test_trivial_targets() -> None:
    rng = random.Random(1)
    for _ in range(40):
        p = random_prime(rng, 3, 100000)
        g = rng.randrange(2, p)
        n = len(power_table(g, p))
        assert index_calculus(g, 1, n, p) == 0
        assert index_calculus(g, g, n, p) == (1 if n > 1 else 0)


def test_tiny_groups_exhaustive() -> None:
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
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
    for _ in range(40):
        p = random_prime(rng, 10000, 100000)
        g = rng.randrange(2, p)
        table = power_table(g, p)
        n = len(table)
        for _ in range(3):
            x = rng.randrange(n)
            h = pow(g, x, p)
            assert index_calculus(g, h, n, p, rng.randrange(1000)) == table[h]
        outside = rng.randrange(1, p)
        expected = table.get(outside)
        assert index_calculus(g, outside, n, p) == expected


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
            assert index_calculus(g, pow(g, x, p), q, p, rng.randrange(100)) == x
        non_member = next(y for y in range(2, p) if pow(y, q, p) != 1)
        assert index_calculus(g, non_member, q, p) is None
        found += 1


def test_composite_order_subgroups() -> None:
    rng = random.Random(9)
    for _ in range(45):
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
            assert index_calculus(g, pow(g, x, p), n, p, rng.randrange(100)) == x
        check(g, rng.randrange(1, p), p)


def test_seed_independence_of_answer() -> None:
    for seed in range(20):
        assert index_calculus(6, 13, 228, 229, seed) == 117
        assert index_calculus(2, 228, 191, 383, seed) == 110


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        index_calculus(2, 3, 0, 5)
    with pytest.raises(ValueError):
        index_calculus(2, 3, 1, 1)
