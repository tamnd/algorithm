# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dot-product-hashing/. The authors are listed in prov/2WYWCR.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from dot_product_hashing import (
    DotProductHashTable,
    affine_dot_product_hash,
    dot_product_hash,
    draw_affine_dot_product_hash,
    draw_dot_product_hash,
    key_digits,
)


def test_worked_example() -> None:
    p, r = 7, 3
    assert key_digits(123, p, r) == [4, 3, 2]
    assert key_digits(124, p, r) == [5, 3, 2]
    a = [3, 5, 1]
    assert dot_product_hash(a, key_digits(123, p, r), p) == 1
    assert dot_product_hash(a, key_digits(124, p, r), p) == 4
    # the keys 7, 14, ..., 70 all have x mod 7 = 0, but a spreads them
    slots = [dot_product_hash(a, key_digits(7 * i, p, r), p) for i in range(1, 11)]
    assert slots == [5, 3, 1, 6, 4, 2, 1, 6, 4, 2]
    # 123 and 124 collide exactly for the 49 vectors with a_0 = 0
    hits = sum(
        1
        for v in product(range(p), repeat=r)
        if dot_product_hash(v, key_digits(123, p, r), p) == dot_product_hash(v, key_digits(124, p, r), p)
    )
    assert hits == 49


@pytest.mark.parametrize("p,r", [(2, 1), (2, 3), (3, 2), (5, 2), (7, 2), (3, 3)])
def test_universal_exactly(p: int, r: int) -> None:
    keys = list(product(range(p), repeat=r))
    vectors = list(product(range(p), repeat=r))
    for x in keys:
        for y in keys:
            if x == y:
                continue
            hits = sum(1 for a in vectors if dot_product_hash(a, x, p) == dot_product_hash(a, y, p))
            assert Fraction(hits, len(vectors)) == Fraction(1, p)


@pytest.mark.parametrize("p,r", [(2, 2), (3, 2), (5, 1), (3, 3)])
def test_affine_variant_strongly_universal_exactly(p: int, r: int) -> None:
    keys = list(product(range(p), repeat=r))
    funcs = [(a, b) for a in product(range(p), repeat=r) for b in range(p)]
    for x in keys:
        for y in keys:
            if x == y:
                continue
            counts: dict[tuple[int, int], int] = {}
            for a, b in funcs:
                key = (affine_dot_product_hash(a, b, x, p), affine_dot_product_hash(a, b, y, p))
                counts[key] = counts.get(key, 0) + 1
            assert len(counts) == p * p
            assert set(counts.values()) == {len(funcs) // (p * p)}


def test_affine_variant_not_3_wise() -> None:
    p = 5
    x, y = (1, 3), (4, 0)
    z = tuple((2 * xi - yi) % p for xi, yi in zip(x, y))
    for a in product(range(p), repeat=2):
        for b in range(p):
            hx, hy, hz = (affine_dot_product_hash(a, b, k, p) for k in (x, y, z))
            assert hz == (2 * hx - hy) % p


def test_plain_family_is_not_uniform_on_zero() -> None:
    # without the offset b, the zero key always goes to slot 0
    rng = random.Random(1)
    for _ in range(20):
        a = draw_dot_product_hash(5, 3, rng)
        assert dot_product_hash(a, [0, 0, 0], 5) == 0


def test_composite_modulus_fails() -> None:
    q = 4  # not a prime: the keys 0 and 2 collide when 2a = 0 mod 4, for a in {0, 2}
    hits = sum(1 for a in range(q) if dot_product_hash([a], [0], q) == dot_product_hash([a], [2], q))
    assert Fraction(hits, q) == Fraction(1, 2)


def test_exact_collision_count_on_bad_keys() -> None:
    # 40 keys that all collide under x mod 13. Over all 13^3 vectors a, the
    # number of colliding pairs has mean exactly C(40, 2) / 13 = 60, but the
    # vectors with a_1 = a_2 = 0 still put every key in slot 0.
    p, r = 13, 3
    keys = [key_digits(p * i, p, r) for i in range(1, 41)]
    total = 0
    worst = 0
    for a in product(range(p), repeat=r):
        loads = [0] * p
        for k in keys:
            loads[dot_product_hash(a, k, p)] += 1
        pairs = sum(c * (c - 1) // 2 for c in loads)
        total += pairs
        worst = max(worst, pairs)
    assert Fraction(total, p**r) == 60
    assert worst == 780


def test_table_and_errors() -> None:
    rng = random.Random(3)
    t = DotProductHashTable(11, 3, rng)
    keys = rng.sample(range(11**3), 40)
    for k in keys:
        t.insert(k)
    assert all(t.contains(k) for k in keys)
    assert sum(len(c) for c in t.slots) == 40
    with pytest.raises(ValueError):
        key_digits(11**3, 11, 3)
    with pytest.raises(ValueError):
        dot_product_hash([1, 2], [1], 11)
    a, b = draw_affine_dot_product_hash(5, 2, rng)
    assert 0 <= affine_dot_product_hash(a, b, [1, 4], 5) < 5
