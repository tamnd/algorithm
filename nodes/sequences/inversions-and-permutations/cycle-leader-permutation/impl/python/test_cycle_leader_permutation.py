# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cycle-leader-permutation/. The authors are listed in prov/J8DYW4.jsonl.

import itertools
import math
import random
from fractions import Fraction

from cycle_leader_permutation import apply_permutation, apply_permutation_readonly, leader_reads


def brute(a: list, p: list[int]) -> list:
    b = [None] * len(a)
    for i, x in enumerate(a):
        b[p[i]] = x
    return b


def test_example() -> None:
    p = [2, 5, 3, 0, 4, 1]  # 3 6 4 1 5 2 in 1-based form
    a = list("ABCDEF")
    assert apply_permutation(a, p) == list("DFACEB")
    assert p == [2, 5, 3, 0, 4, 1]
    a = list("ABCDEF")
    assert apply_permutation_readonly(a, p) == list("DFACEB")
    assert leader_reads(p) == 10


def test_edges() -> None:
    assert apply_permutation([], []) == []
    assert apply_permutation_readonly([], []) == []
    assert apply_permutation([7], [0]) == [7]
    assert apply_permutation([1, 2, 3], [0, 1, 2]) == [1, 2, 3]
    assert apply_permutation([1, 2, 3], [2, 1, 0]) == [3, 2, 1]
    assert apply_permutation(["x", "x", "y"], [1, 2, 0]) == ["y", "x", "x"]
    try:
        apply_permutation([1, 2], [0])
    except ValueError:
        pass
    else:
        raise AssertionError


def test_scatter_not_gather() -> None:
    p = [1, 2, 0]
    assert apply_permutation(list("abc"), p) == ["c", "a", "b"]


def test_exhaustive_small() -> None:
    for n in range(7):
        a0 = list(range(100, 100 + n))
        for q in itertools.permutations(range(n)):
            p = list(q)
            want = brute(a0, p)
            assert apply_permutation(list(a0), p) == want
            assert p == list(q)
            assert apply_permutation_readonly(list(a0), p) == want


def test_leader_cost() -> None:
    for n in range(1, 8):
        h = sum(Fraction(1, k) for k in range(1, n + 1))
        reads = [leader_reads(list(q)) for q in itertools.permutations(range(n))]
        assert Fraction(sum(reads), math.factorial(n)) == (n + 1) * h - n
        assert max(reads) == n * (n + 1) // 2
        assert leader_reads([(i + 1) % n for i in range(n)]) == n * (n + 1) // 2


def test_random() -> None:
    rng = random.Random(8803)
    for _ in range(600):
        n = rng.randint(0, 60)
        p = list(range(n))
        rng.shuffle(p)
        a = [rng.randint(-5, 5) for _ in range(n)]
        want = brute(a, p)
        q = list(p)
        assert apply_permutation(list(a), q) == want
        assert q == p
        assert apply_permutation_readonly(list(a), p) == want
