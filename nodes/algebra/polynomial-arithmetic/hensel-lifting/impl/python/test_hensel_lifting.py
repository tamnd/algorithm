# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hensel-lifting/. The authors are listed in prov/ZKSCMK.jsonl.

import itertools
import random

import pytest

from hensel_lifting import (
    cofactors_mod_p,
    hensel_lift,
    hensel_step,
    lift_factors,
    lift_root,
    symmetric,
)

PRIMES = [2, 3, 7, 998244353]


# Independent oracle: plain integer polynomial arithmetic written separately.
def ref_trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def ref_mul(a, b):
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            out[i + j] += a[i] * b[j]
    return ref_trim(out)


def ref_mod(a, m):
    return ref_trim([c % m for c in a])


def ref_rem_monic(a, h, m):
    """Remainder of a by the monic h, modulo m, by repeated subtraction of shifts."""
    r = ref_mod(a, m)
    e = len(h) - 1
    while len(r) > e:
        c = r[-1]
        shift = len(r) - 1 - e
        r = ref_mod([r[i] - (c * h[i - shift] if 0 <= i - shift <= e else 0) for i in range(len(r))], m)
    return r


def congruent(a, b, m):
    n = max(len(a), len(b))
    a = list(a) + [0] * (n - len(a))
    b = list(b) + [0] * (n - len(b))
    return all((x - y) % m == 0 for x, y in zip(a, b))


def gcd_is_one_mod_p(a, b, p):
    a, b = ref_mod(a, p), ref_mod(b, p)
    while b:
        inv = pow(b[-1], -1, p)
        while len(a) >= len(b):
            c = a[-1] * inv % p
            s = len(a) - len(b)
            a = ref_mod([a[i] - (c * b[i - s] if i >= s else 0) for i in range(len(a))], p)
        a, b = b, a
    return len(a) == 1


def random_monic(rng, deg, bound):
    return [rng.randint(-bound, bound) for _ in range(deg)] + [1]


def check_lift(f, g0, h0, p, k):
    g, h = hensel_lift(f, g0, h0, p, k)
    pk = p ** k
    assert congruent(f, ref_mul(g, h), pk)
    assert congruent(g, g0, p) and congruent(h, h0, p)
    assert h and h[-1] == 1 and len(h) == len(ref_mod(h0, p))
    assert all(0 <= c < pk for c in g + h)
    return g, h


def test_worked_example():
    f = [-1, 0, 0, 0, 1]
    g0, h0 = [-2, -1, 2, 1], [-2, 1]
    steps = []
    g, h = hensel_lift(f, g0, h0, 5, 4, steps)
    assert cofactors_mod_p(g0, h0, 5) == ([3], [4, 3, 2])
    assert [m for m, _, _ in steps] == [25, 625]
    assert symmetric(steps[0][2], 25) == [-7, 1]
    assert symmetric(steps[0][1], 25) == [-7, -1, 7, 1]
    assert symmetric(h, 625) == [-182, 1]
    assert symmetric(g, 625) == [-182, -1, 182, 1]
    assert (182 * 182 + 1) % 625 == 0


@pytest.mark.parametrize("p", PRIMES)
def test_recovers_true_factors(p):
    rng = random.Random(1000 + p % 1000)
    done = 0
    while done < 25:
        a = random_monic(rng, rng.randint(0, 4), 9)
        b = random_monic(rng, rng.randint(1, 4), 9)
        lc = rng.choice([1, -1, 2, 3, 5, 7, 11])
        if lc % p == 0 or not gcd_is_one_mod_p(a, b, p):
            continue
        f = ref_mul([lc], ref_mul(a, b))
        bound = 2 * max(abs(c) for c in b) + 1
        k = 1
        while p ** k <= bound:
            k += 1
        k += rng.randint(0, 2)
        g, h = check_lift(f, ref_mul([lc], a), b, p, k)
        assert symmetric(h, p ** k) == b
        assert congruent(g, ref_mul([lc], a), p ** k)
        done += 1


@pytest.mark.parametrize("p", [2, 3, 7, 998244353])
def test_random_factorizations_mod_p(p):
    """f is only known to factor modulo p; check the lifted congruence."""
    rng = random.Random(7 * (p % 10007))
    done = 0
    while done < 40:
        g0 = [rng.randrange(p) for _ in range(rng.randint(1, 5))]
        h0 = [rng.randrange(p) for _ in range(rng.randint(0, 4))] + [1]
        g0 = ref_mod(g0, p)
        if not g0 or not gcd_is_one_mod_p(g0, h0, p):
            continue
        noise = [p * rng.randint(-50, 50) for _ in range(len(g0) + len(h0) - 2)]
        f = ref_trim([x + (noise[i] if i < len(noise) else 0) for i, x in enumerate(ref_mul(g0, h0))])
        if not f or f[-1] % p == 0:
            continue
        k = rng.randint(1, 6) if p < 100 else rng.randint(1, 3)
        check_lift(f, g0, h0, p, k)
        done += 1


@pytest.mark.parametrize("p,k", [(2, 3), (3, 2), (3, 3), (7, 2)])
def test_uniqueness_by_brute_force(p, k):
    rng = random.Random(p * 100 + k)
    pk = p ** k
    done = 0
    while done < 8:
        a = random_monic(rng, rng.randint(1, 3), 5)
        b = random_monic(rng, rng.randint(1, 2), 5)
        if not gcd_is_one_mod_p(a, b, p):
            continue
        f = ref_mul(a, b)
        g, h = hensel_lift(f, a, b, p, k)
        e = len(b) - 1
        found = []
        base = [c % p for c in b[:e]]
        for lifts in itertools.product(range(p ** (k - 1)), repeat=e):
            cand = [base[i] + p * lifts[i] for i in range(e)] + [1]
            if not ref_rem_monic(f, cand, pk):
                found.append(ref_mod(cand, pk))
        assert found == [h]
        done += 1


