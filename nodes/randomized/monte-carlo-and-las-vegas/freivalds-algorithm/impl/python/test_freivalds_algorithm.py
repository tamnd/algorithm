# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/freivalds-algorithm/. The authors are listed in prov/Z43DEG.jsonl.

import itertools
import random
from fractions import Fraction

from freivalds_algorithm import detects, freivalds, mat_mul, mat_vec, miss_probability

A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
AB = [[30, 24, 18], [84, 69, 54], [138, 114, 90]]


def wrong_c() -> list[list[int]]:
    c = [row[:] for row in AB]
    c[1][2] = 55
    return c


def test_example_product() -> None:
    assert mat_mul(A, B) == AB


def test_example_trace() -> None:
    c = wrong_c()
    assert mat_vec(B, (1, 0, 1)) == [16, 10, 4]
    assert mat_vec(A, [16, 10, 4]) == [48, 138, 228]
    assert mat_vec(c, (1, 0, 1)) == [48, 139, 228]
    assert detects(A, B, c, (1, 0, 1))
    assert not detects(A, B, c, (1, 1, 0))
    detecting = [r for r in itertools.product((0, 1), repeat=3) if detects(A, B, c, r)]
    assert detecting == [r for r in itertools.product((0, 1), repeat=3) if r[2] == 1]
    assert miss_probability(A, B, c) == Fraction(1, 2)


def test_correct_product_always_accepted() -> None:
    rng = random.Random(11)
    for _ in range(200):
        n, m, p = rng.randint(1, 5), rng.randint(1, 5), rng.randint(1, 5)
        a = [[rng.randint(-9, 9) for _ in range(m)] for _ in range(n)]
        b = [[rng.randint(-9, 9) for _ in range(p)] for _ in range(m)]
        assert freivalds(a, b, mat_mul(a, b), 5, rng)
        assert miss_probability(a, b, mat_mul(a, b)) == 1


def test_exact_bound_all_2x2_errors() -> None:
    # Every nonzero D with entries in {-2..2}: C = A B - D is missed by at most half of {0,1}^2.
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    ab = mat_mul(a, b)
    worst = Fraction(0)
    for entries in itertools.product(range(-2, 3), repeat=4):
        if not any(entries):
            continue
        d = [entries[0:2], entries[2:4]]
        c = [[ab[i][j] - d[i][j] for j in range(2)] for i in range(2)]
        q = miss_probability(a, b, c)
        assert q <= Fraction(1, 2)
        worst = max(worst, q)
    assert worst == Fraction(1, 2)


def test_exact_bound_random_errors_n4() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = 4
        a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        b = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        c = mat_mul(a, b)
        for _ in range(rng.randint(1, 3)):
            c[rng.randrange(n)][rng.randrange(n)] += rng.choice((-2, -1, 1, 2))
        if c == mat_mul(a, b):
            continue
        assert miss_probability(a, b, c) <= Fraction(1, 2)


def test_bound_one_over_s_in_a_field() -> None:
    # Over F_7 with r uniform on S^3, the miss probability is at most 1/|S|.
    q = 7
    rng = random.Random(3)
    for _ in range(100):
        a = [[rng.randrange(q) for _ in range(3)] for _ in range(3)]
        b = [[rng.randrange(q) for _ in range(3)] for _ in range(3)]
        c = mat_mul(a, b, q)
        c[rng.randrange(3)][rng.randrange(3)] = (c[0][0] + rng.randrange(1, q)) % q
        if c == mat_mul(a, b, q):
            continue
        for s in ((0, 1, 2), (1, 2, 3, 4, 5), tuple(range(q))):
            assert miss_probability(a, b, c, s, q) <= Fraction(1, len(s))


def test_ring_with_zero_divisors() -> None:
    # Over Z/2^64, D = [[2^63]] kills every even r: the 1/|S| bound fails,
    # but the {0,1} bound 1/2 still holds.
    mod = 2**64
    a, b = [[1]], [[0]]
    c = [[mod - 2**63]]  # A B - C = 2^63
    assert miss_probability(a, b, c, (0, 1, 2, 3), mod) == Fraction(1, 2)
    assert miss_probability(a, b, c, (0, 1), mod) == Fraction(1, 2)


def test_false_accept_rate() -> None:
    c = wrong_c()
    rng = random.Random(2024)
    trials = 4000
    accepted = sum(freivalds(A, B, c, 1, rng) for _ in range(trials))
    assert abs(accepted / trials - 0.5) < 0.04
    accepted3 = sum(freivalds(A, B, c, 3, rng) for _ in range(trials))
    assert abs(accepted3 / trials - 0.125) < 0.03


def test_rectangular() -> None:
    rng = random.Random(9)
    a = [[rng.randint(0, 5) for _ in range(4)] for _ in range(2)]
    b = [[rng.randint(0, 5) for _ in range(3)] for _ in range(4)]
    c = mat_mul(a, b)
    assert freivalds(a, b, c, 10, rng)
    c[1][0] += 1
    assert miss_probability(a, b, c) == Fraction(1, 2)
    assert not freivalds(a, b, c, 40, rng)
