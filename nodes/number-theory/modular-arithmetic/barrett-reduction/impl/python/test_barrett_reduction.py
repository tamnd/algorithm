# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barrett-reduction/. The authors are listed in prov/MXGY63.jsonl.

import random

import pytest

from barrett_reduction import barrett_mulmod, barrett_powmod, barrett_reduce, barrett_setup


def corrections(x, ctx):
    """The number of subtractions of n made by line L5, from the quotient estimate."""
    q = ((x >> (ctx.k - 1)) * ctx.mu) >> (ctx.k + 1)
    return x // ctx.n - q


def moduli(rng):
    """Moduli 1, 2, powers of two, small and large primes, composites, several hundred digits."""
    ms = [1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 47, 50, 97, 255, 256, 257, 65535, 65536, 65537]
    ms += [1 << e for e in (10, 31, 32, 63, 64, 127, 1000)]
    ms += [(1 << e) - 1 for e in (61, 89, 127)] + [(1 << e) + 1 for e in (32, 64)]
    ms += [10**9 + 7, 998244353, 2**61 - 1, 10**18 + 9, 10**300 + 1, 3**700, 10**400 - 3]
    ms += [rng.randrange(1, 1 << rng.randrange(1, 1500)) for _ in range(120)]
    return ms


def test_setup_constants():
    ctx = barrett_setup(47)
    assert (ctx.n, ctx.k, ctx.mu) == (47, 6, 87)
    with pytest.raises(ValueError):
        barrett_setup(0)


def test_worked_examples():
    assert barrett_reduce(3561, barrett_setup(47)) == 36
    assert barrett_reduce(46 * 46, barrett_setup(47)) == 1
    ctx = barrett_setup(50)
    assert barrett_reduce(47 * 49, ctx) == 3
    assert corrections(47 * 49, ctx) == 2


def test_exhaustive_small_moduli():
    for n in range(1, 130):
        ctx = barrett_setup(n)
        for x in range(1 << (2 * ctx.k)):
            assert barrett_reduce(x, ctx) == x % n
            assert 0 <= corrections(x, ctx) <= 2


def test_random_against_python_mod():
    rng = random.Random(20261106)
    for n in moduli(rng):
        ctx = barrett_setup(n)
        top = 1 << (2 * ctx.k)
        xs = [0, 1, n - 1, n, (n - 1) * (n - 1), top - 1, max(top - n, 0)]
        xs += [rng.randrange(top) for _ in range(40)]
        for x in xs:
            assert barrett_reduce(x, ctx) == x % n
            assert 0 <= corrections(x, ctx) <= 2
        for _ in range(30):
            a, b = rng.randrange(n), rng.randrange(n)
            assert barrett_mulmod(a, b, ctx) == a * b % n
        for a in (0, 1, n - 1):
            assert barrett_mulmod(a, n - 1, ctx) == a * (n - 1) % n


def test_powmod_matches_pow():
    rng = random.Random(7)
    for n in moduli(rng)[:60]:
        ctx = barrett_setup(n)
        for _ in range(5):
            base = rng.randrange(n)
            e = rng.randrange(1 << rng.randrange(1, 200))
            assert barrett_powmod(base, e, ctx) == pow(base, e, n)
        assert barrett_powmod(0, 0, ctx) == pow(0, 0, n)


def test_rejects_out_of_range_inputs():
    ctx = barrett_setup(47)
    with pytest.raises(ValueError):
        barrett_reduce(-1, ctx)
    with pytest.raises(ValueError):
        barrett_reduce(1 << 12, ctx)
