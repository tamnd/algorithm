# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/menezes-okamoto-vanstone-reduction/. The authors are listed in prov/HWKGB7.jsonl.

import random

import pytest

from menezes_okamoto_vanstone_reduction import ec_add, ec_mul, mov_reduction, tate


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def _sieve(limit: int) -> list[bool]:
    flags = [True] * limit
    flags[0] = flags[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if flags[i]:
            flags[i * i :: i] = [False] * len(range(i * i, limit, i))
    return flags


_PRIME = _sieve(100000)


def primes_3_mod_4(lo: int, hi: int) -> list[int]:
    return [q for q in range(lo, hi) if q % 4 == 3 and _PRIME[q]]


def random_point(rng: random.Random, p: int) -> tuple[int, int]:
    while True:
        x = rng.randrange(p)
        r = (x * x * x + x) % p
        y = pow(r, (p + 1) // 4, p)
        if y * y % p == r:
            return x, (y if rng.randrange(2) else -y % p)


def multiples(P, p: int) -> list:
    """The multiples kP for 0 <= k < ord(P), in order, by repeated addition."""
    out = [None]
    T = P
    while T is not None:
        out.append(T)
        T = ec_add(T, P, p)
    return out


def odd_part(m: int) -> int:
    while m % 2 == 0:
        m //= 2
    return m


def point_of_odd_order(rng: random.Random, p: int):
    """A random point P with odd order n > 1 and the list of its multiples."""
    w = odd_part(p + 1)
    while True:
        P = ec_mul((p + 1) // w, random_point(rng, p), p)
        if P is not None:
            mult = multiples(P, p)
            return P, mult


def check(P, Q, mult: list, p: int, seed: int = 0) -> None:
    n = len(mult)
    x = mov_reduction(P, Q, n, p, seed)
    if Q in mult:
        assert x == mult.index(Q)
    else:
        assert x is None


def test_worked_example() -> None:
    p, P = 43, (4, 5)
    Q = (23, 8)  # 7 P
    assert mov_reduction(P, Q, 11, p) == 7
    R = ((41, 0), (0, 15))  # psi(2, 15)
    assert tate(P, R, 11, p) == (2, 30)
    assert tate(Q, R, 11, p) == (11, 40)
    assert mov_reduction(P, (2, 15), 11, p) is None  # (2, 15) has order 44


def test_curve_is_supersingular() -> None:
    # #E(F_p) = p + 1 for y^2 = x^3 + x and p = 3 mod 4.
    for p in primes_3_mod_4(3, 200):
        count = 1 + sum(1 for x in range(p) for y in range(p) if (y * y - x ** 3 - x) % p == 0)
        assert count == p + 1


def test_trivial_targets() -> None:
    rng = random.Random(1)
    ps = [q for q in primes_3_mod_4(7, 100000) if odd_part(q + 1) > 1]
    for _ in range(60):
        p = rng.choice(ps)
        P, mult = point_of_odd_order(rng, p)
        n = len(mult)
        assert mov_reduction(P, None, n, p) == 0
        assert mov_reduction(P, P, n, p) == 1


def test_small_primes_exhaustive() -> None:
    for p in primes_3_mod_4(7, 60):
        w = odd_part(p + 1)
        if w == 1:
            continue
        pts = [(x, y) for x in range(p) for y in range(p) if (y * y - x ** 3 - x) % p == 0]
        gens = {ec_mul((p + 1) // w, T, p) for T in pts} - {None}
        for P in sorted(gens):
            mult = multiples(P, p)
            for Q in [None] + pts:
                check(P, Q, mult, p)


def test_random_small_groups() -> None:
    rng = random.Random(2024)
    ps = [q for q in primes_3_mod_4(7, 5000) if odd_part(q + 1) > 1]
    for _ in range(300):
        p = rng.choice(ps)
        P, mult = point_of_odd_order(rng, p)
        Q = rng.choice(mult) if rng.random() < 0.5 else random_point(rng, p)
        check(P, Q, mult, p, rng.randrange(1000))


def test_random_large_groups() -> None:
    rng = random.Random(77)
    ps = [q for q in primes_3_mod_4(10000, 100000) if odd_part(q + 1) > 1]
    for _ in range(40):
        p = rng.choice(ps)
        P, mult = point_of_odd_order(rng, p)
        n = len(mult)
        for _ in range(3):
            x = rng.randrange(n)
            assert mov_reduction(P, mult[x], n, p, rng.randrange(1000)) == x
        check(P, random_point(rng, p), mult, p)


def test_prime_order_subgroups() -> None:
    rng = random.Random(5)
    ps = primes_3_mod_4(100, 100000)
    found = 0
    while found < 40:
        p = rng.choice(ps)
        w = odd_part(p + 1)
        r = max(d for d in range(3, w + 1, 2) if w % d == 0 and is_prime(d)) if w > 1 else 1
        if r < 3:
            continue
        P = None
        while P is None:
            P = ec_mul((p + 1) // r, random_point(rng, p), p)
        mult = multiples(P, p)
        assert len(mult) == r
        for _ in range(4):
            x = rng.randrange(r)
            assert mov_reduction(P, mult[x], r, p, rng.randrange(100)) == x
        check(P, random_point(rng, p), mult, p)
        found += 1


def test_composite_order_subgroups() -> None:
    rng = random.Random(9)
    ps = primes_3_mod_4(100, 50000)
    found = 0
    while found < 40:
        p = rng.choice(ps)
        w = odd_part(p + 1)
        divisors = [d for d in range(9, w + 1, 2) if w % d == 0 and not is_prime(d)]
        if not divisors:
            continue
        n = rng.choice(divisors)
        P = None
        while P is None or len(multiples(P, p)) != n:
            P = ec_mul((p + 1) // n, random_point(rng, p), p)
        mult = multiples(P, p)
        for _ in range(4):
            x = rng.randrange(n)
            assert mov_reduction(P, mult[x], n, p, rng.randrange(100)) == x
        # a random point of order dividing n; it lies in <P> because E(F_p) is cyclic
        check(P, ec_mul((p + 1) // n, random_point(rng, p), p), mult, p)
        found += 1


def test_seed_independence_of_answer() -> None:
    for seed in range(20):
        assert mov_reduction((4, 5), (23, 8), 11, 43, seed) == 7


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        mov_reduction((1, 1), (1, 1), 3, 41)  # p = 1 mod 4
    with pytest.raises(ValueError):
        mov_reduction((4, 5), (4, 5), 22, 43)  # even n
