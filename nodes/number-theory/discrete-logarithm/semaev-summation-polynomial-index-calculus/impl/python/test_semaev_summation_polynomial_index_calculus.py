# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semaev-summation-polynomial-index-calculus/. The authors are listed in prov/WAPFC0.jsonl.

import random

import pytest

from semaev_summation_polynomial_index_calculus import (
    Curve,
    _factor,
    bsgs,
    decompose,
    factor_base,
    relation_log,
    roots_mod,
    s3,
    sqrt_mod,
    summation_index_calculus,
)

SMALL = [5, 7, 11, 13, 17, 19, 23]
MEDIUM = [29, 31, 37, 41, 43, 47, 53, 59]


def random_curve(rng: random.Random, primes: list[int]) -> Curve:
    while True:
        p = rng.choice(primes)
        try:
            return Curve(p, (rng.randrange(p), rng.randrange(p)), (rng.randrange(p), rng.randrange(p)))
        except ValueError:
            pass


def all_points(E: Curve) -> list:
    pts = [None]
    for u in range(E.p):
        for v in range(E.p):
            y = E.sqrt(E.rhs((u, v)))
            if y is not None:
                pts.append(((u, v), y))
                if y != (0, 0):
                    pts.append(E.neg(((u, v), y)))
    return pts


def brute(E: Curve, P, Q, n: int):
    T = None
    for x in range(n):
        if T == Q:
            return x
        T = E.add(T, P)
    return None


def test_square_roots_and_roots_of_polynomials():
    rng = random.Random(1)
    for p in SMALL + MEDIUM:
        for c in range(p):
            s = sqrt_mod(c, p)
            has = any(y * y % p == c for y in range(p))
            assert (s is not None) == has and (s is None or s * s % p == c)
        for _ in range(20):
            f = [rng.randrange(p) for _ in range(rng.randrange(2, 7))]
            if not any(f[1:]):
                continue
            assert roots_mod(f, p, rng) == [x for x in range(p) if sum(c * x**i for i, c in enumerate(f)) % p == 0]
    for p in [5, 7, 13]:
        E = Curve(p, (1, 0), (1, 1))
        for u in range(p):
            for v in range(p):
                y = E.sqrt((u, v))
                assert (y is None) != E.is_square((u, v)) or (u, v) == (0, 0)
                if y is not None:
                    assert E.mul(y, y) == (u, v)


def test_group_law_and_point_count():
    rng = random.Random(2)
    for _ in range(12):
        E = random_curve(rng, [5, 7, 11, 13])
        pts = all_points(E)
        N = E.order()
        assert N == len(pts)
        for _ in range(10):
            P, Q, R = (rng.choice(pts) for _ in range(3))
            S = E.add(E.add(P, Q), R)
            assert S == E.add(P, E.add(Q, R)) and E.on_curve(S)
            assert E.smul(N, P) is None
            assert E.smul(E.point_order(P, N), P) is None


def test_summation_polynomial_s3():
    rng = random.Random(3)
    for _ in range(8):
        E = random_curve(rng, [5, 7])
        pts = [P for P in all_points(E) if P is not None]
        for _ in range(6):
            P1, P2 = rng.choice(pts), rng.choice(pts)
            if P1[0] == P2[0]:
                continue
            want = {S[0] for S in (E.add(P1, P2), E.add(P1, E.neg(P2)))}
            got = {(u, v) for u in range(E.p) for v in range(E.p) if s3(E, P1[0], P2[0], (u, v)) == (0, 0)}
            assert got == want


