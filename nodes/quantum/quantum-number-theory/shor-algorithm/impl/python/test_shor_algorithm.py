# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shor-algorithm/. The authors are listed in prov/MH2W70.jsonl.

import cmath
import functools
import math
import random
from fractions import Fraction

import pytest

from qsim import basis_state, probabilities, sample
from shor_algorithm import (
    continued_fraction,
    convergents,
    exponent_qubits,
    factor_from_order,
    find_order,
    integer_root,
    inverse_qft,
    order_candidates,
    order_finding_distribution,
    order_from_measurement,
    perfect_power_root,
    qft,
    quantum_order,
    shor_factor,
    work_qubits,
)

TOL = 1e-9


def order(a, N):
    """The multiplicative order by brute force."""
    r, x = 1, a % N
    while x != 1:
        x, r = x * a % N, r + 1
    return r


def prime_factors(N):
    """Trial division."""
    out, p = [], 2
    while p * p <= N:
        if N % p == 0:
            out.append(p)
            while N % p == 0:
                N //= p
        p += 1
    if N > 1:
        out.append(N)
    return out


def phi(N):
    out = N
    for p in prime_factors(N):
        out = out // p * (p - 1)
    return out


def closed_form(Q, r):
    """P(c) = (1/Q^2) sum_k |sum_{j < m_k} e^(2 pi i c r j / Q)|^2, with m_k = ceil((Q - k)/r)."""
    m, extra = divmod(Q, r)  # extra values of k have m + 1 terms, the other r - extra have m terms
    out = []
    for c in range(Q):
        num = c * r % Q
        if num == 0:
            g = lambda L: L * L
        else:
            th = 2 * math.pi * num / Q
            g = lambda L: (math.sin(L * th / 2) / math.sin(th / 2)) ** 2
        out.append(((r - extra) * g(m) + extra * g(m + 1)) / (Q * Q))
    return out


@functools.lru_cache(maxsize=None)
def closed_form_dist(Q, r):
    return tuple((c, p) for c, p in enumerate(closed_form(Q, r)) if p > 1e-15)


def closed_form_sampler(N, a, t, rng):
    """Sample the measurement from the exact closed form (the order comes from brute force)."""
    return sample(dict(closed_form_dist(1 << t, order(a, N))), rng)


def test_qft_matches_matrix():
    for t in range(1, 6):
        Q = 1 << t
        for x in range(Q):
            s = basis_state(t, x)
            qft(s, list(range(t)))
            for y in range(Q):
                assert abs(s[y] - cmath.exp(2j * math.pi * x * y / Q) / math.sqrt(Q)) < TOL
            inverse_qft(s, list(range(t)))
            assert abs(s[x] - 1) < TOL


@pytest.mark.parametrize("N,avals", [(15, [2, 4, 7, 8, 11, 13, 14]), (21, [2, 5, 20])])
def test_full_circuit_matches_closed_form(N, avals):
    t = exponent_qubits(N)
    for a in avals:
        D = order_finding_distribution(N, a, t)
        P = closed_form(1 << t, order(a, N))
        assert abs(sum(D.values()) - 1) < TOL
        assert max(abs(D.get(c, 0.0) - P[c]) for c in range(1 << t)) < TOL


def test_deferred_measurement_larger_N():
    # Measuring the work register first does not change the exponent distribution.
    # For the outcome a^k the exponent register holds the x < Q with x = k mod r.
    for N, a in [(33, 5), (35, 2), (39, 7), (51, 2)]:
        t, r = exponent_qubits(N), order(a, N)
        Q = 1 << t
        total = [0.0] * Q
        for k in range(r):
            xs = range(k, Q, r)
            s = [0j] * Q
            for x in xs:
                s[x] = 1 / math.sqrt(len(xs))
            inverse_qft(s, list(range(t)))
            for c, p in enumerate(probabilities(s)):
                total[c] += p * len(xs) / Q
        P = closed_form(Q, r)
        assert max(abs(u - v) for u, v in zip(total, P)) < TOL


def test_continued_fractions_exact():
    assert continued_fraction(0, 5) == [0]
    assert continued_fraction(192, 256) == [0, 1, 3]
    assert convergents(192, 256) == [(0, 1), (1, 1), (3, 4)]
    for p in range(0, 60):
        for q in range(1, 40):
            h, k = convergents(p, q)[-1]
            assert Fraction(h, k) == Fraction(p, q)


@pytest.mark.parametrize("N", [15, 21, 33, 35])
def test_continued_fraction_step_against_brute_force(N):
    t = exponent_qubits(N)
    Q = 1 << t
    for c in range(Q):
        x = Fraction(c, Q)
        cands = order_candidates(c, t, N)
        conv = {Fraction(h, k) for h, k in convergents(c, Q)}
        found = []
        for q in range(1, N):
            p = round(x * q)
            d = abs(x - Fraction(p, q))
            if d < Fraction(1, 2 * q * q):
                assert Fraction(p, q) in conv  # Legendre
            if d <= Fraction(1, 2 * Q):
                found.append(Fraction(p, q))
        # At most one fraction with denominator below N lies within 1/(2Q) <= 1/(2 N^2) of c/Q,
        # and the continued fraction step finds its denominator.
        assert len(set(found)) <= 1
        if found:
            assert found[0].denominator in cands


