# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regev-factoring-algorithm/. The authors are listed in prov/GJ2PQ0.jsonl.
"""Tests of Regev's factoring algorithm on small moduli, with fixed seeds."""

import cmath
import functools
import itertools
import math
import random
from fractions import Fraction

import pytest

from regev_factoring_algorithm import (
    Sampler,
    classical_checks,
    dft_nd,
    exponent_product,
    first_primes,
    lll,
    outcome_distribution,
    postprocessing_basis,
    product_mod,
    recover_factor,
    regev_factor,
    relation_lattice_contains,
    tree_product,
)

D, R = 64, 16.0


@functools.lru_cache(maxsize=None)
def distribution(N, d=2, D=D, R=R):
    a = [b * b for b in first_primes(d)]
    return outcome_distribution(N, a, D, R)


def exact_det(rows):
    m = [[Fraction(x) for x in r] for r in rows]
    n, det = len(m), Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c]), None)
        if p is None:
            return Fraction(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            det = -det
        det *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return det


def test_classical_checks():
    assert first_primes(6) == [2, 3, 5, 7, 11, 13]
    assert classical_checks(2 * 77, 2) == 2
    assert classical_checks(3 ** 5, 2) == 3
    assert classical_checks(121, 2) == 11
    assert classical_checks(3 * 37, 2) == 3
    assert classical_checks(77, 2) is None
    with pytest.raises(ValueError):
        classical_checks(3, 2)


def test_exponent_product_matches_direct_power():
    N, a, Dsmall = 77, [4, 9], 16
    for z in itertools.product(range(-Dsmall // 2, Dsmall // 2), repeat=2):
        e, big = exponent_product(z, a, N, Dsmall)
        assert e == product_mod(a, [zi + Dsmall // 2 for zi in z], N)
        assert big == 2 * 4  # one squaring and one small product per exponent bit
    rng = random.Random(5)
    N = 1000003 * 999983
    a = [b * b for b in first_primes(9)]
    for _ in range(50):
        z = [rng.randrange(-512, 512) for _ in a]
        assert exponent_product(z, a, N, 1024)[0] == product_mod(a, [zi + 512 for zi in z], N)
    assert tree_product([]) == 1 and tree_product(a) == math.prod(a)


def test_dft_matches_naive_transform():
    rng = random.Random(3)
    Dt, d = 4, 3
    arr = [complex(rng.random(), rng.random()) for _ in range(Dt ** d)]
    got = dft_nd(arr, Dt, d)
    for w in range(Dt ** d):
        wv = [(w // Dt ** i) % Dt for i in range(d)]
        want = sum(arr[z] * cmath.exp(2j * math.pi * sum(((z // Dt ** i) % Dt) * wv[i] for i in range(d)) / Dt)
                   for z in range(Dt ** d))
        assert abs(got[w] - want) < 1e-9


@pytest.mark.parametrize("N", [77, 143])
def test_outcome_characteristic_function(N):
    """E[exp(2 pi i <u, w> / D)] is exp(-pi |u|^2 / (2 R^2)) for u in L and 0 for u not in L."""
    dist = distribution(N)
    assert abs(sum(dist.values()) - 1) < 1e-9
    a = [4, 9]
    for u in itertools.product(range(-8, 9), repeat=2):
        chi = sum(p * cmath.exp(2j * math.pi * (u[0] * w[0] + u[1] * w[1]) / D) for w, p in dist.items())
        if relation_lattice_contains(a, u, N):
            assert abs(chi - math.exp(-math.pi * (u[0] ** 2 + u[1] ** 2) / (2 * R * R))) < 1e-6
        else:
            assert abs(chi) < 1e-6


def test_lll_output_is_reduced_basis_of_same_lattice():
    rng = random.Random(11)
    for _ in range(5):
        while True:
            B = [[rng.randrange(-50, 51) for _ in range(5)] for _ in range(5)]
            if exact_det(B):
                break
        red = lll(B)
        assert abs(exact_det(red)) == abs(exact_det(B))
        star, sq = [], []
        for i, v in enumerate(red):
            vv = [Fraction(x) for x in v]
            for j in range(i):
                mu = sum(Fraction(x) * y for x, y in zip(v, star[j])) / sq[j]
                assert abs(mu) <= Fraction(1, 2)  # size reduced
                vv = [x - mu * y for x, y in zip(vv, star[j])]
            star.append(vv)
            sq.append(sum(x * x for x in vv))
        for k in range(1, 5):
            mu = sum(Fraction(x) * y for x, y in zip(red[k], star[k - 1])) / sq[k - 1]
            assert sq[k] >= (Fraction(3, 4) - mu * mu) * sq[k - 1]  # Lovasz condition


def test_lll_vectors_are_in_input_lattice():
    rng = random.Random(12)
    B = [[rng.randrange(-30, 31) for _ in range(4)] for _ in range(4)]
    while not exact_det(B):
        B = [[rng.randrange(-30, 31) for _ in range(4)] for _ in range(4)]
    red = lll(B)
    # solve v = c B for each reduced v and check that c is integral (Cramer's rule)
    det = exact_det(B)
    for v in red:
        for i in range(4):
            Bi = [list(r) for r in B]
            Bi[i] = list(v)
            assert (exact_det(Bi) / det).denominator == 1


def test_lift_of_lattice_vector_is_short():
    """Every u in L lifts to a vector of L' with the same first coordinates and small last ones."""
    N = 77
    rng = random.Random(2)
    s = Sampler(distribution(N))
    ws = [s.draw(rng) for _ in range(6)]
    basis = postprocessing_basis(ws, D)
    for u in [(1, -2), (-6, -3), (0, 15)]:
        tail = []
        for w in ws:
            t = (u[0] * w[0] + u[1] * w[1]) % D
            tail.append(t - D if t > D // 2 else t)
        lift = list(u) + tail
        # lift = u_1 b_1 + u_2 b_2 + sum_i k_i (D e_i) for integers k_i
        rest = [x - u[0] * y - u[1] * z for x, y, z in zip(lift, basis[0], basis[1])]
        assert rest[:2] == [0, 0] and all(r % D == 0 for r in rest)
        assert max(abs(t) for t in tail) <= D // 2


@pytest.mark.parametrize("N", [35, 77, 91, 143])
def test_end_to_end_factors(N):
    s = Sampler(distribution(N))
    found = 0
    for seed in range(10):
        f = regev_factor(N, 2, D, R, random.Random(seed), s)
        if f is not None:
            assert 1 < f < N and N % f == 0
            found += 1
    assert found >= 8


def test_prime_modulus_never_returns_a_factor():
    N = 101  # only +-1 are square roots of 1, so L = L0
    s = Sampler(distribution(N))
    for seed in range(5):
        assert regev_factor(N, 2, D, R, random.Random(seed), s) is None


def test_recover_factor_only_returns_true_factors():
    rng = random.Random(9)
    for N in (77, 143, 221):
        b = [2, 3, 5]
        for _ in range(200):
            vecs = [[rng.randrange(-20, 21) for _ in range(5)] for _ in range(4)]
            f = recover_factor(vecs, b, N)
            assert f is None or (1 < f < N and N % f == 0)
