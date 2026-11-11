# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ring-short-integer-solution/. The authors are listed in prov/NX628Q.jsonl.
"""Tests for the Ring-SIS hash and the x^n - 1 collision attack.

Ring-SIS is a problem, not a standard algorithm, so there are no official
test vectors. SWIFFT has its own reference code, which this toy hash does
not try to match (SWIFFT also maps the output to bytes in its own way).
"""

import random

from ring_short_integer_solution import (
    as_sis_matrix,
    birthday_collision,
    cyclic_collision,
    difference,
    is_ring_sis_solution,
    mul,
    random_input,
    random_key,
    ring_hash,
)


def test_mul_signs():
    # x^3 * x = x^4: -1 mod x^4 + 1 and +1 mod x^4 - 1.
    x3, x1 = [0, 0, 0, 1], [0, 1, 0, 0]
    assert mul(x3, x1, 17, -1) == [16, 0, 0, 0]
    assert mul(x3, x1, 17, +1) == [1, 0, 0, 0]


def test_all_ones_is_eigenvector_for_cyclic():
    rng = random.Random(1)
    n, q = 64, 257
    u = [1] * n
    for _ in range(20):
        a = [rng.randrange(q) for _ in range(n)]
        assert mul(a, u, q, +1) == [sum(a) % q] * n


def test_cyclic_collision_swifft_size():
    # SWIFFT-like sizes (n = 64, m = 16, q = 257), but with x^64 - 1.
    rng = random.Random(2)
    n, m, q = 64, 16, 257
    key = random_key(n, m, q, rng)
    z, w = cyclic_collision(key, q, rng)
    assert z != w
    assert ring_hash(key, z, q, +1) == ring_hash(key, w, q, +1)
    d = difference(z, w)
    assert is_ring_sis_solution(key, d, q, +1, bound=1)
    # The same two inputs do not collide in Z_q[x]/(x^64 + 1).
    assert ring_hash(key, z, q, -1) != ring_hash(key, w, q, -1)
    assert not is_ring_sis_solution(key, d, q, -1, bound=1)


def test_cyclic_collision_many_keys():
    rng = random.Random(3)
    for _ in range(20):
        key = random_key(16, 8, 97, rng)
        z, w = cyclic_collision(key, 97, rng)
        assert is_ring_sis_solution(key, difference(z, w), 97, +1)


def test_negacyclic_birthday_tiny():
    # n = 4, m = 6, q = 17: 2^24 inputs and 17^4 (about 2^16.3) outputs.
    rng = random.Random(4)
    key = random_key(4, 6, 17, rng)
    z, w = birthday_collision(key, 17, -1, rng)
    assert is_ring_sis_solution(key, difference(z, w), 17, -1)


def test_ring_hash_is_sis_with_rotation_matrix():
    rng = random.Random(5)
    for sign in (-1, +1):
        n, m, q = 8, 3, 97
        key = random_key(n, m, q, rng)
        A = as_sis_matrix(key, q, sign)
        for _ in range(500 // 2):
            z = random_input(n, m, rng)
            flat = [c for p in z for c in p]
            want = tuple(sum(x * y for x, y in zip(row, flat)) % q for row in A)
            assert ring_hash(key, z, q, sign) == want
