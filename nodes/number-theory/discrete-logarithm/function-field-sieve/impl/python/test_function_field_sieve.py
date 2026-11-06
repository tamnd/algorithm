# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/function-field-sieve/. The authors are listed in prov/AJXW0K.jsonl.

import random

import pytest

from function_field_sieve import (
    compose,
    decode,
    encode,
    ffs_dlog,
    ffs_field,
    fmul,
    fpow,
    irreducibles,
    padd,
    pdivmod,
)

_FIELDS: dict[tuple[int, int], tuple] = {}


def field(p: int, n: int):
    if (p, n) not in _FIELDS:
        _FIELDS[(p, n)] = ffs_field(p, n, seed=p * 100 + n)
    return _FIELDS[(p, n)]


def powers(g: int, f, p: int) -> dict[int, int]:
    """Map the code of g^i to i for i in [0, ord g), by brute force."""
    gp = decode(g, p)
    table = {}
    y, i = (1,), 0
    while encode(y, p) not in table:
        table[encode(y, p)] = i
        y = fmul(y, gp, f, p)
        i += 1
    return table


def check(g: int, h: int, p: int, n: int, seed: int = 0) -> None:
    f1, f2, f = field(p, n)
    table = powers(g, f, p)
    assert ffs_dlog(g, h, len(table), p, f1, f2, f, seed=seed) == table.get(h), (p, n, g, h)


def test_field_construction():
    for p, n in [(2, 2), (2, 7), (2, 12), (3, 4), (3, 9), (5, 5), (7, 3), (13, 2)]:
        f1, f2, f = field(p, n)
        assert len(f) - 1 == n and f[-1] == 1
        assert not pdivmod(padd(compose(f2, f1, p), (0, p - 1), p), f, p)[1]
        assert all(pdivmod(f, s, p)[1] for s in irreducibles(n // 2, p))


def test_worked_example():
    p, f1, f2 = 3, (0, 0, 1), (2, 0, 1)
    f = padd(compose(f2, f1, p), (0, p - 1), p)
    assert f == (2, 2, 0, 0, 1)  # t^4 + 2t + 2
    g, h = encode(fpow((0, 1), 16, f, p), p), encode(fpow((0, 1), 48, f, p), p)
    assert decode(g, p) == (2, 2, 0, 1) and decode(h, p) == (2, 1, 2)
    assert fmul(decode(g, p), (0, 1), f, p) == (1, 0, 2)  # g t = 2 (t + 1)(t + 2)
    for seed in range(5):
        assert ffs_dlog(g, h, 5, p, f1, f2, f, seed=seed, deg_base=1) == 3


def test_trivial_targets():
    for p, n in [(2, 3), (3, 3), (5, 2), (2, 9), (7, 2)]:
        f1, f2, f = field(p, n)
        for g in (1, 2, p**n - 1, p + 1):
            if g >= p**n:
                continue
            r = len(powers(g, f, p))
            assert ffs_dlog(g, 1, r, p, f1, f2, f) == 0
            if g != 1:
                assert ffs_dlog(g, g, r, p, f1, f2, f) == (1 if r > 1 else 0)
        assert ffs_dlog(1, 2, 1, p, f1, f2, f) is None


def test_small_fields_exhaustive():
    for p, n in [(2, 2), (2, 3), (3, 2), (2, 4), (5, 2)]:
        step = 1 if p**n < 10 else 3
        for g in range(1, p**n, step):
            for h in range(1 + g % step, p**n, step):
                check(g, h, p, n)


def test_random_fields_against_brute_force():
    rng = random.Random(1)
    sizes = [(2, n) for n in range(5, 13)] + [(3, n) for n in range(3, 7)] + [(5, 3), (5, 4), (7, 3), (11, 2), (13, 3), (31, 2)]
    for _ in range(12):
        p, n = rng.choice(sizes)
        f1, f2, f = field(p, n)
        g = rng.randrange(1, p**n)
        table = powers(g, f, p)
        h = rng.randrange(1, p**n)
        check(g, h, p, n, seed=rng.randrange(1000))
        x = rng.randrange(len(table))
        y = encode(fpow(decode(g, p), x, f, p), p)
        assert ffs_dlog(g, y, len(table), p, f1, f2, f, seed=x) == x


def test_generators_and_subgroups():
    rng = random.Random(2)
    for p, n in [(2, 10), (3, 5), (7, 3), (13, 2)]:
        f1, f2, f = field(p, n)
        order = p**n - 1
        gamma = next(c for c in range(2, p**n) if len(powers(c, f, p)) == order)
        divisors = [d for d in range(2, order + 1) if order % d == 0]
        for r in rng.sample(divisors, min(2, len(divisors))) + [order]:
            g = encode(fpow(decode(gamma, p), order // r, f, p), p)
            x = rng.randrange(r)
            y = encode(fpow(decode(g, p), x, f, p), p)
            assert ffs_dlog(g, y, r, p, f1, f2, f, seed=x) == x
            z = rng.randrange(1, p**n)
            assert ffs_dlog(g, z, r, p, f1, f2, f) == powers(g, f, p).get(z)


def test_prime_and_composite_orders():
    p, n = 3, 6  # 3^6 - 1 = 2^3 * 7 * 13
    f1, f2, f = field(p, n)
    order = p**n - 1
    gamma = next(c for c in range(2, p**n) if len(powers(c, f, p)) == order)
    for r in (2, 8, 13, 26, 91, order):
        g = encode(fpow(decode(gamma, p), order // r, f, p), p)
        for x in (0, 1, r - 1):
            y = encode(fpow(decode(g, p), x, f, p), p)
            assert ffs_dlog(g, y, r, p, f1, f2, f) == x
        assert ffs_dlog(g, gamma, r, p, f1, f2, f) == (None if r < order else 1)


def test_no_solution_is_reported():
    rng = random.Random(3)
    found = 0
    for _ in range(60):
        p, n = rng.choice([(2, 8), (2, 10), (3, 5), (3, 6), (5, 3), (7, 3)])
        f1, f2, f = field(p, n)
        g = rng.randrange(1, p**n)
        table = powers(g, f, p)
        h = rng.randrange(1, p**n)
        if h not in table:
            found += 1
            assert ffs_dlog(g, h, len(table), p, f1, f2, f) is None
    assert found >= 10


def test_seed_independence():
    p, n = 3, 6
    f1, f2, f = field(p, n)
    g = 5
    table = powers(g, f, p)
    x = 1000 % len(table)
    h = encode(fpow(decode(g, p), x, f, p), p)
    assert {ffs_dlog(g, h, len(table), p, f1, f2, f, seed=s) for s in range(4)} == {x}


def test_bad_input():
    f1, f2, f = field(3, 3)
    with pytest.raises(ValueError):
        ffs_dlog(0, 1, 1, 3, f1, f2, f)
    with pytest.raises(ValueError):
        ffs_dlog(1, 27, 1, 3, f1, f2, f)
    with pytest.raises(ValueError):
        ffs_dlog(1, 1, 0, 3, f1, f2, f)
    with pytest.raises(ValueError):
        ffs_field(3, 1)
