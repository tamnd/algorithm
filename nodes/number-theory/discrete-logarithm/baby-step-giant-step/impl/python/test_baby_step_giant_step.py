# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baby-step-giant-step/. The authors are listed in prov/KW87TP.jsonl.

import random
from math import gcd

import pytest

from baby_step_giant_step import baby_step_giant_step


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


def order(g: int, p: int) -> int:
    return len(power_table(g, p))


def test_worked_example() -> None:
    # p = 23, g = 5, h = 8: m = 5, baby steps 1, 5, 2, 10, 4; answer 6.
    assert baby_step_giant_step(5, 8, 22, 23) == 6
    assert baby_step_giant_step(2, 8, 22, 23) == 3
    assert baby_step_giant_step(2, 5, 22, 23) is None
    assert baby_step_giant_step(2, 5, 11, 23) is None


def test_edge_cases() -> None:
    assert baby_step_giant_step(5, 1, 22, 23) == 0
    assert baby_step_giant_step(5, 5, 22, 23) == 1
    assert baby_step_giant_step(1, 1, 1, 7) == 0
    assert baby_step_giant_step(1, 3, 6, 7) is None
    assert baby_step_giant_step(22, 22, 2, 23) == 1
    assert baby_step_giant_step(22, 1, 2, 23) == 0
    assert baby_step_giant_step(22, 5, 2, 23) is None
    assert baby_step_giant_step(1, 1, 1, 2) == 0
    assert baby_step_giant_step(1, 0, 1, 2) is None
    assert baby_step_giant_step(3, 0, 6, 7) is None
    assert baby_step_giant_step(3, 7 + 6, 6, 7) == 3  # h is reduced modulo p
    with pytest.raises(ValueError):
        baby_step_giant_step(2, 3, 0, 7)
    with pytest.raises(ValueError):
        baby_step_giant_step(2, 3, 6, 1)


def test_every_target_small_primes() -> None:
    for p in [2, 3, 5, 7, 11, 13, 23, 31, 97, 101]:
        for g in range(1, p):
            tab = power_table(g, p)
            for h in range(p):
                assert baby_step_giant_step(g, h, p - 1, p) == tab.get(h), (g, h, p)
                assert baby_step_giant_step(g, h, len(tab), p) == tab.get(h), (g, h, p)


def test_random_against_brute_force() -> None:
    rng = random.Random(20261106)
    primes = [q for q in range(3, 100000) if is_prime(q)]
    small = [q for q in primes if q < 3000]
    cases = 0
    for trial in range(400):
        p = rng.choice(primes if trial % 8 == 0 else small)
        r = rng.randrange(2, p)
        kind = trial % 4
        if kind == 0:
            g = r  # any element: generator or not
        else:
            # a subgroup of chosen order d | p - 1 (prime or composite)
            divs = [d for d in range(1, p) if (p - 1) % d == 0]
            d = rng.choice(divs)
            g = pow(r, (p - 1) // d, p)
        tab = power_table(g, p)
        n_bound = rng.choice([p - 1, len(tab), len(tab) + rng.randrange(0, 50)])
        targets = [1, g, rng.randrange(1, p), rng.randrange(0, p)]
        targets.append(pow(g, rng.randrange(0, len(tab)), p))
        for h in targets:
            assert baby_step_giant_step(g, h, n_bound, p) == tab.get(h % p), (g, h, p, n_bound)
            cases += 1
    assert cases >= 2000


def test_composite_moduli() -> None:
    rng = random.Random(7)
    for _ in range(300):
        p = rng.randrange(2, 3000)
        g = rng.randrange(1, p)
        if gcd(g, p) != 1:
            continue
        tab = power_table(g, p)
        for h in [1, g, rng.randrange(0, p), pow(g, rng.randrange(0, 1000), p)]:
            assert baby_step_giant_step(g, h, p, p) == tab.get(h % p), (g, h, p)
