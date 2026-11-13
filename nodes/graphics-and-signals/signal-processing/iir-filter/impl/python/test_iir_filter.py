# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iir-filter/. The authors are listed in prov/546JYA.jsonl.

import cmath
import random
from fractions import Fraction

from iir_filter import cascade, iir_filter, impulse_response, is_stable, reflection_coefficients


def difference_equation(b, a, x):
    """The defining recursion, written out directly, with a[0] = 1."""
    y = []
    for n in range(len(x)):
        s = sum(b[k] * x[n - k] for k in range(len(b)) if n - k >= 0)
        s -= sum(a[k] * y[n - k] for k in range(1, len(a)) if n - k >= 0)
        y.append(s)
    return y


def poly_mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, u in enumerate(p):
        for j, v in enumerate(q):
            r[i + j] += u * v
    return r


def roots(a):
    """Roots of z^p + a[1] z^(p-1) + ... + a[p] by the Durand-Kerner iteration."""
    p = len(a) - 1
    z = [(0.4 + 0.9j) ** i for i in range(p)]
    c = [complex(v) for v in a]
    for _ in range(500):
        nz = []
        for i in range(p):
            num = 0j
            for v in c:
                num = num * z[i] + v
            den = 1
            for j in range(p):
                if j != i:
                    den *= z[i] - z[j]
            nz.append(z[i] - num / den)
        done = max(abs(u - v) for u, v in zip(z, nz)) < 1e-14
        z = nz
        if done:
            break
    return z


def test_one_pole_example() -> None:
    b = [Fraction(1, 2)]
    a = [1, Fraction(-1, 2)]
    assert impulse_response(b, a, 5) == [Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16), Fraction(1, 32)]
    assert iir_filter(b, a, [1, 1, 1, 1]) == [Fraction(1, 2), Fraction(3, 4), Fraction(7, 8), Fraction(15, 16)]


def test_against_difference_equation_exact() -> None:
    rng = random.Random(5101)
    for _ in range(300):
        b = [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(rng.randint(1, 5))]
        a = [Fraction(1)] + [Fraction(rng.randint(-9, 9), rng.randint(2, 9)) for _ in range(rng.randint(0, 4))]
        x = [rng.randint(-10, 10) for _ in range(rng.randint(0, 25))]
        assert iir_filter(b, a, x) == difference_equation(b, a, x)


def test_normalizes_a0() -> None:
    b = [Fraction(2), Fraction(4)]
    a = [Fraction(2), Fraction(-1)]
    x = [1, 2, 3]
    assert iir_filter(b, a, x) == difference_equation([1, 2], [1, Fraction(-1, 2)], x)


def test_fir_special_case() -> None:
    assert iir_filter([1, 2, 3], [1], [1, 0, 0, 1]) == [1, 2, 3, 1]


def test_cascade_equals_product() -> None:
    rng = random.Random(5102)
    for _ in range(50):
        s1 = ([Fraction(rng.randint(-5, 5), 3), 1], [1, Fraction(rng.randint(-5, 5), 7)])
        s2 = ([1, Fraction(rng.randint(-5, 5), 2), 1], [1, Fraction(rng.randint(-5, 5), 9), Fraction(rng.randint(-5, 5), 11)])
        x = [rng.randint(-5, 5) for _ in range(20)]
        b = poly_mul(s1[0], s2[0])
        a = poly_mul(s1[1], s2[1])
        assert cascade([s1, s2], x) == iir_filter(b, a, x)


def test_stability_example() -> None:
    assert is_stable([1, Fraction(-9, 10)])
    assert not is_stable([1, -2])
    # 1 - 1.5 z^-1 + 0.56 z^-2 has poles 0.7 and 0.8.
    assert is_stable([1, Fraction(-3, 2), Fraction(14, 25)])
    assert reflection_coefficients([1, Fraction(-3, 2), Fraction(14, 25)]) == [Fraction(14, 25), Fraction(-25, 26)]
    # poles 0.5 and 1.25: unstable although each coefficient is small
    assert not is_stable([1, Fraction(-7, 4), Fraction(5, 8)])


def test_stability_against_roots() -> None:
    rng = random.Random(5103)
    checked = 0
    while checked < 200:
        p = rng.randint(1, 5)
        a = [1] + [Fraction(rng.randint(-30, 30), 10) for _ in range(p)]
        rs = roots(a)
        r = max(abs(z) for z in rs)
        if abs(r - 1) < 1e-3:
            continue  # too close to the circle for the float reference
        assert is_stable(a) == (r < 1)
        checked += 1


def test_unstable_filter_grows() -> None:
    h = impulse_response([1], [1, Fraction(-11, 10)], 60)
    assert h[-1] == Fraction(11, 10) ** 59
    assert h[-1] > 250


def test_stable_filter_decays() -> None:
    a = [1, Fraction(-3, 2), Fraction(14, 25)]
    h = impulse_response([1], a, 200)
    # h[n] = 8 (0.8)^n - 7 (0.7)^n from the partial fractions
    for n in (0, 1, 2, 10, 50):
        assert h[n] == 8 * Fraction(4, 5) ** n - 7 * Fraction(7, 10) ** n
    assert sum(abs(v) for v in h) < 100


def test_frequency_response_of_impulse_response() -> None:
    b = [1, 1]
    a = [1, Fraction(-1, 2)]
    h = impulse_response(b, a, 200)
    for w in (0.0, 0.7, 2.0, 3.1):
        z = cmath.exp(1j * w)
        exact = (1 + 1 / z) / (1 - 0.5 / z)
        approx = sum(float(v) * z ** (-n) for n, v in enumerate(h))
        assert abs(exact - approx) < 1e-12
