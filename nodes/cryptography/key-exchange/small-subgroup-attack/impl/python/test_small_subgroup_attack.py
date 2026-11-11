# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/small-subgroup-attack/. The authors are listed in prov/MG2E7C.jsonl.

import math
import random

import pytest

from small_subgroup_attack import (
    G,
    P,
    Q,
    SAFE_G,
    SAFE_P,
    SAFE_Q,
    SMALL_PRIMES,
    ValidationError,
    Victim,
    crt,
    element_of_order,
    small_subgroup_attack,
)


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def test_toy_groups() -> None:
    assert _is_prime(P) and _is_prime(Q)
    assert P - 1 == 2 * Q * math.prod(SMALL_PRIMES)
    assert all(_is_prime(ell) for ell in SMALL_PRIMES)
    assert math.prod(SMALL_PRIMES) > Q
    assert G != 1 and pow(G, Q, P) == 1
    assert _is_prime(SAFE_P) and _is_prime(SAFE_Q) and SAFE_P == 2 * SAFE_Q + 1
    assert pow(SAFE_G, SAFE_Q, SAFE_P) == 1


def test_crt() -> None:
    assert crt([(2, 3), (3, 5), (2, 7)]) == (23, 105)


def test_attack_recovers_the_full_key_without_validation() -> None:
    rng = random.Random(1997)
    for _ in range(3):
        x = rng.randrange(1, Q)
        public = pow(G, x, P)
        victim = Victim(P, Q, x, validate=False)
        found, modulus = small_subgroup_attack(victim, P, SMALL_PRIMES, rng)
        assert modulus > Q
        assert found == x
        assert pow(G, found, P) == public


def test_validation_stops_the_attack_in_the_dsa_style_group() -> None:
    rng = random.Random(2017)
    victim = Victim(P, Q, rng.randrange(1, Q), validate=True)
    with pytest.raises(ValidationError):
        small_subgroup_attack(victim, P, SMALL_PRIMES, rng)
    # Honest public keys still pass.
    victim.respond(pow(G, 12345, P))


def test_safe_prime_group_with_validation() -> None:
    rng = random.Random(2016)
    x = rng.randrange(1, SAFE_Q)
    victim = Victim(SAFE_P, SAFE_Q, x, validate=True)
    # In a safe-prime group the only small subgroups have order 1 and 2.
    with pytest.raises(ValidationError):
        victim.respond(SAFE_P - 1)  # order 2
    with pytest.raises(ValidationError):
        victim.respond(1)
    # An element of order 2q is also rejected; without the check it would
    # leak x mod 2 and no more.
    nonresidue = SAFE_P - SAFE_G
    assert pow(nonresidue, SAFE_Q, SAFE_P) == SAFE_P - 1
    with pytest.raises(ValidationError):
        victim.respond(nonresidue)
    unchecked = Victim(SAFE_P, SAFE_Q, x, validate=False)
    found, modulus = small_subgroup_attack(unchecked, SAFE_P, [2], rng)
    assert modulus == 2 and found == x % 2


def test_element_of_order() -> None:
    rng = random.Random(5)
    for ell in SMALL_PRIMES:
        h = element_of_order(P, ell, rng)
        assert h != 1 and pow(h, ell, P) == 1