def one_run_success(N, a):
    t, r = exponent_qubits(N), order(a, N)
    P = closed_form(1 << t, r)
    return sum(p for c, p in enumerate(P) if order_from_measurement(c, t, N, a) == r), r, 1 << t


def test_one_run_success_bound():
    # P(one run gives r) >= phi(r) (4 / (pi^2 r)) (1 - pi r / (2Q))^2 for each odd N and each a.
    for N in range(15, 48, 2):
        for a in range(2, N - 1, 4):
            if math.gcd(a, N) != 1:
                continue
            s, r, Q = one_run_success(N, a)
            bound = phi(r) * 4 / (math.pi ** 2 * r) * (1 - math.pi * r / (2 * Q)) ** 2
            assert s >= bound - TOL
            assert s <= 1 + TOL


def test_find_order_on_simulator():
    rng = random.Random(2026)
    for N in (15, 21):
        for a in range(2, N):
            if math.gcd(a, N) == 1:
                r = order(a, N)
                assert find_order(N, a, rng, runs=6) == r
                for _ in range(5):
                    q = quantum_order(N, a, rng)
                    assert q % r == 0 and q < N


def test_quantum_order_rate_matches_exact_probability():
    # N = 21, a = 2: the exact one-pass probability of returning r = 6 is about 0.328.
    rng = random.Random(5)
    exact, r, _ = one_run_success(21, 2)
    hits = sum(quantum_order(21, 2, rng, max_passes=1) == r for _ in range(2000))
    assert abs(hits / 2000 - exact) < 0.04


def test_integer_root_and_perfect_powers():
    for N in range(0, 3000):
        for k in range(1, 6):
            b = integer_root(N, k)
            assert b ** k <= N < (b + 1) ** k
    assert perfect_power_root(64) == 2 and perfect_power_root(3 ** 40) == 3
    assert perfect_power_root(3 ** 40 + 2) is None
    for N in range(4, 2000):
        brute = [b for b in range(2, math.isqrt(N) + 1) if any(b ** k == N for k in range(2, N.bit_length() + 1))]
        assert perfect_power_root(N) == (min(brute) if brute else None)


def test_reduction_against_trial_division():
    # Every odd composite N < 2000 that is not a prime power: count the good bases.
    tight = []
    for N in range(15, 2000, 2):
        ps = prime_factors(N)
        if len(ps) < 2:
            continue
        lam = 1
        for p in ps:
            e = 0
            M = N
            while M % p == 0:
                M, e = M // p, e + 1
            lp = p ** (e - 1) * (p - 1)
            lam = lam * lp // math.gcd(lam, lp)
        lam_primes = prime_factors(lam)
        good = 0
        for a in range(1, N):
            if math.gcd(a, N) != 1:
                continue
            r = lam
            for p in lam_primes:
                while r % p == 0 and pow(a, r // p, N) == 1:
                    r //= p
            f = factor_from_order(N, a, r)
            y = pow(a, r // 2, N)
            assert f == (math.gcd(y - 1, N) if r % 2 == 0 and y != N - 1 else None)
            assert factor_from_order(N, a, lam) == f  # a multiple of r gives the same result
            if f is not None:
                assert 1 < f < N and N % f == 0
                good += 1
        k = len(ps)
        need = phi(N) * (1 - Fraction(1, 2 ** (k - 1)))
        assert good >= need
        if good == need:
            tight.append(N)
    assert 21 in tight and 15 not in tight


def test_factor_on_simulator():
    rng = random.Random(7)
    for N in (15, 21):
        for _ in range(5):
            f = shor_factor(N, rng)
            assert f is not None and 1 < f < N and N % f == 0


def test_factor_with_exact_sampler():
    rng = random.Random(11)
    for N in range(9, 130, 2):
        if len(prime_factors(N)) == 1 and perfect_power_root(N) is None:
            continue  # a prime
        f = shor_factor(N, rng, sampler=closed_form_sampler)
        assert f is not None and 1 < f < N and N % f == 0


def test_edges():
    rng = random.Random(1)
    assert shor_factor(4, rng) == 2
    assert shor_factor(27, rng) == 3
    assert shor_factor(125, rng) == 5
    assert perfect_power_root(15) is None
    with pytest.raises(ValueError):
        shor_factor(13, rng)
    with pytest.raises(ValueError):
        find_order(15, 5, rng)
    assert factor_from_order(15, 14, 2) is None  # a^(r/2) = -1
    assert factor_from_order(21, 2, 6) == 7  # 2^3 = 8, gcd(7, 21) = 7
    assert factor_from_order(21, 2, 12) == 7  # 2^6 = 1 would give gcd(0, 21) = 21
    assert factor_from_order(15, 7, 4) == 3 and factor_from_order(15, 7, 12) == 3
    with pytest.raises(ValueError):
        factor_from_order(15, 7, 6)
    assert work_qubits(15) == 4 and exponent_qubits(15) == 8 and exponent_qubits(21) == 9