def test_worked_example():
    E = Curve(7, (1, 2), (2, 1))
    assert E.nu == 3 and E.order() == 41
    fb = factor_base(E)
    assert fb == {
        0: ((0, 0), (2, 2)),
        3: ((3, 0), (2, 0)),
        4: ((4, 0), (3, 5)),
        5: ((5, 0), (1, 2)),
        6: ((6, 0), (1, 3)),
    }
    P = fb[0]
    Q = E.smul(23, P)
    assert Q == ((1, 5), (1, 3))
    rng = random.Random(0)
    rows = [decompose(E, E.add(E.smul(j, P), Q), fb, rng) for j in range(1, 5)]
    assert rows == [{4: 2}, {6: -1, 0: -1}, {6: -1}, {4: 1, 6: 1}]
    R4 = E.add(E.smul(4, P), Q)
    assert R4 == ((1, 2), (0, 1)) == E.add(fb[4], fb[6]) == E.add(fb[0], E.neg(fb[6]))
    # rho(s1) = 3 + 2 s1 + 4 s1^2 + s1^3 + 3 s1^4 has the roots 3 and 6
    assert roots_mod([3, 2, 4, 1, 3], 7, rng) == [3, 6]
    c = [20, 0, 1, 1]
    for x in fb:
        assert sum(cj * row.get(x, 0) for cj, row in zip(c, rows)) % 41 == 0
    A = sum(cj * j for cj, j in zip(c, range(1, 5))) % 41
    B = sum(c) % 41
    assert (A, B) == (27, 22) and (-A) * pow(B, -1, 41) % 41 == 23
    for seed in range(5):
        assert summation_index_calculus(E, P, Q, seed=seed) == 23


def test_decompositions_are_true_relations():
    rng = random.Random(4)
    for _ in range(10):
        E = random_curve(rng, SMALL + MEDIUM)
        fb = factor_base(E)
        hits = 0
        for _ in range(25):
            R = E.random_point(rng)
            e = decompose(E, R, fb, rng)
            if e is not None:
                hits += 1
                S = None
                for x, c in e.items():
                    assert c in (-2, -1, 1, 2)
                    S = E.add(S, E.smul(abs(c), fb[x] if c > 0 else E.neg(fb[x])))
                assert S == R and sum(abs(c) for c in e.values()) <= 2
        assert decompose(E, None, fb, rng) is None


def test_every_sum_of_two_factor_base_points_decomposes():
    rng = random.Random(5)
    for _ in range(5):
        E = random_curve(rng, [11, 13, 17])
        fb = factor_base(E)
        pts = [Px for Px in fb.values()] + [E.neg(Px) for Px in fb.values()]
        for P1 in pts:
            for P2 in pts:
                R = E.add(P1, P2)
                if R is not None:
                    assert decompose(E, R, fb, rng) is not None


def curve_with_large_prime(rng: random.Random, primes: list[int]):
    while True:
        E = random_curve(rng, primes)
        N = E.order()
        f = dict(_factor(N))
        r = max(f)
        if f[r] == 1 and r > 7:
            return E, N, r


