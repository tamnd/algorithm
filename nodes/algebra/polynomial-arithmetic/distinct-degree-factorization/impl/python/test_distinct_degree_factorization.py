# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distinct-degree-factorization/. The authors are listed in prov/9GANAE.jsonl.

import random

import pytest

from distinct_degree_factorization import distinct_degree_factorization as ddf


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


def expected_groups(f, p):
    groups = {}
    for g in brute_factor(f, p):
        groups.setdefault(len(g) - 1, []).append(g)
    return [(ref_product(gs, p), d) for d, gs in sorted(groups.items())]


def test_worked_example():
    p = 3
    f = ref_product([[1, 1], [1, 0, 1], [1, 2, 0, 1], [2, 2, 0, 1]], p)
    log = []
    assert ddf(f, p, log) == [([1, 1], 1), ([1, 0, 1], 2), ([2, 0, 1, 0, 1, 0, 1], 3)]
    assert log[0] == (1, [0, 0, 0, 1], [1, 1])
    assert log[1] == (2, [0, 1, 0, 0, 0, 1, 0, 1], [1, 0, 1])
    assert log[2] == (3, [0, 1], [2, 0, 1, 0, 1, 0, 1])


@pytest.mark.parametrize("p,maxdeg", [(2, 10), (3, 8), (7, 6)])
def test_random_square_free_against_trial_division(p, maxdeg):
    rng = random.Random(p)
    done = 0
    while done < 60:
        f = random_monic(rng, rng.randint(0, maxdeg), p)
        if not is_square_free_brute(f, p):
            continue
        assert ddf(f, p) == expected_groups(f, p)
        done += 1


def test_products_of_chosen_irreducibles_mod_2():
    p = 2
    irr = [[0, 1], [1, 1], [1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1], [1, 1, 0, 0, 1], [1, 0, 1, 0, 0, 1]]
    rng = random.Random(22)
    for _ in range(40):
        pick = [g for g in irr if rng.random() < 0.5]
        f = ref_product(pick, p)
        assert ddf(f, p) == expected_groups(f, p)


def test_large_prime():
    p = 998244353
    irr = big_prime_irreducibles(p)
    rng = random.Random(5)
    for _ in range(6):
        pick = [g for g in irr if rng.random() < 0.6] or [irr[0]]
        f = ref_product(pick, p)
        groups = {}
        for g in pick:
            groups.setdefault(len(g) - 1, []).append(g)
        want = [(ref_product(gs, p), d) for d, gs in sorted(groups.items())]
        assert ddf(f, p) == want


def test_edge_cases():
    assert ddf([1], 5) == []
    assert ddf([3, 1], 5) == [([3, 1], 1)]
    # an irreducible quintic over Z/2Z leaves the loop early, after i = 2
    log = []
    assert ddf([1, 0, 1, 0, 0, 1], 2, log) == [([1, 0, 1, 0, 0, 1], 5)]
    assert [e[0] for e in log] == [1, 2]
    # leading zero coefficients and unreduced coefficients are accepted
    assert ddf([-1, 0, 1, 0, 0], 7) == [([6, 0, 1], 1)]
    # many linear factors: x^7 - x over Z/7Z
    assert ddf([0, 6, 0, 0, 0, 0, 0, 1], 7) == [([0, 6, 0, 0, 0, 0, 0, 1], 1)]
    with pytest.raises(ValueError):
        ddf([1, 2], 5)
    with pytest.raises(ValueError):
        ddf([], 5)
