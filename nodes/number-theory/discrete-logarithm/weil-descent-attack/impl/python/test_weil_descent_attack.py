# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weil-descent-attack/. The authors are listed in prov/83GQX3.jsonl.

import itertools
import random

import pytest

from weil_descent_attack import (
    Fq,
    Fq2,
    WeilCurve,
    _factor,
    bsgs,
    factor_base,
    gaudry_log,
    jac_add,
    jac_decompose,
    jac_mul,
    jac_neg,
    pdivmod,
    peval,
    pmul,
    psub,
    sqrt_mod,
    weil_descent_log,
)

ZERO = ([1], [])


def random_curve(rng: random.Random, primes) -> WeilCurve:
    while True:
        q = rng.choice(primes)
        try:
            return WeilCurve(q, rng.randrange(q), rng.randrange(q), (rng.randrange(q), rng.randrange(1, q)))
        except ValueError:
            pass


def all_points(W: WeilCurve) -> list:
    q, K = W.q, W.K
    out = [None]
    for u in range(q):
        for v in range(q):
            z = W.f((u, v))
            for a in range(q):
                for b in range(q):
                    if K.mul((a, b), (a, b)) == z:
                        out.append(((u, v), (a, b)))
    return out


def brute_log(W: WeilCurve, P, Q) -> int | None:
    R, k = None, 0
    while True:
        if R == Q:
            return k
        R, k = W.add(R, P), k + 1
        if R is None:
            return None


def reduced_divisors(W: WeilCurve) -> list:
    """Every reduced Mumford pair over F_q by brute force."""
    q, F, H = W.q, W.F, W.H
    out = [ZERO]
    for a0 in range(q):
        a = [a0, 1]
        for b0 in range(q):
            b = [b0] if b0 else []
            if not pdivmod(F, psub(F, H, pmul(F, b, b)), a)[1]:
                out.append((a, b))
    for a0, a1 in itertools.product(range(q), repeat=2):
        a = [a0, a1, 1]
        for b0, b1 in itertools.product(range(q), repeat=2):
            b = [b0, b1] if b1 else ([b0] if b0 else [])
            if not pdivmod(F, psub(F, H, pmul(F, b, b)), a)[1]:
                out.append((a, b))
    return out


