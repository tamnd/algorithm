# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bibo-stability/. The authors are listed in prov/WPRRG6.jsonl.

import random
from fractions import Fraction

from bibo_stability import cancel, impulse_response, is_stable, lfilter, poly_divmod, poly_gcd, reflection_coefficients


def poly_mul(p, q):
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, u in enumerate(p):
        for j, v in enumerate(q):
            out[i + j] += u * v
    return out


def random_factors(rng, limit=Fraction(3, 2)):
    """A(w) as a product of known factors, with the squared pole moduli.

    (1 - r w) has the pole z = r; (1 - t w + s w^2) with t^2 < 4 s has two
    poles of modulus s^(1/2). Returns A and the list of |pole|^2 values.
    """
    a, mods = [Fraction(1)], []
    for _ in range(rng.randint(1, 4)):
        if rng.random() < 0.5:
            r = Fraction(rng.randint(-15, 15), 10)
            a = poly_mul(a, [Fraction(1), -r])
            mods.append(r * r)
        else:
            s = Fraction(rng.randint(1, 225), 100)
            t = Fraction(rng.randint(-10, 10), 10)
            while t * t >= 4 * s:
                t /= 2
            a = poly_mul(a, [Fraction(1), -t, s])
            mods += [s, s]
    return a, mods


def durand_kerner(c):
    """Roots of c[0] z^p + c[1] z^(p-1) + ... + c[p] in floating point."""
    p = len(c) - 1
    lead = complex(c[0])
    c = [complex(v) / lead for v in c]
    roots = [(0.4 + 0.9j) ** k for k in range(p)]
    for _ in range(500):
        new = []
        for i, r in enumerate(roots):
            val = sum(cv * r ** (p - j) for j, cv in enumerate(c))
            den = 1 + 0j
            for j, s in enumerate(roots):
                if j != i:
                    den *= r - s
            new.append(r - val / den)
        roots = new
    return roots


def test_known_poles() -> None:
    rng = random.Random(7601)
    for _ in range(300):
        a, mods = random_factors(rng)
        assert is_stable([1], a) == all(m < 1 for m in mods)


def test_against_numerical_roots() -> None:
    rng = random.Random(7602)
    checked = 0
    for _ in range(200):
        a = [1] + [Fraction(rng.randint(-12, 12), 8) for _ in range(rng.randint(1, 5))]
        roots = durand_kerner(a)
        if min(abs(abs(r) - 1) for r in roots) < 1e-6:
            continue
        checked += 1
        assert is_stable([1], a) == all(abs(r) < 1 for r in roots)
    assert checked > 150


def test_partial_sums_of_abs_h() -> None:
    # stable: the partial sums of |h[n]| settle; unstable or marginal: they grow
    stable = ([1, 2], [1, Fraction(-1, 2), Fraction(1, 4)])
    s = [sum(abs(v) for v in impulse_response(*stable, n)) for n in (50, 100, 200)]
    assert s[2] - s[1] < Fraction(1, 10**12) and s[1] - s[0] < Fraction(1, 10**6)
    assert is_stable(*stable)
    for b, a in (([1], [1, -1]), ([1], [1, 1]), ([1], [1, 0, 1]), ([1], [1, Fraction(-11, 10)])):
        s = [sum(abs(v) for v in impulse_response(b, a, n)) for n in (50, 100, 200)]
        assert s[2] - s[1] >= s[1] - s[0] > 10
        assert not is_stable(b, a)


def test_worst_case_input_reaches_the_l1_norm() -> None:
    # x[n] = sign(h[N - n]) has |x| <= 1 and gives y[N] = sum_{n <= N} |h[n]|
    for b, a in (([1, 2], [1, Fraction(-1, 2), Fraction(1, 4)]), ([1], [1, -1]), ([1], [1, 0, 1])):
        size = 60
        h = impulse_response(b, a, size)
        x = [(1 if h[size - 1 - n] >= 0 else -1) for n in range(size)]
        y = lfilter(b, a, x)
        assert y[size - 1] == sum(abs(v) for v in h)


def test_accumulator_is_unbounded() -> None:
    y = lfilter([1], [1, -1], [1] * 100)
    assert y == list(range(1, 101))


def test_pole_zero_cancellation() -> None:
    # (1 - 2 z^-1) / (1 - 2 z^-1) is the identity system: stable, h = delta
    b = a = [1, -2]
    assert impulse_response(b, a, 20) == [1] + [0] * 19
    assert is_stable(b, a)
    assert reflection_coefficients(a) == [-2]  # the uncancelled denominator fails the test
    # (1 - 3 w)(1 + w / 4) / ((1 - 3 w)(1 - w / 2)): one unstable pole cancels, one stable stays
    b = poly_mul([1, -3], [1, Fraction(1, 4)])
    a = poly_mul([1, -3], [1, Fraction(-1, 2)])
    assert cancel(b, a) == ([1, Fraction(1, 4)], [1, Fraction(-1, 2)])
    assert is_stable(b, a)


def test_polynomial_helpers() -> None:
    rng = random.Random(7603)
    for _ in range(100):
        p = [Fraction(rng.randint(-9, 9)) for _ in range(rng.randint(1, 6))]
        d = [Fraction(rng.randint(-9, 9)) for _ in range(rng.randint(1, 4))]
        if all(v == 0 for v in d):
            continue
        q, r = poly_divmod(p, d)
        recon = poly_mul(q, d)
        recon += [Fraction(0)] * (len(p) - len(recon))
        for i, v in enumerate(r):
            recon[i] += v
        while len(recon) > 1 and recon[-1] == 0:
            recon.pop()
        pt = p[:]
        while len(pt) > 1 and pt[-1] == 0:
            pt.pop()
        assert recon == pt
    g = poly_gcd(poly_mul([1, 1], [2, 3]), poly_mul([1, 1], [5, -1]))
    assert g == [1, 1]


def test_step_down_examples() -> None:
    # poles 1/2 and -1/3: A = (1 - w / 2)(1 + w / 3) = 1 - w / 6 - w^2 / 6
    a = [1, Fraction(-1, 6), Fraction(-1, 6)]
    ks = reflection_coefficients(a)
    assert ks == [Fraction(-1, 6), Fraction(-1, 5)]
    assert is_stable([1], a)
    assert not is_stable([1], [1, 0, 0, Fraction(-27, 8)])  # poles of modulus 3/2
