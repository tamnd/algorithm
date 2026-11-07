# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/payne-hanek-argument-reduction/. The authors are listed in prov/H4GFMJ.jsonl.

import math
import random
from fractions import Fraction

from payne_hanek_argument_reduction import P, reduce, naive_reduce, sin_via_reduction

REF_BITS = 2600


def _atan_inv(n, bits):
    total, term, k, sign = 0, (1 << bits) // n, 1, 1
    while term:
        total += sign * (term // k)
        term //= n * n
        k += 2
        sign = -sign
    return total


def _pi_reference(bits):
    # Gauss's formula, independent of the Machin formula in the implementation.
    g = 40
    b = bits + g
    s = 48 * _atan_inv(18, b) + 32 * _atan_inv(57, b) - 20 * _atan_inv(239, b)
    return Fraction(s >> g, 1 << bits)


PI = _pi_reference(REF_BITS)


def exact_reduce(x):
    """Reference k and r with |r| <= pi/4, from a 2600-bit pi."""
    X = Fraction(x)
    t = X * 2 / PI
    j = math.floor(t + Fraction(1, 2))
    r = X - j * PI / 2
    return j % 4, r


def check(x):
    k, hi, lo = reduce(x)
    kr, r = exact_reduce(x)
    assert k == kr, (x, k, kr)
    err = abs(Fraction(hi) + Fraction(lo) - r)
    assert err <= abs(r) * Fraction(1, 2 ** 104), (x, float(err / abs(r)))
    assert hi == float(r), (x, hi, float(r))


def test_known_values():
    for x in (1e22, 1e300, -5.0, 1.0, 2.0, 3.0, 100.0, 2.0 ** 1023, 1.7976931348623157e308):
        check(x)


def test_small_arguments_unchanged():
    for x in (0.0, -0.0, 5e-324, 1e-300, 0.5, -0.785, 0.7853981633974483):
        assert reduce(x) == (0, x, 0.0)


def test_worst_case_binary64():
    # Closest binary64 to a multiple of pi/2 (Muller, Elementary Functions, Ch. 11).
    x = 6381956970095103 * 2.0 ** 797
    check(x)
    k, hi, lo = reduce(x)
    assert 2.0 ** -61 < hi < 2.0 ** -60


def test_random_all_exponents():
    rng = random.Random(20261107)
    for _ in range(1500):
        e = rng.randint(-1, 1023)
        m = rng.random() + 1.0
        x = math.ldexp(m, e) * rng.choice((1, -1))
        if math.isfinite(x):
            check(x)


def test_near_multiples_of_pi_over_2():
    # Floats next to k*pi/2 for moderate k stress the cancellation.
    for n in range(1, 400):
        c = float(n * PI / 2)
        for x in (c, math.nextafter(c, 0), math.nextafter(c, math.inf)):
            check(x)


def test_sin_matches_libm():
    rng = random.Random(7)
    for _ in range(2000):
        x = math.ldexp(rng.random() + 1.0, rng.randint(0, 1023))
        a, b = sin_via_reduction(x), math.sin(x)
        assert abs(a - b) <= 2 * math.ulp(b), (x, a, b)


def test_naive_reduction_fails_for_large_x():
    k, r = naive_reduce(1e22)
    kr, rr = exact_reduce(1e22)
    assert abs(r - float(rr)) > 0.1


def test_window_error_bound():
    # The dropped tail of 2/pi is below 2^(53 - P) in units of the fraction.
    assert 53 - P <= -190
