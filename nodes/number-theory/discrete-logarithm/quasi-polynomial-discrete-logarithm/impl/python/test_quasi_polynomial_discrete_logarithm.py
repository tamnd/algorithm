# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quasi-polynomial-discrete-logarithm/. The authors are listed in prov/7RM8BX.jsonl.

import random

import pytest

from quasi_polynomial_discrete_logarithm import (
    QPField,
    coset_representatives,
    pdivmod,
    pgcd,
    pmul,
    ppowmod,
    psub,
    pscale,
    padd,
    qp_dlog,
    split_linear,
)

_FIELDS: dict[tuple[int, int], QPField] = {}


def field(q: int, k: int) -> QPField:
    if (q, k) not in _FIELDS:
        _FIELDS[(q, k)] = QPField(q, k, seed=q * 100 + k)
    return _FIELDS[(q, k)]


def powers(K: QPField, g: int) -> dict[int, int]:
    """Map the code of g^i to i for i in [0, ord g), by brute force."""
    gp = K.decode(g)
    table = {}
    y, i = (1,), 0
    while K.encode(y) not in table:
        table[K.encode(y)] = i
        y = K.mul(y, gp)
        i += 1
    return table


def element_of_order(K: QPField, r: int, rng: random.Random) -> int:
    """A random element of order exactly r, r | |K^*|."""
    n = K.size() - 1
    primes = [p for p in range(2, r + 1) if r % p == 0 and all(p % d for d in range(2, p))]
    while True:
        y = K.pow(K.decode(rng.randrange(1, n + 1)), n // r)
        if all(K.pow(y, r // p) != (1,) for p in primes):
            return K.encode(y)


def check(K: QPField, g: int, h: int, seed: int = 0) -> None:
    table = powers(K, g)
    assert qp_dlog(g, h, len(table), K, seed=seed) == table.get(h), (K.q, K.k, g, h)


def test_field_construction():
    for q, k in [(3, 2), (3, 3), (3, 5), (5, 2), (5, 4), (5, 7), (7, 3), (7, 9)]:
        K = field(q, k)
        F = K.F
        assert len(K.I) - 1 == k and K.I[-1] == 1
        big = psub(F, pmul(F, K.h1, (0,) * q + (1,)), K.h0)
        assert not pdivmod(F, big, K.I)[1]
        assert len(split_linear(F, K.h1)[2]) == 1
        # irreducible: X^(q^(2k)) = X mod I and gcd(X^(q^(2d)) - X, I) = 1 for d < k
        assert ppowmod(F, (0, 1), F.n**k, K.I) == (0, 1)
        for d in range(1, k):
            assert len(pgcd(F, K.I, psub(F, ppowmod(F, (0, 1), F.n**d, K.I), (0, 1)))) == 1


def test_coset_representatives_are_the_baer_sublines():
    for q in (3, 5, 7):
        K = field(q, 2)
        F = K.F
        reps = coset_representatives(F)
        assert len(reps) == q**3 + q
        keys = set()
        for a, b, c, d in reps:
            assert F.add[F.mul(a, d)][F.neg[F.mul(b, c)]] != 0
            pts = []
            for al in [None] + list(range(q)):
                u, v = (c, d) if al is None else (F.add[a][F.neg[F.mul(al, c)]], F.add[b][F.neg[F.mul(al, d)]])
                pts.append(-1 if u == 0 else F.mul(v, F.inv(u)))
            assert len(set(pts)) == q + 1
            keys.add(frozenset(pts))
        assert len(keys) == q**3 + q


def test_systematic_equation():
    rng = random.Random(5)
    for q, k in [(3, 4), (5, 3), (7, 2), (7, 9)]:
        K = field(q, k)
        F = K.F
        for a, b, c, d in rng.sample(coset_representatives(F), 20):
            y = (b, a) if a else (b,)  # a X + b, with a != 0 or b != 0
            z = (d, c) if c else (d,)
            left = pmul(F, K.h1, z)
            for al in range(q):
                left = pmul(F, left, psub(F, y, pscale(F, z, al)))
            rm = psub(F, pmul(F, padd(F, pscale(F, K.h0, F.frob[a]), pscale(F, K.h1, F.frob[b])), z),
                      pmul(F, y, padd(F, pscale(F, K.h0, F.frob[c]), pscale(F, K.h1, F.frob[d]))))
            assert pdivmod(F, left, K.I)[1] == pdivmod(F, rm, K.I)[1]


def test_worked_example():
    K = QPField(3, 3, h0=(1, 1))
    F = K.F
    assert K.I == (2, 2, 0, 1)  # X^3 - X - 1 over F_9
    g, h = K.encode((1, 1)), K.encode((1, 2, 2))  # X + 1 and 2X^2 + 2X + 1
    assert len(powers(K, g)) == 13
    assert K.encode(K.pow((1, 1), 11)) == h
    gamma = (3, 1)  # X + i
    z = K.mul((1, 2, 2), K.pow(gamma, 5))
    assert z == (3, 1, 1)  # X^2 + X + i, no root in F_9
    assert len(split_linear(F, z)[2]) == 3
    for seed in range(5):
        assert qp_dlog(g, h, 13, K, seed=seed) == 11


def test_trivial_targets():
    rng = random.Random(1)
    for q, k in [(3, 2), (3, 4), (5, 3), (7, 2)]:
        K = field(q, k)
        n = K.size() - 1
        for r in sorted({p for p in range(2, 200) if n % p == 0 and all(p % d for d in range(2, p))})[:2]:
            g = element_of_order(K, r, rng)
            assert qp_dlog(g, 1, r, K) == 0
            assert qp_dlog(g, g, r, K) == 1


def test_small_fields_exhaustive():
    rng = random.Random(2)
    for q, k in [(3, 2), (3, 3)]:
        K = field(q, k)
        g = element_of_order(K, K.size() - 1, rng)
        table = powers(K, g)
        hs = list(range(1, K.size()))
        for h in rng.sample(hs, 12) + [1, g]:
            assert qp_dlog(g, h, len(table), K, seed=h) == table[h]


def test_random_against_brute_force():
    rng = random.Random(3)
    sizes = [(3, 2), (3, 3), (3, 4), (3, 5), (5, 2), (5, 3), (7, 2), (7, 3)]
    for it in range(16):
        q, k = sizes[it % len(sizes)]
        K = field(q, k)
        n = K.size() - 1
        divs = [d for d in range(2, min(n, 3000) + 1) if n % d == 0]
        r = rng.choice(divs)
        g = element_of_order(K, r, rng)
        h = K.encode(K.pow(K.decode(g), rng.randrange(r)))
        check(K, g, h, seed=it)


def test_generators_and_non_generators():
    rng = random.Random(4)
    for q, k in [(3, 3), (3, 4), (5, 2)]:
        K = field(q, k)
        n = K.size() - 1
        g = element_of_order(K, n, rng)
        table = powers(K, g)
        for h in rng.sample(range(1, K.size()), 3):
            assert qp_dlog(g, h, n, K, seed=h) == table[h]
        g2 = K.encode(K.pow(K.decode(g), 2))  # order n / 2, not a generator
        h_out = g  # an odd power of g is outside <g^2>
        assert qp_dlog(g2, h_out, n // 2, K) is None
        assert qp_dlog(g2, K.encode(K.pow(K.decode(g), 6)), n // 2, K) == 3


def test_prime_and_composite_orders():
    rng = random.Random(6)
    K = field(3, 4)  # |K^*| = 6560 = 2^5 * 5 * 41
    for r in (2, 4, 5, 8, 10, 32, 41, 82, 205, 656):
        g = element_of_order(K, r, rng)
        for _ in range(2):
            h = K.encode(K.pow(K.decode(g), rng.randrange(r)))
            check(K, g, h)


def test_no_solution_is_reported():
    rng = random.Random(7)
    for q, k in [(3, 3), (3, 4), (5, 3), (7, 2)]:
        K = field(q, k)
        n = K.size() - 1
        r = next(d for d in range(2, n) if n % d == 0 and all(d % e for e in range(2, d)))
        g = element_of_order(K, n // r, rng)  # a subgroup of index r
        table = powers(K, g)
        outside = [h for h in rng.sample(range(1, K.size()), 40) if h not in table]
        assert outside
        for h in outside[:3]:
            assert qp_dlog(g, h, len(table), K) is None


def test_seed_independence():
    rng = random.Random(8)
    K = field(5, 3)
    n = K.size() - 1
    g = element_of_order(K, n, rng)
    h = K.encode(K.pow(K.decode(g), 9876))
    assert {qp_dlog(g, h, n, K, seed=s) for s in range(4)} == {9876}


def test_bad_input():
    K = field(3, 3)
    with pytest.raises(ValueError):
        qp_dlog(0, 1, 1, K)
    with pytest.raises(ValueError):
        qp_dlog(2, K.size(), 1, K)
    with pytest.raises(ValueError):
        qp_dlog(2, 1, 0, K)
    with pytest.raises(ValueError):
        QPField(3, 6)
    with pytest.raises(ValueError):
        QPField(4, 2)
    with pytest.raises(ValueError):
        QPField(3, 3, h0=(0, 1))  # X^3 - X splits over F_3
