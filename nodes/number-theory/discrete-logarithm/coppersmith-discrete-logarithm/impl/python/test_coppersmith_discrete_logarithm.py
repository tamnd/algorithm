# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coppersmith-discrete-logarithm/. The authors are listed in prov/TEVZ61.jsonl.

import random

import pytest

from coppersmith_discrete_logarithm import coppersmith_dlog, fmul, fpow, irreducibles, pdivmod

_IRR = irreducibles(8)


def field(n: int) -> int:
    """x^n + f1 with the least f1 that makes it irreducible over F_2."""
    for f1 in range(1, 1 << n):
        f = (1 << n) | f1
        if all(pdivmod(f, s)[1] for s in _IRR if 2 * (s.bit_length() - 1) <= n):
            return f
    raise AssertionError("no irreducible trinomial-like polynomial")


def powers(g: int, f: int) -> dict[int, int]:
    """Map g^i to i for i in [0, ord g), by brute force."""
    table = {}
    y, i = 1, 0
    while y not in table:
        table[y] = i
        y = fmul(y, g, f)
        i += 1
    return table


def check(g: int, h: int, f: int, seed: int = 0) -> None:
    table = powers(g, f)
    got = coppersmith_dlog(g, h, len(table), f, seed=seed)
    assert got == table.get(h), (g, h, f)


def test_galbraith_example():
    f = (1 << 15) | 0b11
    g = 0b100010100101
    h = (1 << 14) | (1 << 11) | (1 << 10) | (1 << 9) | 1
    assert coppersmith_dlog(g, h, 151, f, b=3) == 23
    assert coppersmith_dlog(g, h, 151, f) == 23
    assert fpow(g, 23, f) == h


def test_trivial_targets():
    for n in (1, 2, 3, 8, 13):
        f = field(n)
        for g in (1, 2, 3, (1 << n) - 1):
            if g >= 1 << n:
                continue
            table = powers(g, f)
            r = len(table)
            assert coppersmith_dlog(g, 1, r, f) == 0
            if g != 1:
                assert coppersmith_dlog(g, g, r, f) == (1 if r > 1 else 0)
    f = field(5)
    assert coppersmith_dlog(1, 2, 1, f) is None


def test_small_fields_exhaustive():
    for n in range(1, 6):
        f = field(n)
        for g in range(1, 1 << n):
            for h in range(1, 1 << n):
                check(g, h, f)


def test_random_fields_against_brute_force():
    rng = random.Random(1)
    for _ in range(60):
        n = rng.randrange(6, 15)
        f = field(n)
        g = rng.randrange(1, 1 << n)
        h = rng.randrange(1, 1 << n)
        check(g, h, f, seed=rng.randrange(1000))
        table = powers(g, f)
        x = rng.randrange(len(table))
        check(g, fpow(g, x, f), f, seed=rng.randrange(1000))


def test_generators_and_subgroups():
    rng = random.Random(2)
    for n in (6, 8, 9, 10, 11, 12, 14, 15, 16):
        f = field(n)
        order = (1 << n) - 1
        gamma = next(c for c in range(2, 1 << n) if len(powers(c, f)) == order) if n <= 12 else None
        divisors = [d for d in range(2, order + 1) if order % d == 0]
        for r in rng.sample(divisors, min(4, len(divisors))):
            base = gamma if gamma is not None else rng.randrange(2, 1 << n)
            g = fpow(base, order // r, f)
            table = powers(g, f)
            r = len(table)
            x = rng.randrange(r)
            assert coppersmith_dlog(g, fpow(g, x, f), r, f, seed=x) == x
            y = rng.randrange(1, 1 << n)
            assert coppersmith_dlog(g, y, r, f) == table.get(y)


def test_prime_and_composite_orders():
    f = field(12)  # 2^12 - 1 = 3^2 * 5 * 7 * 13
    full = powers(2, f)
    gamma = 2 if len(full) == 4095 else next(c for c in range(3, 4096) if len(powers(c, f)) == 4095)
    for r in (3, 5, 7, 13, 9, 15, 45, 63, 91, 315, 4095):
        g = fpow(gamma, 4095 // r, f)
        for x in (0, 1, r - 1, r // 2):
            assert coppersmith_dlog(g, fpow(g, x, f), r, f) == x
        outside = fpow(gamma, 1, f)
        assert coppersmith_dlog(g, outside, r, f) == (None if r < 4095 else 1)


def test_no_solution_is_reported():
    rng = random.Random(3)
    found = 0
    for _ in range(60):
        n = rng.randrange(4, 13)
        f = field(n)
        g = rng.randrange(1, 1 << n)
        table = powers(g, f)
        h = rng.randrange(1, 1 << n)
        if h not in table:
            found += 1
            assert coppersmith_dlog(g, h, len(table), f) is None
    assert found >= 10


def test_seed_independence():
    f = field(13)
    g = 0b1011011
    table = powers(g, f)
    h = fpow(g, 1234 % len(table), f)
    assert {coppersmith_dlog(g, h, len(table), f, seed=s) for s in range(8)} == {1234 % len(table)}


def test_bad_input():
    f = field(5)
    with pytest.raises(ValueError):
        coppersmith_dlog(0, 1, 1, f)
    with pytest.raises(ValueError):
        coppersmith_dlog(1, 32, 1, f)
    with pytest.raises(ValueError):
        coppersmith_dlog(1, 1, 0, f)
    with pytest.raises(ValueError):
        coppersmith_dlog(1, 1, 1, 1)
