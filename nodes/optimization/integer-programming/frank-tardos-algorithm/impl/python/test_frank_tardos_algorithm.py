# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frank-tardos-algorithm/. The authors are listed in prov/JSEDZ0.jsonl.

import itertools
import random
from fractions import Fraction

from frank_tardos_algorithm import dot, frank_tardos, simultaneous_approximation


def sgn(x) -> int:
    return (x > 0) - (x < 0)


def ball(n: int, r: int):
    for b in itertools.product(range(-r, r + 1), repeat=n):
        if sum(abs(x) for x in b) <= r:
            yield b


def test_example_of_the_page() -> None:
    w = [1001, 2001, 3000]
    trace: list = []
    assert frank_tardos(w, 3, trace) == [8, 15, 21]
    f = Fraction
    assert trace == [
        ((f(1001, 3000), f(667, 1000), f(1)), 3, (1, 2, 3), (f(1, 1000), f(1, 1000), f(0))),
        ((f(1), f(1), f(0)), 1, (1, 1, 0), (f(0), f(0), f(0))),
    ]
    assert dot(w, [1, 1, -1]) == 2 and dot([8, 15, 21], [1, 1, -1]) == 2
    for b in ball(3, 2):
        assert sgn(dot(w, b)) == sgn(dot([8, 15, 21], b))


def test_zero_and_integer_vectors() -> None:
    assert frank_tardos([0, 0], 5) == [0, 0]
    assert frank_tardos([7, 9, -12], 4) == [7, 9, -12]


def test_simultaneous_approximation_bounds() -> None:
    rng = random.Random(6)
    for _ in range(30):
        n = rng.randint(1, 4)
        big_n = rng.randint(2, 9)
        v = [Fraction(rng.randint(-1000, 1000), 1000) for _ in range(n)]
        v[rng.randrange(n)] = Fraction(1)
        q, p = simultaneous_approximation(v, Fraction(1, big_n))
        k = -(-n * (n + 1) // 4)
        assert 1 <= q <= 2**k * big_n**n
        assert all(abs(q * x - y) <= Fraction(1, big_n) for x, y in zip(v, p))


def test_signs_against_brute_force() -> None:
    rng = random.Random(2)
    for _ in range(40):
        n = rng.randint(1, 3)
        big_n = rng.randint(2, 7)
        w = [Fraction(rng.randint(-10**6, 10**6), rng.randint(1, 10**4)) for _ in range(n)]
        if rng.random() < 0.3:
            w[rng.randrange(n)] = Fraction(0)
        trace: list = []
        u = frank_tardos(w, big_n, trace)
        assert len(trace) <= n
        for b in ball(n, big_n - 1):
            assert sgn(dot(w, b)) == sgn(dot(u, b))
        # the size bound proved on the page: |u|_inf < M^t <= (2^k N^(n+1))^n
        k = -(-n * (n + 1) // 4)
        assert max(abs(x) for x in u) <= (2**k * big_n ** (n + 1)) ** n


def test_same_optimal_solutions_over_the_cube() -> None:
    rng = random.Random(9)
    for _ in range(15):
        n = rng.randint(2, 4)
        w = [Fraction(rng.randint(-10**5, 10**5), rng.randint(1, 999)) for _ in range(n)]
        u = frank_tardos(w, n + 1)  # x - y has 1-norm at most n for x, y in {0,1}^n
        cube = list(itertools.product((0, 1), repeat=n))
        for x, y in itertools.combinations(cube, 2):
            assert sgn(dot(w, x) - dot(w, y)) == sgn(dot(u, x) - dot(u, y))
        best_w = max(dot(w, x) for x in cube)
        best_u = max(dot(u, x) for x in cube)
        assert {x for x in cube if dot(w, x) == best_w} == {x for x in cube if dot(u, x) == best_u}
