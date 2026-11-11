# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arora-ge-algorithm/. The authors are listed in prov/SGHADM.jsonl.
"""Tests for the Arora-Ge linearization attack.

Arora-Ge is a cryptanalytic algorithm with no official test vectors. The
tests use a hand-checked equation, an oracle that knows s (the true vector
of monomial values must solve the system), and 500 random toy instances
with a fixed seed.
"""

import random

from arora_ge_algorithm import (
    arora_ge,
    equation_row,
    lwe_samples,
    monomials,
    poly_from_roots,
    solve_mod_prime,
    unknown_count,
)

E3 = [-1, 0, 1]


def test_polynomial_and_monomials():
    assert poly_from_roots(E3, 31) == [0, 30, 0, 1]  # t^3 - t
    assert unknown_count(4, 3) == 34 == len(monomials(4, 3))
    assert unknown_count(3, 3) == 19 == len(monomials(3, 3))
    assert monomials(2, 2) == [(1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]


def test_hand_checked_row():
    # q = 31, a = (3, 7), b = 7 (s = (5, 12), e = 1). P(7 - 3 s1 - 7 s2) expands to
    # 27 s1 + s2 + 3 s1^2 + 14 s1 s2 + 6 s2^2 + 4 s1^3 + 28 s1^2 s2 + 24 s1 s2^2 + 29 s2^3 = 5.
    row, rhs = equation_row([3, 7], 7, poly_from_roots(E3, 31), monomials(2, 3), 31)
    assert row == [27, 1, 3, 14, 6, 4, 28, 24, 29]
    assert rhs == 5


def test_true_monomials_satisfy_every_row():
    rng = random.Random(1)
    q = 101
    for n in (2, 3, 4):
        mons = monomials(n, 3)
        P = poly_from_roots(E3, q)
        samples, s = lwe_samples(n, 50, q, E3, rng)
        y = []
        for alpha in mons:
            v = 1
            for si, k in zip(s, alpha):
                v = v * pow(si, k, q) % q
            y.append(v)
        for a, b in samples:
            row, rhs = equation_row(a, b, P, mons, q)
            assert sum(c * v for c, v in zip(row, y)) % q == rhs


def test_random_instances_recover_secret():
    rng = random.Random(2)
    wins = 0
    for _ in range(500):
        n = 4 if rng.random() < 0.3 else 3
        q = rng.choice((31, 101))
        samples, s = lwe_samples(n, unknown_count(n, 3) + 10, q, E3, rng)
        got = arora_ge(samples, E3, q)
        assert got is None or got == s  # never a wrong secret
        wins += got == s
    assert wins >= 495


def test_binary_errors():
    rng = random.Random(3)
    for _ in range(50):
        samples, s = lwe_samples(4, unknown_count(4, 2) + 10, 101, [0, 1], rng)
        assert arora_ge(samples, [0, 1], 101) == s


def test_too_few_samples_fails_cleanly():
    rng = random.Random(4)
    samples, s = lwe_samples(4, 20, 101, E3, rng)  # 20 < 34 unknowns
    assert arora_ge(samples, E3, 101) is None


def test_error_outside_set_makes_system_inconsistent():
    rng = random.Random(5)
    q, n = 101, 3
    samples, s = lwe_samples(n, unknown_count(n, 3) + 20, q, E3, rng)
    a, b = samples[0]
    samples[0] = (a, (b + 2) % q)  # now the error of this sample is 2 or 3
    got = arora_ge(samples, E3, q)
    assert got is None


def test_solver_small_system():
    # x + 2y = 5, 3x + 4y = 6 mod 7: x = 3, y = 1.
    assert solve_mod_prime([[1, 2], [3, 4]], [5, 6], 7) == [3, 1]
    assert solve_mod_prime([[1, 2], [2, 4]], [5, 3], 7) is None  # consistent, rank 1
    assert solve_mod_prime([[1, 2], [2, 4]], [5, 4], 7) is None  # inconsistent
