# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/half-gcd/. The authors are listed in prov/NZPF3Q.jsonl.

import math
import random

from half_gcd import fast_gcd, half_gcd


def brute_gcd(a: int, b: int) -> int:
    """Largest common divisor by direct search (small inputs only)."""
    a, b = abs(a), abs(b)
    if a == 0 or b == 0:
        return a + b
    return max(d for d in range(1, min(a, b) + 1) if a % d == 0 and b % d == 0)


def euclid_state(a: int, b: int) -> tuple[list[int], int, int]:
    """Reference: plain Euclid on a >= b >= 0 until the first remainder below 2^m."""
    limit = 1 << ((a.bit_length() + 1) // 2)
    qs = []
    while b >= limit:
        qs.append(a // b)
        a, b = b, a % b
    return qs, a, b


def fib(n: int) -> int:
    x, y = 0, 1
    for _ in range(n):
        x, y = y, x + y
    return x


def check_half(a: int, b: int, threshold: int) -> None:
    mat, qs, alpha, beta = half_gcd(a, b, threshold)
    assert (qs, alpha, beta) == euclid_state(a, b)
    m00, m01, m10, m11 = mat
    assert (m00 * alpha + m01 * beta, m10 * alpha + m11 * beta) == (a, b)
    assert m00 * m11 - m01 * m10 == (-1) ** len(qs)


def test_example() -> None:
    a, b = 3141592653, 2718281828
    mat, qs, alpha, beta = half_gcd(a, b, threshold=16)
    assert qs == [1, 6, 2, 2, 1, 2, 6, 8, 2, 1]
    assert (alpha, beta) == (99065, 56321)
    assert mat == (22873, 15548, 19791, 13453)
    assert fast_gcd(a, b, threshold=16) == 1
    # leading halves of the example and of the second call
    assert half_gcd(47936, 41477, 16)[1:] == ([1, 6, 2, 2, 1, 2], 316, 65)
    assert half_gcd(3353, 400, 16)[1:] == ([8, 2, 1], 94, 59)


def test_fixup_example() -> None:
    # the leading 16 bits suggest a 7th quotient 2, the true one is 1
    a, b = 2723649695, 1569894979
    assert half_gcd(a >> 16, b >> 16, 16)[1] == [1, 1, 2, 1, 3, 2, 2]
    check_half(a, b, 16)
    for t in (2, 3, 4, 8):
        check_half(a, b, t)


def test_zero_one_negative() -> None:
    assert fast_gcd(0, 0) == 0
    assert fast_gcd(0, 5) == 5
    assert fast_gcd(-5, 0) == 5
    assert fast_gcd(1, 0) == 1
    assert fast_gcd(1, 1) == 1
    assert fast_gcd(-12, 18) == 6
    assert fast_gcd(12, -18) == 6
    assert fast_gcd(-12, -18) == 6
    big = 3**400
    assert fast_gcd(-big, 0) == big
    assert fast_gcd(0, -big) == big


def test_equal_inputs() -> None:
    rng = random.Random(1)
    for bits in (1, 10, 65, 300, 2000):
        x = rng.getrandbits(bits) | 1
        assert fast_gcd(x, x, 8) == x
        assert fast_gcd(x, -x) == x
        check_half(x, x, 4)


def test_powers_of_two() -> None:
    for i in range(0, 700, 37):
        for j in range(0, 700, 53):
            assert fast_gcd(1 << i, 1 << j, 8) == 1 << min(i, j)
            x, y = max(1 << i, 1 << j), min(1 << i, 1 << j)
            check_half(x, y, 8)


def test_fibonacci() -> None:
    for k in (10, 50, 200, 1000, 3000):
        a, b = fib(k + 1), fib(k)
        assert fast_gcd(a, b, 16) == 1
        check_half(a, b, 16)
        check_half(a, b, 64)
    # gcd(F_m, F_n) = F_gcd(m, n)
    assert fast_gcd(fib(1200), fib(900), 16) == fib(300)


def test_large_common_factor() -> None:
    rng = random.Random(2)
    for _ in range(40):
        g = rng.getrandbits(rng.randint(1, 1500)) | 1
        x = rng.getrandbits(rng.randint(1, 1500))
        y = rng.getrandbits(rng.randint(1, 1500))
        assert fast_gcd(g * x, g * y, 32) == g * math.gcd(x, y)
        # Euclid reaches 0 while the remainder is still above 2^m
        c = rng.randint(1, 60)
        d = rng.randint(0, 60)
        hi, lo = max(g * c, g * d), min(g * c, g * d)
        check_half(hi, lo, 4)


def test_small_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(600):
        a = rng.randint(-300, 300)
        b = rng.randint(-300, 300)
        assert fast_gcd(a, b, rng.choice([2, 3, 4, 8])) == brute_gcd(a, b)
    for a in range(0, 70):
        for b in range(0, a + 1):
            check_half(a, b, 2)


def test_random_large() -> None:
    rng = random.Random(4)
    for _ in range(600):
        digits = rng.choice([1, 20, 100, 300, 600])
        a = rng.randrange(10**digits) * rng.choice([1, -1])
        b = rng.randrange(10 ** rng.randint(1, digits)) * rng.choice([1, -1])
        threshold = rng.choice([2, 4, 16, 64])
        assert fast_gcd(a, b, threshold) == math.gcd(a, b)
        x, y = max(abs(a), abs(b)), min(abs(a), abs(b))
        check_half(x, y, threshold)
