# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pohlig-hellman/. The authors are listed in prov/PW5NFF.jsonl.

import random
from math import gcd

import pytest

from pohlig_hellman import pohlig_hellman


def factor(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def is_prime(n: int) -> bool:
    return n >= 2 and factor(n) == {n: 1}


def phi(n: int) -> int:
    r = n
    for q in factor(n):
        r = r // q * (q - 1)
    return r


def power_table(g: int, p: int) -> dict[int, int]:
    seen: dict[int, int] = {}
    e, x = 1 % p, 0
    while e not in seen:
        seen[e] = x
        e, x = e * g % p, x + 1
    return seen


def test_worked_example() -> None:
    # Galbraith, Example 13.2.3: p = 19, g = 2, h = 5, p - 1 = 2 * 3^2, answer 16.
    assert pohlig_hellman(2, 5, 19, {2: 1, 3: 2}) == 16
    # HAC, Example 3.64: p = 251, alpha = 71, beta = 210, answer 197.
    assert pohlig_hellman(71, 210, 251, factor(250)) == 197
    # g = 4 has order 9 modulo 19, and 2 is not a power of 4.
    assert pohlig_hellman(4, 2, 19, {2: 1, 3: 2}) is None
    assert pohlig_hellman(4, 16, 19, {2: 1, 3: 2}) == 2


def test_edge_cases() -> None:
    f22 = {2: 1, 11: 1}
    assert pohlig_hellman(5, 1, 23, f22) == 0
    assert pohlig_hellman(5, 5, 23, f22) == 1
    assert pohlig_hellman(1, 1, 23, f22) == 0
    assert pohlig_hellman(1, 5, 23, f22) is None
    assert pohlig_hellman(22, 22, 23, f22) == 1
    assert pohlig_hellman(5, 0, 23, f22) is None
    assert pohlig_hellman(1, 1, 2, {}) == 0
    assert pohlig_hellman(1, 0, 2, {}) is None
    # a multiple of the order is enough: 2^4 * 3 * 11 * 7 is a multiple of 22
    assert pohlig_hellman(5, 8, 23, {2: 4, 3: 1, 7: 1, 11: 1}) == 6
    # 2^16 + 1 is prime and the group order is a power of two
    assert pohlig_hellman(3, pow(3, 40000, 65537), 65537, {2: 16}) == 40000
    with pytest.raises(ValueError):
        pohlig_hellman(1, 1, 1, {})


def test_every_target_small_primes() -> None:
    for p in [3, 5, 7, 13, 17, 31, 37, 73, 97]:
        fp = factor(p - 1)
        for g in range(1, p):
            tab = power_table(g, p)
            for h in range(p):
                assert pohlig_hellman(g, h, p, fp) == tab.get(h), (g, h, p)


def test_random_primes_against_brute_force() -> None:
    rng = random.Random(1978)
    primes = [q for q in range(3, 100000) if is_prime(q)]
    cases = 0
    for trial in range(300):
        p = rng.choice(primes)
        fp = factor(p - 1)
        r = rng.randrange(2, p)
        if trial % 3 == 0:
            g = r
        else:
            divs = [1]
            for q, e in fp.items():
                divs = [d * q ** i for d in divs for i in range(e + 1)]
            g = pow(r, (p - 1) // rng.choice(divs), p)
        tab = power_table(g, p)
        for h in [1, g, rng.randrange(0, p), rng.randrange(1, p), pow(g, rng.randrange(len(tab)), p)]:
            assert pohlig_hellman(g, h, p, fp) == tab.get(h), (g, h, p)
            cases += 1
    assert cases >= 1500


def test_composite_moduli_non_cyclic() -> None:
    rng = random.Random(15)
    for _ in range(400):
        n = rng.randrange(2, 2500)
        g = rng.randrange(1, n)
        if gcd(g, n) != 1:
            continue
        fn = factor(phi(n))
        tab = power_table(g, n)
        for h in [1, g, rng.randrange(0, n), pow(g, rng.randrange(0, 999), n)]:
            assert pohlig_hellman(g, h, n, fn) == tab.get(h % n), (g, h, n)
    # (Z/15Z)^* is Z/2 x Z/4: 4 has order 2, and 11 has order 2 but is not a power of 4.
    assert pohlig_hellman(4, 11, 15, {2: 3}) is None
    assert pohlig_hellman(4, 4, 15, {2: 3}) == 1
