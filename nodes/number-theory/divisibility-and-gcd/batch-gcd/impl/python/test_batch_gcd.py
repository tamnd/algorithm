# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/batch-gcd/. The authors are listed in prov/FT9662.jsonl.

import math
import random

from batch_gcd import batch_gcd, euclid_gcd, product_tree, shared_factor_pairs


def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def reference(values: list[int]) -> list[int]:
    """gcd(a_i, product of the others) with math.gcd (reference only)."""
    out = []
    for i, a in enumerate(values):
        rest = 1
        for j, b in enumerate(values):
            if j != i:
                rest *= b
        out.append(math.gcd(a, rest))
    return out


def reference_pairs(values: list[int]) -> list[tuple[int, int, int]]:
    out = []
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            d = math.gcd(values[i], values[j])
            if d != 1:
                out.append((i, j, d))
    return out


def test_example() -> None:
    assert batch_gcd([12, 18, 35, 49, 10]) == [12, 6, 35, 7, 10]
    moduli = [101 * 103, 101 * 107, 109 * 113, 113 * 127, 131 * 137]
    assert batch_gcd(moduli) == [101, 101, 113, 113, 1]
    assert shared_factor_pairs(moduli) == [(0, 1, 101), (2, 3, 113)]


def test_product_tree_shape() -> None:
    tree = product_tree([2, 3, 5, 7, 11])
    assert tree == [[2, 3, 5, 7, 11], [6, 35, 11], [210, 11], [2310]]


def test_edge_inputs() -> None:
    assert batch_gcd([]) == []
    assert batch_gcd([7]) == [1]
    assert batch_gcd([0]) == [1]
    assert batch_gcd([0, 6, -4]) == [24, 6, 4]
    assert batch_gcd([0, 0, 5]) == [0, 0, 5]
    assert batch_gcd([1, 1, 1]) == [1, 1, 1]
    assert batch_gcd([-6, 10, 1]) == [2, 2, 1]
    assert batch_gcd([9, 9]) == [9, 9]
    for values in ([0], [0, 6, -4], [0, 0, 5], [-6, 10, 1], [9, 9], [1, 1, 1]):
        assert batch_gcd(values) == reference(values)


def test_euclid_gcd() -> None:
    rng = random.Random(3)
    for _ in range(500):
        a = rng.randrange(-(10**rng.randrange(1, 300)), 10**rng.randrange(1, 300))
        b = rng.choice([0, 1, -1, a, 2**rng.randrange(200), rng.randrange(-(10**50), 10**50)])
        assert euclid_gcd(a, b) == math.gcd(a, b)
    for k in range(2, 400):
        assert euclid_gcd(fib(k + 1), fib(k)) == 1


def test_random_small_lists() -> None:
    rng = random.Random(2012)
    for _ in range(500):
        n = rng.randrange(1, 12)
        values = [
            rng.choice(
                [
                    0,
                    1,
                    -1,
                    rng.randrange(-200, 200),
                    2**rng.randrange(0, 40),
                    fib(rng.randrange(1, 60)),
                    rng.randrange(1, 10**6),
                ]
            )
            for _ in range(n)
        ]
        if rng.random() < 0.2 and values:
            values.append(values[0])  # equal inputs
        assert batch_gcd(values) == reference(values)
        if 0 not in values:
            assert shared_factor_pairs(values) == reference_pairs(values)


def test_consecutive_fibonacci_are_coprime() -> None:
    values = [fib(k) for k in range(3, 60, 2)]
    # Odd-index Fibonacci numbers: gcd(F_i, F_j) = F_gcd(i, j).
    assert batch_gcd(values) == reference(values)
    values = [fib(k) for k in (101, 102, 103)]
    assert batch_gcd(values) == [1, 1, 1]


def test_large_rsa_like_moduli() -> None:
    rng = random.Random(77)
    for _ in range(25):
        factors = [rng.randrange(10**149, 10**150) | 1 for _ in range(12)]
        values = []
        for _ in range(10):
            p, q = rng.sample(factors, 2)
            values.append(p * q)
        values.append(rng.randrange(10**299, 10**300))
        assert batch_gcd(values) == reference(values)
        assert shared_factor_pairs(values) == reference_pairs(values)


def test_many_inputs() -> None:
    rng = random.Random(5)
    values = [rng.randrange(2, 10**30) for _ in range(300)]
    assert batch_gcd(values) == reference(values)