def test_relation_step_against_brute_force():
    rng = random.Random(6)
    for it in range(25):
        E, N, r = curve_with_large_prime(rng, SMALL + MEDIUM)
        fb = factor_base(E)
        while True:
            P = E.smul(N // r, E.random_point(rng))
            if P is not None:
                break
        k = rng.randrange(r)
        Q = E.smul(k, P)
        assert relation_log(E, P, Q, r, fb, random.Random(it)) == k == brute(E, P, Q, r)


def test_larger_fields_up_to_about_10_to_the_5():
    rng = random.Random(13)
    for p in [101, 151, 211, 307]:
        E, N, r = curve_with_large_prime(rng, [p])
        P = E.smul(N // r, E.random_point(rng))
        k = rng.randrange(r)
        Q = E.smul(k, P)
        assert summation_index_calculus(E, P, Q, seed=p, N=N) == k == brute(E, P, Q, r)


def test_random_against_brute_force():
    rng = random.Random(7)
    for it in range(60):
        E = random_curve(rng, SMALL + MEDIUM)
        N = E.order()
        P = E.random_point(rng)
        n = E.point_order(P, N)
        k = rng.randrange(n)
        Q = E.smul(k, P)
        assert summation_index_calculus(E, P, Q, seed=it, N=N) == brute(E, P, Q, n) == k


def test_trivial_targets():
    rng = random.Random(8)
    for it in range(20):
        E = random_curve(rng, SMALL + MEDIUM)
        N = E.order()
        P = E.random_point(rng)
        assert summation_index_calculus(E, P, None, seed=it, N=N) == 0
        if E.point_order(P, N) > 1:
            assert summation_index_calculus(E, P, P, seed=it, N=N) == 1
    E = Curve(7, (1, 2), (2, 1))
    assert summation_index_calculus(E, None, None) == 0


def test_generators_and_non_generators():
    rng = random.Random(9)
    for it in range(20):
        E = random_curve(rng, SMALL + MEDIUM)
        N = E.order()
        pts = [E.random_point(rng) for _ in range(12)]
        G = max(pts, key=lambda T: E.point_order(T, N))
        n = E.point_order(G, N)
        for P in (G, E.smul(rng.randrange(2, 6), G)):
            m = E.point_order(P, N)
            k = rng.randrange(m)
            assert summation_index_calculus(E, P, E.smul(k, P), seed=it, N=N) == k
        if n == N:
            # a generator of a cyclic group: every point is a multiple
            T = E.random_point(rng)
            assert E.smul(summation_index_calculus(E, G, T, seed=it, N=N), G) == T


def test_prime_and_composite_orders():
    rng = random.Random(10)
    seen_square, seen_single, seen_prime = 0, 0, 0
    for it in range(40):
        E = random_curve(rng, SMALL + MEDIUM)
        N = E.order()
        P = E.random_point(rng)
        n = E.point_order(P, N)
        f = _factor(n)
        seen_prime += len(f) == 1 and f[0][1] == 1
        seen_square += any(N % (r * r) == 0 for r, _ in f)
        seen_single += any(N % (r * r) for r, _ in f)
        k = rng.randrange(n)
        assert summation_index_calculus(E, P, E.smul(k, P), seed=it, N=N) == k
    assert seen_square and seen_single and seen_prime
    # y^2 = x^3 + x over F_(p^2) with p = 3 mod 4 has the group (Z/(p+1))^2
    for p in [7, 11, 19]:
        E = Curve(p, (1, 0), (0, 0))
        N = E.order()
        assert N == (p + 1) ** 2
        for _ in range(4):
            P = E.random_point(rng)
            n = E.point_order(P, N)
            k = rng.randrange(n)
            assert summation_index_calculus(E, P, E.smul(k, P), seed=p, N=N) == k


def test_no_solution_is_reported():
    rng = random.Random(11)
    count = 0
    for it in range(40):
        E = random_curve(rng, SMALL + MEDIUM)
        N = E.order()
        P, Q = E.random_point(rng), E.random_point(rng)
        n = E.point_order(P, N)
        want = brute(E, P, Q, n)
        assert summation_index_calculus(E, P, Q, seed=it, N=N) == want
        count += want is None
    assert count > 10
    # targets of the right order outside <P> in a non-cyclic group
    for p in [7, 11]:
        E = Curve(p, (1, 0), (0, 0))
        N = E.order()
        found = 0
        for _ in range(30):
            P, Q = E.random_point(rng), E.random_point(rng)
            n = E.point_order(P, N)
            if E.smul(n, Q) is None and brute(E, P, Q, n) is None:
                assert summation_index_calculus(E, P, Q, seed=p, N=N) is None
                found += 1
        assert found


def test_seed_independence():
    rng = random.Random(12)
    E, N, r = curve_with_large_prime(rng, MEDIUM)
    P = E.smul(N // r, E.random_point(rng))
    k = rng.randrange(r)
    Q = E.smul(k, P)
    assert {summation_index_calculus(E, P, Q, seed=s, N=N) for s in range(6)} == {k}
    assert bsgs(E, P, Q, r) == k


def test_bad_input():
    with pytest.raises(ValueError):
        Curve(3, (1, 0), (1, 0))
    with pytest.raises(ValueError):
        Curve(9, (1, 0), (1, 0))
    with pytest.raises(ValueError):
        Curve(7, (0, 0), (0, 0))
    E = Curve(7, (1, 2), (2, 1))
    with pytest.raises(ValueError):
        summation_index_calculus(E, ((0, 0), (1, 0)), None)
