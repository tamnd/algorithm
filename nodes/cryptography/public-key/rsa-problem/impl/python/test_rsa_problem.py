# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-problem/. The authors are listed in prov/07Z52Q.jsonl.

import math
import random

from rsa_problem import (
    blind_instance,
    factor_from_exponents,
    private_exponent_from_factors,
    solve_with_average_case_oracle,
    solve_with_factors,
    unblind_solution,
)

# Toy primes of 128 binary digits each, drawn once with random.Random(20251111)
# and a Miller-Rabin test. They are far too small for real use.
P = 0xE0DEC55CD236DA7CDEDC1501D5CA4963
Q = 0xA22718A3686D1ABB32D27DD8536DC491
N = P * Q
E = 65537


def test_toy_key_is_well_formed() -> None:
    assert N.bit_length() == 256
    lam = (P - 1) * (Q - 1) // math.gcd(P - 1, Q - 1)
    d = private_exponent_from_factors(E, P, Q)
    assert E * d % lam == 1


def test_factoring_solves_the_rsa_problem() -> None:
    """The reduction in the easy direction, on 200 random instances."""
    rnd = random.Random(1)
    for _ in range(200):
        m = rnd.randrange(N)
        c = pow(m, E, N)
        assert solve_with_factors(N, E, c, P, Q) == m


def test_private_exponent_gives_the_factorization() -> None:
    """Miller's probabilistic algorithm recovers p and q from (N, e, d)."""
    rnd = random.Random(2)
    d = private_exponent_from_factors(E, P, Q)
    got = factor_from_exponents(N, E, d, 64, lambda k: rnd.randrange(k))
    assert got == (min(P, Q), max(P, Q))


def test_factorization_works_for_d_modulo_phi() -> None:
    """The same algorithm works when d is taken modulo phi(N) instead of lambda(N)."""
    rnd = random.Random(3)
    d = pow(E, -1, (P - 1) * (Q - 1))
    got = factor_from_exponents(N, E, d, 64, lambda k: rnd.randrange(k))
    assert got == (min(P, Q), max(P, Q))


def test_factorization_with_many_small_keys() -> None:
    """20 small keys, each factored from its exponent pair."""
    rnd = random.Random(4)
    primes = [1000003, 1000033, 1000037, 1000039, 1000081, 1000099, 1000117, 1000121]
    for _ in range(20):
        p, q = rnd.sample(primes, 2)
        n = p * q
        lam = (p - 1) * (q - 1) // math.gcd(p - 1, q - 1)
        e = 65537 if math.gcd(65537, lam) == 1 else 5
        if math.gcd(e, lam) != 1:
            continue
        d = pow(e, -1, lam)
        got = factor_from_exponents(n, e, d, 64, lambda k: rnd.randrange(k))
        assert got == (min(p, q), max(p, q))


def test_one_base_often_fails_so_the_loop_is_needed() -> None:
    """With a single base the algorithm can fail, which is why it repeats."""
    d = private_exponent_from_factors(E, P, Q)
    failures = 0
    for seed in range(40):
        rnd = random.Random(seed)
        if factor_from_exponents(N, E, d, 1, lambda k: rnd.randrange(k)) is None:
            failures += 1
    assert 0 <= failures <= 30  # a failure rate near or below 1/2


def test_random_self_reduction() -> None:
    """A fixed instance is solved with one query to an oracle for random instances."""
    d = private_exponent_from_factors(E, P, Q)
    seen = []

    def oracle(c: int) -> int:
        seen.append(c)
        return pow(c, d, N)

    rnd = random.Random(5)
    for _ in range(50):
        m = rnd.randrange(N)
        c = pow(m, E, N)
        assert solve_with_average_case_oracle(N, E, c, oracle, lambda k: rnd.randrange(k)) == m
    assert len(seen) == 50
    assert len(set(seen)) == 50  # each query carries a fresh blinding factor


def test_blinding_round_trip_and_uniformity() -> None:
    rnd = random.Random(6)
    m = 123456789
    c = pow(m, E, N)
    values = set()
    for _ in range(100):
        r = rnd.randrange(1, N)
        if math.gcd(r, N) != 1:
            continue
        cb = blind_instance(N, E, c, r)
        values.add(cb)
        assert unblind_solution(N, pow(cb, private_exponent_from_factors(E, P, Q), N), r) == m
    assert len(values) > 90  # the blinded instance differs on each run


def test_bad_input_is_rejected() -> None:
    try:
        factor_from_exponents(N, 1, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("e*d - 1 = 0 was accepted")
    try:
        blind_instance(N, E, 1, P)
    except ValueError:
        pass
    else:
        raise AssertionError("a non invertible blinding factor was accepted")
    try:
        solve_with_factors(N, E, 1, P, Q + 2)
    except ValueError:
        pass
    else:
        raise AssertionError("wrong factors were accepted")
