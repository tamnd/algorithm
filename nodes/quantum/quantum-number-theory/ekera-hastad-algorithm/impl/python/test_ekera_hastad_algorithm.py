# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ekera-hastad-algorithm/. The authors are listed in prov/86HVR8.jsonl.

import itertools
import math
import random
from fractions import Fraction

from ekera_hastad_algorithm import (
    brute_candidates,
    candidates,
    centered,
    circuit_distribution,
    closed_form_distribution,
    ekera_hastad,
    exact_distribution,
    factor_rsa,
    gram_schmidt,
    is_good,
    lll,
)
from qsim import sample

TOL = 1e-9

# (N, g, m, l): Z_N^* with g of order at least 2^(l+m) + 2^l (2^m - 1); every circuit has at most 11 qubits
SMALL = [(29, 2, 2, 2), (37, 2, 3, 1), (17, 3, 2, 1)]


def order(g, N):
    r, y = 1, g % N
    while y != 1:
        y, r = y * g % N, r + 1
    return r


def brute_short_log(g, x, N, m):
    y = 1
    for e in range(1 << m):
        if y == x % N:
            return e
        y = y * g % N
    return None


def primes_between(lo, hi):
    return [p for p in range(max(lo, 2), hi) if all(p % q for q in range(2, math.isqrt(p) + 1))]


def test_small_groups_meet_the_order_condition():
    for N, g, m, l in SMALL:
        assert order(g, N) >= (1 << (l + m)) + (1 << l) * ((1 << m) - 1)


def test_state_vector_matches_closed_form_and_exact_distribution():
    for N, g, m, l in SMALL:
        for d in range(1 << m):
            x = pow(g, d, N)
            sv = circuit_distribution(N, g, x, m, l)
            cf = closed_form_distribution(d, m, l)
            ex = exact_distribution(N, g, x, m, l)
            for key in set(sv) | set(cf) | set(ex):
                assert abs(sv.get(key, 0.0) - cf.get(key, 0.0)) < TOL
                assert abs(sv.get(key, 0.0) - ex.get(key, 0.0)) < TOL


def test_probability_depends_only_on_T_and_good_pairs_weigh_at_least_one_eighth():
    for N, g, m, l in SMALL:
        A = 1 << (l + m)
        for d in range(1 << m):
            sv = circuit_distribution(N, g, x := pow(g, d, N), m, l)
            by_T = {}
            for (j, k), p in sv.items():
                by_T.setdefault((d * j + (k << m)) % A, set()).add(round(p, 12))
            assert all(len(v) == 1 for v in by_T.values())
            good = sum(p for (j, k), p in sv.items() if is_good(d, m, l, j, k))
            assert good >= 1 / 8
            assert abs(sum(sv.values()) - 1) < TOL and x == pow(g, d, N)


def test_lll_is_reduced_and_keeps_the_lattice():
    rng = random.Random(3)
    for _ in range(30):
        n = rng.randrange(2, 5)
        B = [[rng.randrange(-40, 41) for _ in range(n)] for _ in range(n)]
        Bs0, _ = gram_schmidt(B)
        if any(all(c == 0 for c in b) for b in Bs0):
            continue  # not a basis
        R = lll(B)
        Bs, mu = gram_schmidt(R)
        vol0 = math.prod(sum(c * c for c in b) for b in Bs0)
        vol1 = math.prod(sum(c * c for c in b) for b in Bs)
        assert vol0 == vol1  # the squared determinant is unchanged
        for i in range(1, n):
            assert all(abs(mu[i][j]) <= Fraction(1, 2) for j in range(i))
            norm_i = sum(c * c for c in Bs[i])
            norm_prev = sum(c * c for c in Bs[i - 1])
            assert norm_i >= (Fraction(3, 4) - mu[i][i - 1] ** 2) * norm_prev
        # the first vector is within the LLL factor 2^((n-1)/2) of a brute-force shortest vector
        shortest = min(
            sum(sum(y[t] * B[t][c] for t in range(n)) ** 2 for c in range(n))
            for y in itertools.product(range(-6, 7), repeat=n)
            if any(y)
        )
        assert sum(c * c for c in R[0]) <= 2 ** (n - 1) * shortest


