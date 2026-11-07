# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harvey-van-der-hoeven-multiplication/. The authors are listed in prov/H0NKE4.jsonl.

import random
from math import prod

import pytest

from harvey_van_der_hoeven_multiplication import (
    Counts,
    Plan,
    crt_cell,
    expected_counts,
    hvdh_toy_multiply,
    is_prime,
    prime_dft,
    primitive_root,
)

SIZES = [(2,), (3,), (5,), (2, 3), (3, 5), (2, 5, 7), (3, 5, 7), (5, 7, 11), (2, 3, 5, 7)]


def test_is_prime_small():
    sieve = [True] * 2000
    sieve[0] = sieve[1] = False
    for i in range(2, 2000):
        if sieve[i]:
            for j in range(i * i, 2000, i):
                sieve[j] = False
    assert all(is_prime(n) == sieve[n] for n in range(2000))
    assert is_prime(998244353) and not is_prime(998244353 * 7)


def test_primitive_root():
    for p in (3, 5, 7, 11, 13, 1831):
        g = primitive_root(p)
        assert len({pow(g, k, p) for k in range(p - 1)}) == p - 1


@pytest.mark.parametrize("s", [2, 3, 5, 7, 11, 13])
def test_prime_dft_matches_definition(s):
    plan = Plan((s,), 6)
    q, root, g = plan.q, plan.roots[0], plan.gens[0]
    assert pow(root, s, q) == 1 and (s == 1 or pow(root, 1, q) != 1)
    rng = random.Random(s)
    for sign in (1, -1):
        w = pow(root, sign, q)
        for _ in range(10):
            x = [rng.randrange(q) for _ in range(s)]
            want = [sum(x[n] * pow(w, n * k, q) for n in range(s)) % q for k in range(s)]
            assert prime_dft(x, w, g, q, Counts()) == want


@pytest.mark.parametrize("sizes", SIZES)
def test_crt_map_is_a_bijection(sizes):
    plan = Plan(sizes, 4)
    assert sorted(crt_cell(j, plan) for j in range(plan.S)) == list(range(plan.S))


@pytest.mark.parametrize("sizes", SIZES)
def test_counts(sizes):
    plan = Plan(sizes, 4)
    counts = Counts()
    hvdh_toy_multiply(3, 5, plan, counts)
    dfts, convs = expected_counts(sizes)
    assert (counts.prime_dfts, counts.rader_convolutions, counts.pointwise_products) == (3 * dfts, 3 * convs, prod(sizes))


def test_example_from_the_page():
    plan = Plan((3, 5), 4)
    assert plan.q == 1831 and plan.chunks == 8
    counts = Counts()
    assert hvdh_toy_multiply(0xBEEF, 0xCAFE, plan, counts) == 0x97660722
    assert (counts.prime_dfts, counts.rader_convolutions, counts.pointwise_products) == (24, 24, 15)


def test_edge_cases():
    for sizes in SIZES:
        for b in (1, 3, 8):
            plan = Plan(sizes, b)
            n = b * plan.chunks
            top = (1 << n) - 1
            for u, v in [(0, 0), (0, top), (1, 1), (1, top), (top, top), (1 << (n - 1), top)]:
                assert hvdh_toy_multiply(u, v, plan) == u * v


def test_random_against_python_ints():
    rng = random.Random(2019)
    plans = [Plan(sizes, b) for sizes in SIZES[:7] for b in (1, 5, 8)]
    checked = 0
    for plan in plans:
        n = plan.b * plan.chunks
        for _ in range(25):
            u = rng.getrandbits(rng.randrange(1, n + 1))
            v = rng.getrandbits(rng.randrange(1, n + 1))
            assert hvdh_toy_multiply(u, v, plan) == u * v
            checked += 1
    assert checked >= 500


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        Plan((3, 3), 4)
    with pytest.raises(ValueError):
        Plan((4, 5), 4)
    plan = Plan((3, 5), 4)
    with pytest.raises(ValueError):
        hvdh_toy_multiply(1 << 32, 1, plan)
    with pytest.raises(ValueError):
        hvdh_toy_multiply(-1, 1, plan)
