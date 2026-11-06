# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ecpp/. The authors are listed in prov/5ZT65R.jsonl.

import math
import random
from collections import Counter
from decimal import Decimal, localcontext

import pytest

from ecpp import (
    LEAF,
    Composite,
    Step,
    cornacchia,
    curve_orders,
    discriminants,
    ec_add,
    ec_mul,
    ecpp,
    find_root,
    hilbert_class_polynomial,
    inverse,
    is_prime_below_leaf,
    is_probable_prime,
    large_enough,
    random_point,
    reduced_forms,
    split_order,
    sqrt_mod,
    twists,
    verify_certificate,
)

LIMIT = 10**5


def sieve(m: int) -> bytearray:
    is_p = bytearray([1]) * (m + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, math.isqrt(m) + 1):
        if is_p[i]:
            is_p[i * i :: i] = bytearray(len(range(i * i, m + 1, i)))
    return is_p


def is_prime_by_trial_division(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def check_proof(n: int, rng: random.Random, leaf: int = LEAF) -> list[Step]:
    chain = ecpp(n, rng, leaf)
    assert chain is not None
    assert verify_certificate(n, chain)
    numbers = [n] + [st.q for st in chain]
    assert all(a > b for a, b in zip(numbers, numbers[1:]))
    assert numbers[-1] < leaf
    return chain


def next_probable_prime(n: int) -> int:
    while not is_probable_prime(n):
        n += 1
    return n


def count_points(a: int, b: int, p: int) -> int:
    squares = [0] * p
    for y in range(p):
        squares[y * y % p] += 1
    return 1 + sum(squares[(x * x * x + a * x + b) % p] for x in range(p))


def test_all_small_n_against_trial_division() -> None:
    is_p = sieve(LIMIT)
    rng = random.Random(1)
    for n in range(LIMIT + 1):
        chain = ecpp(n, rng, leaf=50)
        assert (chain is not None) == bool(is_p[n]), n
        if chain is not None:
            assert verify_certificate(n, chain), n
    for n in range(0, LIMIT + 1, 7):
        assert (ecpp(n, rng) is not None) == bool(is_p[n])
    assert all(is_prime_below_leaf(n) == bool(is_p[n]) for n in range(LIMIT + 1))
    assert is_prime_by_trial_division(99991) and ecpp(99991, rng, leaf=50)


def test_special_inputs() -> None:
    rng = random.Random(2)
    for n in (-7, -1, 0, 1, 4, 6, 9, 49, 2**64, 2**200, 3 * (2**127 - 1)):
        assert ecpp(n, rng) is None
    for n in (2, 3, 5, 7, 37, 2**61 - 1, LEAF - 59):
        assert ecpp(n, rng) == []
        assert verify_certificate(n, [])
    for n in (101**20, (10**9 + 7) ** 3, (2**89 - 1) ** 2, (2**127 - 1) ** 3):
        assert ecpp(n, rng) is None
    with pytest.raises(ValueError):
        ecpp(101, rng, leaf=10)
    with pytest.raises(ValueError):
        ecpp(101, rng, leaf=LEAF + 1)


def test_composites_that_pass_the_base_2_test() -> None:
    rng = random.Random(3)
    carmichael = (561, 1105, 1729, 2465, 2821, 6601, 8911, 41041, 62745, 63973, 75361)
    strong_base_2 = (2047, 3277, 4033, 4681, 8321, 15841, 29341, 42799, 49141, 52633, 65281)
    for n in carmichael + strong_base_2 + (3825123056546413051, 318665857834031151167461):
        assert ecpp(n, rng, leaf=50) is None, n
    # Composite Mersenne and Fermat numbers are strong pseudoprimes to the
    # base 2, so they reach the curve steps.
    for n in (2**67 - 1, 2**71 - 1, 2**101 - 1, 2**64 + 1, 2**128 + 1, 2**256 + 1):
        assert pow(2, n - 1, n) == 1
        assert ecpp(n, rng) is None, n
    k = 10**59 + 3
    while True:
        p1, p2, p3 = 6 * k + 1, 12 * k + 1, 18 * k + 1
        if all(is_probable_prime(p) for p in (p1, p2, p3)):
            break
        k += 1
    big = p1 * p2 * p3
    assert pow(2, big - 1, big) == 1
    assert ecpp(big, rng) is None


def test_primes_with_proofs() -> None:
    rng = random.Random(4)
    for n in (10**20 + 39, 2**89 - 1, 2**127 - 1, 10**30 + 57, 10**100 + 267):
        check_proof(n, rng)
    check_proof(2**521 - 1, rng)
    check_proof(next_probable_prime(10**199), rng)
    for n in (1009, 100003, 999983, 10**12 + 39):
        check_proof(n, rng, leaf=50)


def test_large_composites_and_random_inputs() -> None:
    rng = random.Random(5)
    p = next_probable_prime(10**150 + rng.randrange(10**149))
    q = next_probable_prime(10**150 + rng.randrange(10**149))
    assert ecpp(p * q, rng) is None
    assert ecpp(p * p, rng) is None
    for _ in range(20):
        n = rng.randrange(10**299, 10**300) | 1
        assert (ecpp(n, rng) is not None) == is_probable_prime(n)
    for _ in range(40):
        n = rng.randrange(2**64, 2**130)
        chain = ecpp(n, rng)
        assert (chain is not None) == is_probable_prime(n)
        if chain is not None:
            assert verify_certificate(n, chain)


def test_hilbert_class_polynomials() -> None:
    assert hilbert_class_polynomial(-3) == [0, 1]
    assert hilbert_class_polynomial(-4) == [-1728, 1]
    assert hilbert_class_polynomial(-7) == [3375, 1]
    assert hilbert_class_polynomial(-8) == [-8000, 1]
    assert hilbert_class_polynomial(-11) == [32768, 1]
    assert hilbert_class_polynomial(-163) == [640320**3, 1]
    assert hilbert_class_polynomial(-15) == [-121287375, 191025, 1]
    assert hilbert_class_polynomial(-20) == [-681472000, -1264000, 1]
    assert hilbert_class_polynomial(-23) == [12771880859375, -5151296875, 3491750, 1]


def test_class_numbers_of_the_table() -> None:
    table = discriminants()
    h = Counter(len(reduced_forms(D)) for D in table)
    # The number of imaginary quadratic fields of class number 1 to 8
    # (Watkins 2004); all of them have |D| < 10000.
    assert [h[i] for i in range(1, 9)] == [9, 18, 16, 54, 25, 51, 31, 131]
    assert table[:9] == [-3, -4, -7, -8, -11, -19, -43, -67, -163]


def test_cm_orders_match_point_counts() -> None:
    rng = random.Random(6)
    for p in (1009, 1201, 2003, 2999):
        tried = 0
        for D in discriminants()[:80]:
            d = -D
            if d >= 4 * p or (D % p) == 0 or pow(D % p, (p - 1) // 2, p) != 1:
                continue
            sol = cornacchia(d, p)
            if sol is None:
                continue
            u, v = sol
            assert u * u + d * v * v == 4 * p
            j = find_root(hilbert_class_polynomial(D), p, rng)
            assert j is not None
            curves = twists(D, j, p)
            assert curves is not None
            counts = sorted(count_points(a, b, p) for a, b in curves)
            assert counts == sorted(curve_orders(d, p, u, v)), (p, D)
            tried += 1
        assert tried >= 3


def test_cornacchia_and_square_roots() -> None:
    primes = [p for p in range(5, 3000) if is_prime_by_trial_division(p)]
    for p in primes:
        for d in (3, 4, 7, 8, 15, 20, 23, 163):
            if d >= 4 * p or pow(-d % p, (p - 1) // 2, p) != 1:
                continue
            sol = cornacchia(d, p)
            exists = any(
                (4 * p - d * v * v) >= 0 and math.isqrt(4 * p - d * v * v) ** 2 == 4 * p - d * v * v
                for v in range(1, math.isqrt(4 * p // d) + 1)
            )
            assert (sol is not None) == exists, (p, d)
            if sol:
                assert sol[0] ** 2 + d * sol[1] ** 2 == 4 * p
        for a in range(1, 30):
            if pow(a, (p - 1) // 2, p) == 1:
                y = sqrt_mod(a, p)
                assert y is not None and y * y % p == a % p


def test_large_enough_is_exact() -> None:
    for t in range(2, 200):
        n = t**4
        assert not large_enough((t + 1) ** 2, n)
        assert large_enough((t + 1) ** 2 + 1, n)
    rng = random.Random(7)
    with localcontext() as ctx:
        ctx.prec = 80
        for _ in range(2000):
            n = rng.randrange(10, 10**40)
            bound = (Decimal(n).sqrt().sqrt() + 1) ** 2
            base = int(bound)
            for q in range(base - 3, base + 4):
                assert large_enough(q, n) == (Decimal(q) > bound), (q, n)


def test_worked_example() -> None:
    n = 100003
    assert n % 3 == 1
    assert cornacchia(3, n) == (632, 14)
    assert 632**2 + 3 * 14**2 == 4 * n
    assert curve_orders(3, n, 632, 14) == [100636, 99372, 100341, 99667, 100299, 99709]
    assert split_order(100636, n, set()) is None
    assert split_order(99372, n, set()) is None
    assert split_order(100341, n, set()) == (9, 11149)
    assert 352 < (n**0.25 + 1) ** 2 < 353
    curves = twists(-3, 0, n)
    assert curves == [(0, (-(2**e)) % n) for e in range(6)]
    assert [count_points(a, b, n) for a, b in curves] == [100636, 100341, 99709, 99372, 99667, 100299]
    x, y = 55125, 32871
    assert (y * y - x**3 + 2) % n == 0
    u_point = ec_mul(9, (x, y), 0, n)
    assert u_point == (31794, 59883)
    assert ec_mul(11149, u_point, 0, n) is None
    rng = random.Random(8)
    p = random_point(0, n - 1, n, rng)
    assert p is not None
    assert ec_mul(100636, p, 0, n) is None
    assert ec_mul(100341, p, 0, n) is not None
    # The second step and the leaf.
    m = 11149
    assert cornacchia(3, m) == (211, 5)
    assert split_order(11361, m, set()) == (21, 541)
    assert ec_mul(541, ec_mul(21, (5866, 10392), 0, m), 0, m) is None
    assert ec_mul(21, (5866, 10392), 0, m) == (6858, 3248)
    chain = [Step(n, 0, n - 2, x, y, 9, 11149), Step(m, 0, 1149, 5866, 10392, 21, 541)]
    assert verify_certificate(n, chain)
    assert ecpp(n, random.Random(0), leaf=1000) == chain


def test_verifier_rejects_bad_certificates() -> None:
    rng = random.Random(9)
    n = 10**30 + 57
    chain = check_proof(n, rng)
    st = chain[0]
    assert not verify_certificate(n + 2, chain)
    assert not verify_certificate(n, [st._replace(k=st.k + 1)] + chain[1:])
    assert not verify_certificate(n, [st._replace(y=st.y + 1)] + chain[1:])
    assert not verify_certificate(n, [st._replace(q=st.q + 2)] + chain[1:])
    # A point of small order with a tiny q: [m]P = O holds, but q is too small.
    small = Step(100003, 0, 100001, 55125, 32871, 100341 // 3, 3)
    assert not verify_certificate(100003, [small])
    # The leaf must be prime.
    fake = Step(100003, 0, 100001, 55125, 32871, 9, 11149)
    assert verify_certificate(100003, [fake])
    assert not verify_certificate(100003 * 3, [fake._replace(n=100003 * 3)])


def test_curve_arithmetic_finds_factors() -> None:
    p, q = 1000003, 1000033
    n = p * q
    with pytest.raises(Composite) as info:
        inverse(p * 5, n)
    assert info.value.args[0] == p
    # Two points whose x-coordinates agree modulo p only.
    x1 = 17
    x2 = x1 + p * 3
    with pytest.raises(Composite) as info:
        ec_add((x1, 5), (x2, 9), 1, n)
    assert info.value.args[0] == p
    a, b = 2, 3
    rng = random.Random(10)
    pt = None
    while pt is None:
        x = rng.randrange(n)
        rhs = (x**3 + a * x + b) % n
        yp = sqrt_mod(rhs % p, p)
        yq = sqrt_mod(rhs % q, q)
        if yp is not None and yq is not None and yp * yp % p == rhs % p and yq * yq % q == rhs % q:
            y = (yp * q * pow(q, -1, p) + yq * p * pow(p, -1, q)) % n
            pt = (x, y)
    order_p = count_points(a, b, p)
    with pytest.raises(Composite) as info:
        ec_mul(order_p, pt, a, n)
    assert info.value.args[0] in (p, q)
