# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-diophantine-solution/. The authors are listed in prov/747E8M.jsonl.

import math
import random

from linear_diophantine_solution import solve_linear_diophantine


def brute_solvable(a: int, b: int, c: int) -> bool:
    """Decide solvability by direct search (small inputs only)."""
    if a == 0 and b == 0:
        return c == 0
    if b == 0:
        return c % a == 0
    # x and x + |b| give the same residue of c - a*x modulo b.
    return any((c - a * x) % b == 0 for x in range(abs(b)))


def check(a: int, b: int, c: int) -> tuple[int, int] | None:
    r = solve_linear_diophantine(a, b, c)
    if r is not None:
        x, y = r
        assert a * x + b * y == c
    return r


def fib(n: int) -> int:
    x, y = 0, 1
    for _ in range(n):
        x, y = y, x + y
    return x


def test_example() -> None:
    assert solve_linear_diophantine(1071, 462, 63) == (-9, 21)
    assert solve_linear_diophantine(6, 9, 7) is None
    assert solve_linear_diophantine(3, 5, 1) == (2, -1)


def test_zero_and_signs() -> None:
    assert solve_linear_diophantine(0, 0, 0) == (0, 0)
    assert solve_linear_diophantine(0, 0, 5) is None
    assert check(5, 0, 15) == (3, 0)
    assert check(0, 5, 15) == (0, 3)
    assert check(5, 0, 7) is None
    assert check(-5, 0, 15) == (-3, 0)
    assert check(-4, 6, 10) is not None
    assert check(-4, -6, -10) is not None
    assert check(4, 6, 0) == (0, 0)
    assert check(1, 1, 1) is not None
    assert check(7, 7, 14) is not None
    assert check(7, 7, 15) is None
    assert check(-7, 7, 0) is not None


def test_powers_of_two() -> None:
    for i in range(0, 70, 7):
        for j in range(0, 70, 5):
            a, b = 2**i, 2**j
            g = 2 ** min(i, j)
            assert check(a, b, g) is not None
            assert check(a, b, 3 * g) is not None
            assert (check(a, b, g + 1) is None) == (g > 1)


def test_fibonacci_worst_case() -> None:
    assert solve_linear_diophantine(832040, 1346269, 1) == (514229, -317811)
    for n in range(2, 300, 7):
        a, b = fib(n), fib(n + 1)
        assert check(a, b, 1) is not None
        assert check(b, a, -12345) is not None


def test_random_small_against_brute_force() -> None:
    rng = random.Random(747)
    for _ in range(3000):
        a = rng.randint(-60, 60)
        b = rng.randint(-60, 60)
        c = rng.randint(-200, 200)
        r = check(a, b, c)
        assert (r is not None) == brute_solvable(a, b, c)


def test_random_large() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        digits = rng.choice([1, 5, 20, 100, 300, 500])
        a = rng.randint(-(10**digits), 10**digits)
        b = rng.randint(-(10**digits), 10**digits)
        g = math.gcd(a, b)
        if rng.random() < 0.5 or g == 0:
            c = rng.randint(-(10**digits), 10**digits)
        else:
            c = g * rng.randint(-(10**digits), 10**digits)
        r = check(a, b, c)
        expect = (c == 0) if g == 0 else (c % g == 0)
        assert (r is not None) == expect


def test_common_factor_large() -> None:
    rng = random.Random(9)
    for _ in range(100):
        f = rng.randint(2, 10**200)
        a = f * rng.randint(1, 10**150)
        b = -f * rng.randint(1, 10**150)
        g = math.gcd(a, b)
        assert check(a, b, 7 * g) is not None
        assert check(a, b, g + 1) is None


def test_general_solution_window() -> None:
    rng = random.Random(31)
    for _ in range(300):
        a = rng.randint(-30, 30)
        b = rng.randint(-30, 30)
        c = rng.randint(-60, 60)
        if a == 0 or b == 0:
            continue
        r = solve_linear_diophantine(a, b, c)
        sols = {(x, (c - a * x) // b) for x in range(-100, 101) if (c - a * x) % b == 0}
        if r is None:
            assert not sols
            continue
        x0, y0 = r
        g = math.gcd(a, b)
        dx, dy = b // g, -a // g
        expect = set()
        for k in range(-300, 301):
            x, y = x0 + k * dx, y0 + k * dy
            if -100 <= x <= 100:
                expect.add((x, y))
        assert sols == expect
