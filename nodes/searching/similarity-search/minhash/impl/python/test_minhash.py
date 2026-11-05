# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minhash/. The authors are listed in prov/4BV5E4.jsonl.

import itertools
import math
import random
from fractions import Fraction

from minhash import estimate_jaccard, jaccard, make_hashes, minhash_signature


def linear(a: int, b: int):
    return lambda x: (a * x + b) % 7


def test_example() -> None:
    hs = [linear(a, b) for a, b in [(1, 1), (3, 1), (2, 5), (5, 2), (4, 3), (6, 0)]]
    sa = minhash_signature({0, 1, 2, 3}, hs)
    sb = minhash_signature({2, 3, 4}, hs)
    assert sa == [1, 0, 0, 0, 0, 0]
    assert sb == [3, 0, 2, 1, 1, 3]
    assert estimate_jaccard(sa, sb) == 1 / 6


def test_all_permutations_give_exact_jaccard() -> None:
    a, b = {0, 1, 2, 3}, {2, 3, 4}
    perms = list(itertools.permutations(range(7)))
    hs = [(lambda p: (lambda x: p[x]))(p) for p in perms]
    est = estimate_jaccard(minhash_signature(a, hs), minhash_signature(b, hs))
    assert Fraction(est).limit_denominator(10) == Fraction(2, 5)
    assert len(perms) == 5040


def test_edges() -> None:
    hs = make_hashes(8, seed=1)
    empty = minhash_signature([], hs)
    assert empty == [math.inf] * 8
    assert estimate_jaccard(empty, empty) == 1.0
    one = minhash_signature(["x"], hs)
    assert estimate_jaccard(one, empty) == 0.0
    assert estimate_jaccard(one, minhash_signature(["x", "x"], hs)) == 1.0
    s = minhash_signature(range(10), hs)
    assert estimate_jaccard(s, minhash_signature(range(10, 20), hs)) == 0.0


def test_merge_is_union() -> None:
    hs = make_hashes(16, seed=5)
    a, b = set(range(0, 30)), set(range(20, 50))
    merged = [min(x, y) for x, y in zip(minhash_signature(a, hs), minhash_signature(b, hs))]
    assert merged == minhash_signature(a | b, hs)


def test_random_against_exact() -> None:
    rng = random.Random(4041)
    k = 400
    hs = make_hashes(k, seed=7)
    for _ in range(500):
        u = rng.randint(1, 40)
        a = {x for x in range(u) if rng.random() < 0.5}
        b = {x for x in range(u) if rng.random() < 0.5}
        est = estimate_jaccard(minhash_signature(a, hs), minhash_signature(b, hs))
        # Hoeffding: the chance of an error of 0.15 with k = 400 is below 2 e^{-18}.
        assert abs(est - jaccard(a, b)) < 0.15
