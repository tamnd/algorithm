# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pollard-kangaroo/. The authors are listed in prov/VXD7T2.jsonl.

import random

import pytest

import pollard_kangaroo as module
from pollard_kangaroo import pollard_kangaroo


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


def solvable(table: dict[int, int], h: int, a: int, b: int) -> bool:
    """Is there y in [a, b] with g^y = h? Uses the period n = len(table)."""
    if h not in table:
        return False
    n, x0 = len(table), table[h]
    first = a + (x0 - a) % n
    return first <= b


def check(g: int, h: int, a: int, b: int, p: int, table: dict[int, int], seed: int = 0) -> None:
    x = pollard_kangaroo(g, h, a, b, p, seed)
    if solvable(table, h % p, a, b):
        assert x is not None and a <= x <= b and pow(g, x, p) == h % p
    else:
        assert x is None


def test_galbraith_example_14_5_2() -> None:
    # g = 3 of order 131 mod 263, h = 181, 0 <= x < 53: the answer is 12.
    assert pollard_kangaroo(3, 181, 0, 52, 263) == 12


def test_shifted_interval_example() -> None:
    # 5^21 = 14 mod 23 and 21 lies in [18, 22]; nothing in [0, 10].
    assert pollard_kangaroo(5, 14, 18, 22, 23) == 21
    assert pollard_kangaroo(5, 14, 0, 10, 23) is None
    assert pollard_kangaroo(2, 5, 0, 100, 23) is None


def test_trivial_targets() -> None:
    rng = random.Random(3)
    for _ in range(50):
        p = random_prime(rng, 3, 100000)
        g = rng.randrange(2, p)
        b = rng.randrange(0, 2000)
        table = power_table(g, p)
        check(g, 1, 0, b, p, table)
        check(g, g, 0, b, p, table)
        check(g, 1, 1, b + 1, p, table)


def test_tiny_groups_exhaustive() -> None:
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        for g in range(1, p):
            table = power_table(g, p)
            for h in range(1, p):
                for a in range(0, 6):
                    for b in range(a, a + 12, 3):
                        check(g, h, a, b, p, table)


def test_random_intervals() -> None:
    rng = random.Random(2024)
    for _ in range(250):
        p = random_prime(rng, 50, 100000)
        g = rng.randrange(2, p)
        table = power_table(g, p)
        n = len(table)
        a = rng.randrange(0, 2 * n)
        w = rng.choice([0, 1, 2, rng.randrange(n), rng.randrange(3 * n + 1)])
        b = a + w
        roll = rng.random()
        if roll < 0.5:
            h = pow(g, rng.randrange(a, b + 1), p)
        elif roll < 0.8:
            h = pow(g, rng.randrange(n), p)
        else:
            h = rng.randrange(1, p)
        check(g, h, a, b, p, table, rng.randrange(1000))


def test_prime_order_subgroups() -> None:
    rng = random.Random(11)
    done = 0
    while done < 30:
        q = random_prime(rng, 50, 3000)
        k = rng.randrange(2, 30)
        p = k * q + 1
        if not is_prime(p):
            continue
        g = 1
        while g == 1:
            g = pow(rng.randrange(2, p), k, p)
        table = power_table(g, p)
        assert len(table) == q
        for _ in range(4):
            a = rng.randrange(q)
            b = a + rng.randrange(q // 2 + 1)
            check(g, pow(g, rng.randrange(a, b + 1), p), a, b, p, table)
            check(g, pow(g, rng.randrange(q), p), a, b, p, table)
        non_member = next(y for y in range(2, p) if pow(y, q, p) != 1)
        assert pollard_kangaroo(g, non_member, 0, q, p) is None
        done += 1


def test_kangaroos_usually_succeed_without_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    # Large intervals inside a large prime order subgroup: the walk alone
    # should solve almost every instance, so the certificate is rarely used.
    calls = []
    original = module._bsgs

    def spy(g: int, h: int, n: int, p: int) -> int | None:
        calls.append(n)
        return original(g, h, n, p)

    monkeypatch.setattr(module, "_bsgs", spy)
    rng = random.Random(5)
    p = 99991
    g = next(c for c in range(2, p) if all(pow(c, (p - 1) // f, p) != 1 for f in (2, 3, 5, 11, 101)))
    n = p - 1
    trials = 60
    for _ in range(trials):
        a = rng.randrange(n // 2)
        b = a + rng.randrange(1000, n // 2)
        x = rng.randrange(a, b + 1)
        assert pollard_kangaroo(g, pow(g, x, p), a, b, p, rng.randrange(100)) is not None
    assert len(calls) <= trials // 10


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        pollard_kangaroo(2, 3, 5, 4, 7)
    with pytest.raises(ValueError):
        pollard_kangaroo(2, 3, -1, 4, 7)
    with pytest.raises(ValueError):
        pollard_kangaroo(2, 3, 0, 4, 1)
