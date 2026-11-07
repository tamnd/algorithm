# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berlekamp-factorization/. The authors are listed in prov/T0YM2W.jsonl.

import random

import pytest

from berlekamp_factorization import berlekamp_factorization as bf, berlekamp_matrix, left_null_space


# Independent oracle: plain mod-p list arithmetic and factorization by trial division.
# Independent oracle: plain mod-p list arithmetic and factorization by trial division.
def ref_trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def ref_mod(a, p):
    return ref_trim([x % p for x in a])


def ref_mul(a, b, p):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            out[i + j] += a[i] * b[j]
    return ref_mod(out, p)


def ref_divmod(a, b, p):
    """Long division by the nonzero b, coefficients modulo p."""
    a = ref_mod(a, p)
    inv = pow(b[-1], -1, p)
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b):
        c = a[-1] * inv % p
        s = len(a) - len(b)
        q[s] = c
        a = ref_mod([a[i] - (c * b[i - s] if i >= s else 0) for i in range(len(a))], p)
    return ref_trim(q), a


def ref_product(polys, p):
    out = [1]
    for g in polys:
        out = ref_mul(out, g, p)
    return out


def monic_polys(deg, p):
    """All monic polynomials of the given degree over Z/pZ."""
    for k in range(p ** deg):
        coeffs = []
        for _ in range(deg):
            coeffs.append(k % p)
            k //= p
        yield coeffs + [1]


def brute_factor(f, p):
    """Monic irreducible factors of a monic f, with repetition, by trial division in degree order."""
    f = ref_mod(f, p)
    out = []
    d = 1
    while 2 * d <= len(f) - 1:
        for g in monic_polys(d, p):
            while True:
                q, r = ref_divmod(f, g, p)
                if r:
                    break
                out.append(g)
                f = q
            if 2 * d > len(f) - 1:
                break
        d += 1
    if len(f) > 1:
        out.append(f)
    return sorted(out, key=lambda g: (len(g), g))


def is_square_free_brute(f, p):
    fs = brute_factor(f, p)
    return len(set(map(tuple, fs))) == len(fs)


def random_monic(rng, deg, p):
    return [rng.randrange(p) for _ in range(deg)] + [1]


def nonresidues(p, count, start=2):
    """The first count quadratic non-residues modulo the odd prime p, by Euler's criterion."""
    out, c = [], start
    while len(out) < count:
        if pow(c, (p - 1) // 2, p) == p - 1:
            out.append(c)
        c += 1
    return out


def big_prime_irreducibles(p):
    """Distinct monic irreducibles over Z/pZ for p = 998244353 (p = 1 mod 8): x - a and x^(2^j) - c, c a non-residue."""
    c = nonresidues(p, 4)
    return [[p - 5, 1], [p - 12345, 1], [p - c[0], 0, 1], [p - c[1], 0, 1], [p - c[2], 0, 0, 0, 1], [p - c[3]] + [0] * 7 + [1]]


def ref_powmod_x(e, f, p):
    # x^e mod f by repeated multiplication by x (e is small here)
    out = [1]
    for _ in range(e):
        out = ref_divmod([0] + out, f, p)[1]
    return out


def test_worked_example():
    p = 3
    f = [2, 1, 0, 1, 1]  # (x^2 + 1)(x^2 + x + 2)
    st = {}
    assert bf(f, p, stats=st) == [[1, 0, 1], [2, 1, 1]]
    assert st["q"] == [[1, 0, 0, 0], [0, 0, 0, 1], [1, 1, 2, 1], [0, 1, 0, 0]]
    assert st["basis"] == [[1], [0, 1, 0, 1]]
    assert st["r"] == 2
    assert bf(f, p, method="random") == [[1, 0, 1], [2, 1, 1]]


@pytest.mark.parametrize("p", [2, 3, 7])
def test_matrix_rows(p):
    rng = random.Random(p)
    for _ in range(20):
        f = random_monic(rng, rng.randint(1, 6), p)
        q = berlekamp_matrix(f, p)
        n = len(f) - 1
        for i in range(n):
            row = ref_powmod_x(p * i, f, p)
            assert q[i] == row + [0] * (n - len(row))


def test_null_space_small():
    # rows: v a = 0 for v in the span of (1, 0, 0) and (0, 1, 1) over F_5
    a = [[0, 0, 0], [1, 2, 3], [4, 3, 2]]
    basis = left_null_space(a, 5)
    assert basis == [[1, 0, 0], [0, 1, 1]]
    for v in basis:
        assert all(sum(v[i] * a[i][j] for i in range(3)) % 5 == 0 for j in range(3))


@pytest.mark.parametrize("p,maxdeg,count", [(2, 10, 150), (3, 8, 150), (7, 6, 100)])
def test_random_square_free_against_trial_division(p, maxdeg, count):
    rng = random.Random(500 + p)
    done = 0
    while done < count:
        f = random_monic(rng, rng.randint(1, maxdeg), p)
        if not is_square_free_brute(f, p):
            continue
        done += 1
        want = brute_factor(f, p)
        st = {}
        assert bf(f, p, stats=st) == want
        assert st["r"] == len(want)
        if p > 2:
            assert bf(f, p, method="random", rng=random.Random(done)) == want


@pytest.mark.parametrize("p", [2, 3, 7])
def test_products_of_irreducibles(p):
    rng = random.Random(11 * p)
    irr = {d: [g for g in monic_polys(d, p) if brute_factor(g, p) == [g]] for d in (1, 2, 3, 4)}
    for _ in range(25):
        qs = []
        for d in (1, 2, 3, 4):
            k = rng.randint(0, min(2, len(irr[d])))
            qs.extend(rng.sample(irr[d], k))
        if not qs:
            continue
        want = sorted(qs, key=lambda g: (len(g), g))
        assert bf(ref_product(qs, p), p) == want


def test_large_prime():
    p = 998244353
    irr = big_prime_irreducibles(p)
    rng = random.Random(9)
    for t in range(6):
        qs = rng.sample(irr, rng.randint(2, len(irr)))
        want = sorted(qs, key=lambda g: (len(g), g))
        assert bf(ref_product(qs, p), p, rng=random.Random(t)) == want
    # integer input with negative coefficients: x^2 - 1 = (x - 1)(x + 1)
    assert bf([-1, 0, 1], p) == [[1, 1], [p - 1, 1]]
    # both methods on a prime above SMALL_P: x^2 - 1 over F_101
    assert bf([100, 0, 1], 101, method="deterministic") == [[1, 1], [100, 1]]
    assert bf([100, 0, 1], 101) == [[1, 1], [100, 1]]


def test_edge_cases():
    for p in (2, 3, 7, 998244353):
        with pytest.raises(ValueError):
            bf([], p)
        with pytest.raises(ValueError):
            bf([0, 0], p)
        if p != 2:
            with pytest.raises(ValueError):
                bf([1, 2], p)  # not monic
        with pytest.raises(ValueError):
            bf([0, 0, 1], p)  # x^2 is not square-free
        assert bf([1], p) == []
        assert bf([1, 0, 0], p) == []  # leading zeros are stripped
        assert bf([0, 1], p) == [[0, 1]]
        assert bf([3 % p, 1, 0], p) == [[3 % p, 1]]
    with pytest.raises(ValueError):
        bf([1, 0, 0, 1], 3)  # x^3 + 1 = (x + 1)^3 over F_3
    assert bf([1, 1, 1], 2) == [[1, 1, 1]]  # irreducible over F_2
    assert bf([2, 0, 1], 3) == [[1, 1], [2, 1]]  # x^2 - 1 over F_3
