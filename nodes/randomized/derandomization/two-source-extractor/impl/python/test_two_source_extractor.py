# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-source-extractor/. The authors are listed in prov/20AZMB.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from two_source_extractor import (
    bias,
    bound_squared,
    collision,
    flat,
    ip,
    rectangle_sum,
    sign,
    strong_bias,
    worst_flat_bias,
)


def test_inner_product() -> None:
    assert ip(0b101, 0b111) == 0
    assert ip(0b101, 0b100) == 1
    assert sign(0b11, 0b01) == -1


def test_hadamard_rows_are_orthogonal() -> None:
    for n in range(1, 5):
        size = 1 << n
        for x in range(size):
            for x2 in range(size):
                dot = sum(sign(x, y) * sign(x2, y) for y in range(size))
                assert dot == (size if x == x2 else 0)


def test_lindsey_lemma_all_rectangles_n3() -> None:
    n, size = 3, 8
    subsets = [s for r in range(1, size + 1) for s in combinations(range(size), r)]
    for a in subsets:
        for b in subsets:
            s = rectangle_sum(a, b)
            assert s * s <= len(a) * len(b) * size


def test_exact_worst_bias_n3() -> None:
    v, a, b = worst_flat_bias(3, 2, 2)
    assert v == Fraction(5, 8)
    assert v * v <= bound_squared(3, 2, 2)
    assert bias(flat((0, 1, 2, 4)), flat((0, 1, 2, 4))) == Fraction(5, 8)
    v, a, b = worst_flat_bias(3, 2, 1)
    assert v == 1 and v * v == bound_squared(3, 2, 1)
    assert bias(flat((0, 1, 2, 3)), flat((0, 4))) == 1
    v, _, _ = worst_flat_bias(3, 1, 1)
    assert v == 1 and v * v < bound_squared(3, 1, 1)
    v, _, _ = worst_flat_bias(3, 3, 1)
    assert v == Fraction(1, 2) and v * v < bound_squared(3, 3, 1)


def test_tight_example_half_entropy() -> None:
    for n in (2, 4, 6):
        h = n // 2
        xs = [a for a in range(1 << h)]  # (a, 0): the low half varies
        ys = [b << h for b in range(1 << h)]  # (0, b): the high half varies
        assert bias(flat(xs), flat(ys)) == 1
        assert bound_squared(n, h, h) == 1


def test_bound_on_sampled_flat_sources_n4() -> None:
    rng = random.Random(1)
    n = 4
    for _ in range(400):
        k1 = rng.randrange(0, n + 1)
        k2 = rng.randrange(0, n + 1)
        a = rng.sample(range(1 << n), 1 << k1)
        b = rng.sample(range(1 << n), 1 << k2)
        v = bias(flat(a), flat(b))
        assert v * v <= bound_squared(n, k1, k2)


def test_bound_for_general_sources() -> None:
    # bias <= sqrt(N) ||p||_2 ||q||_2, and the same holds when Y is revealed.
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randrange(1, 5)
        size = 1 << n
        wp = [rng.randrange(0, 4) for _ in range(size)]
        wq = [rng.randrange(0, 4) for _ in range(size)]
        if not sum(wp) or not sum(wq):
            continue
        p = {x: Fraction(w, sum(wp)) for x, w in enumerate(wp) if w}
        q = {y: Fraction(w, sum(wq)) for y, w in enumerate(wq) if w}
        b = bias(p, q)
        sb = strong_bias(p, q)
        assert b <= sb
        assert b * b <= size * collision(p) * collision(q)
        assert sb * sb <= size * collision(p) * max(q.values())


def test_no_large_monochromatic_rectangle() -> None:
    # Error below 1/2 means IP is not constant on any 4 x 4 rectangle of the 8 x 8 matrix.
    for a in combinations(range(8), 4):
        for b in combinations(range(8), 4):
            values = {ip(x, y) for x in a for y in b}
            assert values == {0, 1}
