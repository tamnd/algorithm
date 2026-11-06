# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/number-field-sieve-discrete-logarithm/. The authors are listed in prov/YRSSHK.jsonl.

import random

import pytest

from number_field_sieve_discrete_logarithm import (
    QUADRATIC_FIELDS,
    _algebraic_primes,
    _unit_powers,
    nfs_dlog,
    nfs_polynomials,
    norm,
    qdiv,
    qmul,
)


def is_prime(n: int) -> bool:
    return n > 1 and all(n % i for i in range(2, int(n**0.5) + 1))


def covered(p: int) -> bool:
    try:
        nfs_polynomials(p)
        return True
    except ValueError:
        return False


def powers(g: int, p: int) -> dict[int, int]:
    """Map g^i mod p to i for i in [0, ord g), by brute force."""
    table, y, i = {}, 1, 0
    while y not in table:
        table[y] = i
        y = y * g % p
        i += 1
    return table


def generator(p: int) -> int:
    return next(c for c in range(1, p) if len(powers(c, p)) == p - 1)


PRIMES = [p for p in range(3, 2000) if is_prime(p)]


def test_polynomials():
    for p in PRIMES:
        u, v, c, d = nfs_polynomials(p)
        assert (u, v) in QUADRATIC_FIELDS and d >= 1 and c * c + u * c * d + v * d * d == p
        s = c * pow(d, -1, p) % p
        assert (s * s + u * s + v) % p == 0
    for p in (2, 3167, 8543):
        with pytest.raises(ValueError):
            nfs_polynomials(p)


def test_ring_arithmetic():
    rng = random.Random(4)
    for u, v in QUADRATIC_FIELDS:
        units = _unit_powers(u, v)
        assert len(units) == {(0, 1): 4, (1, 1): 6}.get((u, v), 2)
        for _ in range(50):
            x = (rng.randrange(-30, 31), rng.randrange(-30, 31))
            y = (rng.randrange(-30, 31), rng.randrange(1, 31))
            assert norm(qmul(x, y, u, v), u, v) == norm(x, u, v) * norm(y, u, v)
            assert qdiv(qmul(x, y, u, v), y, u, v) == x
        disc = u * u - 4 * v
        pis = _algebraic_primes(60, u, v, units)
        for q in (q for q in range(2, 61) if is_prime(q)):
            count = sum(1 for z in pis if norm(z, u, v) == q)
            if disc % q == 0:
                assert count == 1  # ramified
            elif q > 2:
                assert count == (2 if pow(disc % q, (q - 1) // 2, q) == 1 else 0)
            inert = sum(1 for z in pis if norm(z, u, v) == q * q)
            assert inert == (1 if count == 0 and q * q <= 60 else 0)


def test_worked_example():
    p = 37
    assert nfs_polynomials(p) == (0, 1, 6, 1)  # f1 = x^2 + 1, f2 = x - 6
    assert _algebraic_primes(5, 0, 1, _unit_powers(0, 1)) == [(1, 1), (2, -1), (2, 1)]
    g = 16  # 2^4, of order 9
    assert len(powers(g, p)) == 9 and pow(g, 3, p) == 26 and pow(g, 5, p) == 33
    for seed in range(5):
        assert nfs_dlog(g, 26, 9, p, seed=seed, bound=5) == 3
        assert nfs_dlog(g, 33, 9, p, seed=seed, bound=5) == 5


def test_trivial_targets():
    assert nfs_dlog(1, 1, 1, 2) == 0
    for p in (3, 5, 7, 11, 13, 101, 1009):
        assert nfs_dlog(1, 1, 1, p) == 0
        assert nfs_dlog(1, 2, 1, p) is None
        for g in (2, p - 1, generator(p)):
            r = len(powers(g, p))
            assert nfs_dlog(g, 1, r, p) == 0
            assert nfs_dlog(g, g, r, p) == (1 if r > 1 else 0)


def test_small_primes_exhaustive():
    for p in [q for q in PRIMES if q < 32]:
        for g in range(1, p, 1 if p < 20 else 2):
            table = powers(g, p)
            for h in range(1, p):
                assert nfs_dlog(g, h, len(table), p, seed=h) == table.get(h), (p, g, h)


def test_random_primes_against_brute_force():
    rng = random.Random(1)
    done = 0
    while done < 20:
        p = rng.randrange(3, 100000)
        if not is_prime(p) or not covered(p):
            continue
        done += 1
        g = rng.randrange(1, p)
        table = powers(g, p)
        h = rng.randrange(1, p)
        assert nfs_dlog(g, h, len(table), p, seed=done) == table.get(h), (p, g, h)
        x = rng.randrange(len(table))
        assert nfs_dlog(g, pow(g, x, p), len(table), p, seed=x) == x


def test_generators_and_subgroups():
    rng = random.Random(2)
    for p in (1009, 10007, 65537, 99991):
        gamma = generator(p)
        divisors = [d for d in range(2, p) if (p - 1) % d == 0]
        for r in rng.sample(divisors, min(2, len(divisors))) + [p - 1]:
            g = pow(gamma, (p - 1) // r, p)
            x = rng.randrange(r)
            assert nfs_dlog(g, pow(g, x, p), r, p, seed=x) == x
            z = rng.randrange(1, p)
            assert nfs_dlog(g, z, r, p) == powers(g, p).get(z)


def test_prime_and_composite_orders():
    p = 7561  # p - 1 = 2^3 * 3^3 * 5 * 7
    gamma = generator(p)
    for r in (2, 8, 3, 27, 5, 7, 35, 216, 1890, p - 1):
        g = pow(gamma, (p - 1) // r, p)
        for x in (0, 1, r - 1):
            assert nfs_dlog(g, pow(g, x, p), r, p) == x
        assert nfs_dlog(g, gamma, r, p) == (None if r < p - 1 else 1)


def test_no_solution_is_reported():
    rng = random.Random(3)
    found = 0
    for _ in range(80):
        p = rng.choice([101, 257, 1009, 4001, 12289])
        g = rng.randrange(1, p)
        table = powers(g, p)
        h = rng.randrange(1, p)
        if h not in table:
            found += 1
            assert nfs_dlog(g, h, len(table), p) is None
    assert found >= 10


def test_seed_independence():
    p = 50021
    g = generator(p)
    h = pow(g, 31337, p)
    assert {nfs_dlog(g, h, p - 1, p, seed=s) for s in range(3)} == {31337}
    assert {nfs_dlog(g, h, p - 1, p, seed=s, bound=b) for s, b in ((0, 8), (1, 60))} == {31337}


def test_bad_input():
    with pytest.raises(ValueError):
        nfs_dlog(0, 1, 1, 13)
    with pytest.raises(ValueError):
        nfs_dlog(1, 13, 1, 13)
    with pytest.raises(ValueError):
        nfs_dlog(1, 1, 0, 13)
    with pytest.raises(ValueError):
        nfs_dlog(5, 3, 3166, 3167)  # 3167 splits in none of the nine fields