def test_lattice_candidates_match_brute_force_on_all_outcomes():
    # s = 1: every outcome of the (m, l) = (2, 2) circuit; s = 2: every pair of outcomes of (2, 1)
    for m, l, s in [(2, 2, 1), (2, 1, 2)]:
        outs = list(itertools.product(range(1 << (l + m)), range(1 << l)))
        for pairs in itertools.product(outs, repeat=s):
            assert candidates(list(pairs), m, l) == brute_candidates(list(pairs), m, l)


def test_lattice_candidates_match_brute_force_on_random_batches():
    rng = random.Random(1)
    for m, l, s in [(3, 1, 3), (4, 2, 2), (5, 2, 3)]:
        outs = list(itertools.product(range(1 << (l + m)), range(1 << l)))
        for _ in range(60):
            pairs = [rng.choice(outs) for _ in range(s)]
            assert candidates(pairs, m, l) == brute_candidates(pairs, m, l)


def test_good_batches_contain_d():
    for m, l, s in [(2, 2, 1), (3, 1, 3), (5, 2, 3)]:
        A, rng = 1 << (l + m), random.Random(9)
        outs = list(itertools.product(range(A), range(1 << l)))
        for d in range(1 << m):
            good = [(j, k) for j, k in outs if is_good(d, m, l, j, k)]
            for _ in range(10):
                pairs = [rng.choice(good) for _ in range(s)]
                assert d in candidates(pairs, m, l)


def test_ekera_hastad_matches_brute_force():
    rng = random.Random(2024)
    for N, g, m, l in SMALL:
        s = -(-m // l)
        for d in range(1 << m):
            x = pow(g, d, N)
            got, runs = ekera_hastad(N, g, x, m, s, rng)
            assert got == d == brute_short_log(g, x, N, m)
            assert runs <= 30 * s


def test_rsa_short_logarithm_and_the_value_of_m():
    # x = g^((N-1)/2) = g^d with d = (p + q - 2)/2 for every g, and 2^(n-1) <= d < 2^n, so m = n bits suffice
    for n in range(3, 11):
        ps = primes_between(2 ** (n - 1) + 1, 2**n)
        for p, q in itertools.combinations(ps, 2):
            d = (p + q - 2) // 2
            assert 2 ** (n - 1) <= d < 2**n
            if n <= 5:
                N = p * q
                for g in range(2, N - 1):
                    if math.gcd(g, N) == 1:
                        assert pow(g, (N - 1) // 2, N) == pow(g, d, N)
                c = d + 1
                assert {c - math.isqrt(c * c - N), c + math.isqrt(c * c - N)} == {p, q}


def test_factor_rsa():
    for N, n, s, seed in [(143, 4, 2, 1), (667, 5, 3, 5), (589, 5, 3, 6)]:
        got = factor_rsa(N, n, s, random.Random(seed))
        assert got is not None and got[0] * got[1] == N and 1 < got[0] < got[1]


def test_worked_example_667():
    N, g, m, l = 667, 2, 5, 2
    assert order(g, N) == 308 >= (1 << (l + m)) + (1 << l) * 25
    x = pow(g, (N - 1) // 2, N)
    assert x == 330 == pow(g, 25, N)
    pairs = [(101, 1), (105, 2), (62, 0)]
    assert [centered(25 * j + 32 * k, 128) for j, k in pairs] == [-3, 1, 14]
    assert candidates(pairs, m, l) == [2, 25]
    dist = exact_distribution(N, g, x, m, l)
    cf = closed_form_distribution(25, m, l)
    assert max(abs(dist[key] - cf[key]) for key in dist) < TOL
    assert abs(sum(p for (j, k), p in dist.items() if is_good(25, m, l, j, k)) - 0.3813) < 1e-4
    rng = random.Random(6)
    assert sorted(sample(dist, rng) for _ in range(3)) == sorted(pairs)