def test_composite_modulus_step():
    """The Hensel step is valid for any modulus, here m = 6 and then m = 36."""
    rng = random.Random(6)
    done = 0
    while done < 30:
        a = random_monic(rng, rng.randint(1, 3), 9)
        b = random_monic(rng, rng.randint(1, 3), 9)
        if not (gcd_is_one_mod_p(a, b, 2) and gcd_is_one_mod_p(a, b, 3)):
            continue
        s2, t2 = cofactors_mod_p(a, b, 2)
        s3, t3 = cofactors_mod_p(a, b, 3)

        def crt(x, y):
            n = max(len(x), len(y))
            x = x + [0] * (n - len(x))
            y = y + [0] * (n - len(y))
            return [(3 * u + 4 * v) % 6 for u, v in zip(x, y)]

        s, t = crt(s2, s3), crt(t2, t3)
        f = [c + 6 * rng.randint(-20, 20) for c in ref_mul(a, b)]
        f[-1] = 1
        g, h, m = ref_mod(a, 6), ref_mod(b, 6), 6
        for _ in range(2):
            g, h, s, t = hensel_step(f, g, h, s, t, m)
            m = m * m
            assert congruent(f, ref_mul(g, h), m)
            assert congruent(ref_trim([x + y for x, y in itertools.zip_longest(ref_mul(s, g), ref_mul(t, h), fillvalue=0)]), [1], m)
            assert h[-1] == 1 and len(h) == len(b)
            assert len(s) < len(h) and len(t) < len(g)
        done += 1


def test_edge_cases():
    # leading zero coefficients in the input are stripped
    g, h = hensel_lift([-1, 0, 0, 0, 1, 0, 0], [-2, -1, 2, 1, 0], [-2, 1, 0], 5, 2)
    assert symmetric(h, 25) == [-7, 1]
    # constant cofactor g: f = 3 (x^2 + x + 1), p = 2
    g, h = hensel_lift([3, 3, 3], [1], [1, 1, 1], 2, 5)
    assert g == [3] and h == [1, 1, 1]
    # monic h of degree 0: everything goes to g
    g, h = hensel_lift([4, 1, 9], [4, 1, 2], [1], 7, 3)
    assert h == [1] and g == [4, 1, 9]
    # k = 1 returns the input reduced modulo p
    assert hensel_lift([-1, 0, 1], [-1, 1], [1, 1], 3, 1) == ([2, 1], [1, 1])
    # a constant f with h = 1
    assert hensel_lift([5], [5], [1], 3, 2) == ([5], [1])


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        hensel_lift([0, 0, 1], [0, 1], [0, 1], 5, 3)  # x and x are not coprime
    with pytest.raises(ValueError):
        hensel_lift([1, 0, 2], [1, 0, 2], [0, 2], 5, 3)  # h not monic
    with pytest.raises(ValueError):
        hensel_lift([1, 0, 1], [1, 1], [1, 1], 5, 3)  # f is not g h mod p
    with pytest.raises(ValueError):
        lift_root([-7, 0, 1], 0, 7, 2)  # not a simple root


@pytest.mark.parametrize("p", [3, 7, 998244353])
def test_lift_root_square_roots(p):
    rng = random.Random(p % 991)
    k = 6 if p < 100 else 2
    pk = p ** k
    for _ in range(30):
        c = rng.randrange(1, p)
        if pow(c, (p - 1) // 2, p) != 1:
            continue
        r = next(x for x in range(p) if x * x % p == c) if p < 100 else _sqrt_big(c, p)
        b = lift_root([-c, 0, 1], r, p, k)
        assert (b * b - c) % pk == 0 and b % p == r


def _sqrt_big(c, p):
    # p = 998244353 = 119 * 2^23 + 1; Tonelli-Shanks
    q, s = p - 1, 0
    while q % 2 == 0:
        q, s = q // 2, s + 1
    z = 3
    m, cc, t, r = s, pow(z, q, p), pow(c, q, p), pow(c, (q + 1) // 2, p)
    while t != 1:
        i, tt = 0, t
        while tt != 1:
            tt, i = tt * tt % p, i + 1
        b = pow(cc, 1 << (m - i - 1), p)
        m, cc, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


def test_lift_root_matches_factor_lift():
    assert lift_root([-2, 0, 1], 3, 7, 4) == 2166
    g, h = hensel_lift([-2, 0, 1], [3, 1], [-3, 1], 7, 4)
    assert h == [(-2166) % 7 ** 4, 1]


@pytest.mark.parametrize("p", [2, 3, 7])
def test_lift_factors(p):
    rng = random.Random(55 + p)
    done = 0
    while done < 12:
        r = rng.randint(2, 4)
        facs = [random_monic(rng, rng.randint(1, 2), 6) for _ in range(r)]
        if any(not gcd_is_one_mod_p(facs[i], facs[j], p) for i in range(r) for j in range(i + 1, r)):
            continue
        lc = rng.choice([1, -1, 5, 11])
        if lc % p == 0:
            continue
        f = [lc]
        for x in facs:
            f = ref_mul(f, x)
        k = 8
        lifted = lift_factors(f, [ref_mod(x, p) for x in facs], p, k)
        prod = [lc]
        for x in lifted:
            prod = ref_mul(prod, x)
        assert congruent(prod, f, p ** k)
        assert [symmetric(x, p ** k) for x in lifted] == facs
        done += 1
