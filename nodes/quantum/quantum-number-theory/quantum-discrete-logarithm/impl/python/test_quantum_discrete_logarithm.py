# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-discrete-logarithm/. The authors are listed in prov/KD2HD3.jsonl.

import itertools
import math
import random

from qsim import apply_register_unitary, basis_state, circuit_matrix, fourier_matrix, is_unitary, padded, registers
from quantum_discrete_logarithm import (
    centered,
    closed_form_distribution,
    merge,
    outcome_distribution,
    quantum_dlog,
    shor_amplitude_formula,
    shor_candidate,
    shor_circuit_distribution,
    shor_is_good,
    shor_q,
    solve_congruence,
)

TOL = 1e-9

# (p, g, r): g has order r in Z_p^*
GROUPS = [(7, 3, 6), (11, 4, 5), (13, 2, 12), (13, 3, 3), (11, 2, 10)]


def order(g, p):
    r, y = 1, g % p
    while y != 1:
        y, r = y * g % p, r + 1
    return r


def brute_dlog(g, h, p):
    y = 1
    for x in range(p):
        if y == h % p:
            return x
        y = y * g % p
    return None


def bsgs(g, h, p, r):
    """Baby-step giant-step, the classical reference method."""
    m = math.isqrt(r - 1) + 1
    table = {}
    y = 1
    for j in range(m):
        table.setdefault(y, j)
        y = y * g % p
    step = pow(g, (-m) % r, p)
    y = h % p
    for i in range(m + 1):
        if y in table:
            return (i * m + table[y]) % r
        y = y * step % p
    return None


def test_groups_are_right():
    for p, g, r in GROUPS:
        assert order(g, p) == r


def test_padded_fourier_is_unitary():
    for N, d in [(3, 4), (5, 8), (6, 8), (12, 16), (16, 16)]:
        assert is_unitary(fourier_matrix(N))
        assert is_unitary(padded(fourier_matrix(N), d))


def test_register_unitary_matches_matrix():
    # the Fourier matrix of Z_3 on the middle register of a 5-qubit state, checked column by column
    ra, rb, rc = registers(1, 2, 2)
    U = padded(fourier_matrix(3), 4)
    M = circuit_matrix(5, lambda s: apply_register_unitary(s, U, rb))
    for x in range(32):
        a, b, c = x & 1, (x >> 1) & 3, x >> 3
        for b2 in range(4):
            y = a | (b2 << 1) | (c << 3)
            assert abs(M[y][x] - U[b2][b]) < TOL


def test_distribution_matches_closed_form():
    for p, g, r in GROUPS:
        for x in range(r):
            h = pow(g, x, p)
            got = outcome_distribution(p, g, h, r)
            want = closed_form_distribution(r, x)
            for key in set(got) | set(want):
                assert abs(got.get(key, 0.0) - want.get(key, 0.0)) < TOL


def test_childs_example_z7():
    # log_3 2 = 2 in Z_7^*: the outcomes are (c, -2c mod 6), each with probability 1/6
    got = outcome_distribution(7, 3, 2, 6)
    assert sorted(k for k, v in got.items() if v > TOL) == [(0, 0), (1, 4), (2, 2), (3, 0), (4, 4), (5, 2)]


def test_post_processing_against_brute_force():
    # every outcome (c, d) of every r up to 30: the solution set of c x = -d (mod r)
    for r in range(1, 31):
        for c in range(r):
            for d in range(r):
                want = {x for x in range(r) if (c * x + d) % r == 0}
                sol = solve_congruence(c, d, r)
                if not want:
                    assert sol is None
                    continue
                x0, m = sol
                assert {x for x in range(r) if x % m == x0} == want


def test_merge_against_brute_force():
    for m1, m2 in itertools.product(range(1, 13), repeat=2):
        for x1 in range(m1):
            for x2 in range(m2):
                l = m1 * m2 // math.gcd(m1, m2)
                want = [x for x in range(l) if x % m1 == x1 and x % m2 == x2]
                got = merge(x1, m1, x2, m2)
                if not want:
                    assert got is None
                else:
                    assert got == (want[0], l)


def test_quantum_dlog_matches_brute_force_and_bsgs():
    rng = random.Random(2024)
    for p, g, r in GROUPS:
        for x in range(r):
            h = pow(g, x, p)
            got, runs = quantum_dlog(p, g, h, r, rng)
            assert got == x == brute_dlog(g, h, p) == bsgs(g, h, p, r)
            assert runs <= 20


def test_success_after_t_runs():
    # Pr[t runs fix x] = prod over primes s | r of (1 - s^-t); the expected number of runs is below 2.775
    for r in [2, 6, 12, 30]:
        primes = [s for s in range(2, r + 1) if r % s == 0 and all(s % u for u in range(2, s))]
        for t in [1, 2, 3]:
            ok = 0
            for cs in itertools.product(range(r), repeat=t):
                if math.gcd(math.gcd(*cs) if t > 1 else cs[0], r) == 1:
                    ok += 1
            assert abs(ok / r**t - math.prod(1 - s ** (-t) for s in primes)) < TOL
        expected = sum(1 - math.prod(1 - s ** (-t) for s in primes) for t in range(0, 200))
        assert expected < 2.775


def test_shor_form_matches_formula_and_bounds():
    for p, g in [(5, 2), (7, 3), (11, 2)]:
        r, q = p - 1, shor_q(p)
        assert p < q < 2 * p
        for x in range(r):
            h = pow(g, x, p)
            dist = shor_circuit_distribution(p, g, h)
            good = 0.0
            for c in range(q):
                for d in range(q):
                    for k in range(r):
                        y = pow(g, k, p)
                        pr = dist.get((c, d, y), 0.0)
                        assert abs(pr - abs(shor_amplitude_formula(p, x, c, d, k)) ** 2) < TOL
                        if shor_is_good(p, x, c, d):
                            assert pr >= 1 / (20 * q * q)
                            good += pr
            assert good >= 1 / 480


def test_shor_candidate_is_right_on_good_pairs():
    for p, g in [(5, 2), (7, 3), (11, 2), (13, 2), (17, 3), (19, 2)]:
        r, q = p - 1, shor_q(p)
        for x in range(r):
            for c in range(q):
                for d in range(q):
                    if shor_is_good(p, x, c, d):
                        cand = shor_candidate(p, c, d)
                        if cand is not None:
                            assert cand == x
            assert centered(q // 2, q) == q // 2 and centered(q // 2 + 1, q) == -(q // 2) + 1
