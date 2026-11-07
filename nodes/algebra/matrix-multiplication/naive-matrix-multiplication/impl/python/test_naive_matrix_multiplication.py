# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/naive-matrix-multiplication/. The authors are listed in prov/F9X6P7.jsonl.

import random

import pytest

from naive_matrix_multiplication import naive_matrix_multiplication as mul


def oracle(a, b, p, mod=None):
    """An independent product: each column of b is formed first, then zipped with each row of a."""
    cols = [[row[j] for row in b] for j in range(p)]
    out = [[sum(x * y for x, y in zip(r, col)) for col in cols] for r in a]
    if mod is not None:
        out = [[x % mod for x in r] for r in out]
    return out


def rand(rng, r, c, lo=-9, hi=9):
    return [[rng.randint(lo, hi) for _ in range(c)] for _ in range(r)]


def test_example() -> None:
    a = [[1, 2, 3], [4, 5, 6]]
    b = [[7, 8], [9, 10], [11, 12]]
    assert mul(a, b) == [[58, 64], [139, 154]]


def test_edges() -> None:
    assert mul([], []) == []
    assert mul([[5]], [[7]]) == [[35]]
    assert mul([[], []], [], p=3) == [[0, 0, 0], [0, 0, 0]]
    assert mul([[1, 2]], [[3], [4]]) == [[11]]
    assert mul([[3], [4]], [[1, 2]]) == [[3, 6], [4, 8]]
    with pytest.raises(ValueError):
        mul([[1, 2]], [[1, 2]])


def test_identity_and_zero() -> None:
    rng = random.Random(11)
    for n in range(0, 7):
        a = rand(rng, n, n)
        eye = [[int(i == j) for j in range(n)] for i in range(n)]
        zero = [[0] * n for _ in range(n)]
        assert mul(a, eye, p=n) == a
        assert mul(eye, a, p=n) == a
        assert mul(a, zero, p=n) == zero


def test_random_over_z() -> None:
    rng = random.Random(2024)
    for _ in range(600):
        n, m, p = rng.randint(0, 6), rng.randint(0, 6), rng.randint(0, 6)
        a, b = rand(rng, n, m, -1000, 1000), rand(rng, m, p, -1000, 1000)
        assert mul(a, b, p=p) == oracle(a, b, p)


def test_random_mod_p() -> None:
    rng = random.Random(7)
    for q in (2, 3, 5, 7, 101):
        for _ in range(100):
            n, m, p = rng.randint(1, 6), rng.randint(0, 6), rng.randint(1, 6)
            a, b = rand(rng, n, m, 0, q - 1), rand(rng, m, p, 0, q - 1)
            assert mul(a, b, p=p, mod=q) == oracle(a, b, p, q)


def test_laws() -> None:
    rng = random.Random(99)
    for _ in range(100):
        n, m, p, r = (rng.randint(1, 5) for _ in range(4))
        a, b, c = rand(rng, n, m), rand(rng, m, p), rand(rng, p, r)
        assert mul(mul(a, b), c) == mul(a, mul(b, c))
        bt = [list(x) for x in zip(*b)]
        at = [list(x) for x in zip(*a)]
        assert [list(x) for x in zip(*mul(a, b))] == mul(bt, at)


def test_large_integers() -> None:
    big = 2**63 - 1
    a = [[big, big], [big, big]]
    assert mul(a, a) == [[2 * big * big] * 2] * 2
