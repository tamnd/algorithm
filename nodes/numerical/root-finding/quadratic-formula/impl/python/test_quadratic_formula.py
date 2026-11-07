# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadratic-formula/. The authors are listed in prov/CQ88BP.jsonl.

import math
import random
from decimal import Decimal, localcontext

from quadratic_formula import quadratic_roots, quadratic_roots_naive

U = 2.0**-53


def reference(a, b, c):
    """Roots of the stored coefficients by the textbook formula at 120 digits."""
    with localcontext() as ctx:
        ctx.prec = 120
        A, B, C = Decimal(a), Decimal(b), Decimal(c)
        d = B * B - 4 * A * C
        if d < 0:
            re = -B / (2 * A)
            im = abs((-d).sqrt() / (2 * A))
            return "complex", (re, im)
        s = d.sqrt()
        r = sorted([(-B - s) / (2 * A), (-B + s) / (2 * A)])
        return "real", tuple(r)


def rel(x, y):
    return abs(Decimal(x) - y) / abs(y) if y != 0 else abs(Decimal(x))


def test_cancellation_example():
    r = quadratic_roots(1.0, -1e8, 1.0)
    assert r.kind == "real" and r.roots == (1e-08, 1e8)
    naive = quadratic_roots_naive(1.0, -1e8, 1.0)
    assert naive[0] == 7.450580596923828e-09  # 25 percent wrong


def test_close_roots_exact_discriminant():
    b, c = -(2 + 2.0**-26), 1 + 2.0**-26
    r = quadratic_roots(1.0, b, c)
    assert r.roots == (1.0, 1 + 2.0**-26)
    naive = quadratic_roots_naive(1.0, b, c)
    assert naive[0] == naive[1] == 1 + 2.0**-27  # the discriminant rounded to 0


def test_complex_pair():
    r = quadratic_roots(1.0, 1.0, 1.0)
    assert r.kind == "complex"
    assert r.roots == (complex(-0.5, 0.8660254037844386), complex(-0.5, -0.8660254037844386))
    r = quadratic_roots(-2.0, 0.0, -8.0)  # pure imaginary 2i, -2i with a < 0
    assert r.roots == (2j, -2j)


def test_double_root_and_zero_root():
    assert quadratic_roots(1.0, -2.0, 1.0).roots == (1.0, 1.0)
    assert quadratic_roots(3.0, 0.0, 0.0).roots == (0.0, 0.0)
    assert quadratic_roots(2.0, -6.0, 0.0).roots == (0.0, 3.0)


def test_not_quadratic_and_invalid():
    assert quadratic_roots(0.0, 1.0, 1.0).kind == "not quadratic"
    assert quadratic_roots(math.nan, 1.0, 1.0).kind == "invalid"
    assert quadratic_roots(1.0, math.inf, 1.0).kind == "invalid"


def test_no_overflow_with_huge_coefficients():
    big = math.ldexp(1.0, 1000)
    r = quadratic_roots(big, -3 * big, 2 * big)
    assert r.roots == (1.0, 2.0)
    naive = quadratic_roots_naive(big, -3 * big, 2 * big)
    assert math.isnan(naive[0]) or math.isinf(naive[0])
    tiny = math.ldexp(1.0, -1000)
    r = quadratic_roots(tiny, -3 * tiny, 2 * tiny)
    assert r.roots == (1.0, 2.0)
    assert quadratic_roots_naive(tiny, -3 * tiny, 2 * tiny) != (1.0, 2.0)


def test_vieta():
    rng = random.Random(7)
    for _ in range(200):
        a, b, c = (rng.uniform(-10, 10) for _ in range(3))
        r = quadratic_roots(a, b, c)
        x, y = r.roots
        assert abs(x + y + b / a) <= 1e-12 * (abs(x) + abs(y) + abs(b / a))
        assert abs(x * y - c / a) <= 1e-12 * (abs(x * y) + abs(c / a))


def test_random_against_decimal_reference():
    rng = random.Random(20261107)
    for _ in range(600):
        a, b, c = (rng.choice((-1, 1)) * rng.uniform(1, 2) * 10.0 ** rng.uniform(-8, 8) for _ in range(3))
        r = quadratic_roots(a, b, c)
        kind, ref = reference(a, b, c)
        assert r.kind == kind
        if kind == "real":
            for got, want in zip(r.roots, ref):
                assert rel(got, want) <= Decimal(4 * U)
        else:
            z = r.roots[0]
            assert rel(z.real, ref[0]) <= Decimal(4 * U)
            assert rel(z.imag, ref[1]) <= Decimal(4 * U)
            assert r.roots[1] == z.conjugate()
