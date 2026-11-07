# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lattice-multiplication/. The authors are listed in prov/HGRER8.jsonl.

import random

from lattice_multiplication import lattice_multiply


def digits(x: int, base: int, n: int) -> list[int]:
    out = []
    for _ in range(n):
        out.append(x % base)
        x //= base
    assert x == 0
    return out


def value(c: list[int], base: int) -> int:
    v = 0
    for d in reversed(c):
        v = v * base + d
    return v


def test_example() -> None:
    assert lattice_multiply([3, 9, 0, 4], [9, 9, 1], 10) == [7, 0, 5, 4, 1, 8, 0]
    assert value(lattice_multiply([13, 15, 15], [7, 12], 16), 16) == 4093 * 199


def test_edges() -> None:
    assert lattice_multiply([], [], 16) == []
    assert lattice_multiply([], [5], 16) == [0]
    assert lattice_multiply([0, 0], [15], 16) == [0, 0, 0]
    assert lattice_multiply([1], [15, 15], 16) == [15, 15, 0]
    assert lattice_multiply([9], [9], 10) == [1, 8]
    for base in (2, 3, 10, 16, 256):
        for m in range(1, 7):
            for n in range(1, 7):
                a, b = [base - 1] * m, [base - 1] * n
                assert value(lattice_multiply(a, b, base), base) == (base**m - 1) * (base**n - 1)


def test_unbalanced() -> None:
    rng = random.Random(3)
    for _ in range(40):
        m = rng.randint(30, 60)
        x, y = rng.randrange(256**m), rng.randrange(256)
        assert value(lattice_multiply(digits(x, 256, m), [y], 256), 256) == x * y
        assert value(lattice_multiply([y], digits(x, 256, m), 256), 256) == x * y


def test_random_against_int() -> None:
    rng = random.Random(1478)
    for _ in range(1500):
        base = rng.choice((2, 10, 16, 256))
        m, n = rng.randint(0, 10), rng.randint(0, 10)
        x, y = rng.randrange(base**m), rng.randrange(base**n)
        c = lattice_multiply(digits(x, base, m), digits(y, base, n), base)
        assert len(c) == m + n and all(0 <= d < base for d in c)
        assert value(c, base) == x * y
