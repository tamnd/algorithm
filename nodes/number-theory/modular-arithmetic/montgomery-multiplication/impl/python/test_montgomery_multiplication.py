# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/montgomery-multiplication/. The authors are listed in prov/C3XQAV.jsonl.

import random

import pytest

from montgomery_multiplication import (
    from_montgomery,
    mont_mul,
    montgomery_modmul,
    montgomery_pow,
    montgomery_setup,
    redc,
    to_montgomery,
)


def check_context(n: int, r: int | None = None) -> None:
    ctx = montgomery_setup(n, r)
    big_r = 1 << ctx.r
    assert big_r > n
    assert (n * ctx.n_prime + 1) % big_r == 0  # n * n' = -1 (mod R)
    assert 0 <= ctx.n_prime < big_r
    assert ctx.r2 == (big_r * big_r) % n


def check_redc(n: int, t: int, r: int | None = None) -> None:
    ctx = montgomery_setup(n, r)
    big_r = 1 << ctx.r
    u = redc(ctx, t)
    assert 0 <= u < n
    assert (u * big_r - t) % n == 0  # u = t * R^(-1) (mod n)


def test_example() -> None:
    ctx = montgomery_setup(97)
    assert ctx.r == 7 and ctx.n_prime == 95 and ctx.r2 == 88
    a_m = to_montgomery(ctx, 50)
    b_m = to_montgomery(ctx, 60)
    assert (a_m, b_m) == (95, 17)
    p_m = mont_mul(ctx, a_m, b_m)
    assert p_m == 74
    assert from_montgomery(ctx, p_m) == 50 * 60 % 97 == 90
    assert redc(ctx, 1615) == 74


def test_rejects_even_and_bad_input() -> None:
    for n in [0, -3, 2, 4, 1024, 2**64]:
        with pytest.raises(ValueError):
            montgomery_setup(n)
    with pytest.raises(ValueError):
        montgomery_setup(17, 4)
    with pytest.raises(ValueError):
        montgomery_pow(2, -1, 7)


def test_modulus_one_and_three() -> None:
    assert montgomery_modmul(5, 7, 1) == 0
    assert montgomery_pow(5, 0, 1) == 0
    for a in range(3):
        for b in range(3):
            assert montgomery_modmul(a, b, 3) == a * b % 3


def test_exhaustive_small() -> None:
    for n in range(1, 80, 2):
        check_context(n)
        ctx = montgomery_setup(n)
        big_r = 1 << ctx.r
        for t in range(n * big_r):
            if t % 7 == 0 or t < 3 * n:
                check_redc(n, t)
        for a in range(n):
            am = to_montgomery(ctx, a)
            assert am == a * big_r % n
            assert from_montgomery(ctx, am) == a
            for b in range(n):
                assert montgomery_modmul(a, b, n) == a * b % n


def test_word_sized_r() -> None:
    rng = random.Random(64)
    for _ in range(300):
        n = rng.randrange(1, 2**64) | 1
        check_context(n, 64)
        ctx = montgomery_setup(n, 64)
        a, b = rng.randrange(n), rng.randrange(n)
        am, bm = to_montgomery(ctx, a), to_montgomery(ctx, b)
        assert from_montgomery(ctx, mont_mul(ctx, am, bm)) == a * b % n
    for n in [2**64 - 59, 2**64 - 1, 2**63 + 1, 3, 1]:
        ctx = montgomery_setup(n, 64)
        for a, b in [(0, 0), (1 % n, n - 1), (n - 1, n - 1)]:
            am, bm = to_montgomery(ctx, a), to_montgomery(ctx, b)
            assert from_montgomery(ctx, mont_mul(ctx, am, bm)) == a * b % n


def test_random_small_and_edges() -> None:
    rng = random.Random(2024)
    for _ in range(3000):
        n = rng.randrange(1, 10**6) | 1
        a = rng.choice([0, 1, n - 1, rng.randrange(n)])
        b = rng.choice([0, 1, n - 1, rng.randrange(n)])
        assert montgomery_modmul(a, b, n) == a * b % n
        t = rng.randrange(n * (1 << n.bit_length()))
        check_redc(n, t)


def test_unreduced_inputs() -> None:
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randrange(1, 10**9) | 1
        a = rng.randrange(-(10**12), 10**12)
        b = rng.randrange(-(10**12), 10**12)
        assert montgomery_modmul(a, b, n) == a * b % n


def test_large_random() -> None:
    rng = random.Random(99)
    for _ in range(600):
        digits = rng.randrange(20, 601)
        n = rng.randrange(10 ** (digits - 1), 10**digits) | 1
        check_context(n)
        a, b = rng.randrange(n), rng.randrange(n)
        assert montgomery_modmul(a, b, n) == a * b % n
        t = rng.randrange(n << n.bit_length())
        check_redc(n, t)


def test_special_moduli() -> None:
    rng = random.Random(5)
    mods = [2**521 - 1, 2**127 - 1, (2**127 - 1) * (2**521 - 1), (2**61 - 1) ** 2,
            2**600 - 1, 2**600 + 1, 3**400, 10**300 + 1]
    for n in mods:
        check_context(n)
        for _ in range(20):
            a, b = rng.randrange(n), rng.randrange(n)
            assert montgomery_modmul(a, b, n) == a * b % n
        assert montgomery_modmul(n - 1, n - 1, n) == 1


def test_pow_against_reference() -> None:
    rng = random.Random(31)
    for _ in range(500):
        n = rng.randrange(1, 10**rng.randrange(1, 60)) | 1
        base = rng.randrange(-(10**30), 10**30)
        e = rng.randrange(0, 10**rng.randrange(1, 40))
        assert montgomery_pow(base, e, n) == pow(base, e, n)
    n = 2**521 - 1
    assert montgomery_pow(3, n - 1, n) == 1
    assert montgomery_pow(2, 560, 561) == 1
