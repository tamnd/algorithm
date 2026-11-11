# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/short-integer-solution/. The authors are listed in prov/JRMD0G.jsonl.
"""Tests for Ajtai's hash and the birthday attack on toy SIS instances.

SIS is a problem, not a standard algorithm, so there are no official test
vectors. All parameters are toy sizes.
"""

import math
import random

from short_integer_solution import (
    ajtai_hash,
    birthday_collision,
    collision_to_sis,
    is_sis_solution,
    kernel_vector,
    output_bits,
    random_matrix,
)


def test_compression():
    # n = 3, q = 101, m = 24: 2^24 inputs and 101^3 (about 2^19.97) outputs.
    n, q, m = 3, 101, 24
    assert m > output_bits(n, q)
    assert 2 ** m > q ** n
    assert math.isclose(output_bits(n, q), 3 * math.log2(101))


def test_hash_is_linear():
    rng = random.Random(1)
    n, q, m = 3, 101, 24
    A = random_matrix(n, m, q, rng)
    for _ in range(200):
        x = [rng.randrange(2) for _ in range(m)]
        y = [rng.randrange(2) for _ in range(m)]
        s = [a + b for a, b in zip(x, y)]
        hx, hy, hs = ajtai_hash(A, x, q), ajtai_hash(A, y, q), ajtai_hash(A, s, q)
        assert hs == tuple((a + b) % q for a, b in zip(hx, hy))


def test_birthday_collision_gives_sis_solution():
    rng = random.Random(2)
    n, q, m = 3, 101, 24
    for _ in range(5):
        A = random_matrix(n, m, q, rng)
        x, x2, tries = birthday_collision(A, q, rng)
        assert x != x2 and ajtai_hash(A, x, q) == ajtai_hash(A, x2, q)
        z = collision_to_sis(x, x2)
        assert set(z) <= {-1, 0, 1}
        assert is_sis_solution(A, z, q, math.sqrt(m))
        assert tries < 20000  # about sqrt(pi * 101^3 / 2), near 1300, expected


def test_birthday_larger():
    # n = 3, q = 257, m = 32: 2^24 outputs, collision after about 2^12 tries.
    rng = random.Random(3)
    A = random_matrix(3, 32, 257, rng)
    x, x2, tries = birthday_collision(A, 257, rng)
    z = collision_to_sis(x, x2)
    assert is_sis_solution(A, z, 257, math.sqrt(32))


def test_checker_rejects():
    rng = random.Random(4)
    A = random_matrix(3, 24, 101, rng)
    assert not is_sis_solution(A, [0] * 24, 101, 100.0)
    z = [1] + [0] * 23
    assert not is_sis_solution(A, z, 101, 100.0) or all(r[0] == 0 for r in A)
    # q e_1 is always in the kernel, but it is long.
    z = [101] + [0] * 23
    assert is_sis_solution(A, z, 101, 101.0)
    assert not is_sis_solution(A, z, 101, 100.0)


def test_kernel_vector_is_long():
    rng = random.Random(5)
    q = 101
    long_count = 0
    for _ in range(500):
        n = rng.randint(1, 4)
        m = n + rng.randint(1, 8)
        A = random_matrix(n, m, q, rng)
        z = kernel_vector(A, q)
        assert z is not None and any(z)
        assert all(v == 0 for v in ajtai_hash(A, z, q))
        long_count += max(z) > 1
    # Elimination almost never gives a 0/1 vector: shortness is the hard part.
    assert long_count > 450
