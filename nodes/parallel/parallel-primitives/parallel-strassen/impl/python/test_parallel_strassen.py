# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-strassen/. The authors are listed in prov/B0S9SD.jsonl.

import random

from parallel_strassen import Matrix, strassen


def triple_loop(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def work_formula(big_l: int) -> int:
    n = 2**big_l
    w3 = 37 * 7**big_l - 32 * n * n - 2
    assert w3 % 3 == 0
    return w3 // 3


def test_example() -> None:
    c, cost = strassen([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    assert c == [[19, 22], [43, 50]]
    assert (cost.work, cost.span) == (43, 14)


def test_random_against_triple_loop() -> None:
    rng = random.Random(9)
    for _ in range(600):
        n = 2 ** rng.randint(0, 3)
        hi = rng.choice([1, 9, 10**6])
        a = [[rng.randint(-hi, hi) for _ in range(n)] for _ in range(n)]
        b = [[rng.randint(-hi, hi) for _ in range(n)] for _ in range(n)]
        assert strassen(a, b)[0] == triple_loop(a, b)


def test_closed_forms() -> None:
    rng = random.Random(10)
    for big_l in range(0, 6):
        n = 2**big_l
        a = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
        b = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
        c, cost = strassen(a, b)
        assert c == triple_loop(a, b)
        assert cost.work == work_formula(big_l)
        assert cost.span == 2 * big_l * big_l + 11 * big_l + 1


def test_work_crossover_with_the_recursive_product() -> None:
    # the recursive product with a temporary matrix, counted with the same rules
    for big_l in range(1, 30):
        n = 2**big_l
        classical = n**3 + 2 * n * n * (n - 1) + 6 * (n**3 - 1) // 7
        assert (work_formula(big_l) < classical) == (n >= 512)