def test_square_roots():
    for q in (3, 5, 7, 11, 13, 101, 307):
        for c in range(q):
            s = sqrt_mod(c, q)
            squares = {x * x % q for x in range(q)}
            assert (s is not None) == (c in squares)
            if s is not None:
                assert s * s % q == c
        if q in (3, 5, 7, 11):
            K = Fq2(q, next(c for c in range(2, q) if pow(c, (q - 1) // 2, q) == q - 1))
            sq = {K.mul((a, b), (a, b)) for a in range(q) for b in range(q)}
            for u in range(q):
                for v in range(q):
                    s = K.sqrt((u, v))
                    assert (s is not None) == ((u, v) in sq)
                    if s is not None:
                        assert K.mul(s, s) == (u, v)


def test_cantor_against_brute_force():
    rng = random.Random(1)
    for q in (3, 5, 7):
        for _ in range(3):
            W = random_curve(rng, [q])
            divs = reduced_divisors(W)
            assert len(divs) == W.order_j()
            keys = {(tuple(a), tuple(b)) for a, b in divs}
            for _ in range(60):
                A, B, C = rng.choice(divs), rng.choice(divs), rng.choice(divs)
                S = jac_add(W.F, W.H, A, B)
                assert (tuple(S[0]), tuple(S[1])) in keys
                assert S == jac_add(W.F, W.H, B, A)
                assert jac_add(W.F, W.H, S, C) == jac_add(W.F, W.H, A, jac_add(W.F, W.H, B, C))
                assert jac_add(W.F, W.H, A, jac_neg(W.F, A)) == ZERO
                assert jac_add(W.F, W.H, A, ZERO) == A
                assert jac_mul(W.F, W.H, len(divs), A) == ZERO


def test_group_orders_agree():
    rng = random.Random(2)
    for _ in range(25):
        W = random_curve(rng, [3, 5, 7, 11, 13, 17, 19, 23])
        ne = W.order_e()
        assert ne == W.order_j()
        if W.q <= 7:
            assert ne == len(all_points(W))
        for _ in range(5):
            assert W.smul(ne, W.random_point(rng)) is None


def test_cover_map_lands_on_e():
    rng = random.Random(3)
    for _ in range(20):
        W = random_curve(rng, [5, 7, 11, 13, 17])
        for u in range(W.q):
            if (W.T - 2 * u) % W.q == 0:
                continue
            Y = sqrt_mod(peval(W.F, W.H, u), W.q)
            if Y is not None:
                assert W.on_curve(W.phi((u, 0), (Y, 0)))


def test_psi_is_a_homomorphism():
    rng = random.Random(4)
    for _ in range(30):
        W = random_curve(rng, [5, 7, 11, 13, 17, 19, 23, 29])
        assert W.psi(None) == ZERO
        T2 = (W.beta, W.K.zero)
        assert W.on_curve(T2) and W.psi(T2) == ZERO
        for _ in range(10):
            A, B = W.random_point(rng), W.random_point(rng)
            assert W.psi(W.add(A, B)) == jac_add(W.F, W.H, W.psi(A), W.psi(B))
            assert W.psi(W.neg(A)) == jac_neg(W.F, W.psi(A))
            assert W.psi(W.add(A, T2)) == W.psi(A)


def test_worked_example():
    W = WeilCurve(7, 0, 1, (2, 1))
    assert W.K.nu == 3 and (W.T, W.N) == (4, 1)
    assert W.H == [2, 0, 2, 4, 3, 2]
    assert W.order_e() == W.order_j() == 52
    fb = factor_base(W)
    assert fb == {0: 3, 2: 0, 5: 2, 6: 1}
    P = ((0, 0), (3, 1))
    Q = ((0, 1), (0, 4))
    assert W.point_order(P, 52) == 13 and W.smul(6, P) == Q
    D1, D2 = W.psi(P), W.psi(Q)
    assert D1 == ([1, 2, 1], [3, 4]) and D2 == ([5, 6, 1], [3, 2])
    rows = {}
    for j in range(7):
        R = jac_add(W.F, W.H, jac_mul(W.F, W.H, j, D1), D2)
        rows[j] = jac_decompose(W, R, fb)
    assert rows == {0: {2: 1, 6: 1}, 1: {2: 1, 6: -1}, 2: {5: 2}, 3: None, 4: None, 5: {0: -2}, 6: {6: 2}}
    A = (0 - 1 - 6) % 13
    C = (1 - 1 - 1) % 13
    assert (A, C) == (6, 12) and (-A) * pow(C, -1, 13) % 13 == 6
    assert weil_descent_log(W, P, Q) == 6


def test_decompositions_are_relations():
    rng = random.Random(5)
    for _ in range(20):
        W = random_curve(rng, [5, 7, 11, 13, 17, 19, 23])
        fb = factor_base(W)
        for _ in range(20):
            D = W.psi(W.random_point(rng))
            e = jac_decompose(W, D, fb)
            if e is None:
                continue
            S = ZERO
            for u, c in e.items():
                Fu = ([(-u) % W.q, 1], [fb[u]] if fb[u] else [])
                S = jac_add(W.F, W.H, S, jac_mul(W.F, W.H, abs(c), Fu if c > 0 else jac_neg(W.F, Fu)))
            assert S == D


def test_gaudry_log_against_brute_force():
    rng = random.Random(6)
    done = 0
    while done < 25:
        W = random_curve(rng, [7, 11, 13, 17, 19, 23, 29, 31, 37])
        nj = W.order_j()
        for r, e in _factor(nj):
            if e != 1 or r == 2:
                continue
            P = W.smul(nj // r, W.random_point(rng))
            if P is None:
                continue
            k = rng.randrange(r)
            D1, D2 = W.psi(P), W.psi(W.smul(k, P))
            assert gaudry_log(W, D1, D2, r, nj, factor_base(W), rng) == k
            done += 1


def check(W: WeilCurve, P, Q, ne: int, nj: int, seed: int):
    assert weil_descent_log(W, P, Q, seed=seed, ne=ne, nj=nj) == brute_log(W, P, Q)


def test_random_against_brute_force():
    rng = random.Random(7)
    for it in range(40):
        W = random_curve(rng, [5, 7, 11, 13, 17, 19, 23, 29])
        ne, nj = W.order_e(), W.order_j()
        P = W.random_point(rng)
        n = W.point_order(P, ne)
        check(W, P, W.smul(rng.randrange(n), P), ne, nj, it)
        check(W, P, W.random_point(rng), ne, nj, it)


def test_trivial_targets():
    rng = random.Random(8)
    for it in range(15):
        W = random_curve(rng, [5, 7, 11, 13, 17, 19])
        ne, nj = W.order_e(), W.order_j()
        P = W.random_point(rng)
        n = W.point_order(P, ne)
        assert weil_descent_log(W, P, None, ne=ne, nj=nj) == 0
        assert weil_descent_log(W, P, P, ne=ne, nj=nj) == (1 % n)
        assert weil_descent_log(W, P, W.neg(P), ne=ne, nj=nj) == (n - 1) % n
        assert weil_descent_log(W, None, None, ne=ne, nj=nj) == 0
        assert weil_descent_log(W, None, P, ne=ne, nj=nj) is None


def test_generators_and_non_generators():
    # E(F_(q^2)) holds the full 2-torsion, so it is never cyclic; a point of
    # order #E/2 generates a cyclic subgroup of the largest possible order.
    rng = random.Random(9)
    gens = nongens = 0
    while gens < 10 or nongens < 10:
        W = random_curve(rng, [5, 7, 11, 13, 17, 19, 23])
        ne, nj = W.order_e(), W.order_j()
        assert len([P for P in [W.random_point(rng) for _ in range(4)] if W.point_order(P, ne) == ne]) == 0
        P = W.random_point(rng)
        if W.point_order(P, ne) == ne // 2:
            gens += 1
            for _ in range(3):
                check(W, P, W.random_point(rng), ne, nj, gens)
                check(W, P, W.smul(rng.randrange(ne), P), ne, nj, gens)
        else:
            nongens += 1
            for _ in range(3):
                check(W, P, W.random_point(rng), ne, nj, nongens)


def test_prime_and_composite_orders():
    rng = random.Random(10)
    prime = composite = 0
    while prime < 10 or composite < 10:
        W = random_curve(rng, [7, 11, 13, 17, 19, 23, 29, 31])
        ne, nj = W.order_e(), W.order_j()
        R = W.random_point(rng)
        r = max(p for p, _ in _factor(ne))
        if r > 2 and ne % (r * r) and prime < 10:
            P = W.smul(ne // r, R)
            if P is not None:
                prime += 1
                check(W, P, W.smul(rng.randrange(r), P), ne, nj, prime)
                check(W, P, W.random_point(rng), ne, nj, prime)
        n = W.point_order(R, ne)
        if len(_factor(n)) >= 2:
            composite += 1
            check(W, R, W.smul(rng.randrange(n), R), ne, nj, composite)


def test_no_solution_is_reported():
    rng = random.Random(11)
    seen = 0
    while seen < 20:
        W = random_curve(rng, [5, 7, 11, 13, 17, 19, 23])
        ne, nj = W.order_e(), W.order_j()
        P, Q = W.random_point(rng), W.random_point(rng)
        if brute_log(W, P, Q) is None:
            assert weil_descent_log(W, P, Q, ne=ne, nj=nj) is None
            seen += 1


def test_larger_fields():
    rng = random.Random(12)
    for q in (101, 211, 307):
        W = random_curve(rng, [q])
        ne, nj = W.order_e(), W.order_j()
        assert ne == nj
        P = W.random_point(rng)
        n = W.point_order(P, ne)
        k = rng.randrange(n)
        Q = W.smul(k, P)
        assert weil_descent_log(W, P, Q, seed=q, ne=ne, nj=nj) == k
        if q == 101:
            assert bsgs(W, P, Q, n) == k


def test_seed_independence():
    rng = random.Random(13)
    W = random_curve(rng, [23])
    ne, nj = W.order_e(), W.order_j()
    P = W.random_point(rng)
    Q = W.smul(rng.randrange(W.point_order(P, ne)), P)
    assert len({weil_descent_log(W, P, Q, seed=s, ne=ne, nj=nj) for s in range(6)}) == 1


def test_bad_input():
    with pytest.raises(ValueError):
        WeilCurve(9, 1, 1, (0, 1))
    with pytest.raises(ValueError):
        WeilCurve(7, 1, 1, (2, 0))
    with pytest.raises(ValueError):
        WeilCurve(7, 2, 1, (0, 1))
    W = WeilCurve(7, 0, 1, (2, 1))
    with pytest.raises(ValueError):
        weil_descent_log(W, ((0, 0), (0, 0)), None)
    assert Fq(7).inv(3) == 5
