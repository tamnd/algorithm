# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feige-fiat-shamir-identification/. The authors are listed in prov/TZZGFT.jsonl.
# There are no official test vectors for the Feige-Fiat-Shamir scheme. The
# tests use the toy Blum integer 499 * 547 and the tiny one 7 * 11, and run
# local simulated parties.

import random
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd

from feige_fiat_shamir_identification import (
    N,
    P,
    Q,
    GuessingProver,
    Prover,
    extract_secret,
    identify,
    jacobi,
    keygen,
    prod_selected,
    secret_from_public,
    simulate,
    sqrt_mod_blum,
    verify_round,
)


def test_modulus_is_a_blum_integer():
    assert N == 272953 and P % 4 == 3 and Q % 4 == 3
    # -1 has Jacobi symbol +1 but is not a square mod N.
    assert jacobi(N - 1, N) == 1
    assert pow(N - 1, (P - 1) // 2, P) == P - 1


def test_jacobi_against_euler_for_primes():
    for p in (P, Q, 7, 11, 23):
        for a in range(1, 60):
            if a % p:
                euler = pow(a, (p - 1) // 2, p)
                assert jacobi(a, p) == (1 if euler == 1 else -1)
    # Multiplicative in the modulus.
    for a in range(1, 200):
        assert jacobi(a, N) == jacobi(a, P) * jacobi(a, Q)


def test_page_example():
    s, n = [5, 7, 11], N
    v = [pow(5, -2, n), n - pow(7, -2, n), pow(11, -2, n)]
    prover = Prover(s)
    x = prover.commit(r=1000, sign=1)
    e = [1, 0, 1]
    y = prover.respond(e)
    assert (x, y) == (n - 1000000 % n, 55000)
    assert verify_round(v, x, e, y)


def test_completeness():
    rng = random.Random(1)
    s, v = keygen(5, rand=rng.randrange)
    prover = Prover(s, rand=rng.randrange)
    for _ in range(100):
        assert identify(prover, v, rounds=4, rand=rng.randrange)


def test_guessing_prover_wins_exactly_two_to_minus_k_per_round():
    rng = random.Random(2)
    k = 3
    _, v = keygen(k, rand=rng.randrange)
    wins = total = 0
    for guess in product((0, 1), repeat=k):
        cheat = GuessingProver(v, list(guess), y=12345)
        x = cheat.commit()
        for e in product((0, 1), repeat=k):
            total += 1
            wins += verify_round(v, x, list(e), cheat.respond(list(e)))
    assert Fraction(wins, total) == Fraction(1, 2**k)


def test_guessing_prover_over_several_rounds():
    rng = random.Random(3)
    k, t = 2, 3                      # 2^-6 = 1/64 in theory
    _, v = keygen(k, rand=rng.randrange)
    passed = 0
    trials = 6400
    for _ in range(trials):
        ok = True
        for _ in range(t):
            cheat = GuessingProver(v, [rng.randrange(2) for _ in range(k)], y=rng.randrange(1, N))
            x = cheat.commit()
            e = [rng.randrange(2) for _ in range(k)]
            if not verify_round(v, x, e, cheat.respond(e)):
                ok = False
                break
        passed += ok
    assert 60 < passed < 145            # mean 100


def test_factorization_gives_square_roots():
    rng = random.Random(4)
    for _ in range(200):
        a = rng.randrange(1, N)
        if gcd(a, N) != 1:
            continue
        sq = a * a % N
        r = sqrt_mod_blum(sq)
        assert r * r % N == sq


def test_holder_of_the_factors_can_impersonate():
    # The secret keys are found from the public keys with the factors, so the
    # factorization must stay secret: computing square roots mod N is as
    # hard as factoring N.
    rng = random.Random(5)
    s, v = keygen(4, rand=rng.randrange)
    found = [secret_from_public(vj) for vj in v]
    for sj, vj in zip(found, v):
        assert sj * sj % N * vj % N in (1, N - 1)
    assert identify(Prover(found, rand=rng.randrange), v, rounds=10, rand=rng.randrange)


def test_extraction_from_two_answers():
    rng = random.Random(6)
    k = 4
    s, v = keygen(k, rand=rng.randrange)
    prover = Prover(s, rand=rng.randrange)
    for j in range(k):
        x = prover.commit()
        e1 = [rng.randrange(2) for _ in range(k)]
        e1[j] = 1
        e2 = list(e1)
        e2[j] = 0
        y1, y2 = prover.respond(e1), prover.respond(e2)
        assert verify_round(v, x, e1, y1) and verify_round(v, x, e2, y2)
        sj = extract_secret(y1, y2)
        assert sj * sj % N * v[j] % N in (1, N - 1)
        assert sj == s[j]


def test_signs_hide_quadratic_residuosity_tiny():
    # n = 77 = 7 * 11. Over all s in Z_77^* and both signs, v = +-s^-2 hits
    # every unit of Jacobi symbol +1 equally often, squares or not.
    n = 77
    units = [a for a in range(1, n) if gcd(a, n) == 1]
    counts = Counter()
    for s in units:
        for sign in (0, 1):
            vj = pow(s, -2, n)
            counts[n - vj if sign else vj] += 1
    plus = [a for a in units if jacobi(a, n) == 1]
    assert sorted(counts) == plus and len(plus) == 30
    assert set(counts.values()) == {4}
    # Without signs only the 15 squares occur, so v would leak that it is a square.
    assert len({pow(s, -2, n) for s in units}) == 15


def test_simulator_matches_real_rounds_tiny():
    # For each fixed challenge, real (x, y) over all r and signs equals the
    # simulated (x, y) over all y and signs, as multisets.
    n = 77
    units = [a for a in range(1, n) if gcd(a, n) == 1]
    s = [2, 13]
    v = [pow(2, -2, n), n - pow(13, -2, n)]
    prover = Prover(s, n)
    for e in product((0, 1), repeat=2):
        e = list(e)
        real, sim = Counter(), Counter()
        for r in units:
            for sign in (0, 1):
                x = prover.commit(r, sign)
                real[(x, prover.respond(e))] += 1
        for y in units:
            for sign in (0, 1):
                sim[(simulate(v, e, y, sign, n), y)] += 1
        assert real == sim
        for x, y in sim:
            assert verify_round(v, x, e, y, n)


def test_verifier_rejects_zero():
    _, v = keygen(2, rand=random.Random(7).randrange)
    assert not verify_round(v, 0, [0, 0], 0)
    assert prod_selected([3, 5], [1, 1], N) == 15
