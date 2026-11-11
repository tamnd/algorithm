# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffie-hellman/. The authors are listed in prov/65FYHX.jsonl.

import random

import pytest

from diffie_hellman import G, P, Q, ValidationError, generate_key_pair, shared_secret, validate_public_value


def _arctan_inv(x: int, one: int) -> int:
    """arctan(1/x) * one, by the Taylor series in integer arithmetic."""
    total = term = one // x
    x2 = x * x
    k = 1
    while term:
        term //= x2
        k += 2
        total += -(term // k) if k % 4 == 3 else term // k
    return total


def _floor_pi_times_2_to(e: int) -> int:
    """floor(2^e * pi) by Machin's formula, with 64 guard bits."""
    guard = 64
    one = 1 << (e + guard)
    pi = 16 * _arctan_inv(5, one) - 4 * _arctan_inv(239, one)
    return pi >> guard


def _is_probable_prime(n: int, rounds: int, rng: random.Random) -> bool:
    if n % 2 == 0:
        return n == 2
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = rng.randrange(2, n - 1)
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


def test_rfc3526_prime_matches_its_formula() -> None:
    # RFC 3526 Section 3: p = 2^2048 - 2^1984 - 1 + 2^64 * ( [2^1918 pi] + 124476 ).
    expected = 2**2048 - 2**1984 - 1 + 2**64 * (_floor_pi_times_2_to(1918) + 124476)
    assert P == expected
    assert P.bit_length() == 2048


def test_rfc3526_prime_is_a_safe_prime() -> None:
    rng = random.Random(3526)
    assert _is_probable_prime(P, 4, rng)
    assert _is_probable_prime(Q, 4, rng)
    assert P == 2 * Q + 1
    # g = 2 is a square mod p because p = 7 mod 8, so it has order q.
    assert P % 8 == 7
    assert pow(G, Q, P) == 1


def test_both_sides_get_the_same_key() -> None:
    rng = random.Random(1976)
    for _ in range(3):
        a, big_a = generate_key_pair(rng)
        b, big_b = generate_key_pair(rng)
        validate_public_value(big_a)
        validate_public_value(big_b)
        k1 = shared_secret(a, big_b)
        k2 = shared_secret(b, big_a)
        assert k1 == k2
        assert len(k1) == 256


def test_validation_rejects_bad_values() -> None:
    rng = random.Random(800)
    x, _ = generate_key_pair(rng)
    # p - 1 has order 2. Since p = 3 mod 4, -1 is a non-residue, so -2 is one
    # too and lies outside the subgroup of order q.
    non_residue = P - G
    assert pow(non_residue, Q, P) == P - 1
    for y in (0, 1, P - 1, P, P + 5, non_residue):
        with pytest.raises(ValidationError):
            validate_public_value(y)
        with pytest.raises(ValidationError):
            shared_secret(x, y)


def test_secret_exponents_are_in_range() -> None:
    rng = random.Random(42)
    xs = [generate_key_pair(rng)[0] for _ in range(20)]
    assert all(1 <= x < Q for x in xs)
    assert len(set(xs)) == 20
