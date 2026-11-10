# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-matrix-multiplication/. The authors are listed in prov/QZM9BG.jsonl.

import random

from parallel_matrix_multiplication import Matrix, ceil_lg, multiply_loops, multiply_no_temp, multiply_temp


def oracle(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def rand_matrix(rng: random.Random, n: int) -> Matrix:
    return [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]


def test_example() -> None:
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    for f in (multiply_loops, multiply_temp, multiply_no_temp):
        assert f(a, b)[0] == [[19, 22], [43, 50]]


def test_loops_any_size() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(1, 12)
        a, b = rand_matrix(rng, n), rand_matrix(rng, n)
        c, cost = multiply_loops(a, b)
        assert c == oracle(a, b)
        assert cost.work == n**3 + n * n - 1
        assert cost.span == 2 * ceil_lg(n) + n


def test_recursive_against_triple_loop() -> None:
    rng = random.Random(6)
    for _ in range(400):
        n = 2 ** rng.randint(0, 3)
        a, b = rand_matrix(rng, n), rand_matrix(rng, n)
        want = oracle(a, b)
        assert multiply_temp(a, b)[0] == want
        assert multiply_no_temp(a, b)[0] == want


def test_closed_forms() -> None:
    rng = random.Random(7)
    for big_l in range(0, 6):
        n = 2**big_l
        a, b = rand_matrix(rng, n), rand_matrix(rng, n)
        want = oracle(a, b)
        c1, k1 = multiply_temp(a, b)
        c2, k2 = multiply_no_temp(a, b)
        c0, k0 = multiply_loops(a, b)
        assert c0 == c1 == c2 == want
        assert k0.work == n**3 + n * n - 1 and k0.span == 2 * big_l + n
        assert 7 * k1.work == 7 * n**3 + 14 * n * n * (n - 1) + 6 * (n**3 - 1)
        assert k1.span == big_l * big_l + 5 * big_l + 1
        assert 7 * k2.work == 7 * n**3 + 6 * (n**3 - 1)
        assert k2.span == 5 * n - 4


def test_span_crossover() -> None:
    # the span with a temporary matrix is below the span of the loops from n = 64 on
    for big_l in range(0, 21):
        n = 2**big_l
        temp, loops = big_l * big_l + 5 * big_l + 1, 2 * big_l + n
        assert (temp < loops) == (n >= 64)
